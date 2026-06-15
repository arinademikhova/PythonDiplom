import streamlit as st

def render_navigation(current_page):
    st.divider()
    st.subheader("Навигация")

    pages = {
        "Главная": "main.py",
        "Метрики": "pages/1_metrics.py",
        "Графики": "pages/2_plots.py",
        "Детальный отчёт": "pages/3_table.py",
        "Сводка загрузки": "pages/4_fullsvodka.py"
    }

    for name, path in pages.items():
        is_active = (
            (current_page == "main" and path == "main.py") or
            (current_page == "metrics" and path == "pages/1_metrics.py") or
            (current_page == "plots" and path == "pages/2_plots.py") or
            (current_page == "table" and path == "pages/3_table.py") or
            (current_page == "fullsvodka" and path == "pages/4_fullsvodka.py")
        )

        if is_active:
            if st.button(name, key=f"nav_{name}", use_container_width=True, type="primary"):
                st.switch_page(path)
        else:
            if st.button(name, key=f"nav_{name}", use_container_width=True):
                st.switch_page(path)