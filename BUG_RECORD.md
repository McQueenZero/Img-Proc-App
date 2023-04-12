# LINUX发布版
打包命令：
pyinstaller -F main.py -o ImageProcessorAPP-Vx.x.x-Linux
dist文件夹里加入含“西工大校徽标缩小.png”的Icons文件夹
## V1.0.2
1. 保存图片需要手动在图片名后面加文件扩展名（例：名字需要写成abc.png）
2. 不能切换中文输入法，输入中文，需要从别的地方粘贴中文过来
3. 默认保存在输入路径，默认保存文件名为 *_edit.*

# WINDOWS发布版
打包命令：
pyinstaller -i Icons/App.ico -F main.py -w -o ImageProcessorAPP-Vx.x.x-Windows
dist文件夹里加入含“西工大校徽标缩小.png”和“App.ico”的Icons文件夹
## V1.0.5
1. 通道提取改成输出单通道图
2. 打包时加入Icons文件夹
3. 修改关于选项里的文字说明
4. 图像保存不下来，查原因是改代码时误删了一行