import RPi.GPIO as GPIO
import time
import os

# 碰撞检测模块
class CollisionDetector:
    def __init__(self, gpio_pin=18):
        """
        初始化碰撞检测器
        
        Args:
            gpio_pin (int): 连接传感器OUT引脚的GPIO引脚号，默认为18
        """
        self.gpio_pin = gpio_pin
        self.setup_gpio()
    
    def setup_gpio(self):
        """初始化GPIO设置"""
        try:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.gpio_pin, GPIO.IN)
            print(f"GPIO {self.gpio_pin} 初始化成功")
        except Exception as e:
            print(f"GPIO 初始化失败: {e}")
            raise
    
    def detect_collision(self):
        """
        检测是否有障碍物
        
        Returns:
            bool: True表示检测到障碍物，False表示无障碍物
        """
        try:
            # 传感器检测到障碍物时输出低电平（0）
            # 无障碍物时输出高电平（1）
            signal = GPIO.input(self.gpio_pin)
            return signal == 0
        except Exception as e:
            print(f"检测障碍物时出错: {e}")
            return False
    
    def get_status(self):
        """
        获取当前检测状态
        
        Returns:
            dict: 包含检测状态和时间戳的字典
        """
        collision = self.detect_collision()
        return {
            "collision": collision,
            "timestamp": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
            "message": "检测到障碍物" if collision else "前方无障碍物"
        }
    
    def cleanup(self):
        """清理GPIO资源"""
        GPIO.cleanup()
        print("GPIO 资源已清理")

def main():
    """主函数"""
    # 从环境变量获取GPIO引脚配置，默认为18
    gpio_pin = int(os.environ.get('COLLISION_GPIO_PIN', 18))
    
    # 创建碰撞检测器实例
    detector = CollisionDetector(gpio_pin)
    
    try:
        print("碰撞检测 Demo 启动")
        print("按 Ctrl+C 退出程序")
        print("-" * 30)
        
        while True:
            # 获取检测状态
            status = detector.get_status()
            
            # 输出检测结果
            print(f"[{status['timestamp']}] {status['message']}")
            
            # 等待一段时间再检测
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n程序被用户中断")
    except Exception as e:
        print(f"程序运行出错: {e}")
    finally:
        # 清理GPIO资源
        detector.cleanup()

if __name__ == "__main__":
    main()