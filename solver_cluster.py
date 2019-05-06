import networkx as nx
import random
import heapq
import numpy as np
import copy

from networkx.algorithms import approximation


class PriorityQueue:
    """
    Implements a priority queue data structure. Each inserted item
    has a priority associated with it and the client is usually interested
    in quick retrieval of the highest-priority item in the queue. This
    data structure allows O(1) access to the highet-priority item.
    """

    def __init__(self):
        self.heap = []
        self.count = 0
        self.priority = {}

    def push(self, item, priority):
        entry = (-priority, self.count, item)
        heapq.heappush(self.heap, entry)
        self.count += 1
        self.priority[item] = -priority

    def pop(self):
        (_, _, item) = heapq.heappop(self.heap)
        return item

    def isEmpty(self):
        return len(self.heap) == 0

    def update(self, item, priority):
        # If item already in priority queue with higher priority, update its priority and rebuild the heap.
        # If item already in priority queue with equal or lower priority, do nothing.
        # If item not in priority queue, do the same thing as self.push.
        for index, (p, c, i) in enumerate(self.heap):
            if i == item:
                if p <= priority:
                    break
                del self.heap[index]
                self.heap.append((priority, c, item))
                heapq.heapify(self.heap)
                self.priority[item] = -priority
                break
        else:
            self.push(item, priority)

    def peekPriority(self, item):
        return self.priority[item]


def dijsktra(graph, home):
    visited = PriorityQueue()
    dist = {}
    paths = {}
    # Instantiate home node
    dist[home] = 0
    visited.push(home, np.inf)
    # Instantiate non-home nodes
    nodes = list(range(1, home)) + \
        list(range(home + 1, graph.number_of_nodes() + 1))
    for node in nodes:
        visited.push(node, 0)
        dist[node] = np.inf

    # Run Dijsktra's
    while not visited.isEmpty():
        u = visited.pop()
        edges = [x for x in graph.edges(data=True) if x[0] == u or x[1] == u]
        for edge in edges:
            if (edge[0] == u):
                v = edge[1]
            else:
                v = edge[0]
            alt = dist[u] + edge[2]['weight']
            if (alt < dist[v]):
                dist[v] = alt
                paths[v] = u
                visited.update(v, -alt)  # PQ is ordered by highest priority
    # dist = dictionary of distances from home of each node
    # paths = dictionary of "prev" node of each node
    return dist, paths


def makeCluster(nodes, distance, threshold):
    '''
    Creates a distance pq based on the first x nodes that are within a THRESHOLD probability apart.
    '''
    cluster = PriorityQueue()
    u = nodes.pop()
    top_weight = nodes.peekPriority(u)
    cluster.push(u, -nodes.peekPriority(u))
    u = nodes.pop()
    while (top_weight - nodes.peekPriority(u) >= threshold):
        cluster.push(u, distance[u])
        u = nodes.pop()
    nodes.push(u, -nodes.peekPriority(u))
    return cluster


def solve_cluster(c):
    # c.end()
    # c.start()

    # keep track of remote calls and home for testing VVVVVVVVVVVVV
    home = c.home
    remote_calls = {}
    edges = [x for x in c.graph.edges(data=True)]
    for x in edges:
        remote_calls["(" + str(x[0]) + ", " + str(x[1]) + ")"] = 0
        remote_calls["(" + str(x[1]) + ", " + str(x[0]) + ")"] = 0
    """
    above is testing ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    """
    # 100 vertices, 5 bots, 10/20/40 students
    chosen = c.students
    all_students = list(range(1, chosen + 1))
    num_students = c.students
    non_home = list(range(1, c.home)) + \
        list(range(c.home + 1, c.v + 1))

    '''
    Orders the nodes in order of probability of having a GuavaBot.
    Do this by scouting all nodes using all students.
    '''
    nodes = PriorityQueue()
    for i in non_home:
        total_true = sum(c.scout(i, all_students).values())
        nodes.push(i, total_true / chosen)

    distance, paths = dijsktra(c.graph, c.home)

    '''
    Make a (remote) call for nodes popped off the Priority Queue ORDERED BY DISTANCES WITHIN CLUSTERS
    CLUSTER = group of nodes within 10% probability within each other
    Repeatedly creates clusters and remotes them each once until all 5 bots + their locations are found.
    '''
    botNodeSet = set()
    lost_bots = 5
    botsFound = dict.fromkeys(list(range(1, c.v + 1)), 0)

    while lost_bots > 0:
        # first put highest priority into clusters
        # if next one is within 10%, put into cluster.
        # else, remote them one by one until you find 5. If the cluster becomes empty, then generate another cluster.
        cluster = makeCluster(nodes, distance, 0.1)
        while lost_bots != 0 and not cluster.isEmpty():
            u = cluster.pop()
            v = paths[u]
            if u in botNodeSet:
                botNodeSet.remove(u)
            num_bots_remoted = c.remote(u, v)
            remote_calls["(" + str(u) + ", " + str(v) + ")"] += 1

            if (num_bots_remoted - botsFound[u]) > 0:  # we found bot(s)
                botsFound[v] += num_bots_remoted - botsFound[u]
                lost_bots -= num_bots_remoted - botsFound[u]
                botsFound[u] = 0
                if v != c.home:
                    botNodeSet.add(v)

    '''
    Remote bots starting from furthest bot to home, ordered using a pq.
    '''

    print(botNodeSet)
    pos_bots = list(botNodeSet)

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


    #### Original implementation ###

    # botPQ = PriorityQueue()
    # for v in botNodeSet:
    #     botPQ.push(v, distance[v])

    # while not botPQ.isEmpty():
    #     u = botPQ.pop()
    #     v = paths[u]
    #     c.remote(u, v)
    #     remote_calls["(" + str(u) + ", " + str(v) + ")"] += 1

    #     if v != c.home:
    #         botPQ.push(v, distance[v])

    # c.end()

    # counter = 0
    # for key in remote_calls.keys():
    #     if remote_calls[key] > 0:
    #         counter += 1
    #         if remote_calls[key] > 1:
    #             print(key, remote_calls[key])
    # print('home = ', home)
    # print('number of students used: ', chosen)
    # print('number of students: ', num_students)
    # print('number of edges', len(edges))
    # print('number remote calls: ', counter)
