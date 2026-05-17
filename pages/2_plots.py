import streamlit as st
import plotly.express as px
import pandas as pd

st.header("📈 Аналитические графики")

if st.session_state.get("df_fund") is None or st.session_state.get("df_services") is None:
    st.warning("Данные не загружены. Примените фильтры на главной странице.")
    st.stop()

df_fund = st.session_state.df_fund
df_services = st.session_state.df_services

if df_fund.empty and df_services.empty:
    st.warning("Нет данных за выбранный период.")
    st.stop()

df_all = pd.concat([df_fund, df_services], ignore_index=True)

if not df_all.empty:
    df_all['reserv_date_dt'] = pd.to_datetime(df_all['reserv_date'], unit='ms')

st.subheader("📊 Выручка по секциям")
if not df_fund.empty:
    rev_by_section = df_fund.groupby('section_name')['realprice'].sum().reset_index()
    fig = px.pie(
        rev_by_section,
        values='realprice',
        names='section_name',
        hole=0.4,
        labels={'section_name': 'Секция', 'realprice': 'Выручка (₽)'},
        hover_data={'realprice': ':,.0f'}
    )
    fig.update_traces(
        hovertemplate='<b>%{label}</b><br>Выручка: %{value:,.0f} ₽<extra></extra>'
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Нет данных по размещению")

st.divider()

st.subheader("🛒 Использование услуг")
if not df_services.empty:
    usage = df_services.groupby('service_type_name').size().reset_index(name='count')
    fig = px.bar(
        usage,
        x='service_type_name',
        y='count',
        labels={'service_type_name': 'Тип услуги', 'count': 'Количество использований'},
        text_auto=True
    )
    fig.update_traces(
        hovertemplate='<b>%{x}</b><br>Использований: %{y}<extra></extra>'
    )
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Нет данных по услугам")

st.divider()

st.subheader("📈 Динамика посещаемости (уникальные бронирования в день)")
if not df_all.empty:
    daily = df_all.groupby('reserv_date_dt')['reservation_id'].nunique().reset_index(name='bookings')
    fig = px.line(
        daily,
        x='reserv_date_dt',
        y='bookings',
        markers=True,
        labels={'reserv_date_dt': 'Дата резерва', 'bookings': 'Количество бронирований'}
    )
    fig.update_traces(
        hovertemplate='<b>%{x|%d.%m.%Y}</b><br>Бронирований: %{y}<extra></extra>'
    )
    fig.update_layout(xaxis_tickformat='%d.%m.%Y')
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Нет данных для динамики")