
def read_csv_with_header(csv_fpath):
    import csv
    with open(csv_fpath) as f:
        csv_data = [{k: v for k, v in row.items()} for row in csv.DictReader(f, skipinitialspace=True)]
    return csv_data