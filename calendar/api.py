from flask import Flask, request
from datetime import datetime
import model
import logic
import storage

app = Flask(__name__)

event_storage = storage.Storage()
_calendar_logic = logic.CalendarLogic(event_storage)

class ApiException(Exception):
    pass

def _from_raw(raw_event: str) -> model.Event:
    parts = raw_event.split('|')
    if len(parts) != 3:
        raise ApiException(f"Некорректные данные события: {raw_event}")
    
    date_str, title, text = parts
    if len(title) > 30:
        raise ApiException(f"Длина заголовка превышает 30 символов: {title}")
    if len(text) > 200:
        raise ApiException(f"Длина текста превышает 200 символов: {text}")
    
    try:
        date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        raise ApiException(f"Некорректный формат даты: {date_str}")
    
    event = model.Event()
    event.date = date
    event.title = title
    event.text = text
    
    return event

def _to_raw(event: model.Event) -> str:
    return f"{event.date}|{event.title}|{event.text}"

API_ROOT = "/api/v1"
CALENDAR_API_ROOT = API_ROOT + "/calendar"

# Создание
@app.route(CALENDAR_API_ROOT + "/", methods=["POST"])
def create():
    try:
        data = request.get_data().decode('utf-8')
        event = _from_raw(data)
        _id = _calendar_logic.create(event)
        return f"Новый id: {_id}", 201
    except Exception as ex:
        return f"Ошибка при создании: {ex}", 400

# Список
@app.route(CALENDAR_API_ROOT + "/", methods=["GET"])
def list():
    try:
        events = _calendar_logic.list()
        raw_events = ""
        for event in events:
            raw_events += _to_raw(event) + '\n'
        return raw_events.strip(), 200
    except Exception as ex:
        return f"Ошибка при получении списка: {ex}", 400

# Чтение
@app.route(CALENDAR_API_ROOT + "/<string:_id>/", methods=["GET"])
def read(_id: str):
    try:
        event = _calendar_logic.read(_id)
        raw_event = _to_raw(event)
        return raw_event, 200
    except Exception as ex:
        return f"Ошибка при чтении: {ex}", 404

# Обновление
@app.route(CALENDAR_API_ROOT + "/<string:_id>/", methods=["PUT"])
def update(_id: str):
    try:
        data = request.get_data().decode('utf-8')
        event = _from_raw(data)
        _calendar_logic.update(_id, event)
        return "Обновлено", 200
    except Exception as ex:
        return f"Ошибка при обновлении: {ex}", 404

# Удаление
@app.route(CALENDAR_API_ROOT + "/<string:_id>/", methods=["DELETE"])
def delete(_id: str):
    try:
        _calendar_logic.delete(_id)
        return "Удалено", 200
    except Exception as ex:
        return f"Ошибка при удалении: {ex}", 404
