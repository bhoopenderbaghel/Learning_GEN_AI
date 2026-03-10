from langgraph.graph import StateGraph, START, END
from typing import TypedDict
from IPython.display import Image

class BMIState(TypedDict):
    weight_kg: float
    height_m: float
    bmi: float
    category: str


def calculate_bmi(state: BMIState) -> BMIState:
    weight = state["weight_kg"]
    height = state["height_m"]

    bmi = weight / (height ** 2)
    state["bmi"] = round(bmi, 2)

    return state

def lable_bmi(state: BMIState) -> BMIState:
    bmi = state['bmi']

    if bmi < 18.5:
        state['category'] = "underweight"
    elif 18.5 <= bmi < 25:
        state['category'] = "normal"
    elif 25 <= bmi <30:
        state['category'] = "overweight"
    else:
        state['category'] = "obese"
    return state


bmi_graph = StateGraph(BMIState)

bmi_graph.add_node("calculate_bmi", calculate_bmi)
bmi_graph.add_node('lable_bmi',lable_bmi)


bmi_graph.add_edge(START, "calculate_bmi")
bmi_graph.add_edge("calculate_bmi" , "lable_bmi")
bmi_graph.add_edge("lable_bmi", END)

workflow = bmi_graph.compile()

initial_state = {"weight_kg": 89.50, "height_m": 1.73}

final_state = workflow.invoke(initial_state)

print(final_state)

graph_bytes = workflow.get_graph().draw_mermaid_png()

# with open("bmi_graph.png", "wb") as f:
#     f.write(graph_bytes)

# print("Graph saved as bmi_graph.png")