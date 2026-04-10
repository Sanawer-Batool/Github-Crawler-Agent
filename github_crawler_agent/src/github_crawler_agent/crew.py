import os

from crewai import Agent, Task, Crew, Process
from crewai.project import CrewBase, agent, task, crew
from .tools.github_tools import (
    get_github_profile,
    get_github_repos,
    get_repo_languages,
    get_repo_readme,
    get_candidate_github_report,
)


@CrewBase
class GithubCrawlerCrew:
    """GitHub Crawler Crew — analyzes a candidate's GitHub and scores their fit."""

    agents_config = "config/agents.yaml"
    tasks_config  = "config/tasks.yaml"
    llm_model = os.getenv("MODEL", "groq/llama-3.3-70b-versatile")

    # ── Agents ────────────────────────────────────────────────────────────────

    @agent
    def github_scraper_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["github_scraper_agent"],
            tools=[
                get_candidate_github_report,
                get_github_profile,
                get_github_repos,
                get_repo_languages,
                get_repo_readme,
            ],
            llm=self.llm_model,
            verbose=True,
        )

    @agent
    def summary_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["summary_agent"],
            tools=[],   # no tools needed — works purely from context
            llm=self.llm_model,
            verbose=True,
        )

    # ── Tasks ─────────────────────────────────────────────────────────────────

    @task
    def scrape_github_task(self) -> Task:
        return Task(
            config=self.tasks_config["scrape_github_task"],
            agent=self.github_scraper_agent(),
        )

    @task
    def evaluate_fit_task(self) -> Task:
        return Task(
            config=self.tasks_config["evaluate_fit_task"],
            agent=self.summary_agent(),
            context=[self.scrape_github_task()],
        )

    # ── Crew ──────────────────────────────────────────────────────────────────

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )