import os
import time
from dotenv import load_dotenv
from utilities.utils import set_project_space

load_dotenv()

# Setting up project
project_id = int(time.time())
project_space = os.path.join("temp", f"project_{project_id}")
set_project_space(project_space)
print("Project ID:", project_id)
print("Project Space:", project_space)
print("Using the model:", os.getenv("OPENAI_GPT_MODEL_NAME"))

from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from langchain_openai.chat_models import ChatOpenAI
from langgraph.graph import END, StateGraph
from typing_extensions import TypedDict
from typing import Annotated, List
import operator

from agents.agent import create_team_supervisor
from agents.researchers_team.agents import research_chain
from agents.slides_team.agents import slides_chain
from agents.presenters_team.agents import presenters_chain


llm = ChatOpenAI(model=os.getenv("OPENAI_GPT_MODEL_NAME"))

supervisor_node = create_team_supervisor(
    llm,
    "You are a supervisor tasked with managing the flow between the following teams: "
    "\n - \"Researchers team\". Given the topic, this team will research and write an article."
    "\n - \"Slides team\". Given the article, this team will find images and rewrite the article in JSON formatted slides."
    "\n - \"Presenters team\": Given the JSON formatted slides, this team will create a video presentation."
    "\nThe goal is to create a video presentation on the given topic. "
    "\nThe normal flow, unless otherwise specified by the user, must follow:"
    "\nResearchers team -> Slides team -> Presenters team"
    "\nWhen finished, respond with FINISH."
    "\nAvoid calling the same team twice unless necessary."
    "\n\nGiven the following topic, respond with the team to act next. ",
    ["Researchers team", "Slides team", "Presenters team"]
)


# Top-level graph state
class State(TypedDict):
    messages: Annotated[List[BaseMessage], operator.add]
    next: str


def get_last_message(state: State) -> str:
    return state["messages"][-1].content


def join_graph(response: dict):
    return {"messages": [response["messages"][-1]]}


# Define the graph.
super_graph = StateGraph(State)
# First add the nodes, which will do the work
super_graph.add_node("Researchers team", get_last_message | research_chain | join_graph)
super_graph.add_node("Slides team", get_last_message | slides_chain | join_graph)
super_graph.add_node("Presenters team", get_last_message | presenters_chain | join_graph)
super_graph.add_node("supervisor", supervisor_node)

# Define the graph connections, which controls how the logic
# propagates through the program
super_graph.add_edge("Researchers team", "supervisor")
super_graph.add_edge("Slides team", "supervisor")
super_graph.add_edge("Presenters team", "supervisor")

super_graph.add_conditional_edges(
    "supervisor",
    lambda x: x["next"],
    {
        "Researchers team": "Researchers team",
        "Slides team": "Slides team",
        "Presenters team": "Presenters team",
        "FINISH": END,
    },
)
super_graph.set_entry_point("supervisor")
super_graph = super_graph.compile()

for s in super_graph.stream(
    {
        "messages": [HumanMessage(content="Effects of coffee on body")],
    },
    {"recursion_limit": 50},
):
    if "__end__" not in s:
        print(s)
        print("---")
