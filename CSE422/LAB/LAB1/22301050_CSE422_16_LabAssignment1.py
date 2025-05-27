import heapq

input_f = open("E:\CSE422\LAB\LAB1\Input file.txt",'r')    
output_f = open("E:\CSE422\LAB\LAB1\Outputfile.txt",'w')

heuristic = {}
graph = {}

start_node = input('Start: ')
end_node = input('Destination: ')

for i in input_f:
    x = i.split(' ')
    # print(x)
    heuristic[x[0]] = int(x[1])
    # print(heuristic)
    graph[x[0]] = []  
    # print(graph)                               
    for j in range(2, len(x)-1, 2):
        adj_node = x[j]
        distance = x[j+1]
        graph[x[0]].append((adj_node, int(distance)))  
        
print(graph)  #Arad': [('Zerind', 75), ('Timisoara', 118), ('Sibiu', 140)] emon kore save hocche

# print(heuristic)    # {'Arad': 366, 'Craiova': 160, 'Eforie': 161, 'Fagaras': 176, 'Giurgiu': 77, 'Mehadia': 241, 
                    # 'Neamt': 234, 'Sibiu': 253, 'Oradea': 380, 'Pitesti': 100, 'RimnicuVilcea': 193, 'Dobreta': 242, 'Hirsova': 151, 
                    # 'lasi': 226, 'Lugoj': 244, 'Timisoara': 329, 'Urziceni': 80, 'Vaslui': 199, 'Zerind': 374, 'Bucharest': 0}

def a_Star_search(start_node, end_node, graph, heuristic):
    path = []
    parent = {start_node: None}
    distance = {start_node: 0}
    heapq.heappush(path, (heuristic[start_node], start_node))

    while path:
        temp1 = heapq.heappop(path)           #lowest cost pop hocche
        # print(temp1)                          #(366, 'Arad')
        for i in graph[temp1[1]]:             #graph[(366, 'Arad')]
            path_cost = int(distance[temp1[1]]) + int(i[1]) 
            # print(path_cost)
            if i[0] not in distance or path_cost < distance[i[0]]:  #for updating distance if short path is available
                distance[i[0]] = path_cost
                # print(i[0])
                # print(distance)
                a = distance[i[0]] + heuristic[i[0]]
                heapq.heappush(path, (a, i[0]))
                parent[i[0]] = temp1[1]  #track rakher jonno
    return parent, distance     
        
def output_function(parent, cost, start_node, end_node):
    out_path = []
    out_path.append(end_node)
    temp2 = end_node #bucharest
    # print(parent)     #{'Arad': None, 'Zerind': 'Arad', 'Timisoara': 'Arad', 'Sibiu': 'Arad', 'Oradea': 'Zerind', 'RimnicuVilcea': 'Sibiu', 'Fagaras': 'Sibiu', 
                        # 'Craiova': 'RimnicuVilcea', 'Pitesti': 'RimnicuVilcea', 'Bucharest': 'Pitesti', 'Giurgiu': 'Bucharest', 'Urziceni': 'Bucharest', 
                        # 'Lugoj': 'Timisoara', 'Mehadia': 'Lugoj', 'Dobreta': 'Mehadia', 'Hirsova': 'Urziceni', 'Vaslui': 'Urziceni', 'Eforie': 'Hirsova', 'lasi': 'Vaslui', 'Neamt': 'lasi'}
    while temp2 != start_node:
        temp2 = parent[temp2]
        out_path.append(temp2)
        # print(out_path)
    out_path.reverse()
    # print(out_path)    
    
    if len(out_path) == 0:
        output_f.write('No path found')
    else:
        output_f.write(f"Path: {' -> '.join(out_path[0:])}\n")          
        output_f.write(f"Total Distance: {cost[end_node]} Km")

# a_Star_search(start_node,end_node,graph,heuristic)            

# start_node = input('Start: ') Arad
# end_node = input('Goal: ')   Bucharest           
if start_node and end_node not in heuristic:
    # arad         bucharest
    print('Write the nodes again')
    start_node = input('Start: ')
    end_node = input('Destination: ')
    parent, cost = a_Star_search(start_node, end_node, graph, heuristic)
    output_function(parent, cost, start_node, end_node)
else:
    parent, cost = a_Star_search(start_node, end_node, graph, heuristic)  
    # print(parent)      
    output_function(parent, cost, start_node, end_node)
    
#OUTPUT    
# Path: Arad -> Sibiu -> RimnicuVilcea -> Pitesti -> Bucharest
# Total Distance: 418 Km    