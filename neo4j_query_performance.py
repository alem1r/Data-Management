from neo4j import GraphDatabase
import time

# Neo4J connection URI and credentials
uri = "bolt://localhost:7687"  
username = "neo4j"             
password = "password"         

# Initialize the Neo4J driver
driver = GraphDatabase.driver(uri, auth=(username, password))

def measure_query_throughput(query, repetitions):
    """
    Measures the execution time of a given Cypher query repeated a specified number of times.
    """
    # Start timing
    start_time = time.time()
    
    # Execute the query multiple times
    with driver.session() as session:
        for _ in range(repetitions):
            session.run(query)
    
    # Calculate elapsed time
    elapsed_time = time.time() - start_time
    queries_per_second = repetitions / elapsed_time
    
    # Output results
    print(f"Total time for {repetitions} queries: {elapsed_time:.2f} seconds")
    print(f"Queries per second: {queries_per_second:.2f}")

# Define your query
#cypher_query = "MATCH (n:Node {id: 2494})-[:CONNECTS_TO]-(connected) RETURN DISTINCT connected.id;"
#cypher_query = "MATCH (a:Node {id: 2494})-[:CONNECTS_TO]->(common)<-[:CONNECTS_TO]-(b:Node {id: 37}) RETURN common.id;"
cypher_query = "MATCH (n:Node {id: 2494})-[:CONNECTS_TO]->(common)<-[:CONNECTS_TO]-(other) WHERE other.id <> 2494 RETURN other.id AS node, COUNT(DISTINCT common) AS common_nodes_count ORDER BY common_nodes_count DESC;"
# Call the function with the query
measure_query_throughput(cypher_query, 100)
