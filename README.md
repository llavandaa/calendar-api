# Запуск приложения

```bash
.venv/bin/flask --app ./calendar/server.py run
```

## cURL тестирование

### Добавление нового события

```bash
curl http://127.0.0.1:5000/api/v1/calendar/ -X POST -d "2024-07-03|Meeting|Discuss project updates"
```

### Получение всего списка событий

```bash
curl http://127.0.0.1:5000/api/v1/calendar/
```

### Получение события по идентификатору / ID == abcd

```bash
curl http://127.0.0.1:5000/api/v1/calendar/abcd/
```

### Обновление события по идентификатору / ID == abcd / новый текст == "Discuss project details"

```bash
curl http://127.0.0.1:5000/api/v1/calendar/abcd/ -X PUT -d "title|new text"
```

### Удаление события по идентификатору / ID == abcd

```bash
curl http://127.0.0.1:5000/api/v1/calendar/abcd/ -X DELETE
```

## Пример исполнения команд с выводом

```bash
$ curl http://127.0.0.1:5000/api/v1/calendar/ -X POST -d "2024-07-03|Meeting|Discuss project details"
Новый id: abcd

$ curl http://127.0.0.1:5000/api/v1/calendar/
2024-07-03|Meeting|Discuss project details

$ curl http://127.0.0.1:5000/api/v1/calendar/abcd/
2024-07-03|Meeting|Discuss project details

$ curl http://127.0.0.1:5000/api/v1/calendar/abcd/ -X PUT -d "2024-07-03|Meeting|Discuss project updates"
Обновлено

$ curl http://127.0.0.1:5000/api/v1/calendar/abcd/
2024-07-03|Meeting|Discuss project updates

$ curl http://127.0.0.1:5000/api/v1/calendar/abcd/ -X DELETE
Удалено

$ curl http://127.0.0.1:5000/api/v1/calendar/
-- пусто --
```
