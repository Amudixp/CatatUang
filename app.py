import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import pandas as pd
import os

st.title("Keuangan Online Bang Purba")

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)

# spreadsheet
sheet_name = os.getenv("SHEET_NAME")
sheet = client.open(sheet_name).sheet1

with st.form("keuangan_form"):
    tipe = st.selectbox("Tipe", ["Pemasukan", "Pengeluaran"])
    kategori = st.text_input("Kategori")
    nominal = st.number_input("Nominal", min_value=0.0)
    catatan = st.text_input("Catatan")
    tanggal = st.date_input("Tanggal", value=datetime.today())
    submitted = st.form_submit_button("Simpan")

if submitted:
    data = [str(tanggal), tipe, kategori, nominal, catatan]
    sheet.append_row(data)
    st.success("Data berhasil ditambahkan ke Google Sheets!")

data = sheet.get_all_records()
df = pd.DataFrame(data)
st.subheader("Data Terkini")
st.dataframe(df)


if not df.empty:
    print("Kolom-kolom:", df.columns.tolist())
    print(df.head())
    total_masuk = df[df["Tipe"] == "Pemasukan"]["Nominal"].sum()
    total_keluar = df[df["Tipe"] == "Pengeluaran"]["Nominal"].sum()
    saldo = total_masuk - total_keluar

    st.metric("Total Pemasukan", f"Rp {total_masuk:,.0f}")
    st.metric("Total Pengeluaran", f"Rp {total_keluar:,.0f}")
    st.metric("Saldo", f"Rp {saldo:,.0f}")
