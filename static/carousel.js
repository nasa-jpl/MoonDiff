const slidesContainer = document.getElementById("slides-container");
const slide = document.querySelector(".slide");
const prevButton = document.getElementById("slide-arrow-prev");
const nextButton = document.getElementById("slide-arrow-next");
const slideWidth = slide.clientWidth;

const goForwards = ()=>{
    if (slidesContainer.scrollLeft < slidesContainer.scrollWidth - slideWidth - 50){
        slidesContainer.scrollLeft += slideWidth;
    } else {
        slidesContainer.scrollLeft = 0;
    }
}

const goBackwards = ()=>{
    if (slidesContainer.scrollLeft > 0){
        slidesContainer.scrollLeft -= slideWidth;
    } else {
        slidesContainer.scrollLeft = slidesContainer.scrollWidth - slideWidth;
    }
}

nextButton.addEventListener("click",goForwards);

prevButton.addEventListener("click", goBackwards);

setInterval(goForwards, 10000);