"""Tests for the GitHub Repository operations using responses for mocking only (no PyGithub object mocking)."""

from datetime import datetime

import pytest

from dev_kit_gh_mcp_server.tools import (
    ListCommitsOp,
)


@pytest.mark.asyncio
# @responses.activate
async def test_list_commits_op_success(commits_response, repo_data, commits_responses):
    """Test listing commits successfully using responses."""
    repo_url, repo_api_url, repo_response = repo_data

    op = ListCommitsOp(root_dir=repo_url, token="fake-token")
    datetime.now()
    result = await op()
    commits = list(result)
    assert len(commits) == 2
    assert commits[0].sha == "abc123"
    assert commits[0].commit.message == "First commit"
    assert commits[1].sha == "def456"
