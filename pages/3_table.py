import streamlit as st
import pandas as pd
from io import BytesIO
from navigation import render_navigation
from filters import render_and_load_data

render_and_load_data()

st.header("📋 Детальный отчёт по бронированиям")

if st.session_state.get("df_fund") is None or st.session_state.get("df_services") is None:
    st.warning("Сначала примените фильтры на главной странице.")
    st.stop()

df_fund = st.session_state.df_fund
df_services = st.session_state.df_services

if df_fund.empty and df_services.empty:
    st.warning("Нет данных за выбранный период.")
    render_navigation('table')
    st.stop()

df_all = pd.concat([df_fund, df_services], ignore_index=True)

df_all = df_all.sort_values(by='reserv_date', ascending=True)

df_all['reserv_date_dt'] = pd.to_datetime(df_all['reserv_date'], unit='ms').dt.strftime('%d.%m.%Y')

def status_label(row):
    if row['paid'] >= row['realprice']:
        return "✅ Оплачено полностью"
    elif row['paid'] > 0:
        return "⚠️ Частичная оплата"
    else:
        return "❌ Не оплачено"

table_df = df_all[['reservation_id', 'reserv_date_dt', 'item_name', 'realprice', 'paid']].copy()
table_df['Статус оплаты'] = table_df.apply(status_label, axis=1)
table_df = table_df.rename(columns={
    'reservation_id': 'ID',
    'reserv_date_dt': 'Дата',
    'item_name': 'Объект/Услуга',
    'realprice': 'Стоимость (₽)',
    'paid': 'Оплачено (₽)'
})
final_columns = ['ID', 'Дата', 'Объект/Услуга', 'Стоимость (₽)', 'Оплачено (₽)', 'Статус оплаты']

st.dataframe(table_df[final_columns], use_container_width=True, height=400)

with st.expander("📥 Экспорт общей таблицы"):
    csv_data = table_df[final_columns].to_csv(index=False).encode('utf-8')
    st.download_button("Скачать как CSV", csv_data, "report.csv", "text/csv")

    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        table_df[final_columns].to_excel(writer, index=False, sheet_name='Report')
    st.download_button("Скачать как Excel", output.getvalue(), "report.xlsx")

st.divider()

if not df_fund.empty:
    st.subheader("🏠 Размещение (номера)")
    df_fund_all = df_fund.sort_values(by='reserv_date', ascending=True)
    df_fund_all['reserv_date_dt'] = pd.to_datetime(df_fund_all['reserv_date'] + 7 * 3600 * 1000, unit='ms').dt.strftime('%d.%m.%Y')

    fund_table = df_fund_all[['reservation_id', 'reserv_date_dt', 'item_name', 'realprice', 'paid']].copy()
    fund_table['Статус оплаты'] = fund_table.apply(status_label, axis=1)
    fund_table = fund_table.rename(columns={
        'reservation_id': 'ID',
        'reserv_date_dt': 'Дата',
        'item_name': 'Объект (номер)',
        'realprice': 'Стоимость (₽)',
        'paid': 'Оплачено (₽)'
    })
    fund_columns = ['ID', 'Дата', 'Объект (номер)', 'Стоимость (₽)', 'Оплачено (₽)', 'Статус оплаты']
    st.dataframe(fund_table[fund_columns], use_container_width=True, height=300)

    with st.expander("📥 Экспорт таблицы размещения"):
        csv_fund = fund_table[fund_columns].to_csv(index=False).encode('utf-8')
        st.download_button("Скачать CSV", csv_fund, "fund_report.csv", "text/csv")
        output_fund = BytesIO()
        with pd.ExcelWriter(output_fund, engine='openpyxl') as writer:
            fund_table[fund_columns].to_excel(writer, index=False, sheet_name='Fund')
        st.download_button("Скачать Excel", output_fund.getvalue(), "fund_report.xlsx")
else:
    st.info("Нет данных по размещению за выбранный период.")

st.divider()

if not df_services.empty:
    st.subheader("🎯 Услуги")
    df_services_all = df_services.sort_values(by='reserv_date', ascending=True)
    df_services_all['reserv_date_dt'] = pd.to_datetime(df_services_all['reserv_date'] + 7 * 3600 * 1000,unit='ms').dt.strftime('%d.%m.%Y')

    services_table = df_services_all[['reservation_id', 'reserv_date_dt', 'item_name', 'realprice', 'paid']].copy()
    services_table['Статус оплаты'] = services_table.apply(status_label, axis=1)
    services_table = services_table.rename(columns={
        'reservation_id': 'ID',
        'reserv_date_dt': 'Дата',
        'item_name': 'Услуга',
        'realprice': 'Стоимость (₽)',
        'paid': 'Оплачено (₽)'
    })
    services_columns = ['ID', 'Дата', 'Услуга', 'Стоимость (₽)', 'Оплачено (₽)', 'Статус оплаты']
    st.dataframe(services_table[services_columns], use_container_width=True, height=300)

    with st.expander("📥 Экспорт таблицы услуг"):
        csv_serv = services_table[services_columns].to_csv(index=False).encode('utf-8')
        st.download_button("Скачать CSV", csv_serv, "services_report.csv", "text/csv")
        output_serv = BytesIO()
        with pd.ExcelWriter(output_serv, engine='openpyxl') as writer:
            services_table[services_columns].to_excel(writer, index=False, sheet_name='Services')
        st.download_button("Скачать Excel", output_serv.getvalue(), "services_report.xlsx")
else:
    st.info("Нет данных по услугам за выбранный период.")

render_navigation('table')