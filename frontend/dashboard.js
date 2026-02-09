const Dashboard = {
    init: async () => {
        const user = JSON.parse(localStorage.getItem(CONFIG.STORAGE_KEYS.USER) || 'null');
        if (!user) { navigateTo('home'); return; }
        
        try {
            const stats = await API.dashboard.getStats();
            Dashboard.renderDashboard(user, stats);
        } catch (error) {
            console.error('Error loading dashboard:', error);
        }
    },
    
    renderDashboard: (user, stats) => {
        const page = document.getElementById('dashboardPage');
        const isFreelancer = user.user_type === 'freelancer';
        
        page.innerHTML = `
            <div class="container" style="padding: 2rem 20px;">
                <h1>Welcome back, ${user.name}!</h1>
                <div class="grid grid-3" style="margin-top: 2rem;">
                    ${isFreelancer ? `
                        <div class="card"><div class="card-body"><h3>${stats.applications_sent || 0}</h3><p>Applications Sent</p></div></div>
                        <div class="card"><div class="card-body"><h3>${stats.jobs_won || 0}</h3><p>Jobs Won</p></div></div>
                        <div class="card"><div class="card-body"><h3>${Utils.formatCurrency(stats.total_earned || 0)}</h3><p>Total Earned</p></div></div>
                    ` : `
                        <div class="card"><div class="card-body"><h3>${stats.jobs_posted || 0}</h3><p>Jobs Posted</p></div></div>
                        <div class="card"><div class="card-body"><h3>${stats.active_jobs || 0}</h3><p>Active Jobs</p></div></div>
                        <div class="card"><div class="card-body"><h3>${Utils.formatCurrency(stats.total_spent || 0)}</h3><p>Total Spent</p></div></div>
                    `}
                </div>
            </div>
        `;
    }
};
