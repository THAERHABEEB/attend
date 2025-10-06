import streamlit as st
import pandas as pd
import os
from datetime import datetime
from PIL import Image
import time

# ========================= إعداد الصفحة =========================
st.set_page_config(page_title="نظام الحضور بالوجه", page_icon="📸", layout="wide")

# ========================= تنسيق CSS + أنيميشن =========================
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    color: white;
    font-family: 'Cairo', sans-serif;
}

/* القائمة الجانبية */
[data-testid="stSidebar"] {
    background: linear-gradient(135deg, #141E30, #243B55);
    color: white;
    padding-top: 1rem;
    border-right: 2px solid rgba(255,255,255,0.1);
    transition: all 0.3s ease-in-out;
}

/* عنوان القائمة */
[data-testid="stSidebar"]::before {
    content: '📊 FACE ATTENDANCE';
    display: block;
    font-weight: 700;
    font-size: 20px;
    color: #00e5ff;
    text-align: center;
    margin-bottom: 1rem;
    animation: fadeIn 2s ease-in-out;
}

/* تأثير hover */
.stRadio > div {
    transition: 0.3s ease;
}
.stRadio > div:hover {
    transform: scale(1.05);
    color: #00e5ff;
}

/* أنيميشن Fade-in */
@keyframes fadeIn {
    from {opacity: 0; transform: translateY(-10px);}
    to {opacity: 1; transform: translateY(0);}
}

/* أنيميشن الدائرة */
@keyframes pulse {
    0% {box-shadow: 0 0 0 0 rgba(0,229,255, 0.6);}
    50% {box-shadow: 0 0 0 25px rgba(0,229,255, 0);}
    100% {box-shadow: 0 0 0 0 rgba(0,229,255, 0);}
}
.circle {
    width: 160px;
    height: 160px;
    border-radius: 50%;
    background: radial-gradient(circle at 30% 30%, #00e5ff, #007acc);
    display: flex;
    align-items: center;
    justify-content: center;
    margin: auto;
    animation: pulse 2.5s infinite;
    color: white;
    font-size: 22px;
    font-weight: bold;
    text-shadow: 1px 1px 10px rgba(0,0,0,0.4);
}

/* قسم التواصل */
.contact-box {
    position: absolute;
    bottom: 30px;
    width: 90%;
    text-align: center;
    border-top: 1px solid rgba(255,255,255,0.2);
    padding-top: 10px;
    animation: fadeIn 2s ease-in-out;
}
.contact-box h4 {
    color: #00e5ff;
    font-size: 16px;
    margin-bottom: 4px;
}
.contact-box p {
    margin: 0;
    font-size: 15px;
    color: #ffffff;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

# ========================= القائمة الجانبية =========================
menu = st.sidebar.radio("القائمة", ["🧑‍🎓 الطالب", "🧑‍🏫 الدكتور"])

# قسم التواصل أسفل القائمة
st.sidebar.markdown("""
<div class="contact-box">
    <h4>👨‍💻 Eng. Thaer Habeeb</h4>
    <p>📞 01121412387</p>
</div>
""", unsafe_allow_html=True)

# ========================= صفحة الطالب =========================
if menu == "🧑‍🎓 الطالب":
    st.title("📸 نظام تسجيل الحضور بالوجه - الطالب")
    st.markdown("### مرحبًا! تأكد أن الكاميرا تعمل ثم التقط صورتك لتسجيل حضورك.")
    
    # دائرة أنيميشن
    st.markdown('<div class="circle">SCAN</div>', unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("📷 ارفع صورتك هنا", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="الصورة المرفوعة", use_container_width=True)
        st.success("✅ تم رفع الصورة بنجاح!")
        time.sleep(1)
        st.info("جارٍ التحقق من الصورة ...")
        time.sleep(2)
        st.success("تم تسجيل حضورك بنجاح ✅")

# ========================= صفحة الدكتور =========================
elif menu == "🧑‍🏫 الدكتور":
    st.title("🧑‍🏫 لوحة تحكم الدكتور")
    password = st.text_input("🔑 أدخل كلمة المرور:", type="password")
    
    if password == "admin123":
        st.success("تم تسجيل الدخول بنجاح ✅")

        st.markdown("### 🔍 نظرة عامة على الحضور")
        if os.path.exists("attendance.xlsx"):
            df = pd.read_excel("attendance.xlsx")
            total = len(df)
            today = datetime.now().strftime("%Y-%m-%d")
            today_attendance = df[df['Date'] == today]
            today_count = len(today_attendance)

            col1, col2, col3 = st.columns(3)
            col1.metric("إجمالي السجلات", total)
            col2.metric("حضور اليوم", today_count)
            if total:
                col3.metric("نسبة الحضور اليوم", f"{(today_count / total * 100):.1f}%")
            else:
                col3.metric("نسبة الحضور اليوم", "0%")

            st.markdown("### 🧾 بيانات الحضور")
            st.dataframe(df, use_container_width=True)
        else:
            st.warning("⚠️ لا يوجد ملف حضور بعد.")
    elif password:
        st.error("❌ كلمة مرور غير صحيحة")
      
