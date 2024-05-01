from json import load, dump


def load_metadata():
    """ Загрузка метаданных из файла, если файла нет, возвращает пустой словарь """
    try:
        with open('file_metadata.json', 'r') as file:
            return load(file)
    except FileNotFoundError:
        return {}


def save_metadata(metadata):
    """ Сохранение метаданных в файл """
    with open('file_metadata.json', 'w') as file:
        dump(metadata, file, indent=4)


def add_file_metadata(file_hash, username, file_path):
    """ Добавление метаданных для нового файла """
    metadata = load_metadata()
    metadata[file_hash] = {"owner": username, "path": file_path}
    save_metadata(metadata)


def delete_file_metadata(file_hash):
    """ Удаление метаданных файла """
    metadata = load_metadata()
    if file_hash in metadata:
        del metadata[file_hash]
        save_metadata(metadata)
        return True
    return False
