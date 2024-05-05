import functools
import operator
import os
from typing import Annotated, List
from typing_extensions import TypedDict

from langchain_core.messages import BaseMessage, HumanMessage
from langchain_openai.chat_models import ChatOpenAI
from langgraph.graph import END, StateGraph
import functools

from agents.agent import agent_node, create_agent
from agents.researcher_team.tools import scrape_webpage, search_google
from utilities.utils import save_draft


# Research team graph state
class ResearchTeamState(TypedDict):
    # A message is added after each team member finishes
    messages: Annotated[List[BaseMessage], operator.add]
    # The team members are tracked so they are aware of
    # the others' skill-sets
    team_members: List[str]
    # Used to route work. The supervisor calls a function
    # that will update this every time it makes a decision
    next: str


llm = ChatOpenAI(model=os.getenv("OPENAI_GPT_MODEL_NAME"), max_tokens=2500)

# Researcher agent
researcher_agent = create_agent(
    llm,
    [scrape_webpage, search_google],
    "You are a research assistant. Follow these steps sequentially:"
    "\n1. Use google search tool to get information about the given topic."
    "\n2. use the tool to scrape webpages for more detailed information."
    "\n3. repeat if needed."
    "\n4. if the returned information is not clear, use your own knowledge to fill the gaps."
)
researcher_node = functools.partial(
    agent_node, agent=researcher_agent, name="Researcher"
)

# Writer agent
writer_agent = create_agent(
    llm,
    [],
    "You are a article writer assistant working in a team of researchers. Follow these steps sequentially:"
    "\n1. You must ask the researcher assistant to get detailed information "
    'about a topic by replying "RESEARCH: the topic you want to know more about".'
    "\n2. Write an article of 700~1000 words on the given topic. Make sure to explain in details."
    "\n3. Double-check your work and make sure it's ready for publication."
)
writer_node = functools.partial(agent_node, agent=writer_agent, name="Writer")


def writer_researcher_edge_condition(state):
    messages = state["messages"]
    last_message = messages[-1]
    # send the message to the researcher agent
    if "RESEARCH:" in last_message.content:
        return "Researcher"
    # Otherwise, return the value
    else:
        # Saving draft
        save_draft(last_message.content, "article")
        return "end"


research_graph = StateGraph(ResearchTeamState)
research_graph.add_node("Researcher", researcher_node)
research_graph.add_node("Writer", writer_node)

# Define the control flow
research_graph.add_edge("Researcher", "Writer")
research_graph.add_conditional_edges(
    "Writer",
    writer_researcher_edge_condition,
    {"Researcher": "Researcher", "Writer": "Writer", "end": END},
)


research_graph.set_entry_point("Writer")
chain = research_graph.compile()


# The following functions interoperate between the top level graph state
# and the state of the research sub-graph
# this makes it so that the states of each graph don't get intermixed
def enter_chain(message: str):
    results = {
        "messages": [HumanMessage(content=message)],
    }
    return results


research_chain = enter_chain | chain
