import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import io

# --- ١. ڕێکخستنی لاپەڕە ---
st.set_page_config(page_title="سیستەمی زانیاری وارسی شەهیدانی هەڵەبجە", page_icon="🏛️", layout="wide")

# بەستنەوە بە گوگڵ شیت (لینکەکەی خۆت لێرە دابنێ)
url = "https://docs.google.com/spreadsheets/d/14KuhfN0_hg_SLtG3s4ky6Zion3fcKE8aKG4gUBK7IEU/edit?usp=sharing"
conn = st.connection("gsheets", type=GSheetsConnection)

# خوێندنەوەی داتاکان
df = conn.read(spreadsheet=url).fillna("")

# --- ٢. ستایلی CSS بۆ دیزاین و پرێنت ---
st.markdown("""
    <style>
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] { 
        background-color: #f0f2f6; border-radius: 10px 10px 0 0; padding: 10px 20px;
    }
    .stTabs [aria-selected="true"] { background-color: #1a5d1a !important; color: white !important; }
    @media print {
        .no-print { display: none !important; }
        .stDataFrame { width: 100% !important; }
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #1a5d1a;'>🏛️ سیستەمی دیجیتاڵی بەڕێوەبەرایەتی گشتی کاروباری شەهیدان و ئەنفالکراوانی هەڵەبجە</h1>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["📝 تۆمارکردنی نوێ", "🔍 گەڕان و بەڕێوەبردن"])

# --- بەشی ١: تۆمارکردنی نوێ ---
with tab1:
    with st.form("add_form", clear_on_submit=True):
        st.subheader("تۆمارکردنی کەسی نوێ")
        col1, col2 = st.columns(2)
        with col1:
            id_num = st.text_input("🔢 زنجیرە")
            waris = st.text_input("👥 ناوی وارس")
            type_sh = st.selectbox("🎗️ جۆری شەهید", ["جینۆساید", "سەنگەر", "هاووڵاتی"])
            address = st.text_input("📍 شوێنی نیشتەجێبوون")
        with col2:
            name = st.text_input("👤 ناوی چواری شەهید")
            
            phone = st.text_input("📞 ژمارەی تەلەفۆن")
            finance = st.selectbox("💰 باری دارایی", ["باش", "ناوەند", "خراپ"])
            benefit = st.selectbox("🏡 سودمەندبووە؟", ["بەڵێ", "نەخێر"])
            
        if st.form_submit_button("📥 پاشەکەوتکردن"):
            if name and id_num:
                new_data = pd.DataFrame([{"ناوی چواری شەهید": name, "زنجیرە": id_num, "جۆری شەهید": type_sh, "شوێنی نیشتەجێبوون (گەڕەک)": address, "ناوی چواری وارس": waris, "ژمارەی تەلەفۆن": phone, "سودمەندبووە لە (زەوی یان خانوو)": benefit, "باری دارایی (باش، ناوەند، خراپ)": finance}])
                updated_df = pd.concat([df, new_data], ignore_index=True)
                conn.update(spreadsheet=url, data=updated_df)
                st.success("بە سەرکەوتوویی پاشەکەوت کرا")
                st.rerun()

# --- بەشی ٢: گەڕان و بەڕێوەبردن ---
with tab2:
    st.subheader("🔎 گەڕانی پێشکەوتوو")
    c1, c2 = st.columns(2)
    with c1:
        s_name = st.text_input("گەڕان بەپێی ناو")
    with c2:
        s_id = st.text_input("گەڕان بەپێی زنجیرە")
    
    # فلتەرکردن
    f_df = df.copy()
    if s_name: f_df = f_df[f_df['ناوی چواری شەهید'].str.contains(s_name)]
    if s_id: f_df = f_df[f_df['زنجیرە'].astype(str).str.contains(s_id)]
    
    st.dataframe(f_df, use_container_width=True)

    # دوگمەکانی هەناردەکردن و پرێنت
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        # دروستکردنی فایلی ئەکسڵ بۆ دابەزاندن
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            f_df.to_excel(writer, index=False, sheet_name='Sheet1')
        st.download_button(label="📥 هەناردەکردن بۆ Excel", data=output.getvalue(), file_name="martyrs_list.xlsx", mime="application/vnd.ms-excel")
    
    with col_btn2:
        st.info("💡 بۆ پرێنتکردنی لیستەکە، دوگمەی **Ctrl + P** دابگرە.")

    # --- دەستکاری و سڕینەوە ---
    st.divider()
    if not f_df.empty:
        st.subheader("🛠️ دەستکاری یان سڕینەوە")
        selected_person = st.selectbox("کەسێک هەڵبژێرە", f_df['ناوی چواری شەهید'].tolist())
        
        col_edit, col_del = st.columns(2)
        with col_del:
            if st.button("🗑️ سڕینەوەی یەکجاری"):
                df = df[df['ناوی چواری شەهید'] != selected_person]
                conn.update(spreadsheet=url, data=df)
                st.warning(f"ناوی {selected_person} سڕایەوە")
                st.rerun()
        
        with col_edit:
            st.write("بۆ دەستکاری: سەرەتا ناوەکە بسڕەوە و پاشان لە بەشی 'تۆمارکردن' بە ڕاستی زیادی بکەرەوە.")
