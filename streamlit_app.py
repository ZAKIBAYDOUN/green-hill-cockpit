import streamlit as st
import requests
import os
import json
from datetime import datetime
import base64
import io

st.set_page_config(page_title="Green Hill Cockpit", layout="wide")

# === CSS CON VERDE OSCURO ===
st.markdown("""
<style>
:root { 
    --gh-primary: #1B4D3E;
    --gh-accent: #2E7D32;
    --gh-light: #E8F5E8;
    --gh-text: #0D3D29;
}
.main { background: #FAFFFE; }
.stTabs [data-baseweb="tab-list"] { 
    border-bottom: 3px solid var(--gh-primary);
    background: var(--gh-light);
}
.stTabs [data-baseweb="tab"] { 
    color: var(--gh-text);
    font-weight: 700;
    font-size: 16px;
    padding: 12px 20px;
}
.stTabs [data-baseweb="tab"][aria-selected="true"] {
    background: var(--gh-primary);
    color: white;
}
.main-header {
    background: linear-gradient(90deg, var(--gh-primary), var(--gh-accent));
    color: white;
    padding: 20px;
    border-radius: 10px;
    text-align: center;
    margin-bottom: 20px;
}
.agent-card {
    background: var(--gh-light);
    border: 2px solid var(--gh-accent);
    border-radius: 10px;
    padding: 15px;
    margin: 10px 0;
}
.success-msg { 
    background: var(--gh-light);
    color: var(--gh-text);
    padding: 10px;
    border-radius: 5px;
    border-left: 4px solid var(--gh-accent);
}
</style>
""", unsafe_allow_html=True)

# === API CONFIGURATION ===
# Las claves se configuran a través de Streamlit Secrets o variables de entorno
try:
    API_URL = st.secrets["API_URL"]
    API_KEY = st.secrets["API_KEY"] 
    OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
except:
    # Fallback a variables de entorno para desarrollo local
    API_URL = os.getenv("API_URL", "")
    API_KEY = os.getenv("API_KEY", "")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# Verificar configuración
if not API_KEY or not OPENAI_API_KEY:
    st.error("🔐 Please configure API keys in Streamlit Secrets or environment variables")
    st.info("For Streamlit Cloud: Add secrets in app settings")
    st.info("For local development: Create .env file with your keys")
    st.stop()

# === LANGUAGES ===
LANGUAGES = {
    "🇺🇸 English": "en",
    "🇪🇸 Español": "es", 
    "🇮🇸 Íslenska": "is",
    "🇫🇷 Français": "fr"
}

TRANSLATIONS = {
    "en": {
        "title": "Green Hill Executive Cockpit",
        "subtitle": "Cannabis Operations Intelligence System",
        "tabs": ["💬 Chat", "🎤 Audio", "📸 Visual", "🤖 CEO", "👥 Agents", "📊 Reports"],
        "chat_title": "Intelligent Chat",
        "audio_title": "Audio Intelligence",
        "visual_title": "Visual Intelligence", 
        "ceo_title": "CEO Digital Twin",
        "agents_title": "Specialized Agents",
        "reports_title": "Executive Reports",
        "type_message": "Type your message here...",
        "send": "Send",
        "upload_audio": "Upload Audio File",
        "record_audio": "🎤 Record Audio",
        "upload_image": "Upload Image",
        "take_photo": "📸 Take Photo",
        "process": "Process",
        "select_agent": "Select Agent:"
    },
    "es": {
        "title": "Green Hill Cockpit Ejecutivo",
        "subtitle": "Sistema de Inteligencia para Operaciones de Cannabis",
        "tabs": ["💬 Chat", "🎤 Audio", "📸 Visual", "🤖 CEO", "👥 Agentes", "📊 Informes"],
        "chat_title": "Chat Inteligente",
        "audio_title": "Inteligencia de Audio",
        "visual_title": "Inteligencia Visual",
        "ceo_title": "CEO Digital Twin",
        "agents_title": "Agentes Especializados", 
        "reports_title": "Informes Ejecutivos",
        "type_message": "Escribe tu mensaje aquí...",
        "send": "Enviar",
        "upload_audio": "Subir Archivo de Audio",
        "record_audio": "🎤 Grabar Audio",
        "upload_image": "Subir Imagen", 
        "take_photo": "📸 Tomar Foto",
        "process": "Procesar",
        "select_agent": "Seleccionar Agente:"
    },
    "is": {
        "title": "Green Hill Stjórnstöð",
        "subtitle": "Greiningarkerfi fyrir Cannabis Rekstur",
        "tabs": ["💬 Spjall", "🎤 Hljóð", "📸 Mynd", "🤖 CEO", "👥 Umboð", "📊 Skýrslur"],
        "chat_title": "Gáfuð Samtöl",
        "audio_title": "Hljóðgreining",
        "visual_title": "Sjóngreining",
        "ceo_title": "CEO Digital Twin",
        "agents_title": "Sérhæfð Umboð",
        "reports_title": "Stjórnunarskýrslur",
        "type_message": "Skrifaðu skilaboð hér...",
        "send": "Senda",
        "upload_audio": "Hlaða upp hljóðskrá",
        "record_audio": "🎤 Taka upp hljóð",
        "upload_image": "Hlaða upp mynd",
        "take_photo": "📸 Taka mynd",
        "process": "Vinna",
        "select_agent": "Veldu umboð:"
    },
    "fr": {
        "title": "Cockpit Exécutif Green Hill",
        "subtitle": "Système d'Intelligence pour Opérations Cannabis",
        "tabs": ["💬 Chat", "🎤 Audio", "📸 Visuel", "🤖 CEO", "👥 Agents", "📊 Rapports"],
        "chat_title": "Chat Intelligent",
        "audio_title": "Intelligence Audio",
        "visual_title": "Intelligence Visuelle",
        "ceo_title": "CEO Digital Twin",
        "agents_title": "Agents Spécialisés",
        "reports_title": "Rapports Exécutifs",
        "type_message": "Tapez votre message ici...",
        "send": "Envoyer", 
        "upload_audio": "Télécharger Fichier Audio",
        "record_audio": "🎤 Enregistrer Audio",
        "upload_image": "Télécharger Image",
        "take_photo": "📸 Prendre Photo",
        "process": "Traiter",
        "select_agent": "Sélectionner Agent:"
    }
}

