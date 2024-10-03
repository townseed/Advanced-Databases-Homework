from redisbackend import *
import sys

def addBook(Title, Author, ISBN, Pages):
    print(backAddBook(Title, Author, int(ISBN), int(Pages)))

def deleteBook(ISBN):
    print(backDeleteBook(int(ISBN)))

def editTitle(ISBN, newTitle):
    print(backEditTitle(int(ISBN), newTitle))

def editAuthor(ISBN, newAuthor):
    print(backEditAuthor(int(ISBN), newAuthor))

def editISBN(oldISBN, newISBN):
    print(backEditISBN(int(oldISBN), int(newISBN)))

def editPages(ISBN, newPageCount):
    print(backEditPages(int(ISBN), int(newPageCount)))

def searchByTitle(Title, sortby = "Author"):
    print(backSearchByTitle(Title, sortby))

def searchByAuthor(Author, sortby = "Author"):
    print(backSearchByAuthor(Author, sortby))

def searchByISBN(ISBN, sortby = "Author"):
    print(backSearchByISBN(ISBN, sortby))

def addBorrower(Name, Username, Phone = "0000000000"):
    print(backAddBorrower(Name, Username, int(Phone)))

def deleteBorrower(Username):
    print(backDeleteBorrower(Username))

def editName(Username, newName):
    print(backEditName(Username, newName))

def editUsername(oldUsername, newUsername):
    print(backEditUsername(oldUsername, newUsername))

def editPhone(Username, newPhone):
    print(backEditPhone(Username, int(newPhone)))

def checkoutBook(Username, ISBN):
    print(backCheckoutBook(Username, int(ISBN)))

def returnBook(Username, ISBN):
    print(backReturnBook(Username, int(ISBN)))

def getCheckedOutBooks(Username):
    print(backGetCheckedOutBooks(Username))

while(1):
    command = input("Lib: ")
    if(command != ""):
        parsedCommand = command.split()
        print("executing command: " + str(parsedCommand))
        if(parsedCommand[0].lower() == "addbook"):
            addBook(parsedCommand[1], parsedCommand[2], parsedCommand[3], parsedCommand[4])
        elif(parsedCommand[0].lower() == "deletebook" or parsedCommand[0].lower() == "removebook"):
            deleteBook(parsedCommand[1])
        elif(parsedCommand[0].lower() == "edittitle"):
            editTitle(parsedCommand[1], parsedCommand[2])
        elif(parsedCommand[0].lower() == "editauthor"):
            editAuthor(parsedCommand[1], parsedCommand[2])
        elif(parsedCommand[0].lower() == "editisbn"):
            editISBN(parsedCommand[1], parsedCommand[2])
        elif(parsedCommand[0].lower() == "editpages"):
            editPages(parsedCommand[1], parsedCommand[2])
        elif(parsedCommand[0].lower() == "searchbytitle" or parsedCommand[0].lower() == "findbooktitle"):
            if(len(parsedCommand) > 3):
                searchByTitle(parsedCommand[1], parsedCommand[2])
            else: searchByTitle(parsedCommand[1], "Author")
        elif(parsedCommand[0].lower() == "searchbyauthor"):
            if(len(parsedCommand) > 2):
                searchByAuthor(parsedCommand[1], parsedCommand[2])
            else: searchByAuthor(parsedCommand[1])
        elif(parsedCommand[0].lower() == "searchbyisbn" or parsedCommand[0].lower() == "getbook"):
            if(len(parsedCommand) > 2):
                searchByISBN(parsedCommand[1], parsedCommand[2])
            else: searchByISBN(parsedCommand[1])
        elif(parsedCommand[0].lower() == "addborrower"):
            if(len(parsedCommand) > 3):
                searchByTitle(parsedCommand[1], parsedCommand[2], parsedCommand[3])
            else: searchByTitle(parsedCommand[1], parsedCommand[2])
        elif(parsedCommand[0].lower() == "deleteborrower" or parsedCommand[0].lower() == "removeborrower"):
            deleteBorrower(parsedCommand[1])
        elif(parsedCommand[0].lower() == "editname" or parsedCommand[0].lower() == "changename"):
            editName(parsedCommand[1], parsedCommand[2])
        elif(parsedCommand[0].lower() == "editusername" or parsedCommand[0].lower() == "changeusername"):
            editUsername(parsedCommand[1], parsedCommand[2])
        elif(parsedCommand[0].lower() == "editphone" or parsedCommand[0].lower() == "changephone"):
            editPhone(parsedCommand[1], parsedCommand[2])
        elif(parsedCommand[0].lower() == "checkoutbook" or parsedCommand[0] == "checkout"):
            checkoutbook(parsedCommand[1], parsedCommand[2])
        elif(parsedCommand[0].lower() == "returnbook" or parsedCommand[0].lower() == "return"):
            returnBook(parsedCommand[1], parsedCommand[2])
        elif(parsedCommand[0].lower() == "getcheckedoutbooks" or parsedCommand[0].lower() == "books"):
            getCheckedOutBooks(parsedCommand[1])
        elif(parsedCommand[0].lower() == "exit" or parsedCommand[0].lower() == "quit"):
            break
        else: print("Unrecognized command")
