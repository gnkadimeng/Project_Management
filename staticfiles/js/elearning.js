document.addEventListener("DOMContentLoaded", function () {
    // Sidebar toggle
    const toggleBtn = document.getElementById("toggleBtn");
    const sidebar = document.getElementById("sidebar");
    const mainContent = document.getElementById("mainContent");
    const mobileMenuBtn = document.getElementById("mobileMenuBtn");

    if (toggleBtn) {
        toggleBtn.addEventListener("click", function () {
            sidebar.classList.toggle("collapsed");
            mainContent.classList.toggle("expanded");

            const icon = toggleBtn.querySelector("i");
            icon.classList.toggle("bi-chevron-left");
            icon.classList.toggle("bi-chevron-right");
        });
    }

    if (mobileMenuBtn) {
        mobileMenuBtn.addEventListener("click", function () {
            sidebar.classList.toggle("show");
        });
    }

    document.addEventListener("click", function (e) {
        if (window.innerWidth <= 768 && !sidebar.contains(e.target) && e.target !== mobileMenuBtn) {
            sidebar.classList.remove("show");
        }
    });

    window.addEventListener("resize", function () {
        if (window.innerWidth > 768) {
            sidebar.classList.remove("show");
        }
    });

    //FILTER FUNCTION
    const chips = document.querySelectorAll(".filter-chip");
    const cards = document.querySelectorAll(".resource-item");

    chips.forEach(chip => {
        chip.addEventListener("click", function () {
            chips.forEach(c => c.classList.remove("active"));
            this.classList.add("active");

            const selected = this.textContent.trim().toLowerCase();

            cards.forEach(card => {
                const type = card.dataset.type.trim().toLowerCase();
                if (selected === 'all' || selected === type) {
                    card.style.display = "block";
                } else {
                    card.style.display = "none";
                }
            });
        });
    });
});
