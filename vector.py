from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
import os
import pandas as pd


df = pd.read_csv("realistic_restaurant_reviews.csv")

embeddings = OllamaEmbeddings(model="mxbai-embed-large") #define the embedding model from Ollama

db_locations = "./chrome_langchain_db" #check if the vector database already exists, if not create it and add documents to it
add_documents = not os.path.exists(db_locations)

if add_documents:
    documents =[]
    ids=[]

    for i, row in df.iterrows():
        document = Document(
            page_content=row["Title"] + " " + row["Review"],
            metadata={"rating": row["Rating"], "date": row["Date"]},
            id=str(i)
        )
        ids.append(str(i))
        documents.append(document)

vector_store = Chroma(
    collection_name="restaurant_reviews", 
    embedding_function=embeddings, 
    persist_directory=db_locations
) 

if add_documents:
    vector_store.add_documents(documents=documents, ids=ids)

retriever = vector_store.as_retriever(
    search_kwargs={"k": 5} # number of relevant documents to retrieve
)

