import pytest

from dev_kit_gh_mcp_server.tools import CreateIssueOp


@pytest.mark.asyncio
async def test_create_issue_op_success(repo_data, responses):
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
    # Only mock the endpoints that are actually called to avoid teardown errors
    responses.add(
        responses.GET,
        f"https://api.github.com:443/repos/{repo_url}",
        json=repo_response,
        status=200,
    )
    responses.add(
        responses.POST,
        issue_url_443,
        json=new_issue,
        status=201,
    )
    op = CreateIssueOp(root_dir=repo_url, token="fake-token")
    issue = await op(title="Test Issue", body="This is a test issue", assignees=[], labels=[])
    assert issue.title == "Test Issue"
    assert issue.body == "This is a test issue"
    assert issue.number == 42
