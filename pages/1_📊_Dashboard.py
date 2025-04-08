import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.title("📊 Dashboard - สรุปรายงานค่าส่งพัสดุ")

# โหลดข้อมูล
if os.path.exists("postal_data.json"):
    df = pd.read_json("postal_data.json")

    # สรุปยอดรวมรายจังหวัด
    province_sum = df.groupby("province")["price"].sum().reset_index().sort_values(by="price", ascending=False)

    # สรุปยอดรวมรายขนส่ง
    carrier_sum = df.groupby("carrier")["price"].sum().reset_index()

    # แสดงกราฟ
    st.subheader("📦 ยอดรวมค่าส่งแต่ละจังหวัด")
    fig1 = px.bar(province_sum, x="province", y="price", title="ค่าส่งรวมต่อจังหวัด", labels={"price": "บาท", "province": "จังหวัด"})
    st.plotly_chart(fig1, use_container_width=True)

    st.subheader("🚚 ยอดรวมค่าส่งตามขนส่ง")
    fig2 = px.pie(carrier_sum, names="carrier", values="price", title="ค่าส่งรวมแยกตามขนส่ง")
    st.plotly_chart(fig2, use_container_width=True)

    st.subheader("📅 รายการทั้งหมด (ล่าสุด)")
    st.dataframe(df[::-1])  # แสดงรายการล่าสุดก่อน

else:
    st.warning("ยังไม่มีข้อมูลในระบบ กรุณากรอกพัสดุก่อนจากหน้าแรก")
