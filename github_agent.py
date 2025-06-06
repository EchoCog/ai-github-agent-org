from typing import Dict, List

from langchain_core.messages import SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import MessagesState, StateGraph
from langgraph.prebuilt import ToolNode

from github_tools import create_github_pull_request, list_github_branches


class GitHubAgent:
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4",
            temperature=0
        )

        # Create tools list
        self.tools = [create_github_pull_request, list_github_branches]

        # Bind tools to LLM
        self.llm_with_tools = self.llm.bind_tools(self.tools)

        # Create the graph
        self.graph = self._create_graph()

    def _create_graph(self):
        """Create the LangGraph workflow."""

        def should_continue(state: MessagesState) -> str:
            """Decide whether to continue with tool calls or end."""
            last_message = state["messages"][-1]
            if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
                return "tools"
            return "end"

        def call_model(state: MessagesState) -> Dict[str, List]:
            """Call the LLM with tools."""
            messages = state["messages"]
            response = self.llm_with_tools.invoke(messages)
            return {"messages": [response]}

        # Create the graph
        workflow = StateGraph(MessagesState)

        # Add nodes
        workflow.add_node("agent", call_model)
        workflow.add_node("tools", ToolNode(self.tools))

        # Set entry point
        workflow.set_entry_point("agent")

        # Add conditional edges
        workflow.add_conditional_edges(
            "agent",
            should_continue,
            {
                "tools": "tools",
                "end": "__end__"
            }
        )

        # Add edge from tools back to agent
        workflow.add_edge("tools", "agent")

        return workflow.compile()

    def run(self, user_input: str) -> str:
        """Process user input and return response."""

        system_message = SystemMessage(content="""
        You are a helpful GitHub assistant that can create pull requests and manage repositories.
        
        When users ask you to create a pull request, extract the following information:
        - Repository owner and name
        - Source branch (head) and target branch (base)
        - Pull request title and description
        
        If any required information is missing, ask the user to provide it.
        
        Always be clear about what actions you're taking and provide helpful feedback.
        """)

        messages = [system_message, HumanMessage(content=user_input)]

        result = self.graph.invoke({"messages": messages})

        # Return the last message content
        return result["messages"][-1].content
