function toggleSidebar() {
    let sidebar = document.querySelector(".sidebar");
    sidebar.classList.toggle("active");
}

// Function to display Nepal time (UTC+5:45)
function displayNepalTime() {
    const nepalTimeElement = document.getElementById("nepal-time");
    
    function updateTime() {
        const now = new Date();
        // Format the time and date for Nepal
        const options = {
            timeZone: "Asia/Kathmandu",
            hour: "2-digit",
            minute: "2-digit",
            second: "2-digit",
            hour12: true
        };
        const formattedTime = now.toLocaleTimeString("en-US", options);
        const formattedDate = now.toLocaleDateString("en-US", {
            timeZone: "Asia/Kathmandu",
            weekday: "long",
            year: "numeric",
            month: "long",
            day: "numeric"
        });
        
        nepalTimeElement.textContent = `Nepal Time: ${formattedDate}, ${formattedTime}`;
    }
    
    // Update time immediately and then every second
    updateTime();
    setInterval(updateTime, 1000);
}

document.addEventListener("DOMContentLoaded", function () {
    // Initialize Nepal time display
    displayNepalTime();

    let currentLocation = window.location.pathname.split("/").pop() || "index.html";
    let navLinks = document.querySelectorAll(".navbar a");

    navLinks.forEach(link => {
        if (link.getAttribute("href") === currentLocation) {
            link.classList.add("active");
        }
    });

    const userIcon = document.querySelector(".user");
    const authModal = document.getElementById("auth-modal");
    const forgotPasswordModal = document.getElementById("forgot-password-modal");
    const closeModal = document.getElementById("close-modal");
    const closeForgotPassword = document.getElementById("close-forgot-password");
    const forgotPasswordBtn = document.getElementById("forgot-password-btn");
    const loginForm = document.getElementById("login-form");
    const signupForm = document.getElementById("signup-form");
    const showSignup = document.getElementById("show-signup");
    const showLogin = document.getElementById("show-login");

    if (userIcon) {
        userIcon.addEventListener("click", function () {
            authModal.classList.remove("hidden");
        });
    }

    if (closeModal) {
        closeModal.addEventListener("click", function () {
            authModal.classList.add("hidden");
        });
    }

    if (closeForgotPassword) {
        closeForgotPassword.addEventListener("click", function () {
            forgotPasswordModal.classList.add("hidden");
        });
    }

    if (forgotPasswordBtn) {
        forgotPasswordBtn.addEventListener("click", function () {
            authModal.classList.add("hidden");
            forgotPasswordModal.classList.remove("hidden");
        });
    }

    if (showSignup) {
        showSignup.addEventListener("click", function (e) {
            e.preventDefault();
            loginForm.classList.add("hidden");
            signupForm.classList.remove("hidden");
        });
    }

    if (showLogin) {
        showLogin.addEventListener("click", function (e) {
            e.preventDefault();
            signupForm.classList.add("hidden");
            loginForm.classList.remove("hidden");
        });
    }

    window.addEventListener("click", function (e) {
        if (e.target === authModal) {
            authModal.classList.add("hidden");
        }
        if (e.target === forgotPasswordModal) {
            forgotPasswordModal.classList.add("hidden");
        }
    });
});

function openAuthModal() {
    document.getElementById("auth-modal").classList.remove("hidden");
}

function closeAuthModal() {
    document.getElementById("auth-modal").classList.add("hidden");
}

function closeForgotPasswordModal() {
    document.getElementById("forgot-password-modal").classList.add("hidden");
}