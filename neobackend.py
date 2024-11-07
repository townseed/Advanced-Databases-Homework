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

def test():
    ISBN = 1
    print(n.run("match (b:Book {ISBN: $ISBN}) with count(b) > 0 as existing return existing", ISBN = ISBN).single()["existing"])

def initSystem():
    n.run("CREATE CONSTRAINT for (b:Book) require b.ISBN IS UNIQUE") 
    n.run("CREATE CONSTRAINT for (u:User) require u.Username IS UNIQUE")

def backAddBook(Title, Author, ISBN, Pages, Copies):
    with driver.session() as neo:
        if(neo.run("match (b:Book {ISBN: $ISBN}) with count(b) > 0 as existing return existing", ISBN = ISBN).single()["existing"]): return "ISBN already exists"
        neo.run("CREATE (b:Book {Title: $Title, ISBN: $ISBN, Pages: $Pages, Copies: $Copies}) with b merge (a:Author {Name: $Author}) create (a)-[:wrote]->(b) return b",
                Title = Title, ISBN = ISBN, Pages = Pages, Copies = Copies, Author = Author)
        neo.close()
        return "book created"
    
def backDeleteBook(ISBN):
    with driver.session() as neo:
        if(neo.run("match (b:Book {ISBN: $ISBN}) with count(b) > 0 as existing return existing", ISBN = ISBN).single() is None): return "book does not exist"
        # if(neo.run("match (u:User)-[r:checkedOut]->(b:Book {ISBN: $ISBN}) return count(r) > 0 as usersHave", ISBN = ISBN).single()["usersHave"]): return "return all copies before deleting the book!"
        neo.run("match (b:Book {ISBN: $ISBN}) detach delete b", ISBN = ISBN)
        neo.close()
        return "book deleted"

def backEditTitle(ISBN, newTitle):
    with driver.session() as neo:
        if not neo.run("match (b:Book {ISBN: $ISBN}) set b.Title = $newTitle return b", ISBN = ISBN, newTitle = newTitle): return "book does not exist"
        neo.close()
        return "updated title"

def backEditAuthor(ISBN, oldAuthor, newAuthor):
    with driver.session() as neo:
        if not neo.run("match (a:Author {Name: $oldAuthor})-[r:wrote]->(b:Book {ISBN: $ISBN}) delete r return b",oldAuthor = oldAuthor, ISBN = ISBN): return "book does not exist"
        neo.run("match (b:Book {ISBN: $ISBN}) with b merge (a:Author {Name: $newAuthor}) create (a)-[:wrote]->(b) return b", ISBN = ISBN, newAuthor = newAuthor)
        neo.close()
        return "edited author"

def backRemoveAuthor(ISBN, Author):
    with driver.session() as neo:
        if not neo.run("match (a:Author {Name: $Author})-[r:wrote]->(b:Book {ISBN: $ISBN}) delete r return b",Author = Author, ISBN = ISBN): return "book does not exist"
        neo.close()
        return "removed author"

def backAddAuthor(ISBN, newAuthor):
    with driver.session() as neo:
        if not neo.run("match (b:Book {ISBN: $ISBN}) with b merge (a:Author {Name: $newAuthor}) create (a)-[:wrote]->(b) return b", ISBN = ISBN, newAuthor = newAuthor): return "book does not exist"
        neo.close()
        return "added author"
    
def backEditISBN(oldISBN, newISBN):
    with driver.session() as neo:
        if not neo.run("match (b:Book {ISBN: $oldISBN}) set b.ISBN = $newISBN return b", oldISBN = oldISBN, newISBN = newISBN): return "book does not exist"
        neo.close()
        return "Edited ISBN"

def backEditPages(ISBN, newPageCount):
    with driver.session() as neo:
        if not neo.run("match (b:Book {ISBN: '" + str(ISBN) +"'}) set b.Pages = $newPageCount return b", newPageCount = newPageCount): return "book does not exist"
        neo.close()
        return "pages updated"

def backSearchByTitle(Title, sortby = "Author"):
    res = ""
    if(sortby == "author" or sortby == "Author"):
        res = n.run("match (b:Book {Title: $Title})<-[:wrote]-(a:Author) return b, a order by a.Name", Title = Title)
    else:
        res = n.run("match (b:Book {Title: $Title})-[:wrote]-(a:Author) return b, a order by b."+sortby, Title = Title)
    books = []
    for book in res: 
        books.append(dict(book["b"]) | {"author": dict(book["a"])})
    return books

