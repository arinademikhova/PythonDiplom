import streamlit as st
import pandas as pd
from filters import render_and_load_data
from bd import get_all_sections_with_room_count
from io import BytesIO

render_and_load_data(current_page="fullsvodka")
st.header("Аналитика по секциям")

if st.session_state.get("df_fund") is None:
    st.warning("Сначала примените фильтры на главной странице.")
    st.stop()

df_fund = st.session_state.df_fund
df_services = st.session_state.df_services

if df_fund.empty:
    st.warning("Нет данных за выбранный период.")
    st.stop()

date_from = st.session_state.date_from
date_to = st.session_state.date_to

if date_from == date_to:
    period_str = date_from.strftime('%d.%m.%Y')
    st.markdown(f"**Период:** {period_str} (один день)")

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
    df_result.insert(0, 'Дата', period_str)
    df_result = df_result[['Дата', 'Улица', 'Всего комнат', 'Свободно', 'Занято (оплачено)']]

    st.subheader("Загрузка номеров по секциям (свободно / занято)")
    st.dataframe(df_result, use_container_width=True, hide_index=True)

else:
    period_str = f"{date_from.strftime('%d.%m.%Y')} - {date_to.strftime('%d.%m.%Y')}"
    st.markdown(f"**Период:** {period_str} (несколько дней)")

    df_fund_paid = df_fund[df_fund['paid'] > 0]
    if not df_fund_paid.empty:
        paid_counts = df_fund_paid.groupby('section_name').size().reset_index(name='paid_bookings')
    else:
        paid_counts = pd.DataFrame(columns=['section_name', 'paid_bookings'])

    df_fund_unpaid = df_fund[df_fund['paid'] == 0]
    if not df_fund_unpaid.empty:
        unpaid_counts = df_fund_unpaid.groupby('section_name').size().reset_index(name='unpaid_bookings')
    else:
        unpaid_counts = pd.DataFrame(columns=['section_name', 'unpaid_bookings'])

    all_sections = get_all_sections_with_room_count()[['section_name']]
    df_result = all_sections.merge(paid_counts, on='section_name', how='left').fillna(0)
    df_result = df_result.merge(unpaid_counts, on='section_name', how='left').fillna(0)

    df_result = df_result.rename(columns={
        'section_name': 'Улица',
        'paid_bookings': 'Оплаченные брони',
        'unpaid_bookings': 'Не оплаченные брони'
    })
    df_result = df_result[['Улица', 'Оплаченные брони', 'Не оплаченные брони']]

    st.subheader("Количество броней по секциям (оплаченные / неоплаченные брони)")
    st.dataframe(df_result, use_container_width=True, hide_index=True)

with st.expander("Экспорт данных"):
    csv_data = df_result.to_csv(index=False).encode('utf-8')
    st.download_button("Скачать CSV", csv_data, "sections_report.csv", "text/csv")
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df_result.to_excel(writer, index=False, sheet_name='Sections')
    st.download_button("Скачать Excel", output.getvalue(), "sections_report.xlsx")

st.divider()

st.subheader("Использование услуг (оплаченные / неоплаченные брони)")
df_services_paid = df_services[df_services['paid'] > 0]
df_services_unpaid = df_services[df_services['paid'] == 0]

paid_services = df_services_paid.groupby('service_type_name').size().reset_index(name='paid_bookings') if not df_services_paid.empty else pd.DataFrame(columns=['service_type_name', 'paid_bookings'])
unpaid_services = df_services_unpaid.groupby('service_type_name').size().reset_index(name='unpaid_bookings') if not df_services_unpaid.empty else pd.DataFrame(columns=['service_type_name', 'unpaid_bookings'])

all_service_types = pd.DataFrame({'service_type_name': df_services['service_type_name'].unique()})
df_result_services = all_service_types.merge(paid_services, on='service_type_name', how='left').fillna(0)
df_result_services = df_result_services.merge(unpaid_services, on='service_type_name', how='left').fillna(0)
df_result_services = df_result_services.rename(columns={
    'service_type_name': 'Тип услуги',
    'paid_bookings': 'Оплаченные брони',
    'unpaid_bookings': 'Не оплаченные брони'
})
df_result_services = df_result_services[['Тип услуги', 'Оплаченные брони', 'Не оплаченные брони']]

st.dataframe(df_result_services, use_container_width=True, hide_index=True)

with st.expander("Экспорт данных по услугам"):
    csv_services = df_result_services.to_csv(index=False).encode('utf-8')
    st.download_button("Скачать CSV (услуги)", csv_services, "services_report.csv", "text/csv")
    output_services = BytesIO()
    with pd.ExcelWriter(output_services, engine='openpyxl') as writer:
        df_result_services.to_excel(writer, index=False, sheet_name='Services')
    st.download_button("Скачать Excel (услуги)", output_services.getvalue(), "services_report.xlsx")


