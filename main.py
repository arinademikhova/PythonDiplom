import streamlit as st
from filters import render_and_load_data

st.set_page_config(page_title="Аналитика Эко-парк Адмирал", layout="wide")
st.markdown('<h1 class="main-header">🏕 Эко-парк "Адмирал"</h1>', unsafe_allow_html=True)

render_and_load_data()

#st.write("Пока пусто")

st.info("Выберите фильтры в боковой панели и нажмите «Применить фильтры».")