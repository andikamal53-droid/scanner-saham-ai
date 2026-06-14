import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np

st.set_page_config(page_title="Super-App Pemindai Saham AI", page_icon="📈", layout="wide")

st.title("📈 Super-App Pemindai Saham AI")
st.write("Aplikasi pemindai saham otomatis Indonesia & Global menggunakan indikator teknikal.")

# Sistem melacak daftar saham secara dinamis berdasarkan input user
if 'daftar_saham_user' not in st.session_state:
    st.session_state['daftar_saham_user'] = ['BBCA.JK', 'BBRI.JK', 'AAPL', 'TSLA']

st.sidebar.header("Pengaturan Pemindai")

# Kotak input teks untuk mengetik saham baru secara bebas
saham_baru = st.sidebar.text_input("Tambah Kode Saham Baru (Contoh: ANTM.JK atau NVDA):", "").upper()

# Jika user mengetik kode baru, masukkan ke dalam daftar pilihan
if saham_baru and saham_baru not in st.session_state['daftar_saham_user']:
    st.session_state['daftar_saham_user'].append(saham_baru)

# Menampilkan daftar saham yang bisa dipilih/dihapus
pilihan_saham = st.sidebar.multiselect(
    "Saham yang akan dipindai:",
    options=st.session_state['daftar_saham_user'],
    default=st.session_state['daftar_saham_user']
)

tombol_pindai = st.sidebar.button("Mulai Pindai Saham")

def hitung_rsi(data, periode=14):
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=periode).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=periode).mean()
    rs = gain / (loss + 1e-10)
    return 100 - (100 / (1 + rs))

if tombol_pindai or pilihan_saham:
    hasil_scan = []
    
    for tickers in pilihan_saham:
        try:
            saham = yf.Ticker(tickers)
            hist = saham.history(period="3mo")
            if len(hist) < 15:
                continue
                
            harga_terakhir = hist['Close'].iloc[-1]
            hist['RSI'] = hitung_rsi(hist['Close'])
            rsi_terakhir = hist['RSI'].iloc[-1]
            
            if rsi_terakhir < 30:
                kondisi_rsi = "Oversold (Murah)"
            elif rsi_terakhir > 70:
                kondisi_rsi = "Overbought (Mahal)"
            else:
                kondisi_rsi = "Netral"
                
            hasil_scan.append({
                "Kode Saham": tickers,
                "Harga Terakhir": f"Rp {harga_terakhir:,.0f}" if ".JK" in tickers else f"${harga_terakhir:,.2f}",
                "RSI (14)": f"{rsi_terakhir:.2f}",
                "Kondisi_RSI": kondisi_rsi
            })
        except Exception as e:
            continue
            
    if hasil_scan:
        df_saham = pd.DataFrame(hasil_scan)
        tab1, tab2 = st.tabs(["📊 Pemindai Utama", "🔮 Target Harga Penutupan"])
        
        with tab1:
            st.subheader("Hasil Pemindaian Indikator Saham")
            st.dataframe(df_saham, use_container_width=True)
            
        with tab2:
            st.subheader("Analisis Target Harga Penutupan")
            st.write("Fitur target harga berbasis AI sedang memuat data historis...")
            st.dataframe(df_saham[["Kode Saham", "Harga Terakhir", "Kondisi_RSI"]], use_container_width=True)
    else:
        st.warning("Silakan ketuk tombol 'Mulai Pindai Saham' atau masukkan kode saham.")
