"""
This is the main entry point for our GitHub repository management tool.
It provides a conversational interface for interacting with GitHub operations.
"""

from github_agent import GitHubAgent


def main():
    """GitHub repository management tool with conversational interface."""

    # Initialize our GitHub agent
    agent = GitHubAgent()

    # Welcome message
    print("Hey! How can I help you today?")
    print("You can ask me to:")
    print("  - Create a PR (e.g., 'create me a PR in the repo my-org/my-repo from branch feature-x to main')")
    print("  - List branches (e.g., 'list all open branches in my-org/my-repo')")
    print("Type 'exit' or 'quit' to end the conversation.\n")

    while True:
        try:
            # Get user input
            user_input = input("> ").strip()

            # Check for exit command
            if user_input.lower() in ['exit', 'quit']:
                print("Goodbye! Have a great day!")
                break

            # Skip empty input
            if not user_input:
                continue

            # Process the request through our agent
            response = agent.run(user_input)
            print("\nResponse:", response, "\n")

        except KeyboardInterrupt:
            print("\nGoodbye! Have a great day!")
            break
        except Exception as e:
            print(f"\nOops! Something went wrong: {str(e)}\n")


if __name__ == "__main__":
    main()
