let dropDown = document.querySelector('.drop_down');
let shopLink = document.querySelector('.shop_link');
let homeLink = document.querySelector('.home_link');
let featuredLink = document.querySelector('.featured_link');
let landingHero = document.querySelector('.login_register_landing_hero');


shopLink.onmouseover = () => {
    dropDown.classList.add('active');
}

dropDown.onmouseover = () => {
    dropDown.classList.add('active');
}

homeLink.onmouseover = () => {
    dropDown.classList.remove('active');
}


featuredLink.onmouseover = () => {
    dropDown.classList.remove('active');
}


landingHero.onmouseover = () => {
    dropDown.classList.remove('active');
}