"""
This module provides the actual GitHub API integration tools that our agent can use.
It implements two main functions:
1. create_github_pull_request: Creates a new pull request
2. list_github_branches: Lists repository branches
"""

import os
from typing import Dict, Any

import requests
from dotenv import load_dotenv
from langchain_core.tools import tool

# Load environment variables from .env file
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

    # Check if GitHub token is configured
    if not GITHUB_TOKEN:
        return {"error": "GitHub token not configured"}

    # Set up headers for GitHub API request
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json",
        "Content-Type": "application/json"
    }

    # Prepare the pull request data
    pr_data = {
        "title": title,
        "body": body,
        "head": head_branch,
        "base": base_branch
    }

    # Construct the API endpoint URL
    url = f"{GITHUB_API_BASE}/repos/{repo_owner}/{repo_name}/pulls"

    try:
        # Make the API request to create the pull request
        response = requests.post(url, headers=headers, json=pr_data)

        if response.status_code == 201:  # 201 means Created
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
            # Handle error response
            error_detail = response.json() if response.content else {"message": "Unknown error"}
            return {
                "success": False,
                "error": f"Failed to create PR: {response.status_code}",
                "details": error_detail.get("message", "No additional details")
            }

    except requests.RequestException as e:
        # Handle network or request errors
        return {
            "success": False,
            "error": f"Request failed: {str(e)}"
        }

@tool
def list_github_branches(repo_owner: str, repo_name: str, open_only: bool = False) -> Dict[str, Any]:
    """
    List branches in a GitHub repository.
    
    Args:
        repo_owner: GitHub username or organization name
        repo_name: Repository name
        open_only: If True, only return branches that have open pull requests
    
    Returns:
        Dictionary containing branch information
    """

    # Check if GitHub token is configured
    if not GITHUB_TOKEN:
        return {"error": "GitHub token not configured"}

    # Set up headers for GitHub API request
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

    # First get all branches from the repository
    url = f"{GITHUB_API_BASE}/repos/{repo_owner}/{repo_name}/branches"
    
    try:
        # Make the API request to list branches
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            return {
                "success": False,
                "error": f"Failed to list branches: {response.status_code}"
            }

        # Extract branch names from the response
        branches = response.json()
        branch_names = [branch["name"] for branch in branches]

        # If we don't need to filter for open branches, return all branches
        if not open_only:
            return {
                "success": True,
                "branches": branch_names
            }

        # If open_only is True, we need to check which branches have open PRs
        open_branches = set()
        page = 1
        while True:
            # Get open pull requests page by page
            prs_url = f"{GITHUB_API_BASE}/repos/{repo_owner}/{repo_name}/pulls?state=open&page={page}"
            prs_response = requests.get(prs_url, headers=headers)
            
            if prs_response.status_code != 200:
                return {
                    "success": False,
                    "error": f"Failed to list pull requests: {prs_response.status_code}"
                }

            prs = prs_response.json()
            if not prs:  # No more PRs to process
                break

            # Add branch names from open PRs to our set
            for pr in prs:
                open_branches.add(pr["head"]["ref"])
            
            page += 1

        return {
            "success": True,
            "branches": list(open_branches)
        }

    except requests.RequestException as e:
        # Handle network or request errors
        return {
            "success": False,
            "error": f"Request failed: {str(e)}"
        }
