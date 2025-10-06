import streamlit as st
import pandas as pd
import os
from datetime import datetime
from PIL import Image

# إعداد الصفحة
st.set_page_config(
    page_title="نظام الحضور بالوجه",
    page_icon="📸",
    layout="centered",
    initial_sidebar_state="expanded"  # ✅ القائمة الجانبية مفتوحة دائمًا
)

# ===================== 🎨 تنسيق CSS + أنيميشن =====================
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
  font-size: 2.5rem;
  animation: glow 2s infinite alternate;
}
@keyframes glow {
  from { text-shadow: 0 0 10px #00e0ff, 0 0 20px #00e0ff; }
  to { text-shadow: 0 0 30px #00e0ff, 0 0 40px #00e0ff; }
}
.HITU {
  position: relative;
  color: #795548;
  bottom: 20px;
}
button {
  border-radius: 10px !important;
  transition: transform 0.3s ease, box-shadow 0.3s ease !important;
}
button:hover {
  transform: scale(1.05);
  box-shadow: 0 0 15px #00e0ff !important;
}
.pulse-animation {
  width: 130px;
  height: 130px;
  border-radius: 50%;
  margin: auto;
  border: 5px solid #00e0ff;
  animation: pulse 2s infinite;
}
@keyframes pulse {
  0% { transform: scale(0.9); box-shadow: 0 0 0 0 rgba(0,224,255, 0.7); }
  70% { transform: scale(1); box-shadow: 0 0 0 20px rgba(0,224,255, 0); }
  100% { transform: scale(0.9); box-shadow: 0 0 0 0 rgba(0,224,255, 0); }
}
@media (max-width: 600px) {
  .stButton button, .stTextInput, .stCameraInput {
    width: 100% !important;
  }
  .stDataFrame {
    font-size: 0.8rem;
  }
}
</style>
<h1 class="HITU">HITU<br>Data Science</h1>
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
page = st.sidebar.radio("اختر الصفحة:", ["🧑‍🎓 صفحة الطالب", "🧑‍🏫 لوحة الدكتور"])

# ===================== 👩‍🎓 صفحة الطالب =====================
if page == "🧑‍🎓 صفحة الطالب":
    st.markdown("<div class='pulse-animation'></div>", unsafe_allow_html=True)
    st.title("🎓 نظام تسجيل الحضور الذكي")
    st.markdown("---")

    name = st.text_input("👤 أدخل اسم الطالب:")
    camera_input = st.camera_input("📸 التقط صورة الطالب:")

    if st.button("✅ تسجيل الحضور"):
        if not name:
            st.warning("⚠️ من فضلك أدخل اسم الطالب أولاً.")
        elif camera_input is None:
            st.warning("📸 التقط صورة قبل التسجيل.")
        elif name in df["Name"].values:
            st.info(f"🟢 الاسم '{name}' موجود بالفعل في القائمة.")
        else:
            img_path = f"students/{name}.jpg"
            with open(img_path, "wb") as f:
                f.write(camera_input.getbuffer())

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

    with open(EXCEL_FILE, "rb") as file:
        btn = st.download_button(
            label="⬇️ تحميل ملف الحضور Excel",
            data=file,
            file_name="attendance.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

# ===================== 🧑‍🏫 لوحة الدكتور =====================
elif page == "🧑‍🏫 لوحة الدكتور":
    st.title("🧑‍🏫 لوحة تحكم الدكتور")
    st.markdown("---")

    if not os.path.exists(EXCEL_FILE) or os.path.getsize(EXCEL_FILE) == 0:
        st.warning("📂 لا توجد بيانات حالياً في ملف الحضور.")
    else:
        df = pd.read_excel(EXCEL_FILE)
        st.dataframe(df)

        # 🔍 البحث
        search_name = st.text_input("🔎 ابحث عن طالب بالاسم:")
        if search_name:
            results = df[df["Name"].str.contains(search_name, case=False, na=False)]
            if not results.empty:
                st.write("نتائج البحث:")
                st.dataframe(results)
            else:
                st.warning("❌ لم يتم العثور على الطالب المطلوب.")

        # 🗑️ حذف طالب
        delete_name = st.text_input("❌ اكتب اسم الطالب لحذفه من السجل:")
        if st.button("🗑️ حذف الطالب"):
            if delete_name in df["Name"].values:
                df = df[df["Name"] != delete_name]
                df.to_excel(EXCEL_FILE, index=False)
                st.success(f"تم حذف {delete_name} بنجاح ✅")
            else:
                st.error("⚠️ الاسم غير موجود.")

        st.markdown("---")
        # ⬇️ تحميل ملف الحضور
        with open(EXCEL_FILE, "rb") as file:
            st.download_button(
                label="⬇️ تحميل ملف Excel كامل",
                data=file,
                file_name="attendance.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
  )
          
