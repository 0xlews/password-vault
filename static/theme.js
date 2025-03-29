document.addEventListener('DOMContentLoaded', () => {
  const themeToggle = document.getElementById('theme-toggle');
  const prefersDarkScheme = window.matchMedia('(prefers-color-scheme: dark)');
  
  // Function to set the theme
  const setTheme = (isDark) => {
    if (isDark) {
      document.documentElement.setAttribute('data-theme', 'dark');
      localStorage.setItem('theme', 'dark');
      if (themeToggle) themeToggle.checked = true;
    } else {
      document.documentElement.setAttribute('data-theme', 'light');
      localStorage.setItem('theme', 'light');
      if (themeToggle) themeToggle.checked = false;
    }
  };
  
  // Check for saved theme preference or use the system preference
  const currentTheme = localStorage.getItem('theme');
  if (currentTheme) {
    setTheme(currentTheme === 'dark');
  } else {
    setTheme(prefersDarkScheme.matches);
  }
  
  // Listen for theme toggle changes
  if (themeToggle) {
    themeToggle.addEventListener('change', function() {
      setTheme(this.checked);
    });
  }
  
  // Listen for system theme changes
  prefersDarkScheme.addEventListener('change', (e) => {
    if (!localStorage.getItem('theme')) {
      setTheme(e.matches);
    }
  });
});