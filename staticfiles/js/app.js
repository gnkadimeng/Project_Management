let editTaskModal;
let currentTaskCard = null;

document.addEventListener("DOMContentLoaded", () => {
  editTaskModal = new bootstrap.Modal(document.getElementById("editTaskModal"));
  const saveTaskBtn = document.getElementById("saveTask");

  // Sidebar toggle
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

  // Add Task
  saveTaskBtn.addEventListener("click", () => {
    const title = document.getElementById("taskTitle").value.trim();
    const description = document.getElementById("task-description").value.trim();
    const priority = document.getElementById("taskPriority").value;
    const dueDate = document.getElementById("taskDate").value;

    const tags = getTags([
      "uxuiTag", "architectureTag", "frontendTag",
      "backendTag", "testingTag", "deploymentTag"
    ]);

    console.log("Add Task Data:", { title, description, priority, dueDate, tags });

    if (!title || !dueDate) {
      alert("Please enter all required fields.");
      return;
    }

    const taskCard = createTaskCard(title, description, priority, dueDate, tags);
    document.getElementById("todo").appendChild(taskCard);
    addTaskEventListeners(taskCard);
    clearForm();
    saveTasksToLocalStorage();
  });

  // Save Task Changes
  document.getElementById("save-task-btn").addEventListener("click", () => {
    const title = document.getElementById("edit-task-title").value.trim();
    const description = document.getElementById("edit-task-description").value.trim();
    const priority = document.getElementById("edit-task-priority").value;
    const dueDate = document.getElementById("edit-task-due-date").value;

    const tags = getTags([
      "edit-uxuiTag", "edit-architectureTag", "edit-frontendTag",
      "edit-backendTag", "edit-testingTag", "edit-deploymentTag"
    ]);

    if (title && dueDate) {
      currentTaskCard.querySelector(".task-title").textContent = title;
      currentTaskCard.querySelector(".task-description").textContent = description;
      currentTaskCard.querySelector(".priority").className = `priority ${priority}`;
      currentTaskCard.querySelector(".priority").textContent = `${priority.toUpperCase()} PRIORITY`;
      currentTaskCard.querySelector(".due-date").textContent = `Due: ${dueDate}`;
      currentTaskCard.dataset.priority = priority;
      currentTaskCard.dataset.dueDate = dueDate;
      currentTaskCard.dataset.tags = tags.join(",");

      const tagsDiv = currentTaskCard.querySelector(".task-tags");
      tagsDiv.innerHTML = tags.map(tag => createBadge(tag)).join(" ");

      editTaskModal.hide();
      saveTasksToLocalStorage();
    } else {
      alert("Please fill in all fields.");
    }
  });

  loadTasksFromLocalStorage();

  document.querySelectorAll(".kanban-column").forEach((column) => {
    column.addEventListener("dragover", (e) => e.preventDefault());
    column.addEventListener("drop", function (e) {
      const id = e.dataTransfer.getData("text/plain");
      const task = document.getElementById(id);
      column.appendChild(task);
      task.style.opacity = "1";
      saveTasksToLocalStorage();
    });
  });
});

// === Utility Functions ===

function getTags(ids) {
  const tags = [];
  ids.forEach((id) => {
    const el = document.getElementById(id);
    if (el && el.checked) {
      tags.push(id.replace("edit-", "").replace("Tag", ""));
    }
  });
  return tags;
}

function createBadge(tag) {
  const colors = {
    uxui: "bg-secondary",
    architecture: "bg-dark",
    frontend: "bg-info",
    backend: "bg-warning text-dark",
    testing: "bg-success",
    deployment: "bg-primary"
  };
  return `<span class="badge ${colors[tag] || "bg-secondary"} me-1">${capitalize(tag)}</span>`;
}

function capitalize(word) {
  return word.charAt(0).toUpperCase() + word.slice(1);
}

function createTaskCard(title, description, priority, dueDate, tags) {
  const taskCard = document.createElement("div");
  taskCard.className = "kanban-item";
  taskCard.draggable = true;
  taskCard.id = `task-${Date.now()}`;
  taskCard.dataset.priority = priority;
  taskCard.dataset.dueDate = dueDate;
  taskCard.dataset.tags = tags.join(",");

  taskCard.innerHTML = `
    <div class="task-title">${title}</div>
    <div class="task-description">${description}</div>
    <div class="priority ${priority}">${priority.toUpperCase()} PRIORITY</div>
    <div class="due-date">Due: ${dueDate}</div>
    <div class="task-tags">${tags.map(tag => createBadge(tag)).join(" ")}</div>
    <div class="task-actions mt-2">
      <button class="btn btn-sm btn-primary edit-btn"><i class="bi bi-pencil"></i> Edit</button>
      <button class="btn btn-sm btn-danger delete-btn"><i class="bi bi-trash"></i> Delete</button>
    </div>
  `;

  taskCard.addEventListener("dragstart", function (e) {
    e.dataTransfer.setData("text/plain", taskCard.id);
    taskCard.style.opacity = "0.4";
  });

  return taskCard;
}

function addTaskEventListeners(taskCard) {
  taskCard.querySelector(".edit-btn").addEventListener("click", () => openEditModal(taskCard));
  taskCard.querySelector(".delete-btn").addEventListener("click", () => {
    if (confirm("Are you sure you want to delete this task?")) {
      taskCard.remove();
      saveTasksToLocalStorage();
    }
  });
}

function openEditModal(taskCard) {
  currentTaskCard = taskCard;
  const tags = (taskCard.dataset.tags || "").split(",");

  document.getElementById("edit-task-title").value = taskCard.querySelector(".task-title").textContent;
  document.getElementById("edit-task-description").value = taskCard.querySelector(".task-description").textContent;
  document.getElementById("edit-task-priority").value = taskCard.dataset.priority;
  document.getElementById("edit-task-due-date").value = taskCard.dataset.dueDate;

  ["uxui", "architecture", "frontend", "backend", "testing", "deployment"].forEach((tag) => {
    document.getElementById(`edit-${tag}Tag`).checked = tags.includes(tag);
  });

  editTaskModal.show();
}

function clearForm() {
  document.getElementById("taskTitle").value = "";
  document.getElementById("task-description").value = "";
  document.getElementById("taskPriority").value = "medium";
  document.getElementById("taskDate").value = "";

  ["uxuiTag", "architectureTag", "frontendTag", "backendTag", "testingTag", "deploymentTag"].forEach((id) => {
    const el = document.getElementById(id);
    if (el) el.checked = false;
  });
}

function saveTasksToLocalStorage() {
  const tasks = [];
  document.querySelectorAll(".kanban-column").forEach((column) => {
    const columnId = column.id;
    column.querySelectorAll(".kanban-item").forEach((task) => {
      tasks.push({
        id: task.id,
        title: task.querySelector(".task-title").textContent,
        description: task.querySelector(".task-description").textContent,
        priority: task.dataset.priority,
        dueDate: task.dataset.dueDate,
        tags: (task.dataset.tags || "").split(","),
        column: columnId,
      });
    });
  });
  localStorage.setItem("kanbanTasks", JSON.stringify(tasks));
}

function loadTasksFromLocalStorage() {
  const saved = JSON.parse(localStorage.getItem("kanbanTasks")) || [];
  saved.forEach((task) => {
    const taskCard = createTaskCard(
      task.title,
      task.description,
      task.priority,
      task.dueDate,
      task.tags || []
    );
    taskCard.id = task.id;
    document.getElementById(task.column).appendChild(taskCard);
    addTaskEventListeners(taskCard);
  });
}