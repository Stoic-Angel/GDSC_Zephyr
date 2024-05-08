from settings import Settings
from llama_index.core import Settings
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding

# Set up the model


def get_embed_model():
  ## set embedding model
  embed_model = OpenAIEmbedding(model="text-embedding-3-large")
  Settings.embed_model = embed_model

  ## set llm model
  Settings.llm = OpenAI("gpt-3.5-turbo-0613", temperature=0.5)

  return embed_model

from llama_index.core import PromptTemplate

zephyr_qa_prompt = (
    "You are a virtual AI assistance named Zephyr (exclusive to GDSC JSSATEN) whose job is to clear the doubts of students related to GDSC JSSATEN club. "
    "You must answer for query/question using only the context provided in less than 50 words"
    "If you are not able to answer query using the context, just reply \"Sorry, I didn't get that. You can try contacting GDSC members directly from https://gdscjss.in/team\" "
    "However, you are allowed to interact with the user for greeting and telling them about yourself. "
    "Context Information:  "
    "{context_str}  "
    "Query:  "
    "{query_str} "
    "Answer: "
)
zephyr_qa_prompt_template = PromptTemplate(zephyr_qa_prompt)