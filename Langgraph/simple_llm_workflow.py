from langgraph.graph import StateGraph,START,END
from langchain_openai import ChatOpenAI
from typing import TypedDict
from dotenv import load_dotenv
from IPython.display import Image
load_dotenv()

model = ChatOpenAI()

# Create the State
class llmState(TypedDict):
    question: str
    answer: str

def llm_q(state: llmState) -> llmState:
    # extract the question from the state
    question = state['question']

    #form the prompt
    prompt = f'Answer the following question {question}'

    #Answer the question to the LLM
    answer = model.invoke(prompt).content

    # Update the answer in the state
    state['answer'] = answer
    return state


#Create the graph
graph = StateGraph(llmState)

# add nodes
graph.add_node("llm_q",llm_q)

#add edges
graph.add_edge(START,"llm_q")
graph.add_edge("llm_q",END)

#Compile
workflow = graph.compile()

#execute
initial_state = {"question":"How far is the venus from the earth?"}

final_state = workflow.invoke(initial_state)

# print(final_state['answer'])

graph_bytes = workflow.get_graph().draw_mermaid_png()
with open("bmi_graph2.png", "wb") as f:
    f.write(graph_bytes)

print("Graph saved as bmi_graph2.png")