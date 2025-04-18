// static/js/scripts.js
function toggleSidebar() {
    let sidebar = document.querySelector(".sidebar");
    sidebar.classList.toggle("active");
}

function displayNepalTime() {
    const nepalTimeElement = document.getElementById("nepal-time");
    
    function updateTime() {
        const now = new Date();
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
        
        if (nepalTimeElement) {
            nepalTimeElement.textContent = `Nepal Time: ${formattedDate}, ${formattedTime}`;
        }
    }
    
    updateTime();
    setInterval(updateTime, 1000);
}

document.addEventListener("DOMContentLoaded", function () {
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
    const forgotPasswordForm = document.getElementById("forgot-password-form");
    const loginForm = document.getElementById("login-form");
    const signupForm = document.getElementById("signup-form");
    const showSignup = document.getElementById("show-signup");
    const showLogin = document.getElementById("show-login");
    const searchForm = document.getElementById("search-form");
    const searchIcon = document.querySelector(".search-icon");

    if (userIcon) {
        userIcon.addEventListener("click", function () {
            if (authModal) authModal.classList.remove("hidden");
        });
    }

    if (closeModal) {
        closeModal.addEventListener("click", function () {
            if (authModal) authModal.classList.add("hidden");
        });
    }

    if (closeForgotPassword) {
        closeForgotPassword.addEventListener("click", function () {
            if (forgotPasswordModal) forgotPasswordModal.classList.add("hidden");
        });
    }

    if (forgotPasswordBtn) {
        forgotPasswordBtn.addEventListener("click", function () {
            if (authModal) authModal.classList.add("hidden");
            if (forgotPasswordModal) forgotPasswordModal.classList.remove("hidden");
        });
    }

    if (showSignup) {
        showSignup.addEventListener("click", function (e) {
            e.preventDefault();
            if (loginForm) loginForm.classList.add("hidden");
            if (signupForm) signupForm.classList.remove("hidden");
        });
    }

    if (showLogin) {
        showLogin.addEventListener("click", function (e) {
            e.preventDefault();
            if (signupForm) signupForm.classList.add("hidden");
            if (loginForm) loginForm.classList.remove("hidden");
        });
    }

    // Handle Forgot Password Form Submission
    if (forgotPasswordForm) {
        forgotPasswordForm.addEventListener("submit", function (e) {
            e.preventDefault();
            // Remove any existing error/success messages
            const existingMessage = forgotPasswordForm.querySelector('.form-message');
            if (existingMessage) existingMessage.remove();

            const formData = new FormData(forgotPasswordForm);
            fetch(forgotPasswordForm.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': document.querySelector('input[name="csrfmiddlewaretoken"]').value
                }
            })
            .then(response => response.json())
            .then(data => {
                const messageDiv = document.createElement('div');
                messageDiv.className = `form-message ${data.status === 'success' ? 'success' : 'error'}`;
                messageDiv.textContent = data.message;
                forgotPasswordForm.appendChild(messageDiv);
                if (data.status === 'success') {
                    setTimeout(() => {
                        if (forgotPasswordModal) forgotPasswordModal.classList.add("hidden");
                    }, 2000);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                const messageDiv = document.createElement('div');
                messageDiv.className = 'form-message error';
                messageDiv.textContent = "An error occurred while communicating with the server.";
                forgotPasswordForm.appendChild(messageDiv);
            });
        });
    }

    window.addEventListener("click", function (e) {
        if (e.target === authModal) {
            if (authModal) authModal.classList.add("hidden");
        }
        if (e.target === forgotPasswordModal) {
            if (forgotPasswordModal) forgotPasswordModal.classList.add("hidden");
        }
    });

    if (searchIcon) {
        searchIcon.addEventListener("click", function () {
            if (searchForm) searchForm.submit();
        });
    }

    if (searchForm) {
        searchForm.addEventListener("submit", function (e) {
            const searchInput = document.querySelector(".search-input");
            if (!searchInput.value.trim()) {
                e.preventDefault();
                alert("Please enter a search query.");
            }
        });
    }
});

function openAuthModal() {
    const authModal = document.getElementById("auth-modal");
    if (authModal) authModal.classList.remove("hidden");
}

function closeAuthModal() {
    const authModal = document.getElementById("auth-modal");
    if (authModal) authModal.classList.add("hidden");
}

function closeForgotPasswordModal() {
    const forgotPasswordModal = document.getElementById("forgot-password-modal");
    if (forgotPasswordModal) forgotPasswordModal.classList.add("hidden");
}