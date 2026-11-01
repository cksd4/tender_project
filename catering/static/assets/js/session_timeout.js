/**
 * Monitors user activity and submits the logout form after the session timeout.
 */
document.addEventListener('DOMContentLoaded', function() {
    const navElement = document.querySelector('[data-idle-timeout-seconds]');
    const logoutForm = document.getElementById('logout-form');
    if (!navElement || !logoutForm) return;

    const IDLE_TIMEOUT_SECONDS = Number(navElement.dataset.idleTimeoutSeconds);
    let idleTimer;

    function resetIdleTimer() {
        clearTimeout(idleTimer);
        idleTimer = setTimeout(forceLogoutRedirect, IDLE_TIMEOUT_SECONDS * 1000);
    }

    function forceLogoutRedirect() {
        logoutForm.requestSubmit();
    }

    ['mousemove', 'mousedown', 'touchstart', 'click', 'keydown'].forEach(function(eventName) {
        window.addEventListener(eventName, resetIdleTimer);
    });

    resetIdleTimer();
});
