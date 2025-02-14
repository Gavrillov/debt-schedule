class Record:


    def __init__(self, discipline, teacher, time, room):
        self.discipline = discipline
        self.teacher = teacher
        self.time = time
        self.room = room

    def __str__(self):
        return f"{self.discipline};{self.teacher};{self.time};{self.room}"

    def to_dict(self):
        return {
            'discipline': self.discipline,
            'teacher': self.teacher,  # Преобразуем дату в строку
            'time': self.time,      # Преобразуем дату в строку
            'room': self.room
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Student':
        return cls(
            discipline=data['discipline'],
            teacher=data['teacher'],
            time=data['time'],
            room=data['room']
        )


class RecordModel:

    def __init__(self, key : str, record : Record):
        self.key = key
        self.record = record

    def to_dict(self):
        return {
            f'{self.key}' : self.record.to_dict()
        }

    def __str__(self):
        return str(self.record)
