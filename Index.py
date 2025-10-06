import streamlit as st
import pandas as pd
import os
from datetime import datetime
from PIL import Image

# ===================== ⚙️ إعداد الصفحة =====================
st.set_page_config(
    page_title="نظام الحضور الذكي",
    page_icon="🎓",
    layout="centered",
    initial_sidebar_state="expanded"
)

# ===================== 🎨 CSS + أنيميشن =====================
st.markdown("""
<style>
body {
  background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
  color: white;
  font-family: "Cairo", sans-serif;
}
h1 {
  text-align: center;
  color: #00e0ff;
  font-size: 2.3rem;
  animation: glow 2s infinite alternate;
}
h2, h3, h4 {
  color: #00e0ff;
  text-align: center;
}
@keyframes glow {
  from { text-shadow: 0 0 10px #00e0ff, 0 0 20px #00e0ff; }
  to { text-shadow: 0 0 25px #00e0ff, 0 0 40px #00e0ff; }
}

/* 🎨 تحسين شكل الأزرار */
button {
  border-radius: 10px !important;
  transition: transform 0.3s ease, box-shadow 0.3s ease !important;
}
button:hover {
  transform: scale(1.05);
  box-shadow: 0 0 15px #00e0ff !important;
}

/* 🌈 أنيميشن القائمة الجانبية */
[data-testid="stSidebar"] {
  background: linear-gradient(180deg, #203a43, #2c5364);
  animation: slideIn 1.2s ease;
  border-right: 2px solid #00e0ff;
}
@keyframes slideIn {
  from { transform: translateX(-100%); opacity: 0; }
  to { transform: translateX(0); opacity: 1; }
}

/* ⚙️ استجابة للأجهزة الصغيرة */
@media (max-width: 600px) {
  h1 { font-size: 1.8rem; }
  .stButton button, .stTextInput, .stCameraInput {
    width: 100% !important;
  }
}
</style>
<h1>HITU<br>Data Science</h1>
""", unsafe_allow_html=True)

# ===================== ⚙️ الإعداد =====================
EXCEL_FILE = "attendance.xlsx"
if not os.path.exists(EXCEL_FILE):
    df = pd.DataFrame(columns=["Name", "Date", "Time"])
    df.to_excel(EXCEL_FILE, index=False)
else:
    df = pd.read_excel(EXCEL_FILE)

if not os.path.exists("students"):
    os.makedirs("students")

# ===================== 🧭 القائمة الجانبية =====================
st.sidebar.title("📋 القائمة")
page = st.sidebar.radio("اختر الصفحة:", ["🎓 صفحة الطالب", "🧑‍🏫 لوحة الدكتور"])

# ===================== 👨‍🎓 صفحة الطالب =====================
if page == "🎓 صفحة الطالب":
    st.markdown("<h2>📸 نظام تسجيل الحضور الذكي</h2>", unsafe_allow_html=True)
    st.markdown("---")

    name = st.text_input("👤 أدخل اسم الطالب:")
    camera_input = st.camera_input("📷 التقط صورة الطالب:")

    if st.button("✅ تسجيل الحضور"):
        if not name:
            st.warning("⚠️ من فضلك أدخل اسم الطالب أولاً.")
        elif camera_input is None:
            st.warning("📸 التقط صورة قبل التسجيل.")
        elif name in df["Name"].values:
            st.info(f"🟢 الاسم '{name}' موجود بالفعل في القائمة.")
        else:
            # حفظ الصورة
            img_path = f"students/{name}.jpg"
            with open(img_path, "wb") as f:
                f.write(camera_input.getbuffer())

            # حفظ البيانات في Excel
            now = datetime.now()
            new_row = pd.DataFrame([[name, now.strftime("%Y-%m-%d"), now.strftime("%H:%M:%S")]],
                                   columns=["Name", "Date", "Time"])
            df = pd.concat([df, new_row], ignore_index=True)
            df.to_excel(EXCEL_FILE, index=False)

            st.success(f"✅ تم تسجيل {name} بنجاح.")
            st.image(img_path, caption=f"📸 صورة {name}", width=250)

    st.markdown("---")
    st.subheader("📋 قائمة الحضور:")
    st.dataframe(df)

# ===================== 👨‍🏫 لوحة الدكتور =====================
elif page == "🧑‍🏫 لوحة الدكتور":
    st.markdown("<h2>🧑‍🏫 لوحة تحكم الدكتور</h2>", unsafe_allow_html=True)
    st.markdown("---")

    # كلمة المرور فقط تظهر بعد اختيار الصفحة
    password = st.text_input("🔑 أدخل كلمة المرور:", type="password", placeholder="********")

    CORRECT_PASSWORD = "hitu123"  # يمكنك تغييرها

    if password:
        if password == CORRECT_PASSWORD:
            st.success("✅ تم تسجيل الدخول بنجاح!")
            st.markdown("---")

            st.markdown("<h3>📊 قائمة الحضور الكاملة</h3>", unsafe_allow_html=True)
            st.dataframe(df, use_container_width=True)

            st.markdown(f"<h4>📅 عدد الطلاب المسجلين: {len(df)}</h4>", unsafe_allow_html=True)

            # زر تحميل الملف
            with open(EXCEL_FILE, "rb") as file:
                st.download_button(
                    label="⬇️ تحميل ملف الحضور Excel",
                    data=file,
                    file_name="attendance.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

        else:
            st.error("❌ كلمة المرور غير صحيحة.")
    else:
        st.info("🟡 الرجاء إدخال كلمة المرور للدخول إلى لوحة التحكم.")
            
