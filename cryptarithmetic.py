import sys
from queue import PriorityQueue

class ANode:
  def __init__(self, name, alphabet):
    self.name = name
    self.alphabet = alphabet
    self.neighbors = []

  def addNeighbor(self, node):
    self.neighbors.append(node)

  def unassignedNeighbors(self):
    pass

  def __lt__(self, other):
    if self.unassignedNeighbors() < self.unassignedNeighbors():
      return False
    return True


class Problem:
  def __init__(self,variables):
    self.X = self._constructVariable(variables)
    self.D = self._buildDomain()

  def XSize(self):
    return len(self.X)

  def _constructVariable(self, variables):
    result = {}
    result["x9"] = variables[2][0]
    result["c4"] = "c4"
    numHolder = 1
    for i in range(len(variables[0])):
      temp = numHolder
      result["x"+str(temp)] = variables[0][i]
      
      temp += 4
      result["x"+str(temp)] = variables[1][i]

      temp += 5
      result["x"+str(temp)] = variables[2][i+1]

      numHolder += 1

      if i < 3:
        result["c"+str(i+1)] = "c"+str(i+1)
    
    return result

  def _buildDomain(self):
    domain = []
    # Adding the domain values for x9
    domain.append(("x9", [1]))

    # Adding domain values for auxillary variables.
    for i in range(4,0,-1):
      if i==4: domain.append(("c"+str(i), [1]))
      else: domain.append(("c"+str(i), [0,1]))
    
    # Creating domains for the rest of the variables.
    for i in range(13):
      if i+1 == 9: continue
      if i+1 == 1 or i+1 == 5: domain.append(("x"+str(i+1), [1,2,3,4,5,6,7,8,9]))
      else: domain.append(("x"+str(i+1), [0,1,2,3,4,5,6,7,8,9]))
    
    return domain

  def selectUnassignedVariable(self, assignments):
    # Most constrained variable
    minDomain = 10
    for i in range(len(self.D)): minDomain = min(minDomain, len(self.D[i][1]))
    vars = [var for var in self.D if len(var[1]) == minDomain]

    # Most unassigned neighbors

    # For filter
    maxNumOfUnassignedVars = self.unassignedNeighbors(vars[0][0], assignments)
    result = vars[0]
    def filterFunc(var):
      if var[0] == result[0]:
        return False
      return True
    if len(vars) == 1:
      self.D = list(filter(filterFunc, self.D))
      return result[0], self.X[result[0]], result[1]
    for i in range(1, len(vars)):
      num = self.unassignedNeighbors(vars[i][0], assignments)
      if num > maxNumOfUnassignedVars:
        maxNumOfUnassignedVars = num
        result = vars[i]
    self.D = list(filter(filterFunc, self.D))
    return result[0], self.X[result[0]], result[1]

  def unassignedNeighbors(self, variable, assignments):
    if variable == "c4":
      return 5
    if variable == "c3":
      return 8
    if variable == "c2":
      return 8
    if variable == "c1":
      return 7
    
    count = 0

    num = int(variable[1])
    n1 = None
    n2 = None
    if num == 9:
      if "c4" not in assignments:
        count += 1
    if 1 <= num <= 4:
      n1 = self.X["x"+str(num+4)]
      n2 = self.X["x"+str(num+9)]
      if n1 not in assignments:
        count += 1
      if n2 not in assignments:
        count += 1
    
    if 5 <= num <= 8:
      n1 = self.X["x"+str(num-4)]
      n2 = self.X["x"+str(num+5)]
      if n1 not in assignments:
        count += 1
      if n2 not in assignments:
        count += 1

    if 10 <= num <= 13:
      n1 = self.X["x"+str(num-5)]
      n2 = self.X["x"+str(num-9)]
      if n1 not in assignments:
        count += 1
      if n2 not in assignments:
        count += 1
    # print("variable " + str(variable) + ": " + str(count))
    return count
      

def checkConsistency(position, alphabet, value, assignments):
  if alphabet in assignments:
    if alphabet == "c1":
      print("HERE")
    return False
  for key,val in assignments.items():
    if key[0] != "c":
      if val == value:
        return False
  if alphabet == "c1":
      print("HERE2")
  return True


def backtracking(csp):
  return backtrackingHelper({}, csp)


def backtrackingHelper(assignments, csp):
  if len(assignments) == csp.XSize():
    return assignments
  position, alphabet, domain = csp.selectUnassignedVariable(assignments)
  for value in domain:
    if alphabet == "c1":
      print(checkConsistency(position, alphabet, value, assignments))
    if checkConsistency(position, alphabet, value, assignments):
      assignments[alphabet] = value
    # inferences = INFERENCE(csp, var, value)
      answer = backtrackingHelper(assignments, csp)
      if answer is not False:
        print("HERE")
        return answer
      assignments.pop(alphabet)
  # print(assignments)
  return False


if __name__ == "__main__":
  filename = sys.argv[1].replace("\n", "")
  with open(filename) as f:
    variables = [line.replace("\n", "") for line in f]
    csp = Problem(variables)
    answer = backtracking(csp)
    print(answer)




# # get the size of the smallest domain
#     smallestDomainSize = 10
#     for i in range(len(self.D)):
#         for j in range(9):
#             if assignment[i][j] is None:
#                 smallestDomainSize = min(len(domain[i][j]),smallestDomainSize)

#     # get those tiles that are unassigned with smallest domain
#     unassigned = [(x,y) for x in range(9) for y in range(9) if assignment[x][y] is None and len(domain[x][y]) == smallestDomainSize]
#     if len(unassigned) == 1: # if there's only 1 variable with smallest domain, return it
#         return unassigned[0]
#     else:   # if there's a tie, use degree heuristic
#         largestDegree = -1  # something really small
#         largestDegreeTile = unassigned[0]
#         for tile in unassigned:
#             if largestDegree < getNumberOfUnassignedNeighbors(assignment,tile): # get largest, if there's a tie, get the first one thats largest
#                 largestDegree = getNumberOfUnassignedNeighbors(assignment,tile)
#                 largestDegreeTile = tile
#         return largestDegreeTile