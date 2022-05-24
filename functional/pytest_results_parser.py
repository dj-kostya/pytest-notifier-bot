import pytest
import pandas as pd
from pytest_jsonreport.plugin import JSONReport
from data.constants import PATH_TO_JSON_REPORT, FAILED_STATUS


def pytest_results(pytest_root_dir):

    plugin = JSONReport()
    pytest.main([f'--json-report-file=none', f'--rootdir={pytest_root_dir}'], plugins=[plugin])
    plugin.save_report(PATH_TO_JSON_REPORT)

    data = pd.read_json(PATH_TO_JSON_REPORT, lines=True, encoding='utf8')
    data = data['tests'][0]
    result = ''
    for test in range(len(data)):

        test_status = data[test]['outcome']

        if test_status == FAILED_STATUS:
            failed_test_path = data[test]['call']['crash']['path']
            failed_test_description = data[test]['call']['longrepr']

            text = f"""🔴Failed!
Test:
\t{failed_test_path}
Comment:
\t{failed_test_description}


"""
            result += text

    if result == '':
        return 1, '🟢 No failures'
    return 0, result


if __name__ == '__main__':
    res = pytest_results('D:\\MyProjects\\WebTesterBot\\pytest')
