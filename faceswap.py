#! /usr/bin/env python
# -*- coding: utf-8 -*-
import urllib.request
import time
from PIL import Image
import cv2
import numpy as np
from numpy import *
from matplotlib import pyplot as plt
import urllib
import base64
import json
import sys
import numpy as np
import cv2
import requests
from json import JSONDecoder
from pylab import *


def get_points(filepath,key,secret ):

    url = 'https://api-cn.faceplusplus.com/facepp/v3/detect'
    # 要调用API的URL

    # face++提供的一对密钥
    data = {"api_key": key, "api_secret": secret, 'return_landmark': 1}
    # 必需的参数，key、secret均为字符串，1表示83个关键点，
	#可以改成2，表示106个关键点

    files = {"image_file": open(filepath, "rb")}
    '''以二进制读入图像，
    这个字典中open(filepath1, "rb")返回的是二进制的图像文件，
    所以"image_file"是二进制文件，符合官网的要求'''
    response = requests.post(url, data=data, files=files)
    # POTS上传

    req_con = response.content.decode('utf-8')
    # response的内容是JSON格式
    req_dict = JSONDecoder().decode(req_con)
    # 对其解码成字典格式
    faceData = req_dict['faces'][0]['landmark']
    points = []
    for value in faceData.values():
        points.append((int(value['x']),int(value['y'])))

    return points



# 定义仿射变换函数
#srcimg, srcimgTri表示源图和源图需要仿射的三角区域
#dstimgTri, size表示目标图的三角区域和结果的大小
def AffineTransform(srcimg, srcimgTri, dstimgTri, size):
    Matrix = cv2.getAffineTransform(np.float32(srcimgTri), np.float32(dstimgTri))
	#获取仿射变换函数
    dstimg = cv2.warpAffine(srcimg, Matrix, (size[0], size[1]), None, flags=cv2.INTER_LINEAR,\
                         borderMode=cv2.BORDER_REFLECT_101)
	#应用仿射变换函数
    return dstimg


# 定义函数，检查点是否在矩形区域
def inrect(rect, point):
    if point[0] < rect[0]:
        return False
    elif point[1] < rect[1]:
        return False
    elif point[0] > rect[0] + rect[2]:
        return False
    elif point[1] > rect[1] + rect[3]:
        return False
    return True


# 定义函数，计算德劳内三角
def DelaunayTriangles(rect, points):
    #openCV中的Subdiv2D函数可以帮我们计算德劳内三角
    subdiv = cv2.Subdiv2D(rect);

    for p in points:
        subdiv.insert(p)

    triangleList = subdiv.getTriangleList();

    delaunayTri = []

    pt = []

    for t in triangleList:
        pt.append((t[0], t[1]))
        pt.append((t[2], t[3]))
        pt.append((t[4], t[5]))

        pt1 = (t[0], t[1])
        pt2 = (t[2], t[3])
        pt3 = (t[4], t[5])

        if inrect(rect, pt1) and inrect(rect, pt2) and inrect(rect, pt3):
            ind = []
            # 从我们的83（或者108）个关键点集中确定三个点
            for j in range(0, 3):
                for k in range(0, len(points)):
                    if (abs(pt[j][0] - points[k][0]) < 1.0 and abs(pt[j][1] - points[k][1]) < 1.0):
                        ind.append(k)
                        # 三角形需要三个点确定
            if len(ind) == 3:
                delaunayTri.append((ind[0], ind[1], ind[2]))

        pt = []

    return delaunayTri


