import pandas as pd

qa_dataset = pd.read_csv('llm_dataset.csv')
members_dataset = pd.read_csv('final_members.csv')

# combining both datasets
final_df = qa_dataset.copy()
for i in range(len(members_dataset)):
    final_df.loc[-1] = [members_dataset.iloc[i, 0], members_dataset.iloc[i, 1]]
    final_df.index = final_df.index + 1
    final_df = final_df.sort_index()


final_df.to_csv('final.csv', index=False)
final_df.to_excel('final.xlsx', index=False)
