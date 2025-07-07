// Initialize data
let projectsData = {
    software: {
        count: 15,
        progress: 80,
        status: 'excellent',
        budget: 60000,
        spent: 42000
    },
    research: {
        count: 8,
        progress: 50,
        status: 'normal',
        budget: 40000,
        spent: 22500
    },
    books: {
        count: 5,
        progress: 70,
        status: 'normal',
        budget: 25000,
        spent: 14000
    }
};

let activities = [
    {
        type: 'success',
        icon: 'check-circle-fill',
        message: 'Software Project "Dashboard UI" completed',
        time: '2 hours ago'
    },
    {
        type: 'warning',
        icon: 'exclamation-triangle-fill',
        message: 'Research Project delayed - awaiting data',
        time: '1 day ago'
    },
    {
        type: 'primary',
        icon: 'currency-dollar',
        message: 'New budget approved for Q3',
        time: '2 days ago'
    },
    {
        type: 'info',
        icon: 'book-fill',
        message: 'New book chapter submitted for review',
        time: '3 days ago'
    }
];

// DOM elements
document.addEventListener('DOMContentLoaded', function () {
    const currentDateEl = document.getElementById('current-date');
    const exportBtn = document.getElementById('export-btn');
    const saveProjectBtn = document.getElementById('saveProjectBtn');
    const saveBudgetBtn = document.getElementById('saveBudgetBtn');
    const activityList = document.getElementById('activity-list');
    const successToast = new bootstrap.Toast(document.getElementById('successToast'));

    // Set current date
    if (currentDateEl) {
        const today = new Date();
        const options = { year: 'numeric', month: 'long', day: 'numeric' };
        currentDateEl.textContent = today.toLocaleDateString('en-ZA', options);
    }

    updateDashboard();
    renderActivities();

    const softwareCard = document.getElementById('software-card');
    const researchCard = document.getElementById('research-card');
    const booksCard = document.getElementById('books-card');

    if (softwareCard) softwareCard.addEventListener('click', () => showProjectDetails('software'));
    if (researchCard) researchCard.addEventListener('click', () => showProjectDetails('research'));
    if (booksCard) booksCard.addEventListener('click', () => showProjectDetails('books'));

    if (exportBtn) exportBtn.addEventListener('click', exportReport);
    if (saveProjectBtn) saveProjectBtn.addEventListener('click', saveProject);
    if (saveBudgetBtn) saveBudgetBtn.addEventListener('click', saveBudget);

    // Handle finance period toggle buttons
    document.querySelectorAll('[data-period]').forEach(btn => {
        btn.addEventListener('click', function () {
            document.querySelectorAll('[data-period]').forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            showToast(`Switched to ${this.textContent} view`);
        });
    });

    function updateDashboard() {
        // Update metric cards
        if (document.getElementById('software-percent')) {
            document.getElementById('software-percent').textContent = `${projectsData.software.progress}%`;
            document.getElementById('software-progress').style.width = `${projectsData.software.progress}%`;
            document.getElementById('software-status').textContent = projectsData.software.status === 'excellent' ? 'Excellent' : 'Normal';
            document.getElementById('software-count').textContent = projectsData.software.count;
        }

        if (document.getElementById('research-percent')) {
            document.getElementById('research-percent').textContent = `${projectsData.research.progress}%`;
            document.getElementById('research-progress').style.width = `${projectsData.research.progress}%`;
            document.getElementById('research-status').textContent = projectsData.research.status === 'excellent' ? 'Excellent' : 'Normal';
            document.getElementById('research-count').textContent = projectsData.research.count;
        }

        if (document.getElementById('books-percent')) {
            document.getElementById('books-percent').textContent = `${projectsData.books.progress}%`;
            document.getElementById('books-progress').style.width = `${projectsData.books.progress}%`;
            document.getElementById('books-status').textContent = projectsData.books.status === 'excellent' ? 'Excellent' : 'Normal';
            document.getElementById('books-count').textContent = projectsData.books.count;
        }

        // Update finance overview
        const totalBudget = projectsData.software.budget + projectsData.research.budget + projectsData.books.budget;
        const totalSpent = projectsData.software.spent + projectsData.research.spent + projectsData.books.spent;
        const remaining = totalBudget - totalSpent;

        if (document.getElementById('total-budget')) document.getElementById('total-budget').textContent = `R ${totalBudget.toLocaleString()}`;
        if (document.getElementById('total-expenses')) document.getElementById('total-expenses').textContent = `R ${totalSpent.toLocaleString()}`;
        if (document.getElementById('remaining-budget')) document.getElementById('remaining-budget').textContent = `R ${remaining.toLocaleString()}`;

        updateBudgetRow('software');
        updateBudgetRow('research');
        updateBudgetRow('books');
    }

    function updateBudgetRow(type) {
        const row = document.querySelector(`#budget-table tr[data-type="${type}"]`);
        if (!row) return;
        const data = projectsData[type];
        const remaining = data.budget - data.spent;
        const percentSpent = Math.round((data.spent / data.budget) * 100);

        row.querySelector('.allocated').textContent = `R ${data.budget.toLocaleString()}`;
        row.querySelector('.spent').textContent = `R ${data.spent.toLocaleString()}`;
        row.querySelector('.remaining').textContent = `R ${remaining.toLocaleString()}`;
        row.querySelector('.progress-bar').style.width = `${percentSpent}%`;
    }

    function renderActivities() {
        if (!activityList) return;
        activityList.innerHTML = '';
        activities.forEach(activity => {
            const li = document.createElement('li');
            li.innerHTML = `
                <div class="d-flex">
                    <div class="flex-shrink-0 me-3">
                        <i class="bi bi-${activity.icon} text-${activity.type}"></i>
                    </div>
                    <div>
                        <p class="mb-0">${activity.message}</p>
                        <small class="text-muted">${activity.time}</small>
                    </div>
                </div>
            `;
            activityList.appendChild(li);
        });
    }

    function showProjectDetails(type) {
        showToast(`Showing details for ${type} projects`);
    }

    function exportReport() {
        showToast('Report exported successfully!');
    }

    function saveProject() {
        const form = document.getElementById('projectForm');
        const errorElement = document.getElementById('formError');

        if (!form.checkValidity()) {
            errorElement.textContent = 'Please fill in all required fields';
            errorElement.classList.remove('d-none');
            return;
        }

        const projectType = document.getElementById('projectType').value;
        const progress = parseInt(document.getElementById('projectProgress').value);
        const budget = parseInt(document.getElementById('projectBudget').value) || 0;

        projectsData[projectType].count++;
        projectsData[projectType].progress = Math.round(
            (projectsData[projectType].progress * (projectsData[projectType].count - 1) + progress) /
            projectsData[projectType].count
        );

        projectsData[projectType].status = projectsData[projectType].progress >= 75 ? 'excellent' : 'normal';
        if (budget > 0) {
            projectsData[projectType].budget += budget;
        }

        const projectName = document.getElementById('projectName').value || 'New Project';
        activities.unshift({
            type: 'success',
            icon: 'plus-circle',
            message: `Added new project: ${projectName}`,
            time: 'Just now'
        });

        updateDashboard();
        renderActivities();

        bootstrap.Modal.getInstance(document.getElementById('addProjectModal')).hide();
        form.reset();
        errorElement.classList.add('d-none');

        showToast('Project added successfully!');
    }

    function saveBudget() {
        const softwareBudget = parseInt(document.getElementById('softwareBudget').value);
        const researchBudget = parseInt(document.getElementById('researchBudget').value);
        const booksBudget = parseInt(document.getElementById('booksBudget').value);

        if (
            !Number.isFinite(softwareBudget) || !Number.isFinite(researchBudget) || !Number.isFinite(booksBudget) ||
            softwareBudget < 0 || researchBudget < 0 || booksBudget < 0
        ) {
            document.getElementById('budgetError').textContent = 'Please enter valid budget amounts';
            document.getElementById('budgetError').classList.remove('d-none');
            return;
        }

        projectsData.software.budget = softwareBudget;
        projectsData.research.budget = researchBudget;
        projectsData.books.budget = booksBudget;

        updateDashboard();

        bootstrap.Modal.getInstance(document.getElementById('editBudgetModal')).hide();
        document.getElementById('budgetError').classList.add('d-none');

        activities.unshift({
            type: 'primary',
            icon: 'currency-dollar',
            message: 'Budget allocations updated',
            time: 'Just now'
        });

        renderActivities();
        showToast('Budget updated successfully!');
    }

    function showToast(message) {
        const toastBody = document.querySelector('.toast-body');
        if (toastBody) {
            toastBody.textContent = message;
            successToast.show();
        }
    }
      
});
