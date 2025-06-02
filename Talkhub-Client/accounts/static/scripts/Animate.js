document.addEventListener("DOMContentLoaded", function () {
  const staticBase = "/static/"; // Set your static prefix here

  const imagePaths = [
    staticBase + "styles/image/Present/1.png",
    staticBase + "styles/image/Present/2.png",
    staticBase + "styles/image/Present/3.png",
    staticBase + "styles/image/Present/4.png",
    staticBase + "styles/image/Present/5.png",
    staticBase + "styles/image/Present/6.png"
  ];

  const imageElement = document.getElementById("animated-image");

  function showRandomImage() {
    const randomPath = imagePaths[Math.floor(Math.random() * imagePaths.length)];
    imageElement.style.opacity = 0;
    imageElement.style.transform = "scale(0.95) rotate(-2deg)";
    imageElement.style.animation = "none"; // reset animation

    setTimeout(() => {
      imageElement.src = randomPath;
      imageElement.onload = () => {
        // Trigger morph animation
        imageElement.style.animation = "fadeInScaleMorph 1s ease-in-out forwards";
      };
    }, 200);
  }

  showRandomImage();
  setInterval(showRandomImage, 4000);
});
