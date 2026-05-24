import streamlit as st
import pandas as pd
from navigation import render_navigation
from filters import render_and_load_data
from bd import get_all_sections_with_room_count
from io import BytesIO

render_and_load_data()
st.header("📊 Загрузка номеров по секциям (свободно / занято)")

if st.session_state.get("df_fund") is None:
    st.warning("Сначала примените фильтры на главной странице.")
    st.stop()

df_fund = st.session_state.df_fund
if df_fund.empty:
    st.warning("Нет данных за выбранный период.")
    render_navigation('fullsvodka')
    st.stop()

date_from = st.session_state.date_from
date_to = st.session_state.date_to
if date_from == date_to:
    period_str = date_from.strftime('%d.%m.%Y')
else:
    period_str = f"{date_from.strftime('%d.%m.%Y')} - {date_to.strftime('%d.%m.%Y')}"
st.markdown(f"**Период:** {period_str}")

df_total = get_all_sections_with_room_count()

df_fund_paid = df_fund[df_fund['paid'] > 0]
if not df_fund_paid.empty:
    df_occupied = df_fund_paid.groupby('section_name')['room_id'].nunique().reset_index(name='occupied')
else:
    df_occupied = pd.DataFrame(columns=['section_name', 'occupied'])

df_result = df_total.merge(df_occupied, on='section_name', how='left').fillna(0)
df_result['free'] = df_result['total_rooms'] - df_result['occupied']
df_result = df_result.rename(columns={
    'section_name': 'Улица',
    'total_rooms': 'Всего комнат',
    'occupied': 'Занято (оплачено)',
    'free': 'Свободно'
})

df_result.insert(0, 'Дата', date_from.strftime('%d.%m.%Y') if date_from == date_to else period_str)
df_result = df_result[['Дата', 'Улица', 'Всего комнат', 'Свободно', 'Занято (оплачено)']]

st.dataframe(df_result, use_container_width=True, hide_index=True)

with st.expander("📥 Экспорт сводки"):
    csv_data = df_result.to_csv(index=False).encode('utf-8')
    st.download_button("Скачать как CSV", csv_data, "occupancy_report.csv", "text/csv")
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df_result.to_excel(writer, index=False, sheet_name='Occupancy')
    st.download_button("Скачать как Excel", output.getvalue(), "occupancy_report.xlsx")


total_rooms_all = df_result['Всего комнат'].sum()
total_occupied_all = df_result['Занято (оплачено)'].sum()
if total_rooms_all > 0:
    st.metric("Общая загрузка парка", f"{(total_occupied_all/total_rooms_all*100):.1f}%")
else:
    st.metric("Общая загрузка парка", "Нет данных")

render_navigation('fullsvodka')

