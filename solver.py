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


def find_robot_position(c):
    # Create Graph G
    G = c.G
    robots_remain = c.bots
    max_num_index_list = find_bot(c)  # get the student's answer (sorted by probability)

    # Initialize the graph as a empty list
    robot_position = []
    print("Home: ", c.home)

    for bot_num in max_num_index_list:

        if robots_remain > 0:  # Judgement condtion: whether to bots are all found

            # get the dijkstra path
            path = nx.dijkstra_path(G, bot_num, c.home)
            print(path)
            print("bots remain", robots_remain)
            judge = c.remote(bot_num, path[1])  # Move one step using Dijstra

            if judge > 0:  # Find a robot!
                if robot_position.count(path[0])==0:
                    robot_position.append(path[1])
                    robots_remain -= 1
                    print("Find a bot! There are still bots left: ", robots_remain, "The bot is from ",path[0] ,"to the node", path[1])
                    print("The current robot_position list is: ",robot_position)
                elif judge == robot_position.count(path[0]):
                    # Get the index of elements we want to update
                    update_index = [i for i,x in enumerate(robot_position) if x == path[0]]
                    for i in update_index: # update the bots location in robot_position
                        robot_position[i]=path[1]

                else: # else condition: the number of robots moved (judge) is larger than pos.count(), which means we need add new bots in r_pos
                    rest_to_change = judge - robot_position.count(path[0]) # calculate how many bots we still nedd to move

                    # Get the index of elements we want to update
                    update_index = [i for i, x in enumerate(robot_position) if x == path[0]]
                    for i in update_index:  # update the bots location in robot_position
                        robot_position[i] = path[1]

                    while rest_to_change >0 : # finally add the new detected bots in r_pos
                        robot_position.append(path[1])

    return robot_position  # a list contains all robots position

    client.end()
