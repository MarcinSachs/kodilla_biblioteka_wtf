import json


class Books:
    def __init__(self):
        try:
            with open("books.json", "r", encoding="utf-8") as f:
                self.books = json.load(f)
        except FileNotFoundError:
            self.books = []

    def all(self):
        return self.books

    def get(self, id):
        return self.books[id]

    def create(self, data):
        self.books.append(data)

    def save_all(self):
        with open("books.json", "w", encoding="utf-8") as f:
            json.dump(self.books, f)

    def update(self, id, data):
        self.books[id] = data
        self.save_all()


books = Books()
