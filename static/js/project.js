document.addEventListener("DOMContentLoaded", function () {
  
  // Filters
  document.getElementById("statusFilter").addEventListener("change", filterProjects);
  document.getElementById("userFilter").addEventListener("change", filterProjects);

  function filterProjects() {
    const status = document.getElementById("statusFilter").value;
    const user = document.getElementById("userFilter").value;

    const rows = document.querySelectorAll("#projectTableBody tr");
    rows.forEach(row => {
      const rowStatus = row.querySelector(".badge").textContent.toLowerCase().replace(" ", "-");
      const rowUser = row.dataset.user;

      const matchStatus = status === "all" || rowStatus === status;
      const matchUser = user === "all" || rowUser === user;

      row.style.display = (matchStatus && matchUser) ? "" : "none";
    });
  }

  // Gantt Chart Modal
// Gantt Chart Modal
document.querySelectorAll('.view-gantt-btn').forEach(btn => {
  btn.addEventListener('click', function () {
    const projectName = this.getAttribute('data-project-name');
    const progress = this.getAttribute('data-progress');
    const tasks = JSON.parse(this.getAttribute('data-tasks'));

    // Update modal header
    document.getElementById('ganttModalLabel').textContent = `Gantt Chart: ${projectName}`;
    document.getElementById('ganttProjectTitle').innerHTML = `<strong>Project:</strong> ${projectName}`;
    document.getElementById('ganttProgressBar').style.width = `${progress}%`;
    document.getElementById('ganttProgressBar').textContent = `${progress}%`;
    document.getElementById('ganttProgressPercent').innerHTML = `<strong>Progress:</strong> ${progress}% Completed`;

    // Create visual breakdown of tasks
    let taskHtml = '';
    tasks.forEach(task => {
      taskHtml += `
        <div class="mt-3">
          <strong>${task.title}</strong> (Due: ${task.due})<br>
          <div class="progress mt-1" style="height: 12px;">
            <div class="progress-bar bg-info" style="width: ${task.progress}%;">
              ${task.progress}%
            </div>
          </div>
        </div>
      `;
    });

    document.getElementById('ganttProgressPercent').innerHTML += taskHtml;

    // Show modal
    const ganttModal = new bootstrap.Modal(document.getElementById('ganttModal'));
    ganttModal.show();
  });
});


});
