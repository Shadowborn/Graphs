from room import Room
from player import Player
from world import World
# from utils import Stack

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

class Stack():
    def __init__(self):
        self.stack = []
    def push(self, value):
        self.stack.append(value)
    def pop(self):
        if self.size() > 0:
            return self.stack.pop()
        else:
            return None
    def size(self):
        return len(self.stack)
    def print_stack(self):
        print(self.stack)

class Queue():
    def __init__(self):
        self.queue = []
    def enqueue(self, value):
        self.queue.append(value)
    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None
    def size(self):
        return len(self.queue)

def adventure(world, traversal_path):
    def unknown_path(graph):
        for blah in graph:
            if '?' in graph[blah].values():
                return True
        return False

    def find_move(visited, current_room):
        curr_room = current_room.id
        room_exits = visited[curr_room]
        for direction in room_exits:
            if room_exits[direction] == '?' and current_room.get_room_in_direction(direction).id not in visited:
                return direction
        return None

    def find_room(traversal_path, visited, curr_room, stack, reverse):
        while True:
            next_move = stack.pop()
            traversal_path.append(next_move)
            next_room = curr_room.get_room_in_direction(next_move)
            if '?' in visited[next_room.id].values():
                return next_room.id
            curr_room = next_room

    s = Stack()
    curr = 0
    visited = {0: {}}
    curr_room = world.rooms[curr]
    backwords = {'n':'s', 'e':'w', 's':'n', 'w':'e'}
    for direction in curr_room.get_exits():
        visited[curr_room.id][direction] = '?'
    while len(visited) < len(world.rooms) and unknown_path(visited):
        curr_room = world.rooms[curr]
        if curr_room not in visited:
            visited[curr_room.id] = {}
            for direction in curr_room.get_exits():
                visited[curr_room.id][direction] = '?'
        next_move = find_move(visited, curr_room)
        if not next_move:
            curr = find_room(traversal_path, visited, curr_room, s, backwords)
        else:
            traversal_path.append(next_move)
            next_room = curr_room.get_room_in_direction(next_move)
            visited[curr][next_move] = next_room.id
            if next_room.id not in visited:
                visited[next_room.id] = {}
                for direction in next_room.get_exits():
                    visited[next_room.id][direction] = '?'
            visited[next_room.id][backwords[next_move]] = curr_room.id
            s.push(backwords[next_move])
            curr = next_room.id

print(adventure(world, traversal_path))
print(traversal_path)

# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")




# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
