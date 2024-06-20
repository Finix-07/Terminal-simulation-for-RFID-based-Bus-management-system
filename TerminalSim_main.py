import config
import mysql.connector as msc
import smtplib
from email.message import EmailMessage
import random
import csv
import time
import os
import customtkinter as ct
import serial
import threading
import queue

capacity = 5
curr_time = time.time()
start_time = time.ctime(curr_time)

EMAIL_ID = config.EMAIL_USER
EMAIL_PASS = config.EMAIL_PASSWORD
SQLUSER = config.SQL_USER
SQLPASS = config.SQL_PASS
SQLHOST = config.SQL_HOST
SQLDATABASE = config.SQL_DATABASE
TransportDeptEmail = config.Transport_Dept_Email
class people():
    def __init__(self, name, uid, branch, rollno, phoneno, email):
        self.name = name
        self.uid = uid
        self.branch = branch
        self.rollno = rollno
        self.phoneno = phoneno
        self.email = email

def encrypt_uid(uid):
    temp=''
    while uid > 0:
        temp += str((uid%10)+random.randint(0,9-(uid%10)))
        temp = temp[::-1]
        uid = uid//10

    return int(temp)

def establish_connection():
    try:
        cnx = msc.connect(user = SQLUSER, password = SQLPASS,
                        host = SQLHOST,
                        database = SQLDATABASE)

    except msc.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your username or password....")
        elif err.errno == errorcorde.ER_BAD_DB_ERROR:
            print("Database does not exist....")
        else:
            print(err)

    return cnx

def send_email_with_otp(subject, From , to):
    with smtplib.SMTP('smtp.gmail.com',587) as smtp: #server we connecting to
        smtp.ehlo() #both server connect with this
        smtp.starttls() #an encrypted communication
        smtp.ehlo() #now connect with this encrypted server


        smtp.login(EMAIL_ID, EMAIL_PASS) #login to service

        msg = EmailMessage() #create object of the class
        msg['Subject'] = f'{subject}'
        msg['From'] = f'{From}'
        msg['To'] = f'{to}'
        otp = random.randint(1000,9999)
        body_data = f'Your OTP for the Updation of UID is {otp}'
        msg.set_content(body_data)
        smtp.send_message(msg)
        return otp

def send_email_with_list(subject, From , to):
    with smtplib.SMTP('smtp.gmail.com',587) as smtp: #server we connecting to
        smtp.ehlo() #both server connect with this
        smtp.starttls() #an encrypted communication
        smtp.ehlo() #now connect with this encrypted server


        smtp.login(EMAIL_ID, EMAIL_PASS) #login to service

        msg = EmailMessage() #create object of the class
        msg['Subject'] = subject
        msg['From'] = From
        msg['To'] = to
        with open("travel_list.csv",'rb') as f:
            data = f.read()
            file_name = os.path.basename("travel_list.csv")
            msg.add_attachment(data, maintype='application', subtype="octet-stream", filename=file_name )

        smtp.send_message(msg) #sends the message with the given parameters


