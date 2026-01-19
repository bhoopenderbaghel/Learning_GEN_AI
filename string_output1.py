from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser 
load_dotenv()


model = ChatOpenAI(model='gpt-4o-mini')

# 1st prompt -> detailed report 
templete1 = PromptTemplate(
    template="write a detailed report on {topic}",
    input_variables=['topic']
)

# 2nd prompt -> summary
templete2 = PromptTemplate(
    template="write a 5 line summary on the following text./n {text}",
    input_variables=['text']
)

parser = StrOutputParser()

chain = templete1 | model | parser | templete2 | model | parser

result = chain.invoke({'topic':'black hole'})

print(result)