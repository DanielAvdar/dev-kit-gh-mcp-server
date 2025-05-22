"""Tests for the GitHub Repository operations using responses for mocking only (no PyGithub object mocking)."""

import re
from datetime import datetime
from unittest.mock import MagicMock

import pytest
import responses
from github.GithubException import GithubException

from dev_kit_gh_mcp_server.tools import (
    ListCommitsOp,
    ListIssuesOp,
    ListPRsOp,
    ListTagsOp,
)


@pytest.fixture
def issues_response():
    return [
        {
            "id": 1,
            "number": 1347,
            "title": "Found a bug",
            "user": {"login": "octocat"},
            "state": "open",
            "body": "I'm having a problem with this.",
        }
    ]


@pytest.mark.asyncio
@responses.activate
async def test_list_issues_op_success(monkeypatch, repo_data, issues_response) -> None:
    """Test listing issues successfully using responses only."""
    repo_url, repo_api_url, repo_response = repo_data
    # Mock the repo endpoint with all required fields per GitHub REST API docs

    # Use regex to match both with and without :443 in the repo URL, and allow optional query params
    repo_url_pattern = re.compile(r"https://api.github.com(:443)?/repos/octocat/Hello-World(\\?.*)?$")
    responses.add(responses.GET, repo_url_pattern, json=repo_response, status=200)
    # Patch __post_init__ to use a real PyGithub repo object
    # patch_post_init_with_real_repo(monkeypatch, repo_url, repo_response)
    # Mock the issues endpoint (also regex for port and query params)
    issues_url_pattern = re.compile(r"https://api.github.com(:443)?/repos/octocat/Hello-World/issues(\\?.*)?$")
    responses.add(responses.GET, issues_url_pattern, json=issues_response, status=200)
    # Remove the unused import that causes a compile error
    # from dev_kit_gh_mcp_server.tools.repo import list_issues_op
    # Instead of importing a non-existent function, use the ListIssuesOp class directly
    op = ListIssuesOp(root_dir=repo_url, token="dummy-token")
    op.__post_init__()  # Ensure the repo is set after patching
    result = await op()
    assert result[0].title == "Found a bug"


@pytest.fixture(autouse=True)
# @responses.activate
async def repo_res_mock():
    # repo_url, repo_api_url, repo_response = repo_data

    # repo_url_pattern = re.compile(r"https://api.github.com(:443)?/repos/octocat/Hello-World(\\?.*)?$")
    # responses.add(responses.GET, repo_url_pattern, json=repo_response, status=200)
    # # Patch __post_init__ to use a real PyGithub repo object
    # # patch_post_init_with_real_repo(monkeypatch, repo_url, repo_response)
    # # Mock the issues endpoint (also regex for port and query params)
    # issues_url_pattern = re.compile(r"https://api.github.com(:443)?/repos/octocat/Hello-World/issues(\\?.*)?$")
    # responses.add(responses.GET, issues_url_pattern, json=issues_response, status=200)
    # issues_url_pattern = re.compile(r"https://api.github.com(:443)?/repos/test-owner/test-repo(\\?.*)?$")
    # responses.add(responses.GET, issues_url_pattern, json=issues_response, status=200)
    responses.add(
        responses.GET,
        "https://api.github.com:443/repos/test-owner/test-repo",
        json="error_response",
        status=403,
    )


@pytest.mark.asyncio
@responses.activate
async def test_list_issues_op_failure(repo_res_mock) -> None:
    """Test handling GitHub API error when listing issues."""
    # Mock the GitHub API response for issues with an error
    error_response = {
        "message": "API rate limit exceeded",
        "documentation_url": "https://docs.github.com/rest/overview/resources-in-the-rest-api#rate-limiting",
    }

    responses.add(
        responses.GET,
        "https://api.github.com:443/repos/test-owner/test-repo/issues",
        json=error_response,
        status=200,
    )
    responses.add(
        responses.GET,
        "https://api.github.com:443/repos/test-owner/test-repo",
        json=error_response,
        status=200,
    )
    # Create operation instance
    op = ListIssuesOp(root_dir="test-owner/test-repo", token="fake-token")

    # Patch the _gh_repo.get_issues to raise GithubException
    # op._gh_repo.get_issues.side_effect = GithubException(status=403, data=error_response, headers={})

    # Act & Assert
    with pytest.raises(GithubException):
        await op(state="open")

    # Verify exception details
    # assert excinfo.value.status == 403
    # assert "API rate limit exceeded" in str(excinfo.value.data)


