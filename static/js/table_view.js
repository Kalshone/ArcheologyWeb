// ADD FORM
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

// ADD FORM SUBMISSION
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

// DROPDOWNS
function toggleDropdown(dropdown) {
    dropdown.classList.toggle('active');
}

function toggleChevron(trigger) {
    const chevron = trigger.querySelector('.fa-chevron-right, .fa-chevron-down');
    if (chevron) {
        chevron.classList.toggle('fa-chevron-right');
        chevron.classList.toggle('fa-chevron-down');
    }
}

function handleOutsideClick(event, dropdown, trigger) {
    if (dropdown.classList.contains('active') && 
        !trigger.contains(event.target) && 
        !dropdown.contains(event.target)) {
        dropdown.classList.remove('active');
        
        // Reset chevron if it's a sidebar dropdown
        const chevron = trigger.querySelector('.fa-chevron-down');
        if (chevron) {
            toggleChevron(trigger);
        }
    }
}

document.addEventListener('DOMContentLoaded', function() {
    // Sidebar dropdowns with chevrons
    const sidebarDropdowns = document.querySelectorAll('.sidebar .dropdown');
    
    sidebarDropdowns.forEach(dropdown => {
        const trigger = dropdown.querySelector('.dropdown-trigger');
        
        if (trigger) {
            trigger.addEventListener('click', function(e) {
                e.preventDefault();
                e.stopPropagation();
                
                // Close other sidebar dropdowns
                sidebarDropdowns.forEach(otherDropdown => {
                    if (otherDropdown !== dropdown && otherDropdown.classList.contains('active')) {
                        otherDropdown.classList.remove('active');
                        const otherTrigger = otherDropdown.querySelector('.dropdown-trigger');
                        if (otherTrigger.querySelector('.fa-chevron-down')) {
                            toggleChevron(otherTrigger);
                        }
                    }
                });
                
                toggleDropdown(dropdown);
                toggleChevron(this);
            });
            
            // Close dropdown when clicking outside
            document.addEventListener('click', (e) => {
                handleOutsideClick(e, dropdown, trigger);
            });
        }
    });

    // Column toggle dropdown (no chevrons)
    const columnToggleDropdown = document.querySelector('.column-toggle-dropdown');
    const columnToggleButton = document.getElementById('toggleButton');
    
    if (columnToggleButton && columnToggleDropdown) {
        columnToggleButton.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            toggleDropdown(columnToggleDropdown);
        });

        // Close column dropdown when clicking outside
        document.addEventListener('click', (e) => {
            handleOutsideClick(e, columnToggleDropdown, columnToggleButton);
        });
    }

    // Column visibility toggles
    const columnCheckboxes = document.querySelectorAll('.column-toggle-dropdown input[type="checkbox"]');
    
    // Load saved column visibility state
    const savedState = JSON.parse(localStorage.getItem('columnVisibility')) || {};
    const isAuthenticated = document.body.dataset.authenticated === 'true';
    
    columnCheckboxes.forEach(checkbox => {
        const columnIndex = parseInt(checkbox.dataset.column, 10) + (isAuthenticated ? 1 : 0); // Adjust for checkbox column
        
        // Set initial checkbox state from localStorage (default to checked/visible)
        checkbox.checked = savedState[columnIndex] !== false;
        
        // Apply initial visibility
        toggleColumnVisibility(columnIndex, checkbox.checked);
        
        // Add change event listener
        checkbox.addEventListener('change', function(e) {
            e.stopPropagation(); // Prevent dropdown from closing
            const columnIndex = parseInt(this.dataset.column, 10) + (isAuthenticated ? 1 : 0);
            toggleColumnVisibility(columnIndex, this.checked);
            
            // Save to localStorage
            savedState[columnIndex] = this.checked;
            localStorage.setItem('columnVisibility', JSON.stringify(savedState));
        });
    });
});

function toggleColumnVisibility(columnIndex, isVisible) {
    const table = document.getElementById('example');
    const rows = table.querySelectorAll('tr');
    
    rows.forEach(row => {
        const cells = row.querySelectorAll('th, td');
        if (cells[columnIndex]) {
            if (isVisible) {
                // Show column: First remove hidden-column, then after a small delay remove hiding-column
                cells[columnIndex].classList.remove('hidden-column');
                setTimeout(() => {
                    cells[columnIndex].classList.remove('hiding-column');
                }, 10);
            } else {
                // Hide column: First add hiding-column to start transition, then add hidden-column after transition completes
                cells[columnIndex].classList.add('hiding-column');
                setTimeout(() => {
                    cells[columnIndex].classList.add('hidden-column');
                }, 300);
            }
        }
    });
}



// function toggleChevronIcon(element) {
//     const chevron = element.querySelector('.fa-chevron-right, .fa-chevron-down');
//     if (chevron) {
//         if (chevron.classList.contains('fa-chevron-right')) {
//             chevron.classList.remove('fa-chevron-right');
//             chevron.classList.add('fa-chevron-down');
//         } else {
//             chevron.classList.remove('fa-chevron-down');
//             chevron.classList.add('fa-chevron-right');
//         }
//     }
// }

// function closeOtherSidebarDropdowns(dropdowns, dropdown) {
//     dropdowns.forEach(otherDropdown => {
//         if (otherDropdown !== dropdown && otherDropdown.classList.contains('active')) {
//             otherDropdown.classList.remove('active');
//             const otherTrigger = otherDropdown.querySelector('.dropdown-trigger');
//             if (otherTrigger) {
//                 toggleChevronIcon(otherTrigger);
//             }
//         }
//     });
// }

