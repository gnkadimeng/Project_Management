// Sidebar Toggle Functionality
const toggleBtn = document.getElementById('toggleBtn');
const sidebar = document.getElementById('sidebar');
const mainContent = document.getElementById('mainContent');
const mobileMenuBtn = document.getElementById('mobileMenuBtn');

toggleBtn.addEventListener('click', function () {
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
mobileMenuBtn.addEventListener('click', function () {
    sidebar.classList.toggle('show');
});

// Close sidebar when clicking outside on mobile
document.addEventListener('click', function (event) {
    if (window.innerWidth <= 768 && !sidebar.contains(event.target) && event.target !== mobileMenuBtn) {
        sidebar.classList.remove('show');
    }
});

// Task Management
document.addEventListener('DOMContentLoaded', function () {
    // DOM Elements
    const addTaskBtn = document.getElementById('add-task-btn');
    const saveTaskBtn = document.getElementById('save-task-btn');
    const editTaskModal = new bootstrap.Modal(document.getElementById('editTaskModal'));

    // Current task being edited
    let currentTaskCard = null;

    // Initialize the board
    loadTasksFromLocalStorage();

    // Add Task Functionality
    addTaskBtn.addEventListener('click', addTask);

    // Save Task Changes
    saveTaskBtn.addEventListener('click', saveTaskChanges);

    // Report Buttons
    document.getElementById('generate-report-btn').addEventListener('click', generateReport);
    document.getElementById('download-report-btn').addEventListener('click', downloadReportAsPDF);
    document.getElementById('send-report-btn').addEventListener('click', sendReport);
});

function addTask() {
    const title = document.getElementById('task-title').value.trim();
    const description = document.getElementById('task-description').value.trim();
    const priority = document.getElementById('task-priority').value;
    const dueDate = document.getElementById('task-due-date').value;

    if (title && description && dueDate) {
        const taskCard = document.createElement('div');
        taskCard.className = 'kanban-item';
        taskCard.draggable = true;
        taskCard.dataset.priority = priority;
        taskCard.dataset.dueDate = dueDate;

        taskCard.innerHTML = `
            <div class="task-title">${title}</div>
            <div class="task-description">${description}</div>
            <div class="priority ${priority}">${priority.toUpperCase()} PRIORITY</div>
            <div class="due-date">Due: ${dueDate}</div>
            <div class="task-actions">
                <button class="btn btn-sm btn-primary edit-btn"><i class="bi-pencil"></i> Edit</button>
                <button class="btn btn-sm btn-danger delete-btn"><i class="bi-trash"></i> Delete</button>
            </div>
        `;

        document.getElementById('backlog').appendChild(taskCard);

        // Clear form
        document.getElementById('task-title').value = '';
        document.getElementById('task-description').value = '';
        document.getElementById('task-due-date').value = '';

        // Add event listeners
        addTaskEventListeners(taskCard);
        saveTasksToLocalStorage();
    } else {
        alert('Please fill in all fields!');
    }
}

function addTaskEventListeners(taskCard) {
    // Drag and drop
    taskCard.addEventListener('dragstart', drag);

    // Edit button
    taskCard.querySelector('.edit-btn').addEventListener('click', () => openEditModal(taskCard));

    // Delete button
    taskCard.querySelector('.delete-btn').addEventListener('click', () => {
        if (confirm('Are you sure you want to delete this task?')) {
            taskCard.remove();
            saveTasksToLocalStorage();
        }
    });
}

function openEditModal(taskCard) {
    currentTaskCard = taskCard;

    document.getElementById('edit-task-title').value = taskCard.querySelector('.task-title').textContent;
    document.getElementById('edit-task-description').value = taskCard.querySelector('.task-description').textContent;
    document.getElementById('edit-task-priority').value = taskCard.dataset.priority;
    document.getElementById('edit-task-due-date').value = taskCard.dataset.dueDate;

    editTaskModal.show();
}

function saveTaskChanges() {
    const title = document.getElementById('edit-task-title').value.trim();
    const description = document.getElementById('edit-task-description').value.trim();
    const priority = document.getElementById('edit-task-priority').value;
    const dueDate = document.getElementById('edit-task-due-date').value;

    if (title && description && dueDate) {
        currentTaskCard.querySelector('.task-title').textContent = title;
        currentTaskCard.querySelector('.task-description').textContent = description;
        currentTaskCard.querySelector('.priority').className = `priority ${priority}`;
        currentTaskCard.querySelector('.priority').textContent = `${priority.toUpperCase()} PRIORITY`;
        currentTaskCard.querySelector('.due-date').textContent = `Due: ${dueDate}`;
        currentTaskCard.dataset.priority = priority;
        currentTaskCard.dataset.dueDate = dueDate;

        editTaskModal.hide();
        saveTasksToLocalStorage();
    } else {
        alert('Please fill in all fields!');
    }
}

// Drag and Drop Functions
function allowDrop(event) {
    event.preventDefault();
}

function drag(event) {
    event.dataTransfer.setData("text", event.target.id);
    event.target.style.opacity = '0.4';
}

function drop(event) {
    event.preventDefault();
    const data = event.dataTransfer.getData("text");
    const draggedElement = document.getElementById(data);

    // Check if we're dropping on a column or another task
    const dropTarget = event.target.classList.contains('kanban-column') ?
        event.target :
        event.target.closest('.kanban-column');

    dropTarget.appendChild(draggedElement);
    draggedElement.style.opacity = '1';
    saveTasksToLocalStorage();
}

// Local Storage Functions
function saveTasksToLocalStorage() {
    const columns = {
        backlog: document.getElementById('backlog'),
        todo: document.getElementById('todo'),
        'in-progress': document.getElementById('in-progress'),
        done: document.getElementById('done')
    };

    const tasks = [];

    Object.entries(columns).forEach(([columnId, column]) => {
        const columnTasks = column.querySelectorAll('.kanban-item');
        columnTasks.forEach(task => {
            tasks.push({
                id: task.id,
                title: task.querySelector('.task-title').textContent,
                description: task.querySelector('.task-description').textContent,
                priority: task.dataset.priority,
                dueDate: task.dataset.dueDate,
                column: columnId
            });
        });
    });

    localStorage.setItem('kanbanTasks', JSON.stringify(tasks));
}

function loadTasksFromLocalStorage() {
    const tasks = JSON.parse(localStorage.getItem('kanbanTasks')) || [];

    tasks.forEach(task => {
        const taskCard = document.createElement('div');
        taskCard.className = 'kanban-item';
        taskCard.draggable = true;
        taskCard.id = task.id || `task-${Date.now()}`;
        taskCard.dataset.priority = task.priority;
        taskCard.dataset.dueDate = task.dueDate;

        taskCard.innerHTML = `
            <div class="task-title">${task.title}</div>
            <div class="task-description">${task.description}</div>
            <div class="priority ${task.priority}">${task.priority.toUpperCase()} PRIORITY</div>
            <div class="due-date">Due: ${task.dueDate}</div>
            <div class="task-actions">
                <button class="btn btn-sm btn-primary edit-btn"><i class="bi-pencil"></i> Edit</button>
                <button class="btn btn-sm btn-danger delete-btn"><i class="bi-trash"></i> Delete</button>
            </div>
        `;

        document.getElementById(task.column).appendChild(taskCard);
        addTaskEventListeners(taskCard);
    });
}

// Report Functions
function generateReport() {
    const columns = {
        backlog: document.getElementById('backlog'),
        todo: document.getElementById('todo'),
        'in-progress': document.getElementById('in-progress'),
        done: document.getElementById('done')
    };

    let reportHTML = '<h3>Task Report</h3><table class="table table-bordered"><thead><tr><th>Task</th><th>Status</th><th>Priority</th><th>Due Date</th></tr></thead><tbody>';

    Object.entries(columns).forEach(([columnId, column]) => {
        const columnName = column.querySelector('h4').textContent;
        const tasks = column.querySelectorAll('.kanban-item');

        tasks.forEach(task => {
            reportHTML += `
                <tr>
                    <td>${task.querySelector('.task-title').textContent}</td>
                    <td>${columnName}</td>
                    <td class="${task.dataset.priority}">${task.dataset.priority.toUpperCase()}</td>
                    <td>${task.dataset.dueDate}</td>
                </tr>
            `;
        });
    });

    reportHTML += '</tbody></table>';
    document.getElementById('report').innerHTML = reportHTML;
}

function downloadReportAsPDF() {
    const { jsPDF } = window.jspdf;
    const doc = new jsPDF();

    const columns = {
        backlog: document.getElementById('backlog'),
        todo: document.getElementById('todo'),
        'in-progress': document.getElementById('in-progress'),
        done: document.getElementById('done')
    };

    // Get all tasks from all columns
    const allTasks = [];
    Object.entries(columns).forEach(([columnId, column]) => {
        const columnName = column.querySelector('h4').textContent;
        const tasks = column.querySelectorAll('.kanban-item');

        tasks.forEach(task => {
            allTasks.push({
                title: task.querySelector('.task-title').textContent,
                description: task.querySelector('.task-description').textContent,
                priority: task.dataset.priority,
                dueDate: task.dataset.dueDate,
                column: columnName
            });
        });
    });

    // Add title
    doc.setFontSize(18);
    doc.text('Kanban Board Report', 105, 15, { align: 'center' });
    doc.setFontSize(12);

    // Add table
    const headers = ['Task', 'Description', 'Status', 'Priority', 'Due Date'];
    const rows = allTasks.map(task => [
        task.title,
        task.description,
        task.column,
        task.priority.toUpperCase(),
        task.dueDate
    ]);

    doc.autoTable({
        head: [headers],
        body: rows,
        startY: 25,
        styles: {
            cellPadding: 5,
            fontSize: 10,
            valign: 'middle'
        },
        columnStyles: {
            0: { cellWidth: 40 },
            1: { cellWidth: 60 },
            2: { cellWidth: 30 },
            3: { cellWidth: 25 },
            4: { cellWidth: 30 }
        }
    });

    // Save the PDF
    doc.save('kanban_report.pdf');
}

function sendReport() {
    alert('Report sent! (This would email the report in a real implementation)');
}

// Initialize sidebar state based on screen size
window.addEventListener('load', function () {
    if (window.innerWidth <= 768) {
        sidebar.classList.remove('collapsed');
        sidebar.classList.remove('show');
        mainContent.classList.remove('expanded');
    }
});

// Handle window resize
window.addEventListener('resize', function () {
    if (window.innerWidth > 768) {
        sidebar.classList.remove('show');
    }
});
