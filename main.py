import streamlit as st
from filters import render_and_load_data

st.set_page_config(page_title="Аналитика Эко-парк Адмирал", layout="wide")
st.markdown('<h1 class="main-header">🏕 Эко-парк "Адмирал"</h1>', unsafe_allow_html=True)

render_and_load_data()

#st.write("Пока пусто")

if st.session_state.get("df_fund") is not None:
    st.success(f"Данные загружены! Размещение: {len(st.session_state.df_fund)} записей, Услуги: {len(st.session_state.df_services)} записей")
else:
    st.info("Выберите фильтры в боковой панели и нажмите «Применить фильтры».")

