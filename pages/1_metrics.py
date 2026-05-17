# pages/1_metrics.py
import streamlit as st
import pandas as pd
from bd import get_total_rooms_count

st.header("📊 Ключевые показатели")

if st.session_state.get("df_fund") is None or st.session_state.get("df_services") is None:
    st.warning("Сначала примените фильтры на главной странице.")
    st.stop()

df_fund = st.session_state.df_fund
df_services = st.session_state.df_services

if df_fund.empty and df_services.empty:
    st.warning("Нет данных за выбранный период.")
    st.stop()

df_all = pd.concat([df_fund, df_services], ignore_index=True)

#колво всей выручки и гостей
total_revenue = df_all['realprice'].sum()
total_guests = df_fund['howadult'].sum() + df_fund['howteenager'].sum() + df_fund['howchild'].sum()

#загрузка парка
if not df_fund.empty:
    occupied_rooms = df_fund['room_id'].nunique()
    total_rooms = get_total_rooms_count()
    occupancy = (occupied_rooms / total_rooms) * 100 if total_rooms else 0.0
else:
    occupancy = 0.0

#всего бронирований
total_bookings = len(df_all)

#фактические поступления
actual_payments = df_all['paid'].sum()

col1, col2 = st.columns(2)
with col1:
    st.metric("Общая выручка (₽)", f"{total_revenue:,.0f}")
with col2:
    st.metric("Количество гостей", f"{total_guests:,}")


col3, col4 = st.columns(2)
with col3:
    st.metric("Загрузка парка (%)", f"{occupancy:.1f}%")
with col4:
    st.metric("Всего бронирований", f"{total_bookings:,}")


#col5 = st.columns(1)
#with col5:
    #st.metric("Факт. поступления (₽)", f"{actual_payments:,.0f}")

st.metric("Факт. поступления (₽)", f"{actual_payments:,.0f}")