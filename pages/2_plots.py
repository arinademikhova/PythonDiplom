import streamlit as st

st.header("📈 Аналитические графики")

if st.session_state.get("df_fund") is not None:
    st.write(f"📊 Размещение: {len(st.session_state.df_fund)} записей")
    st.write(f"🎯 Услуги: {len(st.session_state.df_services)} записей")
else:
    st.warning("Данные не загружены. Примените фильтры на главной странице.")