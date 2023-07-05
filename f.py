import sqlite3
import smtplib

# Set up SQLite database connection
conn = sqlite3.connect('db.sqlite')
cursor = conn.cursor()

# Execute the SQL query to retrieve email addresses
cursor.execute("SELECT email FROM users")
email_list = cursor.fetchall()

# Set up email sending
smtp_server = 'your_smtp_server'
smtp_port = 587
sender_email = 'your_email@example.com'
password = 'your_password'

# Iterate through email addresses and send emails
for email in email_list:
    # Compose the email message
    message = f"Subject: Your Subject\r\n\r\nYour email content here."

    # Send the email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, email[0], message)

# Close the database connection
conn.close()
