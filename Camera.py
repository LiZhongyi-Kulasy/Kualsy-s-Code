from maix import camera, display, image

class Camera:
    def __init__(self, width=160, height=120):
        self.cam = camera.Camera(width, height)
        self.width = width
        self.height = height
        self.dis = display.Display()
        ####巡线####
        self.Rel_Color_Threshold = [[5, 35, -30, 35, -30, 30]]   # 外面黑线
        self.Binar_Color_Threshold = [[0, 15, -5, 5, -5, 5]]     # 二值化后黑线阈值
        # x,y,w,h
        self.ROIS = [
            # (0, int(self.height / 6 * 0), self.width, int(self.height / 6)),
            (0, int(self.height / 6 * 1), self.width, int(self.height / 6)),
            (0, int(self.height / 6 * 2), self.width, int(self.height / 6)),
            (0, int(self.height / 6 * 3), self.width, int(self.height / 6)),
            (0, int(self.height / 6 * 4), self.width, int(self.height / 6)),
            (0, int(self.height / 6 * 5), self.width, int(self.height / 6))
        ]
        self.line_rho = 0 # None
        self.history_len = 5                                     # 融合最近5帧
        self.rho_history = []                                    

         # 起点/终点
        self.fin_roi = [
                        (5,80,15,15),
                        (35,80,15,15),
                        (110,80,15,15),
                        (140,80,15,15)
                       ]
        self.flag  = [0,0,0,0]

    def process_blob_coordinates(self,accepted_blobs, max_blob_pixels):
        # 处理色块坐标：对超过像素阈值的色块进行坐标替换
        processed_coords = []
    
        for i, blob in enumerate(accepted_blobs):
            if blob.pixels() > max_blob_pixels:
                # 色块像素数超过阈值，需要替换坐标
                if i == 0:
                    # 最下面的第一个色块，设为图像中心
                    processed_coords.append(self.width // 2)  # X坐标设为80
                else:
                    # 其他色块，使用上下相邻色块的平均值
                    if i == len(accepted_blobs) - 1:
                        # 如果是最后一个色块，只有下面的邻居
                        processed_coords.append(accepted_blobs[i-1].cx())
                    else:
                        # 有上下邻居，计算平均值
                        prev_cx = accepted_blobs[i-1].cx()
                        next_cx = accepted_blobs[i+1].cx()
                        processed_coords.append((prev_cx + next_cx) // 2)
            else:
                # 正常色块，使用原始坐标
                processed_coords.append(blob.cx())
    
        return processed_coords

    def car_run(self,img):
        accepted_blobs = []  # 最终被接受的色块（从下到上）
        max_dx = 30  # 可调：允许的最大水平偏移（像素）
        min_width = 2  # 宽度小于此值的黑线将被过滤掉
        max_blob_pixels = 500  # 最大像素阈值，像素数大于此值的 blob 会被过滤（可调）
        for r in reversed(self.ROIS):  # 从下往上
            blobs = img.find_blobs(self.Binar_Color_Threshold, roi=r[0:4], merge=True, pixels_threshold=100)  # 像素阈值可调
            # 先过滤宽度过小，再过滤像素过大的色块
            blobs = [b for b in blobs if b.w() >= min_width and b.pixels() <= max_blob_pixels]
            if not blobs:
                continue
            largest_blob = max(blobs, key=lambda b: b.pixels())
            cx = largest_blob.cx()

            if not accepted_blobs:
                # 底部第一个检测到的色块总是接受，作为参考
                accepted_blobs.append(largest_blob)
            else:
                # 与上一个已接受（更低一层）的色块比较水平距离 [-1]列表中最后一个值
                prev_cx = accepted_blobs[-1].cx()
                if abs(cx - prev_cx) <= max_dx:
                    accepted_blobs.append(largest_blob)
                # 若距离过大则忽略该 ROI 的色块

        # 对中间点做邻居范围过滤：若某中间点的 cx 不在其上下邻居 x 范围内，则移除
        if len(accepted_blobs) >= 3:
            filtered = [accepted_blobs[0]]
            for i in range(1, len(accepted_blobs) - 1):
                cx_i = accepted_blobs[i].cx()
                left = min(accepted_blobs[i - 1].cx(), accepted_blobs[i + 1].cx())
                right = max(accepted_blobs[i - 1].cx(), accepted_blobs[i + 1].cx())
                if left <= cx_i <= right:
                    filtered.append(accepted_blobs[i])
            # 若不在范围内则跳过（过滤掉）
            filtered.append(accepted_blobs[-1])
            accepted_blobs = filtered

        if accepted_blobs:    
                                                                   #,reverse=True 小到大
            line_blobs = sorted(accepted_blobs, key=lambda b: b.cy())  # 按Y坐标从小到大排序
            processed_coords = self.process_blob_coordinates(line_blobs, max_blob_pixels)
            # 加权坐标(如：((160+170)/2+180)/2  )

            # 使用处理后的坐标计算加权平均值
            raw_line_rho = processed_coords[0]
            for coord in processed_coords[1:]:
                raw_line_rho = (raw_line_rho + coord) // 2
            raw_line_rho = int(raw_line_rho)
           
            # self.line_rho = int(self.line_rho)
            
            # if weighted_coordinate is None:
            #     weighted_coordinate = line_blobs[0].cx()
            # else:
            #     weighted_coordinate = sum((weighted_coordinate+b.cx())/2 for b in line_blobs[1:]

            # # 最小二乘法线性拟合斜率
            # cx = np.array([float(b.cx()) for b in line_blobs], dtype=np.float64)
            # cy = np.array([float(b.cy()) for b in line_blobs], dtype=np.float64)
            # # cx = np.array([line_blobs[5].cx(),line_blobs[4].cx(),
            # #                line_blobs[3].cx(),line_blobs[2].cx(),
            # #                line_blobs[1].cx(),line_blobs[0].cx()])
            # # cy = np.array([line_blobs[5].cy(),line_blobs[4].cy(),
            # #                line_blobs[3].cy(),line_blobs[2].cy(),
            # #                line_blobs[1].cy(),line_blobs[0].cy()])
            # cov = np.sum((cx - cx.mean()) * (cy - cy.mean()))
            # var = np.sum((cx - cx.mean()) ** 2)
            # slope = cov / var
        else:
            raw_line_rho = int(self.width // 2)  # 没检测到时给默认值
        
            # slope   = 0.0  # 没检测到时斜率为0

        # 多帧融合
        self.rho_history.append(raw_line_rho)
        if len(self.rho_history) > self.history_len:
            self.rho_history.pop(0)                                                  # 删除列表 rho_history 中的第一个元素

        # 平滑处理（取平均值）
        self.line_rho = int(sum(self.rho_history) / len(self.rho_history))
        # print(line_rho)
        img.draw_string(120, 4, str(self.line_rho), image.COLOR_WHITE)

        img.draw_string(120, 4, str(self.line_rho), image.COLOR_WHITE)

        return accepted_blobs
        ##32处理数据：line_rho - 80

    # 标记函数：在每帧内部收集质心，按 Y（从上到下）排序并依次连线
    def Mark(self,Line, img):
        # # 如果没有检测到任何色块，直接返回
        # if not Line:
        #     return
        # # 局部点列表（避免跨帧累积）
        # points = []  # 存储 (cx, cy)
        # # 绘制色块矩形和十字，并收集质心
        for b in Line:
            img.draw_rect(b.x(), b.y(), b.w(), b.h(), color=image.COLOR_WHITE)
            img.draw_cross(b.cx(), b.cy(), image.COLOR_WHITE, size=2, thickness=1)
        #     points.append((b.cx(), b.cy()))
        # # 按 Y 坐标（即points的第二个元素b.cy）排序（从小到大）
        # points.sort(key=lambda p: p[1])
        # # 依次连接相邻的点，绘制红色粗线
        # for i in range(len(points) - 1):
        #     x1, y1 = points[i]
        #     x2, y2 = points[i + 1]
        #     img.draw_line(x1, y1, x2, y2, color=image.COLOR_RED, thickness=2)
    
    # 识别终点
    def find_fin(self,img):
        blobs = []
        img.draw_rect(self.fin_roi[0][0],self.fin_roi[0][1],self.fin_roi[0][2],self.fin_roi[0][3],color=image.COLOR_BLACK)
        img.draw_rect(self.fin_roi[1][0],self.fin_roi[1][1],self.fin_roi[1][2],self.fin_roi[1][3],color=image.COLOR_BLACK)
        img.draw_rect(self.fin_roi[2][0],self.fin_roi[2][1],self.fin_roi[2][2],self.fin_roi[2][3],color=image.COLOR_BLACK)
        img.draw_rect(self.fin_roi[3][0],self.fin_roi[3][1],self.fin_roi[3][2],self.fin_roi[3][3],color=image.COLOR_BLACK)
        for r in self.fin_roi:
            new_blobs = img.find_blobs(self.Binar_Color_Threshold, roi=r[0:4], merge=True, pixels_threshold=100)
            blobs.append(new_blobs)
        # print(1) if blobs[0] else print(0)
        # print(1) if blobs[1] else print(0)
        # print(1) if blobs[2] else print(0)
        # print(1) if blobs[3] else print(0)
        self.flag[0] = 1 if blobs[0] else 0
        self.flag[1] = 1 if blobs[1] else 0
        self.flag[2] = 1 if blobs[2] else 0
        self.flag[3] = 1 if blobs[3] else 0



        





