"""GitHub issue tool module."""

from dataclasses import dataclass
from typing import List, Optional

from github.Issue import Issue

from dev_kit_gh_mcp_server.core import GitHubOperation


@dataclass
class CreateIssueOp(GitHubOperation):
    """Operation to create an issue in a GitHub repository."""

    async def __call__(
        self,
        title: str,
        body: Optional[str] = None,
        assignees: Optional[List[str]] = None,
        labels: Optional[List[str]] = None,
    ) -> Issue:
        """Create a new issue in the repository.

        Returns:
            Issue: The created issue object.

        """
        issue = self._gh_repo.create_issue(
            title=title,
            body=body,
            assignees=assignees,
            labels=labels,
        )
        return issue


@dataclass
class ReadIssueCommentsOp(GitHubOperation):
    """Operation to read comments from a GitHub issue."""

    async def __call__(self, issue_number: int) -> list:
        """Read all comments for a given issue number.

        Returns:
            list: A list of issue comments.

        """
        issue = self._gh_repo.get_issue(number=issue_number)
        return list(issue.get_comments())


@dataclass
class WriteIssueCommentOp(GitHubOperation):
    """Operation to write a comment to a GitHub issue."""

    async def __call__(self, issue_number: int, body: str) -> object:
        """Write a comment to the specified issue.

        Returns:
            object: The created comment object.

        """
        issue = self._gh_repo.get_issue(number=issue_number)
        return issue.create_comment(body)
