from settings import Settings
from llama_index.core import Settings
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding

# Set up the model
def get_model():
  ## set embedding model
  embed_model = OpenAIEmbedding(model="text-embedding-3-large")
  Settings.embed_model = embed_model

  ## set llm model
  llm = OpenAI("gpt-3.5-turbo-0125", temperature=0.9)
  Settings.llm = llm

  return llm

# from llama_index.core import PromptTemplate

# zephyr_qa_prompt = (
#     "You are a virtual AI assistance named Zephyr (exclusive to GDSC JSSATEN) whose job is to clear the doubts of students related to GDSC JSSATEN club. "
#     "You may use the context provided for your answer, also keep your answers short."
#     "If you are not able to answer query using the context, just reply \"Sorry, I didn't get that. You can try contacting GDSC members directly from https://gdscjss.in/team\" "
#     "Context Information:  "
#     "{context}  "
#     "Query:  "
#     "{question} "
#     "Answer: "
# )

# zephyr_qa_prompt_template = PromptTemplate(zephyr_qa_prompt)

zephyr_qa_prompt = f"You are a virtual AI assistance named Zephyr (exclusive to GDSC JSSATEN) whose job is to clear the doubts of students related to GDSC JSSATEN club. \
  YOU MUST use the past chat history for answering the provided Queries unless it is not possible to answer the query using the past chat, then use the new provided context with the query. Also YOU MUST KEEP YOUR ANSWER SHORT. Dont give links unless specifically asked for. If you are not able to answer query using the context, just reply 'Sorry, I didn't get that. You can try contacting GDSC members directly from https://gdscjss.in/team'"

def get_prompt(context, question):
  prompt = f"Context: {context} \
    Query: {question}"

  return prompt
