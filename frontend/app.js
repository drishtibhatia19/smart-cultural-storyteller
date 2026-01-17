document.addEventListener("DOMContentLoaded", () => {
  console.log("✅ app.js loaded");


const craftingOverlay = document.getElementById("craftingOverlay");
const craftingText = document.getElementById("craftingText");

const craftingMessages = [
  "Your story is being crafted...",
  "Weaving fate, myth, and imagination...",
  "Shaping characters and destiny...",
  "Almost there..."
];

let craftingInterval;

function showCrafting() {
  if (!craftingOverlay) return;

  let i = 0;
  craftingText.textContent = craftingMessages[0];
  craftingOverlay.classList.remove("hidden");

  craftingInterval = setInterval(() => {
    i = (i + 1) % craftingMessages.length;
    craftingText.textContent = craftingMessages[i];
  }, 2200);
}

function hideCrafting() {
  clearInterval(craftingInterval);
  craftingOverlay?.classList.add("hidden");
}


  const startBtn = document.getElementById("startBtn");
  const generateBtn = document.getElementById("generateBtn");
  const card = document.getElementById("controlsCard");

  if (!startBtn || !generateBtn || !card) {
    console.error("❌ Required elements missing", {
      startBtn,
      generateBtn,
      card
    });
    return;
  }

  startBtn.addEventListener("click", () => {
    card.classList.remove("hidden");
  });

  generateBtn.addEventListener("click", async () => {
    console.log("🔥 Generate button clicked");

    const getValue = (type) =>
      document.querySelector(`[data-type="${type}"] .dropdown-selected .text`)
        ?.innerText.trim();

    const anchorText = document.getElementById("userInput")?.value.trim();

    if (!anchorText) {
      alert("Please describe what the story should be about.");
      return;
    }
    
    showCrafting();

    const payload = {
      culture: getValue("culture"),
      mode: document.querySelector('input[name="mode"]:checked').value,
      emotion: getValue("emotion"),
      moral: getValue("lesson"),
      user_input: document.getElementById("userInput").value.trim()
    };


    console.log("🧠 Sending payload:", payload);

    try {
      const res = await fetch("/api/generate-story", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });

      if (!res.ok) {
        const err = await res.text();
        console.error("❌ Backend error:", err);
        alert("Failed to generate story");
        return;
      }

      const data = await res.json();
      localStorage.setItem("storyData", JSON.stringify(data));
      window.location.href = "/frontend/story.html";
    } catch (err) {
      console.error("❌ Network error:", err);
      alert("Failed to generate story");
    }
  });
});
