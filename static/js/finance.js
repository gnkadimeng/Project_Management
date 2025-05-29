document.addEventListener('DOMContentLoaded', function () {
    const costCentresTable = document.querySelector("#costCentresTable tbody");
    const costCentreDropdown = document.getElementById("costCentreDropdown");
    const addCostCentreForm = document.getElementById("addCostCentreForm");
    const expenditureTable = document.querySelector("#expenditureTable tbody");

    // AJAX Form Submission
    addCostCentreForm.addEventListener('submit', function (e) {
        e.preventDefault();
        const formData = new FormData(addCostCentreForm);

        fetch("{% url 'add_cost_centre' %}", {
            method: 'POST',
            headers: {
                'X-CSRFToken': '{{ csrf_token }}'
            },
            body: formData
        })
        .then(response => {
            if (response.ok) {
                // Hide Modal
                const modal = bootstrap.Modal.getInstance(document.getElementById('addCostCentreModal'));
                modal.hide();
                // Reload page to show new Cost Centre
                location.reload();
            } else {
                alert('Failed to add cost centre.');
            }
        })
        .catch(error => {
            console.error('Error adding cost centre:', error);
        });
    });

    // Existing Dropdown and Fetching Code (unchanged)
    if (costCentreDropdown) {
        costCentreDropdown.addEventListener("change", function () {
            const selectedId = this.value;
            if (selectedId) {
                fetch(`/finance/expenditures/${selectedId}/`)
                    .then(response => response.json())
                    .then(data => {
                        populateExpenditureTable(data.expenditures);
                    });
            }
        });
    }

    function populateExpenditureTable(expenditures) {
        expenditureTable.innerHTML = "";
        if (expenditures.length === 0) {
            expenditureTable.innerHTML = `<tr><td colspan="13" class="text-center">No expenditures recorded.</td></tr>`;
            return;
        }
        expenditures.forEach(record => {
            const totalExpenses = record.amount;
            expenditureTable.innerHTML += `
                <tr>
                    <td>${record.month}</td>
                    <td>${record.name}</td>
                    <td>${record.category}</td>
                    <td>R ${parseFloat(record.amount).toLocaleString()}</td>
                    <td>R ${parseFloat(record.opening_balance).toLocaleString()}</td>
                    <td>R ${parseFloat(record.closing_balance).toLocaleString()}</td>
                    <td>R ${parseFloat(record.oracle_balance).toLocaleString()}</td>
                </tr>
            `;
        });
    }

});
