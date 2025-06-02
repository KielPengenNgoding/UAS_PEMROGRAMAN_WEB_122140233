import React, { useState, useEffect } from "react";
import { FaUserCircle, FaChartLine, FaBook, FaHistory, FaSpinner, FaPlusCircle, FaTimes, FaEdit, FaCheck } from "react-icons/fa";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { config } from '../config';
import '../styles/Dashboard.css';

// Import components
import Stats from '../components/dashboard/Stats';
import BookingTable from '../components/dashboard/BookingTable';
import CourtTable from '../components/dashboard/CourtTable';
import FilterSection from '../components/dashboard/FilterSection';
import AddCourtForm from '../components/dashboard/AddCourtForm';
import EditCourtModal from '../components/dashboard/EditCourtModal';
import DeleteConfirmModal from '../components/dashboard/DeleteConfirmModal';

function Dashboard() {
  const [bookings, setBookings] = useState([]);
  const [courts, setCourts] = useState([]);
  const [categories, setCategories] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState("");
  const [selectedStatus, setSelectedStatus] = useState("");
  const [statuses, setStatuses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [stats, setStats] = useState({
    totalBookings: 0,
    upcomingBookings: 0,
    completedBookings: 0
  });
  const navigate = useNavigate();
  const [adminName, setAdminName] = useState("");
  
  // State untuk form tambah court
  const [showAddCourtForm, setShowAddCourtForm] = useState(false);
  const [newCourt, setNewCourt] = useState({
    court_name: "",
    court_category: "",
    description: "",
    status: "available"
  });
  const [courtImage, setCourtImage] = useState(null);
  const [imagePreview, setImagePreview] = useState(null);
  const [addCourtLoading, setAddCourtLoading] = useState(false);
  const [addCourtError, setAddCourtError] = useState("");
  const [addCourtSuccess, setAddCourtSuccess] = useState("");
  
  // State untuk menampilkan tab yang aktif
  const [activeTab, setActiveTab] = useState("bookings"); // bookings atau courts
  
  // State untuk edit court
  const [editCourtId, setEditCourtId] = useState(null);
  const [editCourtData, setEditCourtData] = useState({
    court_name: "",
    court_category: "",
    description: "",
    status: "available"
  });
  const [editCourtImage, setEditCourtImage] = useState(null);
  const [editImagePreview, setEditImagePreview] = useState(null);
  const [editCourtLoading, setEditCourtLoading] = useState(false);
  const [editCourtError, setEditCourtError] = useState("");
  const [editCourtSuccess, setEditCourtSuccess] = useState("");
  
  // State untuk konfirmasi delete
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);
  const [deleteCourtId, setDeleteCourtId] = useState(null);
  const [deleteCourtName, setDeleteCourtName] = useState("");
  const [deleteCourtLoading, setDeleteCourtLoading] = useState(false);
  
  // State untuk edit status booking
  const [editBookingId, setEditBookingId] = useState(null);
  const [editBookingStatus, setEditBookingStatus] = useState("");
  const [editBookingLoading, setEditBookingLoading] = useState(false);

  // Handler untuk form tambah court
  const handleCourtInputChange = (e) => {
    const { name, value } = e.target;
    setNewCourt(prev => ({
      ...prev,
      [name]: value
    }));
  };
  
  // Handler untuk upload gambar
  const handleImageChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      // Validasi tipe file
      const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif'];
      if (!allowedTypes.includes(file.type)) {
        setAddCourtError('Format file tidak didukung. Gunakan JPG, JPEG, PNG, atau GIF.');
        return;
      }

      // Validasi ukuran file (max 5MB)
      if (file.size > 5 * 1024 * 1024) {
        setAddCourtError('Ukuran file terlalu besar. Maksimal 5MB.');
        return;
      }

      setCourtImage(file);
      
      // Membuat preview gambar
      const reader = new FileReader();
      reader.onloadend = () => {
        setImagePreview(reader.result);
      };
      reader.readAsDataURL(file);
    }
  };
  
  // Reset form gambar
  const resetImageForm = () => {
    setCourtImage(null);
    setImagePreview(null);
  };
  
  // Reset form edit gambar
  const resetEditImageForm = () => {
    setEditCourtImage(null);
    setEditImagePreview(null);
  };
  
  // Handler untuk edit image
  const handleEditImageChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setEditCourtImage(file);
      
      // Membuat preview gambar
      const reader = new FileReader();
      reader.onloadend = () => {
        setEditImagePreview(reader.result);
      };
      reader.readAsDataURL(file);
    }
  };
  
  // Handler untuk memulai edit court
  const handleStartEditCourt = (court) => {
    setEditCourtId(court.id_court);
    setEditCourtData({
      court_name: court.court_name,
      court_category: court.court_category,
      description: court.description || "",
      status: court.status || "available"
    });
    setEditImagePreview(court.image_url ? `http://localhost:6543${court.image_url}` : null);
  };
  
  // Handler untuk input edit court
  const handleEditCourtInputChange = (e) => {
    const { name, value } = e.target;
    setEditCourtData(prev => ({
      ...prev,
      [name]: value
    }));
  };
  
  // Handler untuk cancel edit
  const handleCancelEdit = () => {
    setEditCourtId(null);
    setEditCourtData({
      court_name: "",
      court_category: "",
      description: "",
      status: "available"
    });
    resetEditImageForm();
    setEditCourtError("");
    setEditCourtSuccess("");
  };
  
  // Handler untuk update court
  const handleUpdateCourt = async (e) => {
    e.preventDefault();
    setEditCourtLoading(true);
    setEditCourtError("");
    setEditCourtSuccess("");
    
    const authToken = localStorage.getItem("authToken");
    
    try {
      // Update court data with proper status field
      const updateData = {
        ...editCourtData,
        status: editCourtData.status || 'available' // Ensure status is always set
      };
      
      // Update court data
      await axios.put(
        `http://localhost:6543/admin/courts/${editCourtId}`,
        updateData,
        { headers: { Authorization: `Bearer ${authToken}` } }
      );
      
      // Jika ada gambar baru, upload gambar
      if (editCourtImage) {
        console.log("Uploading new image for court ID:", editCourtId);
        console.log("Image file:", editCourtImage);
        
        const formData = new FormData();
        formData.append('image', editCourtImage);
        
        // Log FormData contents for debugging
        console.log("FormData entries:");
        for (let pair of formData.entries()) {
          console.log(pair[0] + ': ' + (pair[1] instanceof File ? 
            `File: ${pair[1].name}, size: ${pair[1].size}, type: ${pair[1].type}` : pair[1]));
        }
        
        try {
          const uploadResponse = await axios.post(
            `${config.backendUrl}/admin/courts/${editCourtId}/upload-image`,
            formData,
            { 
              headers: { 
                'Authorization': `Bearer ${authToken}`,
                'Content-Type': 'multipart/form-data'
              } 
            }
          );
          
          console.log("Image upload successful:", uploadResponse.data);
          setEditCourtSuccess("Court updated and image uploaded successfully");
        } catch (uploadError) {
          console.error("Error uploading image:", uploadError);
          console.error("Error response:", uploadError.response?.data);
          setError(`Error uploading image: ${uploadError.response?.data?.message || uploadError.message}`);
        }
      }
      
      // Refresh court list
      fetchCourts();
      
      setEditCourtSuccess("Lapangan berhasil diperbarui!");
      setEditCourtLoading(false);
      
      // Hide form after successful submission
      setTimeout(() => {
        handleCancelEdit();
      }, 2000);
      
    } catch (err) {
      console.error("Error updating court:", err);
      setEditCourtError(err.response?.data?.message || "Gagal memperbarui lapangan. Silakan coba lagi.");
      setEditCourtLoading(false);
    }
  };
  
  // Handler untuk konfirmasi delete court
  const handleConfirmDelete = (court) => {
    setDeleteCourtId(court.id_court);
    setDeleteCourtName(court.court_name);
    setShowDeleteConfirm(true);
  };
  
  // Handler untuk cancel delete
  const handleCancelDelete = () => {
    setShowDeleteConfirm(false);
    setDeleteCourtId(null);
    setDeleteCourtName("");
  };
  
  // Handler untuk delete court
  const handleDeleteCourt = async () => {
    setDeleteCourtLoading(true);
    
    const authToken = localStorage.getItem("authToken");
    
    try {
      await axios.delete(
        `http://localhost:6543/admin/courts/${deleteCourtId}`,
        { headers: { Authorization: `Bearer ${authToken}` } }
      );
      
      // Refresh court list
      fetchCourts();
      
      setDeleteCourtLoading(false);
      handleCancelDelete();
      
    } catch (err) {
      console.error("Error deleting court:", err);
      alert(err.response?.data?.message || "Gagal menghapus lapangan. Silakan coba lagi.");
      setDeleteCourtLoading(false);
    }
  };
  
  // Handler untuk update status booking
  const handleUpdateBookingStatus = async (bookingId, newStatus) => {
    setEditBookingId(bookingId);
    setEditBookingLoading(true);
    
    const authToken = localStorage.getItem("authToken");
    
    try {
      console.log(`Updating booking ${bookingId} status to ${newStatus}`);
      const response = await axios.put(
        `http://localhost:6543/admin/bookings/${bookingId}/status`,
        { status: newStatus },
        { headers: { Authorization: `Bearer ${authToken}` } }
      );
      
      console.log("Status update response:", response.data);
      
      // Refresh data by fetching bookings and courts again
      const bookingsResponse = await axios.get("http://localhost:6543/admin/bookings", {
        headers: { Authorization: `Bearer ${authToken}` },
        withCredentials: true
      });
      
      const courtsResponse = await axios.get("http://localhost:6543/admin/courts", {
        headers: { Authorization: `Bearer ${authToken}` },
        withCredentials: true
      });
      
      // Format booking data
      const formattedBookings = bookingsResponse.data.data.map(booking => {
        const bookingDate = new Date(booking.time);
        return {
          id: booking.id,
          user: booking.full_name,
          date: bookingDate.toLocaleDateString('id-ID'),
          time: bookingDate.toLocaleTimeString('id-ID', { hour: '2-digit', minute: '2-digit' }),
          court: booking.court_name,
          status: booking.status,
          phone: booking.phone_number
        };
      });
      
      setBookings(formattedBookings);
      setCourts(courtsResponse.data.data);
      setCategories(courtsResponse.data.categories || []);
      setStatuses(courtsResponse.data.statuses || []);
      
      // Tampilkan notifikasi sukses
      alert("Status booking berhasil diperbarui!");
      
      setEditBookingLoading(false);
      setEditBookingId(null);
      
    } catch (err) {
      console.error("Error updating booking status:", err);
      if (err.response) {
        console.error("Error response data:", err.response.data);
        console.error("Error status:", err.response.status);
        alert(err.response.data?.message || "Gagal mengubah status booking. Silakan coba lagi.");
      } else {
        alert("Gagal mengubah status booking. Silakan coba lagi.");
      }
      setEditBookingLoading(false);
      setEditBookingId(null);
    }
  };
  
  // Fungsi untuk mendapatkan warna berdasarkan status booking
  const getStatusColor = (status) => {
    switch (status) {
      case "confirmed":
        return "bg-green-100 text-green-800";
      case "pending":
        return "bg-yellow-100 text-yellow-800";
      case "cancelled":
        return "bg-red-100 text-red-800";
      case "completed":
        return "bg-blue-100 text-blue-800";
      default:
        return "bg-gray-100 text-gray-800";
    }
  };

  // Handler untuk tambah court
  const handleAddCourt = async (e) => {
    e.preventDefault();
    setAddCourtLoading(true);
    setAddCourtError("");
    setAddCourtSuccess("");
    
    try {
      // Validasi gambar
      if (!courtImage) {
        setAddCourtError("Harap pilih gambar lapangan");
        setAddCourtLoading(false);
        return;
      }

      // Generate nama file yang unik
      const fileExt = courtImage.name.split('.').pop();
      const fileName = `${newCourt.court_category.toLowerCase()}${Date.now()}.${fileExt}`;

      // Simpan data court dengan nama file gambar
      const courtData = {
        ...newCourt,
        image_url: fileName // Hanya simpan nama file
      };

      // Buat FormData untuk upload file
      const formData = new FormData();
      formData.append('image', courtImage);
      formData.append('filename', fileName);

      // Upload gambar ke folder public/images
      await axios.post(
        `${config.backendUrl}/admin/upload-image`,
        formData,
        { 
          headers: { 
            'Authorization': `Bearer ${localStorage.getItem("authToken")}`,
            'Content-Type': 'multipart/form-data'
          }
        }
      );

      // Simpan data court
      await axios.post(
        `${config.backendUrl}/admin/courts`,
        courtData,
        { headers: { Authorization: `Bearer ${localStorage.getItem("authToken")}` } }
      );

      // Reset form
      setNewCourt({
        court_name: "",
        court_category: "",
        description: "",
        status: "available"
      });
      resetImageForm();
      
      setAddCourtSuccess("Lapangan berhasil ditambahkan!");
      fetchCourts(); // Refresh daftar lapangan
      
      setTimeout(() => {
        setShowAddCourtForm(false);
        setAddCourtSuccess("");
      }, 2000);
      
    } catch (err) {
      console.error("Error adding court:", err);
      setAddCourtError(err.response?.data?.message || "Gagal menambahkan lapangan. Silakan coba lagi.");
    } finally {
      setAddCourtLoading(false);
    }
  };
  
  // Fungsi untuk mengambil data courts saja
  const fetchCourts = async () => {
    const authToken = localStorage.getItem("authToken");
    
    try {
      console.log("Fetching admin courts with token:", authToken);
      
      // Build query string for filters
      const queryParams = new URLSearchParams();
      if (selectedCategory) queryParams.append('category', selectedCategory);
      if (selectedStatus) queryParams.append('status', selectedStatus);
      
      const courtsResponse = await axios.get(
        `http://localhost:6543/admin/courts?${queryParams.toString()}`,
        { headers: { Authorization: `Bearer ${authToken}` } }
      );
      console.log("Courts response:", courtsResponse.data);
      
      setCourts(courtsResponse.data.data);
      setCategories(courtsResponse.data.categories || []);
      setStatuses(courtsResponse.data.statuses || []);
    } catch (error) {
      console.error("Error fetching courts:", error);
    }
  };
  
  useEffect(() => {
    // Fungsi untuk memeriksa autentikasi admin
    const checkAuth = () => {
      const userRole = localStorage.getItem("userRole");
      const authToken = localStorage.getItem("authToken");
      const userName = localStorage.getItem("userName");
      
      console.log("Auth check - Role:", userRole, "Token:", authToken ? "Present" : "Missing");
      
      if (!authToken) {
        console.log("No auth token found, redirecting to login");
        navigate("/login");
        return { isAuth: false, token: null };
      }
      
      if (userRole !== "admin") {
        console.log("User is not admin, redirecting to login");
        navigate("/login");
        return { isAuth: false, token: null };
      }
      
      setAdminName(userName || "Admin");
      return { isAuth: true, token: authToken };
    };
    
    // Fungsi untuk mengambil data dari API
    const fetchData = async () => {
      // Periksa autentikasi dan dapatkan token
      const auth = checkAuth();
      if (!auth.isAuth) return;
      
      const token = auth.token;
      console.log("Using token for requests:", token);
      
      try {
        setLoading(true);
        
        // Fetch all bookings
        console.log("Fetching admin bookings with token:", token);
        const bookingsResponse = await axios.get("http://localhost:6543/admin/bookings", {
          headers: { Authorization: `Bearer ${token}` },
          withCredentials: true // Tetap sertakan cookie untuk kompatibilitas
        });
        
        console.log("Bookings response:", bookingsResponse.data);
        
        // Fetch all courts
        console.log("Fetching admin courts with token:", token);
        const courtsResponse = await axios.get("http://localhost:6543/admin/courts", {
          headers: { Authorization: `Bearer ${token}` },
          withCredentials: true // Tetap sertakan cookie untuk kompatibilitas
        });
        
        console.log("Courts response:", courtsResponse.data);
        
        // Format booking data
        const formattedBookings = bookingsResponse.data.data.map(booking => {
          const bookingDate = new Date(booking.time);
          return {
            id: booking.id,
            user: booking.full_name,
            date: bookingDate.toLocaleDateString('id-ID'),
            time: bookingDate.toLocaleTimeString('id-ID', { hour: '2-digit', minute: '2-digit' }),
            court: booking.court_name,
            status: booking.status,
            phone: booking.phone_number
          };
        });
        
        // Calculate statistics
        const now = new Date();
        const totalBookings = formattedBookings.length;
        const upcomingBookings = formattedBookings.filter(b => 
          new Date(b.date + " " + b.time) > now && b.status !== "cancelled"
        ).length;
        const completedBookings = formattedBookings.filter(b => 
          b.status === "confirmed" || (new Date(b.date + " " + b.time) < now && b.status !== "cancelled")
        ).length;
        
        setBookings(formattedBookings);
        setCourts(courtsResponse.data.data);
        setCategories(courtsResponse.data.categories || []);
        setStatuses(courtsResponse.data.statuses || []);
        setStats({
          totalBookings,
          upcomingBookings,
          completedBookings
        });
        setLoading(false);
      } catch (err) {
        console.error("Error fetching data:", err);
        console.log("Error response:", err.response ? err.response.data : "No response data");
        
        if (err.response && err.response.status === 403) {
          setError("Akses ditolak. Anda tidak memiliki izin admin yang valid.");
          // Clear invalid credentials
          localStorage.removeItem("authToken");
          localStorage.removeItem("userRole");
          setTimeout(() => navigate("/login"), 2000);
        } else {
          setError("Gagal memuat data. Silakan coba lagi.");
        }
        
        setLoading(false);
      }
    };
    
    fetchData();
  }, [navigate, selectedCategory, selectedStatus]);

  return (
    <div className="dashboard-container">
      <div className="dashboard-header">
        <h2 className="dashboard-title">Admin Dashboard</h2>
        <div className="user-info">
          <FaUserCircle className="text-4xl text-blue-600 cursor-pointer" />
          <span className="text-lg font-medium text-gray-700">{adminName}</span>
        </div>
      </div>
      
      {error && (
        <div className="error-message">
          {error}
        </div>
      )}

      <Stats loading={loading} stats={stats} />

      <div className="tab-navigation">
        <button
          className={`tab-button ${activeTab === 'bookings' ? 'active' : ''}`}
          onClick={() => setActiveTab('bookings')}
        >
          Booking Management
        </button>
        <button
          className={`tab-button ${activeTab === 'courts' ? 'active' : ''}`}
          onClick={() => setActiveTab('courts')}
        >
          Court Management
        </button>
      </div>
      
      {activeTab === 'bookings' && (
        <div className="content-card">
          <h3 className="text-2xl font-bold mb-4 text-gray-700">Recent Bookings</h3>
          <BookingTable
            bookings={bookings}
            loading={loading}
            onUpdateStatus={handleUpdateBookingStatus}
            editBookingId={editBookingId}
          />
        </div>
      )}
      
      {activeTab === 'courts' && (
        <div className="content-card">
          <div className="flex justify-between items-center mb-4">
            <h3 className="text-2xl font-bold text-gray-700">Court Management</h3>
            <button 
              onClick={() => setShowAddCourtForm(!showAddCourtForm)}
              className="button button-primary"
            >
              {showAddCourtForm ? (
                <>
                  <FaTimes className="mr-2" />
                  <span>Cancel</span>
                </>
              ) : (
                <>
                  <FaPlusCircle className="mr-2" />
                  <span>Add New Court</span>
                </>
              )}
            </button>
          </div>
          
          <FilterSection
            selectedCategory={selectedCategory}
            selectedStatus={selectedStatus}
            categories={categories}
            statuses={statuses}
            onCategoryChange={setSelectedCategory}
            onStatusChange={setSelectedStatus}
          />
          
          {showAddCourtForm && (
            <AddCourtForm
              newCourt={newCourt}
              onInputChange={handleCourtInputChange}
              onImageChange={handleImageChange}
              imagePreview={imagePreview}
              onSubmit={handleAddCourt}
              loading={addCourtLoading}
              error={addCourtError}
              success={addCourtSuccess}
            />
          )}
          
          <CourtTable
            courts={courts}
            onEdit={handleStartEditCourt}
            onDelete={handleConfirmDelete}
          />
        </div>
      )}
      
      {editCourtId && (
        <EditCourtModal
          editCourtData={editCourtData}
          onInputChange={handleEditCourtInputChange}
          onImageChange={handleEditImageChange}
          editImagePreview={editImagePreview}
          onSubmit={handleUpdateCourt}
          onCancel={handleCancelEdit}
          loading={editCourtLoading}
          error={editCourtError}
          success={editCourtSuccess}
        />
      )}
      
      {showDeleteConfirm && (
        <DeleteConfirmModal
          courtName={deleteCourtName}
          onConfirm={handleDeleteCourt}
          onCancel={handleCancelDelete}
          loading={deleteCourtLoading}
        />
      )}
    </div>
  );
}

export default Dashboard;
