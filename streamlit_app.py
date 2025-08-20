"""
Green Hill Executive Cockpit - Multi-language with full features
Single entry point for Streamlit Cloud deployment
"""

import streamlit as st
import os
import requests
import json
import re
from datetime import datetime
from typing import Dict, Any, Optional, Tuple, List
import time




# Agent configurations
AGENTS = {
    "ghc_dt": "CEO Digital Twin",
    "strategy": "Strategy Advisor",
    "finance": "Finance Advisor",
    "operations": "Operations Advisor", 
    "market": "Market Advisor",
    "risk": "Risk Advisor",
    "compliance": "Compliance Advisor",
    "innovation": "Innovation Advisor",
    "code": "Code Assistant"
}

# Agent configurations
AGENTS = {
    "ghc_dt": "CEO Digital Twin",
    "strategy": "Strategy Advisor",
    "finance": "Finance Advisor",
    "operations": "Operations Advisor", 
    "market": "Market Advisor",
    "risk": "Risk Advisor",
    "compliance": "Compliance Advisor",
    "innovation": "Innovation Advisor",
    "code": "Code Assistant"
}

# Agent configurations
AGENTS = {
    "ghc_dt": "CEO Digital Twin",
    "strategy": "Strategy Advisor",
    "finance": "Finance Advisor",
    "operations": "Operations Advisor", 
    "market": "Market Advisor",
    "risk": "Risk Advisor",
    "compliance": "Compliance Advisor",
    "innovation": "Innovation Advisor",
    "code": "Code Assistant"
}

# Page config
st.set_page_config(
    page_title="Green Hill Cockpit",
    page_icon="🌿",
    layout="wide"
)

# Language translations
LANG = {
    "en": {
        "title": "Green Hill Cockpit",
        "subtitle": "Executive intelligence for Green Hill Canarias",
        "tabs": ["💬 Chat", "📥 Ingest", "📚 Evidence", "🏛️ Governance", "🔍 Diagnostics", "🧑‍💻 Code"],
        "select_agent": "Select agent",
        "ask": "Your question",
        "send": "Send",
        "consult_all": "Consult All Agents",
        "ingest_title": "Ingest Knowledge (per agent & global)",
        "upload_files": "Upload files",
        "paste_text": "Paste text",
        "add_url": "Add URL",
        "ingest_btn": "Ingest",
        "evidence_title": "Evidence Log",
        "governance_title": "Governance State",
        "diagnostics_title": "Diagnostics",
        "test_langgraph": "Test LangGraph",
        "test_openai": "Test OpenAI",
        "code_title": "Code Agent",
        "shareholder_intro": "Welcome — this cockpit showcases our agents and executive workflows.",
        "select_language": "Select Language",
        "phase": "Phase",
        "zec_rate": "ZEC Tax Rate",
        "cash_buffer": "Cash Buffer Target"
    },
    "es": {
        "title": "Cockpit de Green Hill",
        "subtitle": "Inteligencia ejecutiva para Green Hill Canarias",
        "tabs": ["💬 Chat", "📥 Ingesta", "📚 Evidencia", "🏛️ Gobernanza", "🔍 Diagnóstico", "🧑‍💻 Código"],
        "select_agent": "Selecciona agente",
        "ask": "Tu pregunta",
        "send": "Enviar",
        "consult_all": "Consultar a Todos",
        "ingest_title": "Ingesta de Conocimiento (por agente y global)",
        "upload_files": "Subir archivos",
        "paste_text": "Pegar texto",
        "add_url": "Añadir URL",
        "ingest_btn": "Ingerir",
        "evidence_title": "Registro de Evidencia",
        "governance_title": "Estado de Gobernanza",
        "diagnostics_title": "Diagnósticos",
        "test_langgraph": "Probar LangGraph",
        "test_openai": "Probar OpenAI",
        "code_title": "Agente de Código",
        "shareholder_intro": "Bienvenidos — este cockpit presenta nuestros agentes y flujos ejecutivos.",
        "select_language": "Seleccionar Idioma",
        "phase": "Fase",
        "zec_rate": "Tasa ZEC",
        "cash_buffer": "Objetivo Buffer Efectivo"
    },
    "is": {
        "title": "Green Hill stjórnborð",
        "subtitle": "Framkvæmdagreind fyrir Green Hill Canarias",
        "tabs": ["💬 Spjall", "📥 Inntaka", "📚 Sannanir", "🏛️ Stjórnsýsla", "🔍 Greining", "🧑‍💻 Kóði"],
        "select_agent": "Veldu umboðsmann",
        "ask": "Spurning þín",
        "send": "Senda",
        "consult_all": "Ráðfæra við alla",
        "ingest_title": "Þekkingarinntaka (eftir umboðsmanni og alþjóðleg)",
        "upload_files": "Hlaða upp skjölum",
        "paste_text": "Líma texta",
        "add_url": "Bæta við veffangi",
        "ingest_btn": "Inntaka",
        "evidence_title": "Sönnunarskrá",
        "governance_title": "Stjórnsýslustaða",
        "diagnostics_title": "Greining",
        "test_langgraph": "Prófa LangGraph",
        "test_openai": "Prófa OpenAI",
        "code_title": "Kóða-umboðsmaður",
        "shareholder_intro": "Velkomin — þetta stjórnborð sýnir umboðsmennina okkar og stjórnunarferli.",
        "select_language": "Velja Tungumál",
        "phase": "Áfangi",
        "zec_rate": "ZEC Skatthlutfall",
        "cash_buffer": "Reiðufé Markmið"
    },
    "fr": {
        "title": "Cockpit Green Hill",
        "subtitle": "Intelligence exécutive pour Green Hill Canarias",
        "tabs": ["💬 Chat", "📥 Ingestion", "📚 Évidence", "🏛️ Gouvernance", "🔍 Diagnostics", "🧑‍�� Code"],
        "select_agent": "Sélectionner un agent",
        "ask": "Votre question",
        "send": "Envoyer",
        "consult_all": "Consulter tous",
        "ingest_title": "Ingestion de Connaissances (par agent & globale)",
        "upload_files": "Téléverser des fichiers",
        "paste_text": "Coller du texte",
        "add_url": "Ajouter une URL",
        "ingest_btn": "Ingestion",
        "evidence_title": "Journal d'Évidence",
        "governance_title": "État de Gouvernance",
        "diagnostics_title": "Diagnostics",
        "test_langgraph": "Tester LangGraph",
        "test_openai": "Tester OpenAI",
        "code_title": "Agent Code",
        "shareholder_intro": "Bienvenue — ce cockpit présente nos agents et flux exécutifs.",
        "select_language": "Choisir la Langue",
        "phase": "Phase",
        "zec_rate": "Taux ZEC",
        "cash_buffer": "Objectif Trésorerie"
    }
}

