import zipfile
import json


def amount_citizens_in_city_search(city, file):
    amount_citizens = 0
    with zipfile.ZipFile(file) as z_file:
        for path in z_file.namelist():
            info = z_file.getinfo(path)
            if not info.is_dir() and 'json' in path.split("/")[-1]:
                with z_file.open(path) as j_file:
                    j_data = json.load(j_file)
                    try:
                        if j_data["city"] == city:
                            amount_citizens += 1
                    except KeyError:
                        pass
    return amount_citizens


print(amount_citizens_in_city_search('Москва', 'input.zip'))
