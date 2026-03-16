from langgraph.graph import StateGraph,START,END
from typing import TypedDict,Literal

class quadstate(TypedDict):

    a: int
    b: int
    c: int

    equation: str
    discriminant: float
    result: str

def show_equation(state:quadstate):

    equation = f'{state["a"]}*2{state["b"]}*{state["c"]}'

    return{'equation':equation}

def calculate_discrimenant(state:quadstate):
    discriminant = state["b"]**2 - (4*state["a"]*state["c"])

    return{'discriminant':discriminant}

def real_roots(state:quadstate):

    root1 = (-state["b"] + state["discriminant"]**0.5)/(2*state["a"])
    root2 = (-state["b"] - state["discriminant"]**0.5)/(2*state["a"])
    
    result = f'The roots are {root1} and {root2}'

    return{'result': result}

def repeated_roots(state:quadstate):

    root = (-state["b"])/(2*state["a"])
    
    result = f'The only repeated root is {root}'

    return{'result': result}


def no_real_roots(state:quadstate):

    
    result = f'No Real roots'

    return{'result': result}

def check_condition(state:quadstate) -> Literal["real_roots","repeated_roots","no_real_roots"]:

    if state["discriminant"] > 0:
        return "real_roots"
    elif state["discriminant"] == 0:
        return 'repeated_roots'
    else:
        return 'no_real_roots'
    
graph = StateGraph(quadstate)

graph.add_node("show_equation",show_equation)
graph.add_node("calculate_discrimenant",calculate_discrimenant)
graph.add_node("real_roots",real_roots)
graph.add_node("repeated_roots",repeated_roots)
graph.add_node("no_real_roots",no_real_roots)

graph.add_edge(START,"show_equation")
graph.add_edge("show_equation","calculate_discrimenant")

graph.add_conditional_edges("calculate_discrimenant",check_condition)
graph.add_edge("real_roots",END)
graph.add_edge("repeated_roots",END)
graph.add_edge("no_real_roots",END)

workflow = graph.compile()

# png_graph = workflow.get_graph().draw_mermaid_png()
#  To visualize the graph un comment these lines
# with open("conditional_workflow.png", "wb") as f:

#     f.write(png_graph)

# print("Graph saved as conditional_workflow.png")

initial = {
    "a":4,
    "b":-2,
    "c":4
}

final = workflow.invoke(initial)

print(final)