# LINUX发布版
打包命令：
pyinstaller -F main.py
新建 ImageProcessorAPP-Vx.x.x-Linux 文件夹
把生成的build、dist、main.spec移动到该文件夹中
dist文件夹里加入含“西工大校徽标缩小.png”的Icons文件夹

## V1.0.2
1. 保存图片需要手动在图片名后面加文件扩展名（例：名字需要写成abc.png）
2. 不能切换中文输入法，输入中文，需要从别的地方粘贴中文过来
3. 无法默认保存在输入路径（需求：默认保存文件名为 *_edit.*）

## V1.0.8
1. 不应该删除原始图像文件
2. 设置的默认字体字号不对（应该分Windows和Linux系统，区别设置默认字体字号）
3. 笔刷粗细无法记录
4. 删除后无法打开新图片
5. 导入贴图后无法再导入图片替换当前编辑的图片
6. 无法按任意长宽比裁剪（需求：交互框里输入长宽比，按此比率裁剪）

# WINDOWS发布版
打包命令：
pyinstaller -i Icons/App.ico -F main.py -w
新建 ImageProcessorAPP-Vx.x.x-Windows 文件夹
把生成的build、dist、main.spec移动到该文件夹中
dist文件夹里加入含“西工大校徽标缩小.png”和“App.ico”的Icons文件夹

## V1.0.5
1. 通道提取不应该输出三通道，而应该输出单通道图
2. 打包时没有加入Icons文件夹
3. 关于选项里文字说明的学号、版本号未更新
4. 图像保存不下来，查原因是改代码时误删了一行

## V1.0.9
1. 渲染上去的字体大小比预览字体大小小几号（可能是Clip模态复用Editbox的原因）
2. 剪贴板输入的图片虽然有本地路径，但是没有默认保存路径文件名