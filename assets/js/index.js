if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
  document.body.classList.add("dark");
}

function renderContributionGraph(container, days) {
  if (!container || !Array.isArray(days) || !days.length) return;

  const levels = {
    NONE: "0",
    FIRST_QUARTILE: "1",
    SECOND_QUARTILE: "2",
    THIRD_QUARTILE: "3",
    FOURTH_QUARTILE: "4",
  };

  const cells = days
    .map((day) => {
      const level = levels[day.level] || "0";
      const count = Number.isFinite(day.count) ? day.count : 0;
      const date = day.date || "";
      const title = `${count} contributions on ${date}`;
      return `<span class="gh-cell gh-level-${level}" title="${title}"></span>`;
    })
    .join("");

  container.innerHTML = cells;
}

async function loadGitHubActivity() {
  const linkEl = document.getElementById("gh-activity-link");
  const textEl = document.getElementById("gh-activity-text");
  const graphEl = document.getElementById("gh-activity-graph");
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
    renderContributionGraph(graphEl, activity.recent_days);
  } catch (error) {
    textEl.textContent = "GitHub activity";
    linkEl.href = "https://github.com/maxhabra";
    linkEl.title = "GitHub activity";
  }
}

loadGitHubActivity();
