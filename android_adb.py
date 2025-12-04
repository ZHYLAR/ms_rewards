import subprocess
import random
import time
import string

# ===================== 配置参数（根据你的实际情况修改）=====================
TARGET_DEVICE = "127.0.0.1:5557"  # 目标设备标识（从adb devices输出中复制）
# TARGET_DEVICE = "127.0.0.1:5555" 
SEARCH_BOX_COORD = (425, 924)     # 搜索框坐标
SEARCH_BTN_COORD = (360, 347)     # 搜索按钮坐标
BACK_HOME_COORD = (109, 1535)     # 返回主页坐标
LOOP_TIMES = 40                  # 循环次数（-1=无限循环，正数=指定次数）
DELAY_BETWEEN_STEPS = 2         # 步骤间延时（秒，避免操作过快）
DELAY_BETWEEN_LOOPS = 5         # 循环间延时（秒）

# ===================== 核心函数 =====================
def connect_device():
    """尝试连接设备"""
    cmd = f"adb connect {TARGET_DEVICE}"
    print(f"正在尝试连接设备: {cmd}")
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            encoding="utf-8"
        )
        output = result.stdout.strip()
        print(f"连接结果: {output}")
        # 只要输出包含 connected to 或 already connected 即视为成功
        if "connected to" in output or "already connected" in output:
            return True
        return False
    except Exception as e:
        print(f"连接设备时发生异常: {e}")
        return False

def run_adb_command(command):
    """执行ADB命令，返回执行结果"""
    # 拼接设备指定参数
    full_command = f"adb -s {TARGET_DEVICE} {command}"
    try:
        # 执行命令并捕获输出
        result = subprocess.run(
            full_command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            encoding="utf-8"
        )
        if result.returncode != 0:
            print(f"命令执行失败：{full_command}")
            print(f"错误信息：{result.stderr.strip()}")
            return False
        return True
    except Exception as e:
        print(f"执行命令时异常：{e}")
        return False

def click_coord(x, y):
    """点击指定坐标"""
    print(f"点击坐标 ({x}, {y})")
    # 随机偏移坐标，正负10像素
    offset_x = random.randint(-10, 10)
    offset_y = random.randint(-10, 10)
    new_x = x + offset_x
    new_y = y + offset_y
    print(f"点击坐标 ({new_x}, {new_y}) [原始:({x},{y}), 偏移:({offset_x},{offset_y})]")
    return run_adb_command(f"shell input tap {new_x} {new_y}")

def input_random_chars(length=3):
    """随机输入指定长度的英文字母"""
    # 生成随机小写英文字母（如需大写用string.ascii_uppercase）
    random_chars = ''.join(random.choice(string.ascii_lowercase) for _ in range(length))
    print(f"输入随机字符：{random_chars}")
    return run_adb_command(f"shell input text {random_chars}")

# ===================== 主循环逻辑 =====================
if __name__ == "__main__":
    # 尝试自动连接设备
    if not connect_device():
        print("警告：自动连接失败，后续操作可能会出错。请检查ADB服务或设备状态。")

    # 先验证设备是否在线
    if not run_adb_command("devices"):
        print("目标设备无法连接，请检查设备标识和ADB连接！")
        exit(1)
    
    print(f"开始循环执行操作（设备：{TARGET_DEVICE}）")
    loop_count = 0
    
    while True:
        # 终止条件：达到指定循环次数
        if LOOP_TIMES > 0 and loop_count >= LOOP_TIMES:
            print(f"已完成指定{LOOP_TIMES}次循环，脚本结束")
            break
        
        loop_count += 1
        print(f"\n===== 第{loop_count}次循环 =====")
        
        # 步骤1：点击搜索框
        if not click_coord(*SEARCH_BOX_COORD):
            print("点击搜索框失败，跳过本次循环")
            # 步骤间延时，随机±1秒
            step_delay = DELAY_BETWEEN_STEPS + random.uniform(0, 1)
            print(f"步骤间延时: {step_delay:.2f}秒")
            time.sleep(step_delay)
            continue
        time.sleep(DELAY_BETWEEN_STEPS)
        
        # 步骤2：输入随机3个英文字母
        if not input_random_chars(3):
            print("输入字符失败，跳过本次循环")
            step_delay = DELAY_BETWEEN_STEPS + random.uniform(0, 1)
            print(f"步骤间延时: {step_delay:.2f}秒")
            time.sleep(step_delay)
            continue
        time.sleep(DELAY_BETWEEN_STEPS)
        
        # 步骤3：点击搜索按钮
        if not click_coord(*SEARCH_BTN_COORD):
            print("点击搜索按钮失败，跳过本次循环")
            step_delay = DELAY_BETWEEN_STEPS + random.uniform(0, 1)
            print(f"步骤间延时: {step_delay:.2f}秒")
            time.sleep(step_delay)
            continue
        time.sleep(DELAY_BETWEEN_LOOPS)
        
        # 步骤4：点击返回主页
        if not click_coord(*BACK_HOME_COORD):
            print("点击返回主页失败，跳过本次循环")
            loop_delay = DELAY_BETWEEN_STEPS + random.uniform(0, 1)
            print(f"循环间延时: {loop_delay:.2f}秒")
            time.sleep(loop_delay)
            continue
        # time.sleep(DELAY_BETWEEN_LOOPS)