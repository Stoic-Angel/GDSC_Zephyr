from settings import Settings
from llama_index.core import Settings
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding

from openai import OpenAI


def get_model():

    embed_model = OpenAIEmbedding(model="text-embedding-3-large")
    Settings.embed_model = embed_model

    llm = OpenAI()
    # llm = OpenAI("gpt-3.5-turbo-0125", temperature=0.9)
    Settings.llm = llm

    return llm


tools = [
    {
        "type":"function",
        "function": {
            "name": "get_info_from_docs",
            "description": "Get information about GDG OnCampus JSSATEN and it's members and the events in conducts. Whenever asked about people using their names, use this tool. Whenever asked about GDG OnCampus events, use this tool. DONT use the tool when the question is not related to GDG OnCampus or it is a general question.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                       "type" : "string",
                        "description" : "The question you want to query the documents with, e.g. 'Who is Abhay?'",
                    },                    
                },
            },
            "required": ["query"],
        },
    },
]


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
  YOU CAN answer questions that are not about GDG OnCampus or its members with your general knowledge. YOU MUST KEEP YOUR ANSWER SHORT. Dont give links unless specifically asked for. If you are not able to answer query using the context, just reply 'Sorry, I didn't get that. You can try contacting GDSC members directly from https://gdscjss.in/team'"

def get_prompt(context, question):
  prompt = f"Context: {context} \
    Query: {question}"

  return prompt
