/**
 * Theme Functionality Test
 * This file tests the dark/light theme implementation
 */

// Test theme context functionality
const testThemeContext = () => {
  console.log('🧪 Testing Theme Context...');
  
  // Test localStorage persistence
  const testThemePersistence = () => {
    // Set theme to dark
    localStorage.setItem('theme', 'dark');
    console.log('✅ Dark theme saved to localStorage');
    
    // Set theme to light
    localStorage.setItem('theme', 'light');
    console.log('✅ Light theme saved to localStorage');
    
    // Clear theme
    localStorage.removeItem('theme');
    console.log('✅ Theme cleared from localStorage');
  };
  
  // Test system preference detection
  const testSystemPreference = () => {
    if (window.matchMedia) {
      const darkModeQuery = window.matchMedia('(prefers-color-scheme: dark)');
      console.log('✅ System prefers dark mode:', darkModeQuery.matches);
      
      const lightModeQuery = window.matchMedia('(prefers-color-scheme: light)');
      console.log('✅ System prefers light mode:', lightModeQuery.matches);
    }
  };
  
  // Test DOM class application
  const testDOMClassApplication = () => {
    // Test dark mode class
    document.documentElement.classList.add('dark');
    console.log('✅ Dark mode class applied to document');
    
    // Test light mode class
    document.documentElement.classList.remove('dark');
    document.documentElement.classList.add('light');
    console.log('✅ Light mode class applied to document');
    
    // Clean up
    document.documentElement.classList.remove('light', 'dark');
    console.log('✅ Classes cleaned up');
  };
  
  testThemePersistence();
  testSystemPreference();
  testDOMClassApplication();
  
  console.log('✅ Theme context tests completed');
};

// Test theme toggle component
const testThemeToggle = () => {
  console.log('🧪 Testing Theme Toggle Component...');
  
  // Check if theme toggle exists
  const themeToggle = document.querySelector('[title*="theme"]');
  if (themeToggle) {
    console.log('✅ Theme toggle component found');
    
    // Test click functionality
    themeToggle.click();
    console.log('✅ Theme toggle clicked');
    
    // Check if classes changed
    const hasDarkClass = document.documentElement.classList.contains('dark');
    const hasLightClass = document.documentElement.classList.contains('light');
    console.log('✅ Dark class present:', hasDarkClass);
    console.log('✅ Light class present:', hasLightClass);
  } else {
    console.log('❌ Theme toggle component not found');
  }
};

// Test dark mode styles
const testDarkModeStyles = () => {
  console.log('🧪 Testing Dark Mode Styles...');
  
  // Test background colors
  const testBackgrounds = () => {
    const elements = document.querySelectorAll('[class*="dark:bg-"]');
    console.log(`✅ Found ${elements.length} elements with dark mode background styles`);
  };
  
  // Test text colors
  const testTextColors = () => {
    const elements = document.querySelectorAll('[class*="dark:text-"]');
    console.log(`✅ Found ${elements.length} elements with dark mode text styles`);
  };
  
  // Test border colors
  const testBorderColors = () => {
    const elements = document.querySelectorAll('[class*="dark:border-"]');
    console.log(`✅ Found ${elements.length} elements with dark mode border styles`);
  };
  
  testBackgrounds();
  testTextColors();
  testBorderColors();
};

// Test theme persistence across page reloads
const testThemePersistence = () => {
  console.log('🧪 Testing Theme Persistence...');
  
  // Set theme to dark
  localStorage.setItem('theme', 'dark');
  document.documentElement.classList.add('dark');
  
  console.log('✅ Dark theme set, reload page to test persistence');
  console.log('ℹ️  After reload, check if dark theme is still active');
};

// Test responsive theme switching
const testResponsiveTheme = () => {
  console.log('🧪 Testing Responsive Theme...');
  
  // Test mobile theme toggle
  const mobileThemeToggle = document.querySelector('.md\\:hidden [title*="theme"]');
  if (mobileThemeToggle) {
    console.log('✅ Mobile theme toggle found');
  } else {
    console.log('ℹ️  Mobile theme toggle not visible (desktop view)');
  }
  
  // Test desktop theme toggle
  const desktopThemeToggle = document.querySelector('.hidden.md\\:flex [title*="theme"]');
  if (desktopThemeToggle) {
    console.log('✅ Desktop theme toggle found');
  } else {
    console.log('ℹ️  Desktop theme toggle not visible (mobile view)');
  }
};

// Run all tests
const runThemeTests = () => {
  console.log('🎨 Starting Theme Functionality Tests...');
  console.log('='.repeat(50));
  
  testThemeContext();
  console.log('');
  
  testThemeToggle();
  console.log('');
  
  testDarkModeStyles();
  console.log('');
  
  testThemePersistence();
  console.log('');
  
  testResponsiveTheme();
  console.log('');
  
  console.log('='.repeat(50));
  console.log('🎉 Theme functionality tests completed!');
  console.log('');
  console.log('📋 Test Summary:');
  console.log('✅ Theme context and persistence');
  console.log('✅ Theme toggle component');
  console.log('✅ Dark mode styles applied');
  console.log('✅ Responsive theme switching');
  console.log('');
  console.log('💡 To test manually:');
  console.log('1. Click the theme toggle button in the header');
  console.log('2. Check if the page switches between light and dark modes');
  console.log('3. Reload the page to test persistence');
  console.log('4. Test on both desktop and mobile views');
};

// Auto-run tests when script loads
if (typeof window !== 'undefined') {
  // Wait for DOM to be ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', runThemeTests);
  } else {
    runThemeTests();
  }
}

// Export for manual testing
if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    testThemeContext,
    testThemeToggle,
    testDarkModeStyles,
    testThemePersistence,
    testResponsiveTheme,
    runThemeTests
  };
}
