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

// SEARCHBAR
function searchTable() {
    const input = document.getElementById('searchInput');
    const filter = input.value.toLowerCase();
    const table = document.getElementById('example');
    const rows = table.getElementsByTagName('tr');
  
    // Loop through all table rows (skip header row)
    for (let i = 1; i < rows.length; i++) {
      let row = rows[i];
      let shouldShow = false;
      
      // Skip header/footer rows
      if (row.parentNode.tagName === 'THEAD' || row.parentNode.tagName === 'TFOOT') {
        continue;
      }
      
      // Check all cells in the row
      const cells = row.getElementsByTagName('td');
      for (let j = 0; j < cells.length; j++) {
        const cell = cells[j];
        if (cell) {
          const textValue = cell.textContent || cell.innerText;
          if (textValue.toLowerCase().indexOf(filter) > -1) {
            shouldShow = true;
            break;
          }
        }
      }
      
      // Show/hide the row based on search match
      row.style.display = shouldShow ? '' : 'none';
    }
  }

document.addEventListener('DOMContentLoaded', function() {
    // Create tooltip element
    const tooltip = document.createElement('div');
    tooltip.className = 'tooltip';
    tooltip.style.display = 'none';
    document.body.appendChild(tooltip);
    
    // Add event listeners to table cells
    const tableCells = document.querySelectorAll('.table tbody td');
    
    tableCells.forEach(cell => {
        // Show tooltip on mouseenter
        cell.addEventListener('mouseenter', function(e) {
            const fullText = this.dataset.fullText;
            if (fullText && fullText !== this.textContent) {
                tooltip.textContent = fullText;
                tooltip.style.display = 'block';
                tooltip.style.left = (e.pageX + 10) + 'px';
                tooltip.style.top = (e.pageY + 10) + 'px';
            }
        });
        
        // Update tooltip position on mousemove
        cell.addEventListener('mousemove', function(e) {
            tooltip.style.left = (e.pageX + 10) + 'px';
            tooltip.style.top = (e.pageY + 10) + 'px';
        });
        
        // Hide tooltip on mouseleave
        cell.addEventListener('mouseleave', function() {
            tooltip.style.display = 'none';
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
    if (selectedRows.length === 0) return;
    
    selectedRows.forEach(checkbox => {
        const row = checkbox.closest('tr');
        const cells = row.querySelectorAll('td:not(:first-child)'); // Skip checkbox cell
        
        cells.forEach((cell, index) => {
            const value = cell.textContent.trim();
            cell.dataset.originalValue = value;
            cell.innerHTML = `<input type="text" value="${value}" class="edit-field">`;
        });
    });
    
    // Toggle button visibility
    document.getElementById('editButton').style.display = 'none';
    document.getElementById('deleteButton').style.display = 'none';
    document.getElementById('saveButton').style.display = 'inline';
    document.getElementById('cancelButton').style.display = 'inline';
}

function saveSelected() {
    const selectedRows = document.querySelectorAll('.row-selector:checked');
    if (selectedRows.length === 0) return;
    
    let successCount = 0;
    let failCount = 0;
    const totalRows = selectedRows.length;
    
    selectedRows.forEach(checkbox => {
        const row = checkbox.closest('tr');
        // Important: Convert model name to match the URL pattern (capitalized)
        const modelName = row.dataset.modelName;
        const objectId = row.dataset.objectId;
        const data = {};
        
        // Get header cells for field names
        const headers = document.querySelectorAll('thead th:not(:first-child)');
        
        cells = row.querySelectorAll('td:not(:first-child)');
        cells.forEach((cell, index) => {
            const input = cell.querySelector('input.edit-field');
            if (input) {
                const fieldName = headers[index].querySelector('span').textContent.trim();
                data['field' + fieldName] = input.value;
            }
        });

        if (Object.keys(data).length > 0) {
            fetch(`/update_object/${modelName}/${objectId}/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                },
                body: JSON.stringify(data)
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`Failed to update ${modelName} ${objectId}: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                successCount++;
                checkCompletion();
            })
            .catch(error => {
                console.error('Error:', error);
                failCount++;
                alert(`Error updating record: ${error.message}`);
                checkCompletion();
            });
        }
    });
    
    function checkCompletion() {
        if (successCount + failCount === totalRows) {
            if (failCount === 0) {
                alert('All records updated successfully!');
                window.location.reload(); // Only reload if all updates succeeded
            } else {
                alert(`${successCount} records updated, ${failCount} failed. Check console for details.`);
            }
        }
    }
}

function cancelEdit() {
    const selectedRows = document.querySelectorAll('.row-selector:checked');
    if (selectedRows.length === 0) return;
    
    selectedRows.forEach(checkbox => {
        const row = checkbox.closest('tr');
        const cells = row.querySelectorAll('td:not(:first-child)'); // Skip checkbox cell
        
        cells.forEach(cell => {
            if (cell.dataset.originalValue) {
                cell.innerHTML = cell.dataset.originalValue;
                delete cell.dataset.originalValue;
            }
        });
    });
    
    // Reset button visibility
    document.getElementById('editButton').style.display = 'inline';
    document.getElementById('deleteButton').style.display = 'inline';
    document.getElementById('saveButton').style.display = 'none';
    document.getElementById('cancelButton').style.display = 'none';
}

function deleteSelected() {
    const selectedRows = document.querySelectorAll('.row-selector:checked');
    if (selectedRows.length === 0) return;
    
    if (confirm(`Are you sure you want to delete ${selectedRows.length} selected item(s)?`)) {
        let deletedCount = 0;
        
        Array.from(selectedRows).forEach(checkbox => {
            const row = checkbox.closest('tr');
            const modelName = row.dataset.modelName.toLowerCase();
            const objectId = row.dataset.objectId;
            
            fetch(`/delete_object/${modelName}/${objectId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                }
            })
            .then(response => {
                if (response.ok) {
                    deletedCount++;
                    // If all selected items have been processed, reload the page
                    if (deletedCount === selectedRows.length) {
                        window.location.reload();
                    }
                } else {
                    console.error(`Failed to delete: ${modelName} ${objectId}`);
                }
            });
        });
    }
}

function updateButtonStates() {
    const selectedRows = document.querySelectorAll('.row-selector:checked').length;
    const editButton = document.getElementById('editButton');
    const deleteButton = document.getElementById('deleteButton');
    const saveButton = document.getElementById('saveButton');
    const cancelButton = document.getElementById('cancelButton');
    
    // editButton.disabled = selectedRows === 0;
    // deleteButton.disabled = selectedRows === 0;

    document.querySelectorAll('.row-selector').forEach(checkbox => {
        const row = checkbox.closest('tr');
        if (checkbox.checked) {
            row.classList.add('selected');
        } else {
            row.classList.remove('selected');
        }
    });
}




