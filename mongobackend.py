import pymongo
import operator
from functools import cmp_to_key

m = pymongo.MongoClient("mongodb://localhost:27017/")
db = m["library"]
books = db["books"]
users = db["users"]

def compareBookLengths(item1, item2):
    return int(operator.itemgetter("Pages")(item1)) - int(operator.itemgetter("Pages")(item2))

def compareBookISBNs(item1, item2):
    return int(operator.itemgetter("ISBN")(item1)) - int(operator.itemgetter("ISBN")(item2))

def backSearchUname(Username):
    return users.find_one({"_id": Username})

def backAddBook(Title, Author, ISBN, Pages, Copies):
    if(books.find_one({"_id": ISBN})): return "book already exists"
    books.insert_one({"Title": Title, "Author": [Author], "_id": ISBN, "Pages": Pages, "Copies": int(Copies), "CheckedOutBy": [], "NumberCheckedOut": 0})
    return "book added"
    
def backAddAuthor(ISBN, Author):
    if(not books.find_one({"_id": ISBN})): return "Book does not exist"
    books.update_one({"_id": ISBN}, {"$push": {"Author": Author}})
    return "added author"
        
def backDeleteBook(ISBN):
    if(books.find_one({"_id": ISBN})["NumberCheckedOut"] == 0):
        books.delete_one({"_id": ISBN})

    else:
        return "Book is checked out, return before deleting."    

    return "removed"

def backEditTitle(ISBN, newTitle):
    if(not books.find_one({"_id": ISBN})): return "Book does not exist"
    books.update_one({"_id": ISBN}, {"$set": {"Title": newTitle}})
    return "title edited"

def backEditAuthor(ISBN, oldAuthor, newAuthor):
    if(not books.find_one({"_id": ISBN})): return "Book does not exist"
    books.update_one({"_id": ISBN}, {"$pull": {"Author": oldAuthor} })
    books.update_one({"_id": ISBN}, {"$addToSet": {"Author": newAuthor} })
    return "edited author"

def backEditISBN(oldISBN, newISBN):
    if(not books.find_one({"_id": oldISBN})): return "Book does not exist"
    if(books.find_one({"_id": newISBN})): return "Book with new ISBN already exists!"
    old = books.find_one({"_id": oldISBN})
    old['_id'] = newISBN
    books.insert_one(old)
    books.delete_one({"_id": oldISBN})
    usersThatHave = users.find({"CheckedOut": oldISBN})
    for user in usersThatHave:
        users.update_one({"_id": user['_id']}, {"$pull": {"CheckedOut": oldISBN}})
        users.update_one({"_id": user['_id']}, {"$addToSet": {"CheckedOut": newISBN}})
        
    usersThatHave.close()
    return "updated ISBN"

def backEditPages(ISBN, newPageCount):
    if(not books.find_one({"_id": ISBN})): return "Book does not exist"
    books.update_one({"_id": ISBN}, {"$set": {"Pages": newPageCount}})
    return "updated pagecount"

def backSearchByTitle(Title, sortby):
    return books.find({"Title": Title}).sort(sortby)

def backSearchByAuthor(Author, sortby):
    data = ""
    wrote = books.find({"Author": Author}).sort(sortby)
    for book in wrote:
        data += str(book)
    wrote.close()
    return data

def backSearchByISBN(ISBN, sortby):
    return books.find_one({"_id": ISBN})
    
def backAddBorrower(Name, Username, Phone):
    users.insert_one({"Name": Name, "_id": Username, "Phone": Phone, "CheckedOut": []})
    return "borrower added"

def backDeleteBorrower(Username):
    if(users.find_one({"_id": Username})["CheckedOut"] == []):
        users.delete_one({"_id": Username})
        return "borrower deleted"
    else:
        return "return books before deleting borrower"

def backEditName(Username, newName):
    if(not users.find_one({"_id": Username})): return "User does not exist"
    users.update_one({"_id": Username}, {"$set": {"Name": newName}})
    return "name changed"

def backEditUsername(oldUsername, newUsername):
    if(not users.find_one({"_id": oldUsername})): return "User does not exist"
    if(users.find_one({"_id": newUsername})): return "Username is taken"
    old = users.find_one({"_id": oldUsername})
    old._id = newUsername
    users.insert_one(old)
    users.delete_one({"_id": oldUsername})
    booksCheckedOut = books.find({"CheckedOutBy": oldUsername})
    for book in booksCheckedOut:
        books.update_one({"_id": book._id}, {"CheckedOut": {"$pull": oldUsername}})
        books.update_one({"_id": book._id}, {"CheckedOut": {"$addToSet": newUsername}})
    return "username changed"

def backEditPhone(Username, newPhone):
    if(not users.find_one({"_id": Username})): return "User does not exist"
    users.update_one({"_id": Username}, {"Phone": newPhone})
    return "phone changed"

def backCheckoutBook(Username, ISBN):
    if(not users.find_one({"_id": Username})): return "User does not exist"
    if(not books.find_one({"_id": ISBN})): return "Book does not exist"
    if(users.find_one({"CheckedOut": {"$elemMatch": {"$eq": ISBN}}})): return "This user already has a copy"
    if(books.find_one({"_id": ISBN})['Copies'] < 1 + books.find_one({"_id": ISBN})['NumberCheckedOut']): return "no copies available"
    books.update_one({"_id": ISBN}, {"$addToSet": {"CheckedOutBy": Username}})
    users.update_one({"_id": Username}, {"$addToSet": {"CheckedOut": ISBN}})
    return "book borrowed"

def backReturnBook(Username, ISBN):
    if(not users.find_one({"_id": Username})): return "User does not exist"
    if(not books.find_one({"_id": ISBN})): return "Book does not exist"
    if(not users.find_one({"_id": Username}, {"CheckedOut": ISBN})): return "Cannot return book that is not checked out."
    books.update_one({"_id": ISBN}, {"$pull": {"CheckedOutBy": Username}})
    users.update_one({"_id": Username}, {"$pull": {"CheckedOut": ISBN}})
    return "book restored"

def backGetCheckedOutBooks(Username, sortby):
    if(not users.find_one({"_id": Username})): return "User does not exist"
    data = ""
    for book in users.find_one({"_id": Username})["CheckedOut"]:
        data += str(books.find_one({"_id": book}))
    return data
    

def backGetUsersBorrowing(ISBN):
    if(not books.find_one({"_id": ISBN})): return "book does not exist"
    data = ""
    for user in books.find_one({"_id": ISBN})["CheckedOutBy"]:
        data += str(users.find_one({"_id": user}))
    return data

def backSearchName(Name):
    unames = users.find({"Name": Name})
    listinfo = "" 
    for user in unames:
        listinfo += str(user)
    return listinfo

# def backCheckBook(ISBN):
    # if(r.exists(ISBN) == 0): return False
    # cap = r.hget(ISBN, "Copies")
    # out = r.hget(ISBN, "CheckedOut")
    # return cap > out

def test():
    print(books.find_one({"_id": '1'})["NumberCheckedOut"])
