# live_github_listing.py
import asyncio
import os
from datetime import datetime, timedelta

from dotenv import load_dotenv

from dev_kit_gh_mcp_server.tools import ListCommitsOp, ListIssuesOp, ListPRsOp, ListTagsOp

load_dotenv()  # take environment variables


async def main():
    # Ensure GITHUB_TOKEN is set in environment variables, and GITHUB_REPO for the repository
    # repo_path = 'DanielAvdar/pandas-pyarrow'  # Example repository
    repo_path = os.getenv("GITHUB_REPO")

    # List Issues
    print("🔍 Recent Open Issues:")
    issues_op = ListIssuesOp(root_dir=repo_path)
    issues = await issues_op(state="open", since=datetime.now() - timedelta(days=30))
    for issue in issues[:5]:  # Display first 5 issues
        print(f"- {issue.title} (#{issue.number})")

    # List Commits
    print("\n🚀 Recent Commits:")
    commits_op = ListCommitsOp(root_dir=repo_path)
    commits = await commits_op(since=datetime.now() - timedelta(days=30))
    for commit in commits[:5]:  # Display first 5 commits
        print(f"- {commit.commit.message.split('\n')[0]} by {commit.commit.author.name}")

    # List Tags
    print("\n🏷️ Repository Tags:")
    tags_op = ListTagsOp(root_dir=repo_path)
    tags = await tags_op()
    for tag in tags[:5]:  # Display first 5 tags
        print(f"- {tag.name}")

    # List Pull Requests
    print("\n📦 Open Pull Requests:")
    prs_op = ListPRsOp(root_dir=repo_path)
    prs = await prs_op(state="open")
    for pr in prs[:5]:  # Display first 5 PRs
        print(f"- {pr.title} (#{pr.number})")


if __name__ == "__main__":
    asyncio.run(main())