AGENTS = ["Strategy", "Finance", "Operations", "Market", "Risk", "Compliance", "Innovation"]

def call_openai_agent(content, agent_type, lang):
    """Call OpenAI API with specialized prompts"""
    try:
        import openai
        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        
        prompts = {
            "Strategy": f"Eres el Director de Estrategia de Green Hill Canarias. Especialízate en cannabis medicinal en Canarias. Responde en {lang}.",
            "Finance": f"Eres el Director Financiero de Green Hill Canarias. Analiza inversiones y ROI en cannabis medicinal. Responde en {lang}.",
            "Operations": f"Eres el Director de Operaciones de Green Hill Canarias. Planifica operaciones bajo estándares EU-GMP. Responde en {lang}.",
            "Market": f"Eres el Director de Mercado de Green Hill Canarias. Analiza mercado europeo de cannabis medicinal. Responde en {lang}.",
            "Risk": f"Eres el Director de Riesgos de Green Hill Canarias. Evalúa riesgos regulatorios y operacionales. Responde en {lang}.",
            "Compliance": f"Eres el Director de Cumplimiento de Green Hill Canarias. Experto en regulación AEMPS y EU-GMP. Responde en {lang}.",
            "Innovation": f"Eres el Director de Innovación de Green Hill Canarias. Identifica oportunidades tecnológicas en cannabis medicinal. Responde en {lang}.",
            "CEO": f"Eres el CEO de Green Hill Canarias. Proporciona perspectiva ejecutiva integral sobre todas las operaciones. Responde en {lang}."
        }
        
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": prompts.get(agent_type, f"Eres un asistente especializado de Green Hill Canarias. Responde en {lang}.")},
                {"role": "user", "content": content}
            ],
            max_tokens=1000,
            temperature=0.7
        )
        
        return response.choices[0].message.content
    except Exception as e:
        return f"Error connecting to OpenAI: {str(e)}"

def transcribe_audio(audio_file):
    """Transcribe audio using OpenAI Whisper"""
    try:
        import openai
        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            language="es"
        )
        
        return transcript.text
    except Exception as e:
        return f"Error transcribing audio: {str(e)}"

def analyze_image(image_file):
    """Analyze image using GPT-4 Vision"""
    try:
        import openai
        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        
        if hasattr(image_file, 'read'):
            image_data = image_file.read()
        else:
            image_data = image_file
        
        base64_image = base64.b64encode(image_data).decode('utf-8')
        
        response = client.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Analiza esta imagen en el contexto de Green Hill Canarias y operaciones de cannabis medicinal en las Islas Canarias."
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=500
        )
        
        return response.choices[0].message.content
    except Exception as e:
        return f"Error analyzing image: {str(e)}"

