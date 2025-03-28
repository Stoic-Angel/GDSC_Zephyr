from llama_index.core import Document
from llama_index.core.schema import MetadataMode
from llama_index.core import VectorStoreIndex
from llama_index.core import StorageContext, load_index_from_storage
import os
# from llama_index.core.node_parser import SentenceSplitter

from models.zephyr import get_model

import pandas as pd

def load_doc():
    df = pd.read_csv("final.csv")
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

def get_index():
#   text_splitter = SentenceSplitter(chunk_size=128, chunk_overlap=16)
    save_path = "./vector_db"

    if os.path.exists(save_path):
        storage_context = StorageContext.from_defaults(persist_dir=save_path)
        index = load_index_from_storage(storage_context)
    else:
        doc = load_doc()
        index = VectorStoreIndex.from_documents(doc)
        index.storage_context.persist(persist_dir=save_path)
    return index

llm = get_model()
index = get_index()
