from dijkstar import Graph, find_path

graph=Graph() #建立坐标系
graph.add_edge(1,2,{'cost':45}) #节点1到节点2，距离56单位
graph.add_edge(1,8,{'cost':44}) #节点1到节点8，距离39单位
graph.add_edge(1,9,{'cost':38}) #节点1到节点9，距离34单位
graph.add_edge(2,7,{'cost':8.8}) #以此类推将节点到其它节点的距离都加入坐标系就可以了
graph.add_edge(2,8,{'cost':3})
graph.add_edge(3,5,{'cost':2})
graph.add_edge(3,6,{'cost':1.8})
graph.add_edge(3,8,{'cost':1})
graph.add_edge(3,10,{'cost':1})
graph.add_edge(3,11,{'cost':1})
graph.add_edge(4,5,{'cost':2})
graph.add_edge(4,9,{'cost':6.1})
graph.add_edge(4,10,{'cost':3})
graph.add_edge(4,12,{'cost':13})
graph.add_edge(5,6,{'cost':3.3})
graph.add_edge(5,10,{'cost':1.5})
graph.add_edge(5,12,{'cost':16})
graph.add_edge(6,11,{'cost':2.5})
graph.add_edge(6,12,{'cost':13})
graph.add_edge(7,8,{'cost':12})
graph.add_edge(7,11,{'cost':11})
graph.add_edge(8,10,{'cost':1})
graph.add_edge(8,11,{'cost':1})
graph.add_edge(9,10,{'cost':9})

graph.add_edge(2,1,{'cost':45})
graph.add_edge(8,1,{'cost':44})
graph.add_edge(9,1,{'cost':38})
graph.add_edge(7,2,{'cost':8.8})
graph.add_edge(8,2,{'cost':3})
graph.add_edge(5,3,{'cost':2})
graph.add_edge(6,3,{'cost':1.8})
graph.add_edge(8,3,{'cost':1})
graph.add_edge(10,3,{'cost':1})
graph.add_edge(11,3,{'cost':1})
graph.add_edge(5,4,{'cost':2})
graph.add_edge(9,4,{'cost':6.1})
graph.add_edge(10,4,{'cost':3})
graph.add_edge(12,4,{'cost':13})
graph.add_edge(6,5,{'cost':3.3})
graph.add_edge(10,5,{'cost':1.5})
graph.add_edge(12,5,{'cost':16})
graph.add_edge(11,6,{'cost':2.5})
graph.add_edge(12,6,{'cost':13})
graph.add_edge(8,7,{'cost':12})
graph.add_edge(11,7,{'cost':11})
graph.add_edge(10,8,{'cost':1})
graph.add_edge(11,8,{'cost':1})
graph.add_edge(10,9,{'cost':9})


count_paths=[]


def shortestAB(A,B):
    cost_func = lambda u, v, e, prev_e: e['cost']
    shortest_path = find_path(graph, A, B, cost_func=cost_func) #查找节点4到7的最短距离
    if len(shortest_path.nodes) == 2:
        # print(A,shortest_path.nodes[1])
        return shortest_path.nodes[1]



def yilde_nodes(A,use_list):
    list = []
    num_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    for move in use_list:
        num_list.remove(move)
    for i in num_list:
        if shortestAB(A, i) == None:
            pass
        else:
            list.append(shortestAB(A, i))
    return list



def shortest_path(path_list):
    total_cost_list = []
    for i in range(0,len(path_list)-1):
        total_cost_list.append([path_list[i],path_list[i+1]])

    return_shortest_path =0

    for s in total_cost_list:
        cost_func = lambda u, v, e, prev_e: e['cost']
        shortest_path = find_path(graph, s[0], s[1], cost_func=cost_func) #查找节点4到7的最短距离
        return_shortest_path = return_shortest_path + shortest_path.total_cost

    # print('最短行程路径：',path_list,' 共行程：',return_shortest_path)
    return [return_shortest_path,path_list]




if __name__ == '__main__':
    a=1  #以几号节点为起点

    for b in yilde_nodes(a,[1]): #不回头、找最短距离
        for c in yilde_nodes(b,[1,b]):
            for d in yilde_nodes(c,[1,b,c]):
                for e in yilde_nodes(d,[1,b,c,d]):
                    for f in yilde_nodes(e,[1,b,c,d,e]):
                        for g in yilde_nodes(f,[1,b,c,d,e,f]):
                            for h in yilde_nodes(g,[1,b,c,d,e,f,g]):
                                for i in yilde_nodes(h,[1,b,c,d,e,f,g,h]):
                                    for j in yilde_nodes(i,[1,b,c,d,e,f,g,h,i]):
                                        for k in yilde_nodes(j,[1,b,c,d,e,f,g,h,i,j]):
                                            for l in yilde_nodes(k,[1,b,c,d,e,f,g,h,i,j]):
                                                count_paths.append(shortest_path([a,b,c,d,e,f,g,h,i,j,k,l]))

    count_paths.sort() #得到的行程方法按大小排序
    print('当从{}'.format(a),'节点出发时，最短行程路径：',count_paths[0][1],' 共行程：',count_paths[0][0]) #展示最短路线