import smtplib

my_email = "shinpythoncode@gmail.com"
password = "Shin100daysofcode"

with smtplib.SMTP("smtp.gmail.com") as connection:
    connection.starttls()
    connection.login(user=my_email, password=password)
    connection.sendmail(
        from_addr=my_email,
        to_addrs="shin.yagami@hotmail.com",
        msg="Subject:HELLO\n\nThis is testing messages"
    )

import datetime
