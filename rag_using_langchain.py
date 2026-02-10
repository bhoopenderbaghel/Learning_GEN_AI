from youtube_transcript_api import YouTubeTranscriptApi,TranscriptsDisabled
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings,ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableParallel,RunnablePassthrough,RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

video_id = "GvezxUdLrEk"

try:
    
    transcript_list = YouTubeTranscriptApi().fetch(video_id, languages=['en'])

    transcript = " ".join(chunk.text for chunk in transcript_list)
    # print(transcript)

except TranscriptsDisabled:
    print("No caption available for this video")    


splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100,
    )
chunks = splitter.create_documents([transcript])
# print(chunks[0])
# print(len(chunks))  

embedding = OpenAIEmbeddings(model='text-embedding-3-small')

vector_store = FAISS.from_documents(chunks,embedding)

emb = vector_store.index_to_docstore_id
# print(emb)

retriever = vector_store.as_retriever(search_type="similarity",search_kwargs={"k": 4})
# print(retriever)

# ret = retriever.invoke("what is Transformers")
# print(ret)

llm = ChatOpenAI(model="gpt-4o-mini",temperature=0.2)

prompt = PromptTemplate(
    template="""
    You are a helpful assistant
    Answer ONLY from the provided transcript Context.
    IF the context is insufficient, just say you don't know.

    {context}
    Question: {question}
    """,
    input_variables=['context','question']
)

question = "is the topic of Attention discussed in the video? if yes then what was discussed"

retrived_docs = retriever.invoke(question)

# context_text = "\n\n".join(doc.page_content for doc in retrived_docs)
# print(context_text)

# final_prompt = prompt.invoke({"context": context_text,"question":question})
# print(final_prompt)

# answer = llm.invoke(final_prompt)
# print(answer)

def format_docs(retrieved_docs):
    context_text = "\n\n".join(doc.page_content for doc in retrieved_docs)
    return context_text

parallel = RunnableParallel({
    "question": RunnablePassthrough(),
    "context": retriever | RunnableLambda(format_docs)
})

# parallel.invoke("what is Transformers")
# print(a)

parser = StrOutputParser()

main_chain = parallel | prompt | llm | parser

result = main_chain.invoke("can you summarize the video")
print(result)
