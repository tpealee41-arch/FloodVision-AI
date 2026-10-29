import streamlit as st
import requests
import base64
from io import BytesIO
from PIL import Image

# URL ของ Backend API
API_URL = "https://floodvision-ai-2.onrender.com/predict"

# ตั้งค่าหน้าเว็บ
st.set_page_config(
    page_title="FloodVision AI",
    page_icon="🌊",
    layout="wide"
)

# หัวข้อหลัก
st.title("🌊 FloodVision AI")
st.subheader("ระบบวิเคราะห์และเฝ้าระวังน้ำท่วมด้วย AI")

st.write(
    "แพลตฟอร์มสำหรับวิเคราะห์ภาพและประเมินสถานการณ์น้ำท่วม"
)

st.info(
    "ระบบใช้ AI วิเคราะห์ภาพเพื่อคาดการณ์พื้นที่ที่อาจเป็นน้ำท่วม "
    "ผลลัพธ์เป็นการทำนายจากโมเดล ไม่ใช่การยืนยันสถานการณ์จริง"
)

# เมนูด้านข้าง
st.sidebar.header("เมนู")

page = st.sidebar.radio(
    "เลือกหน้าที่ต้องการ",
    ["หน้าหลัก", "วิเคราะห์ภาพน้ำท่วม", "เกี่ยวกับระบบ"]
)

# ==============================
# หน้าหลัก
# ==============================
if page == "หน้าหลัก":
    st.header("ภาพรวมระบบ")

    st.write(
        "ยินดีต้อนรับสู่ FloodVision AI "
        "ระบบวิเคราะห์ภาพพื้นที่น้ำท่วมด้วยปัญญาประดิษฐ์"
    )

    st.write("**ความสามารถของระบบ**")
    st.markdown(
        """
        - อัปโหลดภาพพื้นที่ที่ต้องการตรวจสอบ
        - ใช้โมเดล AI วิเคราะห์ภาพ
        - แสดงภาพ Mask ของพื้นที่ที่โมเดลทำนายว่าเป็นน้ำท่วม
        - แสดงสัดส่วนพิกเซลที่โมเดลทำนายว่าเป็นน้ำท่วม
        """
    )

# ==============================
# หน้าวิเคราะห์ภาพน้ำท่วม
# ==============================
elif page == "วิเคราะห์ภาพน้ำท่วม":
    st.header("🌊 วิเคราะห์ภาพน้ำท่วมด้วย AI")

    uploaded_file = st.file_uploader(
        "อัปโหลดภาพพื้นที่ที่ต้องการตรวจสอบ",
        type=["jpg", "jpeg", "png"]
    )

    if uploaded_file is not None:
        # แสดงภาพต้นฉบับ
        image = Image.open(uploaded_file).convert("RGB")

        st.image(
            image,
            caption="ภาพต้นฉบับ",
            use_container_width=True
        )

        # ปุ่มเริ่มวิเคราะห์
        if st.button("เริ่มวิเคราะห์ภาพ", type="primary"):
            try:
                with st.spinner(
                    "AI กำลังวิเคราะห์ภาพ กรุณารอสักครู่..."
                ):
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

                # ตรวจสอบผลลัพธ์จาก API
                if response.status_code == 200:
                    result = response.json()

                    st.success("วิเคราะห์ภาพเสร็จแล้ว!")

                    # แสดงเปอร์เซ็นต์
                    st.metric(
                        label="สัดส่วนพิกเซลที่โมเดลทำนายว่าเป็นน้ำท่วม",
                        value=f"{result['flood_percent']:.2f}%"
                    )

                    # แปลงภาพ Mask จาก Base64
                    mask_data = result["mask"].split(",", 1)[1]
                    mask_bytes = base64.b64decode(mask_data)

                    mask_image = Image.open(
                        BytesIO(mask_bytes)
                    ).convert("L")

                    # แสดงภาพ Mask
                    st.subheader("ผลการวิเคราะห์พื้นที่น้ำท่วม")

                    st.image(
                        mask_image,
                        caption=(
                            "สีขาว = พื้นที่ที่โมเดลทำนายว่าเป็นน้ำท่วม "
                            "| สีดำ = พื้นที่ที่โมเดลทำนายว่าไม่ใช่น้ำท่วม"
                        ),
                        use_container_width=True
                    )

                    # สรุปผล
                    st.subheader("สรุปผลการวิเคราะห์")
                    st.write(result["summary"])

                    st.caption(
                        "หมายเหตุ: เปอร์เซ็นต์นี้เป็นสัดส่วนพิกเซล "
                        "ไม่ใช่เปอร์เซ็นต์พื้นที่จริงทางภูมิศาสตร์ "
                        "ความแม่นยำขึ้นอยู่กับโมเดลและภาพที่นำเข้า"
                    )

                else:
                    st.error(
                        f"วิเคราะห์ไม่สำเร็จ "
                        f"(HTTP {response.status_code})"
                    )
                    st.code(response.text)

            except requests.exceptions.Timeout:
                st.error(
                    "ระบบใช้เวลาประมวลผลนานเกินไป "
                    "กรุณารอสักครู่แล้วลองใหม่"
                )

            except requests.exceptions.RequestException as e:
                st.error(
                    "ไม่สามารถเชื่อมต่อ Backend ได้ "
                    "กรุณาตรวจสอบว่าเซิร์ฟเวอร์ทำงานอยู่"
                )
                st.code(str(e))

            except Exception as e:
                st.error("เกิดข้อผิดพลาดระหว่างวิเคราะห์ภาพ")
                st.code(str(e))

# ==============================
# หน้าเกี่ยวกับระบบ
# ==============================
elif page == "เกี่ยวกับระบบ":
    st.header("เกี่ยวกับ FloodVision AI")

    st.write(
        "FloodVision AI เป็นระบบสนับสนุนการวิเคราะห์ภาพ "
        "เพื่อช่วยประเมินพื้นที่ที่อาจเกิดน้ำท่วมด้วย AI"
    )

    st.write("**เทคโนโลยีที่ใช้**")
    st.markdown(
        """
        - Streamlit สำหรับส่วนติดต่อผู้ใช้
        - FastAPI สำหรับ Backend API
        - TensorFlow / Keras สำหรับโมเดล AI
        - U-Net สำหรับการแบ่งส่วนภาพ
        """
    )

    st.write(
        "ผลการทำนายควรใช้ร่วมกับข้อมูลจากแหล่งที่เชื่อถือได้ "
        "ไม่ควรใช้แทนประกาศเตือนภัยอย่างเป็นทางการ"
    )
