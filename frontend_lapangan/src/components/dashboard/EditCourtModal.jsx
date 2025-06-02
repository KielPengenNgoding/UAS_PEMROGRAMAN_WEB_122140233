import React from 'react';
import { FaSpinner, FaUpload, FaTimes } from 'react-icons/fa';

const EditCourtModal = ({
  editCourtData,
  onInputChange,
  onImageChange,
  editImagePreview,
  onSubmit,
  onCancel,
  loading,
  error,
  success
}) => {
  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div className="bg-white rounded-xl shadow-xl w-full max-w-2xl max-h-[90vh] overflow-y-auto">
        <div className="p-6">
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-xl font-semibold text-gray-800">Edit Lapangan</h3>
            <button
              onClick={onCancel}
              className="text-gray-400 hover:text-gray-600 transition-colors"
            >
              <FaTimes className="h-5 w-5" />
            </button>
          </div>
          
          {error && (
            <div className="bg-red-50 text-red-700 p-4 rounded-md mb-6">
              <p className="text-sm">{error}</p>
            </div>
          )}
          
          {success && (
            <div className="bg-green-50 text-green-700 p-4 rounded-md mb-6">
              <p className="text-sm">{success}</p>
            </div>
          )}
          
          <form onSubmit={onSubmit} className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2" htmlFor="court_name">
                Nama Lapangan
              </label>
              <input
                type="text"
                id="court_name"
                name="court_name"
                value={editCourtData.court_name}
                onChange={onInputChange}
                className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                required
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2" htmlFor="court_category">
                Kategori
              </label>
              <select
                id="court_category"
                name="court_category"
                value={editCourtData.court_category}
                onChange={onInputChange}
                className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                required
              >
                <option value="">Pilih Kategori</option>
                <option value="Futsal">Futsal</option>
                <option value="Basket">Basket</option>
                <option value="Badminton">Badminton</option>
                <option value="Tennis">Tennis</option>
                <option value="Volleyball">Volleyball</option>
              </select>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2" htmlFor="description">
                Deskripsi
              </label>
              <textarea
                id="description"
                name="description"
                value={editCourtData.description}
                onChange={onInputChange}
                className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                rows="3"
                placeholder="Masukkan deskripsi lapangan"
              ></textarea>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2" htmlFor="status">
                Status
              </label>
              <select
                id="status"
                name="status"
                value={editCourtData.status}
                onChange={onInputChange}
                className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              >
                <option value="available">Tersedia</option>
                <option value="maintenance">Dalam Perbaikan</option>
                <option value="booked">Sudah Dipesan</option>
              </select>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2" htmlFor="image">
                Gambar Lapangan
              </label>
              <div className="bg-gray-50 p-4 rounded-lg border-2 border-dashed border-gray-300 mb-4">
                <div className="space-y-2">
                  <h4 className="text-sm font-medium text-gray-700">Panduan upload gambar:</h4>
                  <ul className="text-sm text-gray-600 list-disc ml-4 space-y-1">
                    <li>Format yang didukung: JPG, JPEG, PNG, GIF</li>
                    <li>Ukuran maksimal: 5MB</li>
                    <li>Resolusi yang disarankan: minimal 600x400 pixel</li>
                    <li>Gambar akan disimpan di folder uploads/courts</li>
                  </ul>
                </div>
                
                <div className="mt-4">
                  <label className="flex justify-center px-6 py-4 cursor-pointer hover:bg-gray-100 rounded-lg transition-colors">
                    <input
                      type="file"
                      id="image"
                      name="image"
                      accept="image/jpeg,image/jpg,image/png,image/gif"
                      onChange={onImageChange}
                      className="hidden"
                    />
                    <div className="text-center">
                      <FaUpload className="mx-auto h-8 w-8 text-gray-400 mb-2" />
                      <p className="text-sm text-gray-600">
                        Klik untuk memilih file atau drag & drop
                      </p>
                      <p className="text-xs text-gray-500 mt-1">
                        JPG, JPEG, PNG, GIF (Max. 5MB)
                      </p>
                    </div>
                  </label>
                </div>
              </div>
              
              {editImagePreview && (
                <div className="mt-4">
                  <p className="text-sm font-medium text-gray-700 mb-2">Preview:</p>
                  <div className="relative rounded-lg overflow-hidden bg-gray-100">
                    <img 
                      src={editImagePreview} 
                      alt="Preview" 
                      className="w-full h-48 object-cover"
                    />
                    <div className="absolute inset-0 bg-black bg-opacity-40 flex items-center justify-center opacity-0 hover:opacity-100 transition-opacity">
                      <p className="text-white text-sm">Klik untuk mengganti gambar</p>
                    </div>
                  </div>
                </div>
              )}
            </div>
            
            <div className="flex justify-end space-x-3 pt-4">
              <button
                type="button"
                onClick={onCancel}
                className="px-6 py-3 bg-gray-100 text-gray-700 font-medium rounded-md hover:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                disabled={loading}
              >
                Batal
              </button>
              <button
                type="submit"
                className="inline-flex items-center px-6 py-3 bg-blue-600 text-white font-medium rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                disabled={loading}
              >
                {loading ? (
                  <>
                    <FaSpinner className="animate-spin -ml-1 mr-2 h-5 w-5" />
                    Menyimpan...
                  </>
                ) : (
                  'Simpan Perubahan'
                )}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default EditCourtModal; 