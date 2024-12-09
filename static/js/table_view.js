function openAddForm() {
    const formContainer = document.getElementById('addFormContainer');
    if (formContainer.style.display !== 'block') {
        formContainer.style.display = 'block';
    } else {
        closeAddForm();
    }
}

function closeAddForm() {
    const formContainer = document.getElementById('addFormContainer');
    formContainer.style.display = 'none';
}


document.addEventListener('DOMContentLoaded', function() {
    const dropdowns = document.querySelectorAll('.dropdown');
    
    dropdowns.forEach(dropdown => {
      const trigger = dropdown.querySelector('.dropdown-trigger');
      
      trigger.addEventListener('click', function(e) {
        e.preventDefault();
        
        // Toggle active class on dropdown
        dropdown.classList.toggle('active');
        
        // Find and toggle chevron icon
        const chevron = this.querySelector('.fa-chevron-right, .fa-chevron-down');
        if (chevron.classList.contains('fa-chevron-right')) {
          chevron.classList.remove('fa-chevron-right');
          chevron.classList.add('fa-chevron-down');
        } else {
          chevron.classList.remove('fa-chevron-down');
          chevron.classList.add('fa-chevron-right');
        }
      });
    });
  });

function updateButtonStates() {
    const selectedRows = document.querySelectorAll('.row-selector:checked').length;
    const editButton = document.getElementById('editButton');
    const deleteButton = document.getElementById('deleteButton');
    const saveButton = document.getElementById('saveButton');
    
    editButton.disabled = selectedRows === 0;
    deleteButton.disabled = selectedRows === 0;
}

function toggleSelectAll() {
    const selectAll = document.getElementById('selectAll');
    const checkboxes = document.querySelectorAll('.row-selector');
    checkboxes.forEach(checkbox => checkbox.checked = selectAll.checked);
    updateButtonStates();
}

function editSelected() {
    const selectedRows = document.querySelectorAll('.row-selector:checked');
    selectedRows.forEach(checkbox => {
        const row = checkbox.closest('tr');
        const cells = row.querySelectorAll('td');
        // Convert cells to input fields
        cells.forEach(cell => {
            if (!cell.querySelector('input')) {
                const value = cell.textContent;
                cell.dataset.originalValue = value;
                cell.innerHTML = `<input type="text" value="${value}">`;
            }
        });
    });
    
    document.getElementById('editButton').style.display = 'none';
    document.getElementById('deleteButton').style.display = 'none';
    document.getElementById('saveButton').style.display = 'inline';
}

function saveChanges() {
    const selectedRows = document.querySelectorAll('.row-selector:checked');
    const updates = [];
    
    selectedRows.forEach(checkbox => {
        const row = checkbox.closest('tr');
        const inputs = row.querySelectorAll('input[type="text"]');
        const data = {};
        
        inputs.forEach(input => {
            const fieldName = input.closest('td').dataset.field;
            data[fieldName] = input.value;
        });
        
        updates.push({
            modelName: row.dataset.modelName,
            objectId: row.dataset.objectId,
            data: data
        });
    });

    Promise.all(updates.map(update => 
        fetch(`/update_object/${update.modelName}/${update.objectId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
            },
            body: JSON.stringify(update.data),
        })
    ))
    .then(responses => {
        if (responses.every(r => r.ok)) {
            alert('Changes saved successfully.');
            window.location.reload();
        } else {
            alert('Failed to save some changes.');
        }
    });
}

function deleteSelected() {
    const selectedRows = document.querySelectorAll('.row-selector:checked');
    if (selectedRows.length === 0) return;
    
    if (confirm(`Are you sure you want to delete ${selectedRows.length} selected items?`)) {
        const deletions = Array.from(selectedRows).map(checkbox => {
            const row = checkbox.closest('tr');
            return fetch(`/delete/${row.dataset.modelName}/${row.dataset.objectId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                }
            });
        });

        Promise.all(deletions)
            .then(responses => {
                if (responses.every(r => r.ok)) {
                    alert('Selected items deleted successfully.');
                    window.location.reload();
                } else {
                    alert('Failed to delete some items.');
                }
            });
    }
}

function toggleColumn(event) {
    const headerCell = event.currentTarget.closest('th');
    const table = headerCell.closest('table');
    const columnIndex = Array.from(headerCell.parentElement.children).indexOf(headerCell);
    const icon = headerCell.querySelector('.column-toggle');
    
    // Toggle icon
    icon.classList.toggle('fa-chevron-down');
    icon.classList.toggle('fa-chevron-right');
    
    // Toggle header
    headerCell.classList.toggle('hidden-column');
    
    // Toggle data cells
    const rows = table.querySelectorAll('tbody tr');
    rows.forEach(row => {
        if (row.cells[columnIndex]) {
            row.cells[columnIndex].classList.toggle('hidden-column');
        }
    });
}

document.addEventListener('DOMContentLoaded', function() {
    const headers = document.querySelectorAll('.header-content');
    headers.forEach(header => {
        header.addEventListener('click', toggleColumn);
    });
});

// Add event listeners when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('addForm').addEventListener('submit', function(e) {
        e.preventDefault();
        const formData = new FormData(this);
        
        fetch('', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Record added successfully!');
                window.location.reload();
            } else {
                alert(data.error || 'Error adding record');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Failed to add record');
        });
    });
});