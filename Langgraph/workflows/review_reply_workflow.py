from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from typing import TypedDict, Literal
from dotenv import load_dotenv
from pydantic import BaseModel, Field

load_dotenv()

model = ChatOpenAI(model="gpt-4o-mini")



class SentimentSchema(BaseModel):
    sentiment: Literal["positive", "negative"] = Field(description="Sentiment of the review")


class DiagnosisSchema(BaseModel):
    issue_type: Literal["UX", "Performance", "Bug", "Support", "Other"] = Field(
        description="The category of issue mentioned in the review"
    )
    tone: Literal["angry", "frustrated", "disappointed", "calm"] = Field(
        description="The emotional tone expressed by the user"
    )
    urgency: Literal["low", "medium", "high"] = Field(
        description="How urgent or critical the issue appears to be"
    )


structured_model = model.with_structured_output(SentimentSchema)
structured_model2 = model.with_structured_output(DiagnosisSchema)



class reviewstate(TypedDict):
    review: str
    sentiment: Literal["positive", "negative"]
    diagnosis: dict
    response: str



def find_sentiment(state: reviewstate):
    prompt = f"For the following review find the sentiment:\n{state['review']}"
    sentiment = structured_model.invoke(prompt).sentiment
    return {"sentiment": sentiment}


def check_sentiment(state: reviewstate) -> Literal["positive_response", "run_diagnosis"]:
    if state["sentiment"] == "positive":
        return "positive_response"
    else:
        return "run_diagnosis"


def positive_response(state: reviewstate):
    prompt = f"""Write a warm thank-you message in response to this review:

"{state['review']}"

Also, kindly ask the user to leave feedback on our website.
"""
    response = model.invoke(prompt).content
    return {"response": response}


def run_diagnosis(state: reviewstate):
    prompt = f"""Diagnose this negative review:

{state['review']}

Return issue_type, tone, and urgency.
"""
    response = structured_model2.invoke(prompt)
    return {"diagnosis": response.model_dump()}


def negative_response(state: reviewstate):
    diagnosis = state["diagnosis"]

    prompt = f"""You are a support assistant.

The user had a "{diagnosis['issue_type']}" issue, sounded "{diagnosis['tone']}", and marked urgency as "{diagnosis['urgency']}".

Write an empathetic, helpful resolution message.
"""
    response = model.invoke(prompt).content
    return {"response": response}



graph = StateGraph(reviewstate)

graph.add_node("find_sentiment", find_sentiment)
graph.add_node("positive_response", positive_response)
graph.add_node("run_diagnosis", run_diagnosis)
graph.add_node("negative_response", negative_response)

graph.add_edge(START, "find_sentiment")

graph.add_conditional_edges("find_sentiment", check_sentiment)

graph.add_edge("positive_response", END)
graph.add_edge("run_diagnosis", "negative_response")
graph.add_edge("negative_response", END)

workflow = graph.compile()

# to visualize the graph un comment this
# png_graph = workflow.get_graph().draw_mermaid_png()

# with open("review_workflow.png", "wb") as f:
    # f.write(png_graph)

# print("Graph Saved as review_workflow.png")



if __name__ == "__main__":
    result = workflow.invoke({
        "review": "The app is very slow and crashes frequently"
    })

    print("\nFinal Output:")
    print(result)