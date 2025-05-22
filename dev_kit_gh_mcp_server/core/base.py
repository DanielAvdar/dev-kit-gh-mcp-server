"""Base class for GitHub operations."""

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from dev_kit_mcp_server.core import AsyncOperation
from github import Github
from github.Repository import Repository


@dataclass
class GitHubOperation(AsyncOperation):
    """Base class for GitHub repository operations."""

    _gh_repo: Repository = field(init=False, default=None)
    token: Optional[str] = field(
        default=None,
        metadata={
            "description": "GitHub token for authentication. "
            "If not provided, it will be fetched from the environment variable GITHUB_TOKEN."
        },
    )

    def __post_init__(self):
        """Post-initialization method to set up the GitHub repository.

        Raises:
            ValueError: If GitHub token is not provided or if repository has no remote URL or multiple remote URLs.

        """
        # Initialize the GitHub repository
        token = self.token or os.getenv("GITHUB_TOKEN")
        if not isinstance(token, str):
            raise ValueError("GitHub token is required. Set it as an environment variable or pass it as an argument.")
        gh = Github(login_or_token=token)
        if self.root_dir_is_a_url():
            self._gh_repo = gh.get_repo(self.root_dir)
            return
        super().__post_init__()

        remote_url = self._repo.remotes
        if len(remote_url) == 0:
            raise ValueError("No remote URL found for the repository. Use GH repo URL instead.")
        if len(remote_url) > 1:
            raise ValueError("Multiple remote URLs found. Use GH repo URL instead.")
        self._gh_repo = gh.get_repo(remote_url[0].url.split(":")[-1])

    def root_dir_is_a_url(self) -> bool:
        """Return True if root_dir is a URL, False if it is a local path.

        Returns:
            bool: True if root_dir is a URL, False if it is a local path.

        """
        return not Path(self.root_dir).exists()

    def uncrooked_params(self, **kwargs):
        """Uncrooked parameters for GitHub operations.

        Args:
            kwargs: Additional keyword arguments to pass to the operation.

        Returns:
            A dictionary of uncrooked parameters.

        """
        return {k: v for k, v in kwargs.items() if v is not None}
