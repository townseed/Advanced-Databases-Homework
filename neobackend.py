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
    n.run("CREATE (b:Book {Title: $title, ISBN: $ISBN, Pages: $pages, Copies: $copies}) with b merge (a:Author {Name: $Author}, create (a)-[:wrote]->(b)) return b",
            Title, ISBN, Pages, copies, Author)
    return "book created"
    
def backDeleteBook(ISBN):
    if(n.run("match (b:Book {ISBN: $ISBN} return count(b) as existing)", ISBN).single()["existing"] == 0): return "book does not exist"
    if(n.run("match (u:User)-[:checkedOut]->(b:Book {ISBN: $ISBN}) return count(u) as usersHave", ISBN).single()["usersHave"] != 0): return "return all copies before deleting the book!"
    n.run("match (b:Book {ISBN: $ISBN}) detach delete b return b")
    return "book deleted"

def backEditTitle(ISBN, newTitle):
    if not n.run("match (b:Book {ISBN: $ISBN}) set b.Title = $newTitle return b", ISBN, newTitle): return "book does not exist"
    return "updated title"

def backEditAuthor(ISBN, oldAuthor, newAuthor):
    if not n.run("match (a:Author {Name: $oldAuthor})-[r:wrote]->(b:Book {ISBN: $ISBN}) delete r return b",oldAuthor, ISBN): return "book does not exist"
    n.run("match (b:Book {ISBN: $ISBN}) with b merge (a:Author {Name: $newAuthor}, create (a)-[:wrote]->(b)) return b", ISBN, newAuthor)
    return "edited author"

def backRemoveAuthor(ISBN, Author):
    if not n.run("match (a:Author {Name: $Author})-[r:wrote]->(b:Book {ISBN: $ISBN}) delete r return b",Author, ISBN): return "book does not exist"
    return "removed author"

def backAddAuthor(ISBN, newAuthor):
    if not n.run("match (b:Book {ISBN: $ISBN}) with b merge (a:Author {Name: $newAuthor}, create (a)-[:wrote]->(b)) return b", ISBN, newAuthor): return "book does not exist"
    return "added author"
    
def backEditISBN(oldISBN, newISBN):
    if not n.run("match (b:Book {ISBN: $ISBN}) set b.ISBN = $newISBN return b", oldISBN, newISBN): return "book does not exist"
    return "Edited ISBN"

def backEditPages(ISBN, newPageCount):
    if not n.run("match (b:Book {ISBN: $ISBN}) set b.Pages = $newPageCount return b", ISBN, newPageCount): return "book does not exist"
    return "pages updated"

def backSearchByTitle(Title, sortby = "Author"):
    res = ""
    if(sortby == "author" or sortby == "Author"):
        res = n.run("match (b:Book {Title: $Title})<-[:wrote]-(a:Author) return b order by a.Name", Title)
    else:
        res = n.run("match (b:Book {Title: $Title}) return b order by b.$sortBy", Title, sortBy)
    return res

def backSearchByAuthor(Author, sortby = "Author"):
    res = ""
    if(sortby == "author" or sortby == "Author"):
        res = n.run("match (b:Book)<-[:wrote]-(a:Author {Name: $name}) return b order by a.Name", Author)
    else:
        res = n.run("match (b:Book)<-[:wrote]-(a:Author {Name: $name}) return b order by b.$sortby", Author, sortby)
    return res
        
def backSearchByISBN(ISBN, sortby = "Author"):
    res = ""
    if(sortby == "author" or sortby == "Author"):
        res = n.run("match (b:Book {ISBN: $ISBN})<-[:wrote]-(a:Author) return b order by a.Name", ISBN)
    else:
        res = n.run("match (b:Book {ISBN: $ISBN})<-[:wrote]-(a:Author) return b order by b.$sortby", ISBN, sortby)
    return res
 
def backAddBorrower(Name, Username, Phone):
    if(n.run("match (u:User {Username: $Username} return count(u) as existing)", Username).single()["existing"] != 0): return "Username taken"
    n.run("CREATE (u:User {Username: $Username, Name: $Name, Phone: $phone}) return u")
    return "User created"

