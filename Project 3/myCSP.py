from csp import *


class myCSP(CSP):

    def __init__(self,name):
        self.constrains = {}
        self.deadEndCounter = None #dict of dicts to count how many times a tuple reached a conflict (for dom/wdeg)
        self.visitedNodes = 0
        self.constraintChecks = 0
        self.conflictsCount = 0
        self.conflicts = {} #dict of sets to save information durring backjumping
        data = self.readFile(name)
        super().__init__(data[0],data[1],data[2],self.f)

    def readFile(self,fileName):
    #dom file
        domFile = open("./rlfap/dom" + fileName, "r")
        int(domFile.readline())
        tempDomains = {}
        for line in domFile:
            domain = int(line.split()[0])
            count = int(line.split()[1])
            values = []
            for i in range(0,count):
                values.append(int(line.split()[i+2]))
            tempDomains[domain] = values

        neighbors = {}
        self.deadEndCounter = {}

    #var file
        varFile = open("./rlfap/var" + fileName, "r")
        int(varFile.readline())
        domains = {}
        variables = []
        for line in varFile:
            variable = int(line.split()[0])
            domain = int(line.split()[1])
            variables.append(variable)
            neighbors[variable] = [] #Initiliazing empty list for neighbors of current var
            self.conflicts[variable] = set()
            domains[variable]=tempDomains[domain]
            self.deadEndCounter[variable] = {} #Initiliazing dict to count how many times a tuple reached a conflict (for dom/wdeg)

    #ctr file
        self.constrains = {}
        ctrFile = open("./rlfap/ctr" + fileName, "r")
        int(ctrFile.readline())
        for line in ctrFile:
            var1 = int(line.split()[0])
            var2 = int(line.split()[1])
            constrain = line.split()[2]
            constrainVal = int(line.split()[3])
            neighbors[var1].append(var2)
            neighbors[var2].append(var1)
            self.deadEndCounter[var1][var2] = 1 #Initiliazing 1 as weight for heuristic
            self.deadEndCounter[var2][var1] = 1 #Initiliazing 1 as weight for heuristic
            self.constrains[(var1,var2)]=(constrain,constrainVal)

        return (variables,domains,neighbors)

    def f(self,A, a, B, b): #the constraints requested function which will be given to CSP
        if (A,B) in self.constrains.keys():
            constrain = self.constrains[(A,B)]
        elif (B,A) in self.constrains.keys():
            constrain = self.constrains[(B,A)]

        if constrain[0] == '>':
            return abs(a-b) > constrain[1]
        elif constrain[0] == '<':
            return abs(a-b) < constrain[1]
        elif constrain[0] == '=':
            return abs(a-b) == constrain[1]


def findSum(csp, minVar):
    Sum = 1
    for var in csp.deadEndCounter[minVar]:
        Sum += csp.deadEndCounter[minVar][var]

    return Sum

def heuristic(assignment, csp): #Impliments the dom/wdeg as in the paper
    Min = None
    for var in csp.variables:
        if var not in assignment:
            legal = num_legal_values(csp, var, assignment)
            tSum = findSum(csp, var)
            if Min != None:
                if Min/minSum > legal/tSum:
                    Min = legal
                    minVar = var
                    minSum = tSum
            else:
                Min = legal
                minVar = var
                minSum = tSum

    return minVar

def my_forward_checking(csp, var, value, assignment, removals):
    """Prune neighbor values inconsistent with var=value."""

    csp.support_pruning()
    for B in csp.neighbors[var]:
        if B not in assignment:
            for b in csp.curr_domains[B][:]:
                csp.constraintChecks += 1 #Counting number of constrains
                if not csp.constraints(var, value, B, b):
                    csp.prune(B, b, removals)
            if not csp.curr_domains[B]:
                #Counting for dom/wdeg
                csp.deadEndCounter[var][B] += 1
                csp.deadEndCounter[B][var] += 1
                return False
    return True

#AC3 but simply calling my_revise to count constraints and collect data for dom/wdeg 
def my_AC3(csp, queue=None, removals=None, arc_heuristic=dom_j_up):
    """[Figure 6.3]"""

    if queue is None:
        queue = {(Xi, Xk) for Xi in csp.variables for Xk in csp.neighbors[Xi]}
    csp.support_pruning()
    queue = arc_heuristic(csp, queue)
    checks = 0
    while queue:
        (Xi, Xj) = queue.pop()
        revised, checks = my_revise(csp, Xi, Xj, removals, checks)
        if revised:
            if not csp.curr_domains[Xi]:
                return False, checks  # CSP is inconsistent
            for Xk in csp.neighbors[Xi]:
                if Xk != Xj:
                    queue.add((Xk, Xi))
    return True, checks  # CSP is satisfiable

#Using AC3
def my_mac(csp, var, value, assignment, removals, constraint_propagation=my_AC3):
    """Maintain arc consistency."""
    return constraint_propagation(csp, {(X, var) for X in csp.neighbors[var]}, removals)

