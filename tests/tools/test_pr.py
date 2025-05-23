import pytest

from dev_kit_gh_mcp_server.tools import CreatePROp


@pytest.mark.asyncio
async def test_create_pr_op_success(repo_data, responses):
    repo_url, repo_api_url, repo_response = repo_data
    pr_url_443 = f"https://api.github.com:443/repos/{repo_url}/pulls"
    new_pr = {
        "id": 202,
        "number": 7,
        "title": "Test PR",
        "state": "open",
        "user": {"login": "octocat"},
        "body": "This is a test PR",
        "head": {"ref": "feature-branch"},
        "base": {"ref": "main"},
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
        pr_url_443,
        json=new_pr,
        status=201,
    )
    op = CreatePROp(root_dir=repo_url, token="fake-token")
    pr = await op(title="Test PR", body="This is a test PR", head="feature-branch", base="main")
    # Always use attribute access for the mock object
    assert getattr(pr, "title", None) == "Test PR"
    assert getattr(pr, "body", None) == "This is a test PR"
    assert getattr(pr, "number", None) == 7
