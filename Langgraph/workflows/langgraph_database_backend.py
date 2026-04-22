from langgraph.graph import StateGraph,START,END
from typing import TypedDict,Annotated
from langchain_core.messages import BaseMessage,HumanMessage
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langgraph.graph.message import add_messages
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3
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

conn = sqlite3.connect(database="chatbot.db",check_same_thread=False)

checkpointer = SqliteSaver(conn=conn)
graph = StateGraph(chatstate)
# add nodes
graph.add_node('chat_node',chat_node)
# add edges
graph.add_edge(START,"chat_node")
graph.add_edge("chat_node",END)

chatbot = graph.compile(checkpointer=checkpointer)

def retrieve_all_thread():
    all = set()
    for checkpoint in checkpointer.list(None):
        all.add(checkpoint.config["configurable"]['thread_id'])

    return(list(all))