from PyQt5 import QtCore, QtGui, QtWidgets

if __name__ == '__main__':
    # 初始化应用程序
    app = QtWidgets.QApplication([])

    # 新建QGraphicsView和QGraphicsScene实例
    view = QtWidgets.QGraphicsView()
    scene = QtWidgets.QGraphicsScene()

    # 填充第一张图片，并将其添加到QGraphicsScene实例中
    pixmap_path = "../InputImages/Fennec Fox.jpg"
    pixmap = QtGui.QPixmap(pixmap_path)
    pixmap_item = QtWidgets.QGraphicsPixmapItem(pixmap)
    scene.addItem(pixmap_item)

    # 加载第二张图片
    image_path = "../InputImages/Fennec Fox.jpg"
    image = QtGui.QPixmap(image_path)

    # 计算新图的大小和位置
    new_width = max(image.width(), pixmap.width())
    new_height = image.height() + pixmap.height()
    new_x = 0  # 在 x 轴方向位置不变
    new_y = pixmap.height()  # 在 y 轴方向拼接到原图的下方

    # 新建一个QGraphicsPixmapItem实例，填充第二张图片，并将其添加到QGraphicsScene实例中
    new_pixmap = QtWidgets.QGraphicsPixmapItem(image)
    new_pixmap.setPos(new_x, new_y)
    scene.addItem(new_pixmap)

    # 调整QGraphicsView的视口，确保新图能够完整显示
    view.fitInView(scene.sceneRect(), QtCore.Qt.KeepAspectRatio)

    # 将QGraphicsView实例显示出来
    view.setScene(scene)
    view.show()

    # 运行应用程序
    app.exec_()
