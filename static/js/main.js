// Main JavaScript file for VulnScanner

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips if Bootstrap tooltips are used
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // URL validation and formatting
    const urlInput = document.getElementById('url');
    const scanForm = document.getElementById('scanForm');
    
    if (urlInput && scanForm) {
        // Real-time URL validation
        urlInput.addEventListener('input', function() {
            const url = this.value.trim();
            const isValid = isValidUrl(url);
            
            if (url && !isValid) {
                this.classList.add('is-invalid');
                this.classList.remove('is-valid');
            } else if (url && isValid) {
                this.classList.add('is-valid');
                this.classList.remove('is-invalid');
            } else {
                this.classList.remove('is-valid', 'is-invalid');
            }
        });

        // Form submission handling
        scanForm.addEventListener('submit', function(e) {
            const url = urlInput.value.trim();
            
            if (!url) {
                e.preventDefault();
                showAlert('Please enter a URL to scan', 'error');
                urlInput.focus();
                return;
            }
            
            if (!isValidUrl(url)) {
                e.preventDefault();
                showAlert('Please enter a valid URL', 'error');
                urlInput.focus();
                return;
            }
            
            // Show loading state
            showScanProgress();
        });
    }

    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            if (alert && alert.parentNode) {
                alert.style.transition = 'opacity 0.5s ease';
                alert.style.opacity = '0';
                setTimeout(function() {
                    if (alert && alert.parentNode) {
                        alert.remove();
                    }
                }, 500);
            }
        }, 5000);
    });

    // Smooth scrolling for anchor links
    const anchorLinks = document.querySelectorAll('a[href^="#"]');
    anchorLinks.forEach(function(link) {
        link.addEventListener('click', function(e) {
            const targetId = this.getAttribute('href').substring(1);
            const targetElement = document.getElementById(targetId);
            
            if (targetElement) {
                e.preventDefault();
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Collapsible vulnerability details
    const vulnerabilityItems = document.querySelectorAll('.vulnerability-item');
    vulnerabilityItems.forEach(function(item) {
        const header = item.querySelector('.vulnerability-header');
        const content = item.querySelector('.vulnerability-content');
        
        if (header && content) {
            header.style.cursor = 'pointer';
            header.addEventListener('click', function() {
                content.style.display = content.style.display === 'none' ? 'block' : 'none';
                
                // Add/remove collapsed class for styling
                item.classList.toggle('collapsed');
            });
        }
    });
});

// Utility Functions

/**
 * Validate URL format
 * @param {string} url - URL to validate
 * @returns {boolean} - True if valid URL
 */
function isValidUrl(url) {
    try {
        // Add protocol if missing
        if (!url.startsWith('http://') && !url.startsWith('https://')) {
            url = 'https://' + url;
        }
        
        const urlObject = new URL(url);
        return urlObject.protocol === 'http:' || urlObject.protocol === 'https:';
    } catch (error) {
        return false;
    }
}

/**
 * Show alert message
 * @param {string} message - Alert message
 * @param {string} type - Alert type (success, error, info)
 */
function showAlert(message, type = 'info') {
    const alertContainer = document.querySelector('.container');
    if (!alertContainer) return;
    
    const alertClass = type === 'error' ? 'alert-danger' : 
                      type === 'success' ? 'alert-success' : 'alert-info';
    
    const iconName = type === 'error' ? 'alert-circle' : 
                    type === 'success' ? 'check-circle' : 'info';
    
    const alertHTML = `
        <div class="alert ${alertClass} alert-dismissible fade show mt-3" role="alert">
            <i data-feather="${iconName}" class="icon-sm me-2"></i>
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;
    
    alertContainer.insertAdjacentHTML('afterbegin', alertHTML);
    
    // Initialize feather icons for the new alert
    feather.replace();
    
    // Auto-hide after 5 seconds
    setTimeout(function() {
        const newAlert = alertContainer.querySelector('.alert');
        if (newAlert) {
            newAlert.style.transition = 'opacity 0.5s ease';
            newAlert.style.opacity = '0';
            setTimeout(function() {
                if (newAlert && newAlert.parentNode) {
                    newAlert.remove();
                }
            }, 500);
        }
    }, 5000);
}

/**
 * Show scan progress UI
 */
function showScanProgress() {
    const scanButton = document.getElementById('scanButton');
    if (!scanButton) return;
    
    const originalText = scanButton.innerHTML;
    scanButton.disabled = true;
    scanButton.innerHTML = `
        <span class="spinner-border spinner-border-sm me-2" role="status"></span>
        Scanning... This may take a few minutes
    `;
    
    // Show progress message
    showAlert('Scan started. Please wait while we analyze the target URL for security vulnerabilities.', 'info');
}

/**
 * Format time duration
 * @param {number} seconds - Duration in seconds
 * @returns {string} - Formatted duration
 */
function formatDuration(seconds) {
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;
    
    if (minutes > 0) {
        return `${minutes}m ${remainingSeconds}s`;
    }
    return `${remainingSeconds}s`;
}

/**
 * Copy text to clipboard
 * @param {string} text - Text to copy
 */
function copyToClipboard(text) {
    if (navigator.clipboard) {
        navigator.clipboard.writeText(text).then(function() {
            showAlert('Copied to clipboard', 'success');
        }).catch(function() {
            fallbackCopyToClipboard(text);
        });
    } else {
        fallbackCopyToClipboard(text);
    }
}

/**
 * Fallback copy to clipboard for older browsers
 * @param {string} text - Text to copy
 */
function fallbackCopyToClipboard(text) {
    const textArea = document.createElement('textarea');
    textArea.value = text;
    textArea.style.position = 'fixed';
    textArea.style.left = '-999999px';
    textArea.style.top = '-999999px';
    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();
    
    try {
        document.execCommand('copy');
        showAlert('Copied to clipboard', 'success');
    } catch (err) {
        showAlert('Failed to copy to clipboard', 'error');
    }
    
    document.body.removeChild(textArea);
}

/**
 * Debounce function to limit function calls
 * @param {function} func - Function to debounce
 * @param {number} wait - Wait time in milliseconds
 * @returns {function} - Debounced function
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

/**
 * Throttle function to limit function calls
 * @param {function} func - Function to throttle
 * @param {number} limit - Time limit in milliseconds
 * @returns {function} - Throttled function
 */
function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

// Export functions for use in other scripts
window.VulnScanner = {
    isValidUrl,
    showAlert,
    copyToClipboard,
    debounce,
    throttle,
    formatDuration
};