# === MAIN APP ===
if "selected_language" not in st.session_state:
    st.markdown('<div class="main-header"><h1>🌿 GREEN HILL CANARIAS</h1><p>Cannabis Operations Intelligence Platform</p></div>', unsafe_allow_html=True)
    
    st.markdown("## �� Select Your Language / Selecciona tu idioma / Veldu tungumál / Sélectionnez votre langue")
    
    cols = st.columns(4)
    for i, (lang_name, lang_code) in enumerate(LANGUAGES.items()):
        with cols[i]:
            if st.button(lang_name, key=f"lang_{lang_code}", use_container_width=True):
                st.session_state.selected_language = lang_code
                st.rerun()

else:
    # Get language
    lang = st.session_state.selected_language
    t = TRANSLATIONS[lang]
    
    # Header
    st.markdown(f'<div class="main-header"><h1>🌿 {t["title"]}</h1><p>{t["subtitle"]}</p></div>', unsafe_allow_html=True)
    
    # Language switcher
    col1, col2 = st.columns([4, 1])
    with col2:
        if st.button("🌍 Change", help="Change language"):
            del st.session_state.selected_language
            st.rerun()
    
    # Main tabs
    tabs = st.tabs(t["tabs"])
    
    # === CHAT TAB ===
    with tabs[0]:
        st.markdown(f'<div class="agent-card"><h2>{t["chat_title"]}</h2></div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            user_input = st.text_area(t["type_message"], height=100, key="chat_input")
        
        with col2:
            selected_agent = st.selectbox(t["select_agent"], AGENTS, key="chat_agent")
            
            if st.button(t["send"], type="primary", use_container_width=True):
                if user_input.strip():
                    with st.spinner("🤖 Processing..."):
                        response = call_openai_agent(user_input, selected_agent, lang)
                        
                        st.markdown(f'<div class="success-msg"><strong>✅ {selected_agent} Response:</strong><br>{response}</div>', unsafe_allow_html=True)
    
    # === AUDIO TAB ===
    with tabs[1]:
        st.markdown(f'<div class="agent-card"><h2>{t["audio_title"]}</h2></div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader(t["record_audio"])
            
            try:
                from st_audiorec import st_audiorec
                
                st.info("🎤 Presiona para grabar")
                audio_bytes = st_audiorec()
                
                if audio_bytes:
                    st.audio(audio_bytes, format="audio/wav")
                    
                    agent_audio = st.selectbox(t["select_agent"], AGENTS, key="audio_agent_rec")
                    
                    if st.button(t["process"], key="process_rec"):
                        with st.spinner("�� Transcribiendo..."):
                            audio_file = io.BytesIO(audio_bytes)
                            audio_file.name = "audio.wav"
                            
                            transcript = transcribe_audio(audio_file)
                            st.success(f"📝 Transcripción: {transcript}")
                            
                            response = call_openai_agent(transcript, agent_audio, lang)
                            st.markdown(f'<div class="success-msg"><strong>✅ {agent_audio}:</strong><br>{response}</div>', unsafe_allow_html=True)
                            
            except ImportError:
                st.warning("📦 Grabación no disponible en este entorno. Sube archivo de audio →")
        
        with col2:
            st.subheader(t["upload_audio"])
            
            uploaded_audio = st.file_uploader(
                t["upload_audio"], 
                type=['wav', 'mp3', 'm4a', 'ogg'],
                key="audio_file"
            )
            
            if uploaded_audio:
                st.audio(uploaded_audio)
                
                agent_upload = st.selectbox(t["select_agent"], AGENTS, key="audio_agent_upload")
                
                if st.button(t["process"], key="process_upload"):
                    with st.spinner("🎤 Transcribiendo..."):
                        transcript = transcribe_audio(uploaded_audio)
                        st.success(f"📝 Transcripción: {transcript}")
                        
                        response = call_openai_agent(transcript, agent_upload, lang)
                        st.markdown(f'<div class="success-msg"><strong>✅ {agent_upload}:</strong><br>{response}</div>', unsafe_allow_html=True)
    
    # === VISUAL TAB ===
    with tabs[2]:
        st.markdown(f'<div class="agent-card"><h2>{t["visual_title"]}</h2></div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader(t["take_photo"])
            
            camera_photo = st.camera_input("📸 Camera")
            
            if camera_photo:
                agent_camera = st.selectbox(t["select_agent"], AGENTS, key="camera_agent")
                
                if st.button(t["process"], key="process_camera"):
                    with st.spinner("📸 Analizando imagen..."):
                        analysis = analyze_image(camera_photo)
                        st.success(f"🔍 Análisis: {analysis}")
                        
                        response = call_openai_agent(f"Análisis visual: {analysis}", agent_camera, lang)
                        st.markdown(f'<div class="success-msg"><strong>✅ {agent_camera}:</strong><br>{response}</div>', unsafe_allow_html=True)
        
        with col2:
            st.subheader(t["upload_image"])
            
            uploaded_image = st.file_uploader(
                t["upload_image"],
                type=['png', 'jpg', 'jpeg', 'gif'],
                key="image_file"
            )
            
            if uploaded_image:
                st.image(uploaded_image, use_column_width=True)
                
                agent_image = st.selectbox(t["select_agent"], AGENTS, key="image_agent")
                
                if st.button(t["process"], key="process_image"):
                    with st.spinner("📸 Analizando imagen..."):
                        analysis = analyze_image(uploaded_image)
                        st.success(f"🔍 Análisis: {analysis}")
                        
                        response = call_openai_agent(f"Análisis visual: {analysis}", agent_image, lang)
                        st.markdown(f'<div class="success-msg"><strong>✅ {agent_image}:</strong><br>{response}</div>', unsafe_allow_html=True)
    
    # === CEO TAB ===
    with tabs[3]:
        st.markdown(f'<div class="agent-card" style="background: linear-gradient(135deg, #1B4D3E, #2E7D32); color: white;"><h2>🤖 {t["ceo_title"]}</h2></div>', unsafe_allow_html=True)
        
        ceo_query = st.text_area("🎯 Executive Query", height=120, placeholder="Ask strategic questions about Green Hill Canarias operations...")
        
        if st.button("🚀 Execute Strategic Analysis", type="primary"):
            if ceo_query.strip():
                with st.spinner("🔄 Engaging CEO intelligence..."):
                    response = call_openai_agent(ceo_query, "CEO", lang)
                    st.markdown(f'<div class="success-msg"><strong>✅ CEO Strategic Response:</strong><br>{response}</div>', unsafe_allow_html=True)
    
    # === AGENTS TAB ===
    with tabs[4]:
        st.markdown(f'<div class="agent-card"><h2>{t["agents_title"]}</h2></div>', unsafe_allow_html=True)
        
        query = st.text_area("Query for all agents:", height=100, placeholder="Ask a question that all agents will analyze from their perspective...")
        
        if st.button("🔄 Consult All Agents", type="primary"):
            if query.strip():
                st.markdown("## 📋 Multi-Agent Analysis")
                
                for agent in AGENTS:
                    with st.expander(f"📊 {agent} Director", expanded=False):
                        with st.spinner(f"Consulting {agent}..."):
                            response = call_openai_agent(query, agent, lang)
                            st.markdown(response)
    
    # === REPORTS TAB ===
    with tabs[5]:
        st.markdown(f'<div class="agent-card"><h2>{t["reports_title"]}</h2></div>', unsafe_allow_html=True)
        
        st.markdown("### 📊 Executive Reports for Green Hill Canarias")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📈 Strategic Report", use_container_width=True):
                st.session_state.report_type = "strategic"
        
        with col2:
            if st.button("💰 Financial Report", use_container_width=True):
                st.session_state.report_type = "financial"
        
        with col3:
            if st.button("⚖️ Compliance Report", use_container_width=True):
                st.session_state.report_type = "compliance"
        
        if "report_type" in st.session_state:
            report_queries = {
                "strategic": "Provide comprehensive strategic overview of Green Hill Canarias current market position, EU cannabis opportunities, Canary Islands advantages, and Q4 2025 growth outlook.",
                "financial": "Generate detailed financial analysis including CAPEX/OPEX for EU-GMP facility, ROI projections for medicinal cannabis operations, and investment requirements for scaling.",
                "compliance": "Deliver complete compliance assessment covering AEMPS regulatory status, EU-GMP certification progress, ZEC tax benefits, and regulatory roadmap for 2025."
            }
            
            query = report_queries[st.session_state.report_type]
            
            with st.spinner("📊 Generating comprehensive executive report..."):
                response = call_openai_agent(query, "CEO", lang)
                st.markdown(f'<div class="success-msg"><strong>✅ Executive Report ({st.session_state.report_type.title()}):</strong><br>{response}</div>', unsafe_allow_html=True)
                
                # Clear the report type so user can generate another
                if st.button("🔄 Generate Another Report"):
                    del st.session_state.report_type
                    st.rerun()
