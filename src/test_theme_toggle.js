/**
 * Theme Toggle Test Script
 * Run this in the browser console to test theme functionality
 */

// Test theme toggle functionality
const testThemeToggle = () => {
  console.log('🧪 Testing Theme Toggle Functionality...');
  
  // Check if theme context is available
  const themeToggle = document.querySelector('[aria-label*="theme"]');
  if (!themeToggle) {
    console.log('❌ Theme toggle button not found');
    return;
  }
  
  console.log('✅ Theme toggle button found');
  
  // Get current theme state
  const currentTheme = document.documentElement.classList.contains('dark') ? 'dark' : 'light';
  console.log('Current theme:', currentTheme);
  
  // Test clicking the toggle
  console.log('Clicking theme toggle...');
  themeToggle.click();
  
  // Wait a bit and check if theme changed
  setTimeout(() => {
    const newTheme = document.documentElement.classList.contains('dark') ? 'dark' : 'light';
    console.log('New theme after click:', newTheme);
    
    if (newTheme !== currentTheme) {
      console.log('✅ Theme toggle working! Theme changed from', currentTheme, 'to', newTheme);
    } else {
      console.log('❌ Theme toggle not working. Theme is still', newTheme);
    }
    
    // Test localStorage
    const storedTheme = localStorage.getItem('theme');
    console.log('Stored theme in localStorage:', storedTheme);
    
    if (storedTheme === newTheme) {
      console.log('✅ Theme persistence working!');
    } else {
      console.log('❌ Theme persistence not working');
    }
  }, 100);
};

// Test theme classes
const testThemeClasses = () => {
  console.log('🧪 Testing Theme Classes...');
  
  const htmlElement = document.documentElement;
  const classes = htmlElement.className;
  const dataTheme = htmlElement.getAttribute('data-theme');
  
  console.log('HTML classes:', classes);
  console.log('Data theme attribute:', dataTheme);
  
  const hasDarkClass = classes.includes('dark');
  const hasLightClass = classes.includes('light');
  
  console.log('Has dark class:', hasDarkClass);
  console.log('Has light class:', hasLightClass);
  
  if (hasDarkClass || hasLightClass) {
    console.log('✅ Theme classes are applied');
  } else {
    console.log('❌ No theme classes found');
  }
};

// Test dark mode styles
const testDarkModeStyles = () => {
  console.log('🧪 Testing Dark Mode Styles...');
  
  // Find elements with dark mode classes
  const darkElements = document.querySelectorAll('[class*="dark:"]');
  console.log(`Found ${darkElements.length} elements with dark mode classes`);
  
  // Test a specific element
  const testElement = document.querySelector('.bg-white.dark\\:bg-slate-900');
  if (testElement) {
    const computedStyle = window.getComputedStyle(testElement);
    console.log('Test element background color:', computedStyle.backgroundColor);
    console.log('✅ Dark mode styles are being applied');
  } else {
    console.log('❌ No test elements found with dark mode classes');
  }
};

// Run all tests
const runAllTests = () => {
  console.log('🎨 Starting Theme Toggle Tests...');
  console.log('='.repeat(50));
  
  testThemeClasses();
  console.log('');
  
  testDarkModeStyles();
  console.log('');
  
  testThemeToggle();
  console.log('');
  
  console.log('='.repeat(50));
  console.log('🎉 Theme toggle tests completed!');
};

// Auto-run tests
if (typeof window !== 'undefined') {
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', runAllTests);
  } else {
    runAllTests();
  }
}

// Export for manual testing
if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    testThemeToggle,
    testThemeClasses,
    testDarkModeStyles,
    runAllTests
  };
}
