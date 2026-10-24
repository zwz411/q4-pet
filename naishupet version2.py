import tkinter as tk
import math
import random

# 颜色配置
TRANSPARENT_COLOR = "#010203"
C_BODY = "#F9E07F"       # 奶鼠黄
C_EAR_IN = "#FADADD"     # 耳朵内侧粉
C_EYE_BG = "#E8F8F5"     # 眼白微绿
C_EYE_IRIS = "#4A3A30"   # 瞳孔
C_HOODIE = "#95A5A6"     # 灰色卫衣
C_HOODIE_DARK = "#7F8C8D"
C_PANTS = "#2C3E50"      # 墨蓝色裤子
C_DESK = "#D4A373"       # 桌子
C_CHAIR = "#6C7A89"      # 椅子
C_CHAIR_DARK = "#56616D"
C_COMPUTER = "#BDC3C7"   # 电脑外壳
C_SCREEN = "#2C3E50"     # 屏幕
C_CODE_LINES = ["#2ECC71", "#3498DB", "#F1C40F", "#E74C3C"]

class MilkMousePet:
    def __init__(self, root):
        self.root = root
        self.root.title("奶鼠桌宠")
        
        self.width = 400
        self.height = 400
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
         
        # 初始位置在右下角
        self.start_x = screen_w - self.width - 50
        self.start_y = screen_h - self.height - 100
        
        self.root.geometry(f"{self.width}x{self.height}+{self.start_x}+{self.start_y}")
        self.root.overrideredirect(True) # 无边框
        self.root.wm_attributes("-topmost", True) # 置顶
        self.root.wm_attributes("-transparentcolor", TRANSPARENT_COLOR) # 背景透明

        self.canvas = tk.Canvas(root, width=self.width, height=self.height, bg=TRANSPARENT_COLOR, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.tick = 0
        self.blink = 0
        self.state = "coding" # coding, looking, hitting
        self.drag_data = {"x": 0, "y": 0}
        self.mx, self.my = 0, 0
        self.hover_timer = None
        
        # 绑定事件
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<Motion>", self.on_motion)
        self.root.bind("<ButtonRelease-1>", self.on_release)

        self.draw_scene()
        self.update_loop()
        
    def draw_scene(self):
        self.canvas.delete("all")
        bob = math.sin(self.tick * 0.1) * 2 # 呼吸浮动
        
        self.draw_background()
        
        if self.state == "coding":
            self.draw_mouse_side(bob)
            self.draw_open_computer()
        elif self.state == "looking":
            self.draw_mouse_front(bob)
            self.draw_closed_computer()
        elif self.state == "hitting":
            self.draw_mouse_side(bob)
            self.draw_open_computer()
            self.draw_hitting_arm()
            
    def draw_background(self):
        # 椅子靠背和坐垫
        self.canvas.create_oval(110, 180, 290, 370, fill=C_CHAIR, outline=C_CHAIR_DARK, width=2)
        self.canvas.create_oval(130, 280, 270, 330, fill=C_CHAIR_DARK, outline="")
        # 椅子腿
        self.canvas.create_line(150, 320, 150, 380, width=6, fill=C_CHAIR_DARK)
        self.canvas.create_line(250, 320, 250, 380, width=6, fill=C_CHAIR_DARK)
        
        # 桌子
        self.canvas.create_rectangle(200, 270, 400, 290, fill=C_DESK, outline="")
        self.canvas.create_rectangle(220, 290, 240, 400, fill="#B08D6A", outline="") # 桌腿
        
    def draw_mouse_side(self, bob):
        # 尾巴
        self.canvas.create_line(130, 300, 80, 330, 70, 310, smooth=True, width=8, fill=C_BODY, capstyle=tk.ROUND)
        
        # 身体连体（去掉描边，同色重叠，完美融合）
        self.canvas.create_oval(150, 110 + bob, 240, 200 + bob, fill=C_BODY, outline="") # 头
        self.canvas.create_oval(140, 160 + bob, 240, 310 + bob, fill=C_BODY, outline="") # 肚子
        
        # 裤子
        self.canvas.create_oval(145, 260 + bob, 235, 320 + bob, fill=C_PANTS, outline="")
        self.canvas.create_oval(160, 300 + bob, 190, 325 + bob, fill=C_BODY, outline="") # 脚丫
        self.canvas.create_oval(200, 300 + bob, 230, 325 + bob, fill=C_BODY, outline="")
        
        # 灰色卫衣
        self.canvas.create_oval(135, 170 + bob, 245, 280 + bob, fill=C_HOODIE, outline="")
        self.canvas.create_oval(160, 150 + bob, 230, 200 + bob, fill=C_HOODIE, outline="") # 帽子
        self.canvas.create_oval(170, 160 + bob, 220, 190 + bob, fill=C_HOODIE_DARK, outline="") # 帽子内衬
        self.canvas.create_line(180, 190 + bob, 180, 220 + bob, fill="white", width=2) # 抽绳
        
        # 大耳朵
        self.canvas.create_oval(120, 70 + bob, 180, 130 + bob, fill=C_BODY, outline="")
        self.canvas.create_oval(135, 85 + bob, 165, 115 + bob, fill=C_EAR_IN, outline="")
        self.canvas.create_oval(190, 70 + bob, 250, 130 + bob, fill=C_BODY, outline="")
        self.canvas.create_oval(205, 85 + bob, 235, 115 + bob, fill=C_EAR_IN, outline="")
        
        # 脸部轮廓
        self.canvas.create_oval(155, 115 + bob, 235, 195 + bob, fill=C_BODY, outline="")
        
        # 侧眼
        if self.blink > 0:
            self.canvas.create_line(200, 145 + bob, 215, 145 + bob, width=2, fill="black")
        else:
            self.canvas.create_oval(200, 135 + bob, 218, 155 + bob, fill=C_EYE_BG, outline="black", width=2)
            self.canvas.create_oval(204, 139 + bob, 214, 149 + bob, fill=C_EYE_IRIS)
            self.canvas.create_oval(206, 141 + bob, 209, 144 + bob, fill="white")
            
        # 鼻子
        self.canvas.create_oval(225, 165 + bob, 235, 172 + bob, fill=C_EAR_IN, outline="")
        # 微笑嘴巴 (中间点y坐标大于两边，形成向上弯的U型)
        self.canvas.create_line(210, 175 + bob, 220, 182 + bob, 230, 175 + bob, smooth=True, width=2, fill="black")
        
        # 手部动作
        if self.state == "coding":
            hand_bob = math.sin(self.tick * 0.8) * 3
            self.canvas.create_line(150, 220 + bob, 230, 260 + bob + hand_bob, width=12, fill=C_HOODIE, smooth=True)
            self.canvas.create_oval(225, 255 + bob + hand_bob, 245, 270 + bob + hand_bob, fill=C_BODY, outline="")
        else:
            self.canvas.create_line(150, 220 + bob, 140, 260 + bob, width=12, fill=C_HOODIE, smooth=True)
            self.canvas.create_oval(130, 255 + bob, 150, 270 + bob, fill=C_BODY, outline="")

    def draw_mouse_front(self, bob):
        # 尾巴
        self.canvas.create_line(200, 310, 230, 350, 260, 340, smooth=True, width=8, fill=C_BODY, capstyle=tk.ROUND)
        
        # 身体连体
        self.canvas.create_oval(150, 110 + bob, 250, 200 + bob, fill=C_BODY, outline="")
        self.canvas.create_oval(140, 160 + bob, 260, 310 + bob, fill=C_BODY, outline="")
        
        # 裤子
        self.canvas.create_oval(145, 260 + bob, 255, 320 + bob, fill=C_PANTS, outline="")
        self.canvas.create_oval(160, 300 + bob, 195, 325 + bob, fill=C_BODY, outline="")
        self.canvas.create_oval(205, 300 + bob, 240, 325 + bob, fill=C_BODY, outline="")
        
        # 卫衣
        self.canvas.create_oval(135, 170 + bob, 265, 280 + bob, fill=C_HOODIE, outline="")
        self.canvas.create_oval(160, 150 + bob, 240, 200 + bob, fill=C_HOODIE, outline="")
        self.canvas.create_line(180, 190 + bob, 180, 220 + bob, fill="white", width=2)
        self.canvas.create_line(220, 190 + bob, 220, 220 + bob, fill="white", width=2)
        
        # 手
        self.canvas.create_line(140, 200 + bob, 120, 260 + bob, width=12, fill=C_HOODIE, smooth=True)
        self.canvas.create_line(260, 200 + bob, 280, 260 + bob, width=12, fill=C_HOODIE, smooth=True)
        self.canvas.create_oval(110, 255 + bob, 130, 270 + bob, fill=C_BODY, outline="")
        self.canvas.create_oval(270, 255 + bob, 290, 270 + bob, fill=C_BODY, outline="")
        
        # 耳朵
        self.canvas.create_oval(110, 70 + bob, 180, 140 + bob, fill=C_BODY, outline="")
        self.canvas.create_oval(130, 90 + bob, 160, 120 + bob, fill=C_EAR_IN, outline="")
        self.canvas.create_oval(220, 70 + bob, 290, 140 + bob, fill=C_BODY, outline="")
        self.canvas.create_oval(240, 90 + bob, 270, 120 + bob, fill=C_EAR_IN, outline="")
        
        # 脸
        self.canvas.create_oval(155, 115 + bob, 245, 195 + bob, fill=C_BODY, outline="")
        
        # 眼睛
        if self.blink > 0:
            self.canvas.create_line(175, 145 + bob, 190, 145 + bob, width=2, fill="black")
            self.canvas.create_line(210, 145 + bob, 225, 145 + bob, width=2, fill="black")
        else:
            for ex in [175, 210]:
                self.canvas.create_oval(ex, 135 + bob, ex+15, 155 + bob, fill=C_EYE_BG, outline="black", width=2)
                self.canvas.create_oval(ex+5, 139 + bob, ex+12, 149 + bob, fill=C_EYE_IRIS)
                self.canvas.create_oval(ex+7, 141 + bob, ex+10, 144 + bob, fill="white")
                
        # 鼻子和向上弯的微笑
        self.canvas.create_oval(195, 165 + bob, 205, 172 + bob, fill=C_EAR_IN, outline="")
        self.canvas.create_line(185, 175 + bob, 200, 182 + bob, 215, 175 + bob, smooth=True, width=2, fill="black")

    def draw_open_computer(self):
        self.canvas.create_polygon(240, 265, 340, 265, 350, 275, 230, 275, fill=C_COMPUTER, outline="")
        self.canvas.create_polygon(250, 180, 350, 180, 350, 265, 250, 265, fill=C_SCREEN, outline="")
        for i in range(6):
            y_pos = 190 + i * 10
            w = random.randint(20, 80) if random.random() > 0.3 else 0
            if w:
                self.canvas.create_rectangle(260, y_pos, 260 + w, y_pos + 6, fill=random.choice(C_CODE_LINES), outline="")

    def draw_closed_computer(self):
        self.canvas.create_polygon(230, 275, 350, 275, 350, 260, 230, 260, fill=C_COMPUTER, outline="")

    def draw_hitting_arm(self):
        # 手臂伸向鼠标
        self.canvas.create_line(230, 220, self.mx, self.my, width=12, fill=C_HOODIE, smooth=True)
        self.canvas.create_oval(self.mx-12, self.my-12, self.mx+12, self.my+12, fill=C_BODY, outline="")
        if self.tick % 10 < 5:
            self.canvas.create_line(self.mx-20, self.my-20, self.mx-30, self.my-30, width=2, fill="gray")
            self.canvas.create_line(self.mx+20, self.my-20, self.mx+30, self.my-30, width=2, fill="gray")

    def update_loop(self):
        self.tick += 1
        if self.blink > 0:
            self.blink -= 1
        elif random.random() < 0.02:
            self.blink = 8
        self.draw_scene()
        self.root.after(40, self.update_loop)

    def on_click(self, event):
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y
        
        # 点击切换合上/打开电脑
        if self.state == "coding":
            self.state = "looking"
        elif self.state == "looking":
            self.state = "coding"
            
        if self.hover_timer:
            self.root.after_cancel(self.hover_timer)
            self.hover_timer = None

    def on_drag(self, event):
        x = self.root.winfo_x() + (event.x - self.drag_data["x"])
        y = self.root.winfo_y() + (event.y - self.drag_data["y"])
        self.root.geometry(f"+{x}+{y}")

    def on_release(self, event):
        self.drag_data["x"] = 0
        self.drag_data["y"] = 0

    def on_motion(self, event):
        self.mx, self.my = event.x, event.y
        dist = math.hypot(event.x - 190, event.y - 200)
        
        # 鼠标靠近奶鼠身体时触发拍打动作
        if dist < 120 and self.state != "hitting" and self.state != "looking":
            self.state = "hitting"
            if self.hover_timer:
                self.root.after_cancel(self.hover_timer)
            self.hover_timer = self.root.after(1500, self.reset_hover)
        elif dist >= 120 and self.state == "hitting":
            self.reset_hover()
            
    def reset_hover(self):
        if self.state == "hitting":
            self.state = "coding"
        self.hover_timer = None

if __name__ == "__main__":
    root = tk.Tk()
    app = MilkMousePet(root)
    root.mainloop()
