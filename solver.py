import networkx as nx
import random

def solve(client):
    client.end()
    client.start()

    t_mst = nx.minimum_spanning_tree(client.G)

    all_students = list(range(1, client.students + 1))
    non_home = list(range(1, client.home)) + list(range(client.home + 1, client.v + 1))
    nodes_depth = nx.shortest_path_length(t_mst, client.home)
    
    nodes_bots = list()
    while t_mst.number_of_nodes() > 1:
        max_depth = max(nodes_depth.values())

        for x in non_home:

            # remote if the depth of x is max
            if nodes_depth[x] == max_depth:
                b_repo = client.scout(x, all_students)
                
                # remote it if scout yes
                if x in nodes_bots:
                    neigh_iter = nx.neighbors(t_mst, x)
                    neghi = neigh_iter.__next__()
                    tmp_bots = client.remote(x, neghi)

                    nodes_bots.append(neghi)
                    nodes_bots.remove(x)

                elif b_repo != None and get_general_scout(b_repo):
                    neigh_iter = nx.neighbors(t_mst, x)
                    neghi = neigh_iter.__next__()
                    tmp_bots = client.remote(x, neghi)

                    if tmp_bots > 0:
                        nodes_bots.append(neghi)

                # delete the node from MST
                t_mst.remove_node(x)
                nodes_depth.pop(x)
                non_home.remove(x)

    client.end()


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
