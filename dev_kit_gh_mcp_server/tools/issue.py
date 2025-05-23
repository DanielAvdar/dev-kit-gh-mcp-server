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
