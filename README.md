# http_file_storage
Сервис предоставляет HTTP API для загрузки, скачивания и удаления файлов.

## Установка и запуск
### Установить зависимости:
```commandline
pip install -r requirements.txt
```
### Запуск:
```commandline
python run.py
```

## Использование API
### Загрузка файла
- **Method**: POST
- **URL**: /upload
- **Body**:
  - **the_file**: Файл для загрузки, отправленный в формате multipart/form-data.
- **Success Response**:
  - **Code**: 200
  - **Content**: { "hash": "abc123..." }
  - **Description**: Возвращает хэш загруженного файла.
- **Error Response**:
  - **Code**: 400 (Bad Request)
  - **Content**: No file provided
  - **Description**: Возвращается, если файл не был предоставлен.

#### Пример запросе с curl
не забудь заменить "example.txt" на путь к своему файлу
```bash
curl -X POST -F "the_file=@example.txt" http://localhost:5000/upload
```

### Скачивание файла

- **Method**: GET
- **URL**: /download/<file_hash>
- **URL Params**:
  - **Required**:
    - `file_hash=[string]`: хэш файла, который необходимо загрузить.
- **Success Response**:
  - **Code**: 200
  - **Content**: содержимое файла.
- **Error Response**:
  - **Code**: 404
  - **Content**: {"message": "File not found"}
- **Description**: позволяет любому пользователю загрузить файл, предоставив его хэш (аутентификация не требуется).

#### Пример запроса с curl
не забудь заменить <file_hash> на хэш файла, который ты хочешь загрузить:

```bash
curl -o filename_to_save_as.extension http://localhost:5000/download/<file_hash>
