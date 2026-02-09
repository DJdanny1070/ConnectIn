const Jobs = {
    jobs: [],
    filters: {},
    
    init: async () => {
        await Jobs.loadJobs();
    },
    
    loadJobs: async (filters = {}) => {
        try {
            const response = await API.jobs.getAll(filters);
            Jobs.jobs = response.jobs || [];
            Jobs.renderJobsPage();
        } catch (error) {
            console.error('Error loading jobs:', error);
        }
    },
    
    renderJobsPage: () => {
        const page = document.getElementById('jobsPage');
        page.innerHTML = `
            <div class="container" style="padding: 2rem 20px;">
                <h1 class="section-title">Find Your Next Project</h1>
                <div style="display: grid; grid-template-columns: 250px 1fr; gap: 2rem;">
                    <div class="filters-sidebar" id="jobFilters">
                        ${Jobs.renderFilters()}
                    </div>
                    <div id="jobsList">${Jobs.renderJobs()}</div>
                </div>
            </div>
        `;
    },
    
    renderFilters: () => `
        <div class="filter-section">
            <h4 class="filter-title">Job Type</h4>
            <div class="filter-options">
                <label class="checkbox-wrapper"><input type="checkbox" value="project"> Project</label>
                <label class="checkbox-wrapper"><input type="checkbox" value="hourly"> Hourly</label>
                <label class="checkbox-wrapper"><input type="checkbox" value="contract"> Contract</label>
            </div>
        </div>
        <div class="filter-section">
            <h4 class="filter-title">Experience Level</h4>
            <div class="filter-options">
                <label class="checkbox-wrapper"><input type="checkbox" value="entry"> Entry</label>
                <label class="checkbox-wrapper"><input type="checkbox" value="intermediate"> Intermediate</label>
                <label class="checkbox-wrapper"><input type="checkbox" value="expert"> Expert</label>
            </div>
        </div>
    `,
    
    renderJobs: () => {
        if (!Jobs.jobs.length) return '<p class="text-center">No jobs found</p>';
        
        return `<div class="grid" style="grid-template-columns: 1fr; gap: 1.5rem;">
            ${Jobs.jobs.map(job => `
                <div class="job-card" onclick="Jobs.viewJob(${job.id})">
                    <div class="job-header">
                        <div>
                            <h3 class="job-title">${job.title}</h3>
                            <p class="job-company">${job.employer?.name || 'Anonymous'}</p>
                        </div>
                        <div class="job-budget">${Utils.formatCurrency(job.budget)}</div>
                    </div>
                    <div class="job-meta">
                        <span class="job-meta-item"><i class="fas fa-briefcase"></i> ${job.job_type}</span>
                        <span class="job-meta-item"><i class="fas fa-clock"></i> ${job.duration}</span>
                        <span class="job-meta-item"><i class="fas fa-map-marker-alt"></i> ${job.location}</span>
                    </div>
                    <p class="job-description">${Utils.truncate(job.description, 150)}</p>
                    <div class="job-skills">
                        ${(job.required_skills || []).slice(0, 5).map(skill => 
                            `<span class="skill-tag">${skill}</span>`
                        ).join('')}
                    </div>
                    <div class="job-footer">
                        <span class="text-gray"><i class="fas fa-calendar"></i> ${Utils.formatRelativeTime(job.created_at)}</span>
                        <button class="btn btn-primary btn-sm" onclick="event.stopPropagation(); Jobs.applyToJob(${job.id})">Apply Now</button>
                    </div>
                </div>
            `).join('')}
        </div>`;
    },
    
    viewJob: (jobId) => {
        Utils.showToast('Job details modal - coming soon!', 'info');
    },
    
    applyToJob: async (jobId) => {
        const user = JSON.parse(localStorage.getItem(CONFIG.STORAGE_KEYS.USER) || 'null');
        if (!user) {
            Auth.showLoginModal();
            return;
        }
        
        if (user.user_type !== 'freelancer') {
            Utils.showToast('Only freelancers can apply to jobs', 'error');
            return;
        }
        
        // Show application modal
        Utils.showToast('Application submitted successfully!', 'success');
    }
};
