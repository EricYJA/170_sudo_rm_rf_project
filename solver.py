# Put your solution here.
import networkx as nx
import random
import heapq

def solve(client):
    client.end()
    client.start()

    all_students = list(range(1, client.students + 1))
    non_home = list(range(1, client.home)) + list(range(client.home + 1, client.v + 1))
    # client.scout(random.choice(non_home), all_students)
    G = client.G

    # for _ in range(100):
    #     u, v = random.choice(list(client.G.edges()))
    #     client.remote(u, v)

    MST = nx.maximum_spanning_tree(G)
    # 找到所有MST的
    # query_student = all_students[:len(all_students)//2]
    query_student = all_students
    query_total = [client.scout(vertex, query_student) for vertex in non_home]
    query_result = []

    # print(non_home)
    # print(client.home)
    for q in query_total:
        witness = 0
        for s in query_student:
            if q[s]:
                witness += 1
        query_result.append(witness)

    # print(query_result)

    # construct the expected bots
    number_of_bots = client.bots
    max_num_index_list = []

    for _ in range(len(query_result)):
        i = query_result.index(max(query_result))
        if i < client.home - 1:
            max_num_index_list.append(i + 1)
            # print("#:", i+1,"  value: ",query_result[i])
        else:
            max_num_index_list.append(i + 2)
        query_result[i] = 0

    # Begin Digstra
    robots_remain = client.bots
    # pred, dist = nx.dijkstra_predecessor_and_distance(G, client.home, cutoff=None, weight='weight')

    print("Home: ",client.home)
    print(max_num_index_list)

    for bot_num in max_num_index_list:

        if robots_remain > 0:

            path = nx.dijkstra_path(G, bot_num, client.home)
            print(path)
            print("bots remain",robots_remain)
            judge = client.remote(bot_num , path[1])
            if judge > 0:
                for i in range(2,len(path)):
                    client.remote(path[i-1], path[i])
                robots_remain -= 1



    client.end()
