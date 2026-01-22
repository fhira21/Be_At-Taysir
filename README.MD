# Warung Pintar Backend

Backend API untuk aplikasi penyimpanan dan manajemen harga barang toko.
Dibangun menggunakan **FastAPI**, **PostgreSQL**, dan **SQLAlchemy**.

## 🚀 Fitur
- Manajemen Produk
- Manajemen Supplier
- Harga Dasar (Base Price)
- Harga Jual (Sell Price)
- Pencarian katalog produk
- Proteksi akses menggunakan PIN (logic-based)
- Dokumentasi otomatis via Swagger

---

## 🛠️ Tech Stack
- Python 3.10+
- FastAPI
- SQLAlchemy
- PostgreSQL
- Uvicorn

---

## 📦 Instalasi

### 1. Clone Repository
```bash
git clone https://github.com/username/warung-backend.git
cd warung-backend
```

### 2. Buat Virtual Environment
```bash
phyton -m venv venv
venv\Scripts\activate #Windows
```

### 3. Install Dependency
```bash
pip install -r requirements.txt
```

### 4. Konfigurasi Environment
buat file .env ( TIDAK di-push ke Github )

```env
DATABASE_URL=postgresql://user:password@localhost:5432/warung_db
PIN_SECRET=1234
```

### ▶️ Menjalankan Server
```bash
uvicorn app.main:app --reload
```

Akses API:
- Swagger UI → http://localhost:8000/docs
- ReDoc → http://localhost:8000/redoc

### 🔐 Proteksi PIN

- Akses data katalog dibatasi menggunakan PIN
- Validasi dilakukan di backend
- PIN disimpan di environment variable

### ❗ Catatan Penting

- Pastikan PostgreSQL aktif
- Pastikan database sudah dibuat
- File .env WAJIB di-ignore
- Backend bersifat REST API (tidak mengurus UI)


### 📌 Contributors
Fhira Triana Maulani