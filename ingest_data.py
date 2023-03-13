from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import DirectoryLoader
from langchain.embeddings import OpenAIEmbeddings
import pickle
import os
from langchain.vectorstores import Chroma
persist_directory = 'db'

def embed_doc(texts=None, default_mode=0):
    #check data folder is not empty

    if len(os.listdir("data")) > 0:
        # Split text
        text_splitter = RecursiveCharacterTextSplitter(
            # Set a really small chunk size, just to show.
            chunk_size = 4000,
            chunk_overlap  = 200,
            length_function = len,
        )
        print("111")
        embeddings = OpenAIEmbeddings()
        print("222")
        if default_mode:
            loader = DirectoryLoader('data', glob="**/*.*")
            raw_documents = loader.load()
            print(len(raw_documents))
            documents = text_splitter.split_documents(raw_documents)
            vectorstore = Chroma.from_documents(documents, embeddings, persist_directory=persist_directory)
        else:
            print(len(texts))
            documents = text_splitter.split_documents(texts)
            vectorstore = Chroma.add_texts(documents, embeddings, persist_directory=persist_directory)
        
        # Load Data to vectorstore
        vectorstore.persist()
        vectorstore = None
        print("333")