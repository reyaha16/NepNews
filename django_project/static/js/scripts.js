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

    const userIcon = document.getElementById("user-icon");
    const authModal = document.getElementById("auth-modal");
    const forgotPasswordModal = document.getElementById("forgot-password-modal");
    const closeModal = document.getElementById("close-modal");
    const closeForgotPassword = document.getElementById("close-forgot-password");
    const forgotPasswordBtn = document.getElementById("forgot-password-btn");
    const forgotPasswordForm = document.getElementById("forgot-password-form");
    const loginForm = document.getElementById("login-form").querySelector("form");
    const signupForm = document.getElementById("signup-form").querySelector("form");
    const loginFormContainer = document.getElementById("login-form");
    const signupFormContainer = document.getElementById("signup-form");
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
            if (loginFormContainer) loginFormContainer.classList.add("hidden");
            if (signupFormContainer) signupFormContainer.classList.remove("hidden");
        });
    }

    if (showLogin) {
        showLogin.addEventListener("click", function (e) {
            e.preventDefault();
            if (signupFormContainer) signupFormContainer.classList.add("hidden");
            if (loginFormContainer) loginFormContainer.classList.remove("hidden");
        });
    }

    // Login form submission handling
    if (loginForm) {
        loginForm.addEventListener("submit", function(e) {
            // We don't prevent default here to allow the normal form submission
            // which will redirect to the login URL
            console.log("Login form submitted");
            // The form will naturally submit to the action URL
        });
    }

    // Signup form submission handling
    if (signupForm) {
        signupForm.addEventListener("submit", function(e) {
            // We don't prevent default here to allow the normal form submission
            // which will redirect to the signup URL
            console.log("Signup form submitted");
            // The form will naturally submit to the action URL
        });
    }

    if (forgotPasswordForm) {
        forgotPasswordForm.addEventListener("submit", function (e) {
            e.preventDefault();
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
            authModal.classList.add("hidden");
        }
        if (e.target === forgotPasswordModal) {
            forgotPasswordModal.classList.add("hidden");
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

    // Like Button Functionality
    const likeButtons = document.querySelectorAll(".like-btn");
    if (likeButtons.length === 0) {
        console.log("No like buttons found on the page.");
    }
    likeButtons.forEach(button => {
        button.addEventListener("click", function () {
            const postId = this.getAttribute("data-post-id");
            if (!postId) {
                console.error("Post ID not found on like button.");
                return;
            }
            fetch(`/post/${postId}/like/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': document.querySelector('input[name="csrfmiddlewaretoken"]').value,
                    'Content-Type': 'application/json'
                }
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                if (data.error) {
                    console.error('Server error:', data.error);
                    alert('Error: ' + data.error);
                    return;
                }
                this.textContent = data.liked ? `Unlike (${data.like_count})` : `Like (${data.like_count})`;
            })
            .catch(error => {
                console.error('Error during like request:', error);
                alert('An error occurred while liking the post. Please try again.');
            });
        });
    });

    // Bookmark Button Functionality
    const bookmarkButtons = document.querySelectorAll(".bookmark-btn");
    if (bookmarkButtons.length === 0) {
        console.log("No bookmark buttons found on the page.");
    }
    bookmarkButtons.forEach(button => {
        button.addEventListener("click", function () {
            const postId = this.getAttribute("data-post-id");
            if (!postId) {
                console.error("Post ID not found on bookmark button.");
                return;
            }
            fetch(`/post/${postId}/bookmark/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': document.querySelector('input[name="csrfmiddlewaretoken"]').value,
                    'Content-Type': 'application/json'
                }
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                if (data.error) {
                    console.error('Server error:', data.error);
                    alert('Error: ' + data.error);
                    return;
                }
                this.textContent = data.bookmarked ? 'Remove Bookmark' : 'Bookmark';
            })
            .catch(error => {
                console.error('Error during bookmark request:', error);
                alert('An error occurred while bookmarking the post. Please try again.');
            });
        });
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

    const forgotPasswordModal = document.getElementById("forgot-password-modal");
    if (forgotPasswordModal) forgotPasswordModal.classList.add("hidden");

document.addEventListener("DOMContentLoaded", function () {
    const scrollToTopBtn = document.getElementById("scrollToTopBtn");

    if (scrollToTopBtn) {
        scrollToTopBtn.addEventListener("click", function () {
            window.scrollTo({
                top: 0,
                behavior: "smooth"
            });
        });
    }

    window.addEventListener("scroll", function () {
        // Progress bar
        const winScroll = document.documentElement.scrollTop || document.body.scrollTop;
        const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
        const scrolled = (winScroll / height) * 100;
        const progressBar = document.getElementById("progressBar");
        if (progressBar) {
            progressBar.style.width = `${scrolled}%`;
        }

        // Scroll-to-top button visibility
        if (scrollToTopBtn) {
            if (winScroll > 300) {
                scrollToTopBtn.classList.add("show");
            } else {
                scrollToTopBtn.classList.remove("show");
            }
        }
    });
});

document.addEventListener('keydown', function(event) {
    // Prevent shortcuts when typing in input or textarea fields
    const activeElement = document.activeElement;
    if (activeElement.tagName === 'INPUT' || activeElement.tagName === 'TEXTAREA') {
        return;
    }

    // L: Open login modal or go to profile
    if (event.key.toLowerCase() === 'l') {
        event.preventDefault();
        const userIcon = document.getElementById('user-icon');
        const profileLink = document.querySelector('.user[href*="profile-page"]');
        if (userIcon) {
            document.getElementById("auth-modal").classList.remove("hidden");
        } else if (profileLink) {
            window.location.href = profileLink.href;
        }
    }

    // U: Open signup modal
    if (event.key.toLowerCase() === 'u') {
        event.preventDefault();
        const userIcon = document.getElementById('user-icon');
        if (userIcon) {
            const authModal = document.getElementById("auth-modal");
            authModal.classList.remove("hidden");
            const showSignupLink = document.getElementById('show-signup');
            if (showSignupLink) {
                showSignupLink.click();
            }
        }
    }

    // M: Toggle sidebar
    if (event.key.toLowerCase() === 'm') {
        event.preventDefault();
        const sidebar = document.querySelector('.sidebar');
        if (sidebar) {
            sidebar.classList.toggle('active');
        }
    }

    // Esc: Close modals
    if (event.key === 'Escape') {
        const authModal = document.getElementById('auth-modal');
        const forgotPasswordModal = document.getElementById('forgot-password-modal');
        if (authModal && !authModal.classList.contains('hidden')) {
            authModal.classList.add("hidden");
        }
        if (forgotPasswordModal && !forgotPasswordModal.classList.contains('hidden')) {
            forgotPasswordModal.classList.add("hidden");
        }
    }

    // H: Go to homepage
    if (event.key.toLowerCase() === 'h') {
        event.preventDefault();
        const homeLink = document.querySelector('nav.navbar a[href*="/"]');
        if (homeLink) {
            window.location.href = homeLink.href;
        }
    }

    // N: Go to new post page (for writers)
    if (event.key.toLowerCase() === 'n') {
        event.preventDefault();
        const newPostLink = document.querySelector('.sidebar a[href*="/new-post"]');
        if (newPostLink) {
            window.location.href = newPostLink.href;
        }
    }

    // A: Go to about page
    if (event.key.toLowerCase() === 'a') {
        event.preventDefault();
        const aboutLink = document.querySelector('footer a[href*="/about"]');
        if (aboutLink) {
            window.location.href = aboutLink.href;
        }
    }

    // C: Go to contact page
    if (event.key.toLowerCase() === 'c') {
        event.preventDefault();
        const contactLink = document.querySelector('footer a[href*="/contact"]');
        if (contactLink) {
            window.location.href = contactLink.href;
        }
    }

    // P: Go to privacy policy page
    if (event.key.toLowerCase() === 'p') {
        event.preventDefault();
        const privacyLink = document.querySelector('footer a[href*="/privacy-policy"]');
        if (privacyLink) {
            window.location.href = privacyLink.href;
        }
    }

    // T: Go to terms of service page
    if (event.key.toLowerCase() === 't') {
        event.preventDefault();
        const termsLink = document.querySelector('footer a[href*="/terms"]');
        if (termsLink) {
            window.location.href = termsLink.href;
        }
    }

    // O: Scroll to top
    if (event.key.toLowerCase() === 'o') {
        event.preventDefault();
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    // B: Scroll to bottom
    if (event.key.toLowerCase() === 'b') {
        event.preventDefault();
        window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' });
    }
});

