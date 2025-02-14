

#from crypt import methods
from flask import Flask, render_template, request, redirect, url_for, session

from api.Record import Record, RecordModel
import pyrebase
# from WordGenerate import Generate

app = Flask(__name__)
app.secret_key = 'as21wwq33qwqe'  # Необходимо для работы с сессиями

# Статичный пароль
PASSWORD = 'madk9KAT%%23'

firebase_config = {
      "apiKey": "AIzaSyDbxKzF0qEGPpQV1x9PTlfTmTHlrRiuGsg",
    "databaseURL" : "https://debt-schedule-3ca23-default-rtdb.europe-west1.firebasedatabase.app/",
      "authDomain": "debt-schedule-3ca23.firebaseapp.com",
      "projectId": "debt-schedule-3ca23",
      "storageBucket": "debt-schedule-3ca23.firebasestorage.app",
      "messagingSenderId": "129534141119",
      "appId": "1:129534141119:web:879c52caedd9a8e1079c0a",
      "measurementId": "G-3ZZNZ3X5M3"
}
firebase = pyrebase.initialize_app(firebase_config)

db = firebase.database()


# Хранение записей в памяти (в реальном приложении лучше использовать базу данных)
records = []
# Главная страница с таблицей

def refresh():
    global records
    records.clear()
    ordered_dict_students = db.get().val()
    if ordered_dict_students == None:
        return
    for key in ordered_dict_students.keys():
        records.append(RecordModel(key, Student.from_dict(ordered_dict_students[key])))
        
@app.route('/')
def index():
    refresh()
    return render_template('index.html', records=records)

# Форма авторизации
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form.get('password')
        if password == PASSWORD:
            session['logged_in'] = True  # Устанавливаем флаг авторизации
            return redirect(url_for('manage'))
        else:
            return render_template('login.html', error='Неверный пароль')

    return render_template('login.html')

# Страница работы с таблицей
@app.route('/manage', methods=['GET', 'POST'])
def manage():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    # if request.method == 'POST':
    #     doc = Generate(records)
    #     doc_path = 'График задолженностей.docx'
    #     doc.save(doc_path)
    #     return send_file(doc_path, as_attachment=True)
    refresh()
    return render_template('manage.html', records=records)


# Добавление записи
@app.route('/add_record', methods=['GET', 'POST'])
def add_record():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    if request.method == 'POST':
        discipline = request.form.get('discipline')
        teacher = request.form.get('teacher')
        time = request.form.get('time')
        room = request.form.get('room')
        global db
        db.push(Record(discipline, teacher, time, room).to_dict())
        refresh()
        return redirect(url_for('manage'))
    
    return render_template('add_record.html')

# Изменение записи
@app.route('/edit_record/<int:index>', methods=['GET', 'POST'])
def edit_record(index):
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    if request.method == 'POST':
        discipline = request.form.get('discipline')
        teacher = request.form.get('teacher')
        time = request.form.get('time')
        room = request.form.get('room')
        global db
        db.update(StudentModel(records[index].key, Record(discipline, teacher, time, room)).to_dict())
        refresh()
        return redirect(url_for('manage'))

    record = records[index]
    return render_template('edit_record.html', record=record, index=index)

# Удаление записи
@app.route('/delete_record/<int:index>')
def delete_record(index):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    global db
    db.child(records[index].key).remove()
    refresh()
    return redirect(url_for('manage'))

# Выход из системы
@app.route('/logout')
def logout():
    session.pop('logged_in', None)

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

