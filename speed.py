import math

x = [(376, 221, 539, 393, 2, 1), (84, 879, 120, 956, 2, 2), (141, 315, 195, 380, 2, 3), (110, 111, 154, 217, 2, 4), (70, 823, 111, 872, 2, 5), (149, 379, 239, 459, 2, 6), (180, 931, 262, 958, 0, 7), (92, 432, 126, 471, 2, 8), (215, 129, 372, 262, 2, 9), (142, 930, 193, 953, 0, 10)]
y = [(428, 210, 539, 368, 2, 1), (83, 877, 120, 957, 2, 2), (148, 303, 206, 372, 2, 3), (111, 114, 154, 219, 2, 4), (68, 818, 111, 871, 2, 5), (161, 369, 257, 454, 2, 6), (177, 929, 263, 958, 0, 7), (92, 426, 133, 471, 2, 8), (234, 91, 412, 243, 2, 9), (142, 928, 193, 951, 0, 10), (83, 19, 116, 58, 2, 13), (139, 904, 175, 916, 0, 14)]
def e_speed(pro, now):
    present_IDs = []
    prev_IDs = []
    work_IDs = []
    work_IDs_index = []
    work_IDs_prev_index = []
    work_locations = []  # 当前帧数据：中心点x坐标、中心点y坐标、目标序号、车辆类别、车辆像素宽度
    work_prev_locations = []  # 上一帧数据，数据格式相同
    speed = []
    downspeed = []
    upspeed=[]
    for (x1, y1, x2, y2, cls_id, pos_id) in now:
        check_point_x = int((x1 + x2) * 0.5)
        check_point_y = int(y1 + ((y2 - y1) * 0.6))
        present_IDs.append(pos_id)
    for (x1, y1, x2, y2, cls_id, pos_id) in pro:
        prev_IDs.append(pos_id)
    for m, n in enumerate(present_IDs):
        if n in prev_IDs:
            work_IDs.append(n)
            work_IDs_index.append(m)
    for x in work_IDs_index:
        work_locations.append(now[x])

    for y, z in enumerate(prev_IDs):
        if z in work_IDs:
            work_IDs_prev_index.append(y)
    for x in work_IDs_prev_index:
        work_prev_locations.append(pro[x])

    for i in range(len(work_IDs)):
        w = work_locations[i][3] - work_locations[i][1]

        y = int((work_locations[i][0] + work_locations[i][2]) * 0.5)
        ppm = w/3
        a = math.atan((540 - y)/100)
        # print(a*180/math.pi)

        b = 85 * math.pi/180
        speed.append(
                math.sqrt(
                    (int((work_locations[i][0] + work_locations[i][2]) * 0.5) - int(
                        (work_prev_locations[i][0] + work_prev_locations[i][2]) * 0.5)) ** 2 +
                    (int((work_locations[i][1] + work_locations[i][3]) * 0.5) - int(
                        (work_prev_locations[i][1] + work_prev_locations[i][3]) * 0.5)) ** 2
                ) / ppm * math.sin(a) * 3.6 * 30 / math.sin(a+b)
        )
        if int((work_locations[i][1] + work_locations[i][3]) * 0.5)<500:
            downspeed.append(
                    math.sqrt(
                        (int((work_locations[i][0] + work_locations[i][2]) * 0.5) - int(
                        (work_prev_locations[i][0] + work_prev_locations[i][2]) * 0.5)) ** 2 +
                        (int((work_locations[i][1] + work_locations[i][3]) * 0.5) - int(
                        (work_prev_locations[i][1] + work_prev_locations[i][3]) * 0.5)) ** 2
                        ) / ppm * math.sin(a) * 3.6 * 30 / math.sin(a+b)
            )
        else:
            upspeed.append(
                math.sqrt(
                    (int((work_locations[i][0] + work_locations[i][2]) * 0.5) - int(
                        (work_prev_locations[i][0] + work_prev_locations[i][2]) * 0.5)) ** 2 +
                    (int((work_locations[i][1] + work_locations[i][3]) * 0.5) - int(
                        (work_prev_locations[i][1] + work_prev_locations[i][3]) * 0.5)) ** 2
                ) / ppm * math.sin(a) * 3.6 * 30 / math.sin(a + b)
            )
        # if int((work_locations[i][0] + work_locations[i][2]) * 0.5) < 100:
        #     speed.append(
        #         math.sqrt(
        #             (int((work_locations[i][0] + work_locations[i][2]) * 0.5) - int(
        #                 (work_prev_locations[i][0] + work_prev_locations[i][2]) * 0.5)) ** 2 +
        #             (int((work_locations[i][1] + work_locations[i][3]) * 0.5) - int(
        #                 (work_prev_locations[i][1] + work_prev_locations[i][3]) * 0.5)) ** 2
        #         )*8
        #     )
        # elif int((work_locations[i][0] + work_locations[i][2]) * 0.5) < 300:
        #     speed.append(
        #         math.sqrt(
        #             (int((work_locations[i][0] + work_locations[i][2]) * 0.5) - int(
        #                 (work_prev_locations[i][0] + work_prev_locations[i][2]) * 0.5)) ** 2 +
        #             (int((work_locations[i][1] + work_locations[i][3]) * 0.5) - int(
        #                 (work_prev_locations[i][1] + work_prev_locations[i][3]) * 0.5)) ** 2
        #         )*4
        #     )
        # else:
        #     speed.append(
        #         math.sqrt(
        #             (int((work_locations[i][0]+work_locations[i][2])*0.5) - int((work_prev_locations[i][0]+work_prev_locations[i][2])*0.5))**2 +
        #             (int((work_locations[i][1] + work_locations[i][3]) * 0.5) - int((work_prev_locations[i][1] + work_prev_locations[i][3]) * 0.5)) ** 2
        #         )*12*math.exp(-0.003*(int((work_locations[i][0] + work_locations[i][2]) * 0.5)))
        #     )
    s = {}
    mean = round(sum(speed) / len(speed), 1)
    downmean = round(sum(downspeed) / len(downspeed), 1)
    if len(upspeed)!=0:
        upmean = round(sum(upspeed) / len(upspeed), 1)
    else:
        upmean = 0
    for i in range(len(speed)):
        s[work_locations[i][-1]] = round(speed[i], 1)

    return s,downmean,upmean,len(downspeed),len(upspeed)

