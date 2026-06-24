import pytest

from dev_kit_gh_mcp_server.tools import (
    CreatePROp,
    ListPRReviewsOp,
    ReadPRCommentsOp,
    WritePRCommentOp,
)


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


@pytest.fixture
def pr_create_response(repo_data, responses): # Removed httpx_mock
    """Fixture for mocked pull request create response."""
    repo_url, repo_api_url, repo_response_data_template = repo_data

    # Mock for the initial GET /repo request (by PyGithub)
    # This needs to be a more complete response for PyGithub to initialize correctly.
    repo_get_url = f"https://api.github.com:443/repos/{repo_url}"
    # Use a copy of the template and ensure 'url' is the API url
    full_repo_data = repo_response_data_template.copy()
    full_repo_data["url"] = repo_api_url # Important for PyGithub's Repository object
    full_repo_data["html_url"] = f"https://github.com/{repo_url}"
    full_repo_data["default_branch"] = "main" # Ensure this is present

    responses.get(
        repo_get_url,
        json=full_repo_data,
        status=200,
    )

    # Mock for the POST request to create the PR (by PyGithub)
    # Ensure the URL includes the :443 port, similar to how PyGithub constructs it.
    create_pr_url = f"https://api.github.com:443/repos/{repo_url}/pulls"
    pr_response_data = {
        "id": 1,
        "number": 1347,
        "state": "open",
        "title": "Amazing new feature",
        "user": {"login": "octocat"},
        "body": "Please pull these awesome changes in!",
        "head": {"ref": "new-topic", "sha": "6dcb09b5b57875f334f61aebed695e2e4193db5e"},
        "base": {"ref": "main", "sha": "6dcb09b5b57875f334f61aebed695e2e4193db5e"},
        "html_url": f"https://github.com/{repo_url}/pull/1347", # Match repo_url
    }
    responses.post(
        create_pr_url,
        json=pr_response_data,
        status=201,
    )
    return responses, repo_url, pr_response_data


@pytest.mark.asyncio
async def test_create_pr_op_success(pr_create_response):
    responses, repo_url, pr_response_data = pr_create_response # Removed httpx_mock
    op = CreatePROp(root_dir=repo_url, token="fake-token")
    pr = await op(
        title="Amazing new feature",
        body="Please pull these awesome changes in!",
        head="new-topic",
        base="main",
    )
    assert pr is not None
    assert pr.title == pr_response_data["title"]
    assert pr.body == pr_response_data["body"]
    assert pr.number == pr_response_data["number"]
    assert pr.head.ref == pr_response_data["head"]["ref"]
    assert pr.base.ref == pr_response_data["base"]["ref"]
    assert pr.html_url == pr_response_data["html_url"]


@pytest.fixture
def pr_comments_response(repo_data, responses):
    """Fixture for mocked pull request comments response."""
    repo_url, repo_api_url, repo_response_data_template = repo_data
    pr_number = 7 # Sample PR number

    # 0. Mock for the initial GET /repo request (by PyGithub's get_repo())
    # This is necessary for self._gh_repo to be initialized correctly.
    base_repo_get_url = f"https://api.github.com:443/repos/{repo_url}"
    full_repo_data = repo_response_data_template.copy()
    full_repo_data["url"] = repo_api_url # Important for PyGithub's Repository object
    full_repo_data["html_url"] = f"https://github.com/{repo_url}"
    full_repo_data["default_branch"] = "main" # Ensure this is present
    responses.get(
        base_repo_get_url,
        json=full_repo_data,
        status=200,
    )

    # 1. Mock for PyGithub to get the PR object (via get_pull())
    pr_get_url = f"https://api.github.com:443/repos/{repo_url}/pulls/{pr_number}"
    pr_data_for_get_pull = {
        "id": 101,
        "number": pr_number,
        "state": "open",
        "title": "PR for comments",
        "user": {"login": "octocat"},
        "body": "This PR has comments.",
        "url": f"{repo_api_url}/pulls/{pr_number}", # PyGithub needs this
        "html_url": f"https://github.com/{repo_url}/pull/{pr_number}",
        "comments_url": f"{repo_api_url}/issues/{pr_number}/comments", # General issue comments
        # PyGithub uses get_review_comments() which hits /pulls/:pr_number/comments
        "_links": {
             "comments": {"href": f"{repo_api_url}/pulls/{pr_number}/comments"},
             "review_comments": {"href": f"{repo_api_url}/pulls/{pr_number}/comments"}
        }
    }
    responses.get(
        pr_get_url,
        json=pr_data_for_get_pull,
        status=200
    )

    # 2. Mock for the actual review comments
    # ReadPRCommentsOp seems to use get_review_comments() which hits /pulls/:pr_number/comments
    comments_get_url = f"https://api.github.com:443/repos/{repo_url}/pulls/{pr_number}/comments"
    sample_comments_data = [
        {
            "id": 1,
            "pull_request_review_id": 42,
            "node_id": "MDI0OlB1bGxSZXF1ZXN0UmV2aWV3Q29tbWVudDE=",
            "user": {"login": "octocat"},
            "body": "This is the first comment.",
            "path": "file1.txt",
            "position": 1,
            "commit_id": "6dcb09b5b57875f334f61aebed695e2e4193db5e",
            "created_at": "2011-04-14T16:00:49Z",
            "updated_at": "2011-04-14T16:00:49Z",
            "html_url": "https://github.com/octocat/Hello-World/pull/1#discussion_r1",
            "pull_request_url": f"https://api.github.com/repos/{repo_url}/pulls/{pr_number}"
        },
        {
            "id": 2,
            "pull_request_review_id": 42,
            "node_id": "MDI0OlB1bGxSZXF1ZXN0UmV2aWV3Q29tbWVudDI=",
            "user": {"login": "another_user"},
            "body": "This is a reply to the first comment.",
            "path": "file1.txt",
            "position": 1,
            "in_reply_to_id": 1,
            "commit_id": "6dcb09b5b57875f334f61aebed695e2e4193db5e",
            "created_at": "2011-04-14T16:01:49Z",
            "updated_at": "2011-04-14T16:01:49Z",
            "html_url": "https://github.com/octocat/Hello-World/pull/1#discussion_r2",
            "pull_request_url": f"https://api.github.com/repos/{repo_url}/pulls/{pr_number}"
        }
    ]
    responses.get(
        comments_get_url,
        json=sample_comments_data,
        status=200
    )

    return responses, repo_url, pr_number, sample_comments_data


