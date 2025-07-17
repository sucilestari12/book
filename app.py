import streamlit as st
import json
import os

# Konfigurasi halaman
st.set_page_config(
    page_title="Books to Scrape Explorer",
    page_icon="📚",
    layout="wide"
)

# Judul aplikasi
st.title("📚 Books to Scrape Explorer")
st.markdown("""
**Aplikasi Pencarian Buku** | Data diambil dari [books.toscrape.com](https://books.toscrape.com/)
""")
st.divider()

# Memuat data buku
@st.cache_data
def load_books():
    try:
        with open('data/books.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        st.error("File data buku tidak ditemukan!")
        return []
    except json.JSONDecodeError:
        st.error("Format data buku tidak valid!")
        return []

books = load_books()

# Sidebar untuk filter
with st.sidebar:
    st.header("🔍 Filter Pencarian")
    search_term = st.text_input("Cari judul buku:")
    
    min_price, max_price = st.slider(
        "Rentang Harga (£)",
        0.0, 100.0, (0.0, 50.0)
    )
    
    rating_options = ["All", "One", "Two", "Three", "Four", "Five"]
    selected_rating = st.selectbox("Rating Buku", rating_options)
    
    availability = st.checkbox("Tampilkan hanya stok tersedia", True)

# Filter data
filtered_books = [
    book for book in books
    if (search_term.lower() in book['title'].lower() or not search_term) and
    (min_price <= float(book['price'].replace('£', '')) <= max_price) and
    (selected_rating == "All" or book['rating'] == selected_rating) and
    (not availability or "In stock" in book['availability'])
]

# Tampilkan hasil
st.subheader(f"📊 Hasil Pencarian: {len(filtered_books)} buku ditemukan")

if not filtered_books:
    st.warning("Tidak ada buku yang sesuai dengan kriteria pencarian!")
else:
    for book in filtered_books:
        with st.expander(f"**{book['title']}**"):
            col1, col2 = st.columns([1, 3])
            with col1:
                st.metric("Harga", book['price'])
            with col2:
                st.caption(f"**Rating:** {book['rating']} bintang")
                st.caption(f"**Ketersediaan:** {book['availability']}")
                st.progress(int(book['rating'][0]) * 20 if book['rating'][0].isdigit() else 0)

# Footer
st.divider()
st.caption("""
**Aplikasi Ujian Akhir Semester** | 
Dibuat dengan Scrapy + Streamlit | 
© Sistem Informasi - Universitas Abulyatama 2025
""")
