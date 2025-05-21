"""Tests for the GitHub Repository operations using responses for mocking."""

from datetime import datetime
from typing import Generator
from unittest.mock import MagicMock, patch

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
def mock_github_operation() -> Generator[MagicMock, None, None]:
    """Mock the GitHubOperation base class."""
    with patch("dev_kit_gh_mcp_server.core.base.GitHubOperation.__post_init__") as mock:
        yield mock


@pytest.mark.asyncio
@responses.activate
async def test_list_issues_op_success(mock_github_operation: MagicMock) -> None:
    """Test listing issues successfully using responses."""
    # Mock the GitHub API response for issues
    issues_response = [
        {
            "number": 1,
            "title": "Test Issue 1",
            "state": "open",
            "body": "This is a test issue",
            "user": {"login": "testuser"},
            "created_at": "2025-05-01T00:00:00Z",
            "updated_at": "2025-05-02T00:00:00Z",
        },
        {
            "number": 2,
            "title": "Test Issue 2",
            "state": "open",
            "body": "This is another test issue",
            "user": {"login": "anotheruser"},
            "created_at": "2025-05-03T00:00:00Z",
            "updated_at": "2025-05-04T00:00:00Z",
        },
    ]

    # Add response mock for GitHub API
    responses.add(
        responses.GET,
        "https://api.github.com/repos/test-owner/test-repo/issues",
        json=issues_response,
        status=200,
    )

    # Create operation instance and mock repo
    op = ListIssuesOp(root_dir="test-owner/test-repo", token="fake-token")
    op._gh_repo = MagicMock()

    # Mock issues
    mock_issues = []
    for issue_data in issues_response:
        mock_issue = MagicMock()
        mock_issue.number = issue_data["number"]
        mock_issue.title = issue_data["title"]
        mock_issue.state = issue_data["state"]
        mock_issues.append(mock_issue)

    op._gh_repo.get_issues.return_value = mock_issues

    # Act
    result = await op(state="open")

    # Assert
    assert len(result) == 2
    assert result[0].number == 1
    assert result[0].title == "Test Issue 1"
    assert result[1].number == 2
    assert result[1].title == "Test Issue 2"

    # Verify correct parameters were passed
    op._gh_repo.get_issues.assert_called_once_with(state="open", sort="created", direction="desc")


@pytest.mark.asyncio
@responses.activate
async def test_list_issues_op_failure(mock_github_operation: MagicMock) -> None:
    """Test handling GitHub API error when listing issues."""
    # Mock the GitHub API response for issues with an error
    error_response = {
        "message": "API rate limit exceeded",
        "documentation_url": "https://docs.github.com/rest/overview/resources-in-the-rest-api#rate-limiting",
    }

    responses.add(
        responses.GET,
        "https://api.github.com/repos/test-owner/test-repo/issues",
        json=error_response,
        status=403,
    )

    # Create operation instance
    op = ListIssuesOp(root_dir="test-owner/test-repo", token="fake-token")
    op._gh_repo = MagicMock()

    # Mock exception
    exception = GithubException(status=403, data=f"Failed to list issues: {error_response['message']}", headers={})
    op._gh_repo.get_issues.side_effect = exception

    # Act & Assert
    with pytest.raises(GithubException) as excinfo:
        await op(state="open")

    # Verify exception details
    assert excinfo.value.status == 403
    assert "Failed to list issues: API rate limit exceeded" in str(excinfo.value.data)


@pytest.mark.asyncio
@responses.activate
async def test_list_commits_op_success(mock_github_operation: MagicMock) -> None:
    """Test listing commits successfully using responses."""
    # Mock the GitHub API response for commits
    commits_response = [
        {
            "sha": "abc123",
            "commit": {
                "message": "First commit",
                "author": {"name": "Test Author", "email": "test@example.com", "date": "2025-05-01T00:00:00Z"},
            },
        },
        {
            "sha": "def456",
            "commit": {
                "message": "Second commit",
                "author": {"name": "Another Author", "email": "another@example.com", "date": "2025-05-02T00:00:00Z"},
            },
        },
    ]

    # Add response mock for GitHub API
    responses.add(
        responses.GET,
        "https://api.github.com/repos/test-owner/test-repo/commits",
        json=commits_response,
        status=200,
    )

    # Create operation instance
    op = ListCommitsOp(root_dir="test-owner/test-repo", token="fake-token")
    op._gh_repo = MagicMock()

    # Mock commits
    mock_commits = []
    for commit_data in commits_response:
        mock_commit = MagicMock()
        mock_commit.sha = commit_data["sha"]
        mock_commit.commit.message = commit_data["commit"]["message"]
        mock_commit.commit.author.name = commit_data["commit"]["author"]["name"]
        mock_commits.append(mock_commit)

    op._gh_repo.get_commits.return_value = mock_commits

    # Act
    since_date = datetime.now()
    result = await op(since=since_date)

    # Assert
    commits = list(result)
    assert len(commits) == 2
    assert commits[0].sha == "abc123"
    assert commits[0].commit.message == "First commit"
    assert commits[1].sha == "def456"

    # Verify correct parameters were passed
    op._gh_repo.get_commits.assert_called_once_with(since=since_date)


@pytest.mark.asyncio
@responses.activate
async def test_list_commits_op_failure(mock_github_operation: MagicMock) -> None:
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
    op._gh_repo = MagicMock()

    # Mock exception
    exception = GithubException(status=404, data=f"Failed to list commits: {error_response['message']}", headers={})
    op._gh_repo.get_commits.side_effect = exception

    # Act & Assert
    with pytest.raises(GithubException) as excinfo:
        await op()

    # Verify exception details
    assert excinfo.value.status == 404
    assert "Failed to list commits: Repository not found" in str(excinfo.value.data)


