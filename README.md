# Terminal simulation for RFID based Bus management system

(still pending for futher development)

This project is a part of our 2nd-semester project, aiming to simulate RFID input via terminal and display updates in a GUI for managing our college bus transportation.

## Features

- **RFID Simulation**: Simulate RFID card inputs through the terminal.
- **GUI Updates**: Display real-time updates in a graphical user interface using `customtkinter`.
- **Email Notifications**: Send OTP (to user's main) and/or passenger list(on transport department) emails using SMTP.
- **Database Integration**: Connect to MySQL database to fetch and update student details.
- **Secure UID Encryption**: Encrypt user IDs for secure storage and transmission.

## Technologies Used

- **Python**: Core programming language.
- **customtkinter**: For building the graphical user interface.
- **MySQL Connector**: To establish and interact with the MySQL database.
- **smtplib**: For sending emails.
- **serial**: To handle serial communication.
- **queue and threading**: For managing concurrent operations.

## Class and Function Overview

- **`people` Class**: Stores details of each passenger.
- **`encrypt_uid(uid)` Function**: Encrypts the UID for secure handling.
- **`establish_connection()` Function**: Establishes a connection to the MySQL database.
- **`send_email_with_otp(subject, From, to)` Function**: Sends an OTP email for UID updates.
- **`send_email_with_list(subject, From, to)` Function**: Sends the list of passengers as an email attachment.
- **`main()` Function**: Orchestrates the RFID simulation, GUI updates, and email notifications.
