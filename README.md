# CS170 Project Skeleton

See [the Guavabot website](http://guavabot.cs170.org/) to get started!

### Group "sudo rm rf"

### Member:

[Jiahan Yu](<https://github.com/VirginiaYu>) 3034502719

[Haosheng Wang](<https://github.com/FlyingDutchman1007>) 3034505150

[Yuan Changcheng](<https://github.com/EricYJA>) 3034298427

---

### The project design document：

The implementation of this project could be split into two parts: one is figuring out the bots' location, the other is moving the bots back home. Notice that the cost of remoting bots towards an edge is far more expensive than the cost of scouting our students. Thus, we should make use of the students and follow the advice of the majority of the students, which turns out to obtain most of the locations of bots generally. Furthermore, the evaluation function of the project implies that the score obtained by sending a bot back home is greater than the score gained by saving time during scouting and remoting. Therefore, our algorithms are supposed to find the locations of bots as much as possible as we regard the situation that all the bots have been sent back home as the highest priority state.



### Question answering:

1. If there was a Guavabot on every node, what sequence of scouts and remotes would you do to get them all home?

   Answer: 
   
   No scout is needed since we are given every bot's location by the assumption that "there was a Guavabot on every node". In order to know the sequence of romotes, we first find the Minimum Spanning Tree of the whole graph and treat the home vertex as the root of the MST. Then, we move the bots from the leaves the MST to the root(home vertex). Due to the minimum property of the MST, it has the optimal(minimum) csot to move all the bots from their original location to the home vertex. 

   To implement it, the detailed algorithm is given as follows. Note that we are in a undirected graph and moving the bots from non-home vertices to the home vertex requires direction specified. Since the cost of remoting bots from one node to another depends only on the weight of the edge we are going to pass, rather than the number of bots we are going to move. In that case, merge operations are needed as we move the bots of the same depth at the same iteration and we have to make sure that we remote every edge in the MST only once. So the remoting process is: 
   
   (1) Start from the vertices with the maximum depth in the MST and remote those vertices along the direction of reducing one depth in MST. 
   
   (2) Delete the vertices with the maximum depth from the MST and get a size-reduced MST. 
   
   (3) Repeat the procedures (1) and (2) based on the updated MST which is generated at the end of each iteration. 
   
   (4) Stop remoting bots/iterations once we detect there is only one vertex, i.e., the home vertex, in the latest MST. As long as we keep following the algorithm, we can ensure that each edge in the original MST can be passed only once, so that the remote cost along any edge in the MST would be counted into total cost for only once. 


2. More generally, if you knew where all the bots were, what sequence of scouts and remotes would you do to get them all home?

   Answer: 
   
   No scout is needed since scouting can only help us find the position of bots and we have known where all the bots are. Note in this case, not every vertex has gauvabots. So the optimality of the solution implemented by MST in question 1 is no longer ensured as a MST that covers some subset of the vertices in the graph also works. To clarify, this MST is a minimum-weight connected subgraph of that inculdes all the vertices that having bots. However, the MST not necessarily consists of only these vertices. The description of such a tree is much close to the definition of a Steiner Tree yet with a specified root (the home vertex).
   
   Hence, MST of the whole graph, several MSTs of the partial graph, and the shortest path tree are the three main ideas to solve the problem of getting all bots home. The solution to generating the Steiner tree would also give us a MST of some vertices for a graph. Using the algorithm stated above to find a tree. Then, use the remote algorithm in 1 to remote the bots home. 
  


3. If you didn't care about getting the bots home and just wanted to find their locations as quickly as possible, what sequence of scouts and remotes would you do?

   Answer: 
   
   The idea is presented as below:
   
   (1) Apply all the students to scout on each vertex in the graph. 
   
   (2) Rank all the vertices with the percentage of students that reports yes on the vertex. 
   
   (3) (we have three ideas about this procedure)
   
         Method 1: Extract the vertex of the highest rank and remote the bots of that vertex to the nearest adjacent vertex. 
      
         Method 2: Extract the vertex of the highest rank and remote the bots of that vertex along the first edge on the shortest path from that vertex to the home vertex. 
      
         Method 3: Extract the vertex of the highest rank and remote the bots of that vertex to the adjacent vertex with highest percentage of students that reports yes. In this case, the destination of remoting is more likely to have bots. 
     
   (4) As the remote function returns the number of bots have been remoted, we can obtain the number of bots we just remote (the number can even be zero). We record the number of the bots if it is non-zero and repeat the above procedures (1)-(3) until we have found all the |L| bots. Note it is not necessary to move all the bots back home, yet it is possible that we have sent back all the bots home when we stop our algorithm. We always keep track of the number of bots in vertices that have been served as remoting destinations.


4. What ideas do you have for solvers? Please provide at least 2. What are their advantages/disadvantages?

5. What kinds of inputs do you think your solvers will do well on? Do poorly on?

   Answer: See below algorithms.
   

### Our algorithms:

##### Brute-force MST without scouting

Main idea:

The main idea is to find the MST for the whole graph and then remote the edges according to Q1. 

Analysis:

This method guarantees that all the bots would be found. When (the bots number / the vertices number) becomes larger, this algorithm would gets better. However, the performance for this algorithm for the test cases is not so good since there's only 5 bots for most of the cases. This algorithm would do poorly when the bot number is relatively small. The average score gained for this algorithm is about 88. 



##### MST with scouting

Main idea:

Find the MST first. Scout all the nodes with the max depth in MST with all students. remote the vertes with the max depth and more than half of the students reports yes. delete all the nodes with the max depth in MST. Repeat the steps above untill there's only one home vertices left in the MST

Analysis:

Notice that this algorithm costs less than the algorithm before. It eliminate all the remotes that are unlikely to find bots. However, this algorithm does not guarantee finding all the bots. The gain for this algorithm has an average of 75. However, the gain could reach 95 and higher if all the bots are found, proving you are lucky. This algorithm would do extremely well when the accuracy of the students are high and the number of bots is relatively large. 



##### Shortest Path with scouting

Main idea:

We first calculate students’ scout. Sorting the node with the possibility of having at least one bot. Thus we could find out which vertex has the most possibility of containing bots. Then we would like to find out which vertex has bots. We move the bots according to student’s scout one by one. Since each remote ends we could know the quantity of bots moved. If the return value is 0 then indicates that node do not have bots. The finding bots process will end if all the missing bots are found. At last we use shortest path algorithm, by calculating the Dijkstra path. Sending the bots home with the shortest path.

Analysis:

The algorithm could find a path for each bots. Because the second step will not stop unless we find out all bots. The model do well on simple cases. If the graph become much more complex, using shortest path directly may use more time.Confirming whether a vertex has robot will be time-consuming. This may cost pretty much time if the student couldn’t provide a very dependable scout. There are still some ways to prove after we confirm the robots position. A way of combining shortest path and MST will be more efficient in some cases.



##### Block MST 

Main idea:

Create dense clusters in the connected graph: we first use some defined function to measure the size of graph and separate the graph into several components. Can be sort the degree descending. Max all shortest path and divide the length by the function of number of vertices, split into subtrees. Function unknow, should try. Another one is to delete heaviest edge until we have some number of subgroups.

Analysis:

The implementation for this algorithm is still in progress. Considering this algorithm is quite complicated. We would not give a detailed analysis for now. 


##### Steiner tree:

Main idea:
Use the algorithm in Q3 to find all the bots's location. Then, find a Steiner tree for all the bot vertices and the home vertices. Then, use the same idea as Q1 to move the bots to the home vertices. 

Analysis:
This algorithm is considered as the best solution so far, since it's the optimal solution for moving all the bots home if their locations are known to us. The only problem is how to find all the bots location with the min cost. If we want to check the scout result, we need to remote on that vertex, which would incereases the cost. The method to find all the bots' location would be improved later.



