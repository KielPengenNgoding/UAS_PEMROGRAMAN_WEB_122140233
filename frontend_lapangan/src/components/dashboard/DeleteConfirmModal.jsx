import React from 'react';
import { FaSpinner } from 'react-icons/fa';

const DeleteConfirmModal = ({
  courtName,
  onConfirm,
  onCancel,
  loading
}) => {
  return (
    <div className="modal-overlay">
      <div className="modal-content">
        <h3 className="modal-title">Konfirmasi Hapus</h3>
        <p className="mb-6">
          Apakah Anda yakin ingin menghapus lapangan <strong>{courtName}</strong>? 
          Tindakan ini tidak dapat dibatalkan.
        </p>
        
        <div className="flex justify-end">
          <button
            onClick={onCancel}
            className="button mr-2"
            disabled={loading}
          >
            Batal
          </button>
          <button
            onClick={onConfirm}
            className="button button-danger"
            disabled={loading}
          >
            {loading ? (
              <>
                <FaSpinner className="animate-spin mr-2" />
                Menghapus...
              </>
            ) : (
              'Hapus Lapangan'
            )}
          </button>
        </div>
      </div>
    </div>
  );
};

export default DeleteConfirmModal; 