# Environment setup - bridge st.secrets to os.environ
def setup_environment():
    """Bridge Streamlit secrets to environment variables"""
    secret_keys = ["LANGGRAPH_API_URL", "LANGGRAPH_API_KEY", "OPENAI_API_KEY", 
                   "DEMO_MODE", "GHC_DT_MODEL", "GHC_DT_TEMPERATURE", "GHC_DT_EVIDENCE_LOG"]
    
    for key in secret_keys:
        try:
            if key in st.secrets:
                os.environ[key] = st.secrets[key]
        except:
            pass  # Use existing env var or default
def load_state(): -> Dict[str, Any]:
    """Load system state from file"""
    default_state = {
        "phase": "Phase 1: Pre-Operational Setup",
        "zec_rate": 4,
        "cash_buffer_to": "2026-06-30",
        "key_dates": {
            "phase1_start": "2025-01-01",
            "phase2_start": "2025-07-01",
            "phase3_start": "2026-01-01"
        }
    }
    
    try:
        if os.path.exists(STATE_FILE):
            with open(STATE_FILE, 'r') as f:
                return json.load(f)
    except:
        pass
    
    return default_state

def save_state(state: Dict[str, Any]):
    """Save system state to file"""
    try:
        with open(STATE_FILE, 'w') as f:
            json.dump(state, f, indent=2)
    except Exception as e:
        st.error(f"Failed to save state: {e}")

def log_evidence(entry: Dict[str, Any]):
    """Append to evidence log"""
    try:
        with open(EVIDENCE_FILE, 'a') as f:
            f.write(json.dumps(entry) + '\n')
    except Exception as e:
        st.error(f"Failed to log evidence: {e}")

# API communication functions
def call_langgraph(question: str, command: Optional[str], agent: str, state: Dict[str, Any]) -> Dict[str, Any]:
    """Call LangGraph API"""
    headers = {"Content-Type": "application/json"}
    
    if LANGGRAPH_API_KEY:
        headers["Authorization"] = f"Bearer {LANGGRAPH_API_KEY}"
    
    payload = {
        "question": question,
        "command": command,
        "agent": agent,
        "state": state
    }
    
    try:
        response = requests.post(
            f"{LANGGRAPH_API_URL}/invoke",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            return {
                "status": "error",
                "message": f"API returned {response.status_code}: {response.text[:200]}"
            }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Connection error: {str(e)}"
        }

def test_langgraph_connection(): -> bool:
    """Test LangGraph API connection"""
    try:
        headers = {}
        if LANGGRAPH_API_KEY:
            headers["Authorization"] = f"Bearer {LANGGRAPH_API_KEY}"
            
        response = requests.get(
            f"{LANGGRAPH_API_URL}/health",
            headers=headers,
            timeout=5
        )
        return response.status_code == 200
    except:
        return False

