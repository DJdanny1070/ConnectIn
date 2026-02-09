// API Service - Handles all communication with the backend
const API = {
    // Get auth token from localStorage
    getToken: () => {
        return localStorage.getItem(CONFIG.STORAGE_KEYS.TOKEN);
    },
    
    // Get auth headers
    getHeaders: (includeAuth = true) => {
        const headers = {
            'Content-Type': 'application/json'
        };
        
        if (includeAuth) {
            const token = API.getToken();
            if (token) {
                headers['Authorization'] = `Bearer ${token}`;
            }
        }
        
        return headers;
    },
    
    // Generic request handler
    request: async (endpoint, options = {}) => {
        try {
            const url = `${CONFIG.API_BASE_URL}${endpoint}`;
            const response = await fetch(url, {
                ...options,
                headers: {
                    ...API.getHeaders(options.auth !== false),
                    ...options.headers
                }
            });
            
            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.error || 'Request failed');
            }
            
            return data;
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    },
    
    // Authentication
    auth: {
        register: (userData) => {
            return API.request('/register', {
                method: 'POST',
                body: JSON.stringify(userData),
                auth: false
            });
        },
        
        login: (credentials) => {
            return API.request('/login', {
                method: 'POST',
                body: JSON.stringify(credentials),
                auth: false
            });
        },
        
        getProfile: () => {
            return API.request('/profile');
        },
        
        logout: () => {
            localStorage.removeItem(CONFIG.STORAGE_KEYS.TOKEN);
            localStorage.removeItem(CONFIG.STORAGE_KEYS.USER);
            window.location.href = '/';
        }
    },
    
    // Freelancer Profile
    freelancer: {
        createProfile: (profileData) => {
            return API.request('/freelancer/profile', {
                method: 'POST',
                body: JSON.stringify(profileData)
            });
        },
        
        updateProfile: (profileData) => {
            return API.request('/freelancer/profile', {
                method: 'PUT',
                body: JSON.stringify(profileData)
            });
        },
        
        getProfile: (userId) => {
            return API.request(`/freelancer/profile/${userId}`);
        },
        
        getJobRecommendations: () => {
            return API.request('/freelancer/job-recommendations');
        }
    },
    
    // Jobs
    jobs: {
        create: (jobData) => {
            return API.request('/jobs', {
                method: 'POST',
                body: JSON.stringify(jobData)
            });
        },
        
        getAll: (filters = {}) => {
            const params = new URLSearchParams(filters);
            return API.request(`/jobs?${params}`);
        },
        
        getById: (jobId) => {
            return API.request(`/jobs/${jobId}`);
        },
        
        update: (jobId, jobData) => {
            return API.request(`/jobs/${jobId}`, {
                method: 'PUT',
                body: JSON.stringify(jobData)
            });
        },
        
        getRecommendations: (jobId) => {
            return API.request(`/jobs/${jobId}/recommendations`);
        },
        
        apply: (jobId, applicationData) => {
            return API.request(`/jobs/${jobId}/apply`, {
                method: 'POST',
                body: JSON.stringify(applicationData)
            });
        },
        
        getApplications: (jobId) => {
            return API.request(`/jobs/${jobId}/applications`);
        }
    },
    
    // Applications
    applications: {
        updateStatus: (applicationId, status) => {
            return API.request(`/applications/${applicationId}/status`, {
                method: 'PUT',
                body: JSON.stringify({ status })
            });
        }
    },
    
    // Payments
    payments: {
        create: (paymentData) => {
            return API.request('/payments/create', {
                method: 'POST',
                body: JSON.stringify(paymentData)
            });
        },
        
        release: (paymentId) => {
            return API.request(`/payments/${paymentId}/release`, {
                method: 'POST'
            });
        },
        
        getHistory: () => {
            return API.request('/payments/history');
        }
    },
    
    // Dashboard
    dashboard: {
        getStats: () => {
            return API.request('/dashboard/stats');
        }
    },
    
    // Search
    search: {
        freelancers: (filters = {}) => {
            const params = new URLSearchParams(filters);
            return API.request(`/search/freelancers?${params}`);
        }
    }
};