#定义函数，用来进行三角形区域的变换
def warpTriangle(img1, img2, t1, t2):
    # Find bounding rectangle for each triangle
    r1 = cv2.boundingRect(np.float32([t1]))
    r2 = cv2.boundingRect(np.float32([t2]))

    t1Rect = []
    t2Rect = []
    t2RectInt = []

    for i in range(0, 3):
        t1Rect.append(((t1[i][0] - r1[0]), (t1[i][1] - r1[1])))
        t2Rect.append(((t2[i][0] - r2[0]), (t2[i][1] - r2[1])))
        t2RectInt.append(((t2[i][0] - r2[0]), (t2[i][1] - r2[1])))

    # 将所有三角形组合成人脸区域
    mask = np.zeros((r2[3], r2[2], 3), dtype=np.float32)
    cv2.fillConvexPoly(mask, np.int32(t2RectInt), (1.0, 1.0, 1.0), 16, 0);

    # 对小区域进行仿射变换
    img1Rect = img1[r1[1]:r1[1] + r1[3], r1[0]:r1[0] + r1[2]]


    size = (r2[2], r2[3])

    img2Rect = AffineTransform(img1Rect, t1Rect, t2Rect, size)

    img2Rect = img2Rect * mask

    # 将三角形区域复制到输出图片
    img2[r2[1]:r2[1] + r2[3], r2[0]:r2[0] + r2[2]] = img2[r2[1]:r2[1] + r2[3], r2[0]:r2[0] + r2[2]] * (
                (1.0, 1.0, 1.0) - mask)

    img2[r2[1]:r2[1] + r2[3], r2[0]:r2[0] + r2[2]] = img2[r2[1]:r2[1] + r2[3], r2[0]:r2[0] + r2[2]] + img2Rect


if __name__ == '__main__':

    # openCV的版本确认
    #(major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')

    #if int(major_ver) < 3:
        #print >> sys.stderr, 'ERROR: Script needs OpenCV 3.0 or higher'
        #sys.exit(1)

    # 读取图片
    filename1 = 'leo.jpg'
    filename2 = 'memsi.jpg'

    img1 = cv2.imread(filename1)
    img2 = cv2.imread(filename2)
    img1Warped = np.copy(img2)

    try:
        key = "3ladvH4L7prwFJE7FC2uGJTqBWAO19fA"
        secret = "9w24kPHsuSovWV3ZZo62T2EodaQAAs1U"

        # Read array of corresponding points
        points1 = get_points(filename1,key,secret)
        points2 = get_points(filename2,key,secret)
    except KeyError:
        key = "VIWAgKDyNLWLq8nK_s1ZdWOL_aMl444f"
        secret = "HKteJJiDYQ0FTCOH2aCZIIe4U5Iv8fej"
        #因为face++的API不能在短时间内连续使用，所以我们用两个账号，交替使用

        # 读取关键点数据
        points1 = get_points(filename1,key,secret)
        points2 = get_points(filename2,key,secret)

    # 寻找凸包
    hull1 = []
    hull2 = []

    hullIndex = cv2.convexHull(np.array(points2), returnPoints=False)

    for i in range(0, len(hullIndex)):
        hull1.append(points1[int(hullIndex[i])])
        hull2.append(points2[int(hullIndex[i])])

    # 德劳内三角划分
    sizeImg2 = img2.shape
    rect = (0, 0, sizeImg2[1], sizeImg2[0])

    dt = DelaunayTriangles(rect, hull2)

    if len(dt) == 0:
        quit()

    # 进行仿射变换
    for i in range(0, len(dt)):
        t1 = []
        t2 = []

        # 从两张图中寻找对应的三角区域
        for j in range(0, 3):
            t1.append(hull1[dt[i][j]])
            t2.append(hull2[dt[i][j]])

        warpTriangle(img1, img1Warped, t1, t2)

    # 计算人脸区域
    hull8U = []
    for i in range(0, len(hull2)):
        hull8U.append((hull2[i][0], hull2[i][1]))

    mask = np.zeros(img2.shape, dtype=img2.dtype)

    cv2.fillConvexPoly(mask, np.int32(hull8U), (255, 255, 255))

    r = cv2.boundingRect(np.float32([hull2]))

    center = ((r[0] + int(r[2] / 2), r[1] + int(r[3] / 2)))

    # 调用seamlesslyClone函数，对人脸变换进行优化.
    output = cv2.seamlessClone(np.uint8(img1Warped), img2, mask, center, cv2.NORMAL_CLONE)

    cv2.imshow("Face Swapped", output)
    cv2.waitKey(0)
    cv2.imwrite('output.jpg',output)

    cv2.destroyAllWindows()