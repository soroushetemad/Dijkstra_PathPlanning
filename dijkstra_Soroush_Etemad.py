import cv2
import numpy as np
import heapq
import time

map = cv2.imread('output_image.JPG')   #Load in the image of the map of choice
map_height, map_width,_ = map.shape
threshold = 50 # Pixel intensity used to detect of obstacle (padding) 

class Node:
    def __init__(self, x, y, cost, parent_id):
        self.x = x
        self.y = y
        self.cost = cost
        self.parent_id = parent_id
    
    def __lt__(self, other):
        return self.cost < other.cost

# Functions that define the different movements of the robot, returning the new coordinate and cost    
def UP(x, y, cost):
    return x, y + 1, cost + 1

def DOWN(x, y, cost):
    return x, y - 1, cost + 1

def LEFT(x, y, cost):
    return x - 1, y, cost + 1

def RIGHT(x, y, cost):
    return x + 1, y, cost + 1

def BOTTOM_LEFT(x, y, cost):
    return x - 1, y - 1, cost + 1.4

def BOTTOM_RIGHT(x, y, cost):
    return x + 1, y - 1, cost + 1.4

def UP_LEFT(x, y, cost):
    return x - 1, y + 1, cost + 1.4

def UP_RIGHT(x, y, cost):
    return x + 1, y + 1, cost + 1.4

# The config_space function is responsible for creating an obstacle space based on the provided map. 
# The obstacle space is a binary matrix where the value at each position represents whether it is an obstacle or not.
def config_space():
    obstacle_space = np.zeros((map_height, map_width), dtype=np.uint8)  # Initialize obstacle space

    for y in range(map_height):
        for x in range(map_width):
            if all(map[y, x] < threshold):  # Check if pixel is black (obstacle)
                obstacle_space[y, x] = 1  # Mark it as obstacle
    
    return obstacle_space

# The valid function checks whether a given position (x, y) is valid within the obstacle space
#  It checks validity based on whether the position is within the boundaries of the obstacle space and whether it corresponds to an obstacle. 
def valid(x, y, obstacle_space):
    height, width = obstacle_space.shape
    
    if x < 0 or x >= width or y < 0 or y >= height or obstacle_space[y][x] == 1:
        return False
    return True

def goal_check(current, goal):
    return current.x == goal.x and current.y == goal.y

def dijkstra(start, goal, obstacle_space):
    # Check if the start node is the same as the goal node

    if goal_check(start, goal):
        return None, True

    goal_node = goal
    start_node = start

    moves = [UP, DOWN, LEFT, RIGHT, BOTTOM_LEFT, BOTTOM_RIGHT, UP_LEFT, UP_RIGHT]
    # Initialize a dictionary to store open nodes (nodes to be explored),
    # a set to store closed nodes (nodes already explored),
    # a queue to prioritize nodes based on cost,
    # and an empty list to store explored nodes.
    open_dict = {(start_node.x, start_node.y): start_node}
    closed_set = set()
    queue = [(start_node.cost, start_node)]
    node_list = []

    # Continue the loop until the queue is empty.
    while queue:
        # Pop the node with the lowest cost from the queue and append the current x and y node to node_list
        current_node = heapq.heappop(queue)[1]
        node_list.append([current_node.x, current_node.y])

        if goal_check(current_node, goal_node):
            goal_node.parent_id = current_node.parent_id
            goal_node.cost = current_node.cost
            print("Path to goal node found!!!!!!!")
            return node_list, True

        current_coords = (current_node.x, current_node.y)
        # Check if the current coordinates are in the closed set
        if current_coords in closed_set:
            continue

        closed_set.add(current_coords)
        
        # Iterate through possible moves (directions)
        for move in moves:
            x, y, cost = move(current_node.x, current_node.y, current_node.cost)
            new_node = Node(x, y, cost, current_node)
            new_coords = (new_node.x, new_node.y)

            # Check if the new node is within the obstacle space and not in the closed set
            if valid(new_node.x, new_node.y, obstacle_space) and new_coords not in closed_set:
                if new_coords in open_dict:
                    # If the new node has a lower cost than the stored node, update the stored node's information
                    if new_node.cost < open_dict[new_coords].cost:
                        open_dict[new_coords].cost = new_node.cost
                        open_dict[new_coords].parent_id = new_node.parent_id
                        heapq.heappush(queue, (new_node.cost, new_node))
                else:
                    # If the new node is not in the open_dict, add it to the open_dict and push it into the priority queue
                    open_dict[new_coords] = new_node
                    heapq.heappush(queue, (new_node.cost, new_node))

    # If the goal is not found after exploring all possible paths, return the node_list and False.
    return node_list, False