def test_openai_connection(): -> bool:
    """Test OpenAI API connection"""
    if not OPENAI_API_KEY:
        return False
    
    try:
        from openai import OpenAI
        client = OpenAI(api_key=OPENAI_API_KEY)
        models = client.models.list()
        return True
    except:
        return False

# Initialize session state
if 'lang' not in st.session_state:
    st.session_state.lang = None

if 'state' not in st.session_state:
    st.session_state.state = load_state()

if 'messages' not in st.session_state:
    st.session_state.messages = []

# Language selection (first screen)
if st.session_state.lang is None:
    st.markdown("# 🌿 Green Hill Cockpit")
    st.markdown("### Select Language / Seleccionar Idioma / Velja Tungumál / Choisir la Langue")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🇬🇧 English", use_container_width=True):
            st.session_state.lang = "en"
            st.rerun()
    
    with col2:
        if st.button("🇪🇸 Español", use_container_width=True):
            st.session_state.lang = "es"
            st.rerun()
    
    with col3:
        if st.button("🇮🇸 Íslenska", use_container_width=True):
            st.session_state.lang = "is"
            st.rerun()
    
    with col4:
        if st.button("🇫🇷 Français", use_container_width=True):
            st.session_state.lang = "fr"
            st.rerun()
    
    st.stop()

# Get current language strings
L = LANG[st.session_state.lang]

# Initialize session state
if 'lang' not in st.session_state:
    st.session_state.lang = None

if 'state' not in st.session_state:
    st.session_state.state = load_state()

if 'messages' not in st.session_state:
    st.session_state.messages = []

# Language selection (first screen)
if st.session_state.lang is None:
    st.markdown("# 🌿 Green Hill Cockpit")
    st.markdown("### Select Language / Seleccionar Idioma / Velja Tungumál / Choisir la Langue")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🇬🇧 English", use_container_width=True):
            st.session_state.lang = "en"
            st.rerun()
    
    with col2:
        if st.button("🇪🇸 Español", use_container_width=True):
            st.session_state.lang = "es"
            st.rerun()
    
    with col3:
        if st.button("🇮🇸 Íslenska", use_container_width=True):
            st.session_state.lang = "is"
            st.rerun()
    
    with col4:
        if st.button("🇫🇷 Français", use_container_width=True):
            st.session_state.lang = "fr"
            st.rerun()
    
    st.stop()

# Get current language strings
L = LANG[st.session_state.lang]

# Main UI
st.title(f"🌿 {L['title']}")
st.caption(L['subtitle'])

# Sidebar
with st.sidebar:
    st.header(L['select_agent'])
    
    # Agent selector
    selected_agent_display = st.selectbox(
        "",
        options=list(AGENTS.keys()),
        label_visibility="collapsed"
    )
    selected_agent = AGENTS[selected_agent_display]
    
    # Command selector
    selected_command = st.selectbox(
        "Command:",
        options=["Auto"] + list(COMMANDS.keys())
    )
    if selected_command == "Auto":
        selected_command = None
    
    # State display
    with st.expander(L['governance_title'], expanded=False):
        st.write(f"**{L['phase']}:** {st.session_state.state.get('phase')}")
        st.write(f"**{L['zec_rate']}:** {st.session_state.state.get('zec_rate')}%")
        st.write(f"**{L['cash_buffer']}:** {st.session_state.state.get('cash_buffer_to')}")
    
    # Language switcher
    if st.button("🌐 " + L['select_language']):
        st.session_state.lang = None
        st.rerun()

# Create tabs
tabs = st.tabs(L['tabs'])

# Chat tab
with tabs[0]:
    # Show shareholder intro on first visit
    if len(st.session_state.messages) == 0:
        st.info(L['shareholder_intro'])
    
    # Display messages
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
            if "agent" in msg:
                st.caption(f"Agent: {msg['agent']}")
    
    # Chat input
    query = st.chat_input(L['ask'])
    
    if query:
        # Add user message
        st.session_state.messages.append({"role": "user", "content": query})
        
        with st.chat_message("user"):
            st.write(query)
        
        # Call API
        with st.spinner("..."):
            result = call_langgraph(query, selected_command, selected_agent, st.session_state.state)
        
        # Process response
        if result.get("status") == "error":
            st.error(f"Error: {result.get('message')}")
        else:
            answer = result.get("answer", "No response")
            agent_used = result.get("meta", {}).get("agent", selected_agent)
            
            # Add assistant message
            st.session_state.messages.append({
                "role": "assistant",
                "content": answer,
                "agent": agent_used
            })
            
            with st.chat_message("assistant"):
                st.write(answer)
                st.caption(f"Agent: {agent_used}")
            
            # Log evidence
            evidence_entry = {
                "timestamp": datetime.utcnow().isoformat(),
                "query": query,
                "agent": agent_used,
                "command": selected_command,
                "answer": answer,
                "state": st.session_state.state
            }
            log_evidence(evidence_entry)
    
    # Consult all button
    if st.button(L['consult_all']):
        query = st.session_state.messages[-1]["content"] if st.session_state.messages else "Status report"
        for agent_name, agent_key in AGENTS.items():
            with st.spinner(f"Consulting {agent_name}..."):
                result = call_langgraph(query, None, agent_key, st.session_state.state)
                if result.get("status") != "error":
                    st.write(f"**{agent_name}:**")
                    st.write(result.get("answer", "No response"))
                    st.divider()

