import kaggle
import pandas as pd
from zipfile import ZipFile
import os

topic = "credit card fraud detection"
datasets_list = kaggle.api.dataset_list(search=topic)

if not datasets_list:
    print("По вашему запросу не найдено ни одного датасета.")
else:
    print(f"Найдено датасетов: {len(datasets_list)}")

    # Берём первый датасет
    selected_dataset = datasets_list[0]
    dataset_name = selected_dataset.ref
    print(f"Выбран датасет: {dataset_name}")

    zip_file_name = f"{dataset_name.replace('/', '_')}.zip"

    # Скачивание архива
    if not os.path.exists(zip_file_name):
        kaggle.api.dataset_download_files(dataset_name, quiet=False, unzip=False)
        if os.path.exists(f"{dataset_name.split('/')[1]}.zip"):
            os.rename(f"{dataset_name.split('/')[1]}.zip", zip_file_name)
        print("Загрузка завершена!")
    else:
        print("Архив с датасетом уже существует.")

    # Распаковка архива
    with ZipFile(zip_file_name, 'r') as zip_ref:
        file_list = zip_ref.namelist()
        print(f"Файлы в архиве: {file_list}")
        zip_ref.extractall("downloaded_data")

    # Поиск CSV
    csv_files = [f for f in file_list if f.endswith('.csv')]

    if csv_files:
        first_csv = csv_files[0]
        df = pd.read_csv(f"downloaded_data/{first_csv}")

        print(f"\nЗагружен файл: {first_csv}")
        print(f"Размерность данных: {df.shape}")
        print("Первые строки:")
        print(df.head())

        # Для датасета creditcard.csv целевой признак = "Class"
        if "Class" in df.columns:
            target = "Class"
        else:
            raise ValueError("Не найден целевой признак Class")

        X = df.drop(columns=[target])
        y = df[target]

        print(f"\nЦелевая переменная: {target}")
        print(f"Уникальные значения метки: {y.unique()}")
        print(f"Признаков всего: {X.shape[1]}")

        # Сохраняем инфо в файл
        with open("dataset_info.txt", "w", encoding="utf-8") as f:
            f.write(f"Датасет: {dataset_name}\n")
            f.write(f"Файл: {first_csv}\n")
            f.write(f"Размерность: {df.shape}\n")
            f.write(f"Целевая переменная: {target}\n")
            f.write(f"Количество признаков: {X.shape[1]}\n")
            f.write(f"Признаки: {list(X.columns)}\n")

        print("\nИнформация о данных сохранена в 'dataset_info.txt'")
    else:
        print("В архиве не найдено CSV-файлов.")


