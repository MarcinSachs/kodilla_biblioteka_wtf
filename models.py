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

    def get_unique_genres(self):
        genres_set = {book.get('genre')
                      for book in self.books if book.get('genre')}
        return sorted([(genre, genre) for genre in genres_set])

    def create(self, data):
        data['id'] = self.next_id
        self.next_id += 1
        self.books.append(data)
        self.save_all()

    def save_all(self):
        with open("books.json", "w", encoding="utf-8") as f:
            json.dump(self.books, f)

    def update(self, id, data):
        book = self.get(id)
        if book:
            book.update(data)
            self.save_all()
            return True
        return False

    def delete(self, id):
        book = self.get(id)
        if book:
            self.books.remove(book)
            self.save_all()
            return True
        return False


books = Books()
