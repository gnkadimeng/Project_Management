// Initialize data and DOM elements
let papers = [];
let nextId = 1;
let paperToDelete = null;
const toastLiveExample = document.getElementById('liveToast');
const toast = new bootstrap.Toast(toastLiveExample);

// DOM elements
const paperForm = document.getElementById('paperForm');
const savePaperBtn = document.getElementById('savePaperBtn');
const editPaperForm = document.getElementById('editPaperForm');
const updatePaperBtn = document.getElementById('updatePaperBtn');
const confirmDeleteBtn = document.getElementById('confirmDeleteBtn');
const searchInput = document.getElementById('searchInput');
const internalPapersBody = document.getElementById('internalPapersBody');
const externalPapersBody = document.getElementById('externalPapersBody');
const journalInfoRow = document.getElementById('journalInfoRow');
const editJournalInfoRow = document.getElementById('editJournalInfoRow');

// Initialize the app
document.addEventListener('DOMContentLoaded', function() {
// Set up event listeners
setupEventListeners();

// Load sample data
loadSampleData();

// Render papers
renderPapers();

// Initialize date fields
initializeDates();
});

function setupEventListeners() {
// Paper type change - show/hide journal info
document.getElementById('paperType').addEventListener('change', function() {
journalInfoRow.style.display = this.value === 'external' ? 'flex' : 'none';
});

// Save paper button
// savePaperBtn.addEventListener('click', savePaper);
// static/js/journal.js

document.getElementById("savePaperBtn").addEventListener("click", function () {
    const form = document.getElementById("paperForm");
    const formData = new FormData(form);

    fetch("/manager/add-paper/", {
        method: "POST",
        headers: {
            "X-CSRFToken": getCookie("csrftoken")
        },
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showToast("Paper added successfully!");
            document.getElementById("paperForm").reset();
            const modal = bootstrap.Modal.getInstance(document.getElementById('addPaperModal'));
            modal.hide();
            // Optionally reload or dynamically add to the table
        } else {
            showToast("Error: " + data.error);
        }
    })
    .catch(err => console.error(err));
});


// Update paper button
updatePaperBtn.addEventListener('click', updatePaper);

// Confirm delete button
confirmDeleteBtn.addEventListener('click', confirmDelete);

// Search input
searchInput.addEventListener('input', filterPapers);

// Edit paper type change - show/hide journal info
document.getElementById('editPaperType').addEventListener('change', function() {
editJournalInfoRow.style.display = this.value === 'external' ? 'flex' : 'none';
});
}

function loadSampleData() {
// Sample internal papers
papers = [
{
    id: nextId++,
    title: "Machine Learning Approaches to Climate Modeling",
    type: "internal",
    status: "in-progress",
    version: "1.2",
    lastUpdated: "2024-05-15",
    leadAuthor: "Sarah Johnson",
    coAuthors: "Michael Chen",
    abstract: "Exploring ML techniques for climate prediction models.",
    file: null,
    comments: 3
},
{
    id: nextId++,
    title: "Quantum Computing Applications in Finance",
    type: "internal",
    status: "draft",
    version: "0.8",
    lastUpdated: "2024-04-28",
    leadAuthor: "Robert Lee",
    coAuthors: "",
    abstract: "Investigating quantum algorithms for financial modeling.",
    file: null,
    comments: 1
},
{
    id: nextId++,
    title: "Neural Networks for Medical Diagnosis",
    type: "internal",
    status: "review",
    version: "2.1",
    lastUpdated: "2024-06-02",
    leadAuthor: "Emily Davis",
    coAuthors: "James Wilson",
    abstract: "Deep learning approaches for early disease detection.",
    file: null,
    comments: 5
},
{
    id: nextId++,
    title: "Advanced Techniques in Data Visualization",
    type: "external",
    status: "published",
    version: "3.0",
    lastUpdated: "2024-02-10",
    leadAuthor: "Maria Garcia",
    coAuthors: "Thomas Brown",
    targetJournal: "IEEE Transactions on Visualization",
    submissionDate: "2024-01-05",
    decisionDate: "2024-01-25",
    abstract: "Novel visualization methods for big data analytics.",
    file: null
},
{
    id: nextId++,
    title: "Machine Learning Approaches to Climate Modeling",
    type: "external",
    status: "review",
    version: "1.2",
    lastUpdated: "2024-05-20",
    leadAuthor: "Sarah Johnson",
    coAuthors: "Michael Chen",
    targetJournal: "Journal of Artificial Intelligence Research",
    submissionDate: "2024-05-20",
    decisionDate: "",
    abstract: "Exploring ML techniques for climate prediction models.",
    file: null
}
];
}

