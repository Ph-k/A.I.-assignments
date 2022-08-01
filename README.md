
# A.I. - assignments
 
### Implementation of some artificial intelligence algorithms as a part of an AI course at DIT - UoA.
 
*Projects 1 & 2 are basically berkeley's [cs188 Pac-Man](https://inst.eecs.berkeley.edu/~cs188/sp19/) projects.*

**Project 1:**

In the folder of the first project you will find the implementation of various search algorithms (DFS, BFS, UCS, A*). Which are used to help Pac-Man win.  Also you will find various heuristics, which are mainly used in combination with the A* algorithm, and aid to improve the overall performance of the program.

**Project 2:**

In the folder of the second project you will find the implementation of a reflex agent (see `evaluationFunction()`), as well as implementations of the minimax and expectimax algorithms along with some improvements such as Alpha-Beta pruning.

Projects 1 & 2 passed the autograder, with grades 26/25 and 25/25 respectively.

Projects 1 & 2 execution commands are the same as in the berkeley projects ([1]([Project 1 - Search - CS 188: Introduction to Artificial Intelligence, Spring 2019 (berkeley.edu)](https://inst.eecs.berkeley.edu/~cs188/sp19/project1.html)),[2](https://inst.eecs.berkeley.edu/~cs188/sp19/project2.html)).

**Project 3**

The main focus of this project is to solve the constraint satisfaction problem (CSP) RLFA (radio link frequency assignment) using the algorithms FC, MAC και FC-CBJ. More information regarding the RLFA problem can be found here [Thomas Schiex - RLFAP (inrae.fr)](https://miat.inrae.fr/schiex/rlfap.shtml). The solution code *(files `csp.py`, `search.py`, `utils.py`)* in based on the code from [Artificial Intelligence: A Modern Approach](https://github.com/aimacode/aima-python/blob/master/csp.py) 

Implementation overview:

Given the input files in the folder `rlfap`, and the code from AIMA, my work can be found in the file `myCSP.py`.  Furthermore:

-	The class myCSP extends AIMA's CSP in order to easily use the already-implemented CSP methods.
-	The input files are read at myCSP constructor.
-	Method heuristic() implements dom/wdeg following the paper [p0146.pdf (frontiersinai.com)](http://www.frontiersinai.com/ecai/ecai2004/ecai04/pdf/p0146.pdf)
-	The FC, MAC, and FC-CBJ algorithms are implemented based on `CSP.py` code in the  functions **[`my_forward_checking()`]** **[`my_mac()` ,`my_revise()` ,`my_AC3()`]** and **[`my_forward_checkingCBJ()`, `backJumping_search`]** of `myCSP.py` 
