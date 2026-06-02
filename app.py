import streamlit as st
import time
import google.generativeai as genai
import os

st.set_page_config(page_title="HealthCare AI - Dokter Digital", page_icon="🩺", layout="centered")

# FILE API KEY PATH
API_KEY_FILE = "api_key.txt"

# CSS Modern & Premium
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');
    
    :root {
        --primary: #2563eb;
        --primary-hover: #1d4ed8;
        --bg-main: #f8fafc;
        --text-dark: #0f172a;
        --text-muted: #64748b;
        --white: #ffffff;
        --user-bubble: #1e293b;
        --ai-bubble: #ffffff;
    }

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    .stApp {
        background-color: var(--bg-main) !important;
    }
    
    [data-testid="stHeader"] {
        display: none !important;
    }
    
    .block-container {
        padding-top: 2rem;
        padding-bottom: 5rem;
        max-width: 800px !important;
    }

    /* Chat Input Styling */
    [data-testid="stChatInputContainer"] {
        padding: 1.5rem !important;
        background: transparent !important;
    }
    
    [data-testid="stChatInput"] {
        border-radius: 30px !important;
        border: 1px solid #e2e8f0 !important;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05) !important;
        background: var(--white) !important;
    }

    /* Chat Bubbles */
    div[data-testid="stChatMessage"] {
        padding: 1rem 0 !important;
        background: transparent !important;
        border: none !important;
        animation: fadeIn 0.4s ease-out forwards;
    }

    /* Hide default avatars */
    [data-testid="stChatMessageAvatarUser"], 
    [data-testid="stChatMessageAvatarAssistant"],
    .stChatMessageAvatar {
        display: none !important;
    }

    /* User Message Style */
    div[data-testid="stChatMessage"]:has(div[aria-label="Chat message from user"]) {
        flex-direction: row-reverse !important;
    }

    div[data-testid="stChatMessage"]:has(div[aria-label="Chat message from user"]) div[data-testid="stMarkdownContainer"] {
        background-color: var(--user-bubble) !important;
        color: white !important;
        border-radius: 24px 24px 4px 24px !important;
        margin-left: auto !important;
        width: fit-content !important;
        padding: 14px 22px !important;
        box-shadow: 0 4px 12px rgba(30, 41, 59, 0.1) !important;
    }

    /* Assistant Message Style */
    div[data-testid="stChatMessage"]:has(div[aria-label="Chat message from assistant"]) div[data-testid="stMarkdownContainer"] {
        background-color: var(--ai-bubble) !important;
        color: var(--text-dark) !important;
        border-radius: 24px 24px 24px 4px !important;
        margin-right: auto !important;
        width: fit-content !important;
        border: 1px solid #f1f5f9 !important;
        padding: 14px 22px !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.04) !important;
    }

    /* Header Styling */
    .chat-header {
        text-align: center;
        margin-bottom: 2.5rem;
    }
    
    .chat-header h1 {
        font-size: 2.2rem;
        font-weight: 800;
        color: var(--text-dark);
        margin: 10px 0 0 0 !important;
        letter-spacing: -1px;
    }

    .api-setup {
        background: white;
        padding: 40px;
        border-radius: 24px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.05);
        text-align: center;
        margin-top: 50px;
    }

    /* Typing Indicator */
    .typing {
        display: flex;
        gap: 5px;
        padding: 10px;
    }
    .dot {
        width: 7px;
        height: 7px;
        background: #cbd5e1;
        border-radius: 50%;
        animation: blink 1.4s infinite both;
    }
    .dot:nth-child(2) { animation-delay: 0.2s; }
    .dot:nth-child(3) { animation-delay: 0.4s; }
    @keyframes blink {
        0%, 80%, 100% { opacity: 0; transform: scale(0.8); }
        40% { opacity: 1; transform: scale(1.1); }
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
</style>
""", unsafe_allow_html=True)

# Initialization
if "messages" not in st.session_state:
    st.session_state.messages = []
if "api_key" not in st.session_state:
    # AUTO LOAD FROM FILE
    if os.path.exists(API_KEY_FILE):
        with open(API_KEY_FILE, "r") as f:
            st.session_state.api_key = f.read().strip()
    else:
        st.session_state.api_key = None

# Header Always Visible
st.markdown("""
<div class="chat-header">
    <div style="font-size: 3.5rem;">🩺</div>
    <h1>HealthCare AI</h1>
</div>
""", unsafe_allow_html=True)

# API Setup Screen (Only if no key)
if not st.session_state.api_key:
    with st.container():
        st.markdown("""
        <div class="api-setup">
            <h3 style="margin-bottom: 20px;">Selamat Datang!</h3>
            <p style="color: #64748b; margin-bottom: 30px;">Silakan masukkan Google Gemini API Key Anda. Sistem akan menyimpannya secara otomatis agar Anda tidak perlu menginputnya lagi nanti.</p>
        </div>
        """, unsafe_allow_html=True)
        
        key_input = st.text_input("Gemini API Key", type="password", placeholder="Masukkan kunci API di sini...")
        if st.button("Mulai Konsultasi", use_container_width=True):
            if key_input.startswith("AIza"):
                # AUTO SAVE TO FILE
                with open(API_KEY_FILE, "w") as f:
                    f.write(key_input)
                st.session_state.api_key = key_input
                st.success("API Key disimpan! Mengalihkan...")
                time.sleep(1)
                st.rerun()
            else:
                st.error("API Key tidak valid. Biasanya dimulai dengan 'AIza'.")
        st.stop()

# Configure Gemini
genai.configure(api_key=st.session_state.api_key)

# System Instruction for Doctor Persona
SYSTEM_INSTRUCTION = """
Anda adalah HealthCare AI, seorang Dokter Spesialis AI Senior yang sangat empati, profesional, dan akurat.
Tugas Anda:
1. HANYA melayani konsultasi kesehatan, penyakit, dan gaya hidup sehat. Tolak dengan sopan jika di luar topik.
2. Jika pasien menyebutkan gejala awal, JANGAN langsung mendiagnosis. Mintalah detail lebih lanjut seperti:
   - Sudah berapa hari gejalanya?
   - Di mana titik sakitnya?
   - Apakah ada gejala penyerta (demam, pusing, mual)?
3. Setelah data dirasa cukup, berikan analisis kemungkinan penyakit dengan bahasa yang mudah dimengerti.
4. Berikan saran penanganan awal (obat bebas yang aman atau tindakan mandiri).
5. Selalu rekomendasikan untuk mengunjungi dokter sungguhan jika gejala menetap atau parah.
6. Gunakan format Markdown yang rapi (bold, list, dll).
7. Gunakan Bahasa Indonesia yang ramah (gunakan sapaan 'Anda' atau 'Bapak/Ibu').
"""

# USE GEMINI FLASH FOR BETTER STABILITY & SPEED
# Gemini 1.5 Pro often hits quota or is not available on some API keys
model_name = 'gemini-flash-latest'

model = genai.GenerativeModel(
    model_name=model_name,
    system_instruction=SYSTEM_INSTRUCTION
)

# Render Chat History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat Input
if prompt := st.chat_input("Ceritakan keluhan kesehatan Anda di sini..."):
    # Display User Message
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display Assistant Message
    with st.chat_message("assistant"):
        typing_placeholder = st.empty()
        typing_placeholder.markdown('<div class="typing"><div class="dot"></div><div class="dot"></div><div class="dot"></div></div>', unsafe_allow_html=True)
        
        try:
            # Map history for Gemini
            history = []
            for m in st.session_state.messages[:-1]:
                role = "user" if m["role"] == "user" else "model"
                history.append({"role": role, "parts": [m["content"]]})
            
            chat = model.start_chat(history=history)
            response = chat.send_message(prompt)
            
            typing_placeholder.empty()
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            
        except Exception as e:
            typing_placeholder.empty()
            error_msg = str(e)
            if "404" in error_msg:
                st.error(f"Model '{model_name}' tidak ditemukan. Mencoba beralih ke model alternatif...")
                st.info("Saran: Pastikan API Key Anda memiliki akses ke model ini di Google AI Studio.")
            elif "429" in error_msg:
                st.error("Batas kuota (Rate Limit) tercapai. Silakan tunggu beberapa saat sebelum mengirim pesan lagi.")
            else:
                st.error(f"Maaf, terjadi kesalahan teknis: {error_msg}")
