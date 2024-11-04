from neo4j import GraphDatabase

driver = GraphDatabase.driver(encrypted=False, uri="bolt://localhost:7687", auth=("neo4j", "neo4j1234"))
n = driver.session()

def backExit():
    print('exiting...')
    n.close()
    # input_string = 'hello Neo4J'
    # session.run("CREATE (a:Greeting) SET a.message = $message return a.message", message=input_string)
    # result = session.run("MATCH (n:Person)-[:DIRECTED]-(m:Movie) RETURN n AS Director,m.title ")
    # for record in result:
    #     print(record[0]['born'], record[0]['name'], record[0], record[1])
    # session.close()

def initSystem():
    n.run("CREATE CONSTRAINT ON (b:Book) ASSERT b.ISBN IS UNIQUE") 
    n.run("CREATE CONSTRAINT ON (u:User) ASSERT u.Username IS UNIQUE")

def backAddBook(Title, Author, ISBN, Pages, copies):
    if(n.run("match (b:Book {ISBN: $ISBN} return count(b) as existing)", ISBN).single()["existing"] != 0): return "ISBN already exists"
    n.run("CREATE (b:Book {title: $title, ISBN: $ISBN, pages: $pages, copies: $copies}) with b merge (a:Author {Name: $Author}, create (a)-[:wrote]->(b)) return b",
            Title, ISBN, Pages, copies, Author)
    return "book created"
    
def backDeleteBook(ISBN):
    if(n.run("match (b:Book {ISBN: $ISBN} return count(b) as existing)", ISBN).single()["existing"] == 0): return "book does not exist"
    if(n.run("match (u:User)-[:checkedOut]->(b:Book {ISBN: $ISBN}) return count(u) as usersHave", ISBN).single()["usersHave"] != 0): return "return all copies before deleting the book!"
    n.run("match (b:Book {ISBN: $ISBN}) detach delete b return b")
    return "book deleted"

def backEditTitle(ISBN, newTitle):
    if not n.run("match (b:Book {ISBN: $ISBN}) set b.title = $newTitle return b", ISBN, newTitle): return "book does not exist"
    return "updated title"

def backEditAuthor(ISBN, oldAuthor, newAuthor):
    if not n.run("match (a:Author {Name: $oldAuthor})-[r:wrote]->(b:Book {ISBN: $ISBN}) delete r return b",oldAuthor, ISBN): return "book does not exist"
    n.run("match (b:Book {ISBN: $ISBN}) with b merge (a:Author {Name: $newAuthor}, create (a)-[:wrote]->(b)) return b", ISBN, newAuthor)
    return "edited author"

def backAddAuthor(ISBN, newAuthor):
    if not n.run("match (b:Book {ISBN: $ISBN}) with b merge (a:Author {Name: $newAuthor}, create (a)-[:wrote]->(b)) return b", ISBN, newAuthor): return "book does not exist"
    return "added author"
    
def backEditISBN(oldISBN, newISBN):
    if not n.run("match (b:Book {ISBN: $ISBN}) set b.ISBN = $newISBN return b", oldISBN, newISBN): return "book does not exist"
    return "Edited ISBN"

def backEditPages(ISBN, newPageCount):
    if not n.run("match (b:Book {ISBN: $ISBN}) set b.pages = $newPageCount return b", ISBN, newPageCount): return "book does not exist"
    return "pages updated"

def backSearchByTitle(Title, sortby = "Author"):
    

def backSearchByAuthor(Author, sortby = "Author"):


def backSearchByISBN(ISBN, sortby = "Author"):


def backAddBorrower(Name, Username, Phone = "0000000000"):
    

def backDeleteBorrower(Username):
    

def backEditName(Username, newName):
    

def backEditUsername(oldUsername, newUsername):
    

def backEditPhone(Username, newPhone):
    

def backCheckoutBook(Username, ISBN):
    

def backReturnBook(Username, ISBN):
    

def backGetCheckedOutBooks(Username, sortby = "Author"):
    

def backSearchByUsername(Username):
    

def backSearchName(Name):


def backGetUsersBorrowing(ISBN):
    

def backSetCopies(ISBN, newCopies):


def backGetAllBooks(sortby):


def backGetRec(Username):


def backAddReview(Username, ISBN, stars, content):

