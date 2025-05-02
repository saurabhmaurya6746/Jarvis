import sqlite3
import os
import csv
con = sqlite3.connect("jarvis.db")
cursor = con.cursor()

# create a table sys_command 

# query = "CREATE TABLE IF NOT EXISTS sys_command(id integer primary key, name VARCHAR(100), path VARCHAR(1000))"
# cursor.execute(query)

# query = "INSERT INTO web_command VALUES (null,'gmail', 'C:\\Program Files\\Microsoft Office\\root\\Office16\\ONENOTE.exe')"
# cursor.execute(query)
# con.commit()

# create a table web_command
# query = "CREATE TABLE IF NOT EXISTS pdf_files(id integer primary key autoincrement, file_name TEXT NOT NULL  )"
# cursor.execute(query)
# pdf_files = [
#     "debug.pdf",
#     "debugging main.pdf",
#     "debugging.pdf",
#     "even.pdf",
#     "final.pdf",
#     "poster.pdf"
# ]
# for pdf in pdf_files:
# cursor.execute("INSERT OR IGNORE INTO pdf_files (file_name) VALUES (?)", ('nodal.pdf',))
# cursor.execute('delete from pdf_files where file_name="debug.pdf"')

# # Create a table with the desired columns
# cursor.execute('''CREATE TABLE IF NOT EXISTS contacts (id integer primary key, name VARCHAR(200), mobile_no VARCHAR(255), email VARCHAR(255) NULL)''')


# Example: Importing the 1st and 3rd columns
# desired_columns_indices = [0, 18]

# # Read data from CSV and insert into SQLite table for the desired columns
# with open('contacts.csv', 'r', encoding='utf-8') as csvfile:
#     csvreader = csv.reader(csvfile)
#     for row in csvreader:
#         selected_data = [row[i] for i in desired_columns_indices]
#         cursor.execute(''' INSERT INTO contacts (id, 'name', 'mobile_no') VALUES (null, ?, ?);''', tuple(selected_data))

#### 4. Insert Single contacts (Optional)
query = "INSERT INTO contacts VALUES (null,'harsh mishra', '8090730048','null')"
# query="delete from pdf_files where file_name='final.pdf'"
cursor.execute(query)

#### 5. Search Contacts from database

# query = 'shagun'
# query = query.strip().lower()

# cursor.execute("SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", ('%' + query + '%', query + '%'))
# results = cursor.fetchall()
# print(results[0][0])

# 
# drop table 
# cursor.execute('drop table pdf_files')
# # query = "INSERT INTO saurabh VALUES (null,'jiocinema', 'https://www.jiocinema.com/')"
# # query='drop table saurabh'
# cursor.execute(query)
# con.commit()

# # testing module
# app_name = "android studio"
# cursor.execute('SELECT path FROM sys_command WHERE name IN (?)', (app_name,))
# results = cursor.fetchall()
# print(results[0][0])


# testing for all pdf are stored 
# List all available PDFs
def list_pdfs():
    cursor.execute("SELECT file_name FROM pdf_files")
    rows = cursor.fetchall()
    print("\nAvailable PDFs:")
    for row in rows:
        print(f"- {row[0]}")
list_pdfs()  # Show all available PDFs

# Function to search for a PDF
 

# def search_pdf_by_name(file_name ):
#     try:
#         search_name =  file_name
#         search_name += ".pdf"  # Append ".pdf" to the search term

#         # Search the database
#         cursor.execute("SELECT file_name FROM pdf_files WHERE file_name = ?", (search_name,))
#         result = cursor.fetchone()

#         if result:
#             print(f"Found '{result[0]}'. Opening...")
#             os.startfile(result[0])  # Ensure this path is correct
#         else:
#             print("PDF not found in the database.")
#     except Exception as e:
#         print(f"An error occurred: {e}")
#     finally:
#         # Close the connection
#         con.close()

# # Example usage
# def process_query(query):
#     query = query.lower()
#     if "open" in query and "search" in query:
#         file_start = query.find("open") + 5
#         file_end = query.find("pdf")
#         file_name = query[file_start:file_end].strip()

#         search_start = query.find("search") + 7
#         search_word = query[search_start:].strip()

#         return file_name, search_word
#     else:
#         return None, None
# query='open poster pdf and search event'
# file_name, search_word= process_query(query)
# search_pdf_by_name(file_name)


con.commit()
con.close()