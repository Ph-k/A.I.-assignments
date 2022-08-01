from myCSP import *
from csp import *
import time

#The program is initialized with the data of the dom ctr var files with the given prefix
CSPobject = myCSP("3-f10.txt")

#Uncomment only the algorithm you wish to use
algorithm = "FC"
#algorithm = "FC-CBJ"
#algorithm = "MAC"
#algorithm = "MIN-CONFLICTS"


if algorithm == "FC-CBJ":
    start = time.time()
    #FC-CBJ uses backjumbing and the dom/wdeg heuristic
    result = backJumping_search(CSPobject,select_unassigned_variable=heuristic, inference=my_forward_checkingCBJ)
    print(result,'\nconstraintChecks = ',CSPobject.constraintChecks,'\nvisitedNodes =',CSPobject.visitedNodes)
    print(time.time() - start,'\n')

elif algorithm == "FC":
    start = time.time()
    #FC uses backtracking and the dom/wdeg heuristic
    result = my_backtracking_search(CSPobject,select_unassigned_variable=heuristic, inference=my_forward_checking)
    print(result,'\nconstraintChecks = ',CSPobject.constraintChecks,'\nvisitedNodes =',CSPobject.visitedNodes)
    print(time.time() - start,'\n')

elif algorithm == "MAC":
    start = time.time()
    #MAC uses backtracking and the dom/wdeg heuristic
    result = my_backtracking_search(CSPobject,select_unassigned_variable=heuristic, inference=my_mac)
    print(result,'\nconstraintChecks = ',CSPobject.constraintChecks,'\nvisitedNodes =',CSPobject.visitedNodes)
    print(time.time() - start)

elif algorithm == "MIN-CONFLICTS":
    start = time.time()
    #min conflicts is simply min conflicts
    result = my_min_conflicts(CSPobject,1000)
    print(result,'\nconflicts =',CSPobject.conflictsCount)
    print(time.time() - start)