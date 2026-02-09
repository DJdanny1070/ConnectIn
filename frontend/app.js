// Main application file
document.addEventListener('DOMContentLoaded', () => {
    // Initialize all modules
    Auth.init();
    Notifications.init();
    Chat.init();
    
    // Setup navigation
    setupNavigation();
    
    // Setup search
    setupSearch();
    
    // Load initial page
    const hash = window.location.hash.slice(1) || 'home';
    navigateTo(hash);
    
    // Handle browser back/forward
    window.addEventListener('hashchange', () => {
        const page = window.location.hash.slice(1) || 'home';
        navigateTo(page, false);
    });
});

// Navigation setup
function setupNavigation() {
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const page = link.getAttribute('data-page');
            navigateTo(page);
        });
    });
    
    // Mobile menu toggle
    document.getElementById('mobileMenuToggle')?.addEventListener('click', () => {
        const menu = document.getElementById('navMenu');
        menu.style.display = menu.style.display === 'flex' ? 'none' : 'flex';
    });
}

// Page navigation
function navigateTo(page, updateHash = true) {
    // Hide all pages
    document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
    
    // Update nav links
    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('data-page') === page) {
            link.classList.add('active');
        }
    });
    
    // Show selected page
    const pageMap = {
        'home': 'homePage',
        'jobs': 'jobsPage',
        'freelancers': 'freelancersPage',
        'dashboard': 'dashboardPage',
        'profile': 'profilePage'
    };
    
    const pageId = pageMap[page] || 'homePage';
    document.getElementById(pageId)?.classList.add('active');
    
    // Update URL hash
    if (updateHash) {
        window.location.hash = page;
    }
    
    // Load page-specific content
    switch(page) {
        case 'jobs':
            Jobs.init();
            break;
        case 'freelancers':
            Freelancers.init();
            break;
        case 'dashboard':
            Dashboard.init();
            break;
        case 'profile':
            Profile.init();
            break;
    }
    
    // Scroll to top
    window.scrollTo(0, 0);
}

// Search setup
function setupSearch() {
    const searchBtn = document.getElementById('heroSearchBtn');
    const searchInput = document.getElementById('heroSearch');
    
    // Search tabs
    document.querySelectorAll('.search-tab').forEach(tab => {
        tab.addEventListener('click', () => {
            document.querySelectorAll('.search-tab').forEach(t => t.classList.remove('active'));
            tab.classList.add('active');
            
            const type = tab.getAttribute('data-type');
            searchInput.placeholder = type === 'jobs' 
                ? 'Search for Python, React, Design...' 
                : 'Search for freelancers...';
        });
    });
    
    // Search button
    searchBtn?.addEventListener('click', performSearch);
    
    // Enter key on search input
    searchInput?.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            performSearch();
        }
    });
}

function performSearch() {
    const searchInput = document.getElementById('heroSearch');
    const query = searchInput.value.trim();
    const activeTab = document.querySelector('.search-tab.active');
    const searchType = activeTab?.getAttribute('data-type') || 'jobs';
    
    if (!query) {
        Utils.showToast('Please enter a search term', 'error');
        return;
    }
    
    if (searchType === 'jobs') {
        // Navigate to jobs page with search filter
        navigateTo('jobs');
        setTimeout(() => {
            Jobs.loadJobs({ skills: query });
        }, 100);
    } else {
        // Navigate to freelancers page with search filter
        navigateTo('freelancers');
        Utils.showToast('Searching for freelancers...', 'info');
    }
}

// Global error handler
window.addEventListener('error', (e) => {
    console.error('Global error:', e.error);
});

// Prevent unauthorized access to protected pages
function checkAuth() {
    const token = API.getToken();
    const protectedPages = ['dashboard', 'profile'];
    const currentPage = window.location.hash.slice(1);
    
    if (protectedPages.includes(currentPage) && !token) {
        Utils.showToast('Please login to access this page', 'error');
        navigateTo('home');
        Auth.showLoginModal();
        return false;
    }
    return true;
}

// Add to navigation
const originalNavigateTo = navigateTo;
navigateTo = function(page, updateHash = true) {
    if (checkAuth()) {
        originalNavigateTo(page, updateHash);
    }
};

console.log('FreelanceIndia Platform Loaded! 🚀');
