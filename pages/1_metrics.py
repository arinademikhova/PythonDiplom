import streamlit as st
import pandas as pd
from navigation import render_navigation
from filters import render_and_load_data
from bd import get_all_sections_with_room_count

render_and_load_data()

st.header("Ключевые показатели")

if st.session_state.get("df_fund") is None or st.session_state.get("df_services") is None:
    st.warning("Сначала примените фильтры на главной странице.")
    st.stop()

df_fund = st.session_state.df_fund
df_services = st.session_state.df_services

if df_fund.empty and df_services.empty:
    st.warning("Нет данных за выбранный период.")
    render_navigation('metrics')
    st.stop()

df_fund_paid = df_fund[df_fund['paid'] > 0]
df_services_paid = df_services[df_services['paid'] > 0]
df_all = pd.concat([df_fund, df_services], ignore_index=True)

#df_all['reserv_date_dt'] = pd.to_datetime(df_all['reserv_date'] + 7*3600*1000, unit='ms')

#колво всей выручки и гостей
total_revenue = df_all['paid'].sum()
total_guests = df_fund_paid['howadult'].sum() + df_fund_paid['howteenager'].sum() + df_fund_paid['howchild'].sum()

#загрузка парка
df_total = get_all_sections_with_room_count()
total_rooms = df_total['total_rooms'].sum()
if not df_fund_paid.empty:
    occupied_rooms = df_fund_paid['room_id'].nunique()
    occupancy = (occupied_rooms / total_rooms) * 100 if total_rooms > 0 else 0.0
else:
    occupancy = 0.0

#всего бронирований
total_bookings = len(df_all)

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

render_navigation('metrics')