def main():
    global capacity
    ct.set_appearance_mode("Dark")
    ct.set_default_color_theme("blue")

    app = ct.CTk()
    app.geometry("400x240")
    app.title("RFID SYSTEM")
    label = ct.CTkLabel(master=app, text="Waiting for Master Card", font=("Helvetica", 32))
    label.place(relx=0.5, rely=0.5, anchor="center")

    input_queue = queue.Queue()

    def register_passenger():
        f = open("travel_list.csv", 'w',newline='')
        writer = csv.writer(f)
        connection = establish_connection()
        cursor = connection.cursor()
        master_key = 777777777

        print("Welcome! To begin the journey, place the master card....")
        scanned_id = int(input("Enter Master UID: "))
        writer.writerow(["rollno", "name", "branch", "phoneno", "email", "passenger_uid", "time"])

        if scanned_id == master_key:
            passenger_uid = 0
            count = 0
            while passenger_uid != master_key:
                display_text =f"Waiting for Passenger {count+1}"
                label.configure(text=display_text)

                passenger_uid = int(input("Enter UID: "))
                if passenger_uid == master_key:
                    break
                passenger_roll = int(input("Enter Roll No. "))
                query1 = 'SELECT * FROM student WHERE roll_no = %s'
                query2 = 'SELECT * FROM student WHERE uid = %s'

                cursor.execute(query1, (passenger_roll,))
                # connection.commit()
                record1 = cursor.fetchone()


                cursor.execute(query2, (passenger_uid,))
                # connection.commit()
                record2 = cursor.fetchone()
                # print(record1)
                # print(record2)

                if record1 == record2:
                    p1 = people(record1[1], encrypt_uid(passenger_uid), record1[2], record1[0], record1[4], record1[5])
                    writer.writerow([p1.rollno, p1.name, p1.branch, p1.phoneno, p1.email, p1.uid, time.ctime(time.time())])
                    display_text = f"Waiting for Passenger {count + 1}"
                    label.after(100,lambda: label.configure(text=f"Passenger Authenticated Succefully!\n\nName: {p1.name}\nBranch: {p1.branch}\nRoll No.: {p1.rollno}\nPhone No.: {p1.phoneno}\nEmail: {p1.email}"))
                    count+=1
                    label.after(3000, lambda: label.configure(text=display_text))

                elif not record2:
                    p1 = people(record1[1], encrypt_uid(passenger_uid), record1[2], record1[0], record1[4], record1[5])
                    query = 'UPDATE student SET uid = %s WHERE roll_no = %s'
                    otp = send_email_with_otp("OTP TO UPDATE UID", EMAIL_ID, p1.email)
                    otp_check = int(input("Enter your otp received on mail...  \n"))
                    label.configure(text="Waiting for OTP")
                    if otp_check == otp:
                        writer.writerow([p1.rollno, p1.name, p1.branch, p1.phoneno, p1.email, passenger_uid,
                                         time.ctime(time.time())])
                        display_text = f"Waiting for Passenger {count + 1}"
                        label.after(100, lambda: label.configure(
                            text=f"Passenger Authenticated Succefully!\n\nName: {p1.name}\nBranch: {p1.branch}\nRoll No.: {p1.rollno}\nPhone No.: {p1.phoneno}\nEmail: {p1.email}"))
                        count += 1
                        label.after(3000, lambda: label.configure(text=display_text))
                    else:
                        print("Invalid otp entered...")
                    cursor.execute(query, (passenger_uid, passenger_roll))
                    connection.commit()
                elif not record1:
                    print("No student of this roll No. is present.... kindly contact the Transport Department")
                else:
                    print("Mismatch try again....")


            curr_time = time.time()
            end_time = time.ctime(curr_time)
            f.close()
            time.sleep(2)
            send_email_with_list(f"List of passengers travelling from {start_time} to {end_time}", EMAIL_ID,
                                 f'{TransportDeptEmail}')
            print("Email successfully sent!!!")

        else:
            print("Invalid Master UID.... Restart the program.")
            label.configure(text="Invalid Master UID....\nRestart the program.")
            app.after(3000, app.destroy)
            return
        label.configure(text="Thank you for traveling with us.\nThe bus journey has come to an end.\nMove to exit the doors open in 5 seconds.")
    # After the completion of register_passenger(), schedule the window to close after 4 seconds
        app.after(5000, app.destroy)
    def input_thread():
        threading.Thread(target=register_passenger, daemon=True).start()

    def update_label():
        if not input_queue.empty():
            display_text = input_queue.get()
            label.configure(text=f"Waiting for Passenger {display_text}")
            animate_dot(f"Waiting for Passenger {display_text}")
        app.after(100, update_label)

    input_thread()
    app.mainloop()

if __name__ == "__main__":
    main()