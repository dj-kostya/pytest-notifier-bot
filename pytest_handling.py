import pandas as pd
import pytest


def parse_results(path_to_report):
    data = pd.read_html(path_to_report)
    data[1].columns = ['Result', 'Test', 'Duration', 'Links']
    data = data[1][["Test", "Result"]]
    comments_column = ['-' for _ in range(data.shape[0])]
    for i in range(data.shape[0]):
        if data['Result'].iloc[i] == 'Failed':
            comments_column[i] = data['Result'].iloc[i + 1]
    data['Comments'] = comments_column
    rows_to_delete = [i for i in range(1, data.shape[0], 2)]
    data.drop(rows_to_delete, axis=0, inplace=True)
    data.reset_index(drop=True, inplace=True)
    data = data[data['Result'] == 'Failed']
    print(data)
    str_res = "🟢 No failures"
    if data.shape[0] != 0:
        str_res = ""
    for i in range(data.shape[0]):
        str_res += f"""🔴 ***Failed!***
    ***Test***: {data["Test"].iloc[i]}
    ***Comments***: {data["Comments"].iloc[i]}  
              
"""
    return str_res


def tests_passed(path):
    pytest.main(["--html", "report.html"])
    data = pd.read_html("report.html")
    data[1].columns = ['Result', 'Test', 'Duration', 'Links']
    data = data[1][["Test", "Result"]]
    comments_column = ['-' for _ in range(data.shape[0])]
    for i in range(data.shape[0]):
        if data['Result'].iloc[i] == 'Failed':
            comments_column[i] = data['Result'].iloc[i + 1]
    data['Comments'] = comments_column
    rows_to_delete = [i for i in range(1, data.shape[0], 2)]
    data.drop(rows_to_delete, axis=0, inplace=True)
    data.reset_index(drop=True, inplace=True)
    data = data[data['Result'] == 'Failed']
    str_res = "🟢 No failures"
    if data.shape[0] != 0:
        str_res = ""
    for i in range(data.shape[0]):
        str_res += f"""🔴 ***Failed!***
        ***Test***: {data["Test"].iloc[i]}
        ***Comments***: {data["Comments"].iloc[i]}  
        
"""
    if str_res[0] == "🔴":
        return 0, str_res
    return 1, str_res


if __name__ == '__main__':
    tests_passed('pytest')
    print("|||||||||||||||||||")
    parse_results('pytest')