document.addEventListener('DOMContentLoaded', function() {
    // Sidebar dropdowns with chevrons
    // const sidebarDropdowns = document.querySelectorAll('.sidebar .dropdown');
    
    // sidebarDropdowns.forEach(dropdown => {
    //     const trigger = dropdown.querySelector('.dropdown-trigger');
        
    //     if (trigger) {
    //         trigger.addEventListener('click', function(e) {
    //             e.preventDefault();
                
    //             closeOtherSidebarDropdowns(sidebarDropdowns, dropdown);
    //             dropdown.classList.toggle('active');
    //             toggleChevronIcon(this);
    //         });
    //     }
    // });

    // Column toggle dropdown (separate implementation without chevrons)
    // const columnToggleButton = document.getElementById('toggleButton');
    // const columnDropdown = document.getElementById('columnList');
    
    // if (columnToggleButton && columnDropdown) {
    //     columnToggleButton.addEventListener('click', function(e) {
    //         e.preventDefault();
    //         e.stopPropagation();
    //         columnDropdown.classList.toggle('active');
    //     });

    //     // Close column dropdown when clicking outside
    //     document.addEventListener('click', function(e) {
    //         if (columnDropdown && 
    //             !columnToggleButton.contains(e.target) && 
    //             !columnDropdown.contains(e.target)) {
    //             columnDropdown.classList.remove('active');
    //         }
    //     });
    // }

    
});

// document.addEventListener('DOMContentLoaded', function() {
//     const button = document.getElementById('toggleButton');
//     const dropdown = document.getElementById('columnList');
//     const isAuthenticated = document.body.dataset.authenticated === 'true';
    
//     button.addEventListener('click', () => {
//         dropdown.classList.toggle('active');
//     });

//     // Load saved column visibility state
//     const savedState = JSON.parse(localStorage.getItem('columnVisibility')) || {};
//     const checkboxes = dropdown.querySelectorAll('input[type="checkbox"]');
//     checkboxes.forEach(checkbox => {
//         const column = parseInt(checkbox.dataset.column, 10) + (isAuthenticated ? 1 : 0); // Adjust for checkbox column if authenticated
//         const isVisible = savedState[column] !== false; // Default to true if not saved
//         checkbox.checked = isVisible;
//         toggleColumnVisibility(column, isVisible);
//     });

//     dropdown.addEventListener('change', (e) => {
//         if (e.target.matches('input[type="checkbox"]')) {
//             const column = parseInt(e.target.dataset.column, 10) + (isAuthenticated ? 1 : 0); // Adjust for checkbox column if authenticated
//             const isVisible = e.target.checked;
//             toggleColumnVisibility(column, isVisible);

//             // Save state to local storage
//             savedState[column] = isVisible;
//             localStorage.setItem('columnVisibility', JSON.stringify(savedState));
//         }
//     });


//     // Column checkboxes behavior
//     const columnCheckboxes = document.querySelectorAll('.column-toggle-dropdown input[type="checkbox"]');
//     columnCheckboxes.forEach(checkbox => {
//         checkbox.addEventListener('change', function(e) {
//             e.stopPropagation(); // Prevent dropdown from closing
//             const columnIndex = this.dataset.column;
//             const cells = document.querySelectorAll(`table tr > *:nth-child(${parseInt(columnIndex) + 2})`);
//             cells.forEach(cell => {
//                 cell.style.display = this.checked ? '' : 'none';
//             });
//         });
//     });
// });

// function toggleColumnVisibility(columnIndex, isVisible) {
//     const table = document.getElementById('example');
//     const rows = table.querySelectorAll('tr');

//     rows.forEach(row => {
//         const cells = row.querySelectorAll('th, td');
//         if (cells[columnIndex]) {
//             cells[columnIndex].style.display = isVisible ? '' : 'none';
//         }
//     });
// }




// CHECKBOXES
function toggleSelectAll(source) {
    const headerCheckbox = document.querySelector('thead #selectAll');
    const footerCheckbox = document.querySelector('tfoot #selectAll');
    const rowCheckboxes = document.querySelectorAll('.row-selector');
    
    const isChecked = source.checked;
    
    headerCheckbox.checked = isChecked;
    footerCheckbox.checked = isChecked;
    
    rowCheckboxes.forEach(checkbox => {
        checkbox.checked = isChecked;
        const row = checkbox.closest('tr');
        if (isChecked) {
            row.classList.add('selected');
        } else {
            row.classList.remove('selected');
        }
    });
    
    updateButtonStates();
}

function editSelected() {
    const selectedRows = document.querySelectorAll('.row-selector:checked');
    selectedRows.forEach(checkbox => {
        const row = checkbox.closest('tr');
        const cells = row.querySelectorAll('td');
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

function updateButtonStates() {
    const selectedRows = document.querySelectorAll('.row-selector:checked').length;
    const editButton = document.getElementById('editButton');
    const deleteButton = document.getElementById('deleteButton');
    const saveButton = document.getElementById('saveButton');
    
    editButton.disabled = selectedRows === 0;
    deleteButton.disabled = selectedRows === 0;

    document.querySelectorAll('.row-selector').forEach(checkbox => {
        const row = checkbox.closest('tr');
        if (checkbox.checked) {
            row.classList.add('selected');
        } else {
            row.classList.remove('selected');
        }
    });
}




