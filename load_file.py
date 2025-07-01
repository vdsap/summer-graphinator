import csv


def load_data_from_file(file_path):
    x_data = []
    y_data = []
    try:
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if len(row) >= 2:
                    try:
                        x = float(row[0])
                        y = float(row[1])
                        x_data.append(x)
                        y_data.append(y)
                    except ValueError:
                        continue
    except Exception as e:
        raise RuntimeError(f"Ошибка чтения файла: {e}")
    return x_data, y_data
