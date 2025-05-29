document.addEventListener("DOMContentLoaded", function () {
    const toggleBtn = document.getElementById("toggleBtn");
    const sidebar = document.getElementById("sidebar");
    const mainContent = document.getElementById("mainContent");
    const mobileMenuBtn = document.getElementById("mobileMenuBtn");

    if (toggleBtn) {
        toggleBtn.addEventListener("click", function () {
            sidebar.classList.toggle("collapsed");
            mainContent.classList.toggle("expanded");

            const icon = toggleBtn.querySelector("i");
            if (sidebar.classList.contains("collapsed")) {
                icon.classList.remove("bi-chevron-left");
                icon.classList.add("bi-chevron-right");
            } else {
                icon.classList.remove("bi-chevron-right");
                icon.classList.add("bi-chevron-left");
            }
        });
    }

    if (mobileMenuBtn) {
        mobileMenuBtn.addEventListener("click", function () {
            sidebar.classList.toggle("show");
        });
    }

    document.addEventListener("click", function (event) {
        if (
            window.innerWidth <= 768 &&
            !sidebar.contains(event.target) &&
            event.target !== mobileMenuBtn
        ) {
            sidebar.classList.remove("show");
        }
    });

    window.addEventListener("load", function () {
        if (window.innerWidth <= 768) {
            sidebar.classList.remove("collapsed");
            sidebar.classList.remove("show");
            mainContent.classList.remove("expanded");
        }
    });

    window.addEventListener("resize", function () {
        if (window.innerWidth > 768) {
            sidebar.classList.remove("show");
        }
    });
});
