import functools
import operator
import os
from typing import Annotated, List
from typing_extensions import TypedDict

from langchain_core.messages import BaseMessage, HumanMessage
from langchain_openai.chat_models import ChatOpenAI
from langgraph.prebuilt import ToolNode
from langgraph.graph import StateGraph, END
import functools

from agents.agent import agent_node, create_agent
from agents.presenters_team.tools import generate_video_slide, merge_video_slides


# Presenters team graph state
class PresentersTeamState(TypedDict):
    # A message is added after each team member finishes
    messages: Annotated[List[BaseMessage], operator.add]
    # The team members are tracked so they are aware of
    # the others' skill-sets
    team_members: List[str]
    # Used to route work. The supervisor calls a function
    # that will update this every time it makes a decision
    next: str


llm = ChatOpenAI(model=os.getenv("OPENAI_GPT_MODEL_NAME"), max_tokens=2500)

tools = [generate_video_slide, merge_video_slides]
tool_node = ToolNode(tools)

# Slide Planner agent
presentation_planner_agent = create_agent(
    llm,
    tools,
    "You are a presentation planner assistant. You must create a video presentation "
    "based on the given JSON formatted data of slides."
    "\nFollow these steps sequentially:"
    "\n1. Generate a video slide based on the given slide data for each slide using the tool"
    "\n2. repeat step one for each slide"
    "\n3. Merge all the generated video slides into a single video presentation using the tool"
    "\n4. Return the path of the generated video presentation",
)


presentation_planner_node = functools.partial(agent_node, agent=presentation_planner_agent, name="PresentationPlanner", team="Presenters team")

# Define the function that determines whether to continue or not
def should_continue(state):
    messages = state["messages"]
    last_message = messages[-1]
    try:
        # If there are no tool calls, then we finish
        if not last_message.get('tool_calls'):
            return "end"
        # Otherwise if there is, we continue
        else:
            return "continue"
    except Exception:
        return "end"


presenters_graph = StateGraph(PresentersTeamState)

presenters_graph.add_node("PresentationPlanner", presentation_planner_node)
presenters_graph.add_node("action", tool_node)

presenters_graph.add_conditional_edges(
    "PresentationPlanner",
    should_continue,
    {
        "continue": "action",
        "end": END,
    },
)
presenters_graph.add_edge("action", "PresentationPlanner")

presenters_graph.set_entry_point("PresentationPlanner")
chain = presenters_graph.compile()


# The following functions interoperate between the top level graph state
# and the state of the presenters sub-graph
# this makes it so that the states of each graph don't get intermixed
def enter_chain(message: str):
    results = {
        "messages": [HumanMessage(content=message)],
    }
    return results


presenters_chain = enter_chain | chain
