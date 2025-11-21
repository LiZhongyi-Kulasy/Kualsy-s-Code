from TouchScreen import  TouchScreen
from UART import UART
from maix import app,time,image
from Camera import Camera
from YOLO import YOLO
def main():
    cam = Camera()
    ts = TouchScreen()
    uart = UART()
    yolo = YOLO()

    ts.map_button_positions(cam.width, cam.height, cam.dis)

    detect_figure = False

    prev_stop = False
    detect_start_time = 0
    dont_detect = False


    while not app.need_exit():
        t = time.time_ms()

        img = cam.cam.read()

        ts.touch(img)
        bin_img = img.binary(cam.Rel_Color_Threshold, invert=False, zero=True)  # 对获取的图像帧中Rel_Color_Threshold进行二进制化处理
        line_element = cam.car_run(bin_img)
        cam.Mark(line_element, img)

        cam.find_fin(img)
        uart.send_rho(cam.line_rho)  # 发送加权坐标

        img.draw_line(80, 0, 80, 120, color=image.COLOR_RED, thickness=1)
        # 停止
        
        if cam.flag == [1,1,1,1] or cam.flag == [1,1,0,0] or cam.flag == [0,0,1,1]:
            if not prev_stop:
                uart.send_command(0x53) # "S"
                # print(0x53)    # 83
                prev_stop = True  # 当不再识别到要停止时重置
        else:
            prev_stop = False
        # if cam.flag[1] == 1 and cam.flag[2] == 1:
        #     uart.send_command(0x53) # "S"
        #     cam.flag = [0,0,0,0]
            # print('S')
        # # 转弯
        # if cam.flag[2]==1 and cam.flag[3]==1: uart.send_command(0x52) ;print(1)# 右转 
        # if cam.flag[0]==1 and cam.flag[1]==1: uart.send_command(0x4C) ;print(2)# 左转

        # if not detect_figure:
        #     if uart.Serial_RxFlag == 0:
        #         uart.receive_data()
        #     elif uart.Serial_RxFlag == 1:
                
        #         # print(uart.rx_buff)
        #         if uart.rx_buff == 68: # 'D'
        #                 detect_figure = True
        #                 yolo.detect_figure(img)
        #                 # 识别数字
        #                 # print(num)
        #                 if yolo.Num != 0:
        #                     if yolo.Num == '3':    uart.send_command(0x46)  #;print(uart.rx_buff)#"F"
        #                     if yolo.Num == '4':    uart.send_command(0x42)  #;print(uart.rx_buff)#"B"    
        #                     yolo.Num = 0
        #                     uart.rx_buff = 0
        #                     uart.Serial_RxFlag = 0
        #         else:
        #             uart.rx_buff = 0
        #         uart.Serial_RxFlag = 0

        if not detect_figure:
            if uart.Serial_RxFlag == 0:
                uart.receive_data()
            elif uart.Serial_RxFlag == 1:  
                # print(uart.rx_buff)
                if uart.rx_buff == 68: # 'D'
                    detect_figure = True
                    uart.rx_buff = 0
                    uart.Serial_RxFlag = 0
                    detect_start_time = time.time_ms()
                else:
                    uart.rx_buff = 0
                    uart.Serial_RxFlag = 0
        
        else:
            yolo.detect_figure(img)

            # 识别数字
            # print(num)
            if yolo.Num != None:
                if yolo.Num == '3':    uart.send_command(0x46)  #;print(uart.rx_buff)#"F"
                if yolo.Num == '4':    uart.send_command(0x42)  #;print(uart.rx_buff)#"B"    
                yolo.Num = None
                detect_figure = False
                dont_detect = True

            if dont_detect:
                if time.time_ms() - detect_start_time >= 1000:
                    detect_figure =False
                    # dont_detect = False ###？？？？

        # img.draw_string(120,15,str(ts.set_luma), image.COLOR_WHITE)
        # img.draw_string(120,25,str(ts.set_con), image.COLOR_WHITE)
        # img.draw_string(120,35,str(ts.set_sat), image.COLOR_WHITE)

        # cam.cam.luma(ts.set_luma)
        # cam.cam.constrast(ts.set_con)
        # cam.cam.saturation(ts.set_sat)
        ts.open_close_camera(cam.dis, img)
        
            
        
        
        print("FPS= ", int(1000 / (time.time_ms() - t)))

if __name__ == "__main__":
    main()