@pytest.mark.asyncio
async def test_read_pr_comments_op_success(pr_comments_response):
    responses, repo_url, pr_number, sample_comments_data = pr_comments_response
    op = ReadPRCommentsOp(root_dir=repo_url, token="fake-token")
    comments = await op(pr_number=pr_number)

    assert comments is not None
    assert len(comments) == len(sample_comments_data)
    assert comments[0].body == sample_comments_data[0]["body"]
    assert comments[1].body == sample_comments_data[1]["body"]


@pytest.fixture
def pr_write_comment_response(repo_data, responses):
    """Fixture for mocked pull request write comment response."""
    repo_url, repo_api_url, repo_response_data_template = repo_data
    pr_number = 9
    comment_body_to_write = "This is a new comment!"

    # 0. Mock for PyGithub's get_repo()
    base_repo_get_url = f"https://api.github.com:443/repos/{repo_url}"
    full_repo_data = repo_response_data_template.copy()
    full_repo_data["url"] = repo_api_url
    full_repo_data["html_url"] = f"https://github.com/{repo_url}"
    full_repo_data["default_branch"] = "main"
    responses.get(
        base_repo_get_url,
        json=full_repo_data,
        status=200,
    )

    # 1. Mock for PyGithub's get_pull()
    pr_get_url = f"https://api.github.com:443/repos/{repo_url}/pulls/{pr_number}"
    # PyGithub's create_issue_comment uses issue_url from the PR object.
    # The issue_url for a PR is typically its own API URL.
    # Or more specifically, PRs are issues, so their comments endpoint is /issues/:number/comments
    issue_comments_url_for_pr = f"{repo_api_url}/issues/{pr_number}/comments"
    pr_data_for_get_pull = {
        "id": 201,
        "number": pr_number,
        "state": "open",
        "title": "PR for writing comments",
        "user": {"login": "testuser"},
        "body": "This PR is ready for comments.",
        "url": f"{repo_api_url}/pulls/{pr_number}",
        "html_url": f"https://github.com/{repo_url}/pull/{pr_number}",
        "comments_url": issue_comments_url_for_pr, # General issue comments endpoint
        "issue_url": f"{repo_api_url}/issues/{pr_number}" # Crucial for create_issue_comment
    }
    responses.get(
        pr_get_url,
        json=pr_data_for_get_pull,
        status=200
    )

    # 2. Mock for POST to create the comment (PyGithub uses create_issue_comment)
    # This POST goes to the PR's "issue_url" + /comments
    # which is effectively /repos/:owner/:repo/issues/:pr_number/comments

    # The URL PyGithub will POST to for create_issue_comment is derived from PR's issue_url
    # For PR #9, issue_url is .../issues/9, so comments are POSTed to .../issues/9/comments
    post_comment_url = f"https://api.github.com:443/repos/{repo_url}/issues/{pr_number}/comments"

    expected_post_payload = {"body": comment_body_to_write}
    created_comment_response_data = {
        "id": 12345,
        "node_id": "MDExOklzc3VlQ29tbWVudDEyMzQ1",
        "url": f"{repo_api_url}/issues/comments/12345",
        "html_url": f"https://github.com/{repo_url}/pull/{pr_number}#issuecomment-12345",
        "body": comment_body_to_write,
        "user": {"login": "testuser", "id": 1},
        "created_at": "2024-05-20T10:00:00Z",
        "updated_at": "2024-05-20T10:00:00Z",
    }
    responses.post(
        post_comment_url,
        json=created_comment_response_data,
        match=[responses.matchers.json_params_matcher(expected_post_payload)],
        status=201
    )

    return responses, repo_url, pr_number, comment_body_to_write, created_comment_response_data


@pytest.mark.asyncio
async def test_write_pr_comment_op_success(pr_write_comment_response):
    responses, repo_url, pr_number, comment_body, expected_response = pr_write_comment_response
    op = WritePRCommentOp(root_dir=repo_url, token="fake-token")

    created_comment = await op(pr_number=pr_number, body=comment_body)

    assert created_comment is not None
    assert created_comment.body == expected_response["body"]
    assert created_comment.user.login == expected_response["user"]["login"]
    assert created_comment.id == expected_response["id"]
