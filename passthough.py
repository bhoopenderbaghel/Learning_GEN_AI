from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from langchain_core.runnables import RunnableSequence, RunnableParallel,RunnablePassthrough

load_dotenv()

prompt = PromptTemplate(
    template='Generate a tweet about {topic}',
    input_variables=['topic']
)

prompt1 = PromptTemplate(
    template='Generate a linkedin post about{topic}',
    input_variables=['topic']
)


model = ChatOpenAI(model='gpt-4o-mini')

parser = StrOutputParser()

joke_gen = RunnableSequence(prompt,model,parser)

parallel = RunnableParallel({
    'joke': RunnablePassthrough(),
    'explaination': RunnableSequence(prompt1,model,parser)
})

final_chain = RunnableSequence(joke_gen,parallel)

result = final_chain.invoke({'topic':'football'})

print(result)