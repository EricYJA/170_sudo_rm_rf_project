# CS170 Project Skeleton

See [the Guavabot website](http://guavabot.cs170.org/) to get started!

### Group "sudo rm rf"

### Member:

[Jiahan Yu](<https://github.com/VirginiaYu>) 3034502719

[Haosheng Wang](<https://github.com/FlyingDutchman1007>) 3034505150

[Yuan Changcheng](<https://github.com/EricYJA>) 3034298427

---

### Design doc：

The implementation of this project could be split into two parts: one is figuring out the bots' location, the other is moving the bots back home. Notice that the cost of remoting bots towards an edge is far more expensive than the cost of scouting our students. Thus, we should make use of the students and follow the advice of the majority of the students, which turns out to obtain most of the locations of bots generally. Furthermore, the evaluation function of the project implies that the score obtained by sending a bot back home is greater than the score gained by saving time during scouting and remoting. Therefore, our algorithms are supposed to find the locations of bots as much as possible as we regard the situation that all the bots have been sent back home as the highest priority state.



### Question answering:

1. If there was a Guavabot on every node, what sequence of scouts and remotes would you do to get them all home?

   Answer: 
   
   No scout is needed since we are given every bot's location by the assumption that "there was a Guavabot on every node". In order to know the sequence of romotes, we first find the Minimum Spanning Tree of the whole graph and treat the home vertex as the root of the MST. Then, we move the bots from the leaves the MST to the root(home vertex). Due to the minimum property of the MST, it has the optimal(minimum) csot to move all the bots from their original location to the home vertex. 

   To implement it, the detailed algorithm is given as follows. Note that we are in a undirected graph and moving the bots from non-home vertices to the home vertex requires direction specified. Since the cost of remoting bots from one node to another depends only on the weight of the edge we are going to pass, rather than the number of bots we are going to move. In that case, merge operations are needed as we move the bots of the same depth at the same iteration and we have to make sure that we remote every edge in the MST only once. So the remoting process is: 
   
   (1) Start from the vertices with the maximum depth in the MST and remote bots on those vertices along the direction of reducing one depth in MST. 
   
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

   Answer for question 4 and 5: Please see below algorithms and their analysis.
   

### Algorithms:

##### Brute-force MST without scouting

Main idea: 

   (1) First find the MST for the whole graph. 
   
   (2) Start from the vertices with the maximum depth in the MST and remote bots on those vertices along the direction of reducing one depth in MST. Then delete the vertices with the maximum depth from the MST and get a size-reduced MST. 
   
   (3) Repeat the procedures (1) and (2) based on the updated MST which is generated at the end of each iteration. 
   
   (4) Stop remoting bots/iterations once we detect there is only one vertex, i.e., the home vertex, in the latest MST. As long as we keep following the algorithm, we can ensure that each edge in the original MST can be passed only once, so that the remote cost along any edge in the MST would be counted into total cost for only once. 

Analysis:

  The algorithm guarantees that all the bots would be found. When the ratio of #bots/#vertices becomes larger (# represents the number of the object), this algorithm would perform better. However, its performance for the given test cases is not so good as there is only 5 bots for most of the test cases, indicating that the algorithm would do poorly under the condition that the number of bots is relatively small. The average score obtained for the algorithm using the given test cases is about 88. 



##### MST with scouting

Main idea:

   (1) First find the MST for the whole graph. 
   
   (2) Apply all the students to scout all the vertices with the maximum depth in the MST, that is, the leaves of MST.

   (3) Find the target vertices set by selecting the vertices with the maximum depth of the current MST and which are reported "YES (has guavabots on that vertex)" by more than half of the students. We remote the bots on every vertex in this target vertices set along the direction of reducing one depth in current MST. Then delete all the vertices with the maximum depth from the MST and get a size-reduced MST. Note here the deleted vertices may be not included in our target vertices set.
   
   (4) Repeat the procedures (1) to (3) based on the updated MST which is generated at the end of each iteration. Stop remoting bots/iterations once we detect there is only one vertex, i.e., the home vertex, in the latest MST. 
  
Analysis:

The cost of this algorithm is less than the algorithm brute-force MST without scouting. It ignores the vertices that are unlikely to have bots in every iteration. However, we cannot confirm the fact that the vertices do not have bots as the students are unreliable and the scouting percentage can only be a reference. That is to say, the algorithm does not guarantee to find all the bots. As mentioned before, the score obtained by sending a bot back home is greater than the score gained by saving time during scouting and remoting, the cost of this algorithm is kind of unstable and we got an average of score 75 using the given test cases. The cost of this algorithm largely depends on the completion of finding the bots' positions. If it is close to the state that all the bots are found, it could even reach the score 95 and higher using some test cases. Hence, we conclude that the algorithm would perform extremely well when students are more reliable and the number of bots is relatively large. 



##### Shortest Path with scouting

Main idea:

   (1) We first calculate students’ scout. Sorting the node with the possibility of having at least one bot. Thus we could find out which vertex has the most possibility of containing bots.
   
   (2) Then we would like to find out which vertex has bots. We move the bots according to student’s scout one by one. Since each remote ends we could know the quantity of bots moved. If the return value is 0 then indicates that node do not have bots. The finding bots process will end if all the missing bots are find.
   
   (3) At last we implement the Dijkstra path and get the shortest path. Sending the bots home through the shortest path.

Analysis:

PROS:
The algorithm could find a path for each bots because the step (2) will not stop unless we find out all bots. The model do well on simple cases. 

CONS:
If the graph become much more complex, using shortest path directly may use more time.Confirming whether a vertex has robot will be time-consuming. This may cost pretty much time if the student couldn’t provide a very dependable scout. There are still some ways to prove after we confirm the robots position. A way of combining shortest path and MST will be more efficient in some cases.



##### Block MST 

Main idea:

The basic point of this algorithm is based on MST method yet to find several dense clusters in the (connected) whole graph and then to find the MST in each cluster. For the implementation of finding several dense clusters, it could be:

We first use some defined function to measure the size the graph and separeate the graph into several components. The function is defined manually, and needs trials (we select the well-performed ones according to the outcomes). For instance, we find the maximum length among all shortest path from the home vertex to other vertices in the graph. Then we divide this length by the square root of #vertices (or some other function with respect to the number of vertices in the graph) and set the ratio as a feature of the graph size. Upon obtaining this feature, we then calculate the diameter of each cluster according to some  formula defined by us. As for the center of each cluster, we are thinking of selecting some vertices with relative high degree, which we can find by sorting the vertices by the descending degree. Another way to find clusters could be: we set a lower bound of the number of clusters, then we remove/delete the edge with the heaviest weight until we reach that number of clusters. Note this approach needs to make a copy of the graph since we need to send those bots back home and we need the edge that have been removed.

Once we obtain those clusters, we gather the bots in each cluster to the center using the path given by the MST of the cluster rooted at the center vertex. Then we send all bots back home by using the MST of the graph consisting only the vertices that are the center of those clusters. 

Analysis:

The algorithm involves several unknown functions we have to define by ourselves. Thus, the performance cannot be predicted with so many uncertain factors. Besides, the implementation for this algorithm is still in progress. We would not give a detailed analysis for now. 


##### Steiner tree:

Main idea:
Use the algorithm in Q3 to find all the bots's location. Then, find a Steiner tree for all the bot vertices and the home vertices. Then, use the same idea as Q1 to move the bots to the home vertices. Knowing that the Networkx library provides the algorithm for finding the Steiner tree. The implementation is quite straight forward. 

Analysis:
This algorithm is considered as the best solution so far, since it's the optimal solution for moving all the bots home if their locations are known to us. The idea of the Steiner tree is to come up with a MST that covers some of given the vertices. The only problem is how to find all the bots location with the min cost. If we want to check the scout result, we need to remote on that vertex, which would incereases the cost. The method to find all the bots' location will be improved later.



