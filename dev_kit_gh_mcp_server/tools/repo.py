"""GitHub repo tool module."""

from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

from github.Issue import Issue
from github.PaginatedList import PaginatedList
from github.PullRequest import PullRequest

from dev_kit_gh_mcp_server.core import GitHubOperation


@dataclass
class ListIssuesOp(GitHubOperation):
    """Operation to list issues in a GitHub repository."""

    async def __call__(
        self,
        max_results: int = 10,
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
        """List issues in a GitHub repository with filtering options.

        Returns:
            List[Issue]: List of issues matching the filter options.

        """
        issues = self._gh_repo.get_issues(
            **self.uncrooked_params(
                state=state,
                labels=labels,
                sort=sort,
                direction=direction,
                since=since,
                assignee=assignee,
                creator=creator,
                mentioned=mentioned,
                milestone=milestone,
            ),
        )
        return list(issues)[:max_results]


@dataclass
class ListCommitsOp(GitHubOperation):
    """Operation to list commits in a GitHub repository."""

    async def __call__(
        self,
        max_results: int = 10,
        sha: Optional[str] = None,
        path: Optional[str] = None,
        author: Optional[str] = None,
        since: Optional[datetime] = None,
        until: Optional[datetime] = None,
    ) -> PaginatedList:
        """List commits in a GitHub repository with filtering options.

        Returns:
            PaginatedList: List of commits matching the filter options.

        """
        commits = self._gh_repo.get_commits(
            **self.uncrooked_params(
                sha=sha,
                path=path,
                author=author,
                since=since,
                until=until,
            ),
        )
        return commits[:max_results]


@dataclass
class ListTagsOp(GitHubOperation):
    """Operation to list tags in a GitHub repository."""

    async def __call__(
        self,
        max_results: int = 10,
    ) -> PaginatedList:
        """List all tags in a GitHub repository.

        Returns:
            PaginatedList: List of tags in the repository.

        """
        tags = self._gh_repo.get_tags()
        return tags[:max_results]


@dataclass
class ListPRsOp(GitHubOperation):
    """Operation to list Pull Requests in a GitHub repository."""

    async def __call__(
        self,
        max_results: int = 10,
        state: str = "open",
        sort: str = "created",
        direction: str = "desc",
        base: Optional[str] = None,
        head: Optional[str] = None,
    ) -> List[PullRequest]:
        """List pull requests in a GitHub repository with filtering options.

        Returns:
            List[PullRequest]: List of pull requests matching the filter options.

        """
        pulls = self._gh_repo.get_pulls(
            **self.uncrooked_params(
                state=state,
                sort=sort,
                direction=direction,
                base=base,
                head=head,
            ),
        )
        return list(pulls)[:max_results]
