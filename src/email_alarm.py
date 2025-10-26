import smtplib
from email.mime.text import MIMEText
import os
import time

def send_alarm_email(
    subject="Watch Dog Alarm",
    content="Somebody enter my home!",
    smtp_host=None,
    smtp_port=587,
    username=None,
    password=None,
    sender=None,
    receivers=None
):
    """
    发送报警邮件
    
    Args:
        subject (str): 邮件主题
        content (str): 邮件内容
        smtp_host (str): SMTP服务器地址
        smtp_port (int): SMTP端口号
        username (str): 邮箱用户名
        password (str): 邮箱密码
        sender (str): 发送者邮箱
        receivers (list): 接收者邮箱列表
    
    Returns:
        bool: 发送成功返回True，否则返回False
    """
    # 从环境变量获取配置
    smtp_host = smtp_host or os.environ.get('MAIL_HOST')
    username = username or os.environ.get('MAIL_USER')
    password = password or os.environ.get('MAIL_PASS')
    sender = sender or os.environ.get('SENDER')
    receivers = receivers or (os.environ.get('RECEIVERS').split(',') if os.environ.get('RECEIVERS') else None)
    
    # 检查必要配置是否存在
    if not all([smtp_host, username, password, sender]):
        print('Email configuration is incomplete. Please set all required environment variables.')
        return False
    
    if not receivers:
        print('No receivers configured. Please set RECEIVERS environment variable.')
        return False
    
    # 创建邮件内容
    message = MIMEText(content, 'plain', 'utf-8')
    message['Subject'] = subject
    message['From'] = sender
    message['To'] = receivers[0]

    try:
        # 使用更安全的连接方式
        smtpObj = smtplib.SMTP(smtp_host, smtp_port, timeout=30)
        smtpObj.starttls()  # 启用TLS加密
        smtpObj.login(username, password)
        smtpObj.sendmail(sender, receivers, message.as_string())
        smtpObj.quit()
        print('Email sent successfully')
        return True
    except smtplib.SMTPException as e:
        print(f'SMTP error: {e}')
        return False
    except Exception as e:
        print(f'Error sending email: {e}')
        return False


def main():
    """主函数 - 用于测试邮件发送功能"""
    print("Sending test alarm email...")
    success = send_alarm_email()
    if success:
        print("Test email sent successfully!")
    else:
        print("Failed to send test email.")


if __name__ == "__main__":
    main()