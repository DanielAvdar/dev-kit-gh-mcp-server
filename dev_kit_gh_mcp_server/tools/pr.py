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
        draft: bool = False,
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
