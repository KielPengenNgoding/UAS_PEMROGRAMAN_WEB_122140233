import React from 'react';

const FilterSection = ({ 
  selectedCategory, 
  selectedStatus, 
  categories, 
  statuses, 
  onCategoryChange, 
  onStatusChange 
}) => {
  return (
    <div className="filter-section">
      <div>
        <label className="form-label">
          Filter by Category
        </label>
        <select
          value={selectedCategory}
          onChange={(e) => onCategoryChange(e.target.value)}
          className="form-select"
        >
          <option value="">All Categories</option>
          {categories.map((category) => (
            <option key={category} value={category}>
              {category}
            </option>
          ))}
        </select>
      </div>
      <div>
        <label className="form-label">
          Filter by Status
        </label>
        <select
          value={selectedStatus}
          onChange={(e) => onStatusChange(e.target.value)}
          className="form-select"
        >
          <option value="">All Statuses</option>
          {statuses.map((status) => (
            <option key={status} value={status}>
              {status.charAt(0).toUpperCase() + status.slice(1)}
            </option>
          ))}
        </select>
      </div>
    </div>
  );
};

export default FilterSection; 