@pytest.mark.asyncio
@responses.activate
async def test_list_tags_op_success(mock_github_operation: MagicMock) -> None:
    """Test listing tags successfully using responses."""
    # Mock the GitHub API response for tags
    tags_response = [
        {
            "name": "v1.0.0",
            "commit": {"sha": "abc123", "url": "https://api.github.com/repos/test-owner/test-repo/commits/abc123"},
        },
        {
            "name": "v2.0.0",
            "commit": {"sha": "def456", "url": "https://api.github.com/repos/test-owner/test-repo/commits/def456"},
        },
    ]

    # Add response mock for GitHub API
    responses.add(
        responses.GET,
        "https://api.github.com/repos/test-owner/test-repo/tags",
        json=tags_response,
        status=200,
    )

    # Create operation instance
    op = ListTagsOp(root_dir="test-owner/test-repo", token="fake-token")
    op._gh_repo = MagicMock()

    # Mock tags
    mock_tags = []
    for tag_data in tags_response:
        mock_tag = MagicMock()
        mock_tag.name = tag_data["name"]
        mock_tag_commit = MagicMock()
        mock_tag_commit.sha = tag_data["commit"]["sha"]
        mock_tag.commit = mock_tag_commit
        mock_tags.append(mock_tag)

    op._gh_repo.get_tags.return_value = mock_tags

    # Act
    result = await op()

    # Assert
    tags = list(result)
    assert len(tags) == 2
    assert tags[0].name == "v1.0.0"
    assert tags[1].name == "v2.0.0"

    # Verify method was called
    op._gh_repo.get_tags.assert_called_once()


@pytest.mark.asyncio
@responses.activate
async def test_list_tags_op_failure(mock_github_operation: MagicMock) -> None:
    """Test handling GitHub API error when listing tags."""
    # Mock the GitHub API response for tags with an error
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

    # Create operation instance
    op = ListTagsOp(root_dir="test-owner/test-repo", token="fake-token")
    op._gh_repo = MagicMock()

    # Mock exception
    exception = GithubException(status=500, data=f"Failed to list tags: {error_response['message']}", headers={})
    op._gh_repo.get_tags.side_effect = exception

    # Act & Assert
    with pytest.raises(GithubException) as excinfo:
        await op()

    # Verify exception details
    assert excinfo.value.status == 500
    assert "Failed to list tags: Internal server error" in str(excinfo.value.data)


@pytest.mark.asyncio
@responses.activate
async def test_list_prs_op_success(mock_github_operation: MagicMock) -> None:
    """Test listing pull requests successfully using responses."""
    # Mock the GitHub API response for PRs
    prs_response = [
        {
            "number": 1,
            "title": "Add new feature",
            "state": "open",
            "body": "This is a new feature",
            "user": {"login": "testuser"},
            "created_at": "2025-05-01T00:00:00Z",
            "updated_at": "2025-05-02T00:00:00Z",
            "head": {"ref": "feature-branch"},
            "base": {"ref": "main"},
        },
        {
            "number": 2,
            "title": "Fix bug",
            "state": "open",
            "body": "This fixes a bug",
            "user": {"login": "anotheruser"},
            "created_at": "2025-05-03T00:00:00Z",
            "updated_at": "2025-05-04T00:00:00Z",
            "head": {"ref": "bugfix-branch"},
            "base": {"ref": "main"},
        },
    ]

    # Add response mock for GitHub API
    responses.add(
        responses.GET,
        "https://api.github.com/repos/test-owner/test-repo/pulls",
        json=prs_response,
        status=200,
    )

    # Create operation instance
    op = ListPRsOp(root_dir="test-owner/test-repo", token="fake-token")
    op._gh_repo = MagicMock()

    # Mock PRs
    mock_prs = []
    for pr_data in prs_response:
        mock_pr = MagicMock()
        mock_pr.number = pr_data["number"]
        mock_pr.title = pr_data["title"]
        mock_pr.state = pr_data["state"]
        mock_prs.append(mock_pr)

    op._gh_repo.get_pulls.return_value = mock_prs

    # Act
    result = await op(state="open", base="main")

    # Assert
    assert len(result) == 2
    assert result[0].number == 1
    assert result[0].title == "Add new feature"
    assert result[1].number == 2
    assert result[1].title == "Fix bug"

    # Verify correct parameters were passed
    op._gh_repo.get_pulls.assert_called_once_with(state="open", sort="created", direction="desc", base="main")


@pytest.mark.asyncio
@responses.activate
async def test_list_prs_op_failure(mock_github_operation: MagicMock) -> None:
    """Test handling GitHub API error when listing pull requests."""
    # Mock the GitHub API response for PRs with an error
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

    # Create operation instance
    op = ListPRsOp(root_dir="test-owner/test-repo", token="fake-token")
    op._gh_repo = MagicMock()

    # Mock exception
    exception = GithubException(
        status=422, data=f"Failed to list pull requests: {error_response['message']}", headers={}
    )
    op._gh_repo.get_pulls.side_effect = exception

    # Act & Assert
    with pytest.raises(GithubException) as excinfo:
        await op(base="non-existing-branch")

    # Verify exception details
    assert excinfo.value.status == 422
    assert "Failed to list pull requests: Validation Failed" in str(excinfo.value.data)
