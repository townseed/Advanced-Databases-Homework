from neobackend import *
import sys

def addBook(Title, Author, ISBN, Pages, copies):
    print(backAddBook(Title, Author, ISBN, int(Pages), copies))

def deleteBook(ISBN):
    print(backDeleteBook(ISBN))

def editTitle(ISBN, newTitle):
    print(backEditTitle(ISBN, newTitle))

def editAuthor(ISBN, oldAuthor, newAuthor):
    print(backEditAuthor(ISBN, oldAuthor, newAuthor))

def addAuthor(ISBN, newAuthor):
    print(backAddAuthor(ISBN, newAuthor))

def editISBN(oldISBN, newISBN):
    print(backEditISBN(oldISBN, newISBN))

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
    print(backCheckoutBook(Username, ISBN))

def returnBook(Username, ISBN):
    print(backReturnBook(Username, ISBN))

def getCheckedOutBooks(Username, sortby = "Author"):
    print(backGetCheckedOutBooks(Username, sortby))

def searchByUsername(Username):
    print(backSearchUname(Username))

def searchByName(Name):
    print(backSearchName(Name))

def getUsersBorrowing(ISBN):
    print(backGetUsersBorrowing(ISBN))

def setCopies(ISBN, newCopies):
    print(backSetCopies(ISBN, newCopies))

def removeTitle(ISBN):
    print(backRemoveTitle(ISBN))

def removePages(ISBN):
    print(backRemovePages(ISBN))

def removeAuthors(ISBN):
    print(backRemoveAuthors(ISBN))

def removeName(Username):
    print(backRemoveName(Username))

def removePhone(Username):
    print(backRemovePhone(Username))

def addReview(Username, ISBN, stars, content = ""):
    print(backAddReview(Username, ISBN, stars, content))

def getRec(Username):
    print(backGetRec(Username))

def getAllBooks(sortby = "ISBN"):
    print(backGetAllBooks(sortby))

def startSystem():
    initSystem()
    print("constraints created")

def removeAuthor(ISBN, Author):
    print(backRemoveAuthor(ISBN, Author))

def getRec(Username):
    print(backGetRec(Username))

def getUserReviews(Username):
    print(backGetUserReviews(Username))

def getBookReviews(ISBN):
    print(backGetBookReviews(ISBN))

def exit():
    backExit()


while(1):
    command = input("Lib: ")
    if(command != ""):
        parsedCommand = command.split()
        # print("executing command: " + str(parsedCommand))
        if(parsedCommand[0].lower() == "addbook"):
            addBook(parsedCommand[1], parsedCommand[2], parsedCommand[3], parsedCommand[4], parsedCommand[5])
        elif(parsedCommand[0].lower() == "deletebook" or parsedCommand[0].lower() == "removebook"):
            deleteBook(parsedCommand[1])
        elif(parsedCommand[0].lower() == "edittitle"):
            editTitle(parsedCommand[1], parsedCommand[2])
        elif(parsedCommand[0].lower() == "editauthor"):
            editAuthor(parsedCommand[1], parsedCommand[2], parsedCommand[3])
        elif(parsedCommand[0].lower() == "addauthor"):
            addAuthor(parsedCommand[1], parsedCommand[2])
        elif(parsedCommand[0].lower() == "editisbn"):
            editISBN(parsedCommand[1], parsedCommand[2])
        elif(parsedCommand[0].lower() == "editpages"):
            editPages(parsedCommand[1], parsedCommand[2])
        elif(parsedCommand[0].lower() == "searchbytitle" or parsedCommand[0].lower() == "findbooktitle"):
            if(len(parsedCommand) > 2):
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
                addBorrower(parsedCommand[1], parsedCommand[2], parsedCommand[3])
            else: addBorrower(parsedCommand[1], parsedCommand[2])
        elif(parsedCommand[0].lower() == "deleteborrower" or parsedCommand[0].lower() == "removeborrower"):
            deleteBorrower(parsedCommand[1])
        elif(parsedCommand[0].lower() == "editname" or parsedCommand[0].lower() == "changename"):
            editName(parsedCommand[1], parsedCommand[2])
        elif(parsedCommand[0].lower() == "editusername" or parsedCommand[0].lower() == "changeusername"):
            editUsername(parsedCommand[1], parsedCommand[2])
        elif(parsedCommand[0].lower() == "editphone" or parsedCommand[0].lower() == "changephone"):
            editPhone(parsedCommand[1], parsedCommand[2])
        elif(parsedCommand[0].lower() == "checkoutbook" or parsedCommand[0] == "checkout"):
            checkoutBook(parsedCommand[1], parsedCommand[2])
        elif(parsedCommand[0].lower() == "returnbook" or parsedCommand[0].lower() == "return"):
            returnBook(parsedCommand[1], parsedCommand[2])
        elif(parsedCommand[0].lower() == "getcheckedoutbooks" or parsedCommand[0].lower() == "books"):
            if(len(parsedCommand) > 2):
                getCheckedOutBooks(parsedCommand[1], parsedCommand[2])
            else: getCheckedOutBooks(parsedCommand[1])
        elif(parsedCommand[0].lower() == "exit" or parsedCommand[0].lower() == "quit"):
            exit()
            break
        elif(parsedCommand[0].lower() == "getuser" or parsedCommand[0] == "getuserbyusername" or parsedCommand[0] == "searchbyusername"):
            searchByUsername(parsedCommand[1])
        elif(parsedCommand[0].lower() == "getuserbyname" or parsedCommand[0].lower() == "searchuserbyname"):
            searchByName(parsedCommand[1])
        elif(parsedCommand[0].lower() == "getusersborrowing"):
            getUsersBorrowing(parsedCommand[1])

        elif(parsedCommand[0].lower() == "removeauthors" or parsedCommand[0].lower() == "removeauthor" or parsedCommand[0].lower() == "deauthor"):
            removeAuthors(parsedCommand[1])

        elif(parsedCommand[0].lower() == "removetitle" or parsedCommand[0].lower() == "detitle"):
            removeTitle(parsedCommand[1])

        elif(parsedCommand[0].lower() == "removepages" or parsedCommand[0].lower() == "depage"):
            removePages(parsedCommand[1])
        elif(parsedCommand[0].lower() == "removename" or parsedCommand[0].lower() == "unname"):
            removeName(parsedCommand[1])
        elif(parsedCommand[0].lower() == "removephone" or parsedCommand[0].lower() == "dephone"):
            removePhone(parsedCommand[1])

        elif(parsedCommand[0].lower() == "addreview"):
            addReview(parsedCommand[1], parsedCommand[2], parsedCommand[3], parsedCommand[4])

        elif(parsedCommand[0].lower() == "start"):
            startSystem()

        elif(parsedCommand[0].lower() == "removeauthor"):
            removeAuthor(parsedCommand[1], parsedCommand[2])

        elif(parsedCommand[0].lower() == "getallbooks" or parsedCommand[0].lower() == "allbooks"):
            getAllBooks()

        elif(parsedCommand[0].lower() == "userreviews"):
            getUserReviews(parsedCommand[1])

        elif(parsedCommand[0].lower() == "getbookreviews"):
            getBookReviews(parsedCommand[1])

        elif(parsedCommand[0].lower() == "getrec"):
            getRec(Username)

        elif(parsedCommand[0].lower() == "setCopies" or parsedCommand[0].lower() == "editcopies"):
            setCopies(parsedCommand[1], parsedCommand[2])
        elif(parsedCommand[0].lower() == "test"):
            test()
        else: print("Unrecognized command")
