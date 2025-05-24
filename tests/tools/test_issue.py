import pytest

from dev_kit_gh_mcp_server.tools import CreateIssueOp, ReadIssueCommentsOp


@pytest.fixture
def issue_post_response(repo_data, repo_responses):
    """Fixture for mocked issue creation response."""
    repo_url, repo_api_url, repo_response = repo_data
    issue_url_443 = f"https://api.github.com:443/repos/{repo_url}/issues"
    new_issue = {
        "id": 101,
        "number": 42,
        "title": "Test Issue",
        "state": "open",
        "user": {"login": "octocat"},
        "body": "This is a test issue",
    }

    repo_responses.add(
        repo_responses.POST,
        issue_url_443,
        json=new_issue,
        status=201,
    )
    return repo_responses, repo_url


@pytest.fixture
def issue_get_response(repo_data, repo_responses):
    """Fixture for mocked issue retrieval response."""
    repo_url, repo_api_url, repo_response = repo_data
    issue_url_443 = f"https://api.github.com:443/repos/{repo_url}/issues/42"
    issue_url = f"https://api.github.com/repos/{repo_url}/issues/42"
    issue_data = {
        "id": 101,
        "number": 42,
        "title": "Test Issue",
        "state": "open",
        "user": {"login": "octocat"},
        "body": "This is a test issue",
        "url": issue_url,
    }

    repo_responses.add(
        repo_responses.GET,
        issue_url_443,
        json=issue_data,
        status=200,
    )

    # Add mock for issue comments endpoint
    comments_url_443 = f"https://api.github.com:443/repos/{repo_url}/issues/42/comments"
    comments_data = [
        {
            "id": 1,
            "node_id": "MDEyOklzc3VlQ29tbWVudDE=",
            "url": f"https://api.github.com/repos/{repo_url}/issues/comments/1",
            "html_url": f"https://github.com/{repo_url}/issues/42#issuecomment-1",
            "body": "Hello from test!",
            "user": {
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
            "created_at": "2011-04-14T16:00:49Z",
            "updated_at": "2011-04-14T16:00:49Z",
            "issue_url": f"https://api.github.com/repos/{repo_url}/issues/42",
            "author_association": "COLLABORATOR",
        }
    ]
    repo_responses.add(
        repo_responses.GET,
        comments_url_443,
        json=comments_data,
        status=200,
    )
    return repo_responses, repo_url


@pytest.mark.asyncio
async def test_create_issue_op_success(issue_post_response):
    repo_responses, repo_url = issue_post_response
    op = CreateIssueOp(root_dir=repo_url, token="fake-token")
    issue = await op(title="Test Issue", body="This is a test issue", assignees=[], labels=[])
    assert issue.title == "Test Issue"
    assert issue.body == "This is a test issue"
    assert issue.number == 42


@pytest.mark.asyncio
async def test_write_and_read_issue_comment(issue_get_response):
    repo_responses, repo_url = issue_get_response
    # comment_url = f"https://api.github.com:443/repos/{repo_url}/issues/42/comments"

    read_op = ReadIssueCommentsOp(root_dir=repo_url, token="fake-token")
    comments = await read_op(issue_number=42)
    assert any(getattr(c, "body", None) == "Hello from test!" for c in comments)
