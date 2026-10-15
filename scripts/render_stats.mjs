// Use the original GitHub Readme Stats renderer with public aggregate data.
// stargazerCount is sufficient; the stargazers connection needs broader access.
import { writeFile } from 'node:fs/promises';
import { renderStatsCard } from '../vendor/github-readme-stats/src/cards/stats.js';
import { calculateRank } from '../vendor/github-readme-stats/src/calculateRank.js';

const username = process.env.GITHUB_REPOSITORY_OWNER || 'DevXingMC';
const token = process.env.GITHUB_TOKEN;
if (!token) throw new Error('GITHUB_TOKEN is required');

const query = `query Profile($login: String!, $after: String) {
  user(login: $login) {
    login
    commits: contributionsCollection { totalCommitContributions }
    reviews: contributionsCollection { totalPullRequestReviewContributions }
    repositoriesContributedTo(first: 1, contributionTypes: [COMMIT, ISSUE, PULL_REQUEST, REPOSITORY]) { totalCount }
    pullRequests(first: 1) { totalCount }
    openIssues: issues(states: OPEN) { totalCount }
    closedIssues: issues(states: CLOSED) { totalCount }
    followers { totalCount }
    repositories(first: 100, privacy: PUBLIC, ownerAffiliations: OWNER, after: $after) {
      totalCount
      nodes { stargazerCount }
      pageInfo { hasNextPage endCursor }
    }
  }
}`;

let user;
let cursor = null;
let stars = 0;
do {
  const response = await fetch('https://api.github.com/graphql', {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${token}`,
      'Content-Type': 'application/json',
      'User-Agent': 'DevXingMC-profile',
    },
    body: JSON.stringify({ query, variables: { login: username, after: cursor } }),
    signal: AbortSignal.timeout(30000),
  });
  if (!response.ok) throw new Error(`GitHub returned HTTP ${response.status}`);
  const result = await response.json();
  if (result.errors?.length) {
    throw new Error(result.errors.map(error => error.message).join('; '));
  }
  user = result.data?.user;
  if (!user) throw new Error('GitHub returned no user data');
  stars += user.repositories.nodes.reduce((total, repo) => total + repo.stargazerCount, 0);
  cursor = user.repositories.pageInfo.hasNextPage ? user.repositories.pageInfo.endCursor : null;
} while (cursor);

const stats = {
  name: user.login,
  totalStars: stars,
  totalCommits: user.commits.totalCommitContributions,
  totalPRs: user.pullRequests.totalCount,
  totalIssues: user.openIssues.totalCount + user.closedIssues.totalCount,
  totalReviews: user.reviews.totalPullRequestReviewContributions,
  contributedTo: user.repositoriesContributedTo.totalCount,
};
for (const [name, value] of Object.entries(stats)) {
  if (name !== 'name' && (!Number.isSafeInteger(value) || value < 0)) {
    throw new Error(`Invalid metric: ${name}`);
  }
}
stats.rank = calculateRank({
  all_commits: false, commits: stats.totalCommits, prs: stats.totalPRs,
  reviews: stats.totalReviews, issues: stats.totalIssues, stars: stats.totalStars,
  repos: user.repositories.totalCount, followers: user.followers.totalCount,
});
const svg = renderStatsCard(stats, {
  show_icons: true,
  hide_rank: true,
  bg_color: '0d1424',
  title_color: '70d8ef',
  text_color: 'bfccde',
  icon_color: '70d8ef',
  border_color: '26354c',
  border_radius: 16,
  card_width: 460,
  custom_title: 'GitHub activity',
  disable_animations: true,
});
await writeFile(new URL('../assets/github-stats.svg', import.meta.url), svg);
console.log(`Rendered public activity for ${username}.`);
