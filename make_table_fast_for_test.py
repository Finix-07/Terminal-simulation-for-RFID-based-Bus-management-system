import mysql.connector as msc
import config

# Establish connection to the database
def establish_connection():
    try:
        cnx = msc.connect(user=config.SQL_USER, password=config.SQL_PASS,
                          host=config.SQL_HOST, database=config.SQL_DATABASE)
        return cnx
    except msc.Error as err:
        print(f"Error: {err}")
        return None

# Function to add a student
def add_student(roll_no, name, branch, uid, phone_no, email):
    cnx = establish_connection()
    if cnx is None:
        print("Failed to connect to the database.")
        return

    cursor = cnx.cursor()
    query = ("INSERT INTO student (roll_no, name, branch, uid, phone_no, email) "
             "VALUES (%s, %s, %s, %s, %s, %s)")

    data = (roll_no, name, branch, uid, phone_no, email)

    try:
        cursor.execute(query, data)
        cnx.commit()
        print(f"Added student: {name}")
    except msc.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        cnx.close()

def main():
    roll_no = int(input("Enter Roll No: "))
    name = input("Enter Name: ")
    branch = input("Enter Branch: ")
    uid = int(input("Enter UID: "))
    phone_no = (input("Enter Phone No: "))
    email = input("Enter Email: ")

    add_student(roll_no, name, branch, uid, phone_no, email)

if __name__ == "__main__":
    main()
