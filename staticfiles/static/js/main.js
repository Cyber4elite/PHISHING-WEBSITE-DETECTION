/**
 * PhishShield Main JavaScript
 * Handles UI interactions and form enhancements
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize theme toggle
    initThemeToggle();
    
    // Initialize form enhancements
    initFormEnhancements();
    
    // Initialize loading states
    initLoadingStates();
    
    // Initialize tooltips and help text
    initTooltips();
});

/**
 * Initialize theme toggle functionality
 */
function initThemeToggle() {
    const themeToggle = document.getElementById('theme-toggle');
    const themeIcon = themeToggle?.querySelector('.theme-icon');
    const body = document.body;
    
    if (!themeToggle || !themeIcon) return;
    
    // Check for saved theme preference or default to light mode
    const currentTheme = localStorage.getItem('theme') || 'light';
    body.setAttribute('data-theme', currentTheme);
    updateThemeIcon(currentTheme);
    
    // Theme toggle event listener
    themeToggle.addEventListener('click', function() {
        const currentTheme = body.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        
        body.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
        updateThemeIcon(newTheme);
    });
    
    function updateThemeIcon(theme) {
        themeIcon.textContent = theme === 'dark' ? '☀️' : '🌙';
    }
}

/**
 * Initialize form enhancements
 */
function initFormEnhancements() {
    const form = document.querySelector('.scan-form');
    const urlInput = document.querySelector('input[name="url"]');
    const submitButton = document.querySelector('button[type="submit"]');
    
    if (!form || !urlInput || !submitButton) return;
    
    // Form submission with loading state
    form.addEventListener('submit', function(e) {
        // Client-side validation removed.
        showLoadingState();
        
        // For scan form, show loading text
        const scanBtn = document.getElementById('scan-btn');
        if (scanBtn) {
            scanBtn.classList.add('loading');
        }
    });
    
    // Auto-focus URL input
    urlInput.focus();
}

/**
 * Show loading state during form submission
 */
function showLoadingState() {
    const submitButton = document.querySelector('button[type="submit"]');
    const originalText = submitButton.textContent;
    
    submitButton.disabled = true;
    submitButton.innerHTML = '<span class="loading"></span> Analyzing URL...';
    
    // Re-enable after 30 seconds as fallback
    setTimeout(() => {
        submitButton.disabled = false;
        submitButton.textContent = originalText;
    }, 30000);
}

/**
 * Initialize loading states for various elements
 */
function initLoadingStates() {
    // Add loading animation to buttons
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(button => {
        button.addEventListener('click', function() {
            if (this.type === 'submit') {
                // Loading state handled in form submission
                return;
            }
            
            // Add loading state to other buttons
            this.classList.add('loading');
            setTimeout(() => {
                this.classList.remove('loading');
            }, 1000);
        });
    });
}

/**
 * Initialize tooltips and help text
 */
function initTooltips() {
    // Add tooltips to feature values
    const featureValues = document.querySelectorAll('.feature-value');
    featureValues.forEach(value => {
        if (value.classList.contains('positive')) {
            value.title = 'This is a positive security indicator';
        } else if (value.classList.contains('negative')) {
            value.title = 'This is a negative security indicator';
        }
    });
    
    // Add help text to confidence scores
    const confidenceValues = document.querySelectorAll('.confidence-value');
    confidenceValues.forEach(value => {
        value.title = 'Confidence score: 0% = uncertain, 100% = very confident';
    });
}

/**
 * Utility function to show notifications
 */
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        notification.remove();
    }, 5000);
}

/**
 * Utility function to copy text to clipboard
 */
function copyToClipboard(text) {
    if (navigator.clipboard) {
        navigator.clipboard.writeText(text).then(() => {
            showNotification('Copied to clipboard!', 'success');
        });
    } else {
        // Fallback for older browsers
        const textArea = document.createElement('textarea');
        textArea.value = text;
        document.body.appendChild(textArea);
        textArea.select();
        document.execCommand('copy');
        document.body.removeChild(textArea);
        showNotification('Copied to clipboard!', 'success');
    }
}

/**
 * Initialize copy functionality for URLs
 */
function initCopyFunctionality() {
    const urlElements = document.querySelectorAll('.analyzed-url');
    urlElements.forEach(element => {
        element.style.cursor = 'pointer';
        element.title = 'Click to copy URL';
        
        element.addEventListener('click', function() {
            copyToClipboard(this.textContent);
        });
    });
}

// Initialize copy functionality when DOM is ready
document.addEventListener('DOMContentLoaded', initCopyFunctionality);
