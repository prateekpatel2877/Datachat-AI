import streamlit as st
import pandas as pd
import os
import pdfplumber
import base64
from dotenv import load_dotenv
from groq import Groq

# Load API key
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ---- MODEL CONFIG (change here if model is deprecated) ----
# 💡 TIP: If model error occurs, update TEXT_MODEL or VISION_MODEL below
TEXT_MODEL = "llama-3.3-70b-versatile"
VISION_MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"

# ---- SESSION STATE ----
if "file_chat_history" not in st.session_state:
    st.session_state.file_chat_history = []
if "image_chat_history" not in st.session_state:
    st.session_state.image_chat_history = []
if "last_uploaded_file" not in st.session_state:
    st.session_state.last_uploaded_file = None
if "last_uploaded_image" not in st.session_state:
    st.session_state.last_uploaded_image = None

# Page config
st.set_page_config(page_title="DataChat AI", page_icon="🤖", layout="wide")

# Custom CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=Space+Mono:wght@400;700&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
.stApp { background-color: #0a0f1e; color: #e2e8f0; }

section[data-testid="stSidebar"] {
    background-color: #111827 !important;
    border-right: 1px solid #1e2d45;
}
section[data-testid="stSidebar"] * { color: #e2e8f0 !important; }
header[data-testid="stHeader"] { background: transparent; }
.block-container { padding: 2rem 2.5rem; max-width: 1200px; }

.gradient-title {
    font-family: 'DM Sans', sans-serif;
    font-size: 32px;
    font-weight: 700;
    background: linear-gradient(90deg, #3b82f6, #06b6d4);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.subtitle { color: #64748b; font-size: 15px; margin-bottom: 28px; }
.section-header { font-size: 15px; font-weight: 600; color: #e2e8f0; margin-bottom: 14px; }

.stat-card {
    background: #111827;
    border: 1px solid #1e2d45;
    border-radius: 12px;
    padding: 16px 20px;
    text-align: center;
}
.stat-label { font-size: 11px; color: #64748b; margin-bottom: 4px; font-family: 'Space Mono', monospace; letter-spacing: 1px; }
.stat-value-blue { font-size: 28px; font-weight: 700; color: #3b82f6; font-family: 'Space Mono', monospace; }
.stat-value-cyan { font-size: 28px; font-weight: 700; color: #06b6d4; font-family: 'Space Mono', monospace; }
.stat-value-green { font-size: 28px; font-weight: 700; color: #10b981; font-family: 'Space Mono', monospace; }

.user-bubble {
    background: rgba(59,130,246,0.12);
    border: 1px solid rgba(59,130,246,0.2);
    border-radius: 12px 12px 4px 12px;
    padding: 12px 16px;
    margin-bottom: 8px;
    font-size: 14px;
    color: #e2e8f0;
    text-align: right;
}
.user-label { font-size: 11px; color: #3b82f6; font-family: 'Space Mono', monospace; margin-bottom: 4px; text-align: right; }
.ai-bubble {
    background: #1a2236;
    border: 1px solid rgba(99,102,241,0.2);
    border-radius: 12px 12px 12px 4px;
    padding: 12px 16px;
    margin-bottom: 16px;
    font-size: 14px;
    line-height: 1.8;
    color: #e2e8f0;
}
.ai-bubble-label { font-size: 11px; color: #6366f1; font-family: 'Space Mono', monospace; margin-bottom: 4px; }

.success-box {
    background: rgba(16,185,129,0.1);
    border: 1px solid rgba(16,185,129,0.3);
    border-radius: 10px;
    padding: 12px 18px;
    color: #10b981;
    font-size: 14px;
    margin-bottom: 20px;
}

.stTextInput > div > div > input {
    background: #1a2236 !important;
    border: 1px solid #1e2d45 !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
    font-family: 'DM Sans', sans-serif !important;
}
.stTextInput > div > div > input:focus {
    border-color: #3b82f6 !important;
    box-shadow: 0 0 0 2px rgba(59,130,246,0.2) !important;
}
.stButton > button {
    background: linear-gradient(135deg, #3b82f6, #6366f1) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
}
.stDownloadButton > button {
    background: rgba(16,185,129,0.1) !important;
    color: #10b981 !important;
    border: 1px solid rgba(16,185,129,0.3) !important;
    border-radius: 8px !important;
    font-size: 13px !important;
}
.stSelectbox > div > div {
    background: #1a2236 !important;
    border: 1px solid #1e2d45 !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
}
.stTabs [data-baseweb="tab-list"] {
    background: #111827;
    border-radius: 10px;
    padding: 4px;
    gap: 4px;
}
.stTabs [data-baseweb="tab"] {
    background: transparent;
    color: #64748b;
    border-radius: 8px;
    font-family: 'DM Sans', sans-serif;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #3b82f6, #6366f1) !important;
    color: white !important;
}
.stForm { border: none !important; background: transparent !important; }
[data-testid="stForm"] { border: none !important; background: transparent !important; padding: 0 !important; }
hr { border-color: #1e2d45 !important; }

.connected-dot {
    width: 10px;
    height: 10px;
    background-color: #10b981;
    border-radius: 50%;
    display: inline-block;
    margin-right: 6px;
    box-shadow: 0 0 6px #10b981;
}
</style>
""", unsafe_allow_html=True)

# ---- SIDEBAR ----
with st.sidebar:
    st.markdown("""
        <div style='font-family: Space Mono, monospace; font-size: 18px; font-weight: 700; color: #06b6d4; margin-bottom: 24px;'>
            🤖 DataChat AI
        </div>
        <div style='color: #64748b; font-size: 11px; letter-spacing: 2px; margin-bottom: 8px;'>ANALYZE</div>
    """, unsafe_allow_html=True)

    st.markdown("📊 File Analyzer — CSV, Excel, PDF")
    st.markdown("🖼️ Image Analyzer — JPG, PNG, WEBP")
    st.divider()

    st.markdown("""
        <div style='background: rgba(59,130,246,0.08); border: 1px solid rgba(59,130,246,0.2); border-radius: 10px; padding: 14px; margin-top: 8px;'>
            <div style='font-size: 11px; color: #64748b; margin-bottom: 10px; letter-spacing: 1px;'>⚡ POWERED BY</div>
            <div style='font-size: 12px; color: #64748b; margin-bottom: 4px;'>Text Analysis</div>
            <div style='font-size: 13px; font-weight: 600; color: #3b82f6; margin-bottom: 10px;'>Llama 3.3 70B</div>
            <div style='font-size: 12px; color: #64748b; margin-bottom: 4px;'>Vision Analysis</div>
            <div style='font-size: 13px; font-weight: 600; color: #6366f1; margin-bottom: 10px;'>Llama 4 Scout</div>
            <div style='font-size: 12px; color: #64748b; margin-bottom: 4px;'>Inference</div>
            <div style='font-size: 13px; font-weight: 600; color: #06b6d4; margin-bottom: 12px;'>Groq API</div>
            <div style='display: flex; align-items: center; margin-top: 4px;'>
                <div class='connected-dot'></div>
                <span style='color: #10b981 !important; font-size: 13px;'>Connected</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

# ---- HEADER ----
st.markdown("""
    <div style='display: flex; align-items: center; gap: 10px; margin-bottom: 4px;'>
        <span style='font-size: 36px;'>🤖</span>
        <span class='gradient-title'>DataChat AI</span>
    </div>
""", unsafe_allow_html=True)
st.markdown('<div class="subtitle">Upload CSV, Excel, PDF or Image — ask questions in plain English!</div>', unsafe_allow_html=True)

# ---- TABS ----
tab1, tab2 = st.tabs(["📁 File Analyzer", "🖼️ Image Analyzer"])

# ================================================================
# TAB 1 — FILE ANALYZER
# ================================================================
with tab1:

    uploaded_file = st.file_uploader(
        "Upload your file",
        type=["csv", "xlsx", "xls", "pdf"],
        help="Supports CSV, Excel, and PDF files"
    )

    df = None
    text_data = None

    if uploaded_file is not None:

        if st.session_state.last_uploaded_file != uploaded_file.name:
            st.session_state.file_chat_history = []
            st.session_state.last_uploaded_file = uploaded_file.name

        file_type = uploaded_file.name.split(".")[-1].lower()

        if file_type == "csv":
            df = pd.read_csv(uploaded_file)
            st.markdown('<div class="success-box">✅ CSV file uploaded successfully!</div>', unsafe_allow_html=True)
        elif file_type in ["xlsx", "xls"]:
            df = pd.read_excel(uploaded_file)
            st.markdown('<div class="success-box">✅ Excel file uploaded successfully!</div>', unsafe_allow_html=True)
        elif file_type == "pdf":
            with pdfplumber.open(uploaded_file) as pdf:
                text_data = ""
                for page in pdf.pages:
                    text_data += page.extract_text() or ""
            st.markdown('<div class="success-box">✅ PDF file uploaded successfully!</div>', unsafe_allow_html=True)

        # ---- STATS ----
        if df is not None:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(f"""
                    <div class="stat-card">
                        <div class="stat-label">TOTAL ROWS</div>
                        <div class="stat-value-blue">{df.shape[0]:,}</div>
                    </div>
                """, unsafe_allow_html=True)
            with col2:
                st.markdown(f"""
                    <div class="stat-card">
                        <div class="stat-label">TOTAL COLUMNS</div>
                        <div class="stat-value-cyan">{df.shape[1]}</div>
                    </div>
                """, unsafe_allow_html=True)
            with col3:
                st.markdown(f"""
                    <div class="stat-card">
                        <div class="stat-label">FILE TYPE</div>
                        <div class="stat-value-green">{file_type.upper()}</div>
                    </div>
                """, unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)

        # ---- CHAT HISTORY ----
        if st.session_state.file_chat_history:
            st.markdown('<div class="section-header">💬 Chat History</div>', unsafe_allow_html=True)
            for chat in st.session_state.file_chat_history:
                st.markdown(f"""
                    <div class="user-label">YOU</div>
                    <div class="user-bubble">{chat['question']}</div>
                    <div class="ai-bubble-label">🤖 AI ANSWER</div>
                    <div class="ai-bubble">{chat['answer']}</div>
                """, unsafe_allow_html=True)
            st.divider()

        # ---- Q&A FORM ----
        st.markdown('<div class="section-header">💬 Ask AI About Your File</div>', unsafe_allow_html=True)

        with st.form(key="file_form", clear_on_submit=True):
            user_question = st.text_input(
                "",
                placeholder="e.g. What is the average closing price? Give me a summary.",
                label_visibility="collapsed"
            )
            col1, col2 = st.columns([1, 5])
            with col1:
                ask_btn = st.form_submit_button("🚀 Ask")
            with col2:
                clear_btn = st.form_submit_button("🗑️ Clear History")

        if clear_btn:
            st.session_state.file_chat_history = []
            st.rerun()

        if ask_btn and user_question:
            with st.spinner("🤖 AI is thinking..."):
                if df is not None:
                    data_summary = df.describe().to_string()
                    columns = df.columns.tolist()
                    content = f"Dataset columns: {columns}\n\nDataset summary:\n{data_summary}\n\nQuestion: {user_question}"
                else:
                    content = f"PDF Content:\n{text_data[:3000]}\n\nQuestion: {user_question}"

                messages = [
                    {"role": "system", "content": "You are a data analyst. Answer questions about the given data clearly and concisely."}
                ]
                for chat in st.session_state.file_chat_history:
                    messages.append({"role": "user", "content": chat["question"]})
                    messages.append({"role": "assistant", "content": chat["answer"]})
                messages.append({"role": "user", "content": content})

                response = client.chat.completions.create(
                    model=TEXT_MODEL,
                    messages=messages
                )
                answer = response.choices[0].message.content

            st.session_state.file_chat_history.append({
                "question": user_question,
                "answer": answer
            })
            st.rerun()

        if st.session_state.file_chat_history:
            last_answer = st.session_state.file_chat_history[-1]["answer"]
            st.download_button(
                label="📥 Download Last Answer",
                data=last_answer,
                file_name="ai_answer.txt",
                mime="text/plain",
                key="file_download"
            )

        st.divider()

        # ---- DATA PREVIEW ----
        if df is not None:
            st.markdown('<div class="section-header">📋 Data Preview</div>', unsafe_allow_html=True)
            st.dataframe(df.head(10), use_container_width=True)
            st.divider()

            # ---- CHART ----
            st.markdown('<div class="section-header">📊 Data Visualization</div>', unsafe_allow_html=True)
            numeric_cols = df.select_dtypes(include='number').columns.tolist()

            if len(numeric_cols) >= 1:
                col1, col2 = st.columns([2, 1])
                with col1:
                    selected_col = st.selectbox("Select column to visualize:", numeric_cols)
                with col2:
                    chart_type = st.radio("Chart type:", ["Line", "Bar", "Area"], horizontal=True)

                total_rows = len(df)
                row_range = st.slider(
                    "Select data range:",
                    min_value=0,
                    max_value=total_rows,
                    value=(0, total_rows),
                    step=1
                )

                filtered_df = df[selected_col].iloc[row_range[0]:row_range[1]]

                if chart_type == "Line":
                    st.line_chart(filtered_df, use_container_width=True)
                elif chart_type == "Bar":
                    st.bar_chart(filtered_df, use_container_width=True)
                elif chart_type == "Area":
                    st.area_chart(filtered_df, use_container_width=True)
            else:
                st.info("No numeric columns found for visualization.")

        if text_data:
            st.divider()
            st.markdown('<div class="section-header">📄 PDF Content Preview</div>', unsafe_allow_html=True)
            st.text_area("", text_data[:1000] + "...", height=200, label_visibility="collapsed")

# ================================================================
# TAB 2 — IMAGE ANALYZER
# ================================================================
with tab2:

    st.markdown('<div class="section-header">🖼️ Upload Image for AI Analysis</div>', unsafe_allow_html=True)

    uploaded_image = st.file_uploader(
        "Upload an image",
        type=["jpg", "jpeg", "png", "webp"],
        help="Supports JPG, PNG, WEBP",
        key="image_uploader"
    )

    if uploaded_image is not None:

        if st.session_state.last_uploaded_image != uploaded_image.name:
            st.session_state.image_chat_history = []
            st.session_state.last_uploaded_image = uploaded_image.name

        col1, col2 = st.columns([1, 1])
        with col1:
            st.image(uploaded_image, caption="Uploaded Image", use_container_width=True)
        with col2:
            st.markdown('<div class="success-box">✅ Image uploaded successfully!</div>', unsafe_allow_html=True)

            if st.session_state.image_chat_history:
                st.markdown('<div class="section-header">💬 Chat History</div>', unsafe_allow_html=True)
                for chat in st.session_state.image_chat_history:
                    st.markdown(f"""
                        <div class="user-label">YOU</div>
                        <div class="user-bubble">{chat['question']}</div>
                        <div class="ai-bubble-label">🤖 AI ANSWER</div>
                        <div class="ai-bubble">{chat['answer']}</div>
                    """, unsafe_allow_html=True)
                st.divider()

            st.markdown('<div class="section-header">💬 Ask AI About This Image</div>', unsafe_allow_html=True)

            with st.form(key="image_form", clear_on_submit=True):
                image_question = st.text_input(
                    "",
                    placeholder="e.g. What is in this image? Describe the chart.",
                    label_visibility="collapsed"
                )
                col_a, col_b = st.columns([1, 2])
                with col_a:
                    ask_img_btn = st.form_submit_button("🚀 Ask")
                with col_b:
                    clear_img_btn = st.form_submit_button("🗑️ Clear History")

            if clear_img_btn:
                st.session_state.image_chat_history = []
                st.rerun()

            if ask_img_btn and image_question:
                image_bytes = uploaded_image.read()
                base64_image = base64.b64encode(image_bytes).decode("utf-8")
                media_type = uploaded_image.type

                with st.spinner("🤖 AI is analyzing your image..."):
                    response = client.chat.completions.create(
                        model=VISION_MODEL,
                        messages=[
                            {
                                "role": "user",
                                "content": [
                                    {
                                        "type": "image_url",
                                        "image_url": {"url": f"data:{media_type};base64,{base64_image}"}
                                    },
                                    {"type": "text", "text": image_question}
                                ]
                            }
                        ]
                    )
                    image_answer = response.choices[0].message.content

                st.session_state.image_chat_history.append({
                    "question": image_question,
                    "answer": image_answer
                })
                st.rerun()

            if st.session_state.image_chat_history:
                last_img_answer = st.session_state.image_chat_history[-1]["answer"]
                st.download_button(
                    label="📥 Download Last Answer",
                    data=last_img_answer,
                    file_name="image_analysis.txt",
                    mime="text/plain",
                    key="img_download"
                )