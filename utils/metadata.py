from json import load, dump


def load_metadata() -> dict:
    """ Загрузка метаданных из файла, если файла нет, возвращает пустой словарь """
    try:
        with open('file_metadata.json', 'r') as file:
            return load(file)
    except FileNotFoundError:
        return {}


def save_metadata(metadata: dict) -> None:
    """ Сохранение метаданных в файл """
    with open('file_metadata.json', 'w') as file:
        dump(metadata, file, indent=4)


def add_file_metadata(file_hash: str, username: str, file_path: str) -> None:
    """ Добавление метаданных для нового файла """
    metadata = load_metadata()
    metadata[file_hash] = {"owner": username, "path": file_path}
    save_metadata(metadata)


def delete_file_metadata(file_hash: str) -> bool:
    """ Удаление метаданных файла """
    metadata = load_metadata()
    if file_hash in metadata:
        del metadata[file_hash]
        save_metadata(metadata)
        return True
    return False
