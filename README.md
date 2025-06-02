# Sistem Pemesanan Lapangan Olahraga

Aplikasi pemesanan lapangan olahraga berbasis web dengan backend Pyramid dan frontend React.

## Struktur Proyek

Proyek ini terdiri dari dua bagian utama:

- **Backend (`lapangan_backend`)**: API server berbasis Pyramid dengan PostgreSQL
- **Frontend (`frontend_lapangan`)**: Aplikasi React untuk antarmuka pengguna

## Fitur Utama

### Umum
- Sistem autentikasi dengan token JWT
- Role-based access control (admin dan user)
- Manajemen transaksi database yang aman

### Admin
- Manajemen lapangan (tambah, edit, hapus)
- Manajemen pemesanan (lihat semua, update status, hapus)
- Dashboard admin untuk monitoring

### User
- Melihat daftar lapangan yang tersedia
- Membuat pemesanan lapangan
- Melihat dan mengelola pemesanan sendiri

## Entitas Utama

1. **User**
   - id
   - full_name
   - email
   - password
   - role (admin/user)

2. **Court (Lapangan)**
   - id_court
   - court_name
   - court_category
   - description
   - status

3. **Booking (Pemesanan)**
   - id
   - user_id
   - court_id
   - booking_date
   - time_slot
   - full_name
   - phone_number
   - status (pending, confirmed, cancelled)

## Teknologi

### Backend
- Pyramid Framework
- SQLAlchemy ORM
- PostgreSQL
- pyramid_tm (Transaction Management)
- pyramid_jwt (Authentication)
- Alembic (Database Migrations)

### Frontend
- React
- Axios
- React Router
- Bootstrap

## Instalasi dan Penggunaan

### Prasyarat
- Python 3.8+
- PostgreSQL
- Node.js dan npm

### Setup Backend

1. Buat virtual environment
   ```
   python -m venv myenv
   ```

2. Aktifkan virtual environment
   ```
   # Windows
   myenv\Scripts\activate
   
   # Linux/Mac
   source myenv/bin/activate
   ```

3. Install dependencies
   ```
   cd lapangan_backend
   pip install -e .
   ```

4. Setup database
   ```
   # Buat database PostgreSQL
   createdb lapangan_backend
   
   # Jalankan migrasi
   alembic upgrade head
   ```

5. Jalankan server
   ```
   pserve development.ini --reload
   ```

### Setup Frontend

1. Install dependencies
   ```
   cd frontend_lapangan
   npm install
   ```

2. Jalankan aplikasi
   ```
   npm start
   ```

## API Endpoints

### Authentication
- POST `/login` - Login user
- POST `/register` - Register user baru

### Courts (Lapangan)
- GET `/courts` - Daftar semua lapangan
- GET `/courts/{id_court}` - Detail lapangan
- POST `/courts` - Tambah lapangan baru (admin)
- PUT `/courts/{id_court}` - Update lapangan (admin)
- DELETE `/courts/{id_court}` - Hapus lapangan (admin)

### Bookings (Pemesanan)
- GET `/bookings/users/{user_id}` - Daftar pemesanan user
- GET `/bookings/{id}/users/{user_id}` - Detail pemesanan
- POST `/bookings` - Buat pemesanan baru
- PUT `/bookings/{id}/users/{user_id}` - Update pemesanan
- DELETE `/bookings/{id}/users/{user_id}` - Batalkan pemesanan

### Admin Endpoints
- GET `/admin/bookings` - Daftar semua pemesanan
- GET `/admin/bookings/{id}` - Detail pemesanan
- PUT `/admin/bookings/{id}` - Update pemesanan
- PUT `/admin/bookings/{id}/status` - Update status pemesanan
- DELETE `/admin/bookings/{id}` - Hapus pemesanan

## Kontributor

- Kiel Kiel - Developer

## Lisensi

Hak Cipta © 2025 Kiel Kiel
