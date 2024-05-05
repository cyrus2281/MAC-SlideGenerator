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
from agents.slides_team.tools import download_image, google_image_search
from utilities.utils import save_draft


# Slides team graph state
class SlidesTeamState(TypedDict):
    # A message is added after each team member finishes
    messages: Annotated[List[BaseMessage], operator.add]
    # The team members are tracked so they are aware of
    # the others' skill-sets
    team_members: List[str]
    # Used to route work. The supervisor calls a function
    # that will update this every time it makes a decision
    next: str


llm = ChatOpenAI(model=os.getenv("OPENAI_GPT_MODEL_NAME"), max_tokens=2500)

# Image Finder agent
image_finder_agent = create_agent(
    llm,
    [google_image_search, download_image],
    "You are responsible for downloading an image for the given topic. Follow these steps sequentially:"
    "\n1. Use google image search to find relevant images for the given topic."
    "\n2. Use the download image tool to download the most relevant image. Never return the URL."
    "\n3. return the following prompt: "
    "\n ```Here is the image you requested: \"[image path from tool]\"."
    "\n Reply with \"FIND_IMAGE: your topic\" to search for more images.```"
    "\nFor following topic you must first search and then you must download one image:"
)
image_finder_node = functools.partial(
    agent_node, agent=image_finder_agent, name="ImageFinder", team="Slides team"
)

# Slide Planner agent
slide_planner_agent = create_agent(
    llm,
    [],
    "You are a PowerPoint slide planner. You're responsible for converting the given "
    "article into slides for PowerPoint, send your output in a JSON format. An array of slides with the following keys for each element:"
    "\n- type: 'text' or 'image'"
    "\n- content: '3 to 4 lines of content in markdown format (Use titles and bullet points) if type is text, or image path if type is image'"
    "\n- note: 'What should the presenter say for this slide. Must be related to the article. (4 to 8 sentences)'"
    "\nCreate between 5 to 7 slides (At least 2 image slides). plus introduction and conclusion pages.\n"
    "\nTo achieve this task, follow these steps sequentially:"
    "\n1. Reply with 'FIND_IMAGE: the topic you want to find an image for.' to get an image for a slide."
    "\n - Only make one request at a time. Wait to receive the first image before making the second request."
    "\n - Example: 'FIND_IMAGE: A person holding a coffee cup'"
    "\n2. Repeat the process until you have all the images you need. You MUST at least use 'FIND_IMAGE' for 2 images."
    "\n3. Convert article to JSON format. Ensure each entry has the keys 'type', 'content', and 'note'."
    "\n4. Expand on any points that need further explanation using your own knowledge. Ensure there are 7 to 9 slides in total."
    "\n5. Return ONLY the JSON formatted slides."
    "\nGiven the following article, first find images for the slides, then convert the article into slides:"
)

slide_planner_agent = functools.partial(
    agent_node, agent=slide_planner_agent, name="SlidePlanner", team="Slides team"
)


def planner_finder_edge_condition(state):
    messages = state["messages"]
    last_message = messages[-1]
    # send the message to the image finder agent
    if "FIND_IMAGE:" in last_message.content:
        return "ImageFinder"
    # Otherwise, return the value
    else:
        # Saving draft
        save_draft(last_message.content, "slides")
        return "end"


slides_graph = StateGraph(SlidesTeamState)
slides_graph.add_node("ImageFinder", image_finder_node)
slides_graph.add_node("SlidePlanner", slide_planner_agent)

# Define the control flow
slides_graph.add_edge("ImageFinder", "SlidePlanner")
slides_graph.add_conditional_edges(
    "SlidePlanner",
    planner_finder_edge_condition,
    {"ImageFinder": "ImageFinder", "SlidePlanner": "SlidePlanner", "end": END},
)


slides_graph.set_entry_point("SlidePlanner")
chain = slides_graph.compile()


# The following functions interoperate between the top level graph state
# and the state of the slides sub-graph
# this makes it so that the states of each graph don't get intermixed
def enter_chain(message: str):
    results = {
        "messages": [HumanMessage(content=message)],
    }
    return results


slides_chain = enter_chain | chain
