"""Tests for the GitHub Repository operations using responses for mocking only (no PyGithub object mocking)."""

from datetime import datetime

import pytest

from dev_kit_gh_mcp_server.tools import (
    ListCommitsOp,
    ListIssuesOp,
    ListPRsOp,
    ListTagsOp,
)


@pytest.mark.asyncio
async def test_list_prs_op_success(repo_data, prs_responses):
    """Test listing pull requests successfully using responses."""
    repo_url, repo_api_url, repo_response = repo_data
    op = ListPRsOp(root_dir=repo_url, token="fake-token")
    result = await op()
    prs = list(result)
    assert len(prs) == 2
    assert prs[0].title == "Add new feature"
    assert prs[1].title == "Fix bug"


@pytest.fixture
def commits_responses(commits_response, repo_data, repo_responses):
    repo_url, repo_api_url, repo_response = repo_data

    repo_responses.add(
        repo_responses.GET,
        f"https://api.github.com:443/repos/{repo_url}/commits",
        json=commits_response,
        status=200,
    )
    return repo_responses


@pytest.fixture
def issues_response():
    return [
        {
            "id": 1,
            "number": 1,
            "title": "Issue 1",
            "state": "open",
            "user": {"login": "octocat"},
            "body": "First issue",
        },
        {
            "id": 2,
            "number": 2,
            "title": "Issue 2",
            "state": "open",
            "user": {"login": "octocat"},
            "body": "Second issue",
        },
    ]


@pytest.fixture
def issues_responses(issues_response, repo_data, repo_responses):
    repo_url, repo_api_url, repo_response = repo_data
    repo_responses.add(
        repo_responses.GET,
        f"https://api.github.com:443/repos/{repo_url}/issues",
        json=issues_response,
        status=200,
    )
    return repo_responses


@pytest.fixture
def tags_responses(tags_response, repo_data, repo_responses):
    repo_url, repo_api_url, repo_response = repo_data
    repo_responses.add(
        repo_responses.GET,
        f"https://api.github.com:443/repos/{repo_url}/tags",
        json=tags_response,
        status=200,
    )
    return repo_responses


@pytest.mark.asyncio
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


@pytest.mark.asyncio
async def test_list_issues_op_success(repo_data, issues_responses):
    """Test listing issues successfully using responses."""
    repo_url, repo_api_url, repo_response = repo_data
    op = ListIssuesOp(root_dir=repo_url, token="fake-token")
    result = await op()
    issues = list(result)
    assert len(issues) == 2
    assert issues[0].title == "Issue 1"
    assert issues[1].title == "Issue 2"


@pytest.fixture
def prs_responses(prs_response, repo_data, repo_responses):
    repo_url, repo_api_url, repo_response = repo_data
    repo_responses.add(
        repo_responses.GET,
        f"https://api.github.com:443/repos/{repo_url}/pulls",
        json=prs_response,
        status=200,
    )
    return repo_responses


@pytest.mark.asyncio
async def test_list_tags_op_success(repo_data, tags_responses):
    """Test listing tags successfully using responses."""
    repo_url, repo_api_url, repo_response = repo_data
    op = ListTagsOp(root_dir=repo_url, token="fake-token")
    result = await op()
    tags = list(result)
    assert len(tags) == 2
    assert tags[0].name == "v1.0.0"
    assert tags[1].name == "v2.0.0"
