"""Write a stream of close approaches to CSV or to JSON.

This module exports two functions: `write_to_csv` and `write_to_json`, each of
which accept an `results` stream of close approaches and a path to which to
write the data.

These functions are invoked by the main module with the output of the `limit`
function and the filename supplied by the user at the command line. The file's
extension determines which of these functions is used.

You'll edit this file in Part 4.
"""
import csv
import json


def write_to_csv(results, filename):
    """Ghi một iterable các đối tượng `CloseApproach` vào tệp CSV.

    Mỗi hàng trong tệp sẽ đại diện cho một lần tiếp cận gần từ `results` 
    và các thông tin liên quan đến NEO đi kèm.

    :param results: Một iterable của các đối tượng `CloseApproach`.
    :param filename: Đường dẫn tệp nơi dữ liệu sẽ được lưu.
    """
    headers = ['datetime_utc', 'distance_au', 'velocity_km_s',
               'designation', 'name', 'diameter_km', 'potentially_hazardous']

    with open(filename, mode='w', newline='') as file:
        csv_writer = csv.DictWriter(file, fieldnames=headers)
        csv_writer.writeheader()
        for approach in results:
            csv_writer.writerow({
                'datetime_utc': approach.time_str,
                'distance_au': approach.distance,
                'velocity_km_s': approach.velocity,
                'designation': approach.neo.designation,
                'name': approach.neo.name,
                'diameter_km': approach.neo.diameter,
                'potentially_hazardous': approach.neo.hazardous,
            })


def write_to_json(results, filename):
    """Ghi một iterable các đối tượng `CloseApproach` vào tệp JSON.

    Mỗi mục trong tệp JSON là một dictionary chứa thông tin về 
    lần tiếp cận gần và NEO liên quan.

    :param results: Một iterable của các đối tượng `CloseApproach`.
    :param filename: Đường dẫn tệp nơi dữ liệu sẽ được lưu.
    """
    approaches_data = []
    for approach in results:
        neo_data = {
            'designation': approach.neo.designation,
            'name': approach.neo.name,
            'diameter_km': approach.neo.diameter,
            'potentially_hazardous': approach.neo.hazardous,
        }
        approach_dict = {
            'datetime_utc': approach.time_str,
            'distance_au': approach.distance,
            'velocity_km_s': approach.velocity,
            'neo': neo_data,
        }
        approaches_data.append(approach_dict)

    with open(filename, mode='w') as file:
        json.dump(approaches_data, file, indent=2)