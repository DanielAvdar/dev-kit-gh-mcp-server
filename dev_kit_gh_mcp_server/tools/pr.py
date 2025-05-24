"""GitHub PR tool module."""

from dataclasses import dataclass
from typing import Optional

from dev_kit_gh_mcp_server.core import GitHubOperation


@dataclass
class CreatePROp(GitHubOperation):
    """Operation to create a pull request in a GitHub repository."""

    async def __call__(
        self,
        title: str,
        body: Optional[str] = None,
        head: str = None,
        base: str = None,
        draft: bool = True,
    ) -> object:
        """Create a new pull request in the repository.

        Returns:
            The created pull request object.

        """
        pr = self._gh_repo.create_pull(
            title=title,
            body=body,
            head=head,
            base=base,
            draft=draft,
        )
        return pr


@dataclass
class ReadPRCommentsOp(GitHubOperation):
    """Operation to read comments from a GitHub pull request."""

    async def __call__(self, pr_number: int) -> list:
        """Read all comments for a given pull request number."""
        pr = self._gh_repo.get_pull(number=pr_number)
        return list(pr.get_comments())


@dataclass
class WritePRCommentOp(GitHubOperation):
    """Operation to write a comment to a GitHub pull request."""

    async def __call__(self, pr_number: int, body: str) -> object:
        """Write a comment to the specified pull request."""
        pr = self._gh_repo.get_pull(number=pr_number)
        return pr.create_issue_comment(body)


@dataclass
class ListPRReviewsOp(GitHubOperation):
    """Operation to list all reviews for a GitHub pull request."""

    async def __call__(self, pr_number: int) -> list:
        """Return all reviews for the specified pull request."""
        pr = self._gh_repo.get_pull(number=pr_number)
        return list(pr.get_reviews())
