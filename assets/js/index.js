if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
  document.body.classList.add("dark");
}

async function loadGitHubActivity() {
  const activityEl = document.getElementById("gh-activity");
  if (!activityEl) return;

  try {
    const response = await fetch("./assets/data/github-activity.json", { cache: "no-store" });
    if (!response.ok) throw new Error("Activity file not available");

    const activity = await response.json();
    const profileUrl = activity.profile_url || "https://github.com/maxhabra";
    const weekEvents = Number.isFinite(activity.week_events) ? activity.week_events : null;
    const lastEventDate = activity.last_event_date || null;

    const parts = [];
    if (weekEvents !== null) parts.push(`7d: ${weekEvents}`);
    if (lastEventDate) parts.push(`last: ${lastEventDate}`);

    activityEl.textContent = parts.length ? parts.join(" | ") : "GitHub activity";
    activityEl.href = activity.activity_url || profileUrl;
    activityEl.title = activity.summary || "GitHub activity";
  } catch (error) {
    activityEl.textContent = "GitHub activity";
    activityEl.href = "https://github.com/maxhabra";
    activityEl.title = "GitHub activity";
  }
}

loadGitHubActivity();
