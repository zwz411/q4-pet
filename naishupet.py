import tkinter as tk
import math
import random
import time

# 颜色配置
TRANSPARENT_COLOR = "#010203"  # 用于透明的底色
C_YELLOW = "#F4D03F"           # 奶鼠肤色
C_EAR_PINK = "#F5B7B1"         # 耳朵内侧
C_HOODIE = "#95A5A6"           # 灰色卫衣
C_PANTS = "#2C3E50"            # 墨蓝色裤子
C_OUTLINE = "#B7950B"          # 轻微边缘线（防止糊成一团）
C_COMPUTER = "#BDC3C7"         # 电脑外壳
C_SCREEN = "#34495E"           # 屏幕
C_DESK = "#E67E22"             # 桌子
C_CHAIR = "#7F8C8D"            # 椅子

class MilkMousePet:
    def __init__(self, root):
        self.root = root
        self.root.title("奶鼠桌宠")
        
        # 窗口设置
        self.width = 400
        self.height = 400
        self.screen_w = self.root.winfo_screenwidth()
        self.screen_h = self.root.winfo_screenheight()
        self.start_x = self.screen_w - self.width - 100
        self.start_y = self.screen_h - self.height - 100

        self.root.geometry(f"{self.width}x{self.height}+{self.start_x}+{self.start_y}")
        self.root.overrideredirect(True)  # 无边框
        self.root.wm_attributes("-topmost", True) # 置顶
        self.root.wm_attributes("-transparentcolor", TRANSPARENT_COLOR) # 透明背景

        # 画布
        self.canvas = tk.Canvas(root, width=self.width, height=self.height, 
                                bg=TRANSPARENT_COLOR, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        # 状态变量
        self.tick = 0
        self.blink = 0
        self.state = "coding"  # coding, looking, hitting
        self.drag_data = {"x": 0, "y": 0}
        self.mouse_x = 0
        self.mouse_y = 0
 
        # 事件绑定
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<Motion>", self.on_hover)
        self.root.bind("<ButtonRelease-1>", self.on_release)

        # 启动主循环
        self.draw_scene()
        self.update_loop()

    def draw_scene(self):
        self.canvas.delete("all")
        
        # 呼吸/敲代码的偏移量
        bob = math.sin(self.tick * 0.1) * 2
        hand_bob = math.sin(self.tick * 0.8) * 3 if self.state == "coding" else 0

        # 1. 绘制背景道具（椅子、桌子）
        self.draw_props()

        if self.state == "coding":
            self.draw_side_view(bob, hand_bob)
        elif self.state == "looking":
            self.draw_front_view(bob)
        elif self.state == "hitting":
            self.draw_side_view(bob, hand_bob)
            self.draw_hitting_hand()

    def draw_props(self):
        # 椅子靠背
        self.canvas.create_oval(120, 200, 320, 380, fill=C_CHAIR, outline="")
        # 桌子
        self.canvas.create_rectangle(220, 280, 380, 300, fill=C_DESK, outline="")
        self.canvas.create_rectangle(240, 300, 250, 380, fill="#D35400", outline="") # 桌腿
        
        if self.state == "coding":
            # 打开状态的电脑
            self.canvas.create_polygon(230, 220, 360, 220, 360, 280, 230, 280, fill=C_COMPUTER, outline="")
            self.canvas.create_rectangle(235, 225, 355, 275, fill=C_SCREEN, outline="")
            # 屏幕代码行
            for i in range(5):
                self.canvas.create_rectangle(245, 235 + i*8, 245 + random.randint(20, 80), 239 + i*8, fill="#2ECC71" if i%2==0 else "#3498DB", outline="")
        elif self.state == "looking":
            # 合上的电脑（盖子扣下来）
            self.canvas.create_polygon(230, 280, 360, 280, 360, 260, 230, 260, fill=C_COMPUTER, outline="")

    def draw_side_view(self, bob, hand_bob):
        # 尾巴
        self.canvas.create_line(160, 340, 120, 350, 110, 370, smooth=True, width=6, fill=C_YELLOW, capstyle=tk.ROUND)
        
        # 身体和衣服(圆润)
        # 裤子
        self.canvas.create_oval(150, 290, 230, 350, fill=C_PANTS, outline=C_OUTLINE)
        # 卫衣
        self.canvas.create_oval(140, 230, 240, 320, fill=C_HOODIE, outline=C_OUTLINE)
        # 卫衣帽子褶皱
        self.canvas.create_arc(160, 230, 220, 270, start=180, extent=180, style=tk.ARC, outline="#7F8C8D", width=2)

        # 头部
        head_y = 180 + bob
        # 大耳朵（侧面只看到一只半）
        self.canvas.create_oval(120, 100 + bob, 180, 160 + bob, fill=C_YELLOW, outline=C_OUTLINE)
        self.canvas.create_oval(135, 115 + bob, 165, 145 + bob, fill=C_EAR_PINK, outline="")
        
        # 脸（侧脸）
        self.canvas.create_oval(160, 140 + bob, 230, 210 + bob, fill=C_YELLOW, outline=C_OUTLINE)
        
        # 眼睛（侧眼）
        if self.blink > 0:
            self.canvas.create_line(200, 165 + bob, 215, 165 + bob, width=2, fill="black")
        else:
            self.canvas.create_oval(200, 155 + bob, 212, 175 + bob, fill="white", outline="")
            self.canvas.create_oval(203, 160 + bob, 210, 170 + bob, fill="black", outline="")
            self.canvas.create_oval(205, 162 + bob, 208, 165 + bob, fill="white", outline="") # 高光
            
        # 嘴巴
        self.canvas.create_arc(210, 180 + bob, 230, 195 + bob, start=0, extent=180, style=tk.ARC, outline="black")
        
        # 手
        if self.state == "coding":
            # 敲代码的手
            self.canvas.create_oval(220, 250 + hand_bob, 240, 270 + hand_bob, fill=C_HOODIE, outline=C_OUTLINE)
        else:
            # 自然下垂的手
            self.canvas.create_oval(210, 280, 230, 300, fill=C_HOODIE, outline=C_OUTLINE)

        # 脚
        self.canvas.create_oval(170, 340, 200, 360, fill=C_YELLOW, outline=C_OUTLINE)

    def draw_front_view(self, bob):
        # 正面视图（面向用户）
        head_y = 150 + bob
        # 尾巴
        self.canvas.create_line(200, 340, 220, 380, smooth=True, width=6, fill=C_YELLOW, capstyle=tk.ROUND)
        # 裤子
        self.canvas.create_oval(160, 290, 240, 350, fill=C_PANTS, outline=C_OUTLINE)
        # 卫衣
        self.canvas.create_oval(150, 230, 250, 320, fill=C_HOODIE, outline=C_OUTLINE)
        # 卫衣抽绳
        self.canvas.create_line(180, 240, 180, 280, fill="white", width=2)
        self.canvas.create_line(220, 240, 220, 280, fill="white", width=2)

        # 双脚
        self.canvas.create_oval(160, 340, 190, 360, fill=C_YELLOW, outline=C_OUTLINE)
        self.canvas.create_oval(210, 340, 240, 360, fill=C_YELLOW, outline=C_OUTLINE)

        # 双手
        self.canvas.create_oval(130, 260, 160, 290, fill=C_HOODIE, outline=C_OUTLINE)
        self.canvas.create_oval(240, 260, 270, 290, fill=C_HOODIE, outline=C_OUTLINE)

        # 大耳朵
        self.canvas.create_oval(110, 80 + bob, 170, 140 + bob, fill=C_YELLOW, outline=C_OUTLINE)
        self.canvas.create_oval(125, 95 + bob, 155, 125 + bob, fill=C_EAR_PINK, outline="")
        self.canvas.create_oval(230, 80 + bob, 290, 140 + bob, fill=C_YELLOW, outline=C_OUTLINE)
        self.canvas.create_oval(245, 95 + bob, 275, 125 + bob, fill=C_EAR_PINK, outline="")

        # 头
        self.canvas.create_oval(150, 120 + bob, 250, 220 + bob, fill=C_YELLOW, outline=C_OUTLINE)
        
        # 眼睛（正面大眼）
        if self.blink > 0:
            self.canvas.create_line(175, 170 + bob, 190, 170 + bob, width=3, fill="black")
            self.canvas.create_line(210, 170 + bob, 225, 170 + bob, width=3, fill="black")
        else:
            for ex in [180, 215]:
                self.canvas.create_oval(ex, 155 + bob, ex+15, 175 + bob, fill="white", outline="black")
                self.canvas.create_oval(ex+4, 160 + bob, ex+11, 170 + bob, fill="black")
                self.canvas.create_oval(ex+6, 162 + bob, ex+9, 165 + bob, fill="white")

        # 鼻子和嘴巴
        self.canvas.create_oval(195, 185 + bob, 205, 192 + bob, fill=C_EAR_PINK, outline="")
        self.canvas.create_arc(185, 192 + bob, 215, 205 + bob, start=180, extent=180, style=tk.ARC, outline="black")

    def draw_hitting_hand(self):
        # 根据鼠标位置画伸出的手
        cx = self.width / 2
        cy = self.height / 2
        # 计算鼠标相对窗口位置
        mx = self.mouse_x
        my = self.mouse_y
        
        # 绘制一条伸缩的手臂
        self.canvas.create_line(240, 270, mx, my, width=8, fill=C_HOODIE, smooth=True)
        # 小手拍
        self.canvas.create_oval(mx-15, my-15, mx+15, my+15, fill=C_YELLOW, outline=C_OUTLINE)

    def update_loop(self):
        self.tick += 1
        
        # 眨眼逻辑
        if self.blink > 0:
            self.blink -= 1
        elif random.random() < 0.02:
            self.blink = 8

        self.draw_scene()
        self.root.after(40, self.update_loop)

    # ================= 交互事件 =================
    def on_click(self, event):
        # 记录拖拽起始位置
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y
        
        # 点击时切换状态：如果在敲代码就转身，在转身就回去敲代码
        if self.state == "coding":
            self.state = "looking"
        elif self.state == "looking":
            self.state = "coding"
            
        # 取消排队的悬停状态
        if hasattr(self, 'hover_timer'):
            self.root.after_cancel(self.hover_timer)
        self.state = "looking" if self.state != "coding" else "coding"

    def on_drag(self, event):
        # 拖动窗口
        x = self.root.winfo_x() + (event.x - self.drag_data["x"])
        y = self.root.winfo_y() + (event.y - self.drag_data["y"])
        self.root.geometry(f"+{x}+{y}")

    def on_release(self, event):
        self.drag_data["x"] = 0
        self.drag_data["y"] = 0

    def on_hover(self, event):
        self.mouse_x = event.x
        self.mouse_y = event.y
        
        # 只有当鼠标靠近奶鼠时，才触发拍打动作
        if 150 < event.x < 300 and 100 < event.y < 300:
            if self.state != "hitting":
                self.state = "hitting"
                # 一定时间没动，恢复原状态
                if hasattr(self, 'hover_timer'):
                    self.root.after_cancel(self.hover_timer)
                self.hover_timer = self.root.after(1500, self.reset_state)
        else:
            if self.state == "hitting":
                self.state = "coding"

    def reset_state(self):
        self.state = "coding"

if __name__ == "__main__":
    root = tk.Tk()
    app = MilkMousePet(root)
    root.mainloop()
