import redis
import operator
from functools import cmp_to_key

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

def compareBookLengths(item1, item2):
    return int(operator.itemgetter("Pages")(item1)) - int(operator.itemgetter("Pages")(item2))

def compareBookISBNs(item1, item2):
    return int(operator.itemgetter("ISBN")(item1)) - int(operator.itemgetter("ISBN")(item2))

def backSearchUname(Username):
    return r.hgetall(Username)

def backAddBook(Title, Author, ISBN, Pages, copies):
    r.hset(ISBN, mapping={"Title": Title, "Author": Author, "Pages": Pages, "ISBN" : ISBN, "Copies": copies, "CheckedOut": 0})
    r.sadd(Title, ISBN)
    r.sadd(Author, ISBN)
    return "book added"
    
def backAddAuthor(ISBN, Author):
    if(r.exists(Username) == 0): return "User does not exist"
    r.sadd(Author, ISBN)
    r.hset(ISBN, "Author", r.hget(ISBN, "Author") + ";" + Author)
    
def backDeleteBook(ISBN):
    if(r.exists(ISBN) == 0): return "Book does not exist"
    if(int(r.hget(ISBN, "CheckedOut")) > 0): return "Return copies before removing book"
    r.srem(r.hget(ISBN, "Title"), ISBN)
    r.srem(r.hget(ISBN, "Author"), ISBN)
    r.delete(ISBN)
    r.delete(ISBN + ":checkedout")
    return "removed"

def backEditTitle(ISBN, newTitle):
    if(r.exists(ISBN) == 0): return "Book does not exist"
    r.srem(r.hget(ISBN, "Title"), ISBN)
    r.hset(ISBN, "Title", newTitle)
    r.sadd(Title, ISBN)
    return "title edited"

def backEditAuthor(ISBN, newAuthor):
    if(r.exists(ISBN) == 0): return "Book does not exist"
    r.srem(r.hget(ISBN, "Author"), ISBN)
    r.hset(ISBN, "Author", newAuthor)
    r.sadd(Author, ISBN)
    return "edited author"

def backEditISBN(oldISBN, newISBN):
    if(r.exists(oldISBN) == 0): return "Book does not exist"
    r.srem(r.hget(oldISBN, "Title"), oldISBN)
    r.srem(r.hget(oldISBN, "Author"), oldISBN)
    r.sadd(r.hget(oldISBN, "Title"), newISBN)
    r.sadd(r.hget(oldISBN, "Author"), newISBN)
    r.hset(oldISBN, "ISBN", newISBN)
    r.rename(oldISBN, newISBN)
    change = r.smembers(oldISBN + ":checkedout")
    for user in change:
        r.srem(user + ":checkedout", oldISBN)
        r.sadd(user + ":checkedout", newISBN)
    r.rename(oldISBN + ":checkedout", newISBN + ":checkedout")
    return "updated ISBN"

def backEditPages(ISBN, newPageCount):
    if(r.exists(ISBN) == 0): return "Book does not exist"
    r.hset(ISBN, "Pages", newPageCount)
    return "updated pagecount"

def backSearchByTitle(Title, sortby):
    isbns = r.smembers(Title)
    listofinfo = []
    for title in isbns:
        listofinfo.append(backSearchByISBN(title, sortby))
    if(sortby == "Pages"):
        listofinfo = sorted(listofinfo, key=cmp_to_key(compareBookLengths))
    elif(sortby == "ISBN"):
        listofinfo = sorted(listofinfo, key=cmp_to_key(compareBookISBNs))
    else: listofinfo.sort(key = operator.itemgetter(sortby))
    return listofinfo

def backSearchByAuthor(Author, sortby):
    isbns = r.smembers(Author)
    listofinfo = []
    for title in isbns:
        listofinfo.append(backSearchByISBN(title, sortby))
    if(sortby == "Pages"):
        listofinfo = sorted(listofinfo, key=cmp_to_key(compareBookLengths))
    elif(sortby == "ISBN"):
        listofinfo = sorted(listofinfo, key=cmp_to_key(compareBookISBNs))
    else: listofinfo.sort(key = operator.itemgetter(sortby))
    return listofinfo

