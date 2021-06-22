import smtplib
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart

"""
qq邮箱的smtp服务器地址：smtp.qq.com,端口：465
163邮箱的smtp服务器地址：smtp.163.com，端口：465 （25）
"""

# =============================邮件只有正文=============================
# 第一步：连接smtp服务器，并登录
# 连接到smtp服务器
smtp = smtplib.SMTP_SSL(host="smtp.qq.com", port=465)
# 登录smtp服务器（邮箱账号和授权码进行登录，注意：不是邮箱的密码）
smtp.login(user="musen_nmb@qq.com", password="algmmzptupjccbab")

# 第二步：构造一封邮件
msg = MIMEText("邮件正文", _charset="utf-8")
msg["Subject"] = "邮件主题"
msg["To"] = "920219832@qq.com"
# msg["To"] = '"920219832@qq.com", "920219831@qq.com"'
msg["From"] = "musen_nmb@qq.com"

# 第三步：发送邮件
smtp.send_message(msg, from_addr="musen_nmb@qq.com", to_addrs="920219832@qq.com")
# smtp.send_message(msg, from_addr="musen_nmb@qq.com", to_addrs=["920219832@qq.com", "920219831@qq.com"])

# =============================邮件只有正文=============================

#
#
#

# =============================邮件带附件=============================
# 第一步：连接smtp服务器，并登录
smtp = smtplib.SMTP_SSL(host="smtp.qq.com", port=465)
smtp.login(user="musen_nmb@qq.com", password="algmmzptupjccbab")

# 第二步：构造一封多组件邮件
msg = MIMEMultipart()
msg["Subject"] = "邮件主题"
msg["To"] = "920219832@qq.com"
msg["From"] = "musen_nmb@qq.com"

# 构建邮件的文本内容
text = MIMEText("邮件正文", _charset="utf-8")
msg.attach(text)

# 构造邮件的附件
with open(r"C:\project\report.html", "rb") as f:
    content = f.read()
report = MIMEApplication(content)
report.add_header('content-disposition', 'attachment', filename='report.html')
msg.attach(report)

# 第三步：发送邮件
smtp.send_message(msg, from_addr="musen_nmb@qq.com", to_addrs=["920219832@qq.com"])
# =============================邮件带附件=============================
