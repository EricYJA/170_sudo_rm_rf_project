# CS170 Project Skeleton

See [the Guavabot website](http://guavabot.cs170.org/) to get started!

### Group "sudo rm rf"

### Member:

[Jiahan Yu](<https://github.com/VirginiaYu>) 3034502719

[Haosheng Wang](<https://github.com/FlyingDutchman1007>) 3034505150

[Yuan Changcheng](<https://github.com/EricYJA>) 3034298427

---

The project design document：

1. If there was a Guavabot on every node, what sequence of scouts and remotes would you do to get them all home?

   Note that no scout is needed since we know every bot's location. First, find the MST and treat the home vertex as root. Then, move the bots from the leaves the MST
   to the root. Since MST is the min, there's no better way. 


2. More generally, if you knew where all the bots were, what sequence of scouts and remotes would you do to get them all home?

   No scout is needed since we know every bot's location. Apply the shortest path tree and the MST, merging according to the MST. Compare the
   cost between moving along the shortest path tree and the cost moving along the MST, 
   then decide which one to move. 
   

3. If you didn't care about getting the bots home and just wanted to find their locations as quickly as possible, what sequence of scouts and remotes would you do?

   Apply all the students to scout on each vertex, and rank all the vertices with the number of students that reports yes. Starts from the vertex with the highest rank and then remote it with respect to method provided in 2 to get the correct number. Keep doing the above step untill all the bots are found. 


4. What ideas do you have for solvers? Please provide at least 2. What are their advantages/disadvantages?

     

   

5. What kinds of inputs do you think your solvers will do well on? Do poorly on?



