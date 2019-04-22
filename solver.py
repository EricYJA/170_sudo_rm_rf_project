import networkx as nx
import random

def solve(client):
    client.end()
    client.start()

    mst_students_checking(client)
    
    client.end()


def mst_students_checking(c):
    pos_bots = find_robot_position(c)
    t_mst = nx.minimum_spanning_tree(c.G)

    non_home = list(range(1, c.home)) + list(range(c.home + 1, c.v + 1))
    nodes_depth = nx.shortest_path_length(t_mst, c.home)
    
    print(c.bot_locations)

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
    
    print(c.bot_locations)
            


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



def mst_student_based(c):
    t_mst = nx.minimum_spanning_tree(c.G)

    all_students = list(range(1, c.students + 1))
    non_home = list(range(1, c.home)) + list(range(c.home + 1, c.v + 1))
    nodes_depth = nx.shortest_path_length(t_mst, c.home)
    
    nodes_bots = list()
    while t_mst.number_of_nodes() > 1:
        max_depth = max(nodes_depth.values())

        for x in non_home:
            # remote if the depth of x is max
            if nodes_depth[x] == max_depth:
                b_repo = c.scout(x, all_students)
                
                # remote it if scout yes
                if x in nodes_bots:
                    neigh_iter = nx.neighbors(t_mst, x)
                    neghi = neigh_iter.__next__()
                    tmp_bots = c.remote(x, neghi)

                    nodes_bots.append(neghi)
                    nodes_bots.remove(x)

                elif b_repo != None and get_general_scout(b_repo):
                    neigh_iter = nx.neighbors(t_mst, x)
                    neghi = neigh_iter.__next__()
                    tmp_bots = c.remote(x, neghi)

                    if tmp_bots > 0:
                        nodes_bots.append(neghi)

                # delete the node from MST
                t_mst.remove_node(x)
                nodes_depth.pop(x)
                non_home.remove(x)


########################
### Helper Functions ###
########################

'''
Helper function to tell a over all T/F result based on a scouting list

Input: a dict of students' scouting result
Output: a bool value
Mechanism: if more students scout True, return true, else return false. 
'''
def get_general_scout(students_dict):

    # count the scout yes number 
    count = 0
    for i in students_dict.values():
        if i:
            count += 1

    if count >= len(students_dict) / 2:
        return True
    else:
        return False

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
    max_num_index_list = find_bot(c) # get the student's answer (sorted by probability)

    # Initialize the graph as a empty list
    robot_position = []
    print("Home: ",c.home)

    for bot_num in max_num_index_list:

        if robots_remain > 0: # Judgement condtion: whether to bots are all found

            # get the dijkstra path
            path = nx.dijkstra_path(G, bot_num, c.home)
            print(path)
            print("bots remain",robots_remain)
            judge = c.remote(bot_num , path[1]) # Move one step using Dijstra

            if judge > 0: # Find a robot!
                robot_position.append(path[1])
                robots_remain -= 1

    return robot_position # a list contains all robots position

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

    print(non_home)
    print(c.home)
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