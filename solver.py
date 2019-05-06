import networkx as nx
import random

from networkx.algorithms import approximation


def solve(client):
    client.end()
    client.start()

    testing_method(client)
    
    client.end()

'''
Average score: 92.95
'''
def naive_dij(c):
    all_students = list(range(1, c.students + 1))
    non_home = list(range(1, c.home)) + list(range(c.home + 1, c.v + 1))
    # c.scout(random.choice(non_home), all_students)
    G = c.G

    # for _ in range(100):
    #     u, v = random.choice(list(c.G.edges()))
    #     c.remote(u, v)

    MST = nx.maximum_spanning_tree(G)
    # 找到所有MST的
    # query_student = all_students[:len(all_students)//2]
    query_student = all_students
    query_total = [c.scout(vertex, query_student) for vertex in non_home]
    query_result = []

    # print(non_home)
    # print(c.home)
    for q in query_total:
        witness = 0
        for s in query_student:
            if q[s]:
                witness += 1
        query_result.append(witness)

    # print(query_result)

    # construct the expected bots
    number_of_bots = c.bots
    max_num_index_list = []

    for _ in range(len(query_result)):
        i = query_result.index(max(query_result))
        if i < c.home - 1:
            max_num_index_list.append(i + 1)
            # print("#:", i+1,"  value: ",query_result[i])
        else:
            max_num_index_list.append(i + 2)
        query_result[i] = 0

    # Begin Digstra
    robots_remain = c.bots
    # pred, dist = nx.dijkstra_predecessor_and_distance(G, c.home, cutoff=None, weight='weight')

    # print("Home: ",c.home)
    # print(max_num_index_list)

    for bot_num in max_num_index_list:

        if robots_remain > 0:

            path = nx.dijkstra_path(G, bot_num, c.home)
            # print(path)
            # print("bots remain",robots_remain)
            judge = c.remote(bot_num , path[1])
            if judge > 0:
                for i in range(2,len(path)):
                    c.remote(path[i-1], path[i])
                robots_remain -= 1


'''
Average score: 91.88
'''
def mst_students_checking(c):
    pos_bots = find_robot_position(c)
    t_mst = nx.minimum_spanning_tree(c.G)

    non_home = list(range(1, c.home)) + list(range(c.home + 1, c.v + 1))
    nodes_depth = nx.shortest_path_length(t_mst, c.home)
    
    while t_mst.number_of_nodes() > 1:
        max_depth = max(nodes_depth.values())

        for x in non_home:

            # remote if the depth of x is max and it has bots
            if nodes_depth[x] == max_depth:
                
                # remote only when there's a bot in the vertex
                if x in pos_bots:
                    # remote every MST edge
                    neigh_iter = nx.neighbors(t_mst, x)
                    neghi = neigh_iter.__next__()

                    tmp_bots = c.remote(x, neghi)

                    pos_bots.remove(x)
                    pos_bots.append(neghi)


                # delete the n ode from MST
                t_mst.remove_node(x)
                nodes_depth.pop(x)
                non_home.remove(x)
            

'''
Average score: 88.68
'''
def mst_brute_force(c):
    t_mst = nx.minimum_spanning_tree(c.G)

    non_home = list(range(1, c.home)) + list(range(c.home + 1, c.v + 1))
    nodes_depth = nx.shortest_path_length(t_mst, c.home)

    while t_mst.number_of_nodes() > 1:
        max_depth = max(nodes_depth.values())

        for x in non_home:

            # remote if the depth of x is max
            if nodes_depth[x] == max_depth:
                
                # remote every MST edge
                neigh_iter = nx.neighbors(t_mst, x)
                neghi = neigh_iter.__next__()
                tmp_bots = c.remote(x, neghi)


                # delete the node from MST
                t_mst.remove_node(x)
                nodes_depth.pop(x)
                non_home.remove(x)


def testing_method(c):
    pos_bots = find_robot_position(c)
    print(pos_bots + [c.home], c.home)
    pos_bots = list(set(pos_bots + [c.home]))
    if len(pos_bots) == 1:
        return 

    st_tree_sb = approximation.steiner_tree(c.G, pos_bots)
    t_mst = nx.Graph.copy(st_tree_sb)

    non_home = list(range(1, c.home)) + list(range(c.home + 1, c.v + 1))
    non_home = [n for n in non_home if n in list(nx.nodes(t_mst))]
    nodes_depth = nx.shortest_path_length(t_mst, c.home)
    
    while t_mst.number_of_nodes() > 1:
        max_depth = max(nodes_depth.values())

        for x in non_home:

            # remote if the depth of x is max and it has bots
            if nodes_depth[x] == max_depth:
                
                # remote only when there's a bot in the vertex
                if x in pos_bots:
                    # remote every MST edge
                    neigh_iter = nx.neighbors(t_mst, x)
                    neghi = neigh_iter.__next__()

                    tmp_bots = c.remote(x, neghi)

                    pos_bots.remove(x)
                    pos_bots.append(neghi)


                # delete the n ode from MST
                t_mst.remove_node(x)
                nodes_depth.pop(x)
                non_home.remove(x)


