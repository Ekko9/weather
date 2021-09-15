import smtplib
from email.mime.text import MIMEText
from weather_utils import get_weather_li
from get_city import get_CityName


mailto_list = ["keep1024@sina.com", "alan.fu@ucloud.cn", "seunie.fan@ucloud.cn"]
mail_host = "smtp.sina.cn"  # 设置服务器
mail_user = "keep1024@sina.com"    # 用户名
mail_pass = "Fu18339800770@"   # 口令


def html_table(lol):
    html_str = "<table>"
    for sub in lol:
        html_str += '<tr><td>'
        html_str += '</td><td>'.join(sub)
        html_str += '</td></tr>'
    html_str += "</table>"
    return html_str


def send_mail(to_list, sub, content):     # 定义一个函数，收件人、标题、邮件内容
    me = "keep1024@sina.com"+"<"+mail_user+">"   # 发件人定义,这里要和认证帐号一致才行的
    msg = MIMEText(content, _subtype='html', _charset='utf-8')  # 这里看email模块的说明，这里构造内容
    msg['Subject'] = sub
    msg['From'] = me
    msg['To'] = ",".join(mailto_list)
    try:
        server = smtplib.SMTP()
        server.connect(mail_host)
        server.login(mail_user, mail_pass)
        server.sendmail(me, to_list, msg.as_string())
        server.close()
        return True
    except Exception as e:
        print(str(e))
        return False


if __name__ == '__main__':
    count = html_table(get_weather_li())
    if send_mail(mailto_list, get_CityName() + "天气", count):
        print("发送成功")
    else:
        print("发送失败")
