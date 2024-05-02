# http_file_storage
Сервис предоставляет HTTP API для загрузки, скачивания и удаления файлов.

## Настройка проекта и запуск 
### Настроить переменные окружения:
1. Создать файл `.env`
2. Добавить все необходимые значения в `.env`
#### Пример файла `.env`:
```text
FILE_STORAGE_PATH="/path/to/store"
USERNAME="username"
PASSWORD="password"
```
   
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
  - **Code**: 401 (Unauthorized)
  - **Content**: Unauthorized Access
  - **Description**: Возвращается, если файл пытается загрузить неавторизованный пользователь.

#### Пример запроса с curl
не забудь заменить "example.txt" на путь к своему файлу, а также логин и пароль:
```bash
curl -X POST -u username:password -F "the_file=@example.txt" http://localhost:5000/upload
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
```

### Удаление файла

- **Method**: DELETE
- **URL**: /delete/<file_hash>
- **URL Params**:
  - **Required**:
    - `file_hash=[string]`: хэш файла, который необходимо удалить.
- **Success Response**:
  - **Code**: 200
  - **Content**: {"message": "File deleted successfully"}
- **Error Response**:
  - **Code**: 404
  - **Content**: {"message": "File not found or access denied"}
- **Description**: Позволяет авторизованному пользователю удалить файл, предоставив его хэш. Пользователь должен быть владельцем файла, чтобы выполнить удаление.
#### Пример запроса с curl
Замените <file_hash> на хэш файла, который вы хотите удалить, и убедитесь, что вы предоставили корректные учетные данные для аутентификации.
```bash
curl -X DELETE -u username:password http://localhost:5000/delete/<file_hash>
```

## Тестирование
Тесты написаны с использованием библиотеки `pytest` и проверяют работу всех эндпоинтов.
#### Запуск тестов
```bash
pytest
```
