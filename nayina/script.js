let currentSlide = 0;
const slides = document.querySelectorAll(".carousel-slide");
const totalSlides = slides.length;

function nextSlide() {
  currentSlide = (currentSlide + 1) % totalSlides;
  showSlide(currentSlide);
}

function prevSlide() {
  currentSlide = (currentSlide - 1 + totalSlides) % totalSlides;
  showSlide(currentSlide);
}

function goToSlide(n) {
  currentSlide = n;
  showSlide(currentSlide);
}

function showSlide(n) {
  const track = document.getElementById("carouselTrack");
  track.style.transform = `translateX(-${n * 100}%)`;
}

// 自动切换功能
function autoSlide() {
  setInterval(nextSlide, 5000); // 每5秒切换一次
}

// 初始化轮播图
window.onload = function () {
  showSlide(currentSlide);
  autoSlide();
};
