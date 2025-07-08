import json


class Books:
    def __init__(self):
        try:
            with open("books.json", "r", encoding="utf-8") as f:
                self.books = json.load(f)
        except FileNotFoundError:
            self.books = []

        if self.books:
            self.next_id = max(book.get('id', 0) for book in self.books) + 1
        else:
            self.next_id = 1

    def all(self):
        return self.books

    def get(self, id):
        return next((book for book in self.books if book.get('id') == id), None)

    def create(self, data):
        data['id'] = self.next_id
        self.next_id += 1
        self.books.append(data)

    def save_all(self):
        with open("books.json", "w", encoding="utf-8") as f:
            json.dump(self.books, f)

    def update(self, id, data):
        for i, book in enumerate(self.books):
            if book.get('id') == id:
                data['id'] = id 
                self.books[i] = data
                self.save_all()
                return


books = Books()
