// script.js

document.addEventListener("DOMContentLoaded", () => {
  const saveTaskBtn = document.getElementById("saveTask");

  // Sidebar functionality
  const toggleBtn = document.getElementById("toggleBtn");
  const sidebar = document.getElementById("sidebar");
  const mainContent = document.getElementById("mainContent");
  const mobileMenuBtn = document.getElementById("mobileMenuBtn");

  toggleBtn.addEventListener("click", () => {
    sidebar.classList.toggle("collapsed");
    mainContent.classList.toggle("expanded");

    const icon = toggleBtn.querySelector("i");
    icon.classList.toggle("bi-chevron-left");
    icon.classList.toggle("bi-chevron-right");
  });

  mobileMenuBtn.addEventListener("click", () => {
    sidebar.classList.toggle("show");
  });

  document.addEventListener("click", (event) => {
    if (window.innerWidth <= 768 && !sidebar.contains(event.target) && event.target !== mobileMenuBtn) {
      sidebar.classList.remove("show");
    }
  });

  // Task creation
  saveTaskBtn.addEventListener("click", () => {
    const title = document.getElementById("taskTitle").value.trim();
    const priority = document.getElementById("taskPriority").value;
    const dueDate = document.getElementById("taskDate").value;
    const frontend = document.getElementById("frontendTag").checked;
    const backend = document.getElementById("backendTag").checked;

    if (!title || !dueDate) {
      alert("Please enter all required fields.");
      return;
    }

    const taskCard = document.createElement("div");
    taskCard.className = "kanban-item";
    taskCard.draggable = true;
    taskCard.innerHTML = `
      <div class="task-title">${title}</div>
      <div class="priority ${priority}">${priority.toUpperCase()} PRIORITY</div>
      <div class="due-date">Due: ${dueDate}</div>
      <div class="task-tags">
        ${frontend ? '<span class="badge bg-info me-1">Frontend</span>' : ''}
        ${backend ? '<span class="badge bg-warning text-dark">Backend</span>' : ''}
      </div>
    `;

    document.getElementById("todo").appendChild(taskCard);

    // Clear form
    document.getElementById("taskTitle").value = "";
    document.getElementById("taskPriority").value = "low";
    document.getElementById("taskDate").value = "";
    document.getElementById("frontendTag").checked = false;
    document.getElementById("backendTag").checked = false;

    saveTasksToLocalStorage();
  });

  // Report generation buttons
  document.getElementById("generate-report-btn").addEventListener("click", generateReport);
  document.getElementById("download-report-btn").addEventListener("click", downloadReportAsPDF);
  document.getElementById("send-report-btn").addEventListener("click", () => alert("Report sent!"));

  // Drag functionality
  document.querySelectorAll(".kanban-column").forEach(column => {
    column.addEventListener("dragover", e => e.preventDefault());
    column.addEventListener("drop", function (e) {
      const id = e.dataTransfer.getData("text/plain");
      const task = document.getElementById(id);
      column.appendChild(task);
      task.style.opacity = "1";
      saveTasksToLocalStorage();
    });
  });

  // Load tasks from storage
  loadTasksFromLocalStorage();
});

function saveTasksToLocalStorage() {
  const columns = document.querySelectorAll(".kanban-column");
  const tasks = [];

  columns.forEach(column => {
    const columnId = column.id;
    column.querySelectorAll(".kanban-item").forEach((task, index) => {
      tasks.push({
        id: `${columnId}-task-${index}`,
        title: task.querySelector(".task-title").textContent,
        priority: task.querySelector(".priority").classList[1],
        dueDate: task.querySelector(".due-date").textContent.replace("Due: ", ""),
        frontend: task.innerHTML.includes("Frontend"),
        backend: task.innerHTML.includes("Backend"),
        column: columnId
      });
    });
  });

  localStorage.setItem("kanbanTasks", JSON.stringify(tasks));
}

function loadTasksFromLocalStorage() {
  const saved = JSON.parse(localStorage.getItem("kanbanTasks")) || [];

  saved.forEach(task => {
    const taskCard = document.createElement("div");
    taskCard.className = "kanban-item";
    taskCard.draggable = true;
    taskCard.id = task.id;
    taskCard.innerHTML = `
      <div class="task-title">${task.title}</div>
      <div class="priority ${task.priority}">${task.priority.toUpperCase()} PRIORITY</div>
      <div class="due-date">Due: ${task.dueDate}</div>
      <div class="task-tags">
        ${task.frontend ? '<span class="badge bg-info me-1">Frontend</span>' : ''}
        ${task.backend ? '<span class="badge bg-warning text-dark">Backend</span>' : ''}
      </div>
    `;

    taskCard.addEventListener("dragstart", function (e) {
      e.dataTransfer.setData("text/plain", taskCard.id);
      taskCard.style.opacity = "0.4";
    });

    document.getElementById(task.column).appendChild(taskCard);
  });
}

function generateReport() {
  const columns = document.querySelectorAll(".kanban-column");
  let reportHTML = '<h3>Task Report</h3><table class="table table-bordered"><thead><tr><th>Task</th><th>Status</th><th>Priority</th><th>Due Date</th></tr></thead><tbody>';

  columns.forEach(col => {
    const status = col.querySelector("h4").textContent;
    col.querySelectorAll(".kanban-item").forEach(task => {
      reportHTML += `
        <tr>
          <td>${task.querySelector(".task-title").textContent}</td>
          <td>${status}</td>
          <td>${task.querySelector(".priority").textContent}</td>
          <td>${task.querySelector(".due-date").textContent.replace("Due: ", "")}</td>
        </tr>
      `;
    });
  });

  reportHTML += '</tbody></table>';
  document.getElementById("report")?.remove();
  const reportDiv = document.createElement("div");
  reportDiv.id = "report";
  reportDiv.innerHTML = reportHTML;
  document.querySelector(".main-content").appendChild(reportDiv);
}

function downloadReportAsPDF() {
  const { jsPDF } = window.jspdf;
  const doc = new jsPDF();

  const headers = ['Task', 'Status', 'Priority', 'Due Date'];
  const rows = [];

  document.querySelectorAll(".kanban-column").forEach(col => {
    const status = col.querySelector("h4").textContent;
    col.querySelectorAll(".kanban-item").forEach(task => {
      rows.push([
        task.querySelector(".task-title").textContent,
        status,
        task.querySelector(".priority").textContent,
        task.querySelector(".due-date").textContent.replace("Due: ", "")
      ]);
    });
  });

  doc.autoTable({ head: [headers], body: rows, startY: 20 });
  doc.save("kanban_report.pdf");
}
