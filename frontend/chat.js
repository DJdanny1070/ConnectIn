// Chat system with WebSocket support
const Chat = {
    conversations: [],
    activeChat: null,
    ws: null,
    
    init: () => {
        document.getElementById('chatBtn')?.addEventListener('click', Chat.togglePanel);
        Chat.loadConversations();
    },
    
    togglePanel: () => {
        document.getElementById('chatPanel').classList.toggle('open');
    },
    
    open: () => {
        document.getElementById('chatPanel').classList.add('open');
    },
    
    loadConversations: () => {
        // Mock data
        Chat.conversations = [
            { id: 1, name: 'TechCorp Solutions', avatar: null, lastMessage: 'When can you start?', time: new Date(), unread: 2 },
            { id: 2, name: 'Raj Kumar', avatar: null, lastMessage: 'Thanks for applying', time: new Date(Date.now() - 3600000), unread: 0 }
        ];
        Chat.renderConversations();
        Chat.updateBadge();
    },
    
    renderConversations: () => {
        const list = document.getElementById('chatList');
        if (!list) return;
        
        list.innerHTML = Chat.conversations.map(conv => `
            <div class="chat-item ${Chat.activeChat === conv.id ? 'active' : ''}" onclick="Chat.openConversation(${conv.id})">
                <img src="${Utils.getAvatarUrl(conv.name, conv.avatar)}" alt="${conv.name}" style="width: 50px; height: 50px; border-radius: 50%;">
                <div style="flex: 1;">
                    <div style="display: flex; justify-content: space-between;">
                        <strong>${conv.name}</strong>
                        <small>${Utils.formatRelativeTime(conv.time)}</small>
                    </div>
                    <p style="margin: 0; color: var(--gray); font-size: 0.9rem;">${Utils.truncate(conv.lastMessage, 40)}</p>
                </div>
                ${conv.unread > 0 ? `<span class="badge badge-danger">${conv.unread}</span>` : ''}
            </div>
        `).join('');
    },
    
    updateBadge: () => {
        const total = Chat.conversations.reduce((sum, c) => sum + c.unread, 0);
        const badge = document.getElementById('chatBadge');
        if (badge) {
            badge.textContent = total;
            badge.style.display = total > 0 ? 'block' : 'none';
        }
    },
    
    openConversation: (convId) => {
        Chat.activeChat = convId;
        // Open chat window - implement full chat UI here
        Utils.showToast('Chat feature - Full implementation coming soon!', 'info');
    }
};

function closeChatPanel() {
    document.getElementById('chatPanel').classList.remove('open');
}
