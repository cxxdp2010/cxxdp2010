#TempConvert.py
val=input("请输入带有温度表示符号的温度值（例如：23C）：")
if val[-1] in ['c','C']:
    f=1.8*float(val[0:-1])+32
    print("转换后的温度为:%.2fF"%f)
elif val[-1] in ['f','F']:
    c=(float(val[0:-1])-32)/1.8
    print("转换后的温度为：%.2fC"%c)
else:
    print("输入有误")
