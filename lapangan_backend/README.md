# Lapangan Backend

Backend API untuk sistem pemesanan lapangan olahraga menggunakan Pyramid Framework dan PostgreSQL.

## Fitur

- Autentikasi berbasis token
- Role-based access control (admin dan user)
- Manajemen lapangan (CRUD)
- Pemesanan lapangan dengan validasi ketersediaan
- Manajemen status pemesanan (pending, confirmed, cancelled)
- API endpoints untuk admin dan user
- Penanganan transaksi database yang aman
- Validasi data dengan Marshmallow
- Upload dan manajemen gambar lapangan

## Struktur Proyek

```
lapangan_backend/
├── alembic/                  # Migrasi database
├── lapangan_backend/         # Kode utama
│   ├── auth/                 # Autentikasi dan otorisasi
│   │   ├── acl.py            # Access Control Lists
│   │   ├── security.py       # Fungsi keamanan
│   │   └── token_auth.py     # Autentikasi berbasis token
│   ├── middleware/           # Middleware aplikasi
│   ├── models/               # Domain models
│   │   ├── booking.py        # Model booking
│   │   ├── court.py          # Model lapangan
│   │   └── user.py           # Model user
│   ├── orms/                 # SQLAlchemy ORM models
│   │   ├── booking.py        # ORM booking
│   │   ├── court.py          # ORM lapangan
│   │   ├── meta.py           # Metadata ORM
│   │   └── user.py           # ORM user
│   ├── schemas/              # Marshmallow schemas
│   │   ├── booking.py        # Schema booking
│   │   ├── court.py          # Schema lapangan
│   │   └── user.py           # Schema user
│   ├── static/               # File statis
│   │   └── uploads/          # Upload gambar
│   ├── views/                # View handlers
│   │   ├── admin_booking.py  # Admin booking views
│   │   ├── booking.py        # Booking views
│   │   ├── court.py          # Court views
│   │   └── user.py           # User views
│   ├── __init__.py           # Konfigurasi aplikasi
│   └── routes.py             # Definisi routes
├── development.ini           # Konfigurasi development
└── production.ini            # Konfigurasi production
```

## Instalasi

### Prasyarat

- Python 3.8+
- PostgreSQL
- pip

### Langkah-langkah

1. Clone repositori
   ```
   git clone <repository-url>
   cd lapangan_backend
   ```

2. Buat dan aktifkan virtual environment
   ```
   python -m venv myenv
   
   # Windows
   myenv\Scripts\activate
   
   # Linux/Mac
   source myenv/bin/activate
   ```

3. Install dependencies
   ```
   pip install -e .
   ```

4. Buat database PostgreSQL
   ```
   createdb lapangan_backend
   ```

5. Jalankan migrasi database
   ```
   alembic upgrade head
   ```

6. Jalankan server development
   ```
   pserve development.ini --reload
   ```

## API Endpoints

### Autentikasi

- `POST /login` - Login user
- `POST /register` - Register user baru

### Lapangan (Courts)

- `GET /courts` - Daftar semua lapangan
- `GET /courts/{id_court}` - Detail lapangan
- `POST /courts` - Tambah lapangan baru (admin)
- `PUT /courts/{id_court}` - Update lapangan (admin)
- `DELETE /courts/{id_court}` - Hapus lapangan (admin)

### Pemesanan (Bookings)

- `GET /bookings/users/{user_id}` - Daftar pemesanan user
- `GET /bookings/{id}/users/{user_id}` - Detail pemesanan
- `POST /bookings` - Buat pemesanan baru
- `PUT /bookings/{id}/users/{user_id}` - Update pemesanan
- `DELETE /bookings/{id}/users/{user_id}` - Batalkan pemesanan

### Admin Endpoints

- `GET /admin/bookings` - Daftar semua pemesanan
- `GET /admin/bookings/{id}` - Detail pemesanan
- `PUT /admin/bookings/{id}` - Update pemesanan
- `PUT /admin/bookings/{id}/status` - Update status pemesanan
- `DELETE /admin/bookings/{id}` - Hapus pemesanan

## Catatan Penting

1. **Status Booking**:
   - Status booking yang valid adalah: `pending`, `confirmed`, dan `cancelled`
   - Status ini didefinisikan sebagai Enum di database dan harus konsisten

2. **Penanganan Transaksi**:
   - Aplikasi menggunakan `pyramid_tm` untuk manajemen transaksi
   - Pastikan untuk memanggil `request.tm.abort()` saat terjadi error untuk rollback transaksi

3. **Autentikasi**:
   - Token JWT digunakan untuk autentikasi
   - Endpoint admin memerlukan role `admin`
   - User hanya dapat mengakses data mereka sendiri

4. **Upload Gambar**:
   - Gambar lapangan disimpan di `static/uploads/courts/`
   - Akses gambar melalui URL `/static/uploads/courts/{filename}`

## Troubleshooting

### Error Transaksi Database

Jika mengalami error `transaction.interfaces.NoTransaction`:
- Pastikan transaksi database diinisialisasi dengan benar
- Gunakan blok `with transaction.manager:` untuk operasi database yang kompleks
- Panggil `transaction.abort()` saat terjadi error

### Error Autentikasi

Jika mengalami masalah autentikasi:
- Periksa token yang dikirim dalam header `Authorization: Bearer <token>`
- Pastikan user memiliki role yang sesuai untuk akses endpoint

## Pengembangan Lanjutan

- Implementasi caching untuk meningkatkan performa
- Penambahan fitur notifikasi untuk perubahan status booking
- Implementasi sistem pembayaran
- Penambahan fitur laporan dan analitik untuk admin
