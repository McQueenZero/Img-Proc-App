import cv2
import numpy as np

if __name__ == '__main__':
    path = "../InputImages/lena.jpg"
    img = cv2.imread(path)
    H_rows, W_cols = img.shape[:2]
    print(H_rows, W_cols)

    # 原图中书本的四个角点(右下、右上、左上、左下),与变换后矩阵位置
    '''
    |--------→x
    |
    |
    ↓
    y
    [x, y]
    '''
    pts1 = np.float32([[400, 400], [500, 200], [300, 200], [200, 400], ])
    pts2 = np.float32([[H_rows, W_cols], [W_cols, 0], [0, 0], [0, H_rows], ])

    # 生成透视变换矩阵；进行透视变换
    M = cv2.getPerspectiveTransform(pts1, pts2)
    dst = cv2.warpPerspective(img, M, (512, 512))

    cv2.imshow("original_img", img)
    cv2.imshow("result", dst)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

