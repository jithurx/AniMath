// DOM Elements
document.addEventListener('DOMContentLoaded', function() {
    // Smooth scrolling for navigation links
    const navLinks = document.querySelectorAll('nav a');
    
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            const targetSection = document.querySelector(targetId);
            
            window.scrollTo({
                top: targetSection.offsetTop - 80,
                behavior: 'smooth'
            });
        });
    });
    
    // FAQ Accordion functionality
    const faqQuestions = document.querySelectorAll('.faq-question');
    
    faqQuestions.forEach(question => {
        question.addEventListener('click', function() {
            const answer = this.nextElementSibling;
            const isOpen = answer.style.display === 'block';
            
            // Close all other answers
            document.querySelectorAll('.faq-answer').forEach(item => {
                item.style.display = 'none';
            });
            
            document.querySelectorAll('.faq-question').forEach(item => {
                item.querySelector('.toggle-icon').textContent = '+';
            });
            
            // Toggle current answer
            if (!isOpen) {
                answer.style.display = 'block';
                this.querySelector('.toggle-icon').textContent = '−';
            }
        });
    });
    
    // Initialize all FAQ items as closed
    document.querySelectorAll('.faq-answer').forEach(item => {
        item.style.display = 'none';
    });
    
    // Add toggle icons to FAQ questions
    document.querySelectorAll('.faq-question').forEach(item => {
        const toggleIcon = document.createElement('span');
        toggleIcon.className = 'toggle-icon';
        toggleIcon.textContent = '+';
        item.appendChild(toggleIcon);
    });
    
    // Download button click tracking
    const downloadButtons = document.querySelectorAll('.download-option .btn');
    
    downloadButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            const platform = this.getAttribute('data-platform');
            console.log(`Download clicked for platform: ${platform}`);
            
            // Show download starting message
            alert(`Your download will start. Thank you for testing AniMath!`);
        });
    });
    
    // Gallery image hover effects
    const galleryItems = document.querySelectorAll('.gallery-item');
    
    galleryItems.forEach(item => {
        item.addEventListener('mouseenter', function() {
            const caption = this.querySelector('.gallery-caption');
            caption.style.transform = 'translateY(0)';
        });
        
        item.addEventListener('mouseleave', function() {
            const caption = this.querySelector('.gallery-caption');
            caption.style.transform = 'translateY(100%)';
        });
    });
    
    // Mobile menu toggle
    const createMobileMenu = () => {
        const header = document.querySelector('header');
        const nav = document.querySelector('nav');
        
        // Create mobile menu button
        const mobileMenuBtn = document.createElement('button');
        mobileMenuBtn.className = 'mobile-menu-btn';
        mobileMenuBtn.innerHTML = '☰';
        
        // Add mobile menu button to header
        header.querySelector('.header-content').appendChild(mobileMenuBtn);
        
        // Mobile menu functionality
        mobileMenuBtn.addEventListener('click', function() {
            nav.classList.toggle('active');
        });
        
        // Add CSS for mobile menu
        const style = document.createElement('style');
        style.textContent = `
            @media (max-width: 768px) {
                nav {
                    display: none;
                    width: 100%;
                }
                
                nav.active {
                    display: block;
                }
                
                nav ul {
                    flex-direction: column;
                    align-items: center;
                }
                
                nav ul li {
                    margin: 0.5rem 0;
                }
                
                .mobile-menu-btn {
                    display: block;
                    background: none;
                    border: none;
                    color: white;
                    font-size: 1.5rem;
                    cursor: pointer;
                }
            }
            
            @media (min-width: 769px) {
                .mobile-menu-btn {
                    display: none;
                }
                
                nav {
                    display: block !important;
                }
            }
        `;
        
        document.head.appendChild(style);
    };
    
    // Check if on mobile
    if (window.innerWidth <= 768) {
        createMobileMenu();
    }
    
    window.addEventListener('resize', function() {
        if (window.innerWidth <= 768 && !document.querySelector('.mobile-menu-btn')) {
            createMobileMenu();
        }
    });
    
    // Lazy loading for images
    if ('IntersectionObserver' in window) {
        const imgOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px 200px 0px'
        };
        
        const imgObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    const src = img.getAttribute('data-src');
                    if (src) {
                        img.src = src;
                        img.removeAttribute('data-src');
                    }
                    observer.unobserve(img);
                }
            });
        }, imgOptions);
        
        document.querySelectorAll('img[data-src]').forEach(img => {
            imgObserver.observe(img);
        });
    }
    
    // Form validation for contact form
    const contactForm = document.getElementById('contact-form');
    
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const nameInput = document.getElementById('name');
            const emailInput = document.getElementById('email');
            const messageInput = document.getElementById('message');
            
            let isValid = true;
            
            // Simple validation
            if (nameInput.value.trim() === '') {
                markInvalid(nameInput, 'Please enter your name');
                isValid = false;
            } else {
                markValid(nameInput);
            }
            
            if (emailInput.value.trim() === '' || !isValidEmail(emailInput.value)) {
                markInvalid(emailInput, 'Please enter a valid email address');
                isValid = false;
            } else {
                markValid(emailInput);
            }
            
            if (messageInput.value.trim() === '') {
                markInvalid(messageInput, 'Please enter your message');
                isValid = false;
            } else {
                markValid(messageInput);
            }
            
            if (isValid) {
                // Simulate form submission
                alert('Thank you for your message! We will get back to you soon.');
                contactForm.reset();
            }
        });
    }
    
    function markInvalid(element, message) {
        element.classList.add('invalid');
        
        // Create or update error message
        let errorDiv = element.nextElementSibling;
        if (!errorDiv || !errorDiv.classList.contains('error-message')) {
            errorDiv = document.createElement('div');
            errorDiv.className = 'error-message';
            element.parentNode.insertBefore(errorDiv, element.nextSibling);
        }
        
        errorDiv.textContent = message;
    }
    
    function markValid(element) {
        element.classList.remove('invalid');
        
        // Remove error message if exists
        const errorDiv = element.nextElementSibling;
        if (errorDiv && errorDiv.classList.contains('error-message')) {
            errorDiv.remove();
        }
    }
    
    function isValidEmail(email) {
        const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return regex.test(email);
    }
    
    // Add animation to features on scroll
    const animateOnScroll = () => {
        const features = document.querySelectorAll('.feature');
        
        const featureObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate');
                    featureObserver.unobserve(entry.target);
                }
            });
        }, { threshold: 0.2 });
        
        features.forEach(feature => {
            featureObserver.observe(feature);
        });
        
        // Add CSS for animations
        const style = document.createElement('style');
        style.textContent = `
            .feature {
                opacity: 0;
                transform: translateY(20px);
                transition: opacity 0.5s ease, transform 0.5s ease;
            }
            
            .feature.animate {
                opacity: 1;
                transform: translateY(0);
            }
        `;
        
        document.head.appendChild(style);
    };
    
    if ('IntersectionObserver' in window) {
        animateOnScroll();
    }
    
    // Newsletter subscription
    const newsletterForm = document.getElementById('newsletter-form');
    
    if (newsletterForm) {
        newsletterForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const emailInput = this.querySelector('input[type="email"]');
            
            if (emailInput.value.trim() === '' || !isValidEmail(emailInput.value)) {
                alert('Please enter a valid email address');
                return;
            }
            
            // Simulate subscription
            alert('Thank you for subscribing to our newsletter!');
            newsletterForm.reset();
        });
    }
});