def backSearchByAuthor(Author, sortby = "Author"):
    res = ""
    if(sortby == "author" or sortby == "Author"):
        res = n.run("match (b:Book)-[:wrote]-(a:Author where a.Name = $name) return b, a order by a.Name", name = Author)
    else:
        res = n.run("match (b:Book)<-[:wrote]-(a:Author {Name: $name}) return b, a order by b."+sortby, name = Author)
    books = []
    for book in res: 
        books.append(dict(book["b"]) | {"author": dict(book["a"])})
    return books
        
def backSearchByISBN(ISBN, sortby = "Author"):
    res = ""
    if(sortby == "author" or sortby == "Author"):
        res = n.run("match (b:Book {ISBN: $ISBN})-[:wrote]-(a:Author) return b, a order by a.Name", ISBN = ISBN)
    else:
        res = n.run("match (b:Book {ISBN: $ISBN})-[:wrote]-(a:Author) return b, a order by b.$sortby", ISBN = ISBN, sortby = sortby)
    books = []
    for book in res: 
        books.append(dict(book["b"]) | {"author": dict(book["a"])})
    return books
 
def backAddBorrower(Name, Username, Phone):
    with driver.session() as neo:
        if(neo.run("match (u:User {Username: $Username}) return count(u) as existing", Username = Username).single()["existing"] != 0): return "Username taken"
        neo.run("CREATE (u:User {Username: $Username, Name: $Name, Phone: $Phone}) return u", Username = Username, Name = Name, Phone = Phone)
        neo.close()
        return "User created"

def backDeleteBorrower(Username):
    with driver.session() as neo:
        if(neo.run("match (u:User {Username: $Username}) return count(u) as existing", Username = Username).single()["existing"] == 0): return "User does not exist"
        booksrelated = neo.run("match (u:User {Username: $Username})-[r]-(:Book) return distinct type(r) as relations", Username = Username)
        for relation in booksrelated:
            if relations["r"] == "checkedOut": return "check out all books before deleting users!"
        
        neo.run("match (u:User {Username: $Username}) detach delete u", Username = Username)
        neo.close()
        return "user removed"

def backEditName(Username, newName):
    with driver.session() as neo:
        if not neo.run("match (u:User {Username: $Username}) set u.Name = $newName return u", Username = Username, newName = newName): return "user does not exist"
        neo.close()
        return "name changed"

def backEditUsername(oldUsername, newUsername):
    with driver.session() as neo:
        if not neo.run("match (u:User {Username: $oldUsername}) set u.Username = $newUsername return u", oldUsername = oldUsername, newUsername = newUsername): return "user does not exist"
        neo.close()
        return "Username changed"

def backEditPhone(Username, newPhone):
    with driver.session() as neo:
        if not neo.run("match (u:User {Username: $Username}) set u.Phone = $newPhone return u", Username = Username, newPhone = newPhone): return "user does not exist"
        neo.close()
        return "phone changed"

def backCheckoutBook(Username, ISBN):
    with driver.session() as neo:
        if(neo.run("match (u:User {Username: $Username}) return count(u) as existing", Username = Username).single()["existing"] == 0): return "User does not exist"
        if(neo.run("match (b:Book {ISBN: $ISBN}) return count(b) as existing", ISBN = ISBN).single()["existing"] == 0): return "book does not exist"
        bookrelated = neo.run("match (u:User {Username: $Username})-[r]->(b:Book {ISBN: $ISBN}) return type(r) as relations", Username = Username, ISBN = ISBN)
        for relation in bookrelated:
            if relation["relations"] == "checkedOut": return "User already has that book!"
        neo.run("match (u:User {Username: $Username}), (b:Book {ISBN: $ISBN}) create (u)-[:checkedOut]->(b)", Username = Username, ISBN = ISBN)
        neo.close()
        return "book checked out"

def backReturnBook(Username, ISBN):
    with driver.session() as neo:
        if not neo.run("match (u:User where u.Username = $Username)-[r:checkedOut]->(b:Book {ISBN: $ISBN}) delete r return b",Username = Username, ISBN = ISBN): return "book or user does not exist"
        neo.close()
        return "book returned"

def backGetCheckedOutBooks(Username, sortby):
    if(n.run("match (u:User where u.Username= $Username) return count(u) as existing", Username = Username).single()["existing"] == 0): return "User does not exist"
    result = ""
    if(sortby == "Author" or sortby == "author"): result = n.run("match (:User {Username: $Username})-[:checkedOut]-(b:Book) with b match (b)-[:wrote]-(a) return b, a order by a.Name", Username = Username)
    else: result = n.run("match (u:User {Username: $Username})-[:checkedOut]->(b:Book) with b match (b)-[:wrote]-(a) return b, a order by b.$sortby", Username = Username, sortby = sortby)
    books = []
    for book in result: 
        books.append(dict(book["b"]) | {"author": dict(book["a"])})
    return books
