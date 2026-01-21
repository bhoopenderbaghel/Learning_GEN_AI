from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import TextLoader
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()

model = ChatOpenAI(model='gpt-4o-mini')

prompt = PromptTemplate(
    template='write a summary for the following poem - \n {poem}',
    input_variables=['poem']
)

parser = StrOutputParser()

loader = TextLoader("/home/bhoopender/langchain/Rag/document_loader/taj.txt",encoding="utf-8")


docs = loader.load()

chain = prompt | model | parser

result = chain.invoke({'poem':docs[0].page_content})
print(result)

# print(type(docs))
# print(type(docs[0]))
# print(docs[0].page_content)
# print(docs[0].metadata)