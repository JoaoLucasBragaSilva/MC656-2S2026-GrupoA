document.addEventListener('DOMContentLoaded', () => {
    // Menu mobile
    const toggle = document.getElementById('nav-toggle');
    const links = document.querySelector('.navbar-links');
    const actions = document.querySelector('.navbar-actions');

    if (toggle) {
        toggle.addEventListener('click', () => {
            const isOpen = toggle.classList.toggle('open');
            [links, actions].forEach(el => {
                if (!el) return;
                el.style.display = isOpen ? 'flex' : '';
                if (isOpen) {
                    el.style.position = 'absolute';
                    el.style.top = '100%';
                    el.style.left = '0';
                    el.style.right = '0';
                    el.style.flexDirection = 'column';
                    el.style.background = '#fff';
                    el.style.padding = '20px 32px';
                    el.style.borderBottom = '1px solid var(--gray-200)';
                    el.style.gap = '16px';
                } else {
                    el.style = '';
                }
            });
        });
    }

    // Scroll suave para âncoras
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const target = document.querySelector(this.getAttribute('href'));
            if (!target) return;
            e.preventDefault();
            target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        });
    });

    // Animação de entrada das sections
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, { threshold: 0.1 });

    document.querySelectorAll('.election-card, .step, .security-list li').forEach((el, i) => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        el.style.transition = `opacity 0.6s ease ${i * 0.08}s, transform 0.6s ease ${i * 0.08}s`;
        observer.observe(el);
    });

    // Simular atualização dos percentuais do card
    const fill = document.querySelector('.progress-fill');
    if (fill) {
        const originalWidth = fill.style.width;
        fill.style.width = '0%';
        setTimeout(() => { fill.style.width = originalWidth; }, 400);
    }
});