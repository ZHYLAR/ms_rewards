from pynput.keyboard import Key, Controller  # 用于模拟键盘操作
import time    # 用于时间等待
import random  # 用于生成随机字母
import string  # 用于获取字母字符集

WAIT_TIME = [6,8]  
REPETITION_TIME_IN_FAST_MODE = 10

# 初始化键盘控制器
keyboard = Controller()

if_shutdown = 0  # 结束是否关机

def simulate_keyboard_actions(repetitions=30):
    """
    模拟键盘操作：随机输入字母，回车，Alt+左，重复指定次数。
    """
    print(f"开始模拟键盘操作，总计重复 {repetitions} 次...")

    for i in range(repetitions):
        print(f"\n--- 第 {i + 1} 次操作 ---")
        time.sleep(1)
        
        # 1. 输入随机字母
        random_letters = ''.join(random.choices(string.ascii_letters, k=3))
        random_letters = random_letters.lower()
        print(f"输入随机字母: {random_letters}")
        keyboard.type(random_letters)  # 输入随机字母

        time.sleep(1)
        keyboard.press(Key.space)
        time.sleep(0.06)
        keyboard.release(Key.space)
        time.sleep(1)
        
        # 2. 模拟输入回车
        print("模拟输入回车键...")
        keyboard.press(Key.enter)
        keyboard.release(Key.enter)

        # 3. 等待
        print("等待...")
        time.sleep(random.randint(WAIT_TIME[0], WAIT_TIME[1]))

        # 4. 模拟输入Alt+方向左 (已注释，如需使用可取消注释)
        # print("模拟输入 Alt + 左方向键...")
        # with keyboard.pressed(Key.alt):
        #     keyboard.press(Key.left)
        #     keyboard.release(Key.left)
        
        time.sleep(0.5)
        for _ in range(2):
            keyboard.press('1')
            keyboard.release('1')
            time.sleep(0.1)
        
        time.sleep(0.5)

        with keyboard.pressed(Key.ctrl):
            keyboard.press('a')
            keyboard.release('a')
        time.sleep(0.5)
        keyboard.press(Key.backspace)
        keyboard.release(Key.backspace)

        # 5. 等待
        print("等待...")
        time.sleep(random.randint(WAIT_TIME[0], WAIT_TIME[1]))

    print("\n所有模拟键盘操作完成。")

def switch_broser(No):
    """切换到指定编号的浏览器窗口（Win+数字键）"""
    with keyboard.pressed(Key.cmd):  # Key.cmd 对应 Windows 键
        keyboard.press(str(No))
        keyboard.release(str(No))
    time.sleep(0.5)  # 等待窗口切换完成

def shutdown():
    """模拟关机操作"""
    # 显示桌面 (Win+D)
    with keyboard.pressed(Key.cmd):
        keyboard.press('d')
        keyboard.release('d')
    time.sleep(2)

    # 关闭所有窗口 (Alt+F4)
    with keyboard.pressed(Key.alt):
        keyboard.press(Key.f4)
        keyboard.release(Key.f4)
    time.sleep(2)


def faster_mode(broser_num, repetitions):
    """快速在多个浏览器间切换操作"""
    assert(broser_num > 1)
    for _ in range(repetitions):
        for i in range(broser_num):
            switch_broser(i + 1)
            # 根据浏览器数量分配等待时间
            sleep_time = REPETITION_TIME_IN_FAST_MODE // broser_num if (REPETITION_TIME_IN_FAST_MODE // broser_num > 0.2) else 0.2
            time.sleep(sleep_time + random.random())

            # time.sleep(0.5)
            for _ in range(2):
                keyboard.press('1')
                time.sleep(0.05)
                keyboard.release('1')
                time.sleep(0.1)
            
            time.sleep(0.5)

            with keyboard.pressed(Key.ctrl):
                keyboard.press('a')
                keyboard.release('a')
            time.sleep(0.1)
            keyboard.press(Key.backspace)
            keyboard.release(Key.backspace)
            time.sleep(0.5)

            # 输入随机字母
            random_letters = ''.join(random.choices(string.ascii_letters, k=3)).lower()
            print(f"输入随机字母: {random_letters}")
            keyboard.type(random_letters)

            time.sleep(0.1)
            keyboard.press(Key.space)
            time.sleep(0.06)
            keyboard.release(Key.space)
            time.sleep(0.1)
            # simulate_keyboard_actions(1)

            time.sleep(0.2)

            # 模拟输入回车
            print("模拟输入回车键...")
            keyboard.press(Key.enter)
            keyboard.release(Key.enter)

            time.sleep(0.2)

if __name__ == "__main__":
    # 切换到第一个浏览器并执行操作
    switch_broser(1)
    simulate_keyboard_actions(40)

    # 如需操作其他浏览器，可取消以下注释
    # switch_broser(2)
    # simulate_keyboard_actions(30)
    #
    # switch_broser(3)
    # simulate_keyboard_actions(30)
    
    # 快速模式示例（如需使用可取消注释）
    # faster_mode(2, 30)

    # # 结束时是否关机
    # if if_shutdown:
    #     shutdown()