########################
### Helper Functions ###
########################

'''
Helper function on how to find all the bots. 

Input: client
Output: A list containing all the bots location
'''
def find_bot_position_st(c):
    all_students = list(range(1, c.students + 1))
    non_home = list(range(1, c.home)) + list(range(c.home + 1, c.v + 1))

    # Find the rank resultof all the nodes
    query_student = all_students
    result = list()

    for n in range(1, c.v + 1):
        if n == c.home:
            result.append((n, -1))
            continue
        
        students_dict = c.scout(n, query_student)

        count = 0
        for i in students_dict.values():
            if i:
                count += 1
        result.append((n, count))

    result.sort(key=sortHelper, reverse=True)

    # start finding using the rank
    checked = list()
    bot_count = 0
    bots_pos = list()
    for i in result:
        if i[0] in checked:
            continue

        node = i[0]
        nei_list = list(c.graph.neighbors(node))
        nei_tuples = [t for t in result if t[0] in nei_list]
        nei_tuples.sort(key=sortHelper, reverse=True)

        node_re = 0
        for e in nei_tuples:
            if e[0] not in checked:
                node_re = e[0]
                break
        
        tmp_bot_count = c.remote(node, node_re)
        tmp_bot_count = c.remote(node_re, node)
        checked.append(node)
        checked.append(node_re)

        bot_count += tmp_bot_count

        if tmp_bot_count > 0:
            bots_pos.append(node)

        if bot_count == c.bots:
            break
    
    return bots_pos


def sortHelper(val):
    return val[1]

'''
Helper function to find the certain position for all bots
Input: default input client
Output: a list contains all robots position
Mechanism: rank all the vertices by the number of student reporting yes.  
    Then, remote all the vertices to check, until all the bots found. 
'''
def find_robot_position(c):
    # Create Graph G
    G = c.G
    robots_remain = c.bots
    max_num_index_list = find_bot(c)  # get the student's answer (sorted by probability)

    # Initialize the graph as a empty list
    robot_position = []
    # print("Home: ", c.home)

    for bot_num in max_num_index_list:

        if robots_remain > 0:  # Judgement condtion: whether to bots are all found

            # get the dijkstra path
            path = nx.dijkstra_path(G, bot_num, c.home)
            # print(path)
            # print("bots remain", robots_remain)
            judge = c.remote(bot_num, path[1])  # Move one step using Dijstra

            if judge > 0:  # Find a robot!
                if robot_position.count(path[0])==0:
                    robot_position.append(path[1])
                    robots_remain -= 1
                    # print("Find a bot! There are still bots left: ", robots_remain, "The bot is from ",path[0] ,"to the node", path[1])
                    # print("The current robot_position list is: ",robot_position)
                
                # elif condition: the bots moved = the bots already exists in the list.
                elif judge == robot_position.count(path[0]): 
                    # Get the index of elements we want to update
                    update_index = [i for i,x in enumerate(robot_position) if x == path[0]]
                    for i in update_index:  # update the bots location in robot_position
                        robot_position[i]=path[1]
                
                # else condition: the number of robots moved (judge) is larger than pos.count() 
                # which means we need add new bots in r_pos
                else: 
                    rest_to_change = judge - robot_position.count(path[0]) # calculate how many bots we still nedd to move

                    # Get the index of elements we want to update
                    update_index = [i for i, x in enumerate(robot_position) if x == path[0]]
                    for i in update_index:      # update the bots location in robot_position
                        robot_position[i] = path[1]

                    while rest_to_change >0 :   # finally add the new detected bots in r_pos
                        robot_position.append(path[1])

    return robot_position  # a list contains all robots position

'''
Helper function for the find_robot_position()
'''
def find_bot(c):

    all_students = list(range(1, c.students + 1))
    non_home = list(range(1, c.home)) + list(range(c.home + 1, c.v + 1))

    # Define the students we want to ask
    query_student = all_students
    query_total = [c.scout(vertex, query_student) for vertex in non_home]
    query_result = []

    # print(non_home)
    # print(c.home)
    for q in query_total:
        witness = 0
        for s in query_student:
            if q[s]:
                witness += 1
        query_result.append(witness)

    max_num_index_list = []

    for _ in range(len(query_result)):
        i = query_result.index(max(query_result))
        if i < c.home - 1: # If the number before home
            max_num_index_list.append(i + 1)
        else: # The number is after home
            max_num_index_list.append(i + 2)
        query_result[i] = 0

    return max_num_index_list
