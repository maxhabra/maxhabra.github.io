if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
  document.body.classList.add("dark");
}

async function loadGitHubActivity() {
  const linkEl = document.getElementById("gh-activity-link");
  const textEl = document.getElementById("gh-activity-text");
  if (!linkEl || !textEl) return;

  function resolveContributionCount(activity) {
    const directCount = Number(activity?.yearly_contributions);
    if (Number.isFinite(directCount) && directCount >= 0) return directCount;

    const fallbackKeys = [
      "total_contributions",
      "contributions_last_year",
      "annual_contributions",
    ];
    for (const key of fallbackKeys) {
      const count = Number(activity?.[key]);
      if (Number.isFinite(count) && count >= 0) return count;
    }

    const summary = typeof activity?.summary === "string" ? activity.summary : "";
    const match = summary.match(/(\d[\d,]*)\s+contributions?\s+in\s+the\s+last\s+year/i);
    if (match) {
      const parsed = Number(match[1].replace(/,/g, ""));
      if (Number.isFinite(parsed) && parsed >= 0) return parsed;
    }

    return null;
  }

  try {
    const response = await fetch("./assets/data/github-activity.json", { cache: "no-store" });
    if (!response.ok) throw new Error("Activity file not available");

    const activity = await response.json();
    const profileUrl = activity.profile_url || "https://github.com/maxhabra";
    const yearlyContributions = resolveContributionCount(activity);

    if (yearlyContributions !== null) {
      textEl.textContent = `${yearlyContributions} contributions in the last year`;
    } else {
      textEl.textContent = "GitHub contributions";
    }

    linkEl.href = activity.activity_url || profileUrl;
    linkEl.title = activity.summary || "GitHub contributions";
  } catch (error) {
    textEl.textContent = "GitHub contributions";
    linkEl.href = "https://github.com/maxhabra";
    linkEl.title = "GitHub contributions";
  }
}

loadGitHubActivity();
