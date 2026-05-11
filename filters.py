import streamlit as st
from datetime import datetime, timedelta
from config import DEFAULT_DAYS_BACK
from bd import get_list_hotels, get_list_sections, get_list_service_types


def render_and_load_data():
    #формируем вкладку фильтры
    if "filters_applied" not in st.session_state:
        st.session_state.filters_applied = False
        st.session_state.date_from = datetime.now() - timedelta(days=DEFAULT_DAYS_BACK)
        st.session_state.date_to = datetime.now()
        st.session_state.hotel = "Все"
        st.session_state.sections = []
        st.session_state.service_types = []

    with st.sidebar:
        st.header("🔍 Фильтры")

        date_from = st.date_input("Период бронирования (От)", st.session_state.date_from)
        date_to = st.date_input("До", st.session_state.date_to)

        hotels_list = ["Все"] + get_list_hotels()
        hotel = st.selectbox(
            "Отель", hotels_list,
            index=hotels_list.index(st.session_state.hotel) if st.session_state.hotel in hotels_list else 0
        )

        sections = st.multiselect("Секции парка", get_list_sections(), default=st.session_state.sections)
        service_types = st.multiselect("Типы услуг", get_list_service_types(), default=st.session_state.service_types)

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Применить фильтры", type="primary"):
                #сохраняем выбранные значения в session_state
                st.session_state.date_from = date_from
                st.session_state.date_to = date_to
                st.session_state.hotel = hotel
                st.session_state.sections = sections
                st.session_state.service_types = service_types
                st.session_state.filters_applied = True
                st.success("✅ Фильтры применены, но данные пока не загружаются (следующий шаг).")
                st.rerun()
        with col2:
            if st.button("Сбросить"):
                st.session_state.filters_applied = False
                st.session_state.date_from = datetime.now() - timedelta(days=DEFAULT_DAYS_BACK)
                st.session_state.date_to = datetime.now()
                st.session_state.hotel = "Все"
                st.session_state.sections = []
                st.session_state.service_types = []
                st.rerun()