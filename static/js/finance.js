document.addEventListener('DOMContentLoaded', function () {
    const costCentreDropdown = document.getElementById("costCentreDropdown");
    const addCostCentreForm = document.getElementById("addCostCentreForm");
    const expenditureTable = document.querySelector("#expenditureTable tbody");

    // ✅ Corrected AJAX Form Submission for Cost Centre
    addCostCentreForm.addEventListener('submit', function (e) {
        e.preventDefault();

        const formData = new FormData(addCostCentreForm);
        const formActionUrl = addCostCentreForm.dataset.url;

        fetch(formActionUrl, {
            method: 'POST',
            headers: {
                'X-CSRFToken': '{{ csrf_token }}'
            },
            body: formData
        })
        .then(response => {
            if (response.ok) {
                const modal = bootstrap.Modal.getInstance(document.getElementById('addCostCentreModal'));
                modal.hide();
                location.reload();
            } else {
                alert('Failed to add cost centre.');
            }
        })
        .catch(error => {
            console.error('Error adding cost centre:', error);
        });
    });

    // ✅ Fetch expenditures for selected cost centre
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

    // ✅ Expenditure Table Loader
    function populateExpenditureTable(expenditures) {
        expenditureTable.innerHTML = "";
        if (expenditures.length === 0) {
            expenditureTable.innerHTML = `<tr><td colspan="13" class="text-center">No expenditures recorded.</td></tr>`;
            return;
        }

        expenditures.forEach(record => {
            const categories = {
                Salary: '', Bursaries: '', Invoices: '', Fitness: '', Equipment: '', Travel: ''
            };
            categories[record.category] = `R ${parseFloat(record.amount).toLocaleString()}`;

            expenditureTable.innerHTML += `
                <tr>
                    <td>${record.month}</td>
                    <td>${record.name}</td>
                    <td>${categories['Salary']}</td>
                    <td>${categories['Bursaries']}</td>
                    <td>${categories['Invoices']}</td>
                    <td>${categories['Fitness']}</td>
                    <td>${categories['Equipment']}</td>
                    <td>${categories['Travel']}</td>
                    <td>R ${parseFloat(record.amount).toLocaleString()}</td>
                    <td>R ${parseFloat(record.opening_balance).toLocaleString()}</td>
                    <td>R ${parseFloat(record.closing_balance).toLocaleString()}</td>
                    <td>R ${parseFloat(record.oracle_balance).toLocaleString()}</td>
                    <td>R ${parseFloat(record.closing_balance).toLocaleString()}</td>
                </tr>
            `;
        });
    }
});
