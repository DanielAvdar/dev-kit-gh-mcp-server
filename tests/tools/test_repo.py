"""Tests for the GitHub Repository operations."""

from datetime import datetime
from typing import Generator
from unittest.mock import MagicMock, patch

import pytest
import responses
from github.GithubException import GithubException
from github.Issue import Issue
from github.PaginatedList import PaginatedList
from github.PullRequest import PullRequest
from github.Tag import Tag

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


@pytest.fixture
def mock_repo() -> MagicMock:
    """Create a mock repository."""
    repo = MagicMock()
    repo.full_name = "test-owner/test-repo"
    return repo


@pytest.mark.asyncio
@responses.activate
async def test_list_issues_op_success(mock_github_operation: MagicMock) -> None:
    """Test listing issues successfully."""
    # Arrange
    op = ListIssuesOp(root_dir="test-owner/test-repo", token="fake-token")
    op._gh_repo = MagicMock()

    # Mock data
    mock_issue1 = MagicMock(spec=Issue)
    mock_issue1.number = 1
    mock_issue1.title = "Test Issue 1"

    mock_issue2 = MagicMock(spec=Issue)
    mock_issue2.number = 2
    mock_issue2.title = "Test Issue 2"

    mock_issues = MagicMock()
    mock_issues.__iter__.return_value = iter([mock_issue1, mock_issue2])
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
    """Test handling GitHub exception when listing issues."""
    # Arrange
    op = ListIssuesOp(root_dir="test-owner/test-repo", token="fake-token")
    op._gh_repo = MagicMock()

    # Create a custom exception with the expected error message
    error_data = {"message": "API rate limit exceeded"}
    GithubException(status=403, data=error_data, headers={})
    # Create a wrapper exception with our specific error message
    wrapper_exception = GithubException(
        status=403, data=f"Failed to list issues: {error_data.get('message', '')}", headers={}
    )
    op._gh_repo.get_issues.side_effect = wrapper_exception

    # Act & Assert
    with pytest.raises(GithubException) as excinfo:
        await op(state="open")

    # Verify exception details
    assert excinfo.value.status == 403
    assert "Failed to list issues: API rate limit exceeded" in str(excinfo.value.data)


@pytest.mark.asyncio
@responses.activate
async def test_list_commits_op_success(mock_github_operation: MagicMock) -> None:
    """Test listing commits successfully."""
    # Arrange
    op = ListCommitsOp(root_dir="test-owner/test-repo", token="fake-token")
    op._gh_repo = MagicMock()
    # Mock data
    mock_commit1 = MagicMock()
    mock_commit1.sha = "abc123"
    mock_commit1.commit.message = "First commit"
    mock_commit1.commit.author.name = "Test Author"

    mock_commit2 = MagicMock()
    mock_commit2.sha = "def456"
    mock_commit2.commit.message = "Second commit"
    mock_commit2.commit.author.name = "Another Author"

    # For PaginatedList, we need to mock both __iter__ and direct returns
    commits_list = [mock_commit1, mock_commit2]
    mock_commits = MagicMock(spec=PaginatedList)
    mock_commits.__iter__.return_value = iter(commits_list)
    # Ensure the direct list conversion works
    op._gh_repo.get_commits.return_value = commits_list

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
    """Test handling GitHub exception when listing commits."""
    # Arrange
    op = ListCommitsOp(root_dir="test-owner/test-repo", token="fake-token")
    op._gh_repo = MagicMock()

    # Create a custom exception with the expected error message
    error_data = {"message": "Repository not found"}
    wrapper_exception = GithubException(
        status=404, data=f"Failed to list commits: {error_data.get('message', '')}", headers={}
    )
    op._gh_repo.get_commits.side_effect = wrapper_exception

    # Act & Assert
    with pytest.raises(GithubException) as excinfo:
        await op()

    # Verify exception details
    assert excinfo.value.status == 404
    assert "Failed to list commits: Repository not found" in str(excinfo.value.data)


@pytest.mark.asyncio
@responses.activate
async def test_list_tags_op_success(mock_github_operation: MagicMock) -> None:
    """Test listing tags successfully."""
    # Arrange
    op = ListTagsOp(root_dir="test-owner/test-repo", token="fake-token")
    op._gh_repo = MagicMock()
    # Mock data
    mock_tag1 = MagicMock(spec=Tag)
    mock_tag1.name = "v1.0.0"
    mock_tag1.commit.sha = "abc123"

    mock_tag2 = MagicMock(spec=Tag)
    mock_tag2.name = "v2.0.0"
    mock_tag2.commit.sha = "def456"

    # For PaginatedList, we need to mock both __iter__ and direct returns
    tags_list = [mock_tag1, mock_tag2]
    mock_tags = MagicMock(spec=PaginatedList)
    mock_tags.__iter__.return_value = iter(tags_list)
    # Ensure the direct list conversion works
    op._gh_repo.get_tags.return_value = tags_list

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
    """Test handling GitHub exception when listing tags."""
    # Arrange
    op = ListTagsOp(root_dir="test-owner/test-repo", token="fake-token")
    op._gh_repo = MagicMock()

    # Create a custom exception with the expected error message
    error_data = {"message": "Internal server error"}
    wrapper_exception = GithubException(
        status=500, data=f"Failed to list tags: {error_data.get('message', '')}", headers={}
    )
    op._gh_repo.get_tags.side_effect = wrapper_exception

    # Act & Assert
    with pytest.raises(GithubException) as excinfo:
        await op()

    # Verify exception details
    assert excinfo.value.status == 500
    assert "Failed to list tags: Internal server error" in str(excinfo.value.data)


@pytest.mark.asyncio
@responses.activate
async def test_list_prs_op_success(mock_github_operation: MagicMock) -> None:
    """Test listing pull requests successfully."""
    # Arrange
    op = ListPRsOp(root_dir="test-owner/test-repo", token="fake-token")
    op._gh_repo = MagicMock()

    # Mock data
    mock_pr1 = MagicMock(spec=PullRequest)
    mock_pr1.number = 1
    mock_pr1.title = "Add new feature"
    mock_pr1.state = "open"

    mock_pr2 = MagicMock(spec=PullRequest)
    mock_pr2.number = 2
    mock_pr2.title = "Fix bug"
    mock_pr2.state = "open"

    mock_prs = MagicMock()
    mock_prs.__iter__.return_value = iter([mock_pr1, mock_pr2])
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
    """Test handling GitHub exception when listing pull requests."""
    # Arrange
    op = ListPRsOp(root_dir="test-owner/test-repo", token="fake-token")
    op._gh_repo = MagicMock()

    # Create a custom exception with the expected error message
    error_data = {"message": "Validation Failed"}
    wrapper_exception = GithubException(
        status=422, data=f"Failed to list pull requests: {error_data.get('message', '')}", headers={}
    )
    op._gh_repo.get_pulls.side_effect = wrapper_exception

    # Act & Assert
    with pytest.raises(GithubException) as excinfo:
        await op(base="non-existing-branch")

    # Verify exception details
    assert excinfo.value.status == 422
    assert "Failed to list pull requests: Validation Failed" in str(excinfo.value.data)
