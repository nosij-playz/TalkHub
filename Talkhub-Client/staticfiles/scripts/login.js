
  const imagePaths = [
    '/static/styles/image/Present/1.png',
    '/static/styles/image/Present/2.png',
    '/static/styles/image/Present/3.png',
    '/static/styles/image/Present/4.png',
    '/static/styles/image/Present/5.png'
    // Add as many as you have
  ];

  const imageElement = document.getElementById('animated-image');

  function showRandomImage() {
    const randomPath = imagePaths[Math.floor(Math.random() * imagePaths.length)];
    imageElement.style.opacity = 0;
    imageElement.style.transform = 'scale(0.95) rotate(-2deg)';

    setTimeout(() => {
      imageElement.src = randomPath;
      imageElement.onload = () => {
        imageElement.style.opacity = 1;
        imageElement.style.transform = 'scale(1) rotate(0)';
      };
    }, 300);
  }

  showRandomImage();
  setInterval(showRandomImage, 4000);

