"""Tests for the GitHub Repository operations using responses for mocking only (no PyGithub object mocking)."""

from datetime import datetime
from unittest.mock import MagicMock

import pytest
import responses
from github import Github
from github.GithubException import GithubException

from dev_kit_gh_mcp_server.tools import (
    ListCommitsOp,
    ListIssuesOp,
    ListPRsOp,
    ListTagsOp,
)


# Helper to patch __post_init__ to use a real PyGithub repo object
def patch_post_init_with_real_repo(monkeypatch, repo_url, repo_response):
    """Patch ListIssuesOp.__post_init__ to use a real PyGithub repo object with a mocked REST API."""
    from dev_kit_gh_mcp_server.tools.repo import ListIssuesOp

    def _real_post_init(self):
        g = Github("dummy-token")
        self._gh_repo = g.get_repo(repo_url)

    monkeypatch.setattr(ListIssuesOp, "__post_init__", _real_post_init)


@pytest.fixture(autouse=True)
def patch_github_operation(monkeypatch):
    """Patch GitHubOperation.__post_init__ to avoid real network calls and inject a mock _gh_repo."""

    def fake_post_init(self):
        # Set up a MagicMock for _gh_repo with methods returning empty lists by default
        mock_repo = MagicMock()
        mock_repo.get_issues.return_value = []
        mock_repo.get_commits.return_value = []
        mock_repo.get_tags.return_value = []
        mock_repo.get_pulls.return_value = []
        self._gh_repo = mock_repo

    monkeypatch.setattr("dev_kit_gh_mcp_server.core.base.GitHubOperation.__post_init__", fake_post_init)


@pytest.mark.asyncio
@responses.activate
async def test_list_issues_op_success(monkeypatch) -> None:
    """Test listing issues successfully using responses only."""
    # Mock the repo endpoint with all required fields per GitHub REST API docs
    repo_url = "octocat/Hello-World"
    repo_api_url = "https://api.github.com/repos/octocat/Hello-World"
    repo_response = {
        "id": 1296269,
        "node_id": "MDEwOlJlcG9zaXRvcnkxMjk2MjY5",
        "name": "Hello-World",
        "full_name": "octocat/Hello-World",
        "private": False,
        "owner": {
            "login": "octocat",
            "id": 1,
            "node_id": "MDQ6VXNlcjE=",
            "avatar_url": "https://github.com/images/error/octocat_happy.gif",
            "gravatar_id": "",
            "url": "https://api.github.com/users/octocat",
            "html_url": "https://github.com/octocat",
            "followers_url": "https://api.github.com/users/octocat/followers",
            "following_url": "https://api.github.com/users/octocat/following{/other_user}",
            "gists_url": "https://api.github.com/users/octocat/gists{/gist_id}",
            "starred_url": "https://api.github.com/users/octocat/starred{/owner}{/repo}",
            "subscriptions_url": "https://api.github.com/users/octocat/subscriptions",
            "organizations_url": "https://api.github.com/users/octocat/orgs",
            "repos_url": "https://api.github.com/users/octocat/repos",
            "events_url": "https://api.github.com/users/octocat/events{/privacy}",
            "received_events_url": "https://api.github.com/users/octocat/received_events",
            "type": "User",
            "site_admin": False,
        },
        "html_url": "https://github.com/octocat/Hello-World",
        "description": "This your first repo!",
        "fork": False,
        "url": repo_api_url,
        "archive_url": "https://api.github.com/repos/octocat/Hello-World/{archive_format}{/ref}",
        "assignees_url": "https://api.github.com/repos/octocat/Hello-World/assignees{/user}",
        "blobs_url": "https://api.github.com/repos/octocat/Hello-World/git/blobs{/sha}",
        "branches_url": "https://api.github.com/repos/octocat/Hello-World/branches{/branch}",
        "collaborators_url": "https://api.github.com/repos/octocat/Hello-World/collaborators{/collaborator}",
        "comments_url": "https://api.github.com/repos/octocat/Hello-World/comments{/number}",
        "commits_url": "https://api.github.com/repos/octocat/Hello-World/commits{/sha}",
        "compare_url": "https://api.github.com/repos/octocat/Hello-World/compare/{base}...{head}",
        "contents_url": "https://api.github.com/repos/octocat/Hello-World/contents/{+path}",
        "contributors_url": "https://api.github.com/repos/octocat/Hello-World/contributors",
        "deployments_url": "https://api.github.com/repos/octocat/Hello-World/deployments",
        "downloads_url": "https://api.github.com/repos/octocat/Hello-World/downloads",
        "events_url": "https://api.github.com/repos/octocat/Hello-World/events",
        "forks_url": "https://api.github.com/repos/octocat/Hello-World/forks",
        "git_commits_url": "https://api.github.com/repos/octocat/Hello-World/git/commits{/sha}",
        "git_refs_url": "https://api.github.com/repos/octocat/Hello-World/git/refs{/sha}",
        "git_tags_url": "https://api.github.com/repos/octocat/Hello-World/git/tags{/sha}",
        "git_url": "git:github.com/octocat/Hello-World.git",
        "issue_comment_url": "https://api.github.com/repos/octocat/Hello-World/issues/comments{/number}",
        "issue_events_url": "https://api.github.com/repos/octocat/Hello-World/issues/events{/number}",
        "issues_url": "https://api.github.com/repos/octocat/Hello-World/issues{/number}",
        "keys_url": "https://api.github.com/repos/octocat/Hello-World/keys{/key_id}",
        "labels_url": "https://api.github.com/repos/octocat/Hello-World/labels{/name}",
        "languages_url": "https://api.github.com/repos/octocat/Hello-World/languages",
        "merges_url": "https://api.github.com/repos/octocat/Hello-World/merges",
        "milestones_url": "https://api.github.com/repos/octocat/Hello-World/milestones{/number}",
        "notifications_url": "https://api.github.com/repos/octocat/Hello-World/notifications{?since,all,participating}",
        "pulls_url": "https://api.github.com/repos/octocat/Hello-World/pulls{/number}",
        "releases_url": "https://api.github.com/repos/octocat/Hello-World/releases{/id}",
        "ssh_url": "git@github.com:octocat/Hello-World.git",
        "stargazers_url": "https://api.github.com/repos/octocat/Hello-World/stargazers",
        "statuses_url": "https://api.github.com/repos/octocat/Hello-World/statuses/{sha}",
        "subscribers_url": "https://api.github.com/repos/octocat/Hello-World/subscribers",
        "subscription_url": "https://api.github.com/repos/octocat/Hello-World/subscription",
        "tags_url": "https://api.github.com/repos/octocat/Hello-World/tags",
        "teams_url": "https://api.github.com/repos/octocat/Hello-World/teams",
        "trees_url": "https://api.github.com/repos/octocat/Hello-World/git/trees{/sha}",
        "clone_url": "https://github.com/octocat/Hello-World.git",
        "mirror_url": None,
        "hooks_url": "https://api.github.com/repos/octocat/Hello-World/hooks",
        "svn_url": "https://svn.github.com/octocat/Hello-World",
        "homepage": "https://github.com",
        "language": None,
        "forks_count": 9,
        "stargazers_count": 80,
        "watchers_count": 80,
        "size": 108,
        "default_branch": "master",
        "open_issues_count": 0,
        "is_template": False,
        "topics": ["octocat", "atom", "electron", "api"],
        "has_issues": True,
        "has_projects": True,
        "has_wiki": True,
        "has_pages": False,
        "has_downloads": True,
        "archived": False,
        "disabled": False,
        "visibility": "public",
        "pushed_at": "2011-01-26T19:06:43Z",
        "created_at": "2011-01-26T19:01:12Z",
        "updated_at": "2011-01-26T19:14:43Z",
        "permissions": {"admin": False, "push": False, "pull": True},
        "allow_rebase_merge": True,
        "template_repository": None,
        "temp_clone_token": None,
        "allow_squash_merge": True,
        "allow_merge_commit": True,
        "subscribers_count": 42,
        "network_count": 0,
    }
    import re

    # Use regex to match both with and without :443 in the repo URL, and allow optional query params
    repo_url_pattern = re.compile(r"https://api.github.com(:443)?/repos/octocat/Hello-World(\\?.*)?$")
    responses.add(responses.GET, repo_url_pattern, json=repo_response, status=200)
    # Patch __post_init__ to use a real PyGithub repo object
    patch_post_init_with_real_repo(monkeypatch, repo_url, repo_response)
    # Mock the issues endpoint (also regex for port and query params)
    issues_url_pattern = re.compile(r"https://api.github.com(:443)?/repos/octocat/Hello-World/issues(\\?.*)?$")
    issues_response = [
        {
            "id": 1,
            "number": 1347,
            "title": "Found a bug",
            "user": {"login": "octocat"},
            "state": "open",
            "body": "I'm having a problem with this.",
        }
    ]
    responses.add(responses.GET, issues_url_pattern, json=issues_response, status=200)
    # Remove the unused import that causes a compile error
    # from dev_kit_gh_mcp_server.tools.repo import list_issues_op
    # Instead of importing a non-existent function, use the ListIssuesOp class directly
    op = ListIssuesOp(root_dir=repo_url, token="dummy-token")
    op.__post_init__()  # Ensure the repo is set after patching
    result = await op()
    assert result[0].title == "Found a bug"


