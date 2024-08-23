import psycopg2
import time

# Database connection parameters
db_params = {
    'database': 'postgres',
    'user': 'postgres',
    'password': 'password',
    'host': 'localhost',
    'port': '5432'
}

# Define your query
#sql_query = "SELECT DISTINCT to_node_id FROM nodes WHERE from_node_id = 2494 UNION SELECT DISTINCT from_node_id FROM nodes WHERE to_node_id = 2494;"
#sql_query = "SELECT DISTINCT a.to_node_id FROM nodes a JOIN nodes b ON a.to_node_id = b.to_node_id WHERE a.from_node_id = 2494 AND b.from_node_id = 37;"
sql_query = "SELECT b.from_node_id AS node, COUNT(DISTINCT a.to_node_id) AS common_nodes_count FROM nodes AS a JOIN nodes AS b ON a.to_node_id = b.to_node_id WHERE a.from_node_id = 2494 AND b.from_node_id != 2494 GROUP BY b.from_node_id ORDER BY common_nodes_count DESC;"


def measure_query_throughput(query, repetitions):
    """ Measures the execution time of a given SQL query repeated a specified number of times. """
    connection = None
    try:
        # Connect to the PostgreSQL database
        connection = psycopg2.connect(**db_params)
        cursor = connection.cursor()

        # Start timing
        start_time = time.time()

        # Execute the query multiple times
        for _ in range(repetitions):
            cursor.execute(query)

        # Calculate elapsed time
        elapsed_time = time.time() - start_time
        queries_per_second = repetitions / elapsed_time

        # Output results
        print(f"Total time for {repetitions} queries: {elapsed_time:.2f} seconds")
        print(f"Queries per second: {queries_per_second:.2f}")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the database connection
        if connection is not None:
            cursor.close()
            connection.close()

# Call the function with the query
measure_query_throughput(sql_query, 100)

