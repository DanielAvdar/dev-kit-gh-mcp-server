import pytest

from dev_kit_gh_mcp_server.tools import ListPRReviewsOp


@pytest.fixture
def pr_reviews_response(repo_data, repo_responses):
    """Fixture for mocked pull request reviews response."""
    repo_url, repo_api_url, repo_response = repo_data
    pr_number = 5
    reviews_url_443 = f"https://api.github.com:443/repos/{repo_url}/pulls/{pr_number}/reviews"
    pr_url_443 = f"https://api.github.com:443/repos/{repo_url}/pulls/{pr_number}"
    pr_url = f"https://api.github.com/repos/{repo_url}/pulls/{pr_number}"
    pr_data = {
        "id": 201,
        "number": pr_number,
        "state": "open",
        "title": "Test PR",
        "user": {"login": "octocat"},
        "body": "This is a test PR",
        "url": pr_url,
    }
    reviews_data = [
        {
            "id": 80,
            "node_id": "MDE3OlB1bGxSZXF1ZXN0UmV2aWV3ODA=",
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
            "body": "Here is the body for the review.",
            "state": "APPROVED",
            "html_url": "https://github.com/octocat/Hello-World/pull/12#pullrequestreview-80",
            "pull_request_url": "https://api.github.com/repos/octocat/Hello-World/pulls/12",
            "_links": {
                "html": {"href": "https://github.com/octocat/Hello-World/pull/12#pullrequestreview-80"},
                "pull_request": {"href": "https://api.github.com/repos/octocat/Hello-World/pulls/12"},
            },
            "submitted_at": "2019-11-17T17:43:43Z",
            "commit_id": "ecdd80bb57125d7ba9641ffaa4d7d2c19d3f3091",
            "author_association": "COLLABORATOR",
        }
    ]
    # Only add mocks with :443 in the URL (PyGithub expects this in your environment)
    pr_url_443 = f"https://api.github.com:443/repos/{repo_url}/pulls/{pr_number}"
    repo_responses.add(
        repo_responses.GET,
        pr_url_443,
        json=pr_data,
        status=200,
    )
    # Register both :443 and non-ported URLs for reviews endpoint

    reviews_url_443 = f"https://api.github.com:443/repos/{repo_url}/pulls/{pr_number}/reviews"
    repo_responses.add(
        repo_responses.GET,
        reviews_url_443,
        json=reviews_data,
        status=200,
    )
    return repo_responses, repo_url


@pytest.mark.asyncio
async def test_list_pr_reviews(pr_reviews_response):
    repo_responses, repo_url = pr_reviews_response
    op = ListPRReviewsOp(root_dir=repo_url, token="fake-token")
    reviews = await op(pr_number=5)
    assert len(reviews) == 1
    assert getattr(reviews[0], "body", None) == "Here is the body for the review."
    assert getattr(reviews[0], "state", None) == "APPROVED"
