import redisbackend.py
import sys

def addBook(Title, Author, ISBN, Pages):
    # TODO: add books :)

def deleteBook(Title):
    #TODO: remove book

def editTitle(oldTitle, newTitle):
    #TODO: edit title

def editAuthor(Title, newAuthor):
    #TODO: this

def editISBN(Title, newISBN):
    #TODO: this

def editPages(Title, newPageCount):
    #TODO: this

def searchByTitle(Title, sortby = Author):
    #TODO: this

def searchByAuthor(Author, sortby = Author):
    #TODO: this

def searchByISBN(ISBN, sortby = Author):
    #TODO: this

def addBorrower(Name, Username, Phone = 0000000000):
    #TODO: this

def deleteBorrower(Username):
    #TODO: this

def editName(Username, newName):
    #TODO: this

def editUsername(oldUsername, newUsername):
    #TODO: this

def editPhone(Username, newPhone):
    #TODO: this

def checkoutBook(Username, ISBN):
    #TODO: this

def returnBook(Username, ISBN):
    #TODO: this

def getCheckedOutBooks(Username):
    #TODO: this

while(1):
    command = input()
    if(command != ""):
        parsedCommand = command.split()
