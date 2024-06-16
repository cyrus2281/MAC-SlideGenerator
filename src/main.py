import os
import time
from dotenv import load_dotenv
from utilities.utils import set_project_space

load_dotenv()

os.environ["OPENAI_GPT_MODEL_NAME"] = os.getenv("OPENAI_GPT_MODEL_NAME", "gpt-4o")
os.environ["USE_OPENAI_FOR_TEXT_TO_AUDIO"] = os.getenv("USE_OPENAI_FOR_TEXT_TO_AUDIO", "True")
os.environ["SLIDES_WATERMARK"] = os.getenv("SLIDES_WATERMARK", "MLC-Slide-Generator by Cyrus Mobini")

# Setting up project
project_id = int(time.time())
project_space = os.path.join("projects", f"project_{project_id}")
set_project_space(project_space)
print("Project ID:", project_id)
print("Project Space:", project_space)
print("Using the model:", os.getenv("OPENAI_GPT_MODEL_NAME"))
print("Extended Slide Generation: ", os.getenv("EXTENDED_SLIDES", False))

from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_openai.chat_models import ChatOpenAI
from langgraph.graph import END, StateGraph
from typing_extensions import TypedDict
from typing import Annotated, List, Optional
import operator

from agents.agent import create_team_supervisor
from agents.researchers_team.agents import research_chain
from agents.slides_team.agents import slides_chain
from agents.presenters_team.agents import presenters_chain


llm = ChatOpenAI(model=os.getenv("OPENAI_GPT_MODEL_NAME"))

supervisor_node = create_team_supervisor(
    llm,
    "You are a supervisor tasked with managing the flow between the following teams: "
    '\n - "Researchers team". Given the topic, this team will research and write an article.'
    '\n - "Slides team". Given the article, this team will find images and rewrite the article in JSON formatted slides.'
    '\n - "Presenters team": Given the JSON formatted slides, this team will create a video presentation.'
    "\nThe goal is to create a video presentation on the given topic. "
    "\nThe normal flow, unless otherwise specified by the user, must follow:"
    "\nResearchers team -> Slides team -> Presenters team"
    "\nWhen finished, respond with FINISH."
    "\nAvoid calling the same team twice unless necessary."
    "\n\nGiven the following topic, respond with the team to act next. ",
    ["Researchers team", "Slides team", "Presenters team"],
)


# Top-level graph state
class State(TypedDict):
    messages: Annotated[List[BaseMessage], operator.add]
    next: str
    previous_agent: Optional[str]


def get_last_message(state: State) -> str:
    return state["messages"][-1].content


def join_graph(response: dict):
    return {"messages": [response["messages"][-1]]}


# Define the graph.
super_graph = StateGraph(State)
# First add the nodes, which will do the work
super_graph.add_node("Researchers_team", get_last_message | research_chain | join_graph)
super_graph.add_node("Slides_team", get_last_message | slides_chain | join_graph)
super_graph.add_node(
    "Presenters_team", get_last_message | presenters_chain | join_graph
)
super_graph.add_node("supervisor", supervisor_node)

# Define the graph connections, which controls how the logic
# propagates through the program
super_graph.add_edge("Researchers_team", "supervisor")
super_graph.add_edge("Slides_team", "supervisor")
super_graph.add_edge("Presenters_team", "supervisor")

super_graph.add_conditional_edges(
    "supervisor",
    lambda x: x["next"],
    {
        "Researchers team": "Researchers_team",
        "Slides team": "Slides_team",
        "Presenters team": "Presenters_team",
        "FINISH": END,
    },
)
super_graph.set_entry_point("supervisor")
super_graph = super_graph.compile()

iteration_limit = 75 if os.getenv("EXTENDED_SLIDES", False) else 50
# Getting input from console in a while loop till users enters "exit"
prompt = "\nEnter the topic: "
messages = []
while True:
    user_input = input(prompt).strip()
    if not user_input:
        continue
    if user_input == "exit":
        break
    messages.append(HumanMessage(content=user_input))
    for state in super_graph.stream(
        {
            "messages": messages,
        },
        {"recursion_limit": iteration_limit},
    ):
        if "__end__" not in state:
            print("-----")
            print(state)

            if "Researchers_team" in state:
                msg = state["Researchers_team"]["messages"][0].content
                messages.append(AIMessage(content=msg, name="Researchers_team"))
            elif "Slides_team" in state:
                msg = state["Slides_team"]["messages"][0].content
                messages.append(AIMessage(content=msg, name="Slides_team"))
            elif "Presenters_team" in state:
                msg = state["Presenters_team"]["messages"][0].content
                messages.append(AIMessage(content=msg, name="Presenters_team"))

            prompt = "Ask a follow-up request: (Type 'exit' to leave program) "
