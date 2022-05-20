import json
import pytest
import pandas as pd


def parse(path):

    pytest.main(["--json-report", "pytest"])
    data = pd.read_json(".report.json", lines=True, encoding = "utf8")
    result = ""
    for test in range(len(data['tests'][0])):
        if data['tests'][0][test]['outcome'] == 'failed':
            text = f"""🔴***Failed!***
***Test:*** 
\t{data['tests'][0][test]['call']['crash']['path']}
***Comment:*** 
\t{data['tests'][0][test]['call']['longrepr']}

        
"""
            result += text

    if result == "":
        return 1, "🟢 No failures"
    return 0, result





if __name__ == '__main__':
    result = parse("pytest/")
    print("____________________")
    print(result)