def my_revise(csp, Xi, Xj, removals, checks=0):
    """Return true if we remove a value."""
    revised = False
    for x in csp.curr_domains[Xi][:]:
        # If Xi=x conflicts with Xj=y for every possible y, eliminate Xi=x
        # if all(not csp.constraints(Xi, x, Xj, y) for y in csp.curr_domains[Xj]):
        conflict = True
        for y in csp.curr_domains[Xj]:
            csp.constraintChecks += 1 #Counting number of constrains
            if csp.constraints(Xi, x, Xj, y):
                conflict = False
            checks += 1
            if not conflict:
                break
        if conflict:
            #Counting for dom/wdeg
            csp.deadEndCounter[Xj][Xi] += 1
            csp.deadEndCounter[Xi][Xj] += 1
            csp.prune(Xi, x, removals)
            revised = True
    return revised, checks

def my_backtracking_search(csp, select_unassigned_variable=first_unassigned_variable,
                        order_domain_values=unordered_domain_values, inference=no_inference):
    """[Figure 6.5]"""

    csp.visitedNodes = 0
    csp.constraintChecks = 0

    def backtrack(assignment):
        if len(assignment) == len(csp.variables):
            return assignment
        var = select_unassigned_variable(assignment, csp)
        for value in order_domain_values(var, assignment, csp):
            if 0 == csp.nconflicts(var, value, assignment):
                csp.assign(var, value, assignment)
                csp.visitedNodes += 1 #Counting number of visited nodes
                removals = csp.suppose(var, value)
                if inference(csp, var, value, assignment, removals):
                    result = backtrack(assignment)
                    if result is not None:
                        return result
                csp.restore(removals)
        csp.unassign(var, assignment)
        return None

    result = backtrack({})
    assert result is None or csp.goal_test(result)
    return result

def my_forward_checkingCBJ(csp, var, value, assignment, removals):
    """Prune neighbor values inconsistent with var=value."""

    csp.support_pruning()
    for B in csp.neighbors[var]:
        conflict = False
        if B not in assignment:
            for b in csp.curr_domains[B][:]:
                csp.constraintChecks += 1
                if not csp.constraints(var, value, B, b):
                    csp.prune(B, b, removals)
                    conflict = True
            if conflict: #Adding conflict in the set for backjumbing
                csp.conflicts[B].add(var)
            if not csp.curr_domains[B]:
                csp.deadEndCounter[var][B] += 1
                csp.deadEndCounter[B][var] += 1
                if conflict: #Adding the rest conflicts in the set for backjumbing
                    for conflic in csp.conflicts[var]:
                        csp.conflicts[B].add(conflic)
                return False
    return True

def backJumping_search(csp, select_unassigned_variable=first_unassigned_variable,
                        order_domain_values=unordered_domain_values, inference=no_inference):
    """[Figure 6.5]"""

    csp.visitedNodes = 0
    csp.constraintChecks = 0

    def backJump(assignment):
        if len(assignment) == len(csp.variables):
            return (assignment,None)
        var = select_unassigned_variable(assignment, csp)
        for value in order_domain_values(var, assignment, csp):
            if 0 == csp.nconflicts(var, value, assignment):
                csp.assign(var, value, assignment)
                csp.visitedNodes += 1
                removals = csp.suppose(var, value)
                if inference(csp, var, value, assignment, removals):
                    result = backJump(assignment)
                    if result[0] is not None:
                        return result
                    #If the backjumping stops at this point of the recursion
                    if result[1] != None and var not in csp.conflicts[result[1]]:
                        #The function returns None to indicate the end of the backjumping...
                        csp.restore(removals)
                        csp.unassign(var, assignment)
                        for key in csp.conflicts:#... after removing the current variable from the conflict sets
                            if var in csp.conflicts[key]:
                                csp.conflicts[key].remove(var)
                        return (None,result[1])

                csp.restore(removals)
        csp.unassign(var, assignment)
        return (None,var)

    result = backJump({})
    assert result[0] is None or csp.goal_test(result[0])
    return result[0]


def my_min_conflicts(csp, max_steps=100000):
    """Solve a CSP by stochastic Hill Climbing on the number of conflicts."""
    # Generate a complete assignment for all variables (probably with conflicts)
    csp.current = current = {}
    for var in csp.variables:
        val = min_conflicts_value(csp, var, current)
        csp.assign(var, val, current)
    # Now repeatedly choose a random conflicted variable and change it
    for i in range(max_steps):
        conflicted = csp.conflicted_vars(current)
        if not conflicted:
            return current
        var = random.choice(conflicted)
        val = min_conflicts_value(csp, var, current)
        csp.assign(var, val, current)

    csp.conflictsCount = len(csp.conflicted_vars(current)) #Simply counting the conflicts the algorithm left

    return None
