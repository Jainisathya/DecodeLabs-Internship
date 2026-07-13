import streamlit as st
import pandas as pd
import os
from datetime import datetime
from PIL import Image

from utils.image_classifier import classify_image
from utils.text_classifier import read_text, draw_boxes

# ─────────────────────────────────────────────
# Page Config
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="VisionAI – Image & Text Recognition",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# Global CSS – Light Theme
# ─────────────────────────────────────────────
st.markdown("""
<style>
/* ── Google Font ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* ── App background ── */
.stApp {
    background: linear-gradient(135deg, #f0f4ff 0%, #faf5ff 50%, #fff0f9 100%);
    min-height: 100vh;
}

/* ── Hide default Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1e1b4b 0%, #312e81 50%, #4c1d95 100%) !important;
    border-right: none !important;
}
[data-testid="stSidebar"] * { color: #e0e7ff !important; }
[data-testid="stSidebar"] .stMarkdown h1,
[data-testid="stSidebar"] .stMarkdown h2,
[data-testid="stSidebar"] .stMarkdown h3 { color: #ffffff !important; }
[data-testid="stSidebar"] hr { border-color: rgba(255,255,255,0.15) !important; }

/* ── Sidebar success/info boxes ── */
[data-testid="stSidebar"] .stAlert {
    background: rgba(255,255,255,0.08) !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    border-radius: 10px !important;
    color: #c7d2fe !important;
}

/* ── Hero banner ── */
.hero-banner {
    background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 50%, #a855f7 100%);
    border-radius: 20px;
    padding: 48px 40px;
    text-align: center;
    margin-bottom: 32px;
    box-shadow: 0 20px 60px rgba(79,70,229,0.25);
    position: relative;
    overflow: hidden;
}
.hero-banner::before {
    content: '';
    position: absolute;
    top: -50%; left: -50%;
    width: 200%; height: 200%;
    background: radial-gradient(circle, rgba(255,255,255,0.05) 0%, transparent 60%);
    animation: shimmer 4s infinite;
}
@keyframes shimmer {
    0%   { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}
.hero-title {
    font-size: 2.8rem;
    font-weight: 800;
    color: #ffffff;
    margin: 0 0 12px 0;
    letter-spacing: -0.5px;
    text-shadow: 0 2px 20px rgba(0,0,0,0.2);
}
.hero-subtitle {
    font-size: 1.1rem;
    color: rgba(255,255,255,0.85);
    margin: 0;
    font-weight: 400;
}

/* ── Section cards ── */
.section-card {
    background: #ffffff;
    border-radius: 16px;
    padding: 28px 28px 24px 28px;
    box-shadow: 0 4px 24px rgba(79,70,229,0.08);
    border: 1px solid rgba(79,70,229,0.08);
    margin-bottom: 24px;
    transition: box-shadow 0.2s;
}
.section-card:hover {
    box-shadow: 0 8px 32px rgba(79,70,229,0.14);
}

/* ── Section heading ── */
.section-heading {
    font-size: 1.2rem;
    font-weight: 700;
    color: #1e1b4b;
    margin: 0 0 18px 0;
    display: flex;
    align-items: center;
    gap: 8px;
}

/* ── Stat cards ── */
.stat-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 16px;
    margin-bottom: 24px;
}
.stat-card {
    background: #ffffff;
    border-radius: 14px;
    padding: 22px 20px;
    text-align: center;
    box-shadow: 0 2px 12px rgba(79,70,229,0.08);
    border: 1px solid rgba(79,70,229,0.06);
}
.stat-number {
    font-size: 2rem;
    font-weight: 800;
    background: linear-gradient(135deg, #4f46e5, #a855f7);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.stat-label {
    font-size: 0.82rem;
    color: #6b7280;
    font-weight: 500;
    margin-top: 4px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

/* ── Prediction bar ── */
.pred-row {
    background: linear-gradient(135deg, #f8f7ff, #fdf4ff);
    border-radius: 12px;
    padding: 14px 18px;
    margin-bottom: 10px;
    border: 1px solid rgba(79,70,229,0.1);
}
.pred-label {
    font-weight: 600;
    color: #1e1b4b;
    font-size: 0.95rem;
    margin-bottom: 6px;
}
.pred-bar-bg {
    background: #e5e7eb;
    border-radius: 999px;
    height: 8px;
    overflow: hidden;
    margin-bottom: 4px;
}
.pred-bar-fill {
    height: 8px;
    border-radius: 999px;
    background: linear-gradient(90deg, #4f46e5, #a855f7);
    transition: width 0.5s ease;
}
.pred-pct {
    font-size: 0.8rem;
    color: #7c3aed;
    font-weight: 600;
    text-align: right;
}

/* ── Best prediction card ── */
.best-pred-card {
    background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
    border-radius: 16px;
    padding: 24px;
    color: white;
    text-align: center;
    margin-bottom: 20px;
    box-shadow: 0 8px 30px rgba(79,70,229,0.3);
}
.best-pred-label {
    font-size: 0.8rem;
    text-transform: uppercase;
    letter-spacing: 1px;
    opacity: 0.8;
    margin-bottom: 6px;
}
.best-pred-value {
    font-size: 1.6rem;
    font-weight: 800;
    margin: 0;
}
.best-pred-conf {
    font-size: 0.95rem;
    opacity: 0.85;
    margin-top: 4px;
}

/* ── Tag badge ── */
.badge {
    display: inline-block;
    background: linear-gradient(135deg, #ede9fe, #fae8ff);
    color: #6d28d9;
    font-size: 0.78rem;
    font-weight: 600;
    padding: 4px 12px;
    border-radius: 999px;
    margin: 2px;
    border: 1px solid rgba(109,40,217,0.15);
}

/* ── OCR text area ── */
.stTextArea textarea {
    border-radius: 12px !important;
    border: 1.5px solid #c4b5fd !important;
    font-family: 'Courier New', monospace !important;
    font-size: 0.9rem !important;
    background: #fafafa !important;
    color: #1e1b4b !important;
}

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #4f46e5, #7c3aed) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 12px 28px !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    letter-spacing: 0.3px !important;
    box-shadow: 0 4px 15px rgba(79,70,229,0.35) !important;
    transition: all 0.2s !important;
    width: 100%;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(79,70,229,0.45) !important;
}

/* ── Download buttons ── */
.stDownloadButton > button {
    background: linear-gradient(135deg, #059669, #10b981) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 10px 22px !important;
    font-weight: 600 !important;
    box-shadow: 0 4px 15px rgba(5,150,105,0.3) !important;
}
.stDownloadButton > button:hover {
    box-shadow: 0 6px 20px rgba(5,150,105,0.4) !important;
}

/* ── File uploader ── */
[data-testid="stFileUploader"] {
    background: linear-gradient(135deg, #f8f7ff, #fdf4ff) !important;
    border: 2px dashed #a78bfa !important;
    border-radius: 16px !important;
    padding: 8px !important;
}

/* ── Radio buttons ── */
.stRadio > div { gap: 12px; }
.stRadio > div > label {
    background: #f8f7ff !important;
    border: 1.5px solid #c4b5fd !important;
    border-radius: 12px !important;
    padding: 10px 20px !important;
    cursor: pointer !important;
    transition: all 0.2s !important;
    color: #1e1b4b !important;
    font-weight: 500 !important;
}
.stRadio > div > label:hover {
    background: #ede9fe !important;
    border-color: #7c3aed !important;
}

/* ── Metric cards ── */
[data-testid="stMetric"] {
    background: #ffffff !important;
    border: 1px solid rgba(79,70,229,0.1) !important;
    border-radius: 14px !important;
    padding: 18px 20px !important;
    box-shadow: 0 2px 12px rgba(79,70,229,0.07) !important;
}
[data-testid="stMetricLabel"] { color: #6b7280 !important; font-weight: 500 !important; }
[data-testid="stMetricValue"] { color: #1e1b4b !important; font-weight: 800 !important; }

/* ── Dataframe ── */
[data-testid="stDataFrame"] {
    border-radius: 14px !important;
    overflow: hidden !important;
    box-shadow: 0 2px 16px rgba(79,70,229,0.08) !important;
}

/* ── Alert boxes ── */
.stSuccess {
    background: linear-gradient(135deg, #ecfdf5, #d1fae5) !important;
    border: 1px solid #6ee7b7 !important;
    border-radius: 12px !important;
    color: #065f46 !important;
}
.stWarning {
    background: linear-gradient(135deg, #fffbeb, #fef3c7) !important;
    border: 1px solid #fcd34d !important;
    border-radius: 12px !important;
    color: #92400e !important;
}

/* ── Spinner ── */
.stSpinner > div > div { border-top-color: #7c3aed !important; }

/* ── Expander ── */
.streamlit-expanderHeader {
    background: linear-gradient(135deg, #f8f7ff, #fdf4ff) !important;
    border-radius: 12px !important;
    border: 1px solid rgba(79,70,229,0.12) !important;
    color: #1e1b4b !important;
    font-weight: 600 !important;
}

/* ── Divider ── */
hr { border-color: rgba(79,70,229,0.1) !important; }

/* ── Footer ── */
.footer {
    background: linear-gradient(135deg, #1e1b4b, #312e81);
    border-radius: 16px;
    padding: 28px 20px;
    text-align: center;
    margin-top: 32px;
    color: rgba(255,255,255,0.85);
}
.footer h4 { color: #ffffff; margin: 0 0 8px 0; font-size: 1.1rem; }
.footer p  { margin: 4px 0; font-size: 0.85rem; color: rgba(255,255,255,0.6); }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# Create Required Folders & History File
# ─────────────────────────────────────────────
os.makedirs("uploads", exist_ok=True)
os.makedirs("results", exist_ok=True)

if not os.path.exists("history.csv"):
    pd.DataFrame(columns=["Time", "File Name", "Task", "Prediction", "Confidence"]
                 ).to_csv("history.csv", index=False)

# ─────────────────────────────────────────────
# Sidebar
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 20px 0 10px 0;'>
        <div style='font-size:3rem;'>🔮</div>
        <h2 style='color:#ffffff; margin:8px 0 4px 0; font-size:1.3rem; font-weight:800;'>VisionAI</h2>
        <p style='color:rgba(255,255,255,0.6); font-size:0.8rem; margin:0;'>Powered by ResNet50 & EasyOCR</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("""
    <p style='color:#c7d2fe; font-size:0.75rem; font-weight:700;
              text-transform:uppercase; letter-spacing:1px; margin-bottom:10px;'>
        ✦ Capabilities
    </p>
    """, unsafe_allow_html=True)

    features = [
        ("🖼️", "Image Recognition", "ResNet50 top-5 predictions"),
        ("📝", "OCR Text Extraction", "Powered by EasyOCR"),
        ("📊", "Confidence Scores", "Per-prediction accuracy"),
        ("📜", "Prediction History", "Full session log"),
        ("💾", "Download Reports", "TXT & CSV export"),
    ]
    for icon, title, desc in features:
        st.markdown(f"""
        <div style='background:rgba(255,255,255,0.07); border:1px solid rgba(255,255,255,0.1);
                    border-radius:10px; padding:10px 14px; margin-bottom:8px;'>
            <div style='font-size:0.95rem; font-weight:600; color:#e0e7ff;'>{icon} {title}</div>
            <div style='font-size:0.78rem; color:rgba(255,255,255,0.5); margin-top:2px;'>{desc}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("""
    <p style='color:#c7d2fe; font-size:0.75rem; font-weight:700;
              text-transform:uppercase; letter-spacing:1px; margin-bottom:10px;'>
        ✦ Tech Stack
    </p>
    <div style='background:rgba(255,255,255,0.07); border:1px solid rgba(255,255,255,0.1);
                border-radius:10px; padding:14px 16px;'>
        <div style='color:#e0e7ff; font-size:0.85rem; line-height:1.8;'>
            🔷 <b>Model</b>: ResNet50<br>
            🔷 <b>OCR</b>: EasyOCR<br>
            🔷 <b>Framework</b>: Streamlit<br>
            🔷 <b>DL</b>: PyTorch<br>
            🔷 <b>Vision</b>: OpenCV + Pillow
        </div>
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# Hero Banner
# ─────────────────────────────────────────────
st.markdown("""
<div class="hero-banner">
    <div class="hero-title">🔮 VisionAI Recognition System</div>
    <p class="hero-subtitle">
        Upload any image · Identify objects with ResNet50 · Extract text with EasyOCR
    </p>
    <div style='margin-top:16px; display:flex; gap:10px; justify-content:center; flex-wrap:wrap;'>
        <span class="badge">⚡ ResNet50</span>
        <span class="badge">📖 EasyOCR</span>
        <span class="badge">🎯 Top-5 Predictions</span>
        <span class="badge">📥 Downloadable Reports</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# Upload & Task Selection
# ─────────────────────────────────────────────
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown('<p class="section-heading">📁 Upload & Configure</p>', unsafe_allow_html=True)

upload_col, task_col = st.columns([3, 2], gap="large")

with upload_col:
    uploaded_file = st.file_uploader(
        "Drop your image here (JPG, JPEG, PNG)",
        type=["jpg", "jpeg", "png"],
        label_visibility="visible"
    )

with task_col:
    st.markdown("**Select Analysis Mode**")
    task = st.radio(
        "Task",
        ["🖼️ Image Recognition", "📝 Text Recognition"],
        label_visibility="collapsed"
    )
    task = task.split(" ", 1)[1]   # strip the emoji prefix

st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# Main Analysis Section
# ─────────────────────────────────────────────
if uploaded_file is not None:

    image = Image.open(uploaded_file)
    filepath = os.path.join("uploads", uploaded_file.name)
    image.save(filepath)

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<p class="section-heading">🖼️ Preview & Analyze</p>', unsafe_allow_html=True)

    img_col, ctrl_col = st.columns([3, 2], gap="large")

    with img_col:
        st.markdown("**Uploaded Image**")
        st.image(image, use_container_width=True)
        st.markdown(f"""
        <div style='margin-top:8px; display:flex; gap:8px; flex-wrap:wrap;'>
            <span class='badge'>📄 {uploaded_file.name}</span>
            <span class='badge'>📐 {image.width} × {image.height} px</span>
            <span class='badge'>🎨 {image.mode}</span>
        </div>
        """, unsafe_allow_html=True)

    with ctrl_col:
        st.markdown("**Selected Mode**")
        st.markdown(f"""
        <div style='background:linear-gradient(135deg,#ede9fe,#fae8ff);
                    border:1.5px solid #c4b5fd; border-radius:14px;
                    padding:16px 20px; margin-bottom:18px;'>
            <div style='font-size:1.1rem; font-weight:700; color:#4f46e5;'>
                {"🖼️" if task == "Image Recognition" else "📝"} {task}
            </div>
            <div style='font-size:0.82rem; color:#6d28d9; margin-top:4px;'>
                {"ResNet50 — Top 5 class predictions" if task == "Image Recognition"
                 else "EasyOCR — Full text extraction"}
            </div>
        </div>
        """, unsafe_allow_html=True)
        analyze = st.button("🚀 Analyze Image", use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # ─────────────────────────────────────────
    # Results
    # ─────────────────────────────────────────
    if analyze:

        with st.spinner("⚙️ Running AI model — please wait..."):

            # ══════════════════════════════════
            # IMAGE RECOGNITION
            # ══════════════════════════════════
            if task == "Image Recognition":

                predictions = classify_image(image)
                prediction  = predictions[0]["label"]
                confidence  = predictions[0]["confidence"]

                st.markdown('<div class="section-card">', unsafe_allow_html=True)
                st.markdown('<p class="section-heading">🎯 Recognition Results</p>',
                            unsafe_allow_html=True)

                # Best prediction highlight
                st.markdown(f"""
                <div class="best-pred-card">
                    <div class="best-pred-label">🏆 Best Prediction</div>
                    <div class="best-pred-value">{prediction}</div>
                    <div class="best-pred-conf">Confidence: {confidence:.2f}%</div>
                </div>
                """, unsafe_allow_html=True)

                # Top 5 prediction bars
                st.markdown("**Top 5 Predictions**")
                colors = ["#4f46e5", "#7c3aed", "#a855f7", "#c084fc", "#ddd6fe"]
                for i, item in enumerate(predictions):
                    pct = item["confidence"]
                    width = f"{pct:.1f}%"
                    st.markdown(f"""
                    <div class="pred-row">
                        <div class="pred-label">#{i+1} &nbsp; {item['label']}</div>
                        <div class="pred-bar-bg">
                            <div class="pred-bar-fill" style="width:{width};
                                 background:linear-gradient(90deg,{colors[i]},{colors[min(i+1,4)]});"></div>
                        </div>
                        <div class="pred-pct">{pct:.2f}%</div>
                    </div>
                    """, unsafe_allow_html=True)

                st.markdown('</div>', unsafe_allow_html=True)

                # Save history
                history = pd.read_csv("history.csv")
                history.loc[len(history)] = [datetime.now(), uploaded_file.name,
                                             task, prediction, round(confidence, 2)]
                history.to_csv("history.csv", index=False)

                # Download
                top5_lines = "\n".join(
                    f"  {i+1}. {p['label']} - {p['confidence']:.2f}%"
                    for i, p in enumerate(predictions)
                )
                report = (
                    "AI IMAGE RECOGNITION REPORT\n"
                    "=" * 46 + "\n"
                    f"  File Name   : {uploaded_file.name}\n"
                    f"  Prediction  : {prediction}\n"
                    f"  Confidence  : {confidence:.2f} %\n"
                    f"  Generated   : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                    "=" * 46 + "\n"
                    "  Top 5 Predictions:\n"
                    f"{top5_lines}\n"
                    "=" * 46 + "\n"
                )
                st.success("✅ Image Recognition completed successfully!")
                st.download_button("📥 Download Prediction Report", data=report,
                                   file_name="prediction_report.txt", mime="text/plain")

            # ══════════════════════════════════
            # OCR TEXT RECOGNITION
            # ══════════════════════════════════
            else:

                extracted_text, score, count = read_text(filepath)
                boxed_image = draw_boxes(filepath)

                st.markdown('<div class="section-card">', unsafe_allow_html=True)
                st.markdown('<p class="section-heading">📝 OCR Results</p>',
                            unsafe_allow_html=True)

                ocr_col1, ocr_col2 = st.columns([3, 2], gap="large")

                with ocr_col1:
                    st.markdown("**Extracted Text**")
                    st.text_area("", extracted_text, height=260, label_visibility="collapsed")

                with ocr_col2:
                    st.markdown("**OCR Metrics**")
                    st.markdown(f"""
                    <div style='display:grid; gap:12px;'>
                        <div class="stat-card">
                            <div class="stat-number">{score:.1f}%</div>
                            <div class="stat-label">OCR Confidence</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-number">{count}</div>
                            <div class="stat-label">Text Regions Found</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                st.markdown("**Detected Text Regions**")
                st.image(boxed_image, use_container_width=True)

                st.markdown('</div>', unsafe_allow_html=True)

                # Save history
                history = pd.read_csv("history.csv")
                history.loc[len(history)] = [datetime.now(), uploaded_file.name,
                                             task, "Text Extracted", round(score, 2)]
                history.to_csv("history.csv", index=False)

                st.success("✅ OCR Text Extraction completed successfully!")
                st.download_button("📥 Download Extracted Text", data=extracted_text,
                                   file_name="ocr_result.txt", mime="text/plain")

# ─────────────────────────────────────────────
# History Dashboard
# ─────────────────────────────────────────────
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown('<p class="section-heading">📊 Prediction History</p>', unsafe_allow_html=True)

history = pd.read_csv("history.csv")

if history.empty:
    st.markdown("""
    <div style='text-align:center; padding:40px 20px; color:#9ca3af;'>
        <div style='font-size:3rem; margin-bottom:12px;'>📭</div>
        <div style='font-size:1rem; font-weight:500;'>No predictions yet</div>
        <div style='font-size:0.85rem; margin-top:4px;'>Upload an image and run analysis to get started.</div>
    </div>
    """, unsafe_allow_html=True)

else:
    total  = len(history)
    img_n  = len(history[history["Task"] == "Image Recognition"])
    text_n = len(history[history["Task"] == "Text Recognition"])

    st.markdown(f"""
    <div class="stat-grid">
        <div class="stat-card">
            <div class="stat-number">{total}</div>
            <div class="stat-label">Total Predictions</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">{img_n}</div>
            <div class="stat-label">Image Recognition</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">{text_n}</div>
            <div class="stat-label">Text Recognition</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.dataframe(history, use_container_width=True, hide_index=True)

    dl_col, clr_col = st.columns([3, 1])
    with dl_col:
        csv = history.to_csv(index=False).encode("utf-8")
        st.download_button("📥 Download History CSV", data=csv,
                           file_name="history.csv", mime="text/csv")
    with clr_col:
        if st.button("🗑️ Clear History", use_container_width=True):
            history.iloc[0:0].to_csv("history.csv", index=False)
            st.success("History cleared.")
            st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# About
# ─────────────────────────────────────────────
with st.expander("ℹ️  About VisionAI"):
    st.markdown("""
    **VisionAI** is an intelligent image analysis platform combining state-of-the-art computer vision
    and optical character recognition into a single, easy-to-use interface.

    | Capability | Technology |
    |---|---|
    | Image Classification | ResNet50 (ImageNet, 1000 classes) |
    | Optical Character Recognition | EasyOCR (multi-language) |
    | Deep Learning Framework | PyTorch |
    | UI Framework | Streamlit |
    | Image Processing | OpenCV + Pillow |

    **How to use:**
    1. Upload a JPG / PNG image using the file uploader above.
    2. Select *Image Recognition* to identify objects or *Text Recognition* to extract text.
    3. Click **Analyze Image** and view the results instantly.
    4. Download the report or view session history below.
    """)

# ─────────────────────────────────────────────
# Footer
# ─────────────────────────────────────────────
st.markdown("""
<div class="footer">
    <h4>🔮 VisionAI – Image & Text Recognition</h4>
    <p>Powered by ResNet50 · EasyOCR · PyTorch · Streamlit</p>
    <p>© 2026 · Built with ❤️ using Python</p>
</div>
""", unsafe_allow_html=True)
