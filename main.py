import streamlit as st
from filters import render_and_load_data
from navigation import render_navigation

with open("assets/style.css", "r", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.set_page_config(page_title="Аналитика Эко-парк Адмирал", layout="wide")
st.markdown('<h1 class="main-header">Эко-парк "Адмирал"</h1>', unsafe_allow_html=True)

render_and_load_data()

#st.write("Пока пусто")

if st.session_state.get("df_fund") is not None:
    st.success(f"Данные загружены! Размещение: {len(st.session_state.df_fund)} записей, Услуги: {len(st.session_state.df_services)} записей")
    render_navigation('main')
else:
    st.info("Выберите фильтры в боковой панели и нажмите «Применить фильтры».")

