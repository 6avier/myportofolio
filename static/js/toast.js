let toastTimer;
let toastHideTimer;

function showToast(title, message, type = 'normal', duration = 3000) {
    const toastComponent = document.getElementById('toast-component');
    const toastTitle = document.getElementById('toast-title');
    const toastMessage = document.getElementById('toast-message');

    if (!toastComponent || !toastTitle || !toastMessage) return;

    toastComponent.classList.remove('toast-success', 'toast-error', 'toast-normal');
    toastComponent.classList.add(`toast-${type}`);

    toastTitle.textContent = title;
    toastMessage.textContent = message;

    clearTimeout(toastTimer);
    clearTimeout(toastHideTimer);

    if (!toastComponent.matches(':popover-open')) {
        toastComponent.showPopover();
    }
    toastComponent.classList.remove('toast-hidden');
    toastComponent.classList.add('toast-show');

    toastTimer = setTimeout(() => {
        toastComponent.classList.remove('toast-show');
        toastComponent.classList.add('toast-hidden');
        toastHideTimer = setTimeout(() => {
            if (toastComponent.matches(':popover-open')) {
                toastComponent.hidePopover();
            }
        }, 300);
    }, duration);
}
