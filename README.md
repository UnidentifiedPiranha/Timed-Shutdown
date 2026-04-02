# Timed-Shutdown 带计时的自动关机休眠睡眠小工具
A simple power operation software that allows for shutdown, hibernation, sleep, and screen closure, with a timing function.

一个简易的电源操作软件，允许关机、休眠、睡眠、以及单独关闭屏幕，带有计时功能



**CMD Usage:**

Shutdown 关机: `shutdown /s /t 0`

Hibernate 休眠: `shutdown /h`

Sleep 睡眠: `System.Windows.Forms.PowerState]::Suspend`

Screen-Shutdown 仅关闭屏幕: `WM_SYSCOMMAND` through `ctypes` 



Send signal to execute after given time.

软件内计时后发出信号执行。

