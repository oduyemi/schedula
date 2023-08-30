var swiper = new Swiper(".mySwiper", {
  slidesPerView: 1,
  grabCursor:true,
  loop: true,
  loopFillGroupWithBlank: true,
  pagination: {
    el: ".swiper-pagination",
    clickable: true,
  },
  navigation: {
    nextEl: ".swiper-button-next",
    prevEl: ".swiper-button-prev",
  },
});

let i=0
let images=[];
let time=3000;

images[0]=
images[1]=
images[2]=
function changeImg(){
document._slide.src=images
if(i<(images.length)-1){
i++
}else{i=0}
}