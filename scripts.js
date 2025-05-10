<<<<<<< HEAD
// Toggles the sidebar open/close state by toggling the "active" class
=======
>>>>>>> origin/main
function toggleSidebar() {
    let sidebar = document.querySelector(".sidebar");
    sidebar.classList.toggle("active");
}

<<<<<<< HEAD
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
=======

>>>>>>> origin/main
document.addEventListener("DOMContentLoaded", function () {
    let currentLocation = window.location.pathname.split("/").pop() || "index.html"; // Default to home page
    let navLinks = document.querySelectorAll(".navbar a");

    navLinks.forEach(link => {
        if (link.getAttribute("href") === currentLocation) {
            link.classList.add("active"); // Add active class to current page link
        }
    });
});
<<<<<<< HEAD
=======

document.addEventListener("DOMContentLoaded", function () {
    const userIcon = document.querySelector(".user");
    const authModal = document.getElementById("auth-modal");
    const closeModal = document.getElementById("close-modal");
    const loginForm = document.getElementById("login-form");
    const signupForm = document.getElementById("signup-form");
    const showSignup = document.getElementById("show-signup");
    const showLogin = document.getElementById("show-login");

    // Show modal when user icon is clicked
    userIcon.addEventListener("click", function () {
        authModal.classList.remove("hidden");
    });

    // Close modal when close button is clicked
    closeModal.addEventListener("click", function () {
        authModal.classList.add("hidden");
    });

    // Toggle between login and signup forms
    showSignup.addEventListener("click", function (e) {
        e.preventDefault();
        loginForm.classList.add("hidden");
        signupForm.classList.remove("hidden");
    });

    showLogin.addEventListener("click", function (e) {
        e.preventDefault();
        signupForm.classList.add("hidden");
        loginForm.classList.remove("hidden");
    });

    // Close modal when clicking outside the form
    window.addEventListener("click", function (e) {
        if (e.target === authModal) {
            authModal.classList.add("hidden");
        }
    });
});


document.addEventListener("DOMContentLoaded", function () {
    const userIcon = document.querySelector(".user");
    const authModal = document.getElementById("auth-modal");
    const forgotPasswordModal = document.getElementById("forgot-password-modal");
    const closeModal = document.getElementById("close-modal");
    const closeForgotPassword = document.getElementById("close-forgot-password");
    const forgotPasswordBtn = document.getElementById("forgot-password-btn");

    // Open Login Modal
    userIcon.addEventListener("click", function () {
        authModal.classList.remove("hidden");
    });

    // Close Login Modal
    closeModal.addEventListener("click", function () {
        authModal.classList.add("hidden");
    });

    // Open Forgot Password Modal
    forgotPasswordBtn.addEventListener("click", function () {
        authModal.classList.add("hidden"); // Close login modal
        forgotPasswordModal.classList.remove("hidden"); // Open forgot password modal
    });

    // Close Forgot Password Modal
    closeForgotPassword.addEventListener("click", function () {
        forgotPasswordModal.classList.add("hidden");
    });

    // Close modal when clicking outside
    window.addEventListener("click", function (e) {
        if (e.target === authModal) {
            authModal.classList.add("hidden");
        }
        if (e.target === forgotPasswordModal) {
            forgotPasswordModal.classList.add("hidden");
        }
    });
});

// Function to search news
function searchNews() {
    const searchInput = document.querySelector('.search-input').value.toLowerCase();
    const newsItems = document.querySelectorAll('.news-item');
    let found = false;

    // Loop through all news items and check if they match the search input
    newsItems.forEach(item => {
        const text = item.textContent.toLowerCase();
        if (text.includes(searchInput)) {
            item.style.display = "block"; // Show matching item
            found = true;
        } else {
            item.style.display = "none"; // Hide non-matching item
        }
    });

    // Show "No results found" if no matches
    const noResults = document.querySelector('.no-results');
    if (!found) {
        if (!noResults) {
            const noResultsDiv = document.createElement('div');
            noResultsDiv.classList.add('no-results');
            noResultsDiv.textContent = 'No results found';
            document.querySelector('.news-container').appendChild(noResultsDiv);
        }
    } else {
        const existingNoResults = document.querySelector('.no-results');
        if (existingNoResults) {
            existingNoResults.remove(); // Remove "No results found" if results appear
        }
    }
}

// Event listener for the search input
document.querySelector('.search-input').addEventListener('input', searchNews);
>>>>>>> origin/main