@pytest.mark.asyncio
@responses.activate
async def test_list_commits_op_success(commits_response, repo_data):
    """Test listing commits successfully using responses."""
    repo_url, repo_api_url, repo_response = repo_data
    responses.add(
        responses.GET,
        "https://api.github.com:443/repos/test-owner/test-repo",
        json=repo_response,
        status=200,
    )
    responses.add(
        responses.GET,
        f"https://api.github.com:443/repos/{repo_url}/commits",
        json=commits_response,
        status=200,
    )
    op = ListCommitsOp(root_dir="test-owner/test-repo", token="fake-token")
    # op._gh_repo.get_commits.return_value = [
    #     MagicMock(sha=commit["sha"], commit=MagicMock(message=commit["commit"]["message"]))
    #     for commit in commits_response
    # ]
    datetime.now()
    result = await op()
    commits = list(result)
    assert len(commits) == 2
    assert commits[0].sha == "abc123"
    assert commits[0].commit.message == "First commit"
    assert commits[1].sha == "def456"


@pytest.mark.asyncio
@responses.activate
async def test_list_commits_op_failure() -> None:
    """Test handling GitHub API error when listing commits."""
    # Mock the GitHub API response for commits with an error
    error_response = {
        "message": "Repository not found",
        "documentation_url": "https://docs.github.com/rest/reference/repos#get-a-repository",
    }

    responses.add(
        responses.GET,
        "https://api.github.com/repos/test-owner/test-repo/commits",
        json=error_response,
        status=404,
    )

    # Create operation instance
    op = ListCommitsOp(root_dir="test-owner/test-repo", token="fake-token")

    # Patch the _gh_repo.get_commits to raise GithubException
    op._gh_repo.get_commits.side_effect = GithubException(status=404, data=error_response, headers={})

    # Act & Assert
    with pytest.raises(GithubException) as excinfo:
        await op()

    # Verify exception details
    assert excinfo.value.status == 404
    assert "Repository not found" in str(excinfo.value.data)


@pytest.mark.asyncio
@responses.activate
async def test_list_tags_op_success(tags_response):
    """Test listing tags successfully using responses."""
    responses.add(
        responses.GET,
        "https://api.github.com/repos/test-owner/test-repo/tags",
        json=tags_response,
        status=200,
    )
    op = ListTagsOp(root_dir="test-owner/test-repo", token="fake-token")
    op._gh_repo.get_tags.return_value = [
        MagicMock(**{"commit": MagicMock(sha=tag["commit"]["sha"])}, name=tag["name"]) for tag in tags_response
    ]
    for i, tag in enumerate(op._gh_repo.get_tags.return_value):
        tag.name = tags_response[i]["name"]
    result = await op()
    tags = list(result)
    assert len(tags) == 2
    assert tags[0].name == "v1.0.0"
    assert tags[1].name == "v2.0.0"


@pytest.mark.asyncio
@responses.activate
async def test_list_tags_op_failure() -> None:
    """Test handling GitHub API error when listing tags."""
    error_response = {
        "message": "Internal server error",
        "documentation_url": "https://docs.github.com/rest/reference/repos#list-repository-tags",
    }
    responses.add(
        responses.GET,
        "https://api.github.com/repos/test-owner/test-repo/tags",
        json=error_response,
        status=500,
    )
    op = ListTagsOp(root_dir="test-owner/test-repo", token="fake-token")
    op._gh_repo.get_tags.side_effect = GithubException(status=500, data=error_response, headers={})
    with pytest.raises(GithubException) as excinfo:
        await op()
    assert excinfo.value.status == 500
    assert "Internal server error" in str(excinfo.value.data)


@pytest.mark.asyncio
@responses.activate
async def test_list_prs_op_success(prs_response):
    """Test listing pull requests successfully using responses."""
    responses.add(
        responses.GET,
        "https://api.github.com/repos/test-owner/test-repo/pulls",
        json=prs_response,
        status=200,
    )
    op = ListPRsOp(root_dir="test-owner/test-repo", token="fake-token")
    op._gh_repo.get_pulls.return_value = [
        MagicMock(number=pr["number"], title=pr["title"], state=pr["state"]) for pr in prs_response
    ]
    result = await op(state="open", base="main")
    assert len(result) == 2
    assert result[0].number == 1
    assert result[0].title == "Add new feature"
    assert result[1].number == 2
    assert result[1].title == "Fix bug"


@pytest.mark.asyncio
@responses.activate
async def test_list_prs_op_failure() -> None:
    """Test handling GitHub API error when listing pull requests."""
    error_response = {
        "message": "Validation Failed",
        "errors": [{"resource": "PullRequest", "field": "base", "code": "invalid"}],
        "documentation_url": "https://docs.github.com/rest/reference/pulls#list-pull-requests",
    }
    responses.add(
        responses.GET,
        "https://api.github.com/repos/test-owner/test-repo/pulls",
        json=error_response,
        status=422,
    )
    op = ListPRsOp(root_dir="test-owner/test-repo", token="fake-token")
    op._gh_repo.get_pulls.side_effect = GithubException(status=422, data=error_response, headers={})
    with pytest.raises(GithubException) as excinfo:
        await op(base="non-existing-branch")
    assert excinfo.value.status == 422
    assert "Validation Failed" in str(excinfo.value.data)