def backDeleteBorrower(Username):
    if(n.run("match (u:User {Username: $Username} return count(u) as existing)", Username).single()["existing"] == 0): return "User does not exist"
    if not n.run("match (u:User {Username: $Username})-[r:checkedOut]->(:Book) return count(r) as existing", Username).single()["existing"] != 0): return "return all books before removing users!"
    n.run("match (u:User {Username: $Username}) detach delete u return u")
    return "user removed"

def backEditName(Username, newName):
    if not n.run("match (u:User {Username: $Username}) set u.Name = $newName return u", Username, newName): return "user does not exist"
    return "name changed"

def backEditUsername(oldUsername, newUsername):
    if not n.run("match (u:User {Username: $oldUsername}) set u.Username = $newUsername return u", oldUsername, newUsername): return "user does not exist"
    return "Username changed"

def backEditPhone(Username, newPhone):
    if not n.run("match (u:User {Username: $Username}) set u.Phone = $newPhone return u", Username, newPhone): return "user does not exist"
    return "phone changed"

def backCheckoutBook(Username, ISBN):
    if(n.run("match (u:User {Username: $Username}) return count(u) as existing)", Username).single()["existing"] == 0): return "User does not exist"
    if(n.run("match (b:Book {ISBN: $ISBN}) return count(b) as existing)", ISBN).single()["existing"] == 0): return "book does not exist"
    if(n.run("match (u:User {Username: $Username})-[:checkedOut]->(b:Book {ISBN: $ISBN}) return count(u) as existing)", Username, ISBN).single()["existing"] != 0): return "User already has a copy"
    n.run("create (u:User {Username: $Username})-[:checkedOut]->(b:Book {ISBN: $ISBN})", Username, ISBN)
    return "book checked out"

def backReturnBook(Username, ISBN):
    if not n.run("match (u:User {Username: $Username})-[r:checkedOut]->(b:Book {ISBN: $ISBN}) delete r return b",Username , ISBN): return "book or user does not exist"
    return "book returned"

def backGetCheckedOutBooks(Username, sortby):
    if(n.run("match (u:User {Username: $Username}) return count(u) as existing)", Username).single()["existing"] == 0): return "User does not exist"
    if(sortby == "Author" or sortby == "author"): return n.run()
    return n.run("match (u:User {Username: $Username})-[:checkedOut]->(b:Book) return b orderby b.$sortby", Username, sortby)

def backSearchByUsername(Username):
    return n.run("match (u:User {Username: $Username})")

def backSearchName(Name):
    return n.run("match (u:User {Name: $Name}) return u", Name)

def backGetUsersBorrowing(ISBN):
    if not n.run("match (b:Book {ISBN: $ISBN}) return b", ISBN): return "Book does not exist"
    return n.run("match (b:Book {ISBN: $ISBN})<-[:checkedOut]-(u:User) return u")

def backSetCopies(ISBN, newCopies):
    if(n.run("match (b:Book {ISBN: $ISBN}) return count(b) as existing)", ISBN).single()["existing"] == 0): return "book does not exist"
    if(n.run("match (b:Book {ISBN: $ISBN})<-[r:checkedOut]-(:User) return count(r)") > newCopies): return "return more copies first"
    n.run("match (b:Book {ISBN: $ISBN}) set b.Copies = $newCopies return b", ISBN, newCopies)
    return "copies updated"

def backGetAllBooks(sortby):
    search = ""
    if(sortby == "Author"): 
        search = n.run("match (b:Book)<-[:wrote]-(a:Author) return b order by a.name")
    else:
        search = n.run("match (b:Book) return b order by b.$sortby", sortby)
    return search
    
def backGetRec(Username):


def backAddReview(Username, ISBN, stars, content):
    if(n.run("match (u:User {Username: $Username}) return count(u) as existing", Username).single()["existing"] == 0): return "User does not exist"
    if(n.run("match (b:Book {ISBN: $ISBN} return count(b) as existing)", ISBN).single()["existing"] == 0): return "Book does not exist"
    if(n.run("match (u:User {Username: $Username})-[:reviewed] return count(u) as existing", Username).single()["existing"] != 0): return "Username taken"
