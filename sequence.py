from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from langchain_core.runnables import RunnableSequence

load_dotenv()


model = ChatOpenAI(model='gpt-4o-mini')

parser  = StrOutputParser()

prompt = PromptTemplate(
    template='Write a joke about {topic}',
    input_variables=['topic']
)
prompt1 = PromptTemplate(
    template='explain the following joke - {text}',
    input_variables=['text']
)

chain = RunnableSequence(prompt, model, parser, prompt1, model, parser)

print(chain.invoke({'topic':'AI'}))