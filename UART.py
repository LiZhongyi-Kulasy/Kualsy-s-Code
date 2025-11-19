from maix import uart
####串口通信####
class UART:
    def __init__(self, device="/dev/ttyS0", baudrate=115200):
        self.serial = uart.UART(device, baudrate)
        self.Serial_RxFlag = 0
        self.rx_buff = 0
        self.state = 0
        # self.rx_flag = 0
        

    # 串口发送路口移动命令（帧格式：{ cmd }）
    def send_command(self, command: int):
        data = bytes([0x7B,
                      command,
                      0x7D])
        self.serial.write(data)

    # 串口发送加权X坐标
    def send_rho(self,x: int):
        # 拆分坐标值为高低字节
        x_high = (x >> 8) & 0xFF
        x_low = x & 0xFF
        # 构建数据帧
        data = bytes([
                    0x3C,           # 帧头 <
                    x_high, x_low,  # X坐标
                    0x3E            # 帧尾 >
                    ])
        self.serial.write(data)

    # 串口接收函数
    # state = 0
    # Serial_RxFlag = 0
    # rx_buff = 0
    def receive_data(self):
        # global state # , rx_buff  # Serial_RxFlag,
        if self.state == 0:
            # 状态0：检测帧头 0x7B，即{
            res = self.serial.read(1)
            if res:
                byte = res[0]
                if byte == 0x7B:  # 匹配帧头
                    self.state = 1
                    self.rx_buff = None  # 开始新帧时清空上次数据
        elif self.state == 1:
            # 状态1：接收数据（#R G T----十进制82 71 84）
            res = self.serial.read(1)
            if res:
                self.rx_buff = res[0]
                self.state = 2
        elif self.state == 2:
            # 状态2：检测帧尾 0x7D，即}
            res = self.serial.read(1)
            if res:
                byte = res[0]
                if byte == 0x7D:  # 帧尾
                    # print(rx_buff)
                    self.state = 0
                    self.Serial_RxFlag = 1



