import google.generativeai as genai
from settings import Settings
from load_creds import load_creds

creds = load_creds()

genai.configure(credentials=creds)

print('Available base models:', [m.name for m in genai.list_models()])

# Set up the model
generation_config = {
    "temperature": 0,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}

safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
]

zephyr_model = genai.GenerativeModel(model_name="tunedModels/gdsczephyr-xkrx9ry35pja",
                                     generation_config=generation_config,
                                     safety_settings=safety_settings)

# def test():
#     from dataset.final_datas import final_datas
#     while 1:
#         question = input("You: ")
#         prompt_parts = [
#             "You are a virtual AI assistance named Zypher (exclusive to GDSC JSSATEN) whose job is to clear the doubts of students related to GDSC JSSATEN chapter. You should answer strictly to training dataset. If you do not know the answer to query or question, just reply \"Sorry, I didn't get that. You can try contacting GDSC members directly from https://gdscjss.in/team\". You reply should not exceed more than 50 words.",
#         ]
#         prompt_parts.extend(final_datas)
#         prompt_parts.append("input: " + question)
#         prompt_parts.append("output:")
#         response = zephyr_model.generate_content(prompt_parts)
#         print(f"GDSC Zephyr: {response.text}")
