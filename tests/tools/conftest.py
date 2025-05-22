import pytest

# import pytest_responses


@pytest.fixture
def repo_data():
    repo_url = "octocat/Hello-World"
    repo_api_url = f"https://api.github.com/repos/{repo_url}"
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
        "archive_url": f"{repo_api_url}/{{archive_format}}{{/ref}}",
        "assignees_url": f"{repo_api_url}/assignees{{/user}}",
        "blobs_url": f"{repo_api_url}/git/blobs{{/sha}}",
        "branches_url": f"{repo_api_url}/branches{{/branch}}",
        "collaborators_url": f"{repo_api_url}/collaborators{{/collaborator}}",
        "comments_url": f"{repo_api_url}/comments{{/number}}",
        "commits_url": f"{repo_api_url}/commits{{/sha}}",
        "compare_url": f"{repo_api_url}/compare/{{base}}...{{head}}",
        "contents_url": f"{repo_api_url}/contents/{{+path}}",
        "contributors_url": f"{repo_api_url}/contributors",
        "deployments_url": f"{repo_api_url}/deployments",
        "downloads_url": f"{repo_api_url}/downloads",
        "events_url": f"{repo_api_url}/events",
        "forks_url": f"{repo_api_url}/forks",
        "git_commits_url": f"{repo_api_url}/git/commits{{/sha}}",
        "git_refs_url": f"{repo_api_url}/git/refs{{/sha}}",
        "git_tags_url": f"{repo_api_url}/git/tags{{/sha}}",
        "git_url": "git:github.com/octocat/Hello-World.git",
        "issue_comment_url": f"{repo_api_url}/issues/comments{{/number}}",
        "issue_events_url": f"{repo_api_url}/issues/events{{/number}}",
        "issues_url": f"{repo_api_url}/issues{{/number}}",
        "keys_url": f"{repo_api_url}/keys{{/key_id}}",
        "labels_url": f"{repo_api_url}/labels{{/name}}",
        "languages_url": f"{repo_api_url}/languages",
        "merges_url": f"{repo_api_url}/merges",
        "milestones_url": f"{repo_api_url}/milestones{{/number}}",
        "notifications_url": f"{repo_api_url}/notifications{{?since,all,participating}}",
        "pulls_url": f"{repo_api_url}/pulls{{/number}}",
        "releases_url": f"{repo_api_url}/releases{{/id}}",
        "ssh_url": "git@github.com:octocat/Hello-World.git",
        "stargazers_url": f"{repo_api_url}/stargazers",
        "statuses_url": f"{repo_api_url}/statuses/{{sha}}",
        "subscribers_url": f"{repo_api_url}/subscribers",
        "subscription_url": f"{repo_api_url}/subscription",
        "tags_url": f"{repo_api_url}/tags",
        "teams_url": f"{repo_api_url}/teams",
        "trees_url": f"{repo_api_url}/git/trees{{/sha}}",
        "clone_url": "https://github.com/octocat/Hello-World.git",
        "mirror_url": None,
        "hooks_url": f"{repo_api_url}/hooks",
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
    return repo_url, repo_api_url, repo_response


@pytest.fixture
def repo_resp(responses, repo_data):
    repo_url, repo_api_url, repo_response = repo_data
    responses.add(
        responses.GET,
        repo_api_url,
        json=repo_response,
        status=200,
        content_type="application/json",
    )
    return responses


@pytest.fixture
def commits_response():
    return [
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


@pytest.fixture
def tags_response():
    return [
        {
            "name": "v1.0.0",
            "commit": {"sha": "abc123", "url": "https://api.github.com/repos/test-owner/test-repo/commits/abc123"},
        },
        {
            "name": "v2.0.0",
            "commit": {"sha": "def456", "url": "https://api.github.com/repos/test-owner/test-repo/commits/def456"},
        },
    ]


@pytest.fixture
def prs_response():
    return [
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


@pytest.fixture
def repo_responses(commits_response, repo_data, responses):
    repo_url, repo_api_url, repo_response = repo_data
    responses.add(
        responses.GET,
        f"https://api.github.com:443/repos/{repo_url}",
        json=repo_response,
        status=200,
    )

    return responses


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
