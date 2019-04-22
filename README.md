# CS170 Project Skeleton

See [the Guavabot website](http://guavabot.cs170.org/) to get started!

### Group "sudo rm rf"

### Member:

[Jiahan Yu](<https://github.com/VirginiaYu>) 3034502719

[Haosheng Wang](<https://github.com/FlyingDutchman1007>) 3034505150

[Yuan Changcheng](<https://github.com/EricYJA>) 3034298427

---

### The project design document：

This project implementation could be split into two parts, one is finding the bots' location, the other is moving the bot back home. Notice that generally, students would give us the answer. Hence, it's reasonable to follow the advice of the students. Look into the score counting formula, we find that the score gain by getting bots home is greater than the score gain by min the time cost. Thus, moving all the bots home have the highest priority. 



### Question answering:

1. If there was a Guavabot on every node, what sequence of scouts and remotes would you do to get them all home?

   Note that no scout is needed since we know every bot's location. First, find the MST and treat the home vertex as root. Then, move the bots from the leaves the MST to the root. Since MST is the min, there's no better way. 

   To implement this, the detailed algorithm is stated as follows. Note that we are in a undirected graph, then to move the bots from non-home vertices to home vertices requires direction specified. Also note that the merging operation is needed, that is, move the bots according to their depth, make sure remoting every edge in the MST once. Start from the vertices with the max depth and remote them along the MST. Then, delete the vertices with the max depth from the MST. Keep doing this until there's only one home vertex in the MST. 


2. More generally, if you knew where all the bots were, what sequence of scouts and remotes would you do to get them all home?

   No scout is needed since we know every bot's location. In this case, the algorithm is more complicated, cause we want a MST that covers part of the vertices. Hence, global MST, block MST, and shortest path tree are the three main pathes to solve it in our idea. With more investigation, we found Steiner tree problem that maches what
   we are looking for. The solution of the problem would give us a MST of some vertices for a graph. Using the algorithm stated above to find a tree. Then, use the remote algorithm in 1 to remote the bots home. 
   
3. If you didn't care about getting the bots home and just wanted to find their locations as quickly as possible, what sequence of scouts and remotes would you do?

   Apply all the students to scout on each vertex, and rank all the vertices with the number of students that reports yes. Starts from the vertex with the highest rank and then remote it with respect to the shortest path tree. Count the number of the 
   bots found and repeat the step until all the bots are found. 



### Our algorithms:

##### Brute-force MST without scouting

Main idea:

The main idea is to find the MST for the whole graph and then remote the edges according to Q1. 

Analysis:

This method guarantees that all the bots would be found. When (the bots number / the vertices number) becomes larger, this algorithm would gets better. However, the performance for this algorithm for the test cases is not so good since there's only 5 bots for most of the cases. The average score gained for this algorithm is about 88. 



##### MST with scouting

Main idea:

Find the MST first. Scout all the nodes with the max depth in MST with all students. remote the vertes with the max depth and more than half of the students reports yes. delete all the nodes with the max depth in MST. Repeat the steps above untill there's only one home vertices left in the MST

Analysis:

Notice that this algorithm costs less than the algorithm before. It eliminate all the remotes that are unlikely to find bots. However, this algorithm does not guarantee finding all the bots. The gain for this algorithm has. an average of 75. However, the gain could reach 95 and higher if all the bots are found, proving you are lucky. 



##### Shortest Path with scouting

Main idea:

We first calculate students’ scout. Sorting the node with the possibility of having at least one bot. Thus we could find out which vertex has the most possibility of containing bots. Then we would like to find out which vertex has bots. We move the bots according to student’s scout one by one. Since each remote ends we could know the quantity of bots moved. If the return value is 0 then indicates that node do not have bots. The finding bots process will end if all the missing bots are find. At last we use shortest path algorithm, by calculating the Dijkstra path. Sending the bots home with the shortest path.

Analysis:

The algorithm could find a path for each bots. Because the second step will not stop unless we find out all bots. The model do well on simple cases. If the graph become much more complex, using shortest path directly may use more time.Confirming whether a vertex has robot will be time-consuming. This may cost pretty much time if the student couldn’t provide a very dependable scout. There are still some ways to prove after we confirm the robots position. A way of combining shortest path and MST will be more efficient in some cases.



##### Block MST 

Main idea:

create dense clusters in the connected graph: we first use some defined function to measure the size of graph and separate the graph into several components. Can be sort the degree descending. Max all shortest path and divide the length by the function of number of vertices, split into subtrees. Function unknow, should try. Another one is to delete heaviest edge until we have some number of subgroups.





