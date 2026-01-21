from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from langchain_core.runnables import RunnableSequence, RunnableParallel

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

parallel_chain = RunnableParallel({
    'tweet' :RunnableSequence(prompt,model,parser),
    'linkedin' : RunnableSequence(prompt1,model,parser)
})

result = parallel_chain.invoke({'topic':'AI'})

print(result['tweet'])
print(result['linkedin'])