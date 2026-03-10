from langgraph.graph import StateGraph,START,END
from langchain_openai import ChatOpenAI
from typing import TypedDict
from dotenv import load_dotenv
from IPython.display import Image
load_dotenv()

model = ChatOpenAI()

class blogState(TypedDict):
    title: str
    outline: str
    content: str

def create_outline(state: blogState) -> blogState:
    #fetch title
    title = state["title"]

    #call llm generate outline 
    prompt = f"Generate a detailed outline for a blog on the topic - {title}"
    outline = model.invoke(prompt).content

    #update state
    state["outline"] = outline

    return state

def create_blog(state: blogState) -> blogState:
    title = state["title"]
    outline = state["outline"]

    prompt = f"Write a detailed blog on the title -{title} using the following outline \n {outline}"

    content = model.invoke(prompt).content

    state["content"] = content

    return state


graph = StateGraph(blogState)

# nodes
graph.add_node("create_outline",create_outline)
graph.add_node("create_blog",create_blog)

#edges
graph.add_edge(START,"create_outline")
graph.add_edge("create_outline","create_blog")
graph.add_edge("create_blog",END)

workflow = graph.compile()

initial = {"title":"Rise of  Hate Speech in India "}

final = workflow.invoke(initial)

# print(final['outline'])


graph_bytes = workflow.get_graph().draw_mermaid_png()
with open("bmi_graph3.png", "wb") as f:
    f.write(graph_bytes)

print("Graph saved as bmi_graph3.png")