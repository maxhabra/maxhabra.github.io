if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
  document.body.classList.add("dark");
}

async function loadGitHubActivity() {
  const linkEl = document.getElementById("gh-activity-link");
  const textEl = document.getElementById("gh-activity-text");
  if (!linkEl || !textEl) return;

  try {
    const response = await fetch("./assets/data/github-activity.json", { cache: "no-store" });
    if (!response.ok) throw new Error("Activity file not available");

    const activity = await response.json();
    const profileUrl = activity.profile_url || "https://github.com/maxhabra";
    const yearlyContributions = Number.isFinite(activity.yearly_contributions)
      ? activity.yearly_contributions
      : null;

    if (yearlyContributions !== null) {
      textEl.textContent = `${yearlyContributions} contributions in the last year`;
    } else {
      textEl.textContent = "GitHub activity";
    }

    linkEl.href = activity.activity_url || profileUrl;
    linkEl.title = activity.summary || "GitHub activity";
  } catch (error) {
    textEl.textContent = "GitHub activity";
    linkEl.href = "https://github.com/maxhabra";
    linkEl.title = "GitHub activity";
  }
}

loadGitHubActivity();
