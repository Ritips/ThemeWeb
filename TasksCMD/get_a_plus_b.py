import requests


def get_request(address, port, val1, val2):
    params = {'a': val1, 'b': val2}
    create_address = address + ":" + port
    response = requests.get(create_address, params=params)
    if response:
        json_object = response.json()
        res = json_object['result']
        print(res)
        print(json_object['check'])
    else:
        print('Bruh')


if __name__ == '__main__':
    address_server = input()
    port_server = input()
    a = int(input())
    b = int(input())
    get_request(address_server, port_server, a, b)
