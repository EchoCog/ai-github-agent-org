from github_agent import GitHubAgent


def main():
    """Example usage of the GitHub agent."""

    agent = GitHubAgent()

    print("=== Example 1: List All Branches ===")
    list_branches_request = "List all branches in the repository 'myuser/my-awesome-project'"

    list_branches_response = agent.run(list_branches_request)
    print("Response:", list_branches_response)
    print("\n" + "="*50 + "\n")

    # Example 1: Create a pull request with specific parameters
    print("=== Example 2: Creating a Pull Request ===")
    create_pr_request = """
    Create a pull request in the repository 'myuser/my-awesome-project'
    from branch 'my-branch' to 'main'.

    Use this title: 'Add user authentication system'

    And this description: 'This PR implements a comprehensive user authentication
    system including login, registration, password reset, and session management.

    Key features:
    - JWT-based authentication
    - Password hashing with bcrypt
    - Email verification
    - Rate limiting for login attempts
    - Comprehensive unit tests

    Fixes #123'
    """

    create_pr_response = agent.run(create_pr_request)
    print("Response:", create_pr_response)
    print("\n" + "="*50 + "\n")

if __name__ == "__main__":
    main()
