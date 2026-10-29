
import base64
from io import BytesIO

import requests
import streamlit as st
from PIL import Image

# ==========================================
# CONFIGURATION
# ==========================================
API_URL = "https://floodvision-ai-2.onrender.com/predict"

st.set_page_config(
    page_title="FloodVision AI | Flood Analysis",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ==========================================
# CUSTOM CSS
# ==========================================
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Prompt:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"], [data-testid="stAppViewContainer"] {
        font-family: 'Prompt', sans-serif;
    }

    .stApp {
        background: linear-gradient(180deg, #f0f7ff 0%, #f8fbff 45%, #ffffff 100%);
        color: #16324f;
    }

    [data-testid="stHeader"] {
        background: rgba(240, 247, 255, 0.8);
    }

    .block-container {
        max-width: 1200px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    .hero {
        background: linear-gradient(120deg, #0b1f45 0%, #124b83 55%, #0788c9 100%);
        padding: 2.4rem 2.6rem;
        border-radius: 24px;
        color: white;
        margin-bottom: 1.5rem;
        box-shadow: 0 14px 35px rgba(14, 73, 130, 0.18);
    }

    .hero-label {
        color: #8fe5ff;
        font-size: 0.82rem;
        letter-spacing: 2px;
        font-weight: 600;
        margin-bottom: 0.7rem;
    }

    .hero h1 {
        color: white;
        font-size: clamp(2rem, 4vw, 3rem);
        font-weight: 700;
        margin: 0;
        line-height: 1.25;
    }

    .hero p {
        color: #e1f2ff;
        font-size: 1rem;
        margin-top: 0.9rem;
        margin-bottom: 0;
        line-height: 1.8;
    }

    .section-title {
        color: #123a65;
        font-size: 1.35rem;
        font-weight: 600;
        margin: 1.2rem 0 0.4rem 0;
    }

    .section-desc {
        color: #60758d;
        font-size: 0.93rem;
        margin-bottom: 1rem;
    }

    .upload-card {
        background: white;
        border: 1px solid #d8e8f7;
        border-radius: 20px;
        padding: 1.5rem;
        box-shadow: 0 6px 22px rgba(27, 78, 125, 0.06);
        margin-bottom: 1.2rem;
    }

    .info-card {
        background: white;
        border: 1px solid #dceaf7;
        border-radius: 18px;
        padding: 1.2rem 1.3rem;
        box-shadow: 0 5px 18px rgba(27, 78, 125, 0.05);
        height: 100%;
    }

    .info-card .label {
        color: #71859b;
        font-size: 0.85rem;
        margin-bottom: 0.4rem;
    }

    .info-card .value {
        color: #075985;
        font-size: 1.45rem;
        font-weight: 700;
    }

    .result-heading {
        color: #123a65;
        font-size: 1.08rem;
        font-weight: 600;
        margin: 0.5rem 0 0.7rem 0;
    }

    .stButton > button {
        background: linear-gradient(100deg, #0879c9, #05a4d6);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 1.2rem;
        font-weight: 600;
        min-height: 3rem;
        transition: all 0.2s ease;
        box-shadow: 0 5px 14px rgba(8, 121, 201, 0.16);
    }

    .stButton > button:hover {
        background: linear-gradient(100deg, #0666aa, #078bb9);
        color: white;
        border: none;
        transform: translateY(-1px);
    }

    [data-testid="stFileUploader"] {
        background: #f7fbff;
        border: 1px dashed #87bce7;
        border-radius: 14px;
        padding: 0.8rem;
    }

    [data-testid="stMetric"] {
        background: white;
        border: 1px solid #dceaf7;
        border-radius: 16px;
        padding: 1rem 1.2rem;
        box-shadow: 0 5px 18px rgba(27, 78, 125, 0.05);
    }

    [data-testid="stMetricLabel"] {
        color: #60758d;
    }

    [data-testid="stMetricValue"] {
        color: #0879c9;
        font-weight: 700;
    }

    .footer {
        text-align: center;
        color: #8294a8;
        font-size: 0.82rem;
        padding-top: 1.5rem;
        margin-top: 2.5rem;
        border-top: 1px solid #e0ebf5;
    }

    </style>
    """,
    unsafe_allow_html=True,
)

# ==========================================
# HERO HEADER
# ==========================================
st.markdown(
    """
    <div class="hero">
        <div class="hero-label">AI-POWERED FLOOD ANALYSIS</div>
        <h1>🌊 FloodVision AI</h1>
        <p>
            ระบบวิเคราะห์ภาพน้ำท่วมด้วยปัญญาประดิษฐ์<br>
            Intelligent Image Segmentation for Flood Assessment
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ==========================================
# UPLOAD SECTION
# ==========================================
st.markdown(
    '<div class="section-title">📷 วิเคราะห์ภาพน้ำท่วม | Flood Image Analysis</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="section-desc">อัปโหลดภาพพื้นที่ที่ต้องการตรวจสอบ แล้วกดปุ่มเพื่อเริ่มวิเคราะห์ด้วย AI</div>',
    unsafe_allow_html=True,
)

with st.container(border=True):
    uploaded_file = st.file_uploader(
        "เลือกภาพพื้นที่ (JPG, JPEG, PNG)",
        type=["jpg", "jpeg", "png"],
        help="เลือกภาพพื้นที่ที่ต้องการให้โมเดลวิเคราะห์",
    )

    if uploaded_file is not None:
        original_image = Image.open(uploaded_file).convert("RGB")

        st.caption(
            f"ชื่อไฟล์: {uploaded_file.name} · "
            f"ขนาดภาพ: {original_image.width} × {original_image.height} px"
        )

        analyze = st.button(
            "🌊 เริ่มวิเคราะห์ภาพ | Analyze Image",
            type="primary",
            use_container_width=True,
        )

        if analyze:
            try:
                with st.spinner(
                    "กำลังเชื่อมต่อ AI และวิเคราะห์ภาพ... Please wait."
                ):
                    response = requests.post(
                        API_URL,
                        files={
                            "file": (
                                uploaded_file.name,
                                uploaded_file.getvalue(),
                                uploaded_file.type or "image/jpeg",
                            )
                        },
                        timeout=180,
                    )

                if response.status_code == 200:
                    result = response.json()

                    mask_data = result["mask"].split(",", 1)[1]
                    mask_bytes = base64.b64decode(mask_data)
                    mask_image = Image.open(
                        BytesIO(mask_bytes)
                    ).convert("L")

                    # Keep results in session state so they remain visible
                    # after Streamlit reruns.
                    st.session_state["flood_result"] = {
                        "original": original_image.copy(),
                        "mask": mask_image.copy(),
                        "data": result,
                        "filename": uploaded_file.name,
                    }

                else:
                    st.error(
                        f"วิเคราะห์ไม่สำเร็จ | HTTP {response.status_code}"
                    )
                    st.code(response.text[:1500])

            except requests.exceptions.Timeout:
                st.error(
                    "เซิร์ฟเวอร์ใช้เวลาประมวลผลนานเกินไป "
                    "กรุณาลองใหม่อีกครั้ง"
                )

            except requests.exceptions.RequestException as exc:
                st.error("ไม่สามารถเชื่อมต่อ Backend API ได้")
                st.code(str(exc))

            except Exception as exc:
                st.error("เกิดข้อผิดพลาดระหว่างประมวลผลภาพ")
                st.code(str(exc))

# ==========================================
# ANALYSIS RESULTS
# ==========================================
saved = st.session_state.get("flood_result")

if saved is not None:
    result = saved["data"]

    st.markdown("---")
    st.markdown(
        '<div class="section-title">📊 ผลการวิเคราะห์ | Analysis Results</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="section-desc">เปรียบเทียบภาพต้นฉบับกับผลการแบ่งส่วนภาพจากโมเดล</div>',
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown(
            '<div class="result-heading">🖼️ ภาพต้นฉบับ | Original Image</div>',
            unsafe_allow_html=True,
        )
        st.image(
            saved["original"],
            use_container_width=True,
        )

    with col2:
        st.markdown(
            '<div class="result-heading">🗺️ ภาพผลทำนาย | Predicted Mask</div>',
            unsafe_allow_html=True,
        )
        st.image(
            saved["mask"],
            use_container_width=True,
        )
        st.caption("สีขาว = โมเดลทำนายว่าเป็นพื้นที่น้ำท่วม")

    st.markdown("")

    metric_col1, metric_col2 = st.columns(2)

    with metric_col1:
        st.metric(
            "สัดส่วนพิกเซลที่ทำนายว่าน้ำท่วม",
            f"{result['flood_percent']:.2f}%",
        )

    with metric_col2:
        st.metric(
            "Model Input Size",
            "256 × 256 px",
        )

    st.markdown(
        """
        <div class="info-card">
            <div class="label">ANALYSIS SUMMARY | สรุปผล</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.info(result.get("summary", "ไม่มีข้อมูลสรุปจาก API"))

    st.caption(
        "ข้อควรทราบ: ค่าเปอร์เซ็นต์คือสัดส่วนพิกเซลที่โมเดลจัดเป็นน้ำท่วม "
        "ไม่ใช่เปอร์เซ็นต์พื้นที่จริงทางภูมิศาสตร์ และไม่ใช่การยืนยันสถานการณ์น้ำท่วม"
    )

    if st.button("🗑️ ล้างผลการวิเคราะห์"):
        del st.session_state["flood_result"]
        st.rerun()

# ==========================================
# FOOTER
# ==========================================
st.markdown(
    """
    <div class="footer">
        FloodVision AI · AI-Powered Flood Image Analysis<br>
        ระบบสนับสนุนการวิเคราะห์ภาพน้ำท่วมด้วย AI
    </div>
    """,
    unsafe_allow_html=True,
)
