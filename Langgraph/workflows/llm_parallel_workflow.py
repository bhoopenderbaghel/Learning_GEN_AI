from langgraph.graph import StateGraph,START,END
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from typing import TypedDict,Annotated
from pydantic import BaseModel,Field
import operator

load_dotenv()

model = ChatOpenAI(model='gpt-4o-mini')

class evaluationschema(BaseModel):

    feedback: str =Field(description= 'Detailed feedback for the essay')
    score: int = Field(description='Score out of 10', ge=0 , le=10)

structure_model = model.with_structured_output(evaluationschema)

essay = """
The relationship between the United States, Israel, and Iran has been one of the most complex and volatile dynamics in modern international politics. Over the past several decades, ideological differences, regional power struggles, nuclear concerns, and security alliances have intensified tensions among these countries. Discussions about the possibility of a conflict involving America and Israel on one side and Iran on the other often reflect deeper geopolitical rivalries and competing visions for the future of the Middle East.

The United States and Israel share a strong strategic alliance built on political cooperation, military collaboration, and shared security interests. The U.S. has long been Israel’s most significant ally, providing diplomatic support, defense funding, and advanced military technology. Israel, in turn, is considered by the United States to be a key partner in maintaining stability and countering hostile actors in the Middle East. Both countries view Iran as a major security challenge, particularly because of Iran’s nuclear program and its support for various armed groups across the region.

Iran, however, sees itself as resisting Western influence and defending its regional interests. Since the 1979 Iranian Revolution, relations between Iran and the United States have been extremely hostile. Iran’s leadership has frequently criticized U.S. foreign policy in the Middle East, accusing Washington of interference and of supporting governments that Iran considers oppressive or illegitimate. Israel is also viewed by Iran as a strategic rival, especially due to longstanding political disagreements and conflicting regional alliances.

One of the central issues driving tensions is Iran’s nuclear program. Western governments, including the United States and Israel, have expressed concern that Iran could develop nuclear weapons capability. Iran has consistently stated that its nuclear program is intended for peaceful purposes, such as energy production and scientific research. However, the lack of trust between the parties has led to sanctions, diplomatic standoffs, and periodic threats of military action.

If a war were to occur involving the United States, Israel, and Iran, the consequences would likely extend far beyond the immediate region. The Middle East is strategically important for global energy supply, international trade routes, and geopolitical stability. A major conflict could disrupt oil markets, trigger economic instability, and potentially draw in other regional or global powers. Countries allied with Iran or opposed to U.S. influence might become involved, increasing the risk of a broader regional war.

Additionally, such a conflict would likely involve modern forms of warfare beyond traditional military operations. Cyber warfare, missile systems, drone technology, and proxy groups could all play major roles. In recent years, conflicts in the region have increasingly relied on indirect confrontation through allied militias and regional partners rather than direct state-to-state battles.

Despite these tensions, diplomacy and international negotiations remain important tools for preventing escalation. Agreements such as nuclear negotiations, regional dialogue, and international mediation efforts demonstrate that peaceful solutions are still possible. Global institutions and diplomatic channels often work to reduce tensions and prevent misunderstandings that could lead to conflict.

Ultimately, the relationship between the United States, Israel, and Iran reflects a broader struggle over influence, security, and ideology in the Middle East. While the possibility of war is frequently discussed in political analysis, many experts emphasize that diplomacy, negotiation, and international cooperation are essential for maintaining stability and preventing large-scale conflict.

Understanding these dynamics requires examining historical grievances, strategic interests, and the perspectives of all parties involved. Only through dialogue and careful diplomacy can the international community hope to reduce tensions and move toward a more stable and peaceful global order.
"""

# prompt = f'Evaluate the language quality of the following essay and provide a feedback and assign a score out of 10 \n {essay}'
# a = structure_model.invoke(prompt)
# print(a)

class upseState(TypedDict):
    essay: str
    language_feedback: str
    analysis_feedback: str
    clarity_feedback: str
    overall_feedback: str
    individual_scores: Annotated[list[int],operator.add]
    avg_score: float

def evaluate_language(state: upseState):
    prompt = f'Evaluate the language quality of the following essay and provide a feedback and assign a score out of 10 \n {essay}'
    output = structure_model.invoke(prompt)

    return{'language_feedback': output.feedback,'individual_scores':[output.score]}

def evaluate_analysis(state: upseState):
    prompt = f'Evaluate the depth of analysis of the following essay and provide a feedback and assign a score out of 10 \n {essay}'
    output = structure_model.invoke(prompt)

    return{'analysis_feedback': output.feedback,'individual_scores':[output.score]}

def evaluate_thought(state: upseState):
    prompt = f'Evaluate the clarity of thought of the following essay and provide a feedback and assign a score out of 10 \n {essay}'
    output = structure_model.invoke(prompt)

    return{'clarity_feedback': output.feedback,'individual_scores':[output.score]}

def final_evaluation(state: upseState):
    # summary feedback
    prompt = f'Based on the following feedbacks create a summarized feedback \n language feedback - {state["language_feedback"]} \n depth of analysis feedback -{state["analysis_feedback"]} \n calrity of feedback -{state["clarity_feedback"]}'
    overall_feedback = model.invoke(prompt).content
    # avg score
    avg_score = sum(state['individual_scores'])/len(state['individual_scores'])
    return {'overall_feedback': overall_feedback, 'avg_score':avg_score}

graph = StateGraph(upseState)

graph.add_node('evaluate_language',evaluate_language)
graph.add_node('evaluate_analysis',evaluate_analysis)
graph.add_node('evaluate_thought',evaluate_thought)
graph.add_node('final_evaluation',final_evaluation)

graph.add_edge(START, 'evaluate_language')
graph.add_edge(START, 'evaluate_analysis')
graph.add_edge(START, 'evaluate_thought')

graph.add_edge('evaluate_language','final_evaluation')
graph.add_edge('evaluate_analysis','final_evaluation')
graph.add_edge('evaluate_thought','final_evaluation')

graph.add_edge('final_evaluation',END)

workflow = graph.compile()

png_graph = workflow.get_graph().draw_mermaid_png()

# To visualize the graph un comment these lines
# with open("llm_parallel_workflow.png", "wb") as f:
#     f.write(png_graph)

# print("Graph saved as llm_parallel_workflow.png")

initial = {
    'essay': essay
}

a = workflow.invoke(initial)

print(a)