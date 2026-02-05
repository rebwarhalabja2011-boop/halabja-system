import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# --- ١. ڕێکخستنی لاپەڕە و ئایکۆنی ئەپەکە ---
st.set_page_config(
    page_title="سیستەمی شەهیدانی هەڵەبجە",
    page_icon="🏛️",
    layout="centered"
)

# --- ٢. ستایلی CSS بۆ جوانکردنی ڕووکارەکە ---
st.markdown("""
    <style>
    /* گۆڕینی ڕەنگی پشتێنە */
    .stApp {
        background-color: #f8f9fa;
    }
    
    /* ستایلی چوارچێوەی فۆرمەکە */
    div[data-testid="stForm"] {
        border: none;
        border-radius: 15px;
        padding: 40px;
        background-color: white;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
    }
    
    /* ستایلی دوگمەی پاشەکەوتکردن */
    .stButton>button {
        width: 100%;
        background-color: #1a5d1a;
        color: white;
        border-radius: 8px;
        height: 3.5em;
        font-weight: bold;
        font-size: 18px;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #2e7d32;
        border: none;
    }
    
    /* جوانکردنی تایتڵ */
    .main-title {
        color: #1a5d1a;
        text-align: center;
        font-family: 'Arial';
        font-weight: bold;
        border-bottom: 3px solid #1a5d1a;
        padding-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# لینکەکەت لێرە دابنێ
url = "لینکەکەی_خۆت_لێرە_دابنێ"

conn = st.connection("gsheets", type=GSheetsConnection)

# --- ٣. ڕووکاری سەرەوەی ئەپەکە ---
st.markdown("<h1 class='main-title'>🏛️ بەڕێوەبەرایەتی کاروباری شەهیدان</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #555;'>فۆرمی دیجیتاڵی تۆمارکردنی زانیاری وارسی شەهیدان - هەڵەبجە</p>", unsafe_allow_html=True)

# --- ٤. فۆرمی داخڵکردن لەگەڵ ئایکۆنەکان ---
with st.form("main_form", clear_on_submit=True):
    
    col1, col2 = st.columns(2)
    
    with col1:
        name = st.text_input("👤 ناوی چواری شەهید")
        id_num = st.text_input("🔢 زنجیرە")
        type_sh = st.selectbox("🎗️ جۆری شەهید", ["جینۆساید", "سەنگەر", "هاووڵاتی"])
        address = st.text_input("📍 شوێنی نیشتەجێبوون")
        waris_name = st.text_input("👥 ناوی چواری وارس")
        social_status = st.selectbox("💍 باری کۆمەڵایەتی", ["خێزاندار", "سەڵت"])
        family_count = st.text_input("👨‍👩‍👧‍👦 ژمارەی ئەندامانی خێزان")

    with col2:
        waris_count = st.text_input("📜 چەن وارسی هەیە")
        job = st.text_input("🛠️ پیشەی وارس")
        phone = st.text_input("📞 ژمارەی تەلەفۆن")
        benefit = st.selectbox("🏡 سودمەندبووە لە زەوی/خانوو؟", ["بەڵێ", "نەخێر"])
        prop_type = st.selectbox("🔑 جۆری مۆڵک", ["مۆڵک", "کرێ", "نییە"])
        finance = st.selectbox("💰 باری دارایی", ["باش", "ناوەند", "خراپ"])
        illness = st.selectbox("🏥 نەخۆشی درێژخایەن؟", ["بەڵێ", "نەخێر"])
        disability = st.selectbox("♿ خاوەن پێداویستی تایبەت؟", ["بەڵێ", "نەخێر"])

    st.markdown("<br>", unsafe_allow_html=True)
    submitted = st.form_submit_button("📥 ناردن و پاشەکەوتکردن")

    if submitted:
        if name and id_num:
            # ئامادەکردنی داتا
            new_entry = pd.DataFrame([{
                "ناوی چواری شەهید": name, "زنجیرە": id_num, "جۆری شەهید": type_sh,
                "شوێنی نیشتەجێبوون (گەڕەک)": address, "ناوی چواری وارس": waris_name,
                "باری کۆمەڵایەتی": social_status, "ژمارەی ئەندامانی خێزان": family_count,
                "چەن وارسی هەیە": waris_count, "پیشەی وارس": job, "ژمارەی تەلەفۆن": phone,
                "سودمەندبووە لە (زەوی یان خانوو)": benefit, "جۆری مۆڵک (مۆڵک یان کرێ)": prop_type,
                "باری دارایی (باش، ناوەند، خراپ)": finance,
                "نەخۆشی درێژخایەن لە خێزانەکەیدا هەیە (بەڵێ یان نەخێر)": illness,
                "ئایا خاوەن پێداویستی تایبەت هەیە (بەڵێ یان نەخێر )": disability
            }])
            
            # ناردن بۆ گوگڵ شیت
            df = conn.read(spreadsheet=url)
            updated_df = pd.concat([df, new_entry], ignore_index=True)
            conn.update(spreadsheet=url, data=updated_df)
            
            st.balloons()
            st.success("زانیارییەکان بە سەرکەوتوویی نێردران بۆ بنکەی زانیاری!")
        else:
            st.error("تکایە خانە سەرەکییەکان (ناو و زنجیرە) پڕ بکەرەوە!")
