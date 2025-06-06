import os
from typing import Dict, Any

import requests
from dotenv import load_dotenv
from langchain_core.tools import tool

# Load environment variables
load_dotenv()

# GitHub API configuration
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_API_BASE = "https://api.github.com"

@tool
def create_github_pull_request(
    repo_owner: str,
    repo_name: str,
    title: str,
    body: str,
    head_branch: str,
    base_branch: str = "main"
) -> Dict[str, Any]:
    """
    Create a pull request in a GitHub repository.
    
    Args:
        repo_owner: GitHub username or organization name
        repo_name: Repository name
        title: Pull request title
        body: Pull request description/body
        head_branch: Source branch (the branch you want to merge FROM)
        base_branch: Target branch (the branch you want to merge INTO, defaults to 'main')
    
    Returns:
        Dictionary containing pull request details or error information
    """

    if not GITHUB_TOKEN:
        return {"error": "GitHub token not configured"}

    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json",
        "Content-Type": "application/json"
    }

    # Prepare pull request data
    pr_data = {
        "title": title,
        "body": body,
        "head": head_branch,
        "base": base_branch
    }

    # Create pull request
    url = f"{GITHUB_API_BASE}/repos/{repo_owner}/{repo_name}/pulls"

    try:
        response = requests.post(url, headers=headers, json=pr_data)

        if response.status_code == 201:
            pr_info = response.json()
            return {
                "success": True,
                "pull_request": {
                    "number": pr_info["number"],
                    "title": pr_info["title"],
                    "html_url": pr_info["html_url"],
                    "head": pr_info["head"]["ref"],
                    "base": pr_info["base"]["ref"],
                    "state": pr_info["state"]
                }
            }
        else:
            error_detail = response.json() if response.content else {"message": "Unknown error"}
            return {
                "success": False,
                "error": f"Failed to create PR: {response.status_code}",
                "details": error_detail.get("message", "No additional details")
            }

    except requests.RequestException as e:
        return {
            "success": False,
            "error": f"Request failed: {str(e)}"
        }

@tool
def list_github_branches(repo_owner: str, repo_name: str) -> Dict[str, Any]:
    """
    List branches in a GitHub repository.
    
    Args:
        repo_owner: GitHub username or organization name
        repo_name: Repository name
    
    Returns:
        Dictionary containing branch information
    """

    if not GITHUB_TOKEN:
        return {"error": "GitHub token not configured"}

    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

    url = f"{GITHUB_API_BASE}/repos/{repo_owner}/{repo_name}/branches"

    try:
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            branches = response.json()
            return {
                "success": True,
                "branches": [branch["name"] for branch in branches]
            }
        else:
            return {
                "success": False,
                "error": f"Failed to list branches: {response.status_code}"
            }

    except requests.RequestException as e:
        return {
            "success": False,
            "error": f"Request failed: {str(e)}"
        }
