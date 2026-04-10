import sys

from dotenv import load_dotenv
load_dotenv()

from .crew import GithubCrawlerCrew


def _configure_console_encoding() -> None:
    """Force UTF-8 output on Windows terminals to avoid charmap crashes."""
    for stream_name in ("stdout", "stderr"):
        stream = getattr(sys, stream_name, None)
        if stream is None:
            continue
        reconfigure = getattr(stream, "reconfigure", None)
        if callable(reconfigure):
            reconfigure(encoding="utf-8", errors="replace")


def run():
    """
    Entry point — called by `crewai run`.
    Edit candidate_inputs below to test with different GitHub profiles.
    """

    _configure_console_encoding()

    # ── Candidate data (hardcoded for practice) ───────────────────────────────
    candidate_inputs = {
        "github_username": "Sanawer-Batool",          # ← swap to any GitHub username
        "role_applied"   : "Backend Python Developer",
        "job_description": (
            "We are looking for a Python backend developer with experience "
            "in REST APIs, databases, and basic DevOps. "
            "The role is remote and project-based."
        ),
    }
    # ─────────────────────────────────────────────────────────────────────────

    print("=" * 60)
    print("  GitHub Crawler Agent — CrewAI")
    print(f"  GitHub Username : {candidate_inputs['github_username']}")
    print(f"  Role            : {candidate_inputs['role_applied']}")
    print("=" * 60 + "\n")

    result = GithubCrawlerCrew().crew().kickoff(inputs=candidate_inputs)

    print("\n" + "=" * 60)
    print("  FINAL SCORECARD")
    print("=" * 60)
    print(result)


if __name__ == "__main__":
    run()