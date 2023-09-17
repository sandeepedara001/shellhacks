from django.shortcuts import render
from django.http import HttpResponse
import json

from pathlib import Path


import heapq
from collections import defaultdict

# Create your views here.

def index(request):
	if (request.GET.get('source', None) and request.GET.get('dest', None)):

		data = runProgram(request.GET.get('source'), request.GET.get('dest'))

		# test = [
		# 		  [
		# 		    {
		# 		      "start_station": "Hyd",
		# 		      "end_station": "War",
		# 		      "start_time": "9:00",
		# 		      "end_time": "12:00"
		# 		    },
		# 		    {
		# 		      "start_station": "War",
		# 		      "end_station": "Tir",
		# 		      "start_time": "13:00",
		# 		      "end_time": "16:00"
		# 		    }
		# 		  ],
		# 		  [
		# 		    {
		# 		      "start_station": "Hyd",
		# 		      "end_station": "Guntur",
		# 		      "start_time": "19:00",
		# 		      "end_time": "23:00"
		# 		    },
		# 		    {
		# 		      "start_station": "Guntur",
		# 		      "end_station": "Tir",
		# 		      "start_time": "1:00",
		# 		      "end_time": "5:00"
		# 		    }
		# 		  ]
		# 		]

		testJson = json.dumps(data)
		# return HttpResponse(request.GET['source'] + " " + request.GET['dest'])
		return HttpResponse(testJson)
	else:
		return HttpResponse("Please pass parameters properly!")




class PathFinder:
    def __init__(self, end_node, weight, nodes, arrival_time):
        self.end_node = end_node
        self.weight = weight
        self.nodes = list(nodes)
        self.arrival_time = arrival_time

    def __lt__(self, other):
        return self.weight < other.weight

    def extend(self, new_node, edge_weight, arrival_time):
        new_nodes = self.nodes[:]
        new_nodes.append(new_node)
        return PathFinder(new_node, self.weight + edge_weight, new_nodes, arrival_time % 1440)

class ScheduleDestination:
    def __init__(self, destination, weight, arrival_time):
        self.destination = destination
        self.weight = weight
        self.arrival_time = arrival_time

def find_k_shortest_paths(graph, source, target, K, first_arrival_time):
    priority_queue = []
    k_shortest_paths = []

    heapq.heappush(priority_queue, PathFinder(source, 0, [source], first_arrival_time))

    while priority_queue and len(k_shortest_paths) < K:
        current_path = heapq.heappop(priority_queue)
        arrival_time = current_path.arrival_time

        if current_path.end_node == target:
            k_shortest_paths.append(current_path.nodes)

        if len(k_shortest_paths) >= K:
            continue

        for edge in graph[current_path.end_node]:
            neighbor = edge.destination
            edge_weight = edge.weight * 60
            added_weight = 0

            if edge.arrival_time < arrival_time:
                added_weight = edge.arrival_time + abs(arrival_time - 1440)
            else:
                added_weight = edge.arrival_time - arrival_time

            edge_weight += added_weight
            new_path = current_path.extend(neighbor, edge_weight, edge_weight + arrival_time % 1440)
            heapq.heappush(priority_queue, new_path)

    return k_shortest_paths

def runProgram(s, d):
    V = 1000  # Number of vertices
    graph = [[] for _ in range(V)]
    source_destination_weights = defaultdict(dict)

    # Read city names from the "City.txt" file
    cities = []
    # script_dir = Path(__file__).resolve().parent
    # file_path = script_dir / City.txt
    filepath = Path(__file__).parent / "City.txt"

    with open(filepath, "r", encoding="utf-8") as city_file:
        print("Success")
        for line in city_file:
            cities.append(line.strip())

    # Read data from the "example.txt" file
    filepath = Path(__file__).parent / "example.txt"
    with open(filepath, "r", encoding="utf-8") as file:
        for line in file:
            values = line.strip().split("@@")
            source = int(values[0])
            destination = int(values[1])
            weight = int(values[2])
            arrival_time = int(values[3])

            if destination not in source_destination_weights[source]:
                source_destination_weights[source][destination] = ScheduleDestination(destination, weight, arrival_time)

    for source, w_map in source_destination_weights.items():
        for destination, obj in w_map.items():
            graph[source].append(obj)




    source = cities.index(s) # rand.randint(0, 999)
    target = cities.index(d)  # rand.randint(0, 999)
    K = 3
    arrival_time = 240

    k_shortest_paths = find_k_shortest_paths(graph, source, target, K, arrival_time)

    l1 = []
    print(len(k_shortest_paths))
    for path in k_shortest_paths:
    #     print(path)
    # for i in range(len(k_shortest_paths)):
        # print(i)
        print(k_shortest_paths)
        source_station = 0
        destination = 0

        l2 = []

        # path = k_shortest_paths[i]
        print(path)
        print(len(path))

        for i in range(1, len(path)):
            dict1 = {}
            # print("dict is")
            # print(dict1)
            # print()
            # print()
            source_station = path[i - 1]
            destination = path[i]
            obj = source_destination_weights[source_station][destination]
            # print(cities[source_station], cities[destination], obj.arrival_time, obj.weight, end="\t")
            dict1['start_station'] = cities[source_station]
            dict1['end_station'] = cities[destination]
            dict1['start_time'] = obj.arrival_time
            dict1['end_time'] = obj.arrival_time + obj.weight
            l2.append(dict1)
        # print("list is")
        # print()
        # print()
        # print(l2)
        l1.append(l2)
        # print(l1)

    return l1

# if __name__ == "__main__":
#     main()

