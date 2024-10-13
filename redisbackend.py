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

def backAddBook(Title, Author, ISBN, Pages):
    r.hset(ISBN, mapping={"Title": Title, "Author": Author, "Pages": Pages, "ISBN" : ISBN})
    r.sadd(Title, ISBN)
    r.sadd(Author, ISBN)
    return "book added"
    
def backAddAuthor(ISBN, Author):
    r.sadd(Author, ISBN)
    r.hset(ISBN, "Author", r.hget(ISBN, "Author") + ";" + Author)
    
def backDeleteBook(ISBN):
    r.srem(r.hget(ISBN, Title), ISBN)
    r.srem(r.hget(ISBN, Author), ISBN)
    r.delete(ISBN)
    change = r.smembers(ISBN + ":checkedout")
    for user in change:
        r.srem(user + ":checkedout", ISBN)
    r.delete(ISBN + ":checkedout")
    return "removed"

def backEditTitle(ISBN, newTitle):
    r.srem(r.hget(ISBN, "Title"), ISBN)
    r.hset(ISBN, "Title", newTitle)
    r.sadd(Title, ISBN)
    return "title edited"

def backEditAuthor(ISBN, newAuthor):
    r.srem(r.hget(ISBN, "Author"), ISBN)
    r.hset(ISBN, "Author", newAuthor)
    r.sadd(Author, ISBN)
    return "edited author"

def backEditISBN(oldISBN, newISBN):
    r.srem(r.hget(oldISBN, "Title"), oldISBN)
    r.srem(r.hget(oldISBN, "Author"), oldISBN)
    r.sadd(Title, newISBN)
    r.sadd(Author, newISBN)
    r.hset(oldISBN, "ISBN", newISBN)
    r.rename(oldISBN, newISBN)
    change = r.smembers(newISBN + ":checkedout")
    for user in change:
        r.srem(user + ":checkedout", oldISBN)
        r.sadd(user + ":checkedout", newISBN)
    return "updated ISBN"

def backEditPages(ISBN, newPageCount):
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
    r.delete(Username + ":checkedout")
    r.delete(Username)
    change = r.smembers(Username + ":checkedout")
    for book in change:
        r.srem(book + ":checkedout", Username)
    r.delete(Username + ":checkedout")
    return "borrower deleted"

def backEditName(Username, newName):
    r.srem(r.hget(Username, "Name"), Username)
    r.sadd(newName, Username)
    r.hset(Username, "Name", newName)
    return "name changed"

def backEditUsername(oldUsername, newUsername):
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
    r.hset(Username, "Phone", newPhone)
    return "phone changed"

def backCheckoutBook(Username, ISBN):
    r.sadd(Username + ":checkedout", ISBN)
    r.hincrby(Username, "CheckedOut", 1)
    r.sadd(ISBN + ":checkedout", Username)
    return "book borrowed"

def backReturnBook(Username, ISBN):
    r.srem(Username + ":checkedout", ISBN)
    r.hincrby(Username, "CheckedOut", -1)
    r.srem(ISBN + ":checkedout", Username)
    return "book restored"

def backGetCheckedOutBooks(Username, sortby):
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
