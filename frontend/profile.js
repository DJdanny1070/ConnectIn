const Profile = {
    init: () => {},
    showSetupModal: () => {
        Utils.showToast('Please complete your profile setup', 'info');
        setTimeout(() => navigateTo('profile'), 1000);
    }
};
