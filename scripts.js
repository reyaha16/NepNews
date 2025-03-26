function toggleSidebar() {
    let sidebar = document.querySelector(".sidebar");
    sidebar.classList.toggle("active");
}


document.addEventListener("DOMContentLoaded", function () {
    let currentLocation = window.location.pathname.split("/").pop() || "index.html"; // Default to home page
    let navLinks = document.querySelectorAll(".navbar a");

    navLinks.forEach(link => {
        if (link.getAttribute("href") === currentLocation) {
            link.classList.add("active"); // Add active class to current page link
        }
    });
});
