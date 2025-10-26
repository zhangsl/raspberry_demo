import time
import RPi.GPIO as GPIO
import smtplib
from email.mime.text import MIMEText
import os

# 配置参数
BODY_GPIO = 18
DETECTION_INTERVAL = 6  # 检测间隔(秒)
ALARM_COOLDOWN = 60     # 报警冷却时间(秒)

# 邮件配置(从环境变量读取)
def get_email_config():
    return {
        'mail_host': os.environ.get('MAIL_HOST'),
        'mail_user': os.environ.get('MAIL_USER'),
        'mail_pass': os.environ.get('MAIL_PASS'),
        'sender': os.environ.get('SENDER'),
        'receivers': os.environ.get('RECEIVERS', '').split(',') if os.environ.get('RECEIVERS') else []
    }

# 全局变量
last_alarm_time = 0


def setup_gpio():
    """初始化GPIO设置"""
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BODY_GPIO, GPIO.IN)


def body_detect():
    """检测人体活动"""
    signal = GPIO.input(BODY_GPIO)
    if signal == 1:
        print("YES!")
        return True
    else:
        print("NO!")
        return False


def send_email():
    """发送报警邮件"""
    global last_alarm_time
    
    # 检查冷却时间
    current_time = time.time()
    if current_time - last_alarm_time < ALARM_COOLDOWN:
        print("Alarm is in cooldown period.")
        return
    
    message = MIMEText('Somebody enter my home!', 'plain', 'utf-8')
    message['Subject'] = 'Watch Dog Alarm'
    message['From'] = sender
    message['To'] = receivers[0]

    try:
        # 获取邮件配置
        email_config = get_email_config()
        
        # 检查必要配置是否存在
        if not all([email_config['mail_host'], email_config['mail_user'], email_config['mail_pass'], email_config['sender']]):
            print('Email configuration is incomplete. Please set all required environment variables.')
            return
        
        if not email_config['receivers']:
            print('No receivers configured. Please set RECEIVERS environment variable.')
            return
        
        # 使用更安全的连接方式
        smtpObj = smtplib.SMTP(email_config['mail_host'], 587, timeout=30)
        smtpObj.starttls()  # 启用TLS加密
        smtpObj.login(email_config['mail_user'], email_config['mail_pass'])
        smtpObj.sendmail(email_config['sender'], email_config['receivers'], message.as_string())
        smtpObj.quit()
        print('Email sent successfully')
        last_alarm_time = current_time
    except smtplib.SMTPException as e:
        print(f'SMTP error: {e}')
    except Exception as e:
        print(f'Error sending email: {e}')


def main():
    """主函数"""
    try:
        setup_gpio()
        print("Body detection started. Press Ctrl+C to exit.")
        
        while True:
            if body_detect():
                send_email()
            time.sleep(DETECTION_INTERVAL)
    except KeyboardInterrupt:
        print("\nProgram interrupted by user.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        GPIO.cleanup()
        print("GPIO cleanup completed.")


if __name__ == "__main__":
    main()