# print(e_speed(x,y))

def e_speed2(pro, now, pre_speed,q):
    present_IDs = []
    prev_IDs = []
    work_IDs = []
    work_IDs_index = []
    work_IDs_prev_index = []
    work_locations = []  # 当前帧数据：中心点x坐标、中心点y坐标、目标序号、车辆类别、车辆像素宽度
    work_prev_locations = []  # 上一帧数据，数据格式相同
    speed = []
    downspeed = []
    upspeed=[]
    for (x1, y1, x2, y2, cls_id, pos_id) in now:
        check_point_x = int((x1 + x2) * 0.5)
        check_point_y = int(y1 + ((y2 - y1) * 0.6))
        present_IDs.append(pos_id)
    for (x1, y1, x2, y2, cls_id, pos_id) in pro:
        prev_IDs.append(pos_id)
    for m, n in enumerate(present_IDs):
        if n in prev_IDs:
            work_IDs.append(n)
            work_IDs_index.append(m)
    for x in work_IDs_index:
        work_locations.append(now[x])

    for y, z in enumerate(prev_IDs):
        if z in work_IDs:
            work_IDs_prev_index.append(y)
    for x in work_IDs_prev_index:
        work_prev_locations.append(pro[x])

    for i in range(len(work_IDs)):
        w = work_locations[i][3] - work_locations[i][1]

        y = int((work_locations[i][0] + work_locations[i][2]) * 0.5)
        ppm = w/3
        a = math.atan((540 - y)/100)
        # print(a*180/math.pi)

        b = 85 * math.pi/180
        speed.append(
                math.sqrt(
                    (int((work_locations[i][0] + work_locations[i][2]) * 0.5) - int(
                        (work_prev_locations[i][0] + work_prev_locations[i][2]) * 0.5)) ** 2 +
                    (int((work_locations[i][1] + work_locations[i][3]) * 0.5) - int(
                        (work_prev_locations[i][1] + work_prev_locations[i][3]) * 0.5)) ** 2
                ) / ppm * math.sin(a) * 3.6 * 30 / math.sin(a+b)
        )
        if int((work_locations[i][1] + work_locations[i][3]) * 0.5)<500:
            downspeed.append(
                    math.sqrt(
                        (int((work_locations[i][0] + work_locations[i][2]) * 0.5) - int(
                        (work_prev_locations[i][0] + work_prev_locations[i][2]) * 0.5)) ** 2 +
                        (int((work_locations[i][1] + work_locations[i][3]) * 0.5) - int(
                        (work_prev_locations[i][1] + work_prev_locations[i][3]) * 0.5)) ** 2
                        ) / ppm * math.sin(a) * 3.6 * 30 / math.sin(a+b)
            )
        else:
            upspeed.append(
                math.sqrt(
                    (int((work_locations[i][0] + work_locations[i][2]) * 0.5) - int(
                        (work_prev_locations[i][0] + work_prev_locations[i][2]) * 0.5)) ** 2 +
                    (int((work_locations[i][1] + work_locations[i][3]) * 0.5) - int(
                        (work_prev_locations[i][1] + work_prev_locations[i][3]) * 0.5)) ** 2
                ) / ppm * math.sin(a) * 3.6 * 30 / math.sin(a + b)
            )
        # if int((work_locations[i][0] + work_locations[i][2]) * 0.5) < 100:
        #     speed.append(
        #         math.sqrt(
        #             (int((work_locations[i][0] + work_locations[i][2]) * 0.5) - int(
        #                 (work_prev_locations[i][0] + work_prev_locations[i][2]) * 0.5)) ** 2 +
        #             (int((work_locations[i][1] + work_locations[i][3]) * 0.5) - int(
        #                 (work_prev_locations[i][1] + work_prev_locations[i][3]) * 0.5)) ** 2
        #         )*8
        #     )
        # elif int((work_locations[i][0] + work_locations[i][2]) * 0.5) < 300:
        #     speed.append(
        #         math.sqrt(
        #             (int((work_locations[i][0] + work_locations[i][2]) * 0.5) - int(
        #                 (work_prev_locations[i][0] + work_prev_locations[i][2]) * 0.5)) ** 2 +
        #             (int((work_locations[i][1] + work_locations[i][3]) * 0.5) - int(
        #                 (work_prev_locations[i][1] + work_prev_locations[i][3]) * 0.5)) ** 2
        #         )*4
        #     )
        # else:
        #     speed.append(
        #         math.sqrt(
        #             (int((work_locations[i][0]+work_locations[i][2])*0.5) - int((work_prev_locations[i][0]+work_prev_locations[i][2])*0.5))**2 +
        #             (int((work_locations[i][1] + work_locations[i][3]) * 0.5) - int((work_prev_locations[i][1] + work_prev_locations[i][3]) * 0.5)) ** 2
        #         )*12*math.exp(-0.003*(int((work_locations[i][0] + work_locations[i][2]) * 0.5)))
        #     )
    s = {}
    mean = round(sum(speed) / len(speed), 1)
    if len(downspeed) != 0:
        downmean = round(sum(downspeed) / len(downspeed), 1)
    else:
        downmean = 0
    if len(upspeed)!=0:
        upmean = round(sum(upspeed) / len(upspeed), 1)
    else:
        upmean = 0
    for i in range(len(speed)):
        if 7 in pre_speed:
            q.append(pre_speed[7])
        if work_locations[i][-1] in pre_speed:
            s[work_locations[i][-1]] = round((speed[i]*0.8 + 0.2 * pre_speed[work_locations[i][-1]]), 1)
        else:
            s[work_locations[i][-1]] = round(speed[i], 1)
    return s,downmean,upmean,len(downspeed),len(upspeed),q