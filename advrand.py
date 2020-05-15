from room import Room
from player import Player
from world import World

from util import Queue

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

'''
player.travel(direction, boolean)
room.print_room_description(player)
room.get_exits()
room.get_exits_string()

room.get_room_in_direction(direction)
room.get_coords()
'''

traversal_path = []
visited_rooms = set()

visited_rooms.add(player.current_room)

while len(visited_rooms) < len(room_graph):

    exits = player.current_room.get_exits()
    unvisitedRoom = []
    for ex in exits:
        
        # if Room in direction is visited, don't need to visit
        room = player.current_room.get_room_in_direction(ex)
        if room not in visited_rooms:
            unvisitedRoom.append((ex, room))
    
    if len(unvisitedRoom) > 0: # calculate immediacy instead when working
        # dirToMostNeighbors = None
        # visitation = 0
        # for n in unvisitedRoom:
        #     exits = n[1].get_exits()

        #     vf = 0

        #     for ex in exits:
        #         room = n[1].get_room_in_direction(ex)
        #         if room not in visited_rooms:
        #             print('hi')
        #             vf += 1
            
        #     if vf > visitation:
        #         visitation = vf
        #         dirToMostNeighbors = n[0]

        # player.travel(dirToMostNeighbors) # [first possible dir][ex]
        # traversal_path.append(dirToMostNeighbors)

        randomVisit = random.randrange(len(unvisitedRoom))

        player.travel(unvisitedRoom[randomVisit][0]) # [first possible room][dir]
        traversal_path.append(unvisitedRoom[randomVisit][0])

        visited_rooms.add(player.current_room)

    elif len(unvisitedRoom) < 1: # no rooms I need to visit in vicinity, bft backtrack
        bfQ = Queue()
        c_room = player.current_room
        bfQ.enqueue((player.current_room, [])) # room / returnPath

        travelMap = []
# c_room[0] == object, c_room[1] == directions
        brk = False

        qVisited = set()
        qVisited.add(c_room)
        while brk == False: 
            c_room, directions = bfQ.dequeue()
            c_exits = c_room.get_exits()
            
            for exs in c_exits:
                dirRoom = c_room.get_room_in_direction(exs)

                if dirRoom not in visited_rooms: # I should be checking neighbors, not the room itself
                    travelMap = directions + [exs]
                    brk = True
                    break

                if dirRoom not in qVisited:
                    bfQ.enqueue((dirRoom, directions + [exs]))
                    qVisited.add(c_room)


        for d in travelMap:
            player.travel(d) # [first possible dir][ex]
            traversal_path.append(d)

            visited_rooms.add(player.current_room)



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
