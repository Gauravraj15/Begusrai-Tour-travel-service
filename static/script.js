        // Mobile Navigation JavaScript
        const openMenuBtn = document.getElementById('open-menu');
        const closeMenuBtn = document.getElementById('close-menu');
        const mobileNav = document.getElementById('mobile-nav');
        const mainContent = document.getElementById('main-content');

        // Open mobile navigation
        openMenuBtn.addEventListener('click', () => {
            mobileNav.classList.add('active');
            mainContent.classList.add('hide');
        });

        // Close mobile navigation
        closeMenuBtn.addEventListener('click', () => {
            mobileNav.classList.remove('active');
            mainContent.classList.remove('hide');
        });

        // Close mobile nav when clicking on a link
        const mobileNavLinks = document.querySelectorAll('.mobile-nav-list a');
        mobileNavLinks.forEach(link => {
            link.addEventListener('click', () => {
                mobileNav.classList.remove('active');
                mainContent.classList.remove('hide');
            });
        });

        // Close mobile nav when clicking outside
        mobileNav.addEventListener('click', (e) => {
            if (e.target === mobileNav) {
                mobileNav.classList.remove('active');
                mainContent.classList.remove('hide');
            }
        });
    
          document.getElementById('open-menu').addEventListener('click', function () {
      document.getElementById('mobile-nav').style.display = 'block';
    });

    document.getElementById('close-menu').addEventListener('click', function () {
      document.getElementById('mobile-nav').style.display = 'none';

      
    });
  setTimeout(function () {
    const welcome = document.getElementById('welcome-message');
    if (welcome) {
      welcome.style.display = 'none';
    }
  }, 5000);  // 5000 milliseconds = 5 seconds

