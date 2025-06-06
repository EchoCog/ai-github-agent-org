# GitHub AI Agent

An intelligent AI agent that can interact with GitHub repositories through natural language commands. Built with
LangGraph and OpenAI, this tool allows you to create pull requests, list branches, and perform other GitHub operations
using conversational AI.

## Features

- 🤖 **Natural Language Interface**: Interact with GitHub using plain English commands
- 🔧 **Pull Request Creation**: Automatically create PRs with custom titles, descriptions, and branch configurations
- 🌿 **Branch Management**: List and manage repository branches
- 🔗 **GitHub API Integration**: Full integration with GitHub's REST API
- ⚡ **LangGraph Powered**: Built on LangGraph for robust AI workflow management
- 🛡️ **Error Handling**: Comprehensive error handling and user feedback
- 🔌 **Extensible**: Easy to add new GitHub operations and tools

## Prerequisites

- Python 3.8 or higher
- GitHub Personal Access Token
- OpenAI API Key
- Git (for version control)

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd github-ai-agent
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**

   Create a `.env` file in the project root:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   GITHUB_TOKEN=your_github_personal_access_token_here
   ```

## Configuration

### GitHub Personal Access Token

1. Go to GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click "Generate new token (classic)"
3. Select the following scopes:
    - `repo` (Full control of private repositories)
    - `public_repo` (Access public repositories)
4. Copy the generated token and add it to your `.env` file

### OpenAI API Key

1. Visit [OpenAI Platform](https://platform.openai.com/api-keys)
2. Create a new API key
3. Add it to your `.env` file

## Usage

### Basic Usage

```python
from github_agent import GitHubAgent

# Initialize the agent
agent = GitHubAgent()

# Create a pull request
response = agent.run("""
Create a pull request in the repository 'username/repo-name' 
from branch 'feature-branch' to 'main'. 
Title: 'Add new feature'
Description: 'This PR adds an awesome new feature'
""")

print(response)
```

### Command Examples

#### Creating a Pull Request

```python
agent.run("""
Create a pull request in myuser/my-project from branch 'feature/auth' to 'develop'.
Title: 'Implement user authentication'
Description: 'Added login, registration, and password reset functionality'
""")
```

#### Listing Branches

```python
agent.run("List all branches in the repository 'myuser/my-project'")
```

#### Complex PR with Detailed Description

```python
agent.run("""
I need to create a pull request for myuser/awesome-app:
- Source branch: hotfix/security-patch  
- Target branch: main
- Title: Fix critical security vulnerability
- Description: This urgent fix addresses a SQL injection vulnerability. 
  Includes input sanitization, parameterized queries, and additional tests.
""")
```

### Running the Examples

Execute the included example script:

```bash
python github_agent.py
```

This will run through several example scenarios demonstrating different capabilities.

## Dependencies

```txt
langgraph>=0.0.40
langchain-core>=0.1.40
langchain-openai>=0.1.0
requests>=2.31.0
python-dotenv>=1.0.0
```

## Available Tools

### `create_github_pull_request`

Creates a new pull request in a GitHub repository.

**Parameters:**

- `repo_owner` (str): GitHub username or organization
- `repo_name` (str): Repository name
- `title` (str): Pull request title
- `body` (str): Pull request description
- `head_branch` (str): Source branch to merge from
- `base_branch` (str): Target branch to merge into (default: "main")

### `list_github_branches`

Lists all branches in a GitHub repository.

**Parameters:**

- `repo_owner` (str): GitHub username or organization
- `repo_name` (str): Repository name

## Error Handling

The agent includes comprehensive error handling for common scenarios:

- **Invalid credentials**: Clear feedback when GitHub token is missing or invalid
- **Repository not found**: Helpful error messages for non-existent repositories
- **Permission issues**: Guidance when lacking necessary repository permissions
- **Network errors**: Retry suggestions for connectivity issues
- **API rate limits**: Information about GitHub API limits

## Extending the Agent

### Adding New Tools

To add new GitHub operations, create a new tool function:

```python
@tool
def create_github_issue(
    repo_owner: str,
    repo_name: str,
    title: str,
    body: str,
    labels: List[str] = None
) -> Dict[str, Any]:
    """Create a new GitHub issue."""
    # Implementation here
    pass


# Add to the tools list in GitHubAgent.__init__
self.tools = [create_github_pull_request, list_github_branches, create_github_issue]
```

### Customizing the LLM

You can customize the language model settings:

```python
self.llm = ChatOpenAI(
    model="gpt-4",  # or "gpt-3.5-turbo"
    temperature=0,  # Adjust for creativity vs consistency
    max_tokens=1000  # Control response length
)
```

## Troubleshooting

### Common Issues

**"GitHub token not configured"**

- Ensure your `.env` file contains a valid `GITHUB_TOKEN`
- Check that the token has the necessary permissions

**"Failed to create PR: 422"**

- Verify the source and target branches exist
- Ensure you have write access to the repository
- Check that a PR between these branches doesn't already exist

**"Request failed: Connection error"**

- Check your internet connection
- Verify GitHub's API status at [githubstatus.com](https://githubstatus.com)

**OpenAI API errors**

- Verify your OpenAI API key is valid and has sufficient credits
- Check the model name is correct (e.g., "gpt-4" vs "gpt-3.5-turbo")

### Debug Mode

Enable verbose logging by setting the environment variable:

```bash
export LANGCHAIN_VERBOSE=true
```

## Security Considerations

- **Never commit your `.env` file** - Add it to `.gitignore`
- **Use minimal permissions** - Grant only necessary GitHub token scopes
- **Rotate tokens regularly** - GitHub tokens should be rotated periodically
- **Validate inputs** - The agent includes input validation, but always verify in production

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [LangGraph](https://github.com/langchain-ai/langgraph) by LangChain
- Powered by [OpenAI](https://openai.com/) GPT models
- GitHub API integration via [GitHub REST API](https://docs.github.com/en/rest)

## Support

If you encounter any issues or have questions:

1. Check the [Troubleshooting](#troubleshooting) section
2. Search existing [GitHub Issues](../../issues)
3. Create a new issue with detailed information about your problem
4. Join our [Discord community](link-to-discord) for real-time help

---

**Happy coding! 🚀**
