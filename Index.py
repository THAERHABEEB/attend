import streamlit as st
import pandas as pd
import os
from datetime import datetime
from PIL import Image

# ===================== ⚙️ إعداد الصفحة =====================
st.set_page_config(
    page_title="نظام الحضور بالوجه",
    page_icon="📸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===================== 🎨 تنسيق واجهة المستخدم =====================
st.markdown("""
<style>
body {
  background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
  color: white;
  font-family: "Cairo", sans-serif;
}

/* ===== عناوين متحركة ===== */
h1, h2, h3 {
  text-align: center;
  color: #00e0ff;
  text-shadow: 0 0 15px rgba(0,224,255,0.7);
  animation: fadeSlide 2s ease-in-out;
}

@keyframes fadeSlide {
  from {opacity: 0; transform: translateY(-10px);}
  to {opacity: 1; transform: translateY(0);}
}

/* ===== أنيميشن الدائرة ===== */
.pulse-circle {
  width: 140px;
  height: 140px;
  border-radius: 50%;
  margin: 30px auto;
  background: radial-gradient(circle, #00e0ff, #007acc);
  box-shadow: 0 0 0 rgba(0, 224, 255, 0.4);
  animation: pulse 2s infinite;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 20px;
  font-weight: bold;
}

@keyframes pulse {
  0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(0,224,255,0.7);}
  70% { transform: scale(1); box-shadow: 0 0 0 25px rgba(0,224,255,0);}
  100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(0,224,255,0);}
}

/* ===== القائمة الجانبية ===== */
[data-testid="stSidebar"] {
  background: linear-gradient(160deg, #141E30, #243B55);
  color: white;
  border-right: 2px solid rgba(255,255,255,0.1);
  transition: all 0.3s ease;
}

[data-testid="stSidebar"] h2 {
  text-align: center;
  color: #00e5ff;
  font-size: 20px;
  animation: glowText 2s ease-in-out infinite alternate;
}

@keyframes glowText {
  from { text-shadow: 0 0 10px #00e5ff; }
  to { text-shadow: 0 0 30px #00e5ff; }
}

/* ===== للأجهزة المختلفة ===== */
@media (max-width: 600px) {
  .pulse-circle { width: 100px; height: 100px; font-size: 14px; }
  h1, h2, h3 { font-size: 1.3rem !important; }
}
</style>
""", unsafe_allow_html=True)

# ===================== ⚙️ تهيئة الملفات =====================
EXCEL_FILE = "attendance.xlsx"
if not os.path.exists(EXCEL_FILE):
    df = pd.DataFrame(columns=["Name", "Date", "Time"])
    df.to_excel(EXCEL_FILE, index=False)
else:
    df = pd.read_excel(EXCEL_FILE)

if not os.path.exists("students"):
    os.makedirs("students")

# ===================== 🧭 القائمة الجانبية =====================
st.sidebar.title("📋 نظام الحضور الذكي")
page = st.sidebar.radio("اختر الصفحة:", ["🧑‍🎓 صفحة الطالب", "🧑‍🏫 لوحة الدكتور"])

# ===================== 🧑‍🎓 صفحة الطالب =====================
if page == "🧑‍🎓 صفحة الطالب":
    st.markdown("<div class='pulse-circle'>SCAN</div>", unsafe_allow_html=True)
    st.title("🎓 نظام تسجيل الحضور بالوجه")
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
    st.subheader("📋 قائمة الحضور الحالية:")
    st.dataframe(df, use_container_width=True)

    with open(EXCEL_FILE, "rb") as file:
        st.download_button(
            label="⬇️ تحميل ملف Excel",
            data=file,
            file_name="attendance.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

# ===================== 🧑‍🏫 لوحة الدكتور =====================
elif page == "🧑‍🏫 لوحة الدكتور":
    st.title("🧑‍🏫 لوحة تحكم الدكتور")
    st.markdown("---")

    password = st.text_input("🔑 أدخل كلمة المرور:", type="password")

    if password == "admin123":
        st.success("✅ تم تسجيل الدخول بنجاح")

        df = pd.read_excel(EXCEL_FILE)
        st.markdown("### 📊 بيانات الحضور")
        st.dataframe(df, use_container_width=True)

        # 📆 ملخص الأرقام
        today = datetime.now().strftime("%Y-%m-%d")
        today_count = len(df[df["Date"] == today])
        total = len(df)
        percent = (today_count / total * 100) if total else 0

        col1, col2, col3 = st.columns(3)
        col1.metric("إجمالي الحضور", total)
        col2.metric("حضور اليوم", today_count)
        col3.metric("نسبة اليوم", f"{percent:.1f}%")

        # 🔍 البحث
        st.markdown("### 🔍 البحث عن طالب")
        search_name = st.text_input("ابحث بالاسم:")
        if search_name:
            results = df[df["Name"].str.contains(search_name, case=False, na=False)]
            if not results.empty:
                st.dataframe(results)
            else:
                st.warning("❌ لم يتم العثور على هذا الاسم.")

        # 🗑️ حذف
        st.markdown("### 🗑️ حذف طالب")
        delete_name = st.text_input("اكتب اسم الطالب لحذفه:")
        if st.button("حذف الطالب"):
            if delete_name in df["Name"].values:
                df = df[df["Name"] != delete_name]
                df.to_excel(EXCEL_FILE, index=False)
                st.success(f"تم حذف {delete_name} بنجاح ✅")
            else:
                st.error("⚠️ الاسم غير موجود.")
    elif password:
        st.error("❌ كلمة مرور غير صحيحة")
        
