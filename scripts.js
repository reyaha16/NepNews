// Toggles the sidebar open/close state by toggling the "active" class
function toggleSidebar() {
    let sidebar = document.querySelector(".sidebar");
    sidebar.classList.toggle("active");
}

// Adds a "sticky" class to the header when scrolling down
window.addEventListener('scroll', function() {
    const header = document.querySelector('header');
    if (window.scrollY > 0) {
      header.classList.add('sticky');
    } else {
      header.classList.remove('sticky');
    }
  });
// Highlights the current page link in the navbar
document.addEventListener("DOMContentLoaded", function () {
    let currentLocation = window.location.pathname.split("/").pop() || "index.html"; // Default to home page
    let navLinks = document.querySelectorAll(".navbar a");

    navLinks.forEach(link => {
        if (link.getAttribute("href") === currentLocation) {
            link.classList.add("active"); // Add active class to current page link
        }
    });
});
