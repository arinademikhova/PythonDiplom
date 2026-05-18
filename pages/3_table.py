import streamlit as st
import pandas as pd

st.header("📋 Детальный отчёт по бронированиям")

if st.session_state.get("df_fund") is None or st.session_state.get("df_services") is None:
    st.warning("Сначала примените фильтры на главной странице.")
    st.stop()

df_fund = st.session_state.df_fund
df_services = st.session_state.df_services

if df_fund.empty and df_services.empty:
    st.warning("Нет данных за выбранный период.")
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