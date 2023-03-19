let scrollBtnEl = document.querySelector(".scroll-to-target");
let mobileNavEl = document.querySelector(".mobile-menu");
let myTemplate = document.querySelector("template");
let footerCurrentYear = document.querySelector(".footer_curr_year");
let filterBox = document.querySelector(
  ".shop-page-section .filter-box .dropdown"
);
let searchWindowPopupEl = document.querySelector(".search-popup");
let preloaderEl = document.querySelector(".preloader");
let sidebarMenuToggler = document.querySelector(".toggler");
let navbarMenuToggler = document.querySelector(".nav-toggler");

if (sidebarMenuToggler) {
  sidebarMenuToggler.addEventListener("click", () => {
    let sidebarMenuContainer = document.querySelector(".menu-container");

    sidebarMenuContainer.classList.toggle("active");
  });
}

if (navbarMenuToggler) {
  navbarMenuToggler.addEventListener("click", () => {
    let navbarContainer = document.querySelector(".navbar-menu");

    navbarContainer.classList.toggle("is-active");
  });
}

footerCurrentYear
  ? (footerCurrentYear.textContent = new Date(Date.now()).getFullYear())
  : "";

if (scrollBtnEl) {
  scrollBtnEl.addEventListener("click", () => {
    window.scroll(0, 0);
  });

  window.addEventListener("scroll", scrollBtnFunc);
  window.addEventListener("load", scrollBtnFunc);

  function scrollBtnFunc() {
    if (window.scrollY > 150) {
      scrollBtnEl.classList.add("open");
    } else {
      scrollBtnEl.classList.remove("open");
    }
  }
}

if (mobileNavEl) {
  let mobileNavTogglerEl = document.querySelector(".mobile-nav-toggler");
  let mobileNaviagtionCont = mobileNavEl.querySelector(".menu-outer");
  mobileNaviagtionCont.append(myTemplate.content.cloneNode(true).children[0]);
  let closeMobileNavEl = mobileNavEl.querySelector(".close-btn");
  function toggleMobileNav() {
    if (mobileNavEl.classList.contains("mobile-menu-visible")) {
      mobileNavEl.classList.remove("mobile-menu-visible");
      mobileNavEl.style.visibility = "hidden";
      mobileNavEl.style.opacity = 0;
    } else {
      mobileNavEl.classList.add("mobile-menu-visible");
      mobileNavEl.classList.add("menu-backdrop");
      mobileNavEl.style.visibility = "visible";
      mobileNavEl.style.opacity = 1;
    }
  }
  mobileNavTogglerEl.addEventListener("click", toggleMobileNav);
  closeMobileNavEl.addEventListener("click", toggleMobileNav);
}

if (filterBox) {
  filterBox.addEventListener("click", () => {
    filterBox.classList.toggle("show");
  });
}

if (searchWindowPopupEl) {
  let searchCloseBtn = document.querySelector(".search-popup .close-search");
  let searchOverlayEl = document.querySelector(".search-popup .overlay-layer");
  let searchOpenBtns = document.querySelectorAll(".search-toggler");

  searchOpenBtns.forEach((searchOpenBtn) => {
    searchOpenBtn.addEventListener("click", () => {
      searchWindowPopupEl.classList.add("popup-visible");
    });
  });
  searchCloseBtn.addEventListener("click", closeSearchWindow);
  searchOverlayEl.addEventListener("click", closeSearchWindow);

  function closeSearchWindow() {
    searchWindowPopupEl.classList.remove("popup-visible");
  }
}

window.addEventListener("DOMContentLoaded", () => {
  if (preloaderEl) {
    setTimeout(() => {
      preloaderEl.style.display = "none";
    }, 1200);
  }
});
