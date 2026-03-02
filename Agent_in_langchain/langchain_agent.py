# from langchain_openai import ChatOpenAI
# from langchain_core.tools import tool
# import requests
# from dotenv import load_dotenv
# from langchain.agents import create_agent
# from langchain_community.tools import DuckDuckGoSearchRun

# load_dotenv()


# search_tool = DuckDuckGoSearchRun()

# # results = search_tool.invoke('top news in world today')

# llm = ChatOpenAI()

# # pull the react prompt from langchain hub

# prompt = hub.pull("hwchase17/react")

# #  create the react agent manually with the pulled prompt

# agent = create_react_agent(
#     llm=llm,
#     tools=[search_tool],
#     prompt=prompt
# )
# # wrap it with agentexcutor

# agent_exceutor = AgentExecutor(
#     agent=agent,
#     tools=[search_tool],
#     verbose=True
# )

# response = agent_exceutor.invoke({"input":"3 ways to reach goa from delhi"})
# print(response)
# # a = response['output']

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain_community.tools import DuckDuckGoSearchRun

load_dotenv()

# LLM
llm = ChatOpenAI()

# Tool
search_tool = DuckDuckGoSearchRun()

tools = [search_tool]

# Create Agent
agent = create_agent(
    model=llm,
    tools=tools,
)

# Invoke directly
response = agent.invoke(
    # {"messages": [{"role": "user", "content": "what happen to the supreme leader of iran, Is he killed "}]}
    {"messages": [{"role": "user", "content": "what is the today's date"}]}
)

# print(response.ToolMessage)
final_message = response["messages"][-1]
print(final_message.content)