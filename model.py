from config import TESTS_PATH


def get_test_result(path):
    f = open(path, "r", encoding='utf8')
    a = f.readline()
    return int(a)


if __name__ == '__main__':
    get_test_result(TESTS_PATH)

