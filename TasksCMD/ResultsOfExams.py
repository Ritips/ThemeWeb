import json


def get_result():
    with open('input.txt', 'r', encoding='utf-8') as file_input:
        dict_check = {}
        for i, el in enumerate(map(str.strip, file_input.readlines())):
            dict_check[i + 1] = el

    with open('scoring.json', 'r') as file:
        data = json.load(file)
        dict_values = {}
        for key, value in data.items():
            for dictionary in value:
                points = dictionary['points']
                required_tests = dictionary['required_tests']
                for task in required_tests:
                    dict_values[task] = points / len(required_tests)

    points = 0
    for key in dict_values:
        if dict_check[key] == 'ok':
            points += dict_values[key]

    return int(points)


print(get_result())
