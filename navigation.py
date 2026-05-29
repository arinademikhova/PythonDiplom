import streamlit as st

def render_navigation(current_page):
    st.divider()

    if current_page == 'main':
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            if st.button("Метрики"):
                st.switch_page("pages/1_metrics.py")
        with col2:
            if st.button("Графики"):
                st.switch_page("pages/2_plots.py")
        with col3:
            if st.button("Детальный отчёт"):
                st.switch_page("pages/3_table.py")
        with col4:
            if st.button("Сводка загрузки"):
                st.switch_page("pages/4_fullsvodka.py")

    elif current_page == 'metrics':
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            if st.button("Главная"):
                st.switch_page("main.py")
        with col2:
            if st.button("Графики"):
                st.switch_page("pages/2_plots.py")
        with col3:
            if st.button("Детальный отчёт"):
                st.switch_page("pages/3_table.py")
        with col4:
            if st.button("Сводка загрузки"):
                st.switch_page("pages/4_fullsvodka.py")

    elif current_page == 'plots':
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            if st.button("Главная"):
                st.switch_page("main.py")
        with col2:
            if st.button("Метрики"):
                st.switch_page("pages/1_metrics.py")
        with col3:
            if st.button("Детальный отчёт"):
                st.switch_page("pages/3_table.py")
        with col4:
            if st.button("Сводка загрузки"):
                st.switch_page("pages/4_fullsvodka.py")

    elif current_page == 'table':
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            if st.button("Главная"):
                st.switch_page("main.py")
        with col2:
            if st.button("Метрики"):
                st.switch_page("pages/1_metrics.py")
        with col3:
            if st.button("Графики"):
                st.switch_page("pages/2_plots.py")
        with col4:
            if st.button("Сводка загрузки"):
                st.switch_page("pages/4_fullsvodka.py")

    elif current_page == 'fullsvodka':
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            if st.button("Главная"):
                st.switch_page("main.py")
        with col2:
            if st.button("Метрики"):
                st.switch_page("pages/1_metrics.py")
        with col3:
            if st.button("Графики"):
                st.switch_page("pages/2_plots.py")
        with col4:
            if st.button("Детальный отчёт"):
                st.switch_page("pages/3_table.py")