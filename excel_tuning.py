import os
import pandas as pd
from argparse import ArgumentParser
def parse_file(file_path, sheet_name, q_col, r_col):
    """
    Input file parser
    """
    df = pd.read_excel (file_path, sheet_name=sheet_name)
    questions = df[q_col]
    responses = df[r_col]
    data = list(zip(questions, responses))
    return data

def getargs():
    usage_message = """excel_tuning.py [--file] -f file  [--sheet] -s sheetname [--qcol] -q questioncolumn [--rcol] -r responsecolumn"""
    parser = ArgumentParser(conflict_handler='resolve', usage=usage_message)
    parser.add_argument('-f', '--file', action='store', type=str, required=True)
    parser.add_argument('-s', '--sheet', action='store', type=str, required=True)
    parser.add_argument('-q', '--qcol', action='store', type=str, required=True)
    parser.add_argument('-r', '--rcol', action='store', type=str, required=True)
    return parser.parse_args()

if __name__ == '__main__':
    args = getargs()
    file_path = args.file
    sheet_name = args.sheet
    rcol=args.rcol
    qcol=args.qcol
    if os.path.exists(file_path) and os.path.isfile(file_path):
        fileContent = parse_file(file_path,sheet_name, qcol,rcol)
        first_q = fileContent[0][1]
        for run in first_q:
            print (run)