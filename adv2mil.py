from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
map_file = "maps/test_loop_fork.txt"
# map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']

'''
player.travel(direction, boolean)
room.print_room_description(player)
room.get_exits()
room.get_exits_string()

room.get_room_in_direction(direction)
room.get_coords()
'''

oppoCards = {
    'n': 's',
    'e': 'w',
    's': 'n',
    'w': 'e'
}

traversal_path = []
visited_rooms = set()

visited_rooms.add(player.current_room)

backtrackCounter = 1

while len(visited_rooms) < len(room_graph):

    exits = player.current_room.get_exits()
    unvisitedDir = []
    for ex in exits:
        
        # if Room in direction is visited, don't need to visit
        room = player.current_room.get_room_in_direction(ex)
        if room not in visited_rooms:
            unvisitedDir.append((ex, room))
    
    if len(unvisitedDir) >= 1:
        player.travel(unvisitedDir[0][0]) # [first possible dir][ex]
        traversal_path.append(unvisitedDir[0][0])

        visited_rooms.add(player.current_room)
        backtrackCounter = 1

    elif len(unvisitedDir) < 1:
        player.travel(oppoCards[traversal_path[-1 * backtrackCounter]])
        traversal_path.append(oppoCards[traversal_path[-1 * backtrackCounter]])
        backtrackCounter += 2
print(traversal_path)
# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

    # if player.current_room not in visited_rooms:
    #     visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



# #######
# # UNCOMMENT TO WALK AROUND
# #######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
