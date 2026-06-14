import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np

# Konfigurasi halaman tema gelap profesional
st.set_page_config(page_title="SahamPro Dashboard", page_icon="📈", layout="wide")

# Custom CSS untuk membuat komponen kotak kartu mirip aplikasi Ajaib
st.markdown("""
<style>
    .main-title { font-size: 24px; font-weight: bold; color: #ffffff; margin-bottom: 2px; }
    .section-title { font-size: 18px; font-weight: bold; color: #ffffff; margin-top: 15px; margin-bottom: 10px; }
    .market-card { background-color: #121214; padding: 12px; border-radius: 8px; border: 1px solid #27272a; margin-bottom: 10px; }
    .card-name { font-size: 13px; color: #9ca3af; font-weight: 500; }
    .card-value { font-size: 16px; font-weight: bold; margin: 4px 0; }
    .text-green { color: #22c55e; font-size: 12px; font-weight: bold; }
    .text-red { color: #ef4444; font-size: 12px; font-weight: bold; }
    
    /* Screener Card Style */
    .screener-card { padding: 15px; border-radius: 8px; margin-bottom: 10px; border: 1px solid #27272a; }
    .bg-buy { background-color: #062f1c; border-left: 4px solid #22c55e; }
    .bg-sell { background-color: #450a0a; border-left: 4px solid #ef4444; }
    .bg-hold { background-color: #18181b; border-left: 4px solid #71717a; }
</style>
""", unsafe_allow_html=True)

# --- HEADER APLIKASI ---
st.markdown('<div class="main-title">📈 SahamPro AI Dashboard</div>', unsafe_allow_html=True)
st.caption("Data kompilasi pasar global, komoditas, dan pemindai saham berbasis kecerdasan buatan.")

# --- SIDEBAR PANEL CONTROL ---
st.sidebar.header("🎯 Pusat Kendali Watchlist")
if 'watchlist' not in st.session_state:
    st.session_state['watchlist'] = ['BBCA.JK', 'BBRI.JK', 'AAPL', 'TSLA', 'NVDA']

saham_baru = st.sidebar.text_input("➕ Tambah Kode Saham:", placeholder="Contoh: ANTM.JK atau MSFT").upper()
if saham_baru and saham_baru not in st.session_state['watchlist']:
    st.session_state['watchlist'].append(saham_baru)

pilihan_saham = st.sidebar.multiselect("Saham Dipantau:", options=st.session_state['watchlist'], default=st.session_state['watchlist'])
tombol_refresh = st.sidebar.button("🔄 Segarkan Data Pasar", type="primary")

# --- FUNGSI HELPER AMBIL DATA CEPAT ---
def dapatkan_data_indeks(ticker_symbol, nama_tampilan):
    try:
        ticker = yf.Ticker(ticker_symbol)
        hist = ticker.history(period="2d")
        if len(hist) >= 2:
            close_now = hist['Close'].iloc[-1]
            close_prev = hist['Close'].iloc[-2]
            pct_change = ((close_now - close_prev) / close_prev) * 100
            
            color_class = "text-green" if pct_change >= 0 else "text-red"
            sign = "+" if pct_change >= 0 else ""
            fmt_val = f"{close_now:,.2f}" if "." in ticker_symbol or close_now < 1000 else f"{close_now:,.0f}"
            
            return f"""
            <div class="market-card">
                <div class="card-name">{nama_tampilan}</div>
                <div class="card-value">{fmt_val}</div>
                <div class="{color_class}">{sign}{pct_change:.2f}%</div>
            </div>
            """
    except:
        pass
    return f'<div class="market-card"><div class="card-name">{nama_tampilan}</div><div class="card-value">--</div><div>0.00%</div></div>'

# --- 1. SEKSI PASAR AS & ID (GRID STYLE ALA AJAIB) ---
st.markdown('<div class="section-title">🇺🇸 Pasar AS</div>', unsafe_allow_html=True)
col_as1, col_as2, col_as3, col_as4 = st.columns(4)
with col_as1: st.markdown(dapatkan_data_indeks("^GSPC", "S&P 500"), unsafe_allow_html=True)
with col_as2: st.markdown(dapatkan_data_indeks("^IXIC", "NASDAQ"), unsafe_allow_html=True)
with col_as3: st.markdown(dapatkan_data_indeks("^DJI", "DJIA"), unsafe_allow_html=True)
with col_as4: st.markdown(dapatkan_data_indeks("^RUT", "IWM (Russell 2000)"), unsafe_allow_html=True)

