# Put your solution here.
import networkx as nx
import random
import heapq

def solve(client):
    client.end()
    client.start()

    '''
    Example: Get the robots position
    
    the list pos represents  the current robot position.
    To get pos, call the function find_robot_position(client).
    '''

    pos = find_robot_position(client)
    print(pos)


def find_bot(client):

    all_students = list(range(1, client.students + 1))
    non_home = list(range(1, client.home)) + list(range(client.home + 1, client.v + 1))

    # Define the students we want to ask
    query_student = all_students
    query_total = [client.scout(vertex, query_student) for vertex in non_home]
    query_result = []

    print(non_home)
    print(client.home)
    for q in query_total:
        witness = 0
        for s in query_student:
            if q[s]:
                witness += 1
        query_result.append(witness)

    max_num_index_list = []

    for _ in range(len(query_result)):
        i = query_result.index(max(query_result))
        if i < client.home - 1: # If the number before home
            max_num_index_list.append(i + 1)
        else: # The number is after home
            max_num_index_list.append(i + 2)
        query_result[i] = 0

    return max_num_index_list


def find_robot_position(client):
    # Create Graph G
    G = client.G
    robots_remain = client.bots
    max_num_index_list = find_bot(client) # get the student's answer (sorted by probability)

    # Initialize the graph as a empty list
    robot_position = []
    print("Home: ",client.home)

    for bot_num in max_num_index_list:

        if robots_remain > 0: # Judgement condtion: whether to bots are all found

            # get the dijkstra path
            path = nx.dijkstra_path(G, bot_num, client.home)
            print(path)
            print("bots remain",robots_remain)
            judge = client.remote(bot_num , path[1]) # Move one step using Dijstra

            if judge > 0: # Find a robot!
                robot_position.append(path[1])
                robots_remain -= 1
    return robot_position # a list contains all robots position

    client.end()
