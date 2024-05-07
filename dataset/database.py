from llama_index.core import Document
from llama_index.core.schema import MetadataMode
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.core.node_parser import SentenceSplitter
import chromadb

from models.zephyr import get_embed_model

import pandas as pd

def load_doc():
    df = pd.read_csv("final_data.csv")

    with open("final_data.txt", "w") as f:
        for i in range(len(df)):
            f.write(f"# {df.iloc[i, 0]} \n")
            f.write(f"{df.iloc[i,1]} \n")

    doc = []
    for i in range(len(df)):
        document = Document(
        text=f"# {df.iloc[i,0]}\n{df.iloc[i,1]}\n",
        metadata={
            "file_name": "zephyr_kb.txt",
            "title": df.iloc[i, 0]
        },
        excluded_llm_metadata_keys=["file_name"],
        metadata_seperator="::",
        metadata_template="{key}=>{value}",
        text_template="Metadata: {metadata_str}\n-----\nContent: {content}",
        )
        doc.append(document)
    return doc

def get_index(documents, embed_model, db_exists=False):
  db = chromadb.PersistentClient(path="./chroma_db")
  collection = db.get_or_create_collection("quickstart")

  vector_store = ChromaVectorStore(chroma_collection=collection)
  text_splitter = SentenceSplitter(chunk_size=128, chunk_overlap=16)

  if not db_exists:
    ## save vectordb on disk (use only one time)
    index =  VectorStoreIndex.from_documents(documents, transformations=[text_splitter])
    # storage_context = StorageContext.from_defaults(vector_store=vector_store)
    # index = VectorStoreIndex.from_documents(documents, storage_context=storage_context, transformations=[text_splitter])
  else:
    index = VectorStoreIndex.from_vector_store(vector_store, embed_model=embed_model)

  return index


embed_model = get_embed_model()
doc = load_doc()
index = get_index(doc, embed_model, db_exists=False)
