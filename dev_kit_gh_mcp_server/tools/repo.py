"""Repository operations for GitHub."""

from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

from github.GithubException import GithubException
from github.Issue import Issue
from github.PaginatedList import PaginatedList
from github.PullRequest import PullRequest

from dev_kit_gh_mcp_server.core import GitHubOperation


@dataclass
class ListIssuesOp(GitHubOperation):
    """Operation to list issues in a GitHub repository."""

    async def __call__(
        self,
        state: str = "open",
        sort: str = "created",
        direction: str = "desc",
        labels: Optional[List[str]] = None,
        since: Optional[datetime] = None,
        assignee: Optional[str] = None,
        creator: Optional[str] = None,
        mentioned: Optional[str] = None,
        milestone: Optional[str] = None,
    ) -> List[Issue]:
        """List issues in a GitHub repository with filtering options."""
        try:
            issues = self._gh_repo.get_issues(
                state=state,
                labels=labels,
                sort=sort,
                direction=direction,
                since=since,
                assignee=assignee,
                creator=creator,
                mentioned=mentioned,
                milestone=milestone,
            )
            return list(issues)
        except GithubException as e:
            raise GithubException(e.status, f"Failed to list issues: {e.data.get('message', '')}", e.headers) from e


@dataclass
class ListCommitsOp(GitHubOperation):
    """Operation to list commits in a GitHub repository."""

    async def __call__(
        self,
        sha: Optional[str] = None,
        path: Optional[str] = None,
        author: Optional[str] = None,
        since: Optional[datetime] = None,
        until: Optional[datetime] = None,
    ) -> PaginatedList:
        """List commits in a GitHub repository with filtering options."""
        try:
            commits = self._gh_repo.get_commits(
                sha=sha,
                path=path,
                author=author,
                since=since,
                until=until,
            )
            return commits
        except GithubException as e:
            raise GithubException(e.status, f"Failed to list commits: {e.data.get('message', '')}", e.headers) from e


@dataclass
class ListTagsOp(GitHubOperation):
    """Operation to list tags in a GitHub repository."""

    async def __call__(self) -> PaginatedList:
        """List all tags in a GitHub repository."""
        try:
            tags = self._gh_repo.get_tags()
            return tags
        except GithubException as e:
            raise GithubException(e.status, f"Failed to list tags: {e.data.get('message', '')}", e.headers) from e


@dataclass
class ListPRsOp(GitHubOperation):
    """Operation to list Pull Requests in a GitHub repository."""

    async def __call__(
        self,
        state: str = "open",
        sort: str = "created",
        direction: str = "desc",
        base: Optional[str] = None,
        head: Optional[str] = None,
    ) -> List[PullRequest]:
        """List pull requests in a GitHub repository with filtering options."""
        try:
            pulls = self._gh_repo.get_pulls(
                state=state,
                sort=sort,
                direction=direction,
                base=base,
                head=head,
            )
            return list(pulls)
        except GithubException as e:
            raise GithubException(
                e.status, f"Failed to list pull requests: {e.data.get('message', '')}", e.headers
            ) from e
