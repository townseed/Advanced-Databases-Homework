import redis
import operator
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

def backAddBook(Title, Author, ISBN, Pages):
    r.hset(ISBN, mapping={"Title": Title, "Author": Author, "Pages": Pages})
    r.sadd(Title, ISBN)
    r.sadd(Author, ISBN)
    return "book added"

def backDeleteBook(ISBN):
    r.srem(r.hget(ISBN, Title), ISBN)
    r.srem(r.hget(ISBN, Author), ISBN)
    r.delete(ISBN)
    return "removed"

def backEditTitle(ISBN, newTitle):
    r.srem(r.hget(ISBN, Title), ISBN)
    r.hset(ISBN, "Title", newTitle)
    r.sadd(Title, ISBN)
    return "title edited"

def backEditAuthor(ISBN, newAuthor):
    r.srem(r.hget(ISBN, Author), ISBN)
    r.hset(ISBN, "Author", newAuthor)
    r.sadd(Author, ISBN)
    return "edited author"

def backEditISBN(oldISBN, newISBN):
    r.srem(r.hget(oldISBN, Title), oldISBN)
    r.srem(r.hget(oldISBN, Author), oldISBN)
    r.sadd(Title, newISBN)
    r.sadd(Author, newISBN)
    r.rename(oldISBN, newISBN)
    return "updated ISBN"

def backEditPages(ISBN, newPageCount):
    r.hset(ISBN, "Pages", newPageCount)
    return "updated pagecount"

def backSearchByTitle(Title, sortby):
    isbns = r.smembers(Title)
    listofinfo = []
    for title in isbns:
        listofinfo.append(backSearchByISBN(title, sortby))
    listofinfo.sort(key = operator.itemgetter(sortby))
    return listofinfo

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
