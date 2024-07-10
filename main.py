import random
import numpy


def read_data(filename):
  with open(filename, "r", encoding="utf8") as f:
    collection_list = []
    for line in f.readlines():
      collection_list.append((int(line.strip().split()[0]),
                              list(map(int,
                                       line.strip().split()[1:]))))
    return collection_list


class Graph:

  def __init__(self, nodes):
    self.nodes = nodes

  def __str__(self):
    output = "--- Graph --- \n"
    for node in self.nodes:
      output += node.__str__() + '\n'
    return output

  def add_node(self, new_key, new_neighbors):
    self.nodes.append(Node(new_key, new_neighbors))

  def delete_node(self, node_to_delete):
    for node in self.nodes:
      if node.key == node_to_delete:
        self.nodes.remove(node)
    for node in self.nodes:
      if node_to_delete in node.neighbors:
        node.neighbors.remove(node_to_delete)


class Node:

  def __init__(self, key, neighbors):
    self.key = key
    self.neighbors = neighbors

  def __str__(self):
    return f"Node {self.key} has neighbors {self.neighbors}"


def make_adjacency_matrix(nodes_list):
  adjacency_matrix = []
  row = []
  for i in range(len(nodes_list)):
    for j in range(len(nodes_list)):
      if j in nodes_list[i][1]:
        row.append(1)
      else:
        row.append(0)
    adjacency_matrix.append(row)
    row = []
  return adjacency_matrix


def find_leaves(nodes_list):
  leaves = []
  for node in nodes_list:
    if len(node[1]) == 1:
      leaves.append(node[0])
  return leaves


def make_tuples(leaves, tuples_list, nodes_list):
  nodes_queue = []
  last_v1 = 0
  for i in range(len(leaves)):
    tuples_list[leaves[i]] = (1, 2, 1, 0)
    if nodes_list[leaves[i]][1][0] not in nodes_queue:
      nodes_queue.append(nodes_list[leaves[i]][1][0])
  #print(nodes_queue)
  while len(nodes_queue) > 0:
    node = nodes_queue.pop(0)
    f_0 = 0
    f_0prime = 0
    f_1 = 1
    f_2 = 2
    #print(nodes_list[node][1])
    children = []
    for i in range(len(nodes_list[node][1])):
      if tuples_list[nodes_list[node][1][i]] != None:
        children.append(nodes_list[node][1][i])
    poss_f0prime = [0] * len(children)
    for i in range(len(children)):
      f_0 += tuples_list[children[i]][0]
      f_1 += tuples_list[children[i]][2]
      f_2 += tuples_list[children[i]][3]
      poss_f0prime[i] += tuples_list[children[i]][1]
      for j in range(len(children)):
        if i != j:
          poss_f0prime[j] += tuples_list[children[i]][0]
    f_0prime = min(poss_f0prime)
    v0 = min(f_0prime, f_1)
    v0prime = f_2
    v1 = min(f_0prime, f_1, f_2)
    v2 = min(f_0, f_1, f_2)
    tuples_list[node] = (v0, v0prime, v1, v2)
    last_v1 = v1
    for i in nodes_list[node][1]:
      if i not in nodes_queue and tuples_list[i] == None:
        nodes_queue.append(i)
        #print("added", i)
    #print("node:", node, "children:", children, "tuples:", tuples_list[node])
    #print("nodes_queue:", nodes_queue)
  return tuples_list, last_v1


def main():
  nodes_list = read_data("graph5.txt")
  #print(nodes_list)
  leaves = find_leaves(nodes_list)
  #print(leaves)
  tuples_list = [None] * len(nodes_list)
  tuples_list, prdn = make_tuples(leaves, tuples_list, nodes_list)
  #print(tuples_list)
  print("Perfect Roman Domination Number:", prdn)

main()