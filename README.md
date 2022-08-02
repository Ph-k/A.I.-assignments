

# A.I. - assignments
 
## Implementation of *some* artificial intelligence algorithms which where a part of an AI course at DIT - UoA.
 
*Only the coding part of the projects is published. This means that projects 1 & 2 are basically berkeley's [cs188 Pac-Man](https://inst.eecs.berkeley.edu/~cs188/sp19/)*

### Project 1:

In the folder of the first project you will find the implementation of various search algorithms (DFS, BFS, UCS, A*). Which are used to help Pac-Man win.  Also you will find various heuristics, which are mainly used in combination with the A* algorithm, and aid to improve the overall performance of the program.

### Project 2:

In the folder of the second project you will find the implementation of a reflex agent *(see `evaluationFunction()`)*, as well as implementations of the minimax and expectimax algorithms along with some improvements such as Alpha-Beta pruning.

Projects 1 & 2 passed the autograder, with grades 26/25 and 25/25 respectively.

Projects 1 & 2 execution commands are the same as in the berkeley projects ([1](https://inst.eecs.berkeley.edu/~cs188/sp19/project1.html)),[2](https://inst.eecs.berkeley.edu/~cs188/sp19/project2.html)).

### Project 3

The main focus of this project is to solve the constraint satisfaction problem (CSP) RLFA (radio link frequency assignment) using the algorithms FC, MAC and FC-CBJ. More information regarding the RLFA problem can be found here [Thomas Schiex - RLFAP (inrae.fr)](https://miat.inrae.fr/schiex/rlfap.shtml). The solution code *(files `csp.py`, `search.py`, `utils.py`)* is based on the code from [Artificial Intelligence: A Modern Approach](https://github.com/aimacode/aima-python/blob/master/csp.py) 

#### Implementation overview:

Given the input files in the folder `rlfap`, and the code from AIMA, my work can be found in the file `myCSP.py`.  Furthermore:

-	The class myCSP extends AIMA's CSP in order to easily use the already-implemented CSP methods.
-	The input files are read at myCSP constructor.
-	Method heuristic() implements dom/wdeg following the paper [p0146.pdf (frontiersinai.com)](http://www.frontiersinai.com/ecai/ecai2004/ecai04/pdf/p0146.pdf)
-	The FC, MAC, and FC-CBJ algorithms are implemented based on `CSP.py` code in the  functions **[`my_forward_checking()`]** **[`my_mac()` ,`my_revise()` ,`my_AC3()`]** and **[`my_forward_checkingCBJ()`, `backJumping_search`]** of `myCSP.py` 

#### Input files format *(`rlfap` folder)* explanation: 

- var prefix files: The first number signifies the number of variables. The rest of the values are tuples of variables and their domains *(the domains can be found in the domXX.txt files)*.
- dom prefix files: The first integer marks the number of domains in the given file. In the following lines the first integer always marks the index of the domain, followed by the number of values it has. The rest numbres in the given line are the actual domain values.
- ctr prefix files: These files define the constraints for a given instance. More specificaly, the first number of the file is the number of constraints in it. The following text is the actual constrain in `|x-y| > k` or `|x-y| = k` form.

#### Execution instructions:

*Note: In order to execute the program, you have to install numpy and sortedcontainers*

In order to select an input file and the algorithm to use *(FC or FC-CBJ or MAC)*, you have to open the file `main.py` and edit lines 6 and 9-12 according to your preference. *Note that the input files need to be in a directory named `rlfap`*

The whole program can be easily executed on a machine with python installed,  using the command: `python main.py`

#### Output format explanation:
The program outputs the resulted constraints, followed by the number of constraintChecks and visitedNodes needed to find the solution, along with the time the total calculation took.
