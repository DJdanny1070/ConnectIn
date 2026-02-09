// Real-time notifications module
const Notifications = {
    notifications: [],
    unreadCount: 0,
    
    init: () => {
        document.getElementById('notificationBtn')?.addEventListener('click', Notifications.togglePanel);
        Notifications.loadNotifications();
        Notifications.startPolling();
    },
    
    togglePanel: () => {
        const panel = document.getElementById('notificationPanel');
        panel.classList.toggle('open');
        
        if (panel.classList.contains('open')) {
            Notifications.markAllAsRead();
        }
    },
    
    loadNotifications: async () => {
        // Mock notifications - replace with actual API call
        Notifications.notifications = [
            {
                id: 1,
                type: 'job_match',
                title: 'New job matches your profile!',
                message: 'E-commerce Platform Development - 87% match',
                time: new Date(Date.now() - 300000).toISOString(),
                read: false
            },
            {
                id: 2,
                type: 'application',
                title: 'Application Update',
                message: 'Your application was accepted',
                time: new Date(Date.now() - 3600000).toISOString(),
                read: false
            },
            {
                id: 3,
                type: 'message',
                title: 'New Message',
                message: 'You have a new message from TechCorp',
                time: new Date(Date.now() - 7200000).toISOString(),
                read: true
            }
        ];
        
        Notifications.renderNotifications();
        Notifications.updateBadge();
    },
    
    renderNotifications: () => {
        const list = document.getElementById('notificationList');
        if (!list) return;
        
        if (Notifications.notifications.length === 0) {
            list.innerHTML = '<p class="text-center text-gray">No notifications</p>';
            return;
        }
        
        list.innerHTML = Notifications.notifications.map(notif => `
            <div class="notification-item ${!notif.read ? 'unread' : ''}" onclick="Notifications.handleClick(${notif.id})">
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                    <strong>${notif.title}</strong>
                    <small class="text-gray">${Utils.formatRelativeTime(notif.time)}</small>
                </div>
                <p style="margin: 0; color: var(--gray);">${notif.message}</p>
            </div>
        `).join('');
    },
    
    updateBadge: () => {
        Notifications.unreadCount = Notifications.notifications.filter(n => !n.read).length;
        const badge = document.getElementById('notificationBadge');
        if (badge) {
            badge.textContent = Notifications.unreadCount;
            badge.style.display = Notifications.unreadCount > 0 ? 'block' : 'none';
        }
    },
    
    markAllAsRead: () => {
        Notifications.notifications.forEach(n => n.read = true);
        Notifications.updateBadge();
        Notifications.renderNotifications();
    },
    
    handleClick: (notifId) => {
        const notif = Notifications.notifications.find(n => n.id === notifId);
        if (!notif) return;
        
        notif.read = true;
        Notifications.updateBadge();
        
        // Navigate based on notification type
        if (notif.type === 'job_match') {
            navigateTo('jobs');
        } else if (notif.type === 'message') {
            Chat.open();
        }
    },
    
    addNotification: (notification) => {
        Notifications.notifications.unshift(notification);
        Notifications.renderNotifications();
        Notifications.updateBadge();
        
        // Show toast
        Utils.showToast(notification.title, 'info');
    },
    
    startPolling: () => {
        // Poll for new notifications every 30 seconds
        setInterval(() => {
            // In production, make API call to check for new notifications
            Notifications.loadNotifications();
        }, 30000);
    }
};

function closeNotificationPanel() {
    document.getElementById('notificationPanel').classList.remove('open');
}
