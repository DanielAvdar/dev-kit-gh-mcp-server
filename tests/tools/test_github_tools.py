"""Tests for GitHub repository operations."""

import json
import os
from unittest.mock import patch

import pytest
from mocket import mocketize
from mocket.mockhttp import Entry

from dev_kit_gh_mcp_server.tools import ListCommitsOp, ListIssuesOp, ListPRsOp, ListTagsOp


@pytest.fixture
def mock_github_token():
    """Mock GitHub token for testing."""
    with patch.dict(os.environ, {"GITHUB_TOKEN": "fake-token"}):
        yield


@mocketize
def test_list_issues_op(mock_github_token):
    """Test listing issues from a GitHub repository."""
    # Mock GitHub API response for issues
    issues_response = [
        {
            "id": 1,
            "number": 101,
            "title": "Test Issue",
            "state": "open",
            "body": "This is a test issue",
            "user": {"login": "testuser"},
            "labels": [{"name": "bug"}],
            "created_at": "2025-05-20T00:00:00Z",
        }
    ]

    # Mock the GitHub API request for issues
    Entry.single_register(
        Entry.GET,
        "https://api.github.com/repos/owner/repo/issues",
        body=json.dumps(issues_response),
        headers={"Content-Type": "application/json"},
        status=200,
    )

    # Test the ListIssuesOp
    with patch("github.Github") as mock_github:
        mock_repo = mock_github.return_value.get_repo.return_value
        mock_issues = mock_repo.get_issues.return_value
        mock_issues.__iter__.return_value = issues_response

        op = ListIssuesOp(root_dir="owner/repo")
        result = pytest.mark.asyncio(op.__call__())

        assert len(result) == 1
        assert result[0]["number"] == 101
        assert result[0]["title"] == "Test Issue"
        assert result[0]["state"] == "open"


@mocketize
def test_list_commits_op(mock_github_token):
    """Test listing commits from a GitHub repository."""
    # Mock GitHub API response for commits
    commits_response = [
        {
            "sha": "abc123",
            "commit": {
                "message": "Test commit",
                "author": {"name": "Test Author", "email": "test@example.com", "date": "2025-05-20T00:00:00Z"},
            },
        }
    ]

    # Mock the GitHub API request for commits
    Entry.single_register(
        Entry.GET,
        "https://api.github.com/repos/owner/repo/commits",
        body=json.dumps(commits_response),
        headers={"Content-Type": "application/json"},
        status=200,
    )

    # Test the ListCommitsOp
    with patch("github.Github") as mock_github:
        mock_repo = mock_github.return_value.get_repo.return_value
        mock_commits = mock_repo.get_commits.return_value
        mock_commits.__iter__.return_value = commits_response

        op = ListCommitsOp(root_dir="owner/repo")
        result = pytest.mark.asyncio(op.__call__())

        commits_list = list(result)
        assert len(commits_list) == 1
        assert commits_list[0]["sha"] == "abc123"
        assert commits_list[0]["commit"]["message"] == "Test commit"


@mocketize
def test_list_tags_op(mock_github_token):
    """Test listing tags from a GitHub repository."""
    # Mock GitHub API response for tags
    tags_response = [
        {
            "name": "v1.0.0",
            "commit": {"sha": "def456", "url": "https://api.github.com/repos/owner/repo/commits/def456"},
        }
    ]

    # Mock the GitHub API request for tags
    Entry.single_register(
        Entry.GET,
        "https://api.github.com/repos/owner/repo/tags",
        body=json.dumps(tags_response),
        headers={"Content-Type": "application/json"},
        status=200,
    )

    # Test the ListTagsOp
    with patch("github.Github") as mock_github:
        mock_repo = mock_github.return_value.get_repo.return_value
        mock_tags = mock_repo.get_tags.return_value
        mock_tags.__iter__.return_value = tags_response

        op = ListTagsOp(root_dir="owner/repo")
        result = pytest.mark.asyncio(op.__call__())

        tags_list = list(result)
        assert len(tags_list) == 1
        assert tags_list[0]["name"] == "v1.0.0"
        assert tags_list[0]["commit"]["sha"] == "def456"


@mocketize
def test_list_prs_op(mock_github_token):
    """Test listing pull requests from a GitHub repository."""
    # Mock GitHub API response for PRs
    prs_response = [
        {
            "id": 1,
            "number": 201,
            "title": "Test PR",
            "state": "open",
            "body": "This is a test PR",
            "user": {"login": "testuser"},
            "base": {"ref": "main"},
            "head": {"ref": "feature-branch"},
        }
    ]

    # Mock the GitHub API request for PRs
    Entry.single_register(
        Entry.GET,
        "https://api.github.com/repos/owner/repo/pulls",
        body=json.dumps(prs_response),
        headers={"Content-Type": "application/json"},
        status=200,
    )

    # Test the ListPRsOp
    with patch("github.Github") as mock_github:
        mock_repo = mock_github.return_value.get_repo.return_value
        mock_prs = mock_repo.get_pulls.return_value
        mock_prs.__iter__.return_value = prs_response

        op = ListPRsOp(root_dir="owner/repo")
        result = pytest.mark.asyncio(op.__call__())

        assert len(result) == 1
        assert result[0]["number"] == 201
        assert result[0]["title"] == "Test PR"
        assert result[0]["state"] == "open"
        assert result[0]["base"]["ref"] == "main"
        assert result[0]["head"]["ref"] == "feature-branch"
