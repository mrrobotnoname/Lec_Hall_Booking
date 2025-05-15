const header = document.querySelector("header");

window.addEventListener("scroll", function () {
    header.classList.toggle("sticky", window.scrollY > 0);
});

let menu = document.querySelector('#menu-icon');
let navbar = document.querySelector('.navbar');

menu.onclick = () => {
    menu.classList.toggle('bx-x');
    navbar.classList.toggle('open');
}

window.onscroll = () => {
    menu.classList.remove('bx-x');
    navbar.classList.remove('open');
}


function selectButton(Department) {
    // Store the selected department (you can use localStorage or sessionStorage)
    sessionStorage.setItem('selectButton', Department);
    
    // Redirect back to main page or to next step
    window.location.href = 'index.html';
}
