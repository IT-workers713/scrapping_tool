import time

import requests
import selectorlib
import smtplib, ssl
import os
import sqlite3





Url = "https://programmer100.pythonanywhere.com/tours/"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

connection  = sqlite3.connect("identifier.sqlite")


def scrape(url):
    response = requests.get(url,headers=HEADERS)
    source = response.text
    return source

def extract(source):
    ext=selectorlib.Extractor.from_yaml_file("extract.yaml")
    value = ext.extract(source)["tours"]
    return value

def send_email(message):
    host = "smtp.gmail.com"
    port = 465

    username = "app8flask@gmail.com"
    password = "here_goes_your_gmail_password"

    receiver = "rayehriad99@gmail.com"
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(host, port, context=context) as server:
        server.login(username, password)
        server.sendmail(username, receiver, message)

def store(exctred):
    row = exctred.split(",")
    row = [item.strip() for item in row]
    cursor = connection.cursor()
    cursor.execute("INSERT INTO events VALUES(?,?,?)",row)
    connection.commit()
def read(exctred):
    row = exctred.split(",")
    row = [item.strip() for item in row]
    band,city,date=row
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM events WHERE band=? AND city=? AND date=?")

    rows = cursor.fetchall()
    print(rows)
    return rows


if __name__ == "__main__":
    while True:

        scraped=scrape(Url)
        exctred = extract(scraped)
        print(exctred)


        if exctred != "No upcoming tours":
            row = read(exctred)
            if not row:
                store(exctred)
                #send_email(message="salut")
        time.sleep(2)