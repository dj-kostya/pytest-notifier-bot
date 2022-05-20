import json
import pandas as pd


def parse(path):
    data = pd.read_json(path, lines=True, encoding = "utf8")
    #print(data)
    print(f'Exitcode : {data["exitcode"][0]}')
    print(data['created'])
    print()

    #p#rint(data.head())




if __name__ == '__main__':
    parse(".report.json")