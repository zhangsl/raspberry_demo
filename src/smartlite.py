import RPi.GPIO as GPIO
import time
import os

# 配置参数
LIGHT_SENSOR_PIN = 3
DETECTION_INTERVAL = 3  # 检测间隔(秒)
GPIO_MODE = GPIO.BCM    # 统一使用BCM模式

def setup_gpio():
    """初始化GPIO设置"""
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO_MODE)
    GPIO.setup(LIGHT_SENSOR_PIN, GPIO.IN)


def detect_light_change():
    """检测光线变化"""
    try:
        while True:
            curtime = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))
            if GPIO.input(LIGHT_SENSOR_PIN):
                alert(curtime)
            # 移除了不必要的else: continue语句
            time.sleep(DETECTION_INTERVAL)
    except KeyboardInterrupt:
        print("\nLight detection interrupted by user.")
    except Exception as e:
        print(f"Error in light detection: {e}")


def alert(timestamp):
    """报警函数"""
    print(f"{timestamp} Someone is coming!")


def main():
    """主函数"""
    try:
        setup_gpio()
        print("Light detection started. Press Ctrl+C to exit.")
        time.sleep(2)  # 短暂延迟后再开始检测
        detect_light_change()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        GPIO.cleanup()
        print("GPIO cleanup completed.")


if __name__ == "__main__":
    main()