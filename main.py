import copy
import time

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

import tracker
import cv2
from speed import e_speed, e_speed2
from yolov7tiny.yolo import YOLO

def det(video_path):
    # 根据视频尺寸，填充一个polygon，供撞线计算使用
    mask_image_temp = np.zeros((1080, 1920), dtype=np.uint8)

    # # 初始化2个撞线polygon
    list_pts_blue = [[54, 600], [67, 650], [605, 650], [1101, 650], [1900, 650], [1902, 600], [1125, 600], [604, 600],
                     [299, 600], [267, 600]]
    ndarray_pts_blue = np.array(list_pts_blue, np.int32)
    polygon_blue_value_1 = cv2.fillPoly(mask_image_temp, [ndarray_pts_blue], color=5)
    polygon_blue_value_1 = polygon_blue_value_1[:, :, np.newaxis]

    # 填充第二个polygon
    mask_image_temp = np.zeros((1080, 1920), dtype=np.uint8)
    list_pts_yellow = [[54, 700], [67, 800], [605, 800], [1101, 800], [1900, 800], [1902, 700], [1125, 700], [604, 700],
                       [299, 700], [267, 700]]
    ndarray_pts_yellow = np.array(list_pts_yellow, np.int32)
    polygon_yellow_value_2 = cv2.fillPoly(mask_image_temp, [ndarray_pts_yellow], color=2)
    polygon_yellow_value_2 = polygon_yellow_value_2[:, :, np.newaxis]

    # 撞线检测用mask，包含2个polygon，（值范围 0、1、2），供撞线计算使用
    polygon_mask_blue_and_yellow = polygon_blue_value_1 + polygon_yellow_value_2
    # print(polygon_mask_blue_and_yellow.shape)

    # 缩小尺寸，1920x1080->960x540
    polygon_mask_blue_and_yellow = cv2.resize(polygon_mask_blue_and_yellow, (960, 540))
    # for i in range(polygon_mask_blue_and_yellow.shape[0]):
    #     for j in range(polygon_mask_blue_and_yellow.shape[1]):
    #         if polygon_mask_blue_and_yellow[i][j]!=0:
    #             print(i,j)

    # 蓝 色盘 b,g,r
    blue_color_plate = [255, 0, 0]
    # 蓝 polygon图片
    blue_image = np.array(polygon_blue_value_1 * blue_color_plate, np.uint8)

    # 黄 色盘
    yellow_color_plate = [0, 255, 255]
    # 黄 polygon图片
    yellow_image = np.array(polygon_yellow_value_2 * yellow_color_plate, np.uint8)

    # 彩色图片（值范围 0-255）
    color_polygons_image = blue_image + yellow_image
    # 缩小尺寸，1920x1080->960x540
    color_polygons_image = cv2.resize(color_polygons_image, (960, 540))

    # list 与蓝色polygon重叠
    list_overlapping_blue_polygon = []

    # list 与黄色polygon重叠
    list_overlapping_yellow_polygon = []

    # 进入数量
    down_count = 0
    # 离开数量
    up_count = 0

    font_draw_number = cv2.FONT_HERSHEY_SIMPLEX
    draw_text_postion = (int(960 * 0.01), int(540 * 0.05))
    draw_text_postion1 = (int(960 * 0.01), int(540 * 0.1))
    draw_text_postion2 = (int(960 * 0.01), int(540 * 0.15))
    # 初始化 yolov5
    # detector = Detector()
    detector = YOLO()
    # # 打开视频
    capture = cv2.VideoCapture(video_path)
    fram = []
    i = 1
    speede = {1: 15.8, 2: 0.5, 3: 6.7, 4: 1.0, 5: 1.6, 6: 8.5, 7: 0.7, 8: 2.1, 9: 20.5, 10: 1.0}
    downspeedmean = 0
    upspeedmean = 0
    downsum = 0
    upsum = 0
    frame_count = 0
    pre_speed = {}
    q = []
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    size = (int(capture.get(cv2.CAP_PROP_FRAME_WIDTH)), int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    out = cv2.VideoWriter("./video/output3.mp4", fourcc, 30, size)
    fps = 0.0
    while True:
        start_time = time.time()
        # 读取每帧图片
        _, im = capture.read()
        if im is None:
            break
        frame_count += 1
        # 缩小尺寸，1920x1080->960x540
        im = cv2.resize(im, (960, 540))

        list_bboxs = []
        # 检测不到框，更换检测器*******************************************************************

        frame = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
        # 转变成Image
        frame = Image.fromarray(np.uint8(frame))
        bboxes = detector.detect_image(frame)
        fps = int(1 / (time.time() - start_time))
        # qianhouframe.append(bboxes)
        # output_image_frame = cv2.rectangle(im, [bboxes[1],bboxes[0],bboxes[3],bboxes[2]],(0, 255, 0),thickness=3, lineType=cv2.LINE_AA)
        # 如果画面中 有bbox
        if len(bboxes) > 0:
            # 一共53秒，1645帧，每秒30帧
            list_bboxs = tracker.update(bboxes, im)
            # print(list_bboxs)
            if len(fram) > 0 and i == 0:
                speede, downspeedmean, upspeedmean, downsum, upsum = e_speed(fram, list_bboxs)
            elif len(fram) > 0 and i % 3 == 0:
                speede, downspeedmean, upspeedmean, downsum, upsum, q = e_speed2(fram, list_bboxs, pre_speed, q)
            i += 1
            fram = copy.copy(list_bboxs)
            pre_speed = speede
            # print(pre_speed)

            # fram = list_bboxs
            # if len(list_bboxs) > 0:
            #     qianhouframe.append(list_bboxs)
            #     print(qianhouframe)
            #     if len(qianhouframe)>2:
            #         q+=1
            #         print(qianhouframe[q-1])
            #         print(qianhouframe[q])
            #         print('jieshu')
            # print(list_bboxs)
            # 画框
            # 撞线检测点，(x1，y1)，y方向偏移比例 0.0~1.0

            output_image_frame = tracker.draw_bboxes(im, list_bboxs, speede, line_thickness=None)
            pass
        else:
            # 如果画面中 没有bbox
            output_image_frame = im
        pass

        # 输出图片，包括两条撞线
        # output_image_frame = cv2.add(output_image_frame, color_polygons_image)
        if len(list_bboxs) > 0:
            # ----------------------判断撞线----------------------
            for item_bbox in list_bboxs:
                y1, x1, y2, x2, label, track_id = item_bbox
                # 撞线检测点，(x1，y1)，y方向偏移比例 0.0~1.0
                y1_offset = int(y1 + ((y2 - y1) * 0.6))
                x_offset = int((x1 + x2) * 0.5)
                # 撞线的点
                y = y1_offset
                x = x_offset
                # print(polygon_mask_blue_and_yellow[y, x])
                if polygon_mask_blue_and_yellow[y, x] == 5:
                    # 如果撞 蓝polygon
                    if track_id not in list_overlapping_blue_polygon:
                        list_overlapping_blue_polygon.append(track_id)
                    pass
                    # 判断 黄polygon list 里是否有此 track_id
                    # 有此 track_id，则 认为是 外出方向
                    if track_id in list_overlapping_yellow_polygon:
                        # 外出+1
                        up_count += 1
                        print(
                            f'类别: {label} | id: {track_id} | 上行撞线 | 上行撞线总数: {up_count}')
                        # 删除 黄polygon list 中的此id
                        list_overlapping_yellow_polygon.remove(track_id)
                        pass
                    else:
                        # 无此 track_id，不做其他操作
                        pass
                elif polygon_mask_blue_and_yellow[y, x] == 2:
                    # 如果撞 黄polygon
                    if track_id not in list_overlapping_yellow_polygon:
                        list_overlapping_yellow_polygon.append(track_id)
                    pass
                    # 判断 蓝polygon list 里是否有此 track_id
                    # 有此 track_id，则 认为是 进入方向
                    if track_id in list_overlapping_blue_polygon:
                        # 进入+1
                        down_count += 1
                        print(
                            f'类别: {label} | id: {track_id} | 下行撞线 | 下行撞线总数: {down_count}')
                        # 删除 蓝polygon list 中的此id
                        list_overlapping_blue_polygon.remove(track_id)
                        pass
                    else:
                        # 无此 track_id，不做其他操作
                        pass
                    pass
                else:
                    pass
                pass
            pass
            # ----------------------清除无用id----------------------
            list_overlapping_all = list_overlapping_yellow_polygon + list_overlapping_blue_polygon
            for id1 in list_overlapping_all:
                is_found = False
                for _, _, _, _, _, bbox_id in list_bboxs:
                    if bbox_id == id1:
                        is_found = True
                        break
                    pass
                pass
                if not is_found:
                    # 如果没找到，删除id
                    if id1 in list_overlapping_yellow_polygon:
                        list_overlapping_yellow_polygon.remove(id1)
                    pass
                    if id1 in list_overlapping_blue_polygon:
                        list_overlapping_blue_polygon.remove(id1)
                    pass
                pass
            list_overlapping_all.clear()
            pass
            # 清空list
            list_bboxs.clear()
            pass
        else:
            # 如果图像中没有任何的bbox，则清空list
            list_overlapping_blue_polygon.clear()
            list_overlapping_yellow_polygon.clear()
            pass
        pass
        downjam = 'False'
        upjam = 'False'
        if downsum > 5 and downspeedmean < 10:
            downjam = 'True'
        if upsum > 5 and upspeedmean < 10:
            upjam = 'True'
        text_draw = 'DOWN: ' + str(down_count) + \
                    ' , UP: ' + str(up_count)
        # ' , DownSpeed: ' + str(downspeedmean) + 'km/h' + ' , Jam: '+ str(jam)
        output_image_frame = cv2.putText(img=output_image_frame, text=text_draw,
                                         org=draw_text_postion,
                                         fontFace=font_draw_number,
                                         fontScale=1, color=(0, 0, 255), thickness=2)
        text_draw = 'DownSpeed: ' + str(downspeedmean) + 'km/h' + ' , Jam: ' + str(downjam)
        output_image_frame = cv2.putText(img=output_image_frame, text=text_draw,
                                         org=draw_text_postion1,
                                         fontFace=font_draw_number,
                                         fontScale=1, color=(0, 0, 255), thickness=2)
        text_draw = 'UpSpeed: ' + str(upspeedmean) + 'km/h' + ' , Jam: ' + str(upjam)
        output_image_frame = cv2.putText(img=output_image_frame, text=text_draw,
                                         org=draw_text_postion2,
                                         fontFace=font_draw_number,
                                         fontScale=1, color=(0, 0, 255), thickness=2)
        cv2.imshow('demo', output_image_frame)

        cv2.waitKey(1)
        out.write(output_image_frame)

        pass
    pass
    end_time = time.time()
    # print('cost %f second' % (end_time - start_time))
    # print(frame_count)
    # print()
    capture.release()
    out.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    video_path = r'./video/output2.mp4'
    det(video_path)