def backtracking(goal_node):
    # Initialize lists to store x and y coordinates of the path
    x_path, y_path = [goal_node.x], [goal_node.y]

    # Continue backtracking until reaching the start node (parent_id = -1)
    while goal_node.parent_id != -1:
        # Update goal_node to its parent and append coordinates to the path lists
        goal_node = goal_node.parent_id
        x_path.append(goal_node.x)
        y_path.append(goal_node.y)

    # Reverse the lists to get the correct order of coordinates
    x_path.reverse()
    y_path.reverse()

    # Return the path as x and y coordinate lists
    return x_path, y_path


def plot_path(map, node_list, x_path, y_path):
    # Mark explored nodes on the map with green color
    for node in node_list:
        map[node[1], node[0]] = [0, 255, 0]  # Green color for explored nodes
    # Draw red lines on the map to represent the path
    for i in range(len(x_path) - 1):
        cv2.line(map, (x_path[i], y_path[i]), (x_path[i + 1], y_path[i + 1]), (0, 0, 255), thickness=2)  # Red color for path

    cv2.imshow("Map with Path", map)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    obstacle_space = config_space()
    
    if obstacle_space is None:
        exit()

    # Ask for user start and goal x,y coordinates
    start_x = int(input("Enter x for Start Node: "))
    start_y = int(input("Enter y for Start Node: "))
    end_x = int(input("Enter x for Goal Node: "))
    end_y = int(input("Enter y for Goal Node: "))   
    
    start_node = Node(start_x, map_height - start_y, 0, -1) #map_height - start_y accounts for opencv frame offset
    goal_node = Node(end_x, end_y, 0, -1)
    start_time = time.time()
    node_list, goal_found = dijkstra(start_node, goal_node, obstacle_space) #function call 
    end_time = time.time() # tracking run time 

    if goal_found:
        print("Runtime [sec]: ", end_time - start_time)
        x_path, y_path = backtracking(goal_node)
        plot_path(map, node_list, x_path, y_path)

    else:
        print("GOAL NODE NOT FOUND")

###################################### UNCOMMMENT THE BELOW IF YOU WANT TO SAVE THE VIDEO ANIMATION ###################################################

# The below code is identical to the above code but includes code to save the video as output_video.mp4. CAUTION: The saving of the video takes about 15min since I wanted the full quality. 
# The video used in submission was a compressed and sped up version of this video

# import cv2
# import numpy as np
# import heapq
# import time

# map = cv2.imread('output_image.JPG')  # Load the map in grayscale
# map_height, map_width,_ = map.shape
# threshold = 50

# video_filename='output_video.mp4'
# # Create a video writer object
# fourcc = cv2.VideoWriter_fourcc(*'mp4v')
# video_writer = cv2.VideoWriter(video_filename, fourcc, 1000, (map_width,map_height))

# class Node:
#     def __init__(self, x, y, cost, parent_id):
#         self.x = x
#         self.y = y
#         self.cost = cost
#         self.parent_id = parent_id
    
#     def __lt__(self, other):
#         return self.cost < other.cost
    
# def UP(x, y, cost):
#     return x, y + 1, cost + 1

# def DOWN(x, y, cost):
#     return x, y - 1, cost + 1

# def LEFT(x, y, cost):
#     return x - 1, y, cost + 1

# def RIGHT(x, y, cost):
#     return x + 1, y, cost + 1

# def BOTTOM_LEFT(x, y, cost):
#     return x - 1, y - 1, cost + 1.4

# def BOTTOM_RIGHT(x, y, cost):
#     return x + 1, y - 1, cost + 1.4

# def UP_LEFT(x, y, cost):
#     return x - 1, y + 1, cost + 1.4

# def UP_RIGHT(x, y, cost):
#     return x + 1, y + 1, cost + 1.4


