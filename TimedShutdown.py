import tkinter as tk
from tkinter import messagebox
import os
import threading
import time
import subprocess
import ctypes # 新增：用于调用Windows底层接口

class ShutdownTool:
    def __init__(self, root):
        self.root = root
        self.root.title("电脑定时助手 v4.0")
        self.root.geometry("380x350")
        self.root.config(padx=20, pady=20)
        
        self.running = False
        self.remaining_time = 0

        # --- UI 界面布局 ---
        tk.Label(root, text="执行操作", font=("微软雅黑", 10, "bold")).pack()
        
        radio_frame = tk.Frame(root)
        radio_frame.pack(pady=10)
        
        self.action_var = tk.StringVar(value="shutdown")
        # 新增了“仅熄屏”选项
        tk.Radiobutton(radio_frame, text="关机", variable=self.action_var, value="shutdown").grid(row=0, column=0, padx=5)
        tk.Radiobutton(radio_frame, text="睡眠", variable=self.action_var, value="sleep").grid(row=0, column=1, padx=5)
        tk.Radiobutton(radio_frame, text="休眠", variable=self.action_var, value="hibernate").grid(row=0, column=2, padx=5)
        tk.Radiobutton(radio_frame, text="仅熄屏", variable=self.action_var, value="monitor_off").grid(row=1, column=0, columnspan=3, pady=5)

        tk.Label(root, text="设定时间 (分钟, 0为立即执行):", font=("微软雅黑", 9)).pack()
        self.entry = tk.Entry(root, justify='center', font=("Arial", 12), width=10)
        self.entry.insert(0, "30") 
        self.entry.pack(pady=5)

        self.lbl_status = tk.Label(root, text="等待指令...", fg="#666", font=("微软雅黑(italic)", 14, "bold"))
        self.lbl_status.pack(pady=15)

        self.btn_start = tk.Button(root, text="开始任务", command=self.start_task, 
                                 bg="#0078D7", fg="white", width=20, height=2, relief=tk.FLAT)
        self.btn_start.pack(pady=5)

        self.btn_stop = tk.Button(root, text="取消任务", command=self.stop_timer, 
                                state=tk.DISABLED, width=20, relief=tk.FLAT)
        self.btn_stop.pack(pady=10)

    def start_task(self):
        try:
            mins = float(self.entry.get())
            if mins < 0: raise ValueError
            self.remaining_time = int(mins * 60)
        except ValueError:
            messagebox.showerror("错误", "请输入有效的数字")
            return

        if self.remaining_time == 0:
            self.execute_action()
            return

        self.running = True
        self.btn_start.config(state=tk.DISABLED, bg="#ccc")
        self.btn_stop.config(state=tk.NORMAL)
        self.entry.config(state=tk.DISABLED)
        self.lbl_status.config(fg="#E81123") 
        
        threading.Thread(target=self.countdown, daemon=True).start()

    def countdown(self):
        while self.remaining_time > 0 and self.running:
            mins, secs = divmod(self.remaining_time, 60)
            self.lbl_status.config(text=f"倒计时: {int(mins):02d}:{int(secs):02d}")
            time.sleep(1)
            self.remaining_time -= 1
        
        if self.running:
            self.root.after(0, self.execute_action)

    def stop_timer(self):
        self.running = False
        self.lbl_status.config(text="任务已取消", fg="#666")
        self.reset_ui()

    def reset_ui(self):
        self.btn_start.config(state=tk.NORMAL, bg="#0078D7")
        self.btn_stop.config(state=tk.DISABLED)
        self.entry.config(state=tk.NORMAL)

    def execute_action(self):
        action = self.action_var.get()
        
        if action == "shutdown":
            os.system("shutdown /s /t 0")
        elif action == "hibernate":
            os.system("shutdown /h")
        elif action == "sleep":
            ps_cmd = "Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.Application]::SetSuspendState([System.Windows.Forms.PowerState]::Suspend, $false, $false)"
            subprocess.run(["powershell", "-Command", ps_cmd])
        elif action == "monitor_off":
            # --- 关键代码：仅熄屏 ---
            # 为了防止点击按钮的手感/震动立刻唤醒屏幕，先缓0.5秒
            time.sleep(0.5)
            # 参数说明: 0xFFFF(所有窗口), 0x0112(WM_SYSCOMMAND), 0xF170(SC_MONITORPOWER), 2(关闭)
            ctypes.windll.user32.SendMessageW(0xFFFF, 0x0112, 0xF170, 2)
        
        self.reset_ui()
        self.lbl_status.config(text="指令已执行", fg="#4CAF50")

if __name__ == "__main__":
    root = tk.Tk()
    app = ShutdownTool(root)
    root.mainloop()