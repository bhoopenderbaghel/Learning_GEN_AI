from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from langchain_core.runnables import RunnableSequence,RunnableLambda,RunnablePassthrough,RunnableParallel

load_dotenv()


model = ChatOpenAI(model='gpt-4o-mini')

parser  = StrOutputParser()

prompt = PromptTemplate(
    template='Generate a joke on {topic}',
    input_variables=['topic']
)

joke_gen = RunnableSequence(prompt,model,parser)

parallel_chain = RunnableParallel({
    'joke': RunnablePassthrough(),
    "word_count" : RunnableLambda(lambda x: len(x.split()))
})


final = RunnableSequence(joke_gen,parallel_chain)

result = final.invoke({'topic':'robot'})

print(result)