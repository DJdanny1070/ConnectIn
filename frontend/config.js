// Configuration file for the application
const CONFIG = {
    API_BASE_URL: 'http://localhost:5000/api',
    WS_URL: 'ws://localhost:5000',
    
    // Storage keys
    STORAGE_KEYS: {
        TOKEN: 'freelance_token',
        USER: 'freelance_user',
        THEME: 'freelance_theme'
    },
    
    // Pagination
    ITEMS_PER_PAGE: 12,
    
    // WebRTC Configuration for video calls
    WEBRTC_CONFIG: {
        iceServers: [
            { urls: 'stun:stun.l.google.com:19302' },
            { urls: 'stun:stun1.l.google.com:19302' }
        ]
    },
    
    // Payment methods
    PAYMENT_METHODS: {
        upi: { name: 'UPI', icon: 'fab fa-google-pay' },
        netbanking: { name: 'Net Banking', icon: 'fas fa-university' },
        card: { name: 'Credit/Debit Card', icon: 'fas fa-credit-card' },
        wallet: { name: 'Wallet', icon: 'fas fa-wallet' }
    },
    
    // Skill categories for better organization
    SKILL_CATEGORIES: {
        'Web Development': ['HTML', 'CSS', 'JavaScript', 'React', 'Vue', 'Angular', 'Node.js', 'PHP', 'Django', 'Flask'],
        'Mobile Development': ['React Native', 'Flutter', 'iOS', 'Android', 'Kotlin', 'Swift'],
        'Backend': ['Python', 'Java', 'Node.js', 'PHP', 'Ruby', 'Go', 'C#'],
        'Database': ['MySQL', 'PostgreSQL', 'MongoDB', 'Redis', 'Oracle'],
        'Design': ['UI/UX', 'Figma', 'Adobe XD', 'Photoshop', 'Illustrator'],
        'DevOps': ['AWS', 'Docker', 'Kubernetes', 'CI/CD', 'Jenkins'],
        'Data Science': ['Python', 'Machine Learning', 'Data Analysis', 'TensorFlow', 'Pandas'],
        'Other': ['Project Management', 'Content Writing', 'SEO', 'Digital Marketing']
    },
    
    // Experience levels
    EXPERIENCE_LEVELS: ['entry', 'intermediate', 'expert'],
    
    // Job types
    JOB_TYPES: ['project', 'hourly', 'contract'],
    
    // Default avatar
    DEFAULT_AVATAR: 'https://ui-avatars.com/api/?name=User&background=4f46e5&color=fff',
    
    // Notification types
    NOTIFICATION_TYPES: {
        JOB_MATCH: 'job_match',
        APPLICATION: 'application',
        MESSAGE: 'message',
        PAYMENT: 'payment',
        REVIEW: 'review'
    },
    
    // Match score thresholds
    MATCH_THRESHOLDS: {
        excellent: 80,
        good: 60,
        fair: 40
    }
};

// Helper functions
const Utils = {
    // Format currency
    formatCurrency: (amount) => {
        return new Intl.NumberFormat('en-IN', {
            style: 'currency',
            currency: 'INR',
            maximumFractionDigits: 0
        }).format(amount);
    },
    
    // Format date
    formatDate: (dateString) => {
        const date = new Date(dateString);
        return new Intl.DateTimeFormat('en-IN', {
            year: 'numeric',
            month: 'short',
            day: 'numeric'
        }).format(date);
    },
    
    // Format relative time
    formatRelativeTime: (dateString) => {
        const date = new Date(dateString);
        const now = new Date();
        const diffMs = now - date;
        const diffMins = Math.floor(diffMs / 60000);
        const diffHours = Math.floor(diffMs / 3600000);
        const diffDays = Math.floor(diffMs / 86400000);
        
        if (diffMins < 1) return 'Just now';
        if (diffMins < 60) return `${diffMins} min${diffMins > 1 ? 's' : ''} ago`;
        if (diffHours < 24) return `${diffHours} hour${diffHours > 1 ? 's' : ''} ago`;
        if (diffDays < 7) return `${diffDays} day${diffDays > 1 ? 's' : ''} ago`;
        return Utils.formatDate(dateString);
    },
    
    // Truncate text
    truncate: (text, maxLength) => {
        if (!text) return '';
        if (text.length <= maxLength) return text;
        return text.substr(0, maxLength) + '...';
    },
    
    // Get initials from name
    getInitials: (name) => {
        if (!name) return 'U';
        return name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2);
    },
    
    // Generate avatar URL
    getAvatarUrl: (name, image = null) => {
        if (image) return image;
        return `https://ui-avatars.com/api/?name=${encodeURIComponent(name)}&background=4f46e5&color=fff`;
    },
    
    // Debounce function
    debounce: (func, wait) => {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    },
    
    // Show toast notification
    showToast: (message, type = 'info') => {
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.innerHTML = `
            <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : 'info-circle'}"></i>
            <span>${message}</span>
        `;
        
        // Add toast styles if not already present
        if (!document.querySelector('#toast-styles')) {
            const style = document.createElement('style');
            style.id = 'toast-styles';
            style.textContent = `
                .toast {
                    position: fixed;
                    bottom: 20px;
                    right: 20px;
                    padding: 1rem 1.5rem;
                    background: white;
                    border-radius: 8px;
                    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
                    display: flex;
                    align-items: center;
                    gap: 1rem;
                    z-index: 10000;
                    animation: slideIn 0.3s ease;
                }
                .toast-success { border-left: 4px solid #10b981; }
                .toast-error { border-left: 4px solid #ef4444; }
                .toast-info { border-left: 4px solid #3b82f6; }
                @keyframes slideIn {
                    from { transform: translateX(400px); opacity: 0; }
                    to { transform: translateX(0); opacity: 1; }
                }
            `;
            document.head.appendChild(style);
        }
        
        document.body.appendChild(toast);
        
        setTimeout(() => {
            toast.style.animation = 'slideIn 0.3s ease reverse';
            setTimeout(() => toast.remove(), 300);
        }, 3000);
    },
    
    // Validate email
    validateEmail: (email) => {
        return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
    },
    
    // Get match badge HTML
    getMatchBadge: (score) => {
        if (score >= CONFIG.MATCH_THRESHOLDS.excellent) {
            return '<span class="match-badge match-excellent">Excellent Match</span>';
        } else if (score >= CONFIG.MATCH_THRESHOLDS.good) {
            return '<span class="match-badge match-good">Good Match</span>';
        } else if (score >= CONFIG.MATCH_THRESHOLDS.fair) {
            return '<span class="match-badge match-fair">Fair Match</span>';
        }
        return '';
    },
    
    // Generate star rating HTML
    getStarRating: (rating, maxRating = 5) => {
        let html = '';
        for (let i = 1; i <= maxRating; i++) {
            if (i <= Math.floor(rating)) {
                html += '<i class="fas fa-star"></i>';
            } else if (i === Math.ceil(rating) && rating % 1 !== 0) {
                html += '<i class="fas fa-star-half-alt"></i>';
            } else {
                html += '<i class="far fa-star"></i>';
            }
        }
        return html;
    }
};

// Export for use in other files
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { CONFIG, Utils };
}
