const burger = document.querySelector('.burger');
const navLinks = document.querySelector('.nav-links');

const navSide = document.querySelector('.side-nav');
burger.addEventListener('click', () => {
    navSide.classList.toggle('active');
});

document.addEventListener('click', (event) => {
    if (!burger.contains(event.target) && !navSide.contains(event.target)) {
        navSide.classList.remove('active');
    }
});