import psycopg2
from decimal import Decimal

# Function to connect to the PostgreSQL database
def connect_to_db():
    try:
        conn = psycopg2.connect(
            dbname="laptops2024",
            user="postgres", #please replace with your account user name if not usuing local one
            password="password", #please replace with your password for postgresql local account or standard account password
            host="localhost",
            port="5432"
        )
        return conn
    except Exception as e:
        print(f"An error occurred while connecting to the database: {e}")
        return None

# Function to insert data into a table
def insert_data(conn, table_name):
    try:
        with conn.cursor() as cur:
            if table_name == "Laptop":
                model = input("Enter laptop model: ")
                istouchscreen = input("Enter True of False, if it's touch compatible: ").strip().lower() in ('true', 't', 'yes', 'y')
                displaysize = float(input("Enter display size (decimal value): "))
                resolutionwidth = int(input("Enter resoultion width (i.e 1920, 2560, etc): "))
                resolutionheight = int(input("Enter resoultion height (i.e 1080, 1440, etc): "))
                cur.execute("INSERT INTO laptop (model, is_touch_screen, display_size, resolution_width, resolution_height) VALUES (%s, %s, %s, %s, %s) RETURNING laptop_id;", (model, istouchscreen, displaysize, resolutionwidth, resolutionheight,))

            elif table_name == "Storage":
                laptop_id = input("Enter laptop ID this spec information belongs to: ")
                primarystorage = input("Enter storage type (SSD, HDD, NVMe, etc): ")
                primarystoragecapacity = input("Enter primary storage capacity (250gb, 1 Tb, etc): ")
                secondarystorage = input("Enter secondary storage type: ")
                secondarystoragecapacity = input("Enter secondary storage capacity: ")
                cur.execute("INSERT INTO storage (laptop_id, primary_storage, primary_storage_capacity, secondary_storage, secondary_storage_capacity) VALUES (%s, %s, %s, %s, %s) RETURNING storage_id, laptop_id;", (laptop_id, primarystorage, primarystoragecapacity, secondarystorage, secondarystoragecapacity,))


            elif table_name == "Memory":
                laptop_id = input("Enter laptop ID this spec information belongs to: ")
                rammemory = input("Enter ram memory size (8, 16, 32, etc) in gb: ")
                cur.execute("INSERT INTO memory (laptop_id, ram_memory) VALUES (%s, %s) RETURNING memory_id, laptop_id;", (laptop_id, rammemory,))


            elif table_name == "Processor":
                laptop_id = input("Enter laptop ID this spec information belongs to: ")
                processorbrand = input("Enter processor brand name: ")
                processortier = input("Enter processor tier (i.e Ryzen 5, Ryzen 9, Intel i5, etc): ")
                numcores = input("Enter number of processor cores: ")
                numthreds = input("Enter number of processor threads: ")
                cur.execute("INSERT INTO processor (laptop_id, processor_brand, processor_tier, num_cores, num_threads) VALUES (%s, %s, %s, %s, %s) RETURNING processor_id, laptop_id;", (laptop_id, processorbrand, processortier, numcores, numthreds,))


            elif table_name == "Graphics":
                laptop_id = input("Enter laptop ID this spec information belongs to: ")
                gpubrand= input("Enter gpu brand name: ")
                gputype = input("Enter gpu type (i.e rtx 3060, rx5600XT, etc): ")
                cur.execute("INSERT INTO graphics (laptop_id, gpu_brand, gpu_type) VALUES (%s, %s, %s) RETURNING graphics_id, laptop_id;", (laptop_id, gpubrand, gputype,))


            elif table_name == "Product":
                laptop_id = input("Enter laptop ID this spec information belongs to: ")
                brand = input("Enter laptop brand name: ")
                price = input("Enter laptop price: ")
                rating = input("Enter laptop rating (Scale of 1 - 10): ")
                os = input("Enter Operating System currently running: ")
                yearOfwarranty = input("Enter the year the warranty ends (i.e 2023, 2024, etc): ")
                cur.execute("INSERT INTO product (laptop_id, brand, price, rating, os, year_of_warranty) VALUES (%s, %s, %s, %s, %s, %s) RETURNING product_id, laptop_id;", (laptop_id, brand, price, rating, os, yearOfwarranty,))

            laptop_id = cur.fetchone()[0]
            conn.commit()
            print(f"Data inserted successfully into {table_name} with ID {laptop_id}.")
    except Exception as e:
        print(f"An error occurred: {e}")
        conn.rollback()

