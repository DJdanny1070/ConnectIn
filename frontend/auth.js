// Authentication module
const Auth = {
    init: () => {
        document.getElementById('loginBtn')?.addEventListener('click', () => Auth.showLoginModal());
        document.getElementById('signupBtn')?.addEventListener('click', () => Auth.showSignupModal());
        document.getElementById('logoutBtn')?.addEventListener('click', () => API.auth.logout());
        
        // Check if user is logged in
        Auth.checkAuthState();
    },
    
    checkAuthState: () => {
        const token = API.getToken();
        const user = JSON.parse(localStorage.getItem(CONFIG.STORAGE_KEYS.USER) || 'null');
        
        if (token && user) {
            Auth.showAuthenticatedUI(user);
        } else {
            Auth.showGuestUI();
        }
    },
    
    showAuthenticatedUI: (user) => {
        document.getElementById('navActions').style.display = 'none';
        document.getElementById('navUser').style.display = 'flex';
        document.getElementById('userAvatar').src = Utils.getAvatarUrl(user.name, user.profile_image);
    },
    
    showGuestUI: () => {
        document.getElementById('navActions').style.display = 'flex';
        document.getElementById('navUser').style.display = 'none';
    },
    
    showLoginModal: () => {
        const modal = `
            <div class="modal" id="loginModal">
                <div class="modal-content">
                    <div class="modal-header">
                        <h2 class="modal-title">Login</h2>
                        <span class="modal-close" onclick="closeModal('loginModal')">&times;</span>
                    </div>
                    <div class="modal-body">
                        <form id="loginForm">
                            <div class="form-group">
                                <label class="form-label">Email</label>
                                <input type="email" class="form-control" name="email" required>
                            </div>
                            <div class="form-group">
                                <label class="form-label">Password</label>
                                <input type="password" class="form-control" name="password" required>
                            </div>
                            <button type="submit" class="btn btn-primary btn-lg" style="width: 100%">Login</button>
                        </form>
                        <p class="mt-2 text-center">Don't have an account? <a href="#" onclick="closeModal('loginModal'); Auth.showSignupModal();" style="color: var(--primary)">Sign up</a></p>
                    </div>
                </div>
            </div>
        `;
        
        document.getElementById('modalContainer').innerHTML = modal;
        
        document.getElementById('loginForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(e.target);
            const credentials = Object.fromEntries(formData);
            
            try {
                const response = await API.auth.login(credentials);
                localStorage.setItem(CONFIG.STORAGE_KEYS.TOKEN, response.access_token);
                localStorage.setItem(CONFIG.STORAGE_KEYS.USER, JSON.stringify(response.user));
                
                Utils.showToast('Login successful!', 'success');
                closeModal('loginModal');
                Auth.checkAuthState();
                
                // Navigate to dashboard
                if (response.user.user_type === 'freelancer') {
                    navigateTo('dashboard');
                } else {
                    navigateTo('dashboard');
                }
            } catch (error) {
                Utils.showToast(error.message, 'error');
            }
        });
    },
    
    showSignupModal: (userType = null) => {
        const modal = `
            <div class="modal" id="signupModal">
                <div class="modal-content">
                    <div class="modal-header">
                        <h2 class="modal-title">Create Account</h2>
                        <span class="modal-close" onclick="closeModal('signupModal')">&times;</span>
                    </div>
                    <div class="modal-body">
                        <form id="signupForm">
                            <div class="form-group">
                                <label class="form-label">I want to</label>
                                <select class="form-control form-select" name="user_type" required>
                                    <option value="">Select...</option>
                                    <option value="freelancer" ${userType === 'freelancer' ? 'selected' : ''}>Find Work (Freelancer)</option>
                                    <option value="employer" ${userType === 'employer' ? 'selected' : ''}>Hire Talent (Employer)</option>
                                </select>
                            </div>
                            <div class="form-group">
                                <label class="form-label">Full Name</label>
                                <input type="text" class="form-control" name="name" required>
                            </div>
                            <div class="form-group">
                                <label class="form-label">Email</label>
                                <input type="email" class="form-control" name="email" required>
                            </div>
                            <div class="form-group">
                                <label class="form-label">Phone</label>
                                <input type="tel" class="form-control" name="phone" placeholder="+91-9876543210">
                            </div>
                            <div class="form-group">
                                <label class="form-label">Location</label>
                                <input type="text" class="form-control" name="location" placeholder="City, State">
                            </div>
                            <div class="form-group">
                                <label class="form-label">Password</label>
                                <input type="password" class="form-control" name="password" required minlength="6">
                            </div>
                            <button type="submit" class="btn btn-primary btn-lg" style="width: 100%">Sign Up</button>
                        </form>
                        <p class="mt-2 text-center">Already have an account? <a href="#" onclick="closeModal('signupModal'); Auth.showLoginModal();" style="color: var(--primary)">Login</a></p>
                    </div>
                </div>
            </div>
        `;
        
        document.getElementById('modalContainer').innerHTML = modal;
        
        document.getElementById('signupForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(e.target);
            const userData = Object.fromEntries(formData);
            
            if (!Utils.validateEmail(userData.email)) {
                Utils.showToast('Please enter a valid email', 'error');
                return;
            }
            
            try {
                const response = await API.auth.register(userData);
                localStorage.setItem(CONFIG.STORAGE_KEYS.TOKEN, response.access_token);
                localStorage.setItem(CONFIG.STORAGE_KEYS.USER, JSON.stringify(response.user));
                
                Utils.showToast('Account created successfully!', 'success');
                closeModal('signupModal');
                Auth.checkAuthState();
                
                // Show profile setup for freelancers
                if (response.user.user_type === 'freelancer') {
                    Profile.showSetupModal();
                } else {
                    navigateTo('dashboard');
                }
            } catch (error) {
                Utils.showToast(error.message, 'error');
            }
        });
    }
};

// Helper functions
function closeModal(modalId) {
    document.getElementById(modalId)?.remove();
}

function showSignupModal(userType) {
    Auth.showSignupModal(userType);
}
