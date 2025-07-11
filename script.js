// DOM Elements
const inputText = document.getElementById('inputText');
const outputText = document.getElementById('outputText');
const shiftSlider = document.getElementById('shiftSlider');
const shiftNumber = document.getElementById('shiftValue');
const processBtn = document.getElementById('processBtn');
const copyBtn = document.getElementById('copyBtn');
const loadingOverlay = document.getElementById('loadingOverlay');
const operationRadios = document.querySelectorAll('input[name="operation"]');

// Initialize event listeners
document.addEventListener('DOMContentLoaded', function() {
    initializeEventListeners();
    updateShiftDisplay();
});

function initializeEventListeners() {
    // Sync slider and number input
    shiftSlider.addEventListener('input', function() {
        shiftNumber.value = this.value;
        updateShiftDisplay();
    });

    shiftNumber.addEventListener('input', function() {
        if (this.value >= 1 && this.value <= 25) {
            shiftSlider.value = this.value;
            updateShiftDisplay();
        }
    });

    // Process button
    processBtn.addEventListener('click', processCipher);

    // Copy button
    copyBtn.addEventListener('click', copyToClipboard);

    // Enter key in input text
    inputText.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && e.ctrlKey) {
            processCipher();
        }
    });

    // Operation radio buttons
    operationRadios.forEach(radio => {
        radio.addEventListener('change', updateUI);
    });

    // Real-time processing (optional - can be enabled for instant results)
    // inputText.addEventListener('input', debounce(processCipher, 500));
}

function updateShiftDisplay() {
    const shiftValue = parseInt(shiftSlider.value);
    shiftSlider.style.background = `linear-gradient(90deg, #ff6b6b ${(shiftValue/25)*100}%, #4ecdc4 ${(shiftValue/25)*100}%)`;
}

function updateUI() {
    const operation = document.querySelector('input[name="operation"]:checked').value;
    const btnText = operation === 'encrypt' ? 'Encrypt Text' : 'Decrypt Text';
    document.querySelector('.btn-text').textContent = btnText;
}

async function processCipher() {
    const text = inputText.value.trim();
    const shift = parseInt(shiftNumber.value);
    const operation = document.querySelector('input[name="operation"]:checked').value;

    if (!text) {
        showNotification('Please enter some text to process!', 'warning');
        return;
    }

    showLoading(true);

    try {
        // Try to use Python backend first, fallback to JavaScript
        let result;
        try {
            result = await processWithPython(text, shift, operation);
            showNotification(`Text ${operation}ed successfully using Python backend!`, 'success');
        } catch (backendError) {
            console.log('Python backend not available, using JavaScript fallback');
            result = await processWithJavaScript(text, shift, operation);
            showNotification(`Text ${operation}ed successfully!`, 'success');
        }
        
        outputText.value = result;
        
        // Animate the output
        outputText.style.transform = 'scale(0.95)';
        setTimeout(() => {
            outputText.style.transform = 'scale(1)';
        }, 150);

    } catch (error) {
        console.error('Error processing cipher:', error);
        showNotification('An error occurred while processing the text.', 'error');
    } finally {
        showLoading(false);
    }
}

// JavaScript implementation of Caesar cipher (fallback)
async function processWithJavaScript(text, shift, operation) {
    return new Promise((resolve) => {
        // Simulate processing delay
        setTimeout(() => {
            const actualShift = operation === 'decrypt' ? -shift : shift;
            const result = caesarCipherJS(text, actualShift);
            resolve(result);
        }, 800);
    });
}

function caesarCipherJS(text, shift) {
    return text.split('').map(char => {
        if (char.match(/[a-z]/i)) {
            const code = char.charCodeAt(0);
            const base = code < 97 ? 65 : 97; // Uppercase or lowercase
            const shifted = ((code - base + shift + 26) % 26) + base;
            return String.fromCharCode(shifted);
        }
        return char;
    }).join('');
}

// Alternative: Send to Python backend
async function processWithPython(text, shift, operation) {
    const response = await fetch('/api/caesar-cipher', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            text: text,
            shift: shift,
            operation: operation
        })
    });

    if (!response.ok) {
        throw new Error('Network response was not ok');
    }

    const data = await response.json();
    return data.result;
}

