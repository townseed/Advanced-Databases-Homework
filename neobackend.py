from neo4j import GraphDatabase


def test_connection():
    # driver = GraphDatabase.driver(encrypted=False, uri="bolt://localhost:7687",
    #                               auth=("neo4j", "neo4j"))
    # session = driver.session()
    # input_string = 'hello Neo4J'
    # session.run("CREATE (a:Greeting) SET a.message = $message return a.message", message=input_string)
    # result = session.run("MATCH (n:Person)-[:DIRECTED]-(m:Movie) RETURN n AS Director,m.title ")
    # for record in result:
    #     print(record[0]['born'], record[0]['name'], record[0], record[1])
    # session.close()


test_connection()
