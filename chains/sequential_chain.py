from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
load_dotenv()

prompt = PromptTemplate(
    template='Generate a detailed report on {topic}',
    input_variables={'topic'}
)


prompt1 = PromptTemplate(
    template='Generate a 5 pointer summary from the following text \n {text}',
    input_variables={'text'}
)

model = ChatOpenAI(model='gpt-4o-mini')

parser = StrOutputParser()

chain = prompt | model | parser | prompt1 | model | parser

result = chain.invoke({'topic':'communal hate in india'})

# print(result)

chain.get_graph().print_ascii()