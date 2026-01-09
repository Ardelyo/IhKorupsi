# IH-Korupsi - Changelog dan Catatan Proyek

## Versi 1.0.0 - Rilis Awal

### Dibuat oleh
**OurCreativity Edisi Coding**

### Tanggal Rilis
9 Januari 2026

### Fitur yang Diimplementasikan

#### 1. Modul The Mathematician
- ✅ Hukum Benford untuk deteksi manipulasi angka
- ✅ Relative Size Factor (RSF) untuk deteksi outlier vendor
- ✅ Z-Score dan IQR untuk deteksi pencilan

#### 2. Modul The Connector
- ✅ Deteksi perdagangan memutar (circular trading)
- ✅ Analisis sentralitas menggunakan PageRank dan Betweenness
- ✅ Deteksi komunitas/kluster tersembunyi

#### 3. Modul The Chronologist
- ✅ Deteksi Fiscal Cliff (budget dumping)
- ✅ Velocity check untuk transaksi tidak wajar

#### 4. Modul String Detective
- ✅ Fuzzy matching dengan Levenshtein Distance
- ✅ Deteksi vendor hantu

### Teknologi yang Digunakan
- Python 3.10+
- Pandas untuk manipulasi data
- NumPy untuk operasi matematika
- NetworkX untuk analisis graf
- SciPy untuk statistik

### Prinsip Desain
1. **Zero AI**: Tidak menggunakan Machine Learning sama sekali
2. **Transparan**: Setiap deteksi bisa dijelaskan secara matematis
3. **Auditable**: Kode terbuka dan bisa diverifikasi
4. **Edukatif**: Dibuat untuk pembelajaran dan transparansi publik

### Penggunaan
```bash
python main.py --type sample
```

### Lisensi
MIT License

### Kontribusi
Terbuka untuk kontribusi dari komunitas!

---

*Demi Indonesia Bebas Korupsi*
