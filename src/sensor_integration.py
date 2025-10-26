import time
import RPi.GPIO as GPIO
import logging
import os
from datetime import datetime


# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('sensor_detection.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# 配置参数
BODY_GPIO = 18      # 人体传感器GPIO引脚
COLLISION_GPIO = 4  # 碰撞传感器GPIO引脚
BUZZER_GPIO = 17    # 蜂鸣器GPIO引脚
LED_GPIO = 23       # LED GPIO引脚
DETECTION_INTERVAL = 1  # 检测间隔(秒)


class SensorDetector:
    def __init__(self):
        """初始化传感器检测器"""
        self.setup_gpio()
        self.buzzer_on = False  # 蜂鸣器状态标志
    
    def setup_gpio(self):
        """初始化GPIO设置"""
        try:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(BODY_GPIO, GPIO.IN)
            GPIO.setup(COLLISION_GPIO, GPIO.IN)
            GPIO.setup(BUZZER_GPIO, GPIO.OUT)
            GPIO.setup(LED_GPIO, GPIO.OUT)
            
            # 初始化输出为低电平
            GPIO.output(BUZZER_GPIO, GPIO.LOW)
            GPIO.output(LED_GPIO, GPIO.LOW)
            
            logger.info(f"GPIO {BODY_GPIO} (人体传感器) 初始化成功")
            logger.info(f"GPIO {COLLISION_GPIO} (碰撞传感器) 初始化成功")
            logger.info(f"GPIO {BUZZER_GPIO} (蜂鸣器) 初始化成功")
            logger.info(f"GPIO {LED_GPIO} (LED) 初始化成功")
        except Exception as e:
            logger.error(f"GPIO 初始化失败: {e}")
            raise
    
    def detect_body(self):
        """
        检测人体活动
        
        Returns:
            bool: True表示检测到人体，False表示无人体
        """
        try:
            signal = GPIO.input(BODY_GPIO)
            return signal == 1
        except Exception as e:
            logger.error(f"检测人体时出错: {e}")
            return False
    
    def detect_collision(self):
        """
        检测碰撞/障碍物
        
        Returns:
            bool: True表示检测到障碍物，False表示无障碍物
        """
        try:
            # 红外避障传感器检测到障碍物时输出低电平（0）
            signal = GPIO.input(COLLISION_GPIO)
            return signal == 0
        except Exception as e:
            logger.error(f"检测碰撞时出错: {e}")
            return False
    
    def set_buzzer(self, state):
        """
        设置蜂鸣器状态
        
        Args:
            state (bool): True表示开启蜂鸣器，False表示关闭蜂鸣器
        """
        try:
            if state != self.buzzer_on:  # 只有状态改变时才操作
                GPIO.output(BUZZER_GPIO, GPIO.LOW if state else GPIO.HIGH)
                self.buzzer_on = state
                logger.info(f"蜂鸣器已{'开启' if state else '关闭'}")
        except Exception as e:
            logger.error(f"设置蜂鸣器状态时出错: {e}")
    
    def set_led(self, state):
        """
        设置LED状态
        
        Args:
            state (bool): True表示点亮LED，False表示熄灭LED
        """
        try:
            GPIO.output(LED_GPIO, GPIO.HIGH if state else GPIO.LOW)
            logger.info(f"LED已{'点亮' if state else '熄灭'}")
        except Exception as e:
            logger.error(f"设置LED状态时出错: {e}")
    
    def get_all_status(self):
        """
        获取所有传感器的检测状态
        
        Returns:
            dict: 包含人体和碰撞检测状态的字典
        """
        body_detected = self.detect_body()
        collision_detected = self.detect_collision()
        
        return {
            "body": body_detected,
            "collision": collision_detected,
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    
    def run_detection(self):
        """运行传感器检测循环"""
        logger.info("传感器检测程序启动")
        logger.info(f"人体传感器GPIO: {BODY_GPIO}, 碰撞传感器GPIO: {COLLISION_GPIO}")
        logger.info(f"蜂鸣器GPIO: {BUZZER_GPIO}, LED GPIO: {LED_GPIO}")
        
        try:
            # 初始化LED为熄灭状态
            self.set_led(False)
            self.set_buzzer(False)
            
            while True:
                # 获取所有传感器状态
                status = self.get_all_status()
                
                # 记录检测结果
                body_status = "检测到人体" if status["body"] else "无人体"
                collision_status = "检测到障碍物" if status["collision"] else "无障碍物"
                
                log_message = f"人体: {body_status}, 碰撞: {collision_status}"
                logger.info(log_message)
                
                # 根据检测结果执行相应操作
                if status["body"] and status["collision"]:
                    logger.warning("同时检测到人体和障碍物!")
                    self.set_buzzer(True)  # 持续开启蜂鸣器
                    self.set_led(True)
                elif status["body"]:
                    logger.info("仅检测到人体")
                    self.set_buzzer(True)  # 持续开启蜂鸣器
                    self.set_led(False)
                elif status["collision"]:
                    logger.info("仅检测到障碍物")
                    self.set_buzzer(False)  # 关闭蜂鸣器
                    self.set_led(True)
                else:
                    # 无检测时确保LED熄灭并关闭蜂鸣器
                    self.set_buzzer(False)
                    self.set_led(False)
                
                time.sleep(DETECTION_INTERVAL)
                
        except KeyboardInterrupt:
            logger.info("程序被用户中断")
        except Exception as e:
            logger.error(f"程序运行出错: {e}")
        finally:
            # 确保退出时LED和蜂鸣器都关闭
            try:
                self.set_led(False)
                self.set_buzzer(False)
            except:
                pass
            self.cleanup()
    
    def cleanup(self):
        """清理GPIO资源"""
        GPIO.cleanup()
        logger.info("GPIO 资源已清理")


def main():
    """主函数"""
    try:
        detector = SensorDetector()
        detector.run_detection()
    except Exception as e:
        logger.error(f"初始化传感器检测器失败: {e}")


if __name__ == "__main__":
    main()