function initializeDates() {
const today = new Date().toISOString().split('T')[0];
document.getElementById('submissionDate').value = today;

// Set submission date to 1 month from now by default
const futureDate = new Date();
futureDate.setMonth(futureDate.getMonth() + 1);
document.getElementById('submissionDate').valueAsDate = futureDate;
}

function renderPapers() { 
// Clear existing rows
internalPapersBody.innerHTML = '';
externalPapersBody.innerHTML = '';

// Filter papers based on search term
const searchTerm = searchInput.value.toLowerCase();
const filteredPapers = papers.filter(paper => 
paper.title.toLowerCase().includes(searchTerm) ||
paper.leadAuthor.toLowerCase().includes(searchTerm) ||
(paper.coAuthors && paper.coAuthors.toLowerCase().includes(searchTerm))
); // <-- this closing parenthesis was missing

// Render each paper
filteredPapers.forEach(paper => {
if (paper.type === 'internal') {
    renderInternalPaper(paper);
} else {
    renderExternalPaper(paper);
}
});
}

function renderInternalPaper(paper) {
const row = document.createElement('tr');
row.dataset.id = paper.id;

// Status dropdown
const statusOptions = {
'draft': 'Draft',
'in-progress': 'In Progress',
'review': 'Internal Review',
'submitted': 'Submitted',
'accepted': 'Accepted',
'published': 'Published',
'rejected': 'Rejected'
};

let statusSelect = `<select class="status-select" data-id="${paper.id}" 
style="${getStatusStyle(paper.status)}" onchange="updateStatus(${paper.id}, this.value)">
${Object.entries(statusOptions).map(([value, text]) => 
    `<option value="${value}" ${paper.status === value ? 'selected' : ''}>${text}</option>`
).join('')}
</select>`;

row.innerHTML = `
<td>${paper.title}</td>
<td>${paper.leadAuthor}${paper.coAuthors ? ', ' + paper.coAuthors : ''}</td>
<td>${statusSelect}</td>
<td>${paper.version}</td>
<td>${formatDate(paper.lastUpdated)}</td>
<td class="actions-cell">
    <button class="btn btn-sm btn-outline-primary me-1" onclick="viewPaper(${paper.id})">
        <i class="bi bi-eye"></i>
    </button>
    <button class="btn btn-sm btn-outline-secondary me-1" onclick="editPaper(${paper.id})">
        <i class="bi bi-pencil"></i>
    </button>
    <button class="btn btn-sm btn-outline-danger" onclick="showDeleteConfirmation(${paper.id})">
        <i class="bi bi-trash"></i>
    </button>
</td>
`;

internalPapersBody.appendChild(row);
}

function renderExternalPaper(paper) {
const row = document.createElement('tr');
row.dataset.id = paper.id;

// Status dropdown
const statusOptions = {
'draft': 'Draft',
'in-progress': 'In Progress',
'review': 'Under Review',
'submitted': 'Submitted',
'accepted': 'Accepted',
'published': 'Published',
'rejected': 'Rejected'
};

let statusSelect = `<select class="status-select" data-id="${paper.id}" 
style="${getStatusStyle(paper.status)}" onchange="updateStatus(${paper.id}, this.value)">
${Object.entries(statusOptions).map(([value, text]) => 
    `<option value="${value}" ${paper.status === value ? 'selected' : ''}>${text}</option>`
).join('')}
</select>`;

row.innerHTML = `
<td>${paper.title}</td>
<td>${paper.leadAuthor}${paper.coAuthors ? ', ' + paper.coAuthors : ''}</td>
<td>${paper.targetJournal || '-'}</td>
<td>${statusSelect}</td>
<td>${formatDate(paper.submissionDate)}</td>
<td>${paper.decisionDate ? formatDate(paper.decisionDate) : '-'}</td>
<td class="actions-cell">
    <button class="btn btn-sm btn-outline-primary me-1" onclick="viewPaper(${paper.id})">
        <i class="bi bi-eye"></i>
    </button>
    <button class="btn btn-sm btn-outline-secondary me-1" onclick="editPaper(${paper.id})">
        <i class="bi bi-pencil"></i>
    </button>
    <button class="btn btn-sm btn-outline-danger" onclick="showDeleteConfirmation(${paper.id})">
        <i class="bi bi-trash"></i>
    </button>
</td>
`;

externalPapersBody.appendChild(row);
}

