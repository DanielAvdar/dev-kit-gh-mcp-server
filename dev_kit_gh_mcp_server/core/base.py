"""Base class for GitHub operations."""

import os
from dataclasses import dataclass, field
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
        """Post-initialization method to set up the GitHub repository."""
        # Initialize the GitHub repository
        token = self.token or os.getenv("GITHUB_TOKEN")
        if isinstance(token, str):
            raise ValueError("GitHub token is required. Set it as an environment variable or pass it as an argument.")
        gh = Github(login_or_token=self.token or os.getenv("GITHUB_TOKEN"))
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