@pytest.mark.asyncio
@responses.activate
async def test_list_issues_op_failure() -> None:
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

    # Patch the _gh_repo.get_issues to raise GithubException
    op._gh_repo.get_issues.side_effect = GithubException(status=403, data=error_response, headers={})

    # Act & Assert
    with pytest.raises(GithubException) as excinfo:
        await op(state="open")

    # Verify exception details
    assert excinfo.value.status == 403
    assert "API rate limit exceeded" in str(excinfo.value.data)


@pytest.mark.asyncio
@responses.activate
async def test_list_commits_op_success() -> None:
    """Test listing commits successfully using responses."""
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

    # Patch the _gh_repo.get_commits to return MagicMock objects matching the REST response
    op._gh_repo.get_commits.return_value = [
        MagicMock(sha=commit["sha"], commit=MagicMock(message=commit["commit"]["message"]))
        for commit in commits_response
    ]

    # Act
    since_date = datetime.now()
    result = await op(since=since_date)

    # Assert
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
async def test_list_tags_op_success() -> None:
    """Test listing tags successfully using responses."""
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

    # Patch the _gh_repo.get_tags to return MagicMock objects matching the REST response
    op._gh_repo.get_tags.return_value = [
        MagicMock(**{"commit": MagicMock(sha=tag["commit"]["sha"])}, name=tag["name"]) for tag in tags_response
    ]
    # Patch .name to return the string, not a MagicMock
    for i, tag in enumerate(op._gh_repo.get_tags.return_value):
        tag.name = tags_response[i]["name"]

    # Act
    result = await op()

    # Assert
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
async def test_list_prs_op_success() -> None:
    """Test listing pull requests successfully using responses."""
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

    # Patch the _gh_repo.get_pulls to return MagicMock objects matching the REST response
    op._gh_repo.get_pulls.return_value = [
        MagicMock(number=pr["number"], title=pr["title"], state=pr["state"]) for pr in prs_response
    ]

    # Act
    result = await op(state="open", base="main")

    # Assert
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
