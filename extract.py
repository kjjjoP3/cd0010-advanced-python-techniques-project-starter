import csv
import json
from models import NearEarthObject, CloseApproach


def load_neos(neo_csv_path='data/neos.csv'):
    """Đọc thông tin về các vật thể gần Trái Đất từ tệp CSV.

    :param neo_csv_path: Đường dẫn đến tệp CSV chứa dữ liệu về các vật thể gần Trái Đất.
    :return: Một danh sách các đối tượng `NearEarthObject`.
    """
    neos = []
    with open(neo_csv_path, mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            diameter = float(row["diameter"]) if row["diameter"] else float('nan')
            hazardous = row["hazardous"] == 'Y'
            neos.append(NearEarthObject(
                designation=row["designation"],
                name=row["name"],
                diameter=diameter,
                hazardous=hazardous
            ))
    return neos


def load_approaches(cad_json_path='data/cad.json'):
    """Đọc dữ liệu về các lần tiếp cận gần từ tệp JSON.

    :param cad_json_path: Đường dẫn đến tệp JSON chứa dữ liệu về các lần tiếp cận gần.
    :return: Một danh sách các đối tượng `CloseApproach`.
    """
    approaches = []
    with open(cad_json_path, mode='r') as file:
        json_data = json.load(file)
        for entry in json_data["data"]:
            approaches.append(CloseApproach(
                designation=entry[0],
                time=entry[3],
                distance=float(entry[4]),
                velocity=float(entry[7])
            ))
    return approaches