def backSearchUname(Username):
    search = n.run("match (u:User where u.Username = $Username) return u", Username = Username)
    users = []
    for user in search:
        users.append(dict(user["u"]))
    return users
    
def backSearchName(Name):
    search = n.run("match (u:User {Name: $Name}) return u", Name = Name)
    users = []
    for user in search:
        users.append(dict(user["u"]))
    return users

def backGetUsers():
    search = n.run("match (u:User) return u")
    users = []
    for user in search:
        users.append(dict(user["u"]))
    return users

def backGetUsersBorrowing(ISBN):
    if not n.run("match (b:Book {ISBN: $ISBN}) return b", ISBN = ISBN): return "Book does not exist"
    search = n.run("match (b:Book {ISBN: $ISBN})<-[:checkedOut]-(u:User) return u", ISBN = ISBN)
    users = []
    for user in search:
        users.append(dict(user["u"]))
    return users
    
def backSetCopies(ISBN, newCopies):
    with driver.session() as neo:
        if(neo.run("match (b:Book {ISBN: $ISBN}) return count(b) as existing", ISBN = ISBN).single()["existing"] == 0): return "book does not exist"
        bookrelated = neo.run("match (u:User)-[r]->(b:Book {ISBN: $ISBN}) return type(r) as relations", ISBN = ISBN)
        checkedout = 0
        for relation in bookrelated:
            if relation["relations"] == "checkedOut": checkedout = checkedout + 1
        if(checkedout > int(newCopies)): return "return more copies first"
        neo.run("match (b:Book {ISBN: $ISBN}) set b.Copies = $newCopies return b", ISBN = ISBN, newCopies = newCopies)
        neo.close()
        return "copies updated"

def backGetAllBooks(sortby):
    search = ""
    if(sortby == "Author"): 
        search = n.run("match (b:Book)-[:wrote]-(a:Author) return b, a order by a.name")
    else:
        search = n.run("match (b:Book)-[:wrote]-(a:Author) return b, a order by b." + sortby)
    books = []
    for book in search: 
        books.append(dict(book["b"]) | {"author": dict(book["a"])})
    return books
    
def backGetRec(Username):
    if(n.run("match (u:User where u.Username= $Username) return count(u) as existing", Username = Username).single()["existing"] == 0): return "User does not exist"
    #1: get books you liked
    #2: get other users who also liked them
    #3: get other books they liked
    search = n.run("match (:User {Username: $Username})-[r:reviewed where toInteger(r.Stars) >= 3]-(b:Book) with b match (b)-[r:reviewed where toInteger(r.Stars) >= 3]-(u:User where u.Username <> $Username) with u match (u)-[r:reviewed where toInteger(r.Stars) >= 3]-(f:Book) with f match (f)-[:wrote]-(a) return f, a", Username = Username)
    books = []
    for book in search: 
        books.append(dict(book["f"]) | {"author": dict(book["a"])})
    return books

def backAddReview(Username, ISBN, Stars, Content):
    if not 0 <= int(Stars) <= 5: return "unreasonable star rating"
    with driver.session() as neo:
        if(neo.run("match (u:User where u.Username= $Username) return count(u) as existing", Username = Username).single()["existing"] == 0): return "User does not exist"
        if(neo.run("match (b:Book {ISBN: $ISBN}) return count(b) as existing", ISBN = ISBN).single()["existing"] == 0): return "Book does not exist"
        neo.run("match (u:User {Username: $Username}), (b:Book {ISBN: $ISBN}) merge (u)-[r:reviewed]->(b) set r.Stars = $Stars, r.Content = $Content", Username = Username, Stars = Stars, Content = Content, ISBN = ISBN)
        neo.close()
        return "book reviewed"

def backGetUserReviews(Username):
    if(n.run("match (u:User where u.Username = $Username) return count(u) as existing", Username = Username).single()["existing"] == 0): return "User does not exist"
    result = n.run("match (:User {Username: $Username})-[r:reviewed]-(b:Book) return r, b", Username = Username)
    reviews = []
    for review in result:
        reviews.append(dict(review["r"]) | dict(review["b"]))
    return reviews

def backGetBookReviews(ISBN):
    if(n.run("match (b:Book {ISBN: $ISBN}) return count(b) as existing", ISBN = ISBN).single()["existing"] == 0): return "Book does not exist"
    result = n.run("match (:Book {ISBN: $ISBN})-[r:reviewed]-(u:User) return r, u", ISBN = ISBN)
    reviews = []
    for review in result:
        reviews.append(dict(review["r"]) | dict(review["u"]))
    return reviews
