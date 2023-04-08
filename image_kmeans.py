import numpy as np
import cv2

if __name__ == '__main__':
    path = "./InputImages/Fennec Fox.jpg"
    img = cv2.imdecode(np.fromfile(path, dtype=np.uint8), -1)
    # img = cv2.imread(path)
    h, w, ch = img.shape
    data = img.reshape((-1, 3))
    data = np.float32(data)

    # 图像分割
    # MAX_ITER最大迭代次数，EPS最高精度
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    num_cluster = 3
    ret, label, center = cv2.kmeans(data, num_cluster, None, criteria, num_cluster, cv2.KMEANS_RANDOM_CENTERS)
    # label = np.squeeze(label)
    center = np.uint8(center)

    # color = np.uint8([[255, 0, 0],
    #                   [0, 0, 255],
    #                   [128, 128, 128]])

    # res = color[np.squeeze(label)]
    # print(res.shape)

    # result = res.reshape((img.shape))
    # cv2.imshow("demo", result)

    # 背景颜色替换
    # 生成mask区域
    index = label[0][0]
    center = np.uint8(center)
    color = center[0]
    mask = np.ones((h, w), dtype=np.uint8) * 255
    label = np.reshape(label, (h, w))
    mask[label == index] = 0

    # 高斯模糊
    se = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    # 膨胀，防止出现背景
    cv2.erode(mask, se, mask)
    # 边缘模糊
    mask = cv2.GaussianBlur(mask, (5, 5), 0)
    mask = np.expand_dims(mask, axis=2)
    # mask = mask[..., None]
    # 白色背景
    # bg = np.ones(img.shape, dtype=np.float32)*255
    # 红色背景
    red_bg = np.array([0, 0, 255])
    bg = np.tile(red_bg, (h, w, 1))

    alpha = mask.astype(np.float32) / 255.
    fg = alpha * img

    new_image = np.uint8(fg + (1 - alpha) * bg)

    cv2.imshow("white", np.hstack([img, new_image]))
    cv2.waitKey(0)