function getStatusStyle(status) {
const styles = {
'draft': 'background-color: #f8f9fa; color: #6c757d; border: 1px solid #dee2e6;',
'in-progress': 'background-color: #fff3cd; color: #856404;',
'review': 'background-color: #cce5ff; color: #004085;',
'submitted': 'background-color: #e2e3e5; color: #383d41;',
'accepted': 'background-color: #d4edda; color: #155724;',
'published': 'background-color: #d1e7dd; color: #0a3622; font-weight: bold;',
'rejected': 'background-color: #f8d7da; color: #721c24;'
};
return styles[status] || '';
}

function formatDate(dateString) {
if (!dateString) return '-';
const options = { year: 'numeric', month: 'short', day: 'numeric' };
return new Date(dateString).toLocaleDateString('en-US', options);
}

function savePaper() {
if (!paperForm.checkValidity()) {
document.getElementById('formError').textContent = 'Please fill in all required fields';
document.getElementById('formError').classList.remove('d-none');
return;
}

const paperType = document.getElementById('paperType').value;
const newPaper = {
id: nextId++,
title: document.getElementById('paperTitle').value,
type: paperType,
status: document.getElementById('paperStatus').value,
version: document.getElementById('currentVersion').value,
lastUpdated: new Date().toISOString().split('T')[0],
leadAuthor: document.getElementById('leadAuthor').value,
coAuthors: document.getElementById('coAuthors').value,
abstract: document.getElementById('paperAbstract').value,
file: document.getElementById('paperFile').files[0] || null
};

if (paperType === 'external') {
newPaper.targetJournal = document.getElementById('targetJournal').value;
newPaper.submissionDate = document.getElementById('submissionDate').value;
newPaper.decisionDate = '';
}

papers.push(newPaper);
renderPapers();

// Reset form and close modal
paperForm.reset();
document.getElementById('formError').classList.add('d-none');
bootstrap.Modal.getInstance(document.getElementById('addPaperModal')).hide();

showToast('Paper added successfully!', 'success');
}

function editPaper(id) {
const paper = papers.find(p => p.id === id);
if (!paper) return;

// Fill the edit form with paper data
document.getElementById('editPaperId').value = paper.id;
document.getElementById('editPaperTitle').value = paper.title;
document.getElementById('editPaperType').value = paper.type;
document.getElementById('editPaperStatus').value = paper.status;
document.getElementById('editCurrentVersion').value = paper.version;
document.getElementById('editLeadAuthor').value = paper.leadAuthor;
document.getElementById('editCoAuthors').value = paper.coAuthors || '';
document.getElementById('editPaperAbstract').value = paper.abstract || '';

if (paper.type === 'external') {
document.getElementById('editTargetJournal').value = paper.targetJournal || '';
document.getElementById('editSubmissionDate').value = paper.submissionDate || '';
editJournalInfoRow.style.display = 'flex';
} else {
editJournalInfoRow.style.display = 'none';
}

// Show the edit modal
const editModal = new bootstrap.Modal(document.getElementById('editPaperModal'));
editModal.show();
}

