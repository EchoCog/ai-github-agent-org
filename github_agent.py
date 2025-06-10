"""
This module implements a GitHub agent using LangChain and LangGraph.
It creates an AI agent that can understand natural language requests and perform GitHub operations
using a combination of LLM (Language Model) and tools.
"""

from typing import Dict, List

from langchain_core.messages import SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import MessagesState, StateGraph
from langgraph.prebuilt import ToolNode

from github_tools import create_github_pull_request, list_github_branches


class GitHubAgent:
    def __init__(self):
        # Initialize the language model (GPT-4) with zero temperature for consistent results
        self.llm = ChatOpenAI(
            model="gpt-4",
            temperature=0
        )

        # Define the tools our agent can use
        self.tools = [create_github_pull_request, list_github_branches]

        # Bind the tools to our language model so it knows what operations it can perform
        self.llm_with_tools = self.llm.bind_tools(self.tools)

        # Create the workflow graph that defines how our agent processes requests
        self.graph = self._create_graph()

        # We want to store the messages so the agent can maintain context across different requests
        # For example, this allows the following behaviour:
        # - User: "List branches in my-org/my-repo"
        # - Agent: "Here are the branches: ..."
        # - User: "Create a PR from branch feature-x to main"
        # - Agent: "Creating PR from feature-x to main"
        # Notice that we didn't have to provide the repository information again,
        # since the agent was aware of our previous interaction
        self._messages = []

    def _create_graph(self):
        """Create the LangGraph workflow that defines how our agent processes requests."""

        def should_continue(state: MessagesState) -> str:
            """
            Decision function that determines whether to continue with tool calls or end.
            Returns 'tools' if the last message contains tool calls, otherwise 'end'.
            """
            last_message = state["messages"][-1]
            if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
                return "tools"
            return "end"

        def call_model(state: MessagesState) -> Dict[str, List]:
            """
            Function that calls the LLM with the current state of messages.
            Returns the LLM's response.
            """
            messages = state["messages"]
            response = self.llm_with_tools.invoke(messages)
            return {"messages": [response]}

        # Initialize the workflow graph with a state that tracks messages
        workflow = StateGraph(MessagesState)

        # Add nodes to our graph:
        # - 'agent': Handles LLM interactions
        # - 'tools': Executes GitHub operations
        workflow.add_node("agent", call_model)
        workflow.add_node("tools", ToolNode(self.tools))

        # Set the entry point of our workflow
        workflow.set_entry_point("agent")

        # Define the flow of our workflow:
        # - After agent, check if we need to use tools
        # - If tools are needed, execute them and return to agent
        # - If no tools needed, end the workflow
        workflow.add_conditional_edges(
            "agent",
            should_continue,
            {
                "tools": "tools",
                "end": "__end__"
            }
        )

        # After tools are executed, return to the agent for further processing
        workflow.add_edge("tools", "agent")

        return workflow.compile()

    def run(self, user_input: str) -> str:
        """
        Process user input and return response.
        This is the main entry point for interacting with our GitHub agent.
        """

        # Define the system message that sets the context for our agent
        system_message = SystemMessage(content="""
        You are a helpful GitHub assistant that can create pull requests and manage repositories.
        
        When users ask you to list branches:
        - Look for phrases like "list branches", "show branches", "get branches"
        - Extract the repository owner and name from the format "owner/repo" or phrases like "in repo owner/repo"
        - If the request mentions "open branches" or "open only", set open_only to True
        - Use the list_github_branches tool with the appropriate parameters
        
        When users ask you to create a pull request:
        - Look for phrases like "create PR", "create pull request", "make a PR"
        - Extract the repository owner and name from the format "owner/repo" or phrases like "in repo owner/repo"
        - If the user has not specified the repository owner and name, try to extract it from the previous messages
        - Extract the source branch (head) and target branch (base) from phrases like "from branch X to Y"
        - If the target branch isn't specified, assume it's "main"
        - Use the create_github_pull_request tool with the appropriate parameters
        
        If any required information is missing, ask the user to provide it in a friendly way.
        Always be clear about what actions you're taking and provide helpful feedback.
        Format your responses in a clear, readable way.
        """)
        
        # Create the message list with system context, previous messages, and new user input
        messages = [system_message] + self._messages + [HumanMessage(content=user_input)]

        # Run the workflow and get the result
        result = self.graph.invoke({"messages": messages})
        
        # Store the updated state for next time
        self._messages = result["messages"]

        # Return the content of the last message (the final response)
        return result["messages"][-1].content
