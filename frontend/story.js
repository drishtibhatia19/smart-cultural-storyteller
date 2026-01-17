document.addEventListener("DOMContentLoaded", () => {
  const storyData = JSON.parse(localStorage.getItem("storyData"));

  if (!storyData || !storyData.scenes?.length) {
    alert("No story data found. Please generate a story first.");
    return;
  }

  const sceneTitle = document.getElementById("sceneTitle");
  const sceneText = document.getElementById("sceneText");
  const counter = document.getElementById("sceneCounter");

  const prevBtn = document.getElementById("prevBtn");
  const nextBtn = document.getElementById("nextBtn");

  const imageBtn = document.getElementById("generateImageBtn");
  const narrationBtn = document.getElementById("generateNarrationBtn");
  const videoBtn = document.getElementById("generateVideoBtn");

  const sceneImage = document.getElementById("sceneImage");
  const sceneAudio = document.getElementById("sceneAudio");

  let index = 0;

  function renderScene() {
  const scene = storyData.scenes[index];

  sceneTitle.innerHTML = `<h2>${scene.title}</h2>`;
  sceneText.innerHTML = `<p>${scene.text}</p>`;

  counter.innerText = `Scene ${index + 1} of ${storyData.scenes.length}`;

  sceneImage.src = "";
  sceneImage.style.display = "none";

  sceneAudio.pause();
  sceneAudio.src = "";
  sceneAudio.style.display = "none";

  prevBtn.disabled = index === 0;
  nextBtn.disabled = index === storyData.scenes.length - 1;
}


  prevBtn.onclick = () => { if (index > 0) { index--; renderScene(); } };
  nextBtn.onclick = () => { if (index < storyData.scenes.length - 1) { index++; renderScene(); } };

  imageBtn.onclick = async () => {
    imageBtn.disabled = true;
    imageBtn.innerText = "Generating...";

    const scene = storyData.scenes[index];

    try {
      const res = await fetch("/api/generate-image", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title: scene.title, text: scene.text })
      });

      const data = await res.json();

      scene.image_url = data.image_url;
      sceneImage.src = data.image_url;
      sceneImage.style.display = "block";

    } catch {
      alert("Failed to generate image");
    }

    imageBtn.innerText = "🖼 Generate Image";
    imageBtn.disabled = false;
  };

  narrationBtn.onclick = async () => {
    narrationBtn.disabled = true;
    narrationBtn.innerText = "Narrating...";

    const scene = storyData.scenes[index];

    try {
      const res = await fetch("/api/generate-narration", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title: scene.title, text: scene.text })
      });

      const data = await res.json();

      scene.audio_url = data.audio_url;
      sceneAudio.src = data.audio_url;
      sceneAudio.style.display = "block";
      sceneAudio.play();

    } catch {
      alert("Failed to generate narration");
    }

    narrationBtn.innerText = "🎧 Narrate Scene";
    narrationBtn.disabled = false;
  };

  videoBtn.onclick = async () => {
    const scene = storyData.scenes[index];

    if (!scene.image_url || !scene.audio_url) {
      alert("Generate image and narration first");
      return;
    }

    videoBtn.disabled = true;
    videoBtn.innerText = "🎬 Generating...";

    try {
      const res = await fetch("/api/generate-video", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          title: scene.title,
          image_url: scene.image_url,
          audio_url: scene.audio_url
        })
      });

      const data = await res.json();
      window.open(data.video_url, "_blank");

    } catch {
      alert("Video generation failed");
    }

    videoBtn.innerText = "🎬 Generate Video";
    videoBtn.disabled = false;
  };

  renderScene();
});
