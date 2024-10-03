import redis
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

def backAddBook(Title, Author, ISBN, Pages):
    r.hset(ISBN, mapping={
        'Author': Author,
        "Title": Title,
        "Page Count": Pages
    })
    return "book added"

def backDeleteBook(ISBN):
    r.
    return "removed"

def backEditTitle(ISBN, newTitle):
    return "title edited"

def backEditAuthor(ISBN, newAuthor):
    return "edited author"

def backEditISBN(oldISBN, newISBN):
    return "updated ISBN"

def backEditPages(ISBN, newPageCount):
    return "updated pagecount"

def backSearchByTitle(Title, sortby):
    return "search results"

def backSearchByAuthor(Author, sortby):
    return "search results"

def backSearchByISBN(ISBN, sortby):
    return r.hgetall(ISBN)
    
def backAddBorrower(Name, Username, Phone):
    return "borrower added"

def backDeleteBorrower(Username):
    return "borrower deleted"

def backEditName(Username, newName):
    return "name changed"

def backEditUsername(oldUsername, newUsername):
    return "username changed"

def backEditPhone(Username, newPhone):
    return "phone changed"

def backCheckoutBook(Username, ISBN):
    return "book borrowed"

def backReturnBook(Username, ISBN):
    return "book restored"

def backGetCheckedOutBooks(Username):
    return "search results"
