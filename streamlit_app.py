
import base64
from io import BytesIO

import requests
import streamlit as st
from PIL import Image

# ==========================================
# CONFIG
# ==========================================
API_URL = "https://floodvision-ai-2.onrender.com/predict"

st.set_page_config(
    page_title="FloodVision AI",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ==========================================
# DARK PURPLE THEME
# ==========================================
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Prompt:wght@300;400;500;600;700&display=swap');

    .stApp {
        background:
            radial-gradient(ellipse at top left, #24103D 0%, transparent 40%),
            linear-gradient(145deg, #0B0712, #120B20 55%, #090610);
        color: #F0E9FF;
        font-family: 'Prompt', sans-serif;
    }

    [data-testid="stHeader"] {
        background: rgba(11, 7, 18, 0.8);
    }

    .block-container {
        max-width: 1200px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    h1, h2, h3, p, label, .stMarkdown {
        font-family: 'Prompt', sans-serif;
    }

    .hero {
        background: linear-gradient(115deg, #1A0B2E, #35145B 60%, #5725A0);
        border: 1px solid #7443B8;
        border-radius: 24px;
        padding: 2.4rem;
        margin-bottom: 1.7rem;
        box-shadow: 0 12px 40px rgba(139, 92, 246, 0.15);
    }

    .hero-label {
        color: #C4B5FD;
        font-size: 0.8rem;
        letter-spacing: 3px;
        font-weight: 600;
    }

    .hero h1 {
        color: #FFFFFF;
        font-size: clamp(2rem, 4vw, 3rem);
        font-weight: 700;
        margin: 0.5rem 0;
    }

    .hero p {
        color: #DDD0FF;
        line-height: 1.9;
        margin-bottom: 0;
    }

    .section-title {
        color: #E9D5FF;
        font-size: 1.35rem;
        font-weight: 600;
        margin: 1.4rem 0 0.35rem;
    }

    .section-desc {
        color: #B5A5CC;
        font-size: 0.92rem;
        margin-bottom: 1rem;
    }

    [data-testid="stVerticalBlockBorderWrapper"] {
        background: rgba(23, 14, 37, 0.85);
        border: 1px solid #48266A;
        border-radius: 20px;
    }

    [data-testid="stFileUploader"] {
        background: #130D20;
        border: 1px dashed #9461D9;
        border-radius: 15px;
        padding: 1rem;
    }

    [data-testid="stFileUploader"] section {
        background: transparent;
    }

    [data-testid="stFileUploader"] small {
        color: #C4B5FD;
    }

    .stButton > button {
        background: linear-gradient(100deg, #7C3AED, #A855F7);
        color: #FFFFFF;
        border: 1px solid #B794F6;
        border-radius: 12px;
        min-height: 3rem;
        font-weight: 600;
        box-shadow: 0 0 20px rgba(139, 92, 246, 0.18);
        transition: all 0.2s ease;
    }

    .stButton > button:hover {
        background: linear-gradient(100deg, #6D28D9, #9333EA);
        color: white;
        border-color: #D8B4FE;
        transform: translateY(-1px);
    }

    [data-testid="stMetric"] {
        background: linear-gradient(145deg, #211331, #150D21);
        border: 1px solid #58317C;
        border-radius: 17px;
        padding: 1.15rem;
    }

    [data-testid="stMetricLabel"] {
        color: #C4B5FD;
    }

    [data-testid="stMetricValue"] {
        color: #D8B4FE;
        font-weight: 700;
    }

    [data-testid="stAlert"] {
        border-radius: 14px;
    }

    [data-testid="stImage"] img {
        border-radius: 13px;
    }

    hr {
        border-color: #392449;
    }

    .footer {
        text-align: center;
        color: #9F8CB8;
        font-size: 0.82rem;
        padding-top: 1.5rem;
        margin-top: 2rem;
        border-top: 1px solid #352344;
        line-height: 1.9;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ==========================================
# HEADER
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
# UPLOAD
# ==========================================
st.markdown(
    '<div class="section-title">📷 วิเคราะห์ภาพน้ำท่วม | Flood Image Analysis</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="section-desc">อัปโหลดภาพพื้นที่ แล้วให้ AI วิเคราะห์ผลเบื้องต้น</div>',
    unsafe_allow_html=True,
)

with st.container(border=True):
    uploaded_file = st.file_uploader(
        "เลือกภาพพื้นที่ที่ต้องการวิเคราะห์ (JPG, JPEG, PNG)",
        type=["jpg", "jpeg", "png"],
    )

    if uploaded_file is not None:
        try:
            original_image = Image.open(uploaded_file).convert("RGB")

            st.caption(
                f"ไฟล์: {uploaded_file.name} · "
                f"ขนาด: {original_image.width} × {original_image.height} px"
            )

            st.image(
                original_image,
                caption="ภาพที่อัปโหลด | Uploaded Image",
                use_container_width=True,
            )

            if st.button(
                "🌊 เริ่มวิเคราะห์ภาพ | Analyze Image",
                type="primary",
                use_container_width=True,
            ):
                with st.spinner("AI กำลังวิเคราะห์ภาพ... Please wait."):
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

                    st.session_state["flood_result"] = {
                        "original": original_image.copy(),
                        "mask": mask_image.copy(),
                        "data": result,
                        "filename": uploaded_file.name,
                    }
                    st.success("วิเคราะห์ภาพเสร็จแล้ว | Analysis complete")

                else:
                    st.error(
                        f"วิเคราะห์ไม่สำเร็จ (HTTP {response.status_code})"
                    )
                    st.code(response.text[:1500])

        except requests.exceptions.Timeout:
            st.error("ระบบใช้เวลานานเกินไป กรุณาลองใหม่อีกครั้ง")

        except requests.exceptions.RequestException as exc:
            st.error("เชื่อมต่อ Backend ไม่สำเร็จ")
            st.code(str(exc))

        except Exception as exc:
            st.error("เกิดข้อผิดพลาดระหว่างอ่านภาพหรือประมวลผล")
            st.code(str(exc))

# ==========================================
# RESULTS
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
        '<div class="section-desc">เปรียบเทียบภาพต้นฉบับและผล Mask จากโมเดล AI</div>',
        unsafe_allow_html=True,
    )

    left, right = st.columns(2, gap="large")

    with left:
        st.markdown("**🖼️ ภาพต้นฉบับ | Original Image**")
        st.image(saved["original"], use_container_width=True)

    with right:
        st.markdown("**🗺️ ผลการทำนาย | Predicted Mask**")
        st.image(saved["mask"], use_container_width=True)
        st.caption("สีขาว = พื้นที่ที่โมเดลทำนายว่าเป็นน้ำท่วม")

    metric1, metric2 = st.columns(2)

    with metric1:
        st.metric(
            "สัดส่วนพิกเซลที่ทำนายว่าน้ำท่วม",
            f"{result['flood_percent']:.2f}%",
        )

    with metric2:
        st.metric("Model Input Size", "256 × 256 px")

    st.markdown("### ✨ สรุปผล | Analysis Summary")
    st.info(result.get("summary", "ไม่มีข้อมูลสรุปจาก API"))

    st.caption(
        "หมายเหตุ: เปอร์เซ็นต์เป็นสัดส่วนพิกเซลที่โมเดลทำนาย "
        "ไม่ใช่พื้นที่จริงทางภูมิศาสตร์หรือการยืนยันสถานการณ์จริง"
    )

    if st.button("🗑️ ล้างผลการวิเคราะห์"):
        st.session_state.pop("flood_result", None)
        st.rerun()

# ==========================================
# FOOTER
# ==========================================
st.markdown(
    """
    <div class="footer">
        🌊 FloodVision AI · AI-Powered Flood Image Analysis<br>
        ระบบสนับสนุนการวิเคราะห์ภาพน้ำท่วมด้วย AI
    </div>
    """,
    unsafe_allow_html=True,
)
