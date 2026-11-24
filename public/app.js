let appData = null;
let currentWindow = "7d"; // "7d" or "14d"

async function init() {
  try {
    const res = await fetch("data.json");
    if (!res.ok) throw new Error("Could not load data.json");
    appData = await res.json();
    render();
  } catch (err) {
    console.error(err);
    document.getElementById("hero-headline").innerText = "Ready to Sync";
    document.getElementById("hero-summary").innerText = "Connect your Hevy API key to view your live recommendations.";
  }
}

function render() {
  if (!appData) return;

  // 1. Last Updated
  document.getElementById("last-updated").innerText = `Updated: ${appData.generated_at}`;

  // 2. Hero Section
  const rec = appData.today_recommendation;
  document.getElementById("hero-headline").innerText = rec.headline;
  document.getElementById("hero-summary").innerText = rec.summary;

  const tagsContainer = document.getElementById("recommended-tags");
  tagsContainer.innerHTML = "";
  if (rec.focus_muscles && rec.focus_muscles.length > 0) {
    rec.focus_muscles.forEach(muscle => {
      const tag = document.createElement("span");
      tag.className = "tag-focus";
      tag.innerHTML = `✓ <strong>${muscle}</strong> (Ready & Priority)`;
      tagsContainer.appendChild(tag);
    });
  } else {
    tagsContainer.innerHTML = `<span class="tag-focus" style="background:#f1f5f9; color:#475569; border-color:#cbd5e1;">All muscle targets completed! Rest or active recovery.</span>`;
  }

  // 3. Muscle Grid
  renderMuscles();

  // 4. Recent Workouts
  const workoutList = document.getElementById("workout-list");
  workoutList.innerHTML = "";
  if (appData.recent_workouts && appData.recent_workouts.length > 0) {
    appData.recent_workouts.forEach(w => {
      const item = document.createElement("div");
      item.className = "workout-item";
      const timeLabel = w.hours_ago < 24 ? `${Math.round(w.hours_ago)}h ago` : `${Math.round(w.hours_ago / 24)}d ago`;
      item.innerHTML = `
        <div>
          <div class="workout-item-title">${w.title}</div>
          <div class="workout-item-date">${w.date} (${timeLabel})</div>
        </div>
        <div class="workout-item-sets">${w.total_sets} sets</div>
      `;
      workoutList.appendChild(item);
    });
  } else {
    workoutList.innerHTML = `<p style="font-size:0.8rem; color:#64748b;">No recent workouts logged.</p>`;
  }
}

function renderMuscles() {
  const grid = document.getElementById("muscle-grid");
  grid.innerHTML = "";

  const is7d = currentWindow === "7d";

  // Sort: Ready muscles with largest deficits first, then recovering, then resting
  const sorted = [...appData.muscles].sort((a, b) => {
    const statusOrder = { ready: 0, recovering: 1, resting: 2 };
    if (statusOrder[a.recovery_status] !== statusOrder[b.recovery_status]) {
      return statusOrder[a.recovery_status] - statusOrder[b.recovery_status];
    }
    return (b.weekly_target - b.sets_7d) - (a.weekly_target - a.sets_7d);
  });

  sorted.forEach(m => {
    const sets = is7d ? m.sets_7d : m.sets_14d;
    const target = is7d ? m.weekly_target : (m.weekly_target * 2);
    const pct = Math.min(100, Math.round((sets / target) * 100));

    const card = document.createElement("div");
    card.className = "muscle-card";

    let barColor = "#10b981"; // ready: green
    if (m.recovery_status === "recovering") barColor = "#f59e0b"; // yellow
    if (m.recovery_status === "resting") barColor = "#3b82f6"; // blue

    card.innerHTML = `
      <div class="muscle-card-top">
        <span class="muscle-name">${m.name}</span>
        <span class="badge-status ${m.recovery_status}">${m.recovery_status}</span>
      </div>
      <div class="muscle-rest-info">Last hit: ${m.rest_label}</div>
      <div class="progress-container">
        <div class="progress-label-row">
          <span class="sets-done">${sets} sets</span>
          <span class="sets-target">Goal: ${target} sets (${pct}%)</span>
        </div>
        <div class="progress-bar-bg">
          <div class="progress-bar-fill" style="width: ${pct}%; background: ${barColor}"></div>
        </div>
      </div>
    `;
    grid.appendChild(card);
  });
}

// Toggle handlers
document.getElementById("btn-7d").addEventListener("click", () => {
  currentWindow = "7d";
  document.getElementById("btn-7d").classList.add("active");
  document.getElementById("btn-14d").classList.remove("active");
  renderMuscles();
});

document.getElementById("btn-14d").addEventListener("click", () => {
  currentWindow = "14d";
  document.getElementById("btn-14d").classList.add("active");
  document.getElementById("btn-7d").classList.remove("active");
  renderMuscles();
});

document.addEventListener("DOMContentLoaded", init);