# Function to delete a laptop record based on model name
def delete_data(conn):
    laptop_delete = input("Enter the laptop model to delete: ").strip()
    with conn.cursor() as cur:
        cur.execute("DELETE FROM laptop WHERE model ILIKE %s;", (laptop_delete,))
        conn.commit()
        print("If the laptop existed, it has been deleted.")

# Function to update a laptop's detail based on model/attribute name
def update_data(conn):
    laptop_update = input("Enter the laptop model to update: ").strip()
    spec_update = input("Enter the attribute you would like to update: ")
    new_detail = input("Enter the new detail for the laptop model (e.g., 'display_size=15.6'): ")
    with conn.cursor() as cur:
        cur.execute(f"UPDATE laptop SET {spec_update} = %s WHERE model ILIKE %s;", (new_detail, laptop_update))
        conn.commit()
        print("If the laptop existed, it has been updated.")

# Function to search data from a table based on user input
def search_data(conn):
    try:
        # Prompt the user for the laptop model to search for
        model_name = input("Enter the laptop model to search for: ")
        product_name = input("Enter brand name to search for:")

        # Create the SQL query, using ILIKE for case-insensitive search
        model_query = "SELECT * FROM Laptop WHERE model ILIKE %s;"
        product_query = "SELECT * FROM Product WHERE brand ILIKE %s;"
        
        if model_name:
            with conn.cursor() as cur:
                cur.execute(model_query, ('%' + model_name + '%',))
                rows = cur.fetchall()
                if rows:
                    for row in rows:
                        print(row)
                else:
                    print("No laptops found with the specified model.")
            conn.commit()

        if product_name:
            with conn.cursor() as cur:
                cur.execute(product_query, ('%' + product_name + '%',))
                rows = cur.fetchall()
                if rows:
                    for row in rows:
                        print(row)
                else:
                    print("No laptops found with the specified brand.")
            conn.commit()

    except Exception as e:
        print("An unexpected error occurred:", str(e))



# Function to perform an aggregate function on a table
def aggregate_functions(conn, table_name):
    with conn.cursor() as cur:
        try:
            # Prompt the user for the type of aggregation and the column name
            print("Available aggregate functions: SUM, AVG, COUNT, MIN, MAX")
            aggregate_function = input("Enter the aggregate function to use: ").strip().upper()
            column_name = input(f"Enter the column name to aggregate on in {table_name}: ").strip()

            # Validate aggregate function input
            if aggregate_function not in ['SUM', 'AVG', 'COUNT', 'MIN', 'MAX']:
                print("Invalid aggregate function.")
                return

            # If COUNT is selected, column name is not required
            if aggregate_function == 'COUNT':
                column_name = '*'

            query = f"SELECT {aggregate_function}({column_name}) FROM {table_name};"
            cur.execute(query)
            
            # Fetch and print the result
            result = cur.fetchone()
            if result:
                print(f"The {aggregate_function} of {column_name} in {table_name} is: {result[0]}")
            else:
                print(f"No data found to aggregate in {table_name}.")
        except Exception as e:
            print("Could not aggregate data, error occured")

def sorting(conn, table_name):
    column_name = input(f"Enter the column name you want to sort by in {table_name}: ").strip()
    order = input("Enter sort order (ASC or DESC): ").upper() or 'ASC'
    
    with conn.cursor() as cur:
        if column_name:  # If the user provided a column name, sort by that column.
            cur.execute(f"SELECT * FROM {table_name} ORDER BY {column_name} {order};")
        else:  # If no column name is provided, just fetch all data without sorting.
            cur.execute(f"SELECT * FROM {table_name};")
        
        rows = cur.fetchall()
        for row in rows:
            print(row)

def joins(conn):
    # Prompt the user for the necessary information
    print("Join operation selected.")
    table1 = input("Enter the name of the first table: ").strip()
    table1_key = "laptop_id"
    table2 = input("Enter the name of the second table: ").strip()
    table2_key = "laptop_id"
    join_type = input("Enter the type of join (INNER, LEFT, RIGHT): ").strip().upper()
    
    if join_type not in ["INNER", "LEFT", "RIGHT"]:
        print("Invalid join type. Defaulting to INNER JOIN.")
        join_type = "INNER"
    
    with conn.cursor() as cur:
        sql_query = f"SELECT * FROM {table1} {join_type} JOIN {table2} ON {table1}.{table1_key} = {table2}.{table2_key};"
        cur.execute(sql_query)
        rows = cur.fetchall()
        if rows:
            for row in rows:
                print(row)
        else:
            print("No results found for the join operation.")