def backSearchByISBN(ISBN, sortby):
    return r.hgetall(ISBN)
    
def backAddBorrower(Name, Username, Phone):
    r.hset(Username, mapping = {"Name": Name,"Username": Username, "Phone": Phone, "CheckedOut": 0})
    r.sadd(Name, Username)
    return "borrower added"

def backDeleteBorrower(Username):
    if(r.exists(Username) == 0): return "User does not exist"
    if(int(r.hget(Username, "CheckedOut")) > 0): return "Return all books before deleting a user!"
    r.delete(Username)
    r.delete(Username + ":checkedout")
    return "borrower deleted"

def backEditName(Username, newName):
    if(r.exists(Username) == 0): return "User does not exist"
    r.srem(r.hget(Username, "Name"), Username)
    r.sadd(newName, Username)
    r.hset(Username, "Name", newName)
    return "name changed"

def backEditUsername(oldUsername, newUsername):
    if(r.exists(oldUsername) == 0): return "User does not exist"
    r.srem(r.hget(oldUsername, "Name"), oldUsername)
    r.sadd(r.hget(oldUsername, "Name"), newUsername)
    r.hset(oldUsername, "Username", newUsername)
    r.rename(oldUsername, newUsername)
    r.rename(oldUsername + ":checkedout", newUsername + ":checkedout")
    change = r.smembers(newUsername + ":checkedout")
    for book in change:
        r.srem(book + ":checkedout", oldUsername)
        r.sadd(book + ":checkedout", newUsername)
    return "username changed"

def backEditPhone(Username, newPhone):
    if(r.exists(Username) == 0): return "User does not exist"
    r.hset(Username, "Phone", newPhone)
    return "phone changed"

def backCheckoutBook(Username, ISBN):
    if(r.exists(Username) == 0): return "User does not exist"
    if(r.exists(ISBN) == 0): return "Book does not exist"
    if(r.sismember(Username + ":checkedout", ISBN) == 1): return "This user already has a copy"
    r.sadd(Username + ":checkedout", ISBN)
    r.hincrby(Username, "CheckedOut", 1)
    r.sadd(ISBN + ":checkedout", Username)
    r.hincrby(ISBN, "CheckedOut", 1)
    return "book borrowed"

def backReturnBook(Username, ISBN):
    if(r.exists(Username) == 0): return "User does not exist"
    if(r.exists(ISBN) == 0): return "Book does not exist"
    if(r.sismember(Username + ":checkedout", ISBN) == 0): return "Cannot return book that is not checked out."
    r.srem(Username + ":checkedout", ISBN)
    r.hincrby(Username, "CheckedOut", -1)
    r.srem(ISBN + ":checkedout", Username)
    r.hincrby(ISBN, "CheckedOut", -1)
    return "book restored"

def backGetCheckedOutBooks(Username, sortby):
    if(r.exists(Username) == 0): return "User does not exist"
    isbns = r.smembers(Username + ":checkedout")
    listofinfo = []
    for title in isbns:
        listofinfo.append(backSearchByISBN(title, "Title"))
    if(sortby == "Pages"):
        listofinfo = sorted(listofinfo, key=cmp_to_key(compareBookLengths))
    elif(sortby == "ISBN"):
        listofinfo = sorted(listofinfo, key=cmp_to_key(compareBookISBNs))
    else: listofinfo.sort(key = operator.itemgetter(sortby))
    return listofinfo

def backGetUsersBorrowing(ISBN):
    if(r.exists(ISBN) == 0): return "Book does not exist"
    unames = r.smembers(ISBN + ":checkedout")
    listinfo = []
    for user in unames:
        listinfo.append(backSearchUname(user))
    return listinfo

def backSearchName(Name):
    unames = r.smembers(Name)
    listinfo = []
    for user in unames:
        listinfo.append(backSearchUname(user))
    return listinfo

def backCheckBook(ISBN):
    if(r.exists(ISBN) == 0): return False
    cap = r.hget(ISBN, "Copies")
    out = r.hget(ISBN, "CheckedOut")
    return cap > out
