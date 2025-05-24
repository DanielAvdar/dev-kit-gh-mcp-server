import pytest

from dev_kit_gh_mcp_server.tools import CreateIssueOp


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
    issue_data = {
        "id": 101,
        "number": 42,
        "title": "Test Issue",
        "state": "open",
        "user": {"login": "octocat"},
        "body": "This is a test issue",
    }

    repo_responses.add(
        repo_responses.GET,
        issue_url_443,
        json=issue_data,
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
