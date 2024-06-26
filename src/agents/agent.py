from langchain.agents import (
    AgentExecutor,
    create_openai_functions_agent,
)
from langchain.output_parsers.openai_functions import JsonOutputFunctionsParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage
from langchain_core.tools import BaseTool
from langchain_openai import ChatOpenAI


def create_agent(
    llm: ChatOpenAI,
    tools: list,
    system_prompt: str,
) -> str:
    """Create a function-calling agent and add it to the graph."""
    if len(tools) > 0:
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    system_prompt,
                ),
                MessagesPlaceholder(variable_name="messages"),
                MessagesPlaceholder(variable_name="agent_scratchpad"),
            ]
        )
        agent = create_openai_functions_agent(llm, tools, prompt)
        executor = AgentExecutor(agent=agent, tools=tools, max_iterations=50)
        return executor
    else:
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    system_prompt,
                ),
                MessagesPlaceholder(variable_name="messages"),
            ]
        )
        return prompt | llm


def agent_node(state, agent, name, team):
    result = agent.invoke(state)
    content = result["output"] if "output" in result else result.content
    return {
        "messages": [
            HumanMessage(content=content, name=name, additional_kwargs={"team": team})
        ]
    }


def create_team_supervisor(llm: ChatOpenAI, system_prompt, members) -> str:
    """An LLM-based router."""
    options = ["FINISH"] + members
    function_def = {
        "name": "route",
        "description": "Select the next role.",
        "parameters": {
            "title": "routeSchema",
            "type": "object",
            "properties": {
                "next": {
                    "title": "Next",
                    "anyOf": [
                        {"enum": options},
                    ],
                },
            },
            "required": ["next"],
        },
    }
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="messages"),
            (
                "system",
                "Given the conversation above, who should act next?"
                " Or should we FINISH? Select one of: {options}"
                "\nFollow the normal flow unless otherwise specified by the user. (DO NOT CALL THE SAME TEAM TWICE IN A ROW)"
                "\nResearchers team -> Slides team -> Presenters team"
                "{previous_team}",
            ),
        ]
    ).partial(options=str(options), team_members=", ".join(members))

    def supervisor_node(state):
        last_team = state["messages"][-1].additional_kwargs.get("team", "")
        previous_team = ""
        if last_team:
            previous_team = "\n\nLast team was: " + last_team
        state["previous_team"] = previous_team
        return (
            prompt
            | llm.bind_functions(functions=[function_def], function_call="route")
            | JsonOutputFunctionsParser()
        )

    return supervisor_node
