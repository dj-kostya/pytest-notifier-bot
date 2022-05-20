import pytest
import pandas as pd


def parse(my_path):

    pytest.main(["--json-report", f"--rootdir={my_path}"])
    data = pd.read_json(".report.json", lines=True, encoding="utf8")
    result = ""
    for test in range(len(data['tests'][0])):
        if data['tests'][0][test]['outcome'] == 'failed':
            text = f"""🔴Failed!
Test: 
\t{data['tests'][0][test]['call']['crash']['path']}
Comment: 
\t{data['tests'][0][test]['call']['longrepr']}

        
"""
            result += text

    if result == "":
        return 1, "🟢 No failures"
    return 0, result


if __name__ == '__main__':
    res = parse("pytest/")
    print("____________________")
    print(res)