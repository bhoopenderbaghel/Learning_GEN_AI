from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableBranch,RunnableLambda 
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import Literal
load_dotenv()

model = ChatOpenAI(model='gpt-4o-mini')

parser = StrOutputParser()

class Feedback(BaseModel):
    sentiment: Literal['positive','negative'] = Field(description='Give the Sentiment of the feedback')

parser1 = PydanticOutputParser(pydantic_object=Feedback)

prompt = PromptTemplate(
    template='Classify the sentiment of the following feedback of text into positive or negative  \n {feedback} \n {format_instruction}',
    input_variables=['feedback'],
    partial_variables={'format_instruction':parser1.get_format_instructions()}
)

claaifier_chain = prompt | model | parser1

# # result = claaifier_chain.invoke({'feedback':'This is a terrible smartphone'}).sentiment
# result = claaifier_chain.invoke({'feedback':'This is a best smartphone'}).sentiment
# print(result)
prompt1 = PromptTemplate(
    template='Write an appropriate response to this positive feedback \n {feedback}',
    input_variables=['feedback']
)

prompt2 = PromptTemplate(
    template='Write an appropriate response to this negative feedback \n {feedback}',
    input_variables=['feedback']
)

branch = RunnableBranch(
    (lambda x:x.sentiment == 'positive', prompt1 | model | parser),
    (lambda x:x.sentiment == 'negative', prompt2 | model | parser),
    RunnableLambda(lambda x: 'could not find sentiment')
)


chain = claaifier_chain | branch

print(chain.invoke({'feedback':'This is a wonderful smartphone'}))

chain.get_graph().print_ascii()