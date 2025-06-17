import csv
import smtplib
from email.message import EmailMessage
from flask import Flask, render_template, request, redirect

app = Flask('__name__')


@app.route('/')
@app.route('/index.html')
def main():
    return render_template('index.html')


@app.route('/submit_form', methods=['POST'])
def submit():
    # gets all 3 items entered in a form ordered the same as on website top to bottom to a list
    inputs = list(request.form.to_dict().values())
    sender = inputs[0]
    subject = inputs[1]
    content = inputs[2]
    with open('data.csv', 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow([sender, subject, content])

    send_email(sender, subject, content)
    return redirect('/thankyou.html')


@app.route('/<path:page>.html')
def static_page(page):
    if page in ['about', 'components', 'contact', 'index', 'thankyou', 'work', 'works']:
        return render_template(f'{page}.html')
    return render_template('404.html'), 404


def send_email(sender, subject, content):
    email = EmailMessage()
    email['from'] = sender
    email['to'] = ['jan.tomov@gmail.com']
    email['subject'] = subject
    content = content + f'\n\n\nThis email was sent by {sender}'
    email.set_content(content)
    with smtplib.SMTP(host='smtp.gmail.com', port=587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login('jan.tomov24@gmail.com', 'alri pixt gcpg vtny')
        smtp.send_message(email)
        return True
