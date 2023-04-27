def saveHashSets(path,hashsets):

    f = open(path, 'w', encoding='utf-8')  # 以'w'方式打开文件
    for k, v in hashsets.items():  # 遍历字典中的键值
        s2 = str(v)  # 把字典的值转换成字符型
        f.write(str(k) + '\n')  # 键和值分行放，键在单数行，值在双数行
        f.write(s2 + '\n')
    f.close()

def readHashSets(path):
    f = open(path, 'r', encoding='utf-8')
    information = f.readlines()  # 用readlines()函数读取txt文件中的内容，返回值为列表
    L1 = []  # 用来接收键的列表
    L2 = []  # 用来接收值的列表
    D2 = {}  # 用来存放文件中读取出的内容
    for i in range(len(information)):
        if i % 2 == 0:  # 列表下标是从0开始，所以双数行是键，单数行是值
            s1 = information[i][0:-1]  # readlines()函数读取文件会有\n，切片切掉
            L1.append(int(s1))  # 把所有的键存在L1列表中
        else:
            s2 = information[i]
            s2 = s2[1:-2]  # 切掉列表转换成字符串后左右的中括号
            s2 = s2.replace('\'', '').replace(' ', '')  # 把字符串中的单引号和空格去掉
            L3 = s2.split(',')  # 把字符串以逗号隔开变成列表，还原成原字典中的值
            L3=list(map(int,L3))
            L2.append(L3)  # 把值都存在列表L2中
    for n in range(len(L1)):
        D2[L1[n]] = L2[n]  # 以L1中的值为键，L2中的值为值存回字典中
    f.close()

    return D2

