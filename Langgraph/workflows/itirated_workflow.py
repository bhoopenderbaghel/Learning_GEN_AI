from langgraph.graph import StateGraph,START,END
from typing import TypedDict,Literal,Annotated
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from langchain_core.messages import SystemMessage,HumanMessage
from dotenv import load_dotenv
import operator

load_dotenv()

generator_llm = ChatOpenAI(model='gpt-4o-mini')
evaluator_llm = ChatOpenAI(model='gpt-4o-mini')
optimizer_llm = ChatOpenAI(model='gpt-4o-mini')

class PostEvaluation(BaseModel):
    evaluation: Literal["approved", "needs_improvement"] = Field(..., description="Final evaluation result.")
    feedback: str = Field(..., description="feedback for the tweet.")

structured_evaluator_llm = evaluator_llm.with_structured_output(PostEvaluation)

class postState(TypedDict):

    topic: str
    post: str
    evaluation: Literal['approved','needs_improvement']
    feedback:str
    iteration: int
    max_iteration: int

    post_history: Annotated[list[str], operator.add]
    feedback_history: Annotated[list[str], operator.add]
    

def generate_post(state: postState):
    # prompt 
    messages = [
        SystemMessage(content="You are a funny and clever linkedin influencer."),
        HumanMessage(content=f"""
            write a short, original, and hilarious post on the topic:"{state['topic']}".

            Rules:
            - Do Not use question-answer format.
            - Max 280 characters.
            - use observation humor , irony, sarcasm or cultural references.
            - Use simple, day to day english
            - This is version {state['iteration'] + 1 }
            """)
    ]
    # send generator_LLM
    response = generator_llm.invoke(messages).content

    # return response
    return{'post': response, 'post_history':[response]}

def evaluate_post(state: postState):
    messages = [
        SystemMessage(content="You are a ruthless, no-laugh-given Twitter critic. You evaluate tweets based on humor, originality, virality, and tweet format."),
    HumanMessage(content=f"""
Evaluate the following tweet:

Tweet: "{state['post']}"

Use the criteria below to evaluate the tweet:

1. Originality – Is this fresh, or have you seen it a hundred times before?  
2. Humor – Did it genuinely make you smile, laugh, or chuckle?  
3. Punchiness – Is it short, sharp, and scroll-stopping?  
4. Virality Potential – Would people retweet or share it?  
5. Format – Is it a well-formed tweet (not a setup-punchline joke, not a Q&A joke, and under 280 characters)?

Auto-reject if:
- It's written in question-answer format (e.g., "Why did..." or "What happens when...")
- It exceeds 280 characters
- It reads like a traditional setup-punchline joke
- Dont end with generic, throwaway, or deflating lines that weaken the humor (e.g., “Masterpieces of the auntie-uncle universe” or vague summaries)

### Respond ONLY in structured format:
- evaluation: "approved" or "needs_improvement"  
- feedback: One paragraph explaining the strengths and weaknesses 
""")
]

    response = structured_evaluator_llm.invoke(messages)

    return {'evaluation':response.evaluation, 'feedback': response.feedback, 'feedback_history':[response.feedback]}

def optimize_post(state: postState):

    messages = [
        SystemMessage(content="You punch up tweets for virality and humor based on given feedback."),
        HumanMessage(content=f"""
Improve the tweet based on this feedback:
"{state['feedback']}"

Topic: "{state['topic']}"
Original post:
{state['post']}

Re-write it as a short, viral-worthy tweet. Avoid Q&A style and stay under 280 characters.
""")
    ]

    response = optimizer_llm.invoke(messages).content
    iteration = state['iteration'] + 1

    return {'post': response, 'iteration': iteration,'post_history':[response]}

def route_evaluate(state: postState):
    if state['evaluation'] == 'approved' or state['iteration'] >= state['max_iteration']:
        return 'approved'
    else:
        return 'need_improvement'

graph = StateGraph(postState)

graph.add_node('generate',generate_post)
graph.add_node('evaluate',evaluate_post)
graph.add_node('optimize',optimize_post)

graph.add_edge(START,'generate')
graph.add_edge('generate','evaluate')

graph.add_conditional_edges('evaluate',route_evaluate,{'approved':END,'need_improvement':'optimize'})

graph.add_edge('optimize','evaluate')

itirated_workflow = graph.compile()

# png_graph = itirated_workflow.get_graph().draw_mermaid_png()

# To visualize the graph un comment these lines
# with open("itirated_workflow.png", "wb") as f:
#     f.write(png_graph)

# print("Graph saved as itirated_workflow.png")

initial = {
    'topic': 'Hitler',
    'iteration':1,
    'max_iteration':5
}

final = itirated_workflow.invoke(initial)

# print(final)

# for post in final['post_history']:
#     print(post)