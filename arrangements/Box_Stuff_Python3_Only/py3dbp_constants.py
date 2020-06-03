class RotationType:
    RT_WHD = 0
    RT_HWD = 1
    RT_HDW = 2
    RT_DHW = 3
    RT_DWH = 4
    RT_WDH = 5

    #ALL = [RT_WHD, RT_HWD, RT_HDW, RT_DHW, RT_DWH, RT_WDH]
    ALL=[ele for ele in range(0,16)]

class Axis:
    WIDTH = 0
    HEIGHT = 1
    DEPTH = 2
    WIDTH_HEIGHT=3
    WIDTH_DEPTH=4
    HEIGHT_DEPTH=5
    WIDTH_HEIGHT_DEPTH=6
    #ORIGIN=6

    ALL = [ele for ele in range(0,8)]

