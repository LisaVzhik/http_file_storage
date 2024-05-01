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
