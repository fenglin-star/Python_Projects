#coding=utf-8
node = ["幼儿心理研究","幼儿生理研究","学校环境对幼儿情绪的影响","家庭环境对幼儿情绪的影响","教师对幼儿情绪的影响","教学内容、教学方式对幼儿情绪的影响","同学、伙伴对幼儿情绪的影响","幼儿情绪研究"]

node1= ["情绪管理","情绪调节","情绪能力","情绪智力","心理健康","情绪体验",]
node2= ["婴幼儿","0-6岁的幼儿","孩子","小班幼儿"]
node3= ["幼儿园","校园环境","小班幼儿","绘本","游戏","幼儿园环境","家园共育"]
node4= ["家庭","父母","关爱","家庭教育","家园共育"]
node5= ["幼儿教师","教师"]
node6= ["教育活动","教育环境","教育策略","培养","幼儿教育","情绪教育","策略","绘本","游戏"]
node7= ["小班幼儿","同伴接纳"]
node8= ["不良情绪","情绪理解","负面情绪","情绪反应","幼儿情绪","消极情绪","积极情绪","情绪情感"]


def Nodes():
    data = "category: {}, name: {}, value: {}"
    for i in node:
        i = "'" + i + "'"
        txt = data.format("1",str(i),"7")
        txt = "{" + txt + "},"
        txt = txt.replace(" ","")
        print(txt)

    for i in node1:
        i = "'" + i + "'"
        txt = data.format("2",str(i),"4")
        txt = "{" + txt + "},"
        txt = txt.replace(" ","")
        print(txt)

    for i in node2:
        i = "'" + i + "'"
        txt = data.format("2",str(i),"4")
        txt = "{" + txt + "},"
        txt = txt.replace(" ","")
        print(txt)

    for i in node3:
        i = "'" + i + "'"
        txt = data.format("2",str(i),"4")
        txt = "{" + txt + "},"
        txt = txt.replace(" ","")
        print(txt)

    for i in node4:
        i = "'" + i + "'"
        txt = data.format("2",str(i),"4")
        txt = "{" + txt + "},"
        txt = txt.replace(" ","")
        print(txt)

    for i in node5:
        i = "'" + i + "'"
        txt = data.format("2",str(i),"4")
        txt = "{" + txt + "},"
        txt = txt.replace(" ","")
        print(txt)

    for i in node6:
        i = "'" + i + "'"
        txt = data.format("2",str(i),"4")
        txt = "{" + txt + "},"
        txt = txt.replace(" ","")
        print(txt)

    for i in node7:
        i = "'" + i + "'"
        txt = data.format("2",str(i),"4")
        txt = "{" + txt + "},"
        txt = txt.replace(" ","")
        print(txt)

    for i in node8:
        i = "'" + i + "'"
        txt = data.format("2",str(i),"4")
        txt = "{" + txt + "},"
        txt = txt.replace(" ","")
        print(txt)


def links():
    data = "source: {}, target: '{}', weight: {}"
    for i in node:
        i = "'" + i + "'"
        txt = data.format(str(i),"幼儿情绪","2")
        txt = "{" + txt + "},"
        txt = txt.replace(" ", "")
        print(txt)

    for i in node1:
        i = "'" + i + "'"
        txt = data.format(str(i),node[0],"2")
        txt = "{" + txt + "},"
        txt = txt.replace(" ", "")
        print(txt)

    for i in node2:
        i = "'" + i + "'"
        txt = data.format(str(i),node[1],"2")
        txt = "{" + txt + "},"
        txt = txt.replace(" ", "")
        print(txt)

    for i in node3:
        i = "'" + i + "'"
        txt = data.format(str(i),node[2],"2")
        txt = "{" + txt + "},"
        txt = txt.replace(" ", "")
        print(txt)

    for i in node4:
        i = "'" + i + "'"
        txt = data.format(str(i),node[3],"2")
        txt = "{" + txt + "},"
        txt = txt.replace(" ", "")
        print(txt)

    for i in node5:
        i = "'" + i + "'"
        txt = data.format(str(i),node[4],"2")
        txt = "{" + txt + "},"
        txt = txt.replace(" ", "")
        print(txt)

    for i in node6:
        i = "'" + i + "'"
        txt = data.format(str(i),node[5],"2")
        txt = "{" + txt + "},"
        txt = txt.replace(" ", "")
        print(txt)

    for i in node7:
        i = "'" + i + "'"
        txt = data.format(str(i),node[6],"2")
        txt = "{" + txt + "},"
        txt = txt.replace(" ", "")
        print(txt)

    for i in node8:
        i = "'" + i + "'"
        txt = data.format(str(i),node[7],"2")
        txt = "{" + txt + "},"
        txt = txt.replace(" ", "")
        print(txt)

if __name__ == '__main__':
    links()