function copyToClipboard() {
    const text = outputText.value;
    
    if (!text) {
        showNotification('Nothing to copy!', 'warning');
        return;
    }

    navigator.clipboard.writeText(text).then(() => {
        showNotification('Text copied to clipboard!', 'success');
        
        // Visual feedback
        copyBtn.style.background = '#4ecdc4';
        copyBtn.style.transform = 'scale(1.2)';
        
        setTimeout(() => {
            copyBtn.style.background = 'rgba(255, 255, 255, 0.9)';
            copyBtn.style.transform = 'scale(1)';
        }, 200);
        
    }).catch(err => {
        console.error('Failed to copy text: ', err);
        showNotification('Failed to copy text', 'error');
    });
}

function showLoading(show) {
    if (show) {
        loadingOverlay.classList.add('show');
        processBtn.disabled = true;
    } else {
        loadingOverlay.classList.remove('show');
        processBtn.disabled = false;
    }
}

function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;
    
    // Style the notification
    Object.assign(notification.style, {
        position: 'fixed',
        top: '20px',
        right: '20px',
        padding: '1rem 1.5rem',
        borderRadius: '10px',
        color: '#fff',
        fontWeight: '500',
        zIndex: '10000',
        transform: 'translateX(100%)',
        transition: 'transform 0.3s ease',
        boxShadow: '0 4px 12px rgba(0,0,0,0.3)'
    });

    // Set background color based on type
    const colors = {
        success: 'linear-gradient(45deg, #4ecdc4, #44a08d)',
        warning: 'linear-gradient(45deg, #f093fb, #f5576c)',
        error: 'linear-gradient(45deg, #ff6b6b, #ee5a24)',
        info: 'linear-gradient(45deg, #667eea, #764ba2)'
    };
    
    notification.style.background = colors[type] || colors.info;
    
    // Add to DOM
    document.body.appendChild(notification);
    
    // Animate in
    setTimeout(() => {
        notification.style.transform = 'translateX(0)';
    }, 100);
    
    // Remove after delay
    setTimeout(() => {
        notification.style.transform = 'translateX(100%)';
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 300);
    }, 3000);
}

// Debounce function for real-time processing
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

// Add some visual effects
function addVisualEffects() {
    // Add floating particles background
    createFloatingParticles();
    
    // Add keyboard shortcuts info
    document.addEventListener('keydown', function(e) {
        if (e.key === 'F1') {
            e.preventDefault();
            showKeyboardShortcuts();
        }
    });
}

function createFloatingParticles() {
    const particleCount = 20;
    
    for (let i = 0; i < particleCount; i++) {
        const particle = document.createElement('div');
        particle.className = 'particle';
        
        Object.assign(particle.style, {
            position: 'fixed',
            width: '4px',
            height: '4px',
            background: 'rgba(255, 255, 255, 0.3)',
            borderRadius: '50%',
            pointerEvents: 'none',
            zIndex: '-1',
            left: Math.random() * 100 + '%',
            top: Math.random() * 100 + '%',
            animation: `float ${5 + Math.random() * 10}s infinite linear`
        });
        
        document.body.appendChild(particle);
    }
    
    // Add CSS for particle animation
    const style = document.createElement('style');
    style.textContent = `
        @keyframes float {
            0% {
                transform: translateY(0) rotate(0deg);
                opacity: 0;
            }
            10% {
                opacity: 1;
            }
            90% {
                opacity: 1;
            }
            100% {
                transform: translateY(-100vh) rotate(360deg);
                opacity: 0;
            }
        }
    `;
    document.head.appendChild(style);
}

function showKeyboardShortcuts() {
    const shortcuts = [
        'Ctrl + Enter: Process text',
        'F1: Show this help',
        'Tab: Navigate between fields'
    ];
    
    showNotification('Keyboard shortcuts:\n' + shortcuts.join('\n'), 'info');
}

// Initialize visual effects
addVisualEffects();

// Update UI on page load
updateUI(); 