# cyber_code

一个会自动敲命令的终端桌面程序，看起来像程序员正在工作。

命令会一个字一个字打出来，并给出对应的输出，包括 `ls`、`ps`、`tar`、`npm`、`java` / Spring Boot、`docker`、`redis`、`postgres`、`kafka`、`influx`、`nginx`、Linux 系统查看，以及 `kubectl` 等，片段会循环播放。

## 怎么打开

双击 `dist\cyber_code.exe`（打包后的独立程序，不需要安装 Python）。

也可以双击 `start_pyqt.bat`，或在本目录运行：

```
python terminal_app.py
```

需要已安装的 Python 和 PyQt6。终端字体会用 `fonts` 文件夹里的 JetBrains Mono，另外三款（Adwaita Mono、DejaVu Sans Mono、Ubuntu Sans Mono）也已一并加载；打包后的 exe 会自带这些字体。任务栏、窗口和托盘图标使用 `assets/cyber_code.ico`。

关闭窗口后程序会留在系统托盘。右键托盘图标可以切换字体和配色方案。设置会保存在程序旁边的 `settings.json`（运行 exe 时就在 exe 同一目录；直接运行 Python 脚本时则在脚本所在目录）。如果该位置无法写入，会改存到 `%APPDATA%\cyber_code\settings.json`。要从托盘完全退出，选「退出」。

## 重新打包

在本目录双击 `build_exe.bat`，或运行：

```
python -m PyInstaller --noconfirm --clean --windowed --onefile --name cyber_code --icon "assets/cyber_code.ico" --add-data "fonts;fonts" --add-data "assets/cyber_code.ico;assets" terminal_app.py
```

生成的程序在 `dist\cyber_code.exe`。
