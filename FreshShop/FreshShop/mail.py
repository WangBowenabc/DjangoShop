import smtplib
from email.mime.text import MIMEText

subject = "我的学习邮件"
content = "1234"
sender = "1076680849@qq.com"
recver = """2261118049@qq.com,
18732650529@163.com,
597590747@qq.com"""
password = "jcwpywllmbvabach"
message = MIMEText(content, "plain", "utf-8")
message['Subject'] = subject
message["To"] = recver
message["From"] = sender

smtp = smtplib.SMTP_SSL("smtp.qq.com",465)
smtp.login(sender, password)
smtp.sendmail(sender, recver.split(",\n"), message.as_string())
smtp.close()