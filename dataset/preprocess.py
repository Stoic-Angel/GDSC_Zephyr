import pandas as pd

def clean_text(text):
    text = text.replace('\n', ' ')
    text = text.replace('\r', ' ')
    text = text.replace('\t', ' ')
    return text

df = pd.read_csv('llm_dataset.csv')

# data set have 2 columns input and output
# we have to generate final_datas.py file which have the following format
# final_datas = [
#  "input: What are the pros to be a GDSC member? What if I am not selected?",
# "output: Being a member of GDSC (Google Developer Student Clubs) comes with several pros. First off, you get the chance to explore and dive deep into various domains, expanding your knowledge and skill set. It's an excellent opportunity to network with like-minded individuals, and even collaborate on real-world projects.\nNow, if you're not selected, it's not the end of the world! There are always other avenues to explore and opportunities to seize. You can still engage with the community, attend events, and enhance your skills independently. Don't forget, resilience and adaptability are key in the world of tech!",
# .... ]
# and so on

final_datas = []
for i in range(len(df)):
    final_datas.append(f'"input: {clean_text(df["input"][i])}"')
    final_datas.append(f'"output: {clean_text(df["output"][i])}"')

with open('final_datas.py', 'w') as f:
    f.write(f'final_datas = [{",".join(final_datas)}]')
    f.close()