# def config_space():
    
#     obstacle_space = np.zeros((map_height, map_width), dtype=np.uint8)  # Initialize obstacle space

#     for y in range(map_height):
#         for x in range(map_width):
#             if all(map[y, x] < threshold):  # Check if pixel is black (obstacle)
#                 obstacle_space[y, x] = 1  # Mark it as obstacle
    
#     return obstacle_space

# def valid(x, y, obstacle_space):
#     height, width = obstacle_space.shape
    
#     if x < 0 or x >= width or y < 0 or y >= height or obstacle_space[y][x] == 1:
#         return False
    
#     return True

# def goal_check(current, goal):
#     return current.x == goal.x and current.y == goal.y

# def dijkstra(start, goal, obstacle_space):
#     if goal_check(start, goal):
#         return None, True

#     goal_node = goal
#     start_node = start
#     moves = [UP, DOWN, LEFT, RIGHT, BOTTOM_LEFT, BOTTOM_RIGHT, UP_LEFT, UP_RIGHT]
#     open_dict = {(start_node.x, start_node.y): start_node}
#     closed_set = set()
#     queue = [(start_node.cost, start_node)]
#     node_list = []

#     while queue:
#         current_node = heapq.heappop(queue)[1]
#         node_list.append([current_node.x, current_node.y])

#         if goal_check(current_node, goal_node):
#             goal_node.parent_id = current_node.parent_id
#             goal_node.cost = current_node.cost
#             print("Goal Node found")
#             return node_list, True

#         current_coords = (current_node.x, current_node.y)

#         if current_coords in closed_set:
#             continue

#         closed_set.add(current_coords)

#         for move in moves:
#             x, y, cost = move(current_node.x, current_node.y, current_node.cost)
#             new_node = Node(x, y, cost, current_node)
#             new_coords = (new_node.x, new_node.y)

#             if valid(new_node.x, new_node.y, obstacle_space) and new_coords not in closed_set:
#                 if new_coords in open_dict:
#                     if new_node.cost < open_dict[new_coords].cost:
#                         open_dict[new_coords].cost = new_node.cost
#                         open_dict[new_coords].parent_id = new_node.parent_id
#                         heapq.heappush(queue, (new_node.cost, new_node))
#                 else:
#                     open_dict[new_coords] = new_node
#                     heapq.heappush(queue, (new_node.cost, new_node))

#     return node_list, False

# def backtracking(goal_node):
#     x_path, y_path = [goal_node.x], [goal_node.y]

#     while goal_node.parent_id != -1:
#         goal_node = goal_node.parent_id
#         x_path.append(goal_node.x)
#         y_path.append(goal_node.y)

#     x_path.reverse()
#     y_path.reverse()

#     return x_path, y_path

# def plot_path(map, node_list, x_path, y_path, video_filename):
#     for node in node_list:
#         map[node[1], node[0]] = [0, 255, 0]  # Green color for explored nodes
#         video_writer.write(map)

#     for i in range(len(x_path) - 1):
#         cv2.line(map, (x_path[i], y_path[i]), (x_path[i + 1], y_path[i + 1]), (0, 0, 255), thickness=2)  # Red color for path
#         video_writer.write(map)


#     video_writer.release()

# if __name__ == '__main__':
#     obstacle_space = config_space()
    
#     if obstacle_space is None:
#         exit()

#     start_x = int(input("Enter x for Start Node: "))
#     start_y = int(input("Enter y for Start Node: "))
#     end_x = int(input("Enter x for Goal Node: "))
#     end_y = int(input("Enter y for Goal Node: "))   
    
#     start_node = Node(start_x, map_height - start_y, 0, -1)
#     goal_node = Node(end_x, end_y, 0, -1)
#     start_time = time.time()
#     node_list, goal_found = dijkstra(start_node, goal_node, obstacle_space)

#     end_time = time.time()

#     if goal_found:
#         print("Runtime [sec]: ", end_time - start_time)
#         x_path, y_path = backtracking(goal_node)
#         plot_path(map, node_list, x_path, y_path, video_filename)
#         print("Video 'output_video.mp4' created.")


#     else:
#         print("GOAL NODE NOT FOUND")
