class User(object):
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.books = {}

    def __hash__(self):
        return hash((self.name, self.email))

    def __eq__(self, other):
        return self.name == other.name and self.email == other.email

    def __repr__(self):
        return "Name: {name}, Email: {email}, Books read: {books}".format(name=self.name, email=self.email, books=len(self.books))

    def get_email(self):
        return self.email

    def change_email(self, address):
        self.email = address
        return "New email is {email}".format(email=self.email)

    def read_book(self, book, rating=None):
        if rating != None:
            self.books[book] = rating

    def get_average_rating(self):
        total_rating = 0
        if len(self.books) > 0:
            for rating in self.books.values():
                total_rating += rating
        if len(self.books) > 0:
            return total_rating/len(self.books)
        else:
            print("There is no books with ratings for this user.")

    def get_number_of_books(self):
        return len(self.books)

    def get_books(self):
        return self.books

class Book():
    def __init__(self, title, isbn, price):
        self.title = title
        self.isbn = isbn
        self.price = price
        self.ratings = []

    def __hash__(self):
        return hash((self.title, self.isbn, self.price))

    def __eq__(self, other):
        return self.title == other.title and self.isbn == other.isbn and self.price == other.price

    def __repr__(self):
        return "Title: {title}, isbn: {isbn}, ratings: {ratings}, price: {price}".format(title=self.title, isbn=self.isbn, ratings=self.ratings, price=self.price)

    def get_title(self):
        return self.title

    def get_isbn(self):
        return self.isbn

    def get_price(self):
        return self.price

    def set_isbn(self, new_isbn):
        self.isbn = new_isbn
        return "The new ISBN is {isbn}".format(isbn = self.isbn)

    def add_rating(self, rating):
        self.rating = rating
        if self.rating in range(0, 5):
            self.ratings.append(rating)
        elif rating == None:
            pass
        else:
            print("Invalid rating.")

    def get_average_rating(self):
        total_rating = 0
        if len(self.ratings) > 0:
            for rating in self.ratings:
                total_rating += rating
        if len(self.ratings) > 0:
            return total_rating/len(self.ratings)
        else:
            print("There is no ratings for this book.")

class Fiction(Book):
    def __init__(self, title, author, isbn, price):
        super().__init__(title, isbn, price)
        self.author = author

    def __repr__(self):
        return "{title} by {author}, price: {price}".format(title=self.title, author=self.author, price=self.price)

    def get_author(self):
        return self.author

class Non_Fiction(Book):
    def __init__(self, title, subject, level, isbn, price):
        super().__init__(title, isbn, price)
        self.subject = subject
        self.level = level

    def __repr__(self):
        return "{title}, a {level} manual on {subject}, price: {price}".format(title=self.title, level=self.level,subject=self.subject, price=self.price)

    def get_subject(self):
        return self.subject

    def get_level(self):
        return self.level

class TomeRater():
    def __init__(self):
        self.users = {}
        self.books = {}

    def __repr__(self):
        return "Users: {users} \nBooks: {books}".format(users=self.users, books=self.books)

    def __eq__(self, other):
        return self.books == other.books and self.users == other.users

    def create_book(self, title, isbn, price):
        for book in self.books:
            if book.get_isbn() == isbn:
                print("This isbn already in use, please give a unique isbn.")
        else:
            return Book(title, isbn, price)

    def create_novel(self, title, author, isbn, price):
        for book in self.books:
            if book.get_isbn() == isbn:
                print("This isbn already in use, please give a unique isbn.")
        else:
            return Fiction(title, author, isbn, price)

    def create_non_fiction(self, title, subject, level, isbn, price):
        for book in self.books:
            if book.get_isbn() == isbn:
                print("This isbn already in use, please give a unique isbn.")
        else:
            return Non_Fiction(title, subject, level, isbn, price)

    def add_book_to_user(self, book, email, rating=None):
        for key, value in self.users.items():
            if key == email:
                value.read_book(book, rating)
                book.add_rating(rating)
                if book in self.books:
                    self.books.update({book: self.books[book]+1})
                else:
                    self.books[book] = 1
            elif key not in self.users:
                print("No user with email {email}!".format(email=email))

    def add_user(self, name, email, user_books=None):
        if email in self.users:
            print("User with this email already exists.")
        elif '@' not in email:
            print("Email is not valid")
        elif ('.com' not in email) and ('.edu' not in email) and ('.org' not in email):
            print("Email is not valid")
        else:
            self.users[email] = User(name, email)
            if user_books != None:
                for book in user_books:
                    self.add_book_to_user(book, email)

    def print_catalog(self):
        for book in self.books:
            print(book)

    def print_users(self):
        for user in self.users.values():
            print(user)

    def most_read_book(self):
        # return the book that has been read the most
        max = 0
        most_read_book = 0
        for key, value in self.books.items():
            if value > max:
                max = value
                most_read_book = key
        return most_read_book

    def highest_rated_book(self):
        # return the book that has the highest average rating
        highest_rated_book = 0
        max = 0
        for book in self.books:
            if book.get_average_rating() > max:
                max = book.get_average_rating()
                highest_rated_book = book
        return highest_rated_book

    def most_positive_user(self):
        # return the user that has the highest average rating.
        max_rating = 0
        for user in self.users.values():
            if user.get_average_rating() > max_rating:
                max_rating = user.get_average_rating()
        return user

    def get_n_most_read_books(self):
        # return the n books that have been read most, in descending order
        n = int(input("Please enter the number of most read books:"))
        for key, value in sorted(self.books.items(), key=lambda x: x[1], reverse=True)[0:n]:
            print(key)

    def get_n_most_prolific_readers(self):
        # return the n users that have read the most books, in descending order
        n = int(input("Please enter the number of users:"))
        most_prolific_readers = {user for user in sorted(self.users.values(), key=lambda x: x.get_number_of_books(), reverse=True)[0:n]}
        return most_prolific_readers

    def get_n_most_expensive_books(self, n):
        # return the n books with highest price
        most_expensive_books = {book for book in sorted(self.books, key=lambda x: x.get_price(), reverse=True)[0:n]}
        return most_expensive_books

    def get_worth_of_user(self, user_email):
        # return the sum of the costs of all the books read by this user
        for key, value in self.users.items():
            if key == user_email:
                books_read_by_user = [user.get_books() for user in self.users.values() if user == value]
                worth_of_user = 0
                for i in books_read_by_user:
                    for book in i:
                        worth_of_user += book.price
        return worth_of_user

