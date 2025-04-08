import streamlit as st
from datetime import date
import json
import os
import pandas as pd

# -------------------- ฟังก์ชัน --------------------
def load_data():
    if os.path.exists("postal_data.json"):
        with open("postal_data.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_data(data):
    with open("postal_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_receiver_info(zipcode):
    return receiver_data.get(zipcode, {"province": "", "receiver": ""})


# -------------------- รายชื่อผู้รับ --------------------
receiver_data = {
    "10150": {"province": "กรุงเทพมหานคร", "receiver": "ประพิมพรรณ"},
    "20170": {"province": "ชลบุรี", "receiver": "ไพลิน"},
    "50140": {"province": "เชียงใหม่", "receiver": "ภัทรานิษฐ์"},
    "65000": {"province": "พิษณุโลก", "receiver": "จันทรา"},
    "18160": {"province": "สระบุรี", "receiver": "รุ่งอรุณ"},
    "41000": {"province": "อุดรธานี", "receiver": "ชลิดา"},
    "34190": {"province": "อุบลราชธานี", "receiver": "จิราภรณ์"},
    "30000": {"province": "นครราชสีมา", "receiver": "ปัทมาวดี"},
    "73000": {"province": "นครปฐม", "receiver": "อมรรัตน์"},
    "84000": {"province": "สุราษฏร์ธานี", "receiver": "ยุภาวดี"},
    "90110": {"province": "สงขลา", "receiver": "จารุวรรณ"},
}

# -------------------- ส่วนบน --------------------
st.title("📮 ระบบจัดการค่าส่งไปรษณีย์")
st.markdown("กรอกข้อมูลด้านล่าง และจัดการข้อมูลย้อนหลังได้")

data = load_data()

# -------------------- ฟอร์มกรอกข้อมูล --------------------
with st.expander("➕ เพิ่มรายการใหม่"):
    send_date = st.date_input("📅 วันที่ส่ง", value=date.today())
    carrier = st.selectbox("🚚 ขนส่ง", ["ThaiPost", "Kerry", "Flash", "J&T", "อื่น ๆ"])
    tracking_no = st.text_input("🔢 เลขพัสดุ")
    zipcode = st.selectbox("📮 รหัสไปรษณีย์", list(receiver_data.keys()))
    info = get_receiver_info(zipcode)
    st.text_input("🗺️ จังหวัด", value=info["province"], disabled=True)
    st.text_input("👤 ผู้รับ", value=info["receiver"], disabled=True)
    price = st.number_input("💰 ค่าส่ง", min_value=0.0, step=1.0)
    detail = st.text_area("📦 รายละเอียด")

    if st.button("✅ บันทึก"):
        entry = {
            "send_date": str(send_date),
            "carrier": carrier,
            "tracking_no": tracking_no,
            "zipcode": zipcode,
            "province": info["province"],
            "receiver": info["receiver"],
            "price": price,
            "detail": detail
        }
        data.append(entry)
        save_data(data)
        st.success("บันทึกเรียบร้อยแล้ว ✅")
        st.rerun()

# -------------------- ค้นหา --------------------
st.markdown("---")
search = st.text_input("🔍 ค้นหา (Tracking No. หรือ ชื่อผู้รับ)").lower()
filtered_data = [d for d in data if search in d["tracking_no"].lower() or search in d["receiver"].lower()]

# -------------------- แสดงรายการทั้งหมด --------------------
st.subheader("📋 รายการทั้งหมด")
if filtered_data:
    for i, d in enumerate(filtered_data[::-1]):
        st.write(f"**{i+1}. วันที่:** {d['send_date']} | ขนส่ง: {d['carrier']} | ค่าส่ง: {d['price']} บาท")
        st.caption(f"เลขพัสดุ: {d['tracking_no']} | รหัสไปรษณีย์: {d['zipcode']} | จังหวัด: {d['province']}")
        st.caption(f"ผู้รับ: {d['receiver']} | รายละเอียด: {d['detail']}")
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button(f"📝 แก้ไข", key=f"edit_{i}"):
                st.session_state["edit_index"] = len(data) - 1 - i
                st.rerun()
        with col2:
            if st.button(f"🗑️ ลบ", key=f"delete_{i}"):
                data.pop(len(data) - 1 - i)
                save_data(data)
                st.success("ลบรายการแล้ว ✅")
                st.rerun()
else:
    st.warning("ไม่พบข้อมูลที่ค้นหา")

# -------------------- แก้ไข --------------------
if "edit_index" in st.session_state:
    idx = st.session_state["edit_index"]
    edit_entry = data[idx]
    st.markdown("---")
    st.subheader("✏️ แก้ไขรายการ")
    new_send_date = st.date_input("📅 วันที่ส่ง", value=date.fromisoformat(edit_entry["send_date"]), key="edit_date")
    new_carrier = st.selectbox("🚚 ขนส่ง", ["ThaiPost", "Kerry", "Flash", "J&T", "อื่น ๆ"], index=["ThaiPost", "Kerry", "Flash", "J&T", "อื่น ๆ"].index(edit_entry["carrier"]), key="edit_carrier")
    new_tracking_no = st.text_input("🔢 เลขพัสดุ", value=edit_entry["tracking_no"], key="edit_tracking")
    new_zipcode = st.selectbox("📮 รหัสไปรษณีย์", list(receiver_data.keys()), index=list(receiver_data.keys()).index(edit_entry["zipcode"]), key="edit_zipcode")
    new_info = get_receiver_info(new_zipcode)
    st.text_input("🗺️ จังหวัด", value=new_info["province"], disabled=True, key="edit_province")
    st.text_input("👤 ผู้รับ", value=new_info["receiver"], disabled=True, key="edit_receiver")
    new_price = st.number_input("💰 ค่าส่ง", value=edit_entry["price"], min_value=0.0, step=1.0, key="edit_price")
    new_detail = st.text_area("📦 รายละเอียด", value=edit_entry["detail"], key="edit_detail")

    if st.button("💾 บันทึกการแก้ไข"):
        updated = {
            "send_date": str(new_send_date),
            "carrier": new_carrier,
            "tracking_no": new_tracking_no,
            "zipcode": new_zipcode,
            "province": new_info["province"],
            "receiver": new_info["receiver"],
            "price": new_price,
            "detail": new_detail
        }
        data[idx] = updated
        save_data(data)
        st.success("บันทึกการแก้ไขแล้ว ✅")
        del st.session_state["edit_index"]
        st.rerun()

# -------------------- Export Excel --------------------
if st.button("📤 ส่งออกเป็น Excel"):
    df = pd.DataFrame(data)
    df.to_excel("postal_data_export.xlsx", index=False)
    with open("postal_data_export.xlsx", "rb") as f:
        st.download_button("📁 ดาวน์โหลด Excel", f, file_name="postal_data_export.xlsx")

