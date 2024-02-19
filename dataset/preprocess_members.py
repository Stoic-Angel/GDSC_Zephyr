import pandas as pd


def clean_text(text):
    if type(text) != str:
        return text
    text = text.replace('\n', ' ')
    text = text.replace('\r', ' ')
    text = text.replace('\t', ' ')
    text = text.replace('’', "'")
    return text


df = pd.read_csv('members_dataset.csv')

# given dataset have 9 columns
#   0          1     2      3      4      5         6           7         8
# timestamp, email, name, year, branch, domain, introduction, linkedin, github

# we have to generate final_members.py file which have the following format
# final_members = [
#  "input: Who is Abhishek?",
# "output: <processed output after combining with other columns>",
# .... ]

final_members = []
for i in range(len(df)):
    try:
        input = f'"""input: Who is {clean_text(df.iloc[i,2])}?"""'
        output = f'"""output: {clean_text(df.iloc[i,2])} is a {clean_text(df.iloc[i,3])} year student of {clean_text(df.iloc[i,4])} branch and is interested in {clean_text(df.iloc[i,5])}. {clean_text(df.iloc[i,6])}. LinkedIn: {clean_text(df.iloc[i,7])}  GitHub: {clean_text(df.iloc[i,8])}"""'
    except Exception as e:
        print(str(e))
        print(f"Error processing {i+1} member")
        continue
    final_members.append(input)
    final_members.append(output)
    print(f'Processed {i+1} members')

with open('final_members.py', 'w') as f:
    f.write(f'final_members = [{",".join(final_members)}]')
    f.close()
