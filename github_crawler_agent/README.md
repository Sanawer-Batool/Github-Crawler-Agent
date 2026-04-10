# GitHub Crawler Agent (CrewAI)

This project is a multi-agent GitHub candidate evaluator built with CrewAI.
It analyzes a developer's public GitHub profile and repositories, then generates a
structured hiring scorecard against a target role and job description.

## What This Project Does

Given:
- a GitHub username
- the role being applied for
- a job description

the crew:
1. Collects profile-level data (bio, followers, public repos, account age)
2. Pulls top repositories (sorted by stars)
3. Analyzes language usage for those repos
4. Reads and summarizes README content from top repos
5. Produces a fit scorecard with per-dimension scores and a final verdict

Verdict output is one of:
- `STRONG FIT`
- `MODERATE FIT`
- `WEAK FIT`

## How It Works (Architecture)

The workflow is sequential with two agents:

- **GitHub Profile Analyst** (`github_scraper_agent`)
  - Uses GitHub API tools to gather and summarize candidate evidence
- **Technical Fit Evaluator** (`summary_agent`)
  - Uses the previous analysis context to score candidate-role alignment

Task flow:
1. `scrape_github_task`
2. `evaluate_fit_task` (depends on task 1 output)

Core files:
- `src/github_crawler_agent/main.py` - entrypoint, candidate input payload
- `src/github_crawler_agent/crew.py` - crew, agents, tasks, model setup
- `src/github_crawler_agent/config/agents.yaml` - agent roles/goals/backstories
- `src/github_crawler_agent/config/tasks.yaml` - task prompts and output format
- `src/github_crawler_agent/tools/github_tools.py` - GitHub API tool functions

## Built-in Tools

The scraper agent can call:
- `get_candidate_github_report` (preferred one-shot report)
- `get_github_profile`
- `get_github_repos`
- `get_repo_languages`
- `get_repo_readme`

These tools use the GitHub REST API with token auth from environment variables.

## Setup

### Requirements

- Python `>=3.10, <=3.13`
- [uv](https://docs.astral.sh/uv/) (recommended)

### Install

```bash
pip install uv
crewai install
```

Or install directly with your preferred Python package workflow.

## Environment Configuration

Create/update `.env` with the keys below:

```env
MODEL=groq/llama-3.3-70b-versatile
GROQ_API_KEY=your_groq_api_key_here
GITHUB_TOKEN=your_github_token_here
```

Notes:
- `MODEL` defaults to `groq/llama-3.3-70b-versatile` if not set.
- `GITHUB_TOKEN` is recommended to avoid low unauthenticated rate limits.
- Never commit real keys to source control.

## Run

From the project root:

```bash
crewai run
```

The script currently uses hardcoded sample input in `main.py`:
- `github_username`
- `role_applied`
- `job_description`

Edit those values in `main.py` to evaluate different candidates/roles.

## Output Format

The final result is a structured scorecard including:
- Technical Skill Match
- Project Relevance
- Code Activity
- Communication Quality
- Overall Score
- Final Verdict
- Short summary rationale

## Customization Ideas

- Replace hardcoded `candidate_inputs` with CLI args or API input
- Add more signals (commit frequency, issue/PR activity, pinned repos)
- Add repo quality checks (tests, CI setup, project structure heuristics)
- Store outputs in JSON/DB for repeated screening workflows

## Security Reminder

If secrets were ever committed or shared accidentally, rotate them immediately:
- regenerate your LLM provider key
- regenerate your GitHub token

Then update `.env`, and keep `.env` excluded from git.
