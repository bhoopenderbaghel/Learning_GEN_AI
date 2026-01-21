from langchain_community.document_loaders import DirectoryLoader,PyPDFLoader

loader = DirectoryLoader(
    path='/home/bhoopender/langchain/Rag/document_loader/books',
    glob="*.pdf",
    loader_cls=PyPDFLoader
)

docs = loader.lazy_load()
# docs = loader.load()
# print(docs[121].page_content)
# print(docs[121].metadata)

for document in docs:
    print(document.metadata)