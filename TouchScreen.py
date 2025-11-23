from maix import touchscreen, image,camera
from maix._maix.camera import Camera
class TouchScreen:
    def __init__(self):
        self.ts = touchscreen.TouchScreen()
        self.opencamera_labol = "OPEN"
        self.closecamera_labol = "CLOSE"
        self.size1 = image.string_size(self.opencamera_labol)
        self.size2 = image.string_size(self.closecamera_labol)
        # [x, y, w, h]
        self.open_btn_pos = [0, 0, 6 + self.size1.width(), 6 + self.size1.height()]
        self.close_btn_pos = [0, 6 + self.size1.height(), 6 + self.size2.width(), 6 + self.size2.height()]
        self.open_btn_disp_pos = None
        self.close_btn_disp_pos = None
        self.turn_figure = 0
        # 1=打开摄像头, 0=关闭
        self.flag = 1
        #
        # self.luma_add = "L+"
        # self.luma_sub = "L-"
        # self.con_add = "C+"
        # self.con_sub = "C-"
        # self.sat_add = "S+"
        # self.sat_sub = "S-"
        # self.set_luma = 50
        # self.set_con  = 50
        # self.set_sat  = 50
        # self.size_luma = image.string_size(self.luma_add)
        # self.size_con = image.string_size(self.con_add)
        # self.size_sat = image.string_size(self.sat_add)
        # self.set_luma_add_btn_pos = [0,6*2 + self.size1.height() + self.size2.height(),
        #                             6 + self.size_luma.width(),6 + self.size_luma.height()]
        # self.set_luma_sub_btn_pos = [6 + self.size_luma.width(),6*2 + self.size1.height() + self.size2.height(),
        #                             6 + self.size_luma.width(),6 + self.size_luma.height()]
        # self.set_con_add_btn_pos = [0,6*3 + self.size1.height() + self.size2.height() + self.size_luma.height(),
        #                             6 + self.size_con.width(),6 + self.size_con.height()]
        # self.set_con_sub_btn_pos = [6 + self.size_con.width(),6*3 + self.size1.height() + self.size2.height() + self.size_luma.height(),
        #                             6 + self.size_con.width(),6 + self.size_con.height()]
        # self.set_sat_add_btn_pos = [0,6*4 + self.size1.height() + self.size2.height() + self.size_luma.height() + self.size_con.height(),
        #                             6 + self.size_sat.width(),6 + self.size_sat.height()]
        # self.set_sat_sub_btn_pos = [6 + self.size_sat.width(),6*4 + self.size1.height() + self.size2.height() + self.size_luma.height() + self.size_con.height(),
        #                             6 + self.size_sat.width(),6 + self.size_sat.height()]

    # 图像按键坐标映射到屏幕上的坐标
    # 用640X480和屏幕分辨率保持一致就不用映射
    def map_button_positions(self, width, height, dis):
        # self.open_btn_disp_pos = image.resize_map_pos(width, height, dis.width(), dis.height(), image.Fit.FIT_CONTAIN,
        #                                      self.open_btn_pos[0], self.open_btn_pos[1], self.open_btn_pos[2], self.open_btn_pos[3])
        # self.close_btn_disp_pos = image.resize_map_pos(width, height, dis.width(), dis.height(), image.Fit.FIT_CONTAIN,
        #                                       self.close_btn_pos[0], self.close_btn_pos[1], self.close_btn_pos[2], self.close_btn_pos[3])
        self.open_btn_disp_pos = image.resize_map_pos(width, height, dis.width(),
                                                      dis.height(), image.Fit.FIT_CONTAIN,*self.open_btn_pos)
        self.close_btn_disp_pos = image.resize_map_pos(width, height, dis.width(),
                                                       dis.height(), image.Fit.FIT_CONTAIN,*self.close_btn_pos)

        # self.luma_add_btn_disp_pos = image.resize_map_pos(width, height, dis.width(),
        #                                               dis.height(), image.Fit.FIT_CONTAIN,*self.set_luma_add_btn_pos)
        # self.luma_sub_btn_disp_pos = image.resize_map_pos(width, height, dis.width(),
        #                                               dis.height(), image.Fit.FIT_CONTAIN,*self.set_luma_sub_btn_pos)
        # self.con_add_btn_disp_pos = image.resize_map_pos(width, height, dis.width(),
        #                                               dis.height(), image.Fit.FIT_CONTAIN,*self.set_con_add_btn_pos)
        # self.con_sub_btn_disp_pos = image.resize_map_pos(width, height, dis.width(),
        #                                               dis.height(), image.Fit.FIT_CONTAIN,*self.set_con_sub_btn_pos)
        # self.sat_add_btn_disp_pos = image.resize_map_pos(width, height, dis.width(),
        #                                               dis.height(), image.Fit.FIT_CONTAIN,*self.set_sat_add_btn_pos)
        # self.sat_sub_btn_disp_pos = image.resize_map_pos(width, height, dis.width(),
        #                                               dis.height(), image.Fit.FIT_CONTAIN,*self.set_sat_sub_btn_pos)

    # 绘制触摸按钮(关摄像头/打开摄像头)
    def touch(self,img):
        img.draw_string(2, 6, self.opencamera_labol, image.COLOR_WHITE)
        img.draw_string(2, 6 * 2 + self.size1.height(), self.closecamera_labol, image.COLOR_WHITE)
        img.draw_rect(self.open_btn_pos[0], self.open_btn_pos[1], self.open_btn_pos[2], self.open_btn_pos[3], image.COLOR_WHITE, 2)
        img.draw_rect(self.close_btn_pos[0], self.close_btn_pos[1], self.close_btn_pos[2], self.close_btn_pos[3], image.COLOR_WHITE, 2)

    #     img.draw_string(2, 6 * 3 + self.size1.height() + self.size2.height(), self.luma_add, image.COLOR_WHITE)
    #     img.draw_string(2*4 + self.size_luma.width(), 6 * 3 + self.size1.height() + self.size2.height(), self.luma_sub, image.COLOR_WHITE)
    #     img.draw_string(2, 6 * 4 + self.size1.height() + self.size2.height() + self.size_luma.height(), self.con_add, image.COLOR_WHITE)
    #     img.draw_string(2*4 + self.size_con.width(), 6 * 4 + self.size1.height() + self.size2.height() + self.size_luma.height(), self.con_sub, image.COLOR_WHITE)
    #     img.draw_string(2, 6 * 5 + self.size1.height() + self.size2.height() + self.size_luma.height() + self.size_con.height(), self.sat_add, image.COLOR_WHITE)
    #     img.draw_string(2*4 + self.size_sat.width(), 6 * 5 + self.size1.height() + self.size2.height() + self.size_luma.height() + self.size_con.height(), self.sat_sub, image.COLOR_WHITE)
    #     img.draw_rect(self.set_luma_add_btn_pos[0], self.set_luma_add_btn_pos[1], self.set_luma_add_btn_pos[2], self.set_luma_add_btn_pos[3], image.COLOR_WHITE, 2)
    #     img.draw_rect(self.set_luma_sub_btn_pos[0], self.set_luma_sub_btn_pos[1], self.set_luma_sub_btn_pos[2], self.set_luma_sub_btn_pos[3], image.COLOR_WHITE, 2)
    #     img.draw_rect(self.set_con_add_btn_pos[0], self.set_con_add_btn_pos[1], self.set_con_add_btn_pos[2], self.set_con_add_btn_pos[3], image.COLOR_WHITE, 2)
    #     img.draw_rect(self.set_con_sub_btn_pos[0], self.set_con_sub_btn_pos[1], self.set_con_sub_btn_pos[2], self.set_con_sub_btn_pos[3], image.COLOR_WHITE, 2)
    #     img.draw_rect(self.set_sat_add_btn_pos[0], self.set_sat_add_btn_pos[1], self.set_sat_add_btn_pos[2], self.set_sat_add_btn_pos[3], image.COLOR_WHITE, 2)
    #     img.draw_rect(self.set_sat_sub_btn_pos[0], self.set_sat_sub_btn_pos[1], self.set_sat_sub_btn_pos[2], self.set_sat_sub_btn_pos[3], image.COLOR_WHITE, 2)
    # 判断触摸点是否在按钮区域内
    def is_in_button(self, x, y, btn_pos):
        if btn_pos is None:
            return False
        bx, by, bw, bh = btn_pos
        return bx <= x <= bx + bw and by <= y <= by + bh

    def open_close_camera(self, dis, img):
        x, y, pressed = self.ts.read()
        if pressed:
            if self.is_in_button(x, y, self.open_btn_disp_pos):       self.flag = 1  
            if self.is_in_button(x, y, self.close_btn_disp_pos):      self.flag = 0  ;self.turn_figure = 0
            # if self.is_in_button(x, y, self.luma_add_btn_disp_pos):       self.set_luma +=1
            # if self.is_in_button(x, y, self.luma_sub_btn_disp_pos):       self.set_luma -=1
            # if self.is_in_button(x, y, self.con_add_btn_disp_pos):       self.set_con +=1
            # if self.is_in_button(x, y, self.con_sub_btn_disp_pos):       self.set_con -=1
            # if self.is_in_button(x, y, self.sat_add_btn_disp_pos):       self.set_sat +=1
            # if self.is_in_button(x, y, self.sat_sub_btn_disp_pos):       self.set_sat -=1

        # if self.flag:
        dis.show(img)