def grouping(conn, table_name):
    column_name = input(f"Enter the column name to group by in {table_name}: ").strip()
    
    with conn.cursor() as cur:
        cur.execute(f"SELECT {column_name}, COUNT(*) FROM {table_name} GROUP BY {column_name};")
        rows = cur.fetchall()
        for row in rows:
            print(f"{column_name}: {row[0]}, Count: {row[1]}")

def subqueries(conn, table_name):
    table_name = input("Enter table name to group by: ").strip()
    table2_name = input("Enter same/another table to group with: ").strip()
    column_group = "laptop_id"
    column2_name = "laptop_id"
  
    with conn.cursor() as cur:
        cur.execute(f"SELECT * FROM {table_name} WHERE {column_group} IN (SELECT {column2_name} FROM {table2_name});")
        rows = cur.fetchall()
        for row in rows:
            print(row)

def transactions(conn):
    laptopsID_num = input("Enter the laptop ID to apply a discount on: ").strip()
    discount = Decimal(input("Enter a discount percent to apply to the laptop price: ").strip()) / 100
    with conn.cursor() as cur:
        try:
            conn.autocommit = False

            cur.execute("SELECT price FROM Product WHERE laptop_id = %s;", (laptopsID_num,))
            result = cur.fetchone()

            if result:
                current_price = Decimal(result[0])

                discount_price = current_price - (current_price * discount)

                cur.execute("UPDATE Product SET price = %s WHERE laptop_id = %s;", (discount_price, laptopsID_num))

                conn.commit()
                print(f"Discount has been applied successfully. They new price for laptop_id {laptopsID_num} is {discount_price}.")
            else:
                print("Laptop ID not found")
                conn.rollback()
        except Exception as error:
            conn.rollback()  # Rollback in case of error
            print("Transaction failed and has been rolled back.", error)
        finally:
            conn.autocommit = True  # End transaction

# Function to handle operations for a specific table
def table_operations(conn, table_name):
    while True:
        print(f"\nSelected table: {table_name}")
        print("Please select an option:")
        print("1. Insert Data")
        print("2. Delete Data")
        print("3. Update Data")
        print("4. Search Data")
        print("5. Aggregate Functions")
        print("6. Sorting")
        print("7. Joins")
        print("8. Grouping")
        print("9. Subqueiries")
        print("10. Transactions")
        print("11. Error Handling")
        print("12. Return to table selection")
        
        try:
            choice = int(input("Enter your choice (1-12): "))
        except ValueError:
            print("Please enter a valid number.")
            continue
        
        if choice == 1:
            insert_data(conn, table_name)
        elif choice == 2:
            delete_data(conn)
        elif choice == 3:
            update_data(conn)
        elif choice == 4:
            search_data(conn)
        elif choice == 5:
            aggregate_functions(conn, table_name)
        elif choice == 6:
            sorting(conn, table_name)
        elif choice == 7:
            joins(conn)
        elif choice == 8:
            grouping(conn, table_name)
        elif choice == 9:
            subqueries(conn, table_name)
        elif choice == 10:
            transactions(conn)
        elif choice == 11:
            aggregate_functions(conn, table_name)
        elif choice == 12:
            break
        else:
            print("Invalid choice, please try again.")

# Main function to run the CLI
def main():
    conn = connect_to_db()
    if conn is None:
        return
    
    while True:
        print("\nWelcome to the Database CLI Interface!")
        print("Which table would you like to operate on?")
        print("1. Laptop")
        print("2. Processor")
        print("3. Memory")
        print("4. Product")
        print("5. Graphics")
        print("6. Storage")
        print("7. Exit")

        try:
            table_choice = int(input("Enter your choice (1-7): "))
        except ValueError:
            print("Please enter a valid number.")
            continue
        
        if table_choice == 1:
            table_operations(conn, "Laptop")
        elif table_choice == 2:
            table_operations(conn, "Processor")
        elif table_choice == 3:
            table_operations(conn, "Memory")
        elif table_choice == 4:
            table_operations(conn, "Product")
        elif table_choice == 5:
            table_operations(conn, "Graphics")
        elif table_choice == 6:
            table_operations(conn, "Storage")
        elif table_choice == 7:
            print("Exiting the program.")
            break
        else:
            print("Invalid choice, please try again.")

    conn.close()

if __name__ == "__main__":
    main()
