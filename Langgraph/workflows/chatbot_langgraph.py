from langgraph.graph import StateGraph,START,END
from typing import TypedDict,Annotated
from langchain_core.messages import BaseMessage,HumanMessage
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver

load_dotenv()

class chatstate(TypedDict):
    messages: Annotated[list[BaseMessage],add_messages]

llm = ChatOpenAI()

def chat_node(state:chatstate):
    # take user query from state 
    messages = state['messages']

    # send to llm
    response = llm.invoke(messages)

    #response store state
    return{"messages":[response]}

checkpointer = MemorySaver()
graph = StateGraph(chatstate)
# add nodes
graph.add_node('chat_node',chat_node)
# add edges
graph.add_edge(START,"chat_node")
graph.add_edge("chat_node",END)

chatbot = graph.compile(checkpointer=checkpointer)

# initial_state = {
#     "messages":[HumanMessage(content='What is the capital of india')]
# }

# To fetch only the content of the Ai message
# final = chatbot.invoke(initial_state)["messages"][-1].content

# print(final)

thread_id = '1'

while True:

    user_message = input("Type here: ")

    print('User:',user_message)

    if user_message.strip().lower() in ['exit','quit','bye']:
        break

    config = {'configurable': {'thread_id': thread_id}}
    response = chatbot.invoke({'messages': [HumanMessage(content=user_message)]},config=config)

    print('AI:',response['messages'][-1].content)