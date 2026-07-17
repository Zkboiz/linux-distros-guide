// Dark Mode / Light Mode Theme Toggle

document.addEventListener('DOMContentLoaded', function() {
    // Initialize theme on page load
    initializeTheme();
    
    // Set up theme toggle button
    setupThemeToggle();
});

/**
 * Initialize the theme based on user preference or system preference
 */
function initializeTheme() {
    const savedTheme = localStorage.getItem('theme');
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    
    // Use saved theme, or fall back to system preference, or default to light
    const theme = savedTheme || (prefersDark ? 'dark' : 'light');
    
    applyTheme(theme);
}

/**
 * Apply the theme to the document
 */
function applyTheme(theme) {
    const htmlElement = document.documentElement;
    
    if (theme === 'dark') {
        htmlElement.setAttribute('data-theme', 'dark');
        localStorage.setItem('theme', 'dark');
        updateThemeToggleButton('light'); // Show sun icon to switch to light
    } else {
        htmlElement.removeAttribute('data-theme');
        localStorage.setItem('theme', 'light');
        updateThemeToggleButton('dark'); // Show moon icon to switch to dark
    }
}

/**
 * Set up the theme toggle button click handler
 */
function setupThemeToggle() {
    const toggleButton = document.getElementById('themeToggle');
    
    if (toggleButton) {
        toggleButton.addEventListener('click', function(e) {
            e.preventDefault();
            toggleTheme();
        });
    }
}

/**
 * Toggle between light and dark themes
 */
function toggleTheme() {
    const htmlElement = document.documentElement;
    const currentTheme = htmlElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    
    applyTheme(newTheme);
}

/**
 * Update the theme toggle button icon
 */
function updateThemeToggleButton(nextTheme) {
    const toggleButton = document.getElementById('themeToggle');
    
    if (toggleButton) {
        if (nextTheme === 'dark') {
            toggleButton.innerHTML = '🌙'; // Moon icon - click to go dark
            toggleButton.setAttribute('aria-label', 'Switch to dark mode');
            toggleButton.title = 'Dark Mode';
        } else {
            toggleButton.innerHTML = '☀️'; // Sun icon - click to go light
            toggleButton.setAttribute('aria-label', 'Switch to light mode');
            toggleButton.title = 'Light Mode';
        }
    }
}
