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
  document.querySelectorAll('.view-gantt-btn').forEach(btn => {
    btn.addEventListener('click', function () {
      const projectName = this.getAttribute('data-project-name');
      const progress = this.getAttribute('data-progress');

      // Update modal content
      document.getElementById('ganttModalLabel').textContent = `Gantt Chart: ${projectName}`;
      document.getElementById('ganttProjectTitle').innerHTML = `<strong>Project:</strong> ${projectName}`;
      document.getElementById('ganttProgressBar').style.width = `${progress}%`;
      document.getElementById('ganttProgressBar').textContent = `${progress}%`;
      document.getElementById('ganttProgressPercent').innerHTML = `<strong>Progress:</strong> ${progress}% Completed`;

      const ganttModal = new bootstrap.Modal(document.getElementById('ganttModal'));
      ganttModal.show();
    });
  });

});
