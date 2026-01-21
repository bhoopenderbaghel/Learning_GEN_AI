from langchain_community.document_loaders import CSVLoader

loader = CSVLoader(file_path='/home/bhoopender/langchain/Rag/document_loader/data.csv')

docs = loader.load()

print(len(docs))
print(docs[0])