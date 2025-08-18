import os
import streamlit as st
from pathlib import Path

PALETTE = {"bg": "#F0F0F0", "green": "#204030", "gold": "#C09030"}
ALL_LANGS = {"en": "English", "is": "Íslenska", "fr": "Français", "es": "Español"}

def inject_theme():
    st.markdown(f"""
    <style>
    :root {{
      --gh-bg: {PALETTE["bg"]};
      --gh-green: {PALETTE["green"]};
      --gh-gold: {PALETTE["gold"]};
    }}
    html, body, .block-container {{ background: var(--gh-bg); }}
    .block-container {{ padding-top:.5rem; }}
    .gh-header {{ display:flex;justify-content:space-between;align-items:center;
      border-bottom:1px solid #e6e6e6;padding:.6rem 0;margin-bottom:.6rem; }}
    .badge {{ display:inline-flex;gap:.35rem;background:#fff;border:1px solid #e6e6e6;
      color:var(--gh-green);padding:.2rem .55rem;border-radius:999px;font-size:.8rem; }}
    .section {{ background:#fff;border:1px solid #eaeaea;border-radius:12px;padding:.8rem; }}
    </style>
    """, unsafe_allow_html=True)

def topbar(title="🌿 Green Hill Cockpit"):
    allowed = [c.strip() for c in os.getenv("ALLOWED_LANGUAGES", "en,is,fr,es").split(",") if c.strip() in ALL_LANGS]
    if not allowed:
        allowed = list(ALL_LANGS.keys())
    default_code = os.getenv("DEFAULT_LANGUAGE", allowed[0])
    options = [(ALL_LANGS[c], c) for c in allowed]
    labels = [label for label, _ in options]
    default_index = next((i for i, (_, code) in enumerate(options) if code == default_code), 0)
    choice = st.selectbox("🌐 Language", labels, index=default_index, key="lang_select")
    # map label back to code
    code = options[labels.index(choice)][1]
    st.session_state["lang"] = code
    st.markdown(
        f"""
        <div class='gh-header'>
          <div style='display:flex;align-items:center;gap:.6rem'>
            <h2 style='margin:0;color:{PALETTE["green"]}'>{title}</h2>
            <span class='badge'>Palette {PALETTE["green"]} / {PALETTE["gold"]}</span>
          </div>
        </div>
        """, unsafe_allow_html=True)

def section_header(icon_path: str | None, title: str, width: int = 36):
    cols = st.columns([0.08,0.92])
    with cols[0]:
        if icon_path and Path(icon_path).exists():
            st.image(icon_path, width=width)
        else:
            st.markdown("🌿")  # fallback emoji avoids crash
    with cols[1]:
        st.subheader(title)
