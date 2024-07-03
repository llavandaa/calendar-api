from flask import Flask
from flask import request

app = Flask(__name__)


import model
import logic

_calendar_logic = logic.CalendarLogic()


class ApiException(Exception):
    pass


def _from_raw(raw_note: str) -> model.Calendar:
    parts = raw_note.split('|')
    if len(parts) == 2:
        calendar = model.Calendar()
        note.id = None
        note.title = parts[0]
        note.text = parts[1]
        return note
    elif len(parts) == 3:
        note = model.Note()
        note.id = parts[0]
        note.title = parts[1]
        note.text = parts[2]
        return note
    else:
        raise ApiException(f"invalid RAW note data {raw_note}")


def _to_raw(note: model.Note) -> str:
    if note.id is None:
        return f"{note.title}|{note.text}"
    else:
        return f"{note.id}|{note.title}|{note.text}"


API_ROOT = "/api/v1"
CALENDAR_API_ROOT = API_ROOT + "/calendar"


# Добавление
@app.route(CALENDAR_API_ROOT + "/", methods=["POST"])
def create():
    try:
        data = request.get_data().decode('utf-8')
        note = _from_raw(data)
        _id = _calendar_logic.create(note)
        return f"new id: {_id}", 201
    except Exception as ex:
        return f"failed to CREATE with: {ex}", 404


# Список
@app.route(CALENDAR_API_ROOT + "/", methods=["GET"])
def list():
    try:
        events = _calendar_logic.list()
        raw_notes = ""
        for note in notes:
            raw_notes += _to_raw(note) + '\n'
        return raw_notes, 200
    except Exception as ex:
        return f"failed to LIST with: {ex}", 404


# Чтение
@app.route(CALENDAR_API_ROOT + "/<_id>/", methods=["GET"])
def read(_id: str):
    try:
        note = _calendar_logic.read(_id)
        raw_note = _to_raw(note)
        return raw_note, 200
    except Exception as ex:
        return f"failed to READ with: {ex}", 404


# Обновление
@app.route(CALENDAR_API_ROOT + "/<_id>/", methods=["PUT"])
def update(_id: str):
    try:
        data = request.get_data().decode('utf-8')
        note = _from_raw(data)
        _calendar_logic.update(_id, note)
        return "updated", 200
    except Exception as ex:
        return f"failed to UPDATE with: {ex}", 404


# Удаление
@app.route(CALENDAR_API_ROOT + "/<_id>/", methods=["DELETE"])
def delete(_id: str):
    try:
        _calendar_logic.delete(_id)
        return "deleted", 200
    except Exception as ex:
        return f"failed to DELETE with: {ex}", 404
