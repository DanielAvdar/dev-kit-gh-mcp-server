import pytest

from dev_kit_gh_mcp_server.tools import CreatePROp


@pytest.fixture
def pr_post_responses(repo_data, repo_responses):
    """Fixture to mock GitHub responses for PR operations."""
    # Mock response for creating a pull request
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

    repo_responses.add(
        repo_responses.POST,
        pr_url_443,
        json=new_pr,
        status=201,
    )

    return repo_responses, repo_url


@pytest.fixture
def pr_get_responses(repo_data, repo_responses):
    """Fixture to mock GitHub responses for getting PR details."""
    repo_url, repo_api_url, repo_response = repo_data

    pr_url_443 = f"https://api.github.com:443/repos/{repo_url}/pulls/7"
    pr_details = {
        "id": 202,
        "number": 7,
        "title": "Test PR",
        "state": "open",
        "user": {"login": "octocat"},
        "body": "This is a test PR",
        "head": {"ref": "feature-branch"},
        "base": {"ref": "main"},
    }

    repo_responses.add(
        repo_responses.GET,
        pr_url_443,
        json=pr_details,
        status=200,
    )

    return repo_responses, repo_url


@pytest.mark.asyncio
async def test_create_pr_op_success(pr_post_responses):
    """Test creating a pull request operation."""
    pr_responses, repo_url = pr_post_responses
    op = CreatePROp(root_dir=repo_url, token="fake-token")
    pr = await op(title="Test PR", body="This is a test PR", head="feature-branch", base="main")
    # Always use attribute access for the mock object
    assert getattr(pr, "title", None) == "Test PR"
    assert getattr(pr, "body", None) == "This is a test PR"
    assert getattr(pr, "number", None) == 7
