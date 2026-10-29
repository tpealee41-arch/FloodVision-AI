
import base64
from io import BytesIO

import requests
import streamlit as st
from PIL import Image

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="FloodVision AI",
    page_icon="💜",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# =========================
# API CONFIG
# =========================
API_URL = "https://floodvision-ai-2.onrender.com/predict"

# =========================
# PURPLE & WHITE THEME
# =========================
st.markdown("""
<style>
/* Main background */
.stApp {
    background: #F8F7FF;
    color: #35284D;
}

/* Main content width */
.block-container {
    max-width: 1100px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* Headings */
h1, h2, h3 {
    color: #4C347D !important;
    font-weight: 700;
}

/* General text */
p, label, .stMarkdown {
    color: #514568;
}

/* Header */
.hero {
    background: linear-gradient(135deg, #EDE7FF, #FFFFFF);
    border: 1px solid #E5DDF8;
    border-radius: 24px;
    padding: 30px;
    margin-bottom: 25px;
    text-align: center;
}

.hero-title {
    color: #4C347D;
    font-size: 2.5rem;
    font-weight: 800;
    margin-bottom: 8px;
}

.hero-subtitle {
    color: #75658E;
    font-size: 1rem;
}

/* White cards */
.card {
    background: #FFFFFF;
    border: 1px solid #E8E0F7;
    border-radius: 18px;
    padding: 22px;
    margin-bottom: 18px;
}

/* File uploader */
div[data-testid="stFileUploader"] {
    background: #FFFFFF;
    border: 1px solid #E5DDF8;
    border-radius: 16px;
    padding: 12px;
}

[data-testid="stFileUploaderDropzone"] {
    background: #FDFCFF;
    border: 2px dashed #C8B8EF;
    border-radius: 14px;
}

/* Buttons */
.stButton > button {
    background: #8B72D9;
    color: #FFFFFF;
    border: none;
    border-radius: 12px;
    padding: 0.7rem 1.2rem;
    font-weight: 600;
    transition: all 0.2s ease;
}

.stButton > button:hover {
    background: #7054BD;
    color: #FFFFFF;
    border: none;
}

/* Metrics */
div[data-testid="stMetric"] {
    background: #FFFFFF;
    border: 1px solid #E8E0F7;
    padding: 18px;
    border-radius: 16px;
}

div[data-testid="stMetricLabel"] {
    color: #75658E;
}

div[data-testid="stMetricValue"] {
    color: #4C347D;
}

/* Alerts */
div[data-testid="stAlert"] {
    border-radius: 12px;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #F0EBFC;
}

/* Divider */
hr {
    border-color: #E5DDF8;
}

/* Hide Streamlit branding */
#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header[data-testid="stHeader"] {
    background: rgba(248, 247, 255, 0.8);
}
</style>
""", unsafe_allow_html=True)

# =========================
# HEADER
# =========================
st.markdown("""
<div class="hero">
    <div class="hero-title">💜 FloodVision AI</div>
    <div class="hero-subtitle">
        AI-powered Flood Image Segmentation
        <br>
        วิเคราะห์ภาพและตรวจจับพื้นที่น้ำท่วมด้วยปัญญาประดิษฐ์
    </div>
</div>
""", unsafe_allow_html=True)

# =========================
# INTRODUCTION
# =========================
st.markdown("## 🌧️ วิเคราะห์ภาพน้ำท่วม")
st.markdown(
    "อัปโหลดภาพที่ต้องการตรวจสอบ แล้วให้ AI ช่วยระบุพื้นที่น้ำท่วม"
)

# =========================
# IMAGE UPLOAD
# =========================
uploaded_file = st.file_uploader(
    "📁 เลือกภาพที่ต้องการวิเคราะห์",
    type=["jpg", "jpeg", "png"],
    help="รองรับไฟล์ JPG, JPEG และ PNG",
)

# =========================
# ANALYZE IMAGE
# =========================
if uploaded_file is not None:
    try:
        image_bytes = uploaded_file.getvalue()
        original_image = Image.open(
            BytesIO(image_bytes)
        ).convert("RGB")

        st.markdown("### 🖼️ ภาพที่อัปโหลด")

        st.image(
            original_image,
            caption="ภาพต้นฉบับ",
            use_container_width=True,
        )

        if st.button(
            "✨ วิเคราะห์พื้นที่น้ำท่วม",
            use_container_width=True,
        ):
            with st.spinner(
                "กำลังวิเคราะห์ภาพ กรุณารอสักครู่..."
            ):
                response = requests.post(
                    API_URL,
                    files={
                        "file": (
                            uploaded_file.name,
                            image_bytes,
                            uploaded_file.type
                            or "application/octet-stream",
                        )
                    },
                    timeout=180,
                )

            if response.ok:
                result = response.json()

                # Read result from API
                flood_percent = float(
                    result.get("flood_percent", 0)
                )
                summary = result.get(
                    "summary",
                    "วิเคราะห์ภาพเสร็จเรียบร้อย",
                )

                # Decode predicted mask
                mask_data = result.get("mask")

                if not mask_data:
                    st.error(
                        "Backend ไม่ได้ส่งข้อมูล Mask กลับมา "
                        "โปรดตรวจสอบชื่อฟิลด์ใน API"
                    )
                    st.stop()

                # Support both raw base64 and data URL
                if "," in mask_data:
                    mask_data = mask_data.split(",", 1)[1]

                mask_bytes = base64.b64decode(mask_data)
                mask_image = Image.open(
                    BytesIO(mask_bytes)
                ).convert("RGB")

                st.markdown("---")
                st.markdown("## 📊 ผลการวิเคราะห์")

                col1, col2 = st.columns(2)

                with col1:
                    st.markdown("### ภาพต้นฉบับ")
                    st.image(
                        original_image,
                        use_container_width=True,
                    )

                with col2:
                    st.markdown("### พื้นที่น้ำท่วมที่ AI ตรวจพบ")
                    st.image(
                        mask_image,
                        use_container_width=True,
                    )

                st.markdown("### 💧 สรุปผล")

                metric_col1, metric_col2 = st.columns(2)

                with metric_col1:
                    st.metric(
                        "พื้นที่น้ำท่วมที่ตรวจพบ",
                        f"{flood_percent:.2f}%",
                    )

                with metric_col2:
                    st.metric(
                        "ขนาดภาพที่อัปโหลด",
                        f"{original_image.width} × "
                        f"{original_image.height}",
                    )

                st.info(summary)

                st.caption(
                    "หมายเหตุ: ผลลัพธ์เป็นการประมาณจากโมเดล AI "
                    "ควรตรวจสอบกับภาพจริงก่อนนำไปใช้ตัดสินใจ"
                )

            else:
                st.error(
                    f"ไม่สามารถวิเคราะห์ภาพได้ "
                    f"(HTTP {response.status_code})"
                )
                with st.expander("รายละเอียดข้อผิดพลาด"):
                    st.code(response.text[:2000])

    except requests.exceptions.Timeout:
        st.error(
            "การวิเคราะห์ใช้เวลานานเกินไป "
            "กรุณาลองใหม่อีกครั้ง"
        )

    except requests.exceptions.RequestException as e:
        st.error(
            "เชื่อมต่อ Backend ไม่สำเร็จ "
            "กรุณาตรวจสอบสถานะ API"
        )
        st.caption(str(e))

    except Exception as e:
        st.error("เกิดข้อผิดพลาดขณะอ่านภาพหรือแสดงผล")
        st.caption(str(e))

else:
    st.markdown("""
    <div class="card">
        <h3>✨ เริ่มต้นใช้งาน</h3>
        <p>
            1. เลือกภาพน้ำท่วมหรือภาพพื้นที่ที่ต้องการตรวจสอบ
            <br>
            2. กดปุ่มวิเคราะห์พื้นที่น้ำท่วม
            <br>
            3. ตรวจสอบ Mask และเปอร์เซ็นต์พื้นที่น้ำท่วม
        </p>
    </div>
    """, unsafe_allow_html=True)

# =========================
# FOOTER
# =========================
st.markdown("---")
st.markdown(
    "<p style='text-align:center; color:#8B7BA5;'>"
    "FloodVision AI · Flood Image Segmentation"
    "</p>",
    unsafe_allow_html=True,
)