# Ingest tab
with tabs[1]:
    st.header(L['ingest_title'])
    
    agent_for_ingest = st.selectbox("Target agent:", ["Global"] + list(AGENTS.keys()))
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        uploaded_file = st.file_uploader(L['upload_files'], type=['txt', 'pdf', 'docx'])
        if uploaded_file and st.button("Upload", key="upload_btn"):
            st.success(f"File uploaded for {agent_for_ingest}")
    
    with col2:
        text_input = st.text_area(L['paste_text'])
        if text_input and st.button(L['ingest_btn'], key="text_btn"):
            st.success(f"Text ingested for {agent_for_ingest}")
    
    with col3:
        url_input = st.text_input(L['add_url'])
        if url_input and st.button("Add URL", key="url_btn"):
            st.success(f"URL added for {agent_for_ingest}")

# Evidence tab
with tabs[2]:
    st.header(L['evidence_title'])
    
    try:
        if os.path.exists(EVIDENCE_FILE):
            with open(EVIDENCE_FILE, 'r') as f:
                lines = f.readlines()
                if lines:
                    for line in reversed(lines[-10:]):
                        entry = json.loads(line)
                        with st.expander(f"{entry['timestamp']} - {entry['agent']}"):
                            st.write(f"**Query:** {entry['query']}")
                            st.write(f"**Answer:** {entry['answer'][:500]}...")
                else:
                    st.info("No evidence logged yet")
        else:
            st.info("Evidence file not found")
    except Exception as e:
        st.error(f"Error loading evidence: {e}")

# Governance tab
with tabs[3]:
    st.header(L['governance_title'])
    
    col1, col2 = st.columns(2)
    
    with col1:
        new_phase = st.selectbox(L['phase'], [
            "Phase 1: Pre-Operational Setup",
            "Phase 2: Initial Operations",
            "Phase 3: Full Operations"
        ])
        
        if st.button("Update Phase"):
            st.session_state.state["phase"] = new_phase
            save_state(st.session_state.state)
            st.success("Phase updated")
            st.rerun()
    
    with col2:
        new_zec = st.number_input(L['zec_rate'], value=st.session_state.state.get("zec_rate", 4), min_value=0, max_value=100)
        
        if st.button("Update ZEC Rate"):
            st.session_state.state["zec_rate"] = new_zec
            save_state(st.session_state.state)
            st.success("ZEC rate updated")

# Diagnostics tab
with tabs[4]:
    st.header(L['diagnostics_title'])
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button(L['test_langgraph']):
            with st.spinner("Testing..."):
                if test_langgraph_connection():
                    st.success("✅ LangGraph API is accessible")
                else:
                    st.error("❌ Cannot connect to LangGraph API")
    
    with col2:
        if st.button(L['test_openai']):
            with st.spinner("Testing..."):
                if test_openai_connection():
                    st.success("✅ OpenAI API is configured")
                else:
                    st.error("❌ OpenAI API not accessible")
    
    # Show configuration
    st.subheader("Configuration")
    config_data = {
        "LANGGRAPH_API_URL": LANGGRAPH_API_URL,
        "LANGGRAPH_API_KEY": "***" if LANGGRAPH_API_KEY else "Not set",
        "OPENAI_API_KEY": "***" if OPENAI_API_KEY else "Not set",
        "Selected Agent": selected_agent,
        "Language": st.session_state.lang.upper()
    }
    st.json(config_data)

# Code tab
with tabs[5]:
    st.header(L['code_title'])
    
    code_query = st.text_area("Technical question:", height=100)
    
    if st.button("Ask Code Agent"):
        if code_query:
            with st.spinner("Consulting Code Agent..."):
                result = call_langgraph(code_query, None, "code", st.session_state.state)
                
                if result.get("status") != "error":
                    st.code(result.get("answer", "No response"), language="python")
                else:
                    st.error(result.get("message"))

# Footer
st.divider()
st.caption("Green Hill Executive Cockpit v2.0 | Powered by LangGraph & OpenAI")
