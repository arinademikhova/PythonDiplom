import streamlit as st

st.header("📊 Метрики")

if st.session_state.get("df_fund") is not None:
    st.write(f"Загружено записей размещения: {len(st.session_state.df_fund)}")
    st.write(f"Загружено записей услуг: {len(st.session_state.df_services)}")
else:
    st.warning("Данные не загружены. Примените фильтры на главной странице.")