function updatePaper() {
if (!editPaperForm.checkValidity()) {
document.getElementById('editFormError').textContent = 'Please fill in all required fields';
document.getElementById('editFormError').classList.remove('d-none');
return;
}

const id = parseInt(document.getElementById('editPaperId').value);
const paperIndex = papers.findIndex(p => p.id === id);
if (paperIndex === -1) return;

const paperType = document.getElementById('editPaperType').value;

papers[paperIndex] = {
...papers[paperIndex],
title: document.getElementById('editPaperTitle').value,
status: document.getElementById('editPaperStatus').value,
version: document.getElementById('editCurrentVersion').value,
lastUpdated: new Date().toISOString().split('T')[0],
leadAuthor: document.getElementById('editLeadAuthor').value,
coAuthors: document.getElementById('editCoAuthors').value,
abstract: document.getElementById('editPaperAbstract').value,
file: document.getElementById('editPaperFile').files[0] || papers[paperIndex].file
};

if (paperType === 'external') {
papers[paperIndex].targetJournal = document.getElementById('editTargetJournal').value;
papers[paperIndex].submissionDate = document.getElementById('editSubmissionDate').value;

// If status changed to accepted/published/rejected, set decision date
const newStatus = document.getElementById('editPaperStatus').value;
if (['accepted', 'published', 'rejected'].includes(newStatus)) {
    papers[paperIndex].decisionDate = new Date().toISOString().split('T')[0];
}
}

renderPapers();

// Reset form and close modal
editPaperForm.reset();
document.getElementById('editFormError').classList.add('d-none');
bootstrap.Modal.getInstance(document.getElementById('editPaperModal')).hide();

showToast('Paper updated successfully!', 'success');
}

function showDeleteConfirmation(id) {
paperToDelete = id;
const confirmModal = new bootstrap.Modal(document.getElementById('confirmDeleteModal'));
confirmModal.show();
}

function confirmDelete() {
if (!paperToDelete) return;

const paperIndex = papers.findIndex(p => p.id === paperToDelete);
if (paperIndex !== -1) {
papers.splice(paperIndex, 1);
renderPapers();
showToast('Paper deleted successfully!', 'success');
}

paperToDelete = null;
bootstrap.Modal.getInstance(document.getElementById('confirmDeleteModal')).hide();
}

function updateStatus(id, newStatus) {
const paper = papers.find(p => p.id === id);
if (!paper) return;

paper.status = newStatus;
paper.lastUpdated = new Date().toISOString().split('T')[0];

// If external paper and status is accepted/published/rejected, set decision date
if (paper.type === 'external' && ['accepted', 'published', 'rejected'].includes(newStatus)) {
if (!paper.decisionDate) {
    paper.decisionDate = new Date().toISOString().split('T')[0];
}
}

renderPapers();
showToast('Status updated successfully!', 'success');
}

function viewPaper(id) {
const paper = papers.find(p => p.id === id);
if (!paper) return;

// In a real app, this would open a detailed view modal
showToast(`Viewing paper: ${paper.title}`, 'info');
}

function filterPapers() {
renderPapers();
}

function showToast(message, type = 'info') {
const toastTitle = document.getElementById('toastTitle');
const toastMessage = document.getElementById('toastMessage');

// Set title based on type
const titles = {
'success': 'Success',
'error': 'Error',
'warning': 'Warning',
'info': 'Info'
};

toastTitle.textContent = titles[type] || 'Notification';
toastMessage.textContent = message;

// Set appropriate icon and color
const toastHeader = toastLiveExample.querySelector('.toast-header');
toastHeader.className = 'toast-header';

switch(type) {
case 'success':
    toastHeader.classList.add('bg-success', 'text-white');
    break;
case 'error':
    toastHeader.classList.add('bg-danger', 'text-white');
    break;
case 'warning':
    toastHeader.classList.add('bg-warning', 'text-dark');
    break;
default:
    toastHeader.classList.add('bg-info', 'text-white');
}

toast.show();
}

// Sidebar Toggle Functionality
const toggleBtn = document.getElementById('toggleBtn');
const sidebar = document.getElementById('sidebar');
const mainContent = document.getElementById('mainContent');
const mobileMenuBtn = document.getElementById('mobileMenuBtn');

toggleBtn.addEventListener('click', function() {
    sidebar.classList.toggle('collapsed');
    mainContent.classList.toggle('expanded');
    
    // Change the icon based on state
    const icon = toggleBtn.querySelector('i');
    if (sidebar.classList.contains('collapsed')) {
        icon.classList.remove('bi-chevron-left');
        icon.classList.add('bi-chevron-right');
    } else {
        icon.classList.remove('bi-chevron-right');
        icon.classList.add('bi-chevron-left');
    }
});

// Mobile Menu Toggle
mobileMenuBtn.addEventListener('click', function() {
    sidebar.classList.toggle('show');
});

// Close sidebar when clicking outside on mobile
document.addEventListener('click', function(event) {
    if (window.innerWidth <= 768 && !sidebar.contains(event.target) && event.target !== mobileMenuBtn) {
        sidebar.classList.remove('show');
    }
});