st.markdown('<div class="section-title">🇮🇩 Pasar ID</div>', unsafe_allow_html=True)
col_id1, col_id2, col_empty1, col_empty2 = st.columns(4)
with col_id1: st.markdown(dapatkan_data_indeks("^JKSE", "IHSG"), unsafe_allow_html=True)
with col_id2: st.markdown(dapatkan_data_indeks("^JK30", "IDX 30"), unsafe_allow_html=True)

# --- 2. SEKSI KOMODITAS ---
st.markdown('<div class="section-title">🪙 Komoditas</div>', unsafe_allow_html=True)
col_kom1, col_kom2, col_kom3, col_kom4 = st.columns(4)
with col_kom1: st.markdown(dapatkan_data_indeks("GC=F", "Gold (Emas)"), unsafe_allow_html=True)
with col_kom2: st.markdown(dapatkan_data_indeks("SI=F", "Silver (Perak)"), unsafe_allow_html=True)
with col_kom3: st.markdown(dapatkan_data_indeks("HG=F", "Copper (Tembaga)"), unsafe_allow_html=True)
with col_kom4: st.markdown(dapatkan_data_indeks("CL=F", "Crude Oil (Minyak)"), unsafe_allow_html=True)

# --- 3. SEKSI SEKTOR RINGKASAN ---
st.markdown('<div class="section-title">🗂️ Ringkasan Sektor Global</div>', unsafe_allow_html=True)
col_sec1, col_sec2, col_sec3, col_sec4 = st.columns(4)
with col_sec1: st.markdown('<div class="market-card"><div class="card-name">🛠️ Teknologi</div><div class="card-value text-green">+0.73%</div></div>', unsafe_allow_html=True)
with col_sec2: st.markdown('<div class="market-card"><div class="card-name">🏦 Keuangan</div><div class="card-value text-green">+1.16%</div></div>', unsafe_allow_html=True)
with col_sec3: st.markdown('<div class="market-card"><div class="card-name">⚡ Energi</div><div class="card-value text-green">+0.47%</div></div>', unsafe_allow_html=True)
with col_sec4: st.markdown('<div class="market-card"><div class="card-name">🏥 Kesehatan</div><div class="card-value text-red">-0.34%</div></div>', unsafe_allow_html=True)

st.write("---")

# --- 4. ROBOT AI SCREENER & WATCHLIST ---
st.markdown('<div class="section-title">🤖 AI Insights & Watchlist Screener</div>', unsafe_allow_html=True)

def hitung_rsi(data, periode=14):
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=periode).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=periode).mean()
    rs = gain / (loss + 1e-10)
    return 100 - (100 / (1 + rs))

if pilihan_saham:
    for tickers in pilihan_saham:
        try:
            saham = yf.Ticker(tickers)
            hist = saham.history(period="3mo")
            if len(hist) < 15: continue
            
            harga_sekarang = hist['Close'].iloc[-1]
            harga_kemarin = hist['Close'].iloc[-2]
            perubahan_persen = ((harga_sekarang - harga_kemarin) / harga_kemarin) * 100
            
            hist['RSI'] = hitung_rsi(hist['Close'])
            rsi_terakhir = hist['RSI'].iloc[-1]
            
            # Atur kategori rekomendasi sinyal
            if rsi_terakhir < 35:
                status, bg_class, text_color = "BUY ON WEAKNESS (Jenuh Jual / Murah)", "bg-buy", "#22c55e"
            elif rsi_terakhir > 65:
                status, bg_class, text_color = "TAKE PROFIT / OVERBOUGHT (Jenuh Beli / Mahal)", "bg-sell", "#ef4444"
            else:
                status, bg_class, text_color = "TRADING BUY / HOLD (Stabil Netral)", "bg-hold", "#9ca3af"
                
            simbol_uang = "Rp " if ".JK" in tickers else "$ "
            tanda_plus = "+" if perubahan_persen >= 0 else ""
            warna_persen = "color:#22c55e;" if perubahan_persen >= 0 else "color:#ef4444;"
            
            st.markdown(f"""
            <div class="screener-card {bg_class}">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <b>🔍 {tickers}</b>
                    <span style="{warna_persen} font-weight:bold;">{tanda_plus}{perubahan_persen:.2f}%</span>
                </div>
                <div style="font-size: 15px; font-weight: bold; margin-top: 5px; color:{text_color};">{status}</div>
                <div style="font-size: 13px; color: #a1a1aa; margin-top: 3px;">
                    Harga: {simbol_uang}{harga_sekarang:,.2f} | Skor RSI: {rsi_terakhir:.2f}
                </div>
            </div>
            """, unsafe_allow_html=True)
        except:
            continue
else:
    st.info("Watchlist kosong. Tambahkan kode saham di panel samping menu.")
