from langgraph.graph import StateGraph,START,END
from typing import TypedDict

class batsmanState(TypedDict):
    runs: int
    balls:int
    fours: int
    sixes:int

    sr:float
    bpb: float
    boundary_percentage: float
    summary: str

def calculate_sr(state: batsmanState):
    sr = (state["runs"] / state["balls"]) * 100

    # state["sr"] = sr

    return {'sr': sr}

def calculate_bpb(state: batsmanState):
    bpb = state["balls"] / (state["fours"] + state["sixes"])
    # state["bpd"] = bpb

    return {'bpb': bpb}

def calculate_boundary_percentage(state: batsmanState):
    boundary_percentage = (((state["fours"]*4) + (state["sixes"]*6)) / state["runs"]) * 100

    # state["boundary_percentage"] = boundary_percentage

    return {'boundary_percentage': boundary_percentage}

def summary (state: batsmanState):

    summary = f"""
    Strike Rate - {state['sr']}\n
    Balls per Boundary - {state['bpb']}\n
    Boundary Percentage - {state['boundary_percentage']} 
    """
    # state["summary"] = summary

    return {'summary': summary}


graph = StateGraph(batsmanState)

# ADDING Graph Nodes
graph.add_node("calculate_sr",calculate_sr)
graph.add_node("calculate_bpb",calculate_bpb)
graph.add_node("calculate_boundary_percentage",calculate_boundary_percentage)
graph.add_node("summary",summary)

# ADDING Graph Edges 

graph.add_edge(START,'calculate_sr')
graph.add_edge(START,'calculate_bpb')
graph.add_edge(START,'calculate_boundary_percentage')

graph.add_edge('calculate_sr','summary')
graph.add_edge('calculate_bpb','summary')
graph.add_edge("calculate_boundary_percentage","summary")

simple_parallel_workflow = graph.compile()

png_graph = simple_parallel_workflow.get_graph().draw_mermaid_png()

# To visualize the graph un comment these lines
# with open("simple_parallel_workflow.png", "wb") as f:
#     f.write(png_graph)

# print("Graph saved as simple_parallel_workflow.png")


initial = {
    'runs': 89,
    'balls': 46,
    'fours': 5,
    'sixes': 8
}

final = simple_parallel_workflow.invoke(initial)

print(final)