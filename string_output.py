from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
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

prompt1 = templete1.invoke({'topic':'black hole'})

result = model.invoke(prompt1)

prompt2 = templete2.invoke({'text':result.content})

result1 = model.invoke(prompt2)

print(result1.content)
