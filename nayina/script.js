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

var btc1 = "#df5e9a";
var btc2 = "#dc86b0";

var button1 = document.getElementById("tbt1");
var button2 = document.getElementById("tbt2");

button1.addEventListener("click", function () {
  // 改变按钮的背景颜色
  button1.style.backgroundColor = btc1;
  button2.style.backgroundColor = btc2;
});

button2.addEventListener("click", function () {
  // 改变按钮的背景颜色
  button2.style.backgroundColor = btc1;
  button1.style.backgroundColor = btc2;
});

//文本切换
