Cameron Burke
CMPSC 431W
Final Project CLI

Instructions to Install PostgreSQL:
Please navigate to the official PostgreSQL site and install the download specific to your OS.
	--Link: https://www.postgresql.org/download/

During installation you will be prompted to create a password for the standard postgres account, please create a secure password as you will use this to login. 

Once installed, you will need to reboot your machine as this will enable the start of the postgresql service on boot. If this does not start the service, you will need to start the service manually by entering the command, 
net start postgresql-x64-xx (the “xx” being the specific version number you have installed). 
You can find the version number by typing in the command;
	--psql –version
and this will then print out the version of PostgreSQL you have installed.

After you start the service, you can then run the command;
	--psql -U postgres (Do not include: standard user account)
	--password: (Set during PostgreSQL installation)
		or
	--psql -U (your user account created during installation)
	--password: (Set during installation)
 
After, you will have successfully started the PostgreSQL software terminal and are now able to connect to a database and run queries. 
In the case of this project, please create a database called, “laptops2024”. 
You can do this by running the command;
	--CREATE DATABASE laptops2024;
and this will create the database. 

You can run the following commands to connect to see if the database is present and connect to it;
	--\list                                                (Do not write: lists all databases on the PostgreSQL directory)
	--\c laptops2024                        (Connects to the laptops2024 database)

You can now run queries directly or through the CLI python file. 

Before running the python files use a PostgreSQL adapter that allows the connection to the PostgreSQL database. This package will need to be installed on the machine for the code to work properly. 
First you will need to install python from their official site, https://www.python.org/downloads/. 
Once installed run the command;
		--pip install psycopg2  (“pip” package installed is installed usually with python)

To run the python file, please place the file in any directory, open a terminal, navigate to the directory the file is stored in and run the command below;
	--python CB-FinalProject.py  (Please make sure you have python installed beforehand)

Now the CLI should work properly as well as the PostgreSQL database. Please continue to the README.txt.










README for CMPSC 431W Final Project
This CLI (Command-Line Interface) application is designed to manage a PostgreSQL database for a system that handles laptop specifications and product details. Each function within the CLI provides a specific operation for interacting with the database, allowing users to insert, delete, update, search, and perform various other data manipulations.

Below is a description of the functions within the CLI programming:

connect_to_db()
Establishes a connection to the PostgreSQL database using given credentials. It returns a connection object if successful, or None if an error occurs.

insert_data(conn, table_name)
Allows users to insert new records into a specified table. Depending on the table selected, the function will prompt the user for the relevant data needed to create a new record within the table.

delete_data(conn)
Removes a record from the laptop table based on a model name provided by the user. This function will delete the record if it exists.

update_data(conn)
Updates details of a laptop record based on the model name. The user can specify which attribute to update and the new value for that attribute. (Model name must be specific as a general name would be unsafe and not promote the integrity of the data.) 

            --Example
                       Deleting data with the model name "mac" where multiple records could have "mac" in their model name such as "Macbook Pro, iMac, etc". Thus a specific model name must be entered.

search_data(conn)
Enables users to find records in the database based on certain criteria. Users can search for laptop models or products by brand name.

aggregate_functions(conn, table_name)
Performs aggregate calculations, such as sum, average, count, minimum, and maximum, on a specified column within a table. It will prompt the user for the type of aggregation and the column to perform it on.

sorting(conn, table_name)
Sorts the results of a query based on a specified column. Users can choose the column and order (ASC or DESC) for sorting.

joins(conn)
Combines data from multiple tables using relationships defined between them. Users can perform inner, left, or right joins by specifying the tables and the type of join.

grouping(conn, table_name)
Groups query results based on a specified column. This function will prompt the user for the column to group by.

subqueries(conn, table_name)
Supports nested operations within queries, allowing for explicit data retrieval.

transactions(conn)
Handles transactions to ensure the consistency and reliability of database operations. It includes functionality for applying discounts to laptop prices and ensures changes are committed or rolled back appropriately.

table_operations(conn, table_name)
Acts as the central hub for interacting with specific tables. It loops through options allowing users to choose which operation to perform on the selected table.

main()
The entry point of the CLI application. It initiates a connection to the database and presents a menu for the user to choose which table to operate on or exit the program.

Each function is designed with error handling to ensure that any issues during the operation do not affect the stability of the database and are communicated clearly to the user.

Sources + Video:

https://github.com/cfb5473/CMPSC431W-FinalProject.git

Github: git@github.com:cfb5473/CMPSC431W-FinalProject.git

Video:
https://psu.mediaspace.kaltura.com/media/Screen%20Recording%20-%20Fri%20Apr%2026%202024%2019%3A24%3A46%20GMT-0400%20(Eastern%20Daylight%20Time)/1_51v2r56s

