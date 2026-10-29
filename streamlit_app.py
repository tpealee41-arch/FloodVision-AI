
import streamlit as st
from pathlib import Path

st.set_page_config(
    page_title="FloodVision AI",
    page_icon="🌊",
    layout="wide"
)

st.title("🌊 FloodVision AI")
st.subheader("ระบบวิเคราะห์และเฝ้าระวังน้ำท่วมด้วย AI")

st.write(
    "แพลตฟอร์มสำหรับวิเคราะห์ภาพและประเมินสถานการณ์น้ำท่วม"
)

st.info(
    "ระบบอยู่ระหว่างเชื่อมต่อโมเดล AI "
    "กรุณาใช้ผลจากโมเดลและข้อมูลที่ผ่านการตรวจสอบ"
)

st.sidebar.header("เมนู")
page = st.sidebar.radio(
    "เลือกหน้าที่ต้องการ",
    ["หน้าหลัก", "วิเคราะห์ภาพน้ำท่วม", "เกี่ยวกับระบบ"]
)

if page == "หน้าหลัก":
    st.header("ภาพรวมระบบ")
    st.write("ยินดีต้อนรับสู่ FloodVision AI")

elif page == "วิเคราะห์ภาพน้ำท่วม":
    st.header("วิเคราะห์ภาพ")
    uploaded_file = st.file_uploader(
        "อัปโหลดภาพพื้นที่ที่ต้องการตรวจสอบ",
        type=["jpg", "jpeg", "png"]
    )

    if uploaded_file:
        st.image(
            uploaded_file,
            caption="ภาพที่อัปโหลด",
            use_container_width=True
        )
        st.warning(
            "ภาพแสดงแล้ว แต่ยังไม่มีการทำนาย "
            "ต้องเชื่อมขั้นตอนประมวลผลจากโมเดลเดิมก่อน"
        )

elif page == "เกี่ยวกับระบบ":
    st.header("เกี่ยวกับ FloodVision AI")
    st.write(
        "ระบบสนับสนุนการวิเคราะห์สถานการณ์น้ำท่วมด้วย AI"
    )
