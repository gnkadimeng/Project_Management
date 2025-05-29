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
const currentDateEl = document.getElementById('current-date');
const exportBtn = document.getElementById('export-btn');
const projectForm = document.getElementById('projectForm');
const saveProjectBtn = document.getElementById('saveProjectBtn');
const budgetForm = document.getElementById('budgetForm');
const saveBudgetBtn = document.getElementById('saveBudgetBtn');
const successToast = new bootstrap.Toast(document.getElementById('successToast'));
const activityList = document.getElementById('activity-list');

// Initialize the dashboard
document.addEventListener('DOMContentLoaded', function() {
    // Set current date
    const today = new Date();
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    currentDateEl.textContent = today.toLocaleDateString('en-US', options);
    
    // Update dashboard with initial data
    updateDashboard();
    renderActivities();

    // Card click events
    document.getElementById('software-card').addEventListener('click', () => showProjectDetails('software'));
    document.getElementById('research-card').addEventListener('click', () => showProjectDetails('research'));
    document.getElementById('books-card').addEventListener('click', () => showProjectDetails('books'));

    // Export button
    exportBtn.addEventListener('click', exportReport);

    // Save project button
    saveProjectBtn.addEventListener('click', saveProject);

    // Save budget button
    saveBudgetBtn.addEventListener('click', saveBudget);

    // Period buttons
    document.querySelectorAll('[data-period]').forEach(btn => {
        btn.addEventListener('click', function() {
            document.querySelectorAll('[data-period]').forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            // In a real app, you would fetch data for the selected period
            showToast(`Switched to {this.textContent} view`);
        });
    });
});

// Update dashboard with current data
function updateDashboard() {
    // Update software projects
    document.getElementById('software-percent').textContent = `{projectsData.software.progress}%`;
    document.getElementById('software-progress').style.width = `{projectsData.software.progress}%`;
    document.getElementById('software-status').textContent = projectsData.software.status === 'excellent' ? 'Excellent' : 'Normal';
    document.getElementById('software-count').textContent = projectsData.software.count;
    
    // Update research projects
    document.getElementById('research-percent').textContent = `{projectsData.research.progress}%`;
    document.getElementById('research-progress').style.width = `{projectsData.research.progress}%`;
    document.getElementById('research-status').textContent = projectsData.research.status === 'excellent' ? 'Excellent' : 'Normal';
    document.getElementById('research-count').textContent = projectsData.research.count;
    
    // Update books
    document.getElementById('books-percent').textContent = `{projectsData.books.progress}%`;
    document.getElementById('books-progress').style.width = `{projectsData.books.progress}%`;
    document.getElementById('books-status').textContent = projectsData.books.status === 'excellent' ? 'Excellent' : 'Normal';
    document.getElementById('books-count').textContent = projectsData.books.count;
    
    // Update finance data
    const totalBudget = projectsData.software.budget + projectsData.research.budget + projectsData.books.budget;
    const totalSpent = projectsData.software.spent + projectsData.research.spent + projectsData.books.spent;
    const remaining = totalBudget - totalSpent;
    
    document.getElementById('total-budget').textContent = `{totalBudget.toLocaleString()}`;
    document.getElementById('total-expenses').textContent = `{totalSpent.toLocaleString()}`;
    document.getElementById('remaining-budget').textContent = `{remaining.toLocaleString()}`;
    
    // Update budget table
    updateBudgetRow('software');
    updateBudgetRow('research');
    updateBudgetRow('books');
}

function updateBudgetRow(type) {
    const row = document.querySelector(`#budget-table tr[data-type="{type}"]`);
    const data = projectsData[type];
    const remaining = data.budget - data.spent;
    const percentSpent = Math.round((data.spent / data.budget) * 100);
    
    row.querySelector('.allocated').textContent = `{data.budget.toLocaleString()}`;
    row.querySelector('.spent').textContent = `{data.spent.toLocaleString()}`;
    row.querySelector('.remaining').textContent = `{remaining.toLocaleString()}`;
    row.querySelector('.progress-bar').style.width = `{percentSpent}%`;
}

function renderActivities() {
    activityList.innerHTML = '';
    activities.forEach(activity => {
        const li = document.createElement('li');
        li.innerHTML = `
            <div class="d-flex">
                <div class="flex-shrink-0 me-3">
                    <i class="bi bi-{activity.icon} text-{activity.type}"></i>
                </div>
                <div>
                    <p class="mb-0">{activity.message}</p>
                    <small class="text-muted">{activity.time}</small>
                </div>
            </div>
        `;
        activityList.appendChild(li);
    });
}

function showProjectDetails(type) {
    // In a real app, this would show a detailed view or modal
    showToast(`Showing details for {type} projects`);
}

function exportReport() {
    // In a real app, this would generate a PDF or Excel report
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
    
    // Update the relevant project type
    projectsData[projectType].count++;
    projectsData[projectType].progress = Math.min(100, Math.max(0, 
        Math.round((projectsData[projectType].progress * (projectsData[projectType].count - 1) + progress) / projectsData[projectType].count)
    ));
    
    // Update status based on average progress
    if (projectsData[projectType].progress >= 75) {
        projectsData[projectType].status = 'excellent';
    } else {
        projectsData[projectType].status = 'normal';
    }
    
    // Add budget if provided
    if (budget > 0) {
        projectsData[projectType].budget += budget;
    }
    
    // Add to activities
    const projectName = document.getElementById('projectName').value || 'New Project';
    activities.unshift({
        type: 'success',
        icon: 'plus-circle',
        message: `Added new project: {projectName}`,
        time: 'Just now'
    });
    
    // Update UI
    updateDashboard();
    renderActivities();
    
    // Close modal and reset form
    bootstrap.Modal.getInstance(document.getElementById('addProjectModal')).hide();
    form.reset();
    errorElement.classList.add('d-none');
    
    showToast('Project added successfully!');
}

function saveBudget() {
    const softwareBudget = parseInt(document.getElementById('softwareBudget').value);
    const researchBudget = parseInt(document.getElementById('researchBudget').value);
    const booksBudget = parseInt(document.getElementById('booksBudget').value);
    
    if (isNaN(softwareBudget) || isNaN(researchBudget) || isNaN(booksBudget) || 
        softwareBudget < 0 || researchBudget < 0 || booksBudget < 0) {
        document.getElementById('budgetError').textContent = 'Please enter valid budget amounts';
        document.getElementById('budgetError').classList.remove('d-none');
        return;
    }
    
    // Update budgets
    projectsData.software.budget = softwareBudget;
    projectsData.research.budget = researchBudget;
    projectsData.books.budget = booksBudget;
    
    // Update UI
    updateDashboard();
    
    // Close modal
    bootstrap.Modal.getInstance(document.getElementById('editBudgetModal')).hide();
    document.getElementById('budgetError').classList.add('d-none');
    
    // Add activity
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
    document.querySelector('.toast-body').textContent = message;
    successToast.show();
}
