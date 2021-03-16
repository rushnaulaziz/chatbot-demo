import os
import pandas
def parse_file(file_path, sheet_name1):
    """
    Input file parser
    """
    import pandas as pd

    df = pd.read_excel (file_path, sheet_name=sheet_name1)
    questions = df['Questions']
    responses = df['Response']
    data = list(zip(questions, responses))
    return data
if __name__ == '__main__':
    file_path = r'./data.xlsx'
    sheet_name = "Sheet2"
    json_path =  "./intents.json"
    if os.path.exists(file_path) and os.path.isfile(file_path):
        fileContent = parse_file(file_path,sheet_name)
        first_q = fileContent[0][1]
        for run in first_q:
            if run.bold:
                print (run.text)