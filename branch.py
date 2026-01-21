from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from langchain_core.runnables import RunnableSequence,RunnableLambda,RunnablePassthrough,RunnableParallel,RunnableBranch

load_dotenv()


model = ChatOpenAI(model='gpt-4o-mini')

parser  = StrOutputParser()

prompt = PromptTemplate(
    template='Write a detailed report on {topic}',
    input_variables=['topic']
)

prompt1 = PromptTemplate(
    template='summarize the following text \n {text}',
    input_variables=['text']
)

report = RunnableSequence(prompt,model,parser)

branch_chain = RunnableBranch(
    (lambda x: len(x.split())>300, RunnableSequence(prompt1,model,parser)),
    RunnablePassthrough()
)

final = RunnableSequence(report,branch_chain)

result = final.invoke({'topic':'America vs Venezula'})

print(result)