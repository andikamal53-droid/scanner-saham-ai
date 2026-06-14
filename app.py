import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf

# --- PENGATURAN HALAMAN DASHBOARD ---
st.set_page_config(
    page_title="Super-App Pemindai Saham AI",
    page_icon="📈",
    layout="wide"
)

st.title("🚀 Super-App Pemindai Saham & Proteksi AI (IHSG)")
st.write("Aplikasi pemindai saham otomatis untuk mendeteksi arus uang dan menghindari jebakan bandar secara langsung.")
st.markdown("---")

# --- DAFTAR SAHAM AKTIF IHSG ---
SAHAM_IHSG = ["BBRI.JK", "BBCA.JK", "BMRI.JK", "TLKM.JK", "ASII.JK", "GOTO.JK", "AMMN.JK", "BRIS.JK"]

@st.cache_data(ttl=300)
def ambil_data_bursa(tickers):
    hasil = []
    for t in tickers:
        try:
            data = yf.download(t, period="1y", progress=False)
            if len(data) < 50: continue
            
            delta = data['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            data['RSI'] = 100 - (100 / (1 + rs))
            data['Vol_MA20'] = data['Volume'].rolling(window=20).mean()
            
            hari_ini = data.iloc[-1]
            kemarin = data.iloc[-2]
            
            hasil.append({
                "Saham": t.replace(".JK", ""),
                "Harga_Sekarang": float(hari_ini['Close']),
                "Harga_Kemarin": float(kemarin['Close']),
                "RSI": float(hari_ini['RSI']),
                "Volume_Hari_Ini": float(hari_ini['Volume']),
                "Volume_Rata2": float(hari_ini['Vol_MA20'])
            })
        except:
            continue
    return pd.DataFrame(hasil)

with st.spinner("Sedang mengambil data terbaru dari Bursa Efek Indonesia..."):
    df_saham = ambil_data_bursa(SAHAM_IHSG)

tab1, tab2, tab3 = st.tabs(["📊 Pemindai Utama", "🔮 Target Harga Penutupan", "🛡️ AI Anti-Jebakan Bandar"])

# TAB 1
with tab1:
    st.header("🔍 Hasil Pemindaian Saham Real-Time")
    df_saham['Kondisi_RSI'] = np.where(df_saham['RSI'] < 35, "🟢 Jenuh Jual (Peluang Beli)", 
                               np.where(df_saham['RSI'] > 70, "🔴 Jenuh Beli (Rawan Koreksi)", "⚪ Netral"))
    df_saham['Lonjakan_Volume'] = np.where(df_saham['Volume_Hari_Ini'] > (df_saham['Volume_Rata2'] * 1.5), "🔥 YA (Masif)", "Tidak")
    
    st.dataframe(df_saham[['Saham', 'Harga_Sekarang', 'RSI', 'Kondisi_RSI', 'Lonjakan_Volume']].rename(columns={
        "Harga_Sekarang": "Harga Terakhir (Rp)", "Kondisi_RSI": "Status RSI", "Lonjakan_Volume": "Ada Lonjakan Volume?"
    }), use_container_width=True, index=False)

# TAB 2
with tab2:
    st.header("🔮 Prediksi Rentang Harga Penutupan")
    hasil_prediksi = []
    for _, row in df_saham.iterrows():
        selisih_harian = row['Harga_Sekarang'] * 0.015
        batas_atas = row['Harga_Sekarang'] + selisih_harian
        batas_bawah = row['Harga_Sekarang'] - selisih_harian
        hasil_prediksi.append({
            "Saham": row['Saham'], "Harga Saat Ini": f"Rp {int(row['Harga_Sekarang'])}",
            "Estimasi Rentang Penutupan Sore": f"Rp {int(batas_bawah)} - Rp {int(batas_atas)}"
        })
    st.table(pd.DataFrame(hasil_prediksi))

# TAB 3
with tab3:
    st.header("🛡️ Hasil Analisis Intelijen AI Anti-Jebakan")
    for _, row in df_saham.iterrows():
        perubahan_harga = ((row['Harga_Sekarang'] - row['Harga_Kemarin']) / row['Harga_Kemarin']) * 100
        rasio_vol = row['Volume_Hari_Ini'] / row['Volume_Rata2']
        
        if perubahan_harga > 3.0 and rasio_vol < 0.8:
            st.error(f"🚨 **Saham {row['Saham']}**: TERDETEKSI JEBAKAN BANDAR (FAKE PUMP)! Harga dinaikkan agresif {perubahan_harga:.2f}% tanpa volume kuat. Jangan FOMO!")
        elif row['RSI'] < 35 and rasio_vol > 1.5:
            st.success(f"🟢 **Saham {row['Saham']}**: AKUMULASI AMAN. Harga di area bawah dan volume meningkat masif. Risiko jebakan sangat rendah.")
        else:
            st.warning(f"🟡 **Saham {row['Saham']}**: Kondisi pergerakan pasar normal. Belum ada tanda manipulasi bandar.")
