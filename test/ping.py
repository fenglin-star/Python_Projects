from ping3 import ping

import dns.resolver


def a():
    A = dns.resolver.query('www.laosiji.com','A')			#指定查询类型为A记录
    for i in A.response.answer:								#response.answer方法获取查询回应信息
        for j in i.items:									#遍历回应信息
            print(j.address)


def ping_host(ip):
    """
    获取节点的延迟的作用
    :param node:
    :return:
    """
    ip_address = ip
    response = ping(ip_address)
    # print(response)
    if response is not None:
        delay = int(response * 1000)
        # print(delay, "延迟")
        return delay
    else:
        return "False"
        # 下面两行新增的


def ping_list(ip):
    """
    获取节点的延迟的作用
    :param node:
    :return:
    """
    ip_address = ip
    response = ping(ip_address)
    # print(response)
    if response is not None:
        delay = int(response * 1000)
        # print(delay, "延迟")
        return delay
    else:
        return "False"
        # 下面两行新增的


for i in range(1,10):
    print("第{}".format(i) + "次测试: ",ping_host("104.16.148.27"))

if __name__ == '__main__':
    a()