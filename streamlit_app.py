
import streamlit as st
import requests
import base64
from io import BytesIO
from PIL import Image

# Backend API
API_URL = "https://floodvision-ai-2.onrender.com/predict"

# ตั้งค่าหน้าเว็บ
st.set_page_config(
    page_title="FloodVision AI",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# หัวข้อเว็บไซต์
st.title("🌊 FloodVision AI")
st.subheader("ระบบวิเคราะห์ภาพน้ำท่วมด้วย AI")
st.write("อัปโหลดภาพพื้นที่ที่ต้องการตรวจสอบ เพื่อให้ AI วิเคราะห์พื้นที่ที่อาจเป็นน้ำท่วม")

st.divider()

# อัปโหลดภาพ
st.header("📷 วิเคราะห์ภาพน้ำท่วม")

uploaded_file = st.file_uploader(
    "เลือกภาพพื้นที่ที่ต้องการวิเคราะห์",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")

    st.image(
        image,
        caption="ภาพต้นฉบับ",
        use_container_width=True
    )

    if st.button("🌊 เริ่มวิเคราะห์ภาพ", type="primary", use_container_width=True):
        try:
            with st.spinner("AI กำลังวิเคราะห์ภาพ กรุณารอสักครู่..."):
                response = requests.post(
                    API_URL,
                    files={
                        "file": (
                            uploaded_file.name,
                            uploaded_file.getvalue(),
                            uploaded_file.type or "image/jpeg"
                        )
                    },
                    timeout=180
                )

            if response.status_code == 200:
                result = response.json()

                st.success("วิเคราะห์ภาพเสร็จแล้ว")

                st.metric(
                    "สัดส่วนพิกเซลที่โมเดลทำนายว่าเป็นน้ำท่วม",
                    f"{result['flood_percent']:.2f}%"
                )

                mask_data = result["mask"].split(",", 1)[1]
                mask_bytes = base64.b64decode(mask_data)
                mask_image = Image.open(
                    BytesIO(mask_bytes)
                ).convert("L")

                st.subheader("🗺️ ผลการวิเคราะห์จาก AI")

                st.image(
                    mask_image,
                    caption="สีขาว = พื้นที่ที่โมเดลทำนายว่าเป็นน้ำท่วม",
                    use_container_width=True
                )

                st.info(result["summary"])

                st.caption(
                    "หมายเหตุ: ผลลัพธ์เป็นการทำนายจากโมเดล "
                    "เปอร์เซ็นต์เป็นสัดส่วนพิกเซล ไม่ใช่พื้นที่จริงทางภูมิศาสตร์"
                )

            else:
                st.error(f"วิเคราะห์ไม่สำเร็จ: HTTP {response.status_code}")
                st.write(response.text)

        except requests.exceptions.Timeout:
            st.error("ระบบใช้เวลานานเกินไป กรุณาลองใหม่อีกครั้ง")

        except requests.exceptions.RequestException as e:
            st.error("ไม่สามารถเชื่อมต่อระบบวิเคราะห์ได้")
            st.code(str(e))

        except Exception as e:
            st.error("เกิดข้อผิดพลาดระหว่างวิเคราะห์ภาพ")
            st.code(str(e))

st.divider()
st.caption("FloodVision AI | ระบบสนับสนุนการวิเคราะห์ภาพน้ำท่วมด้วย AI")
