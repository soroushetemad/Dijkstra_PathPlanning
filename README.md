# dijkstra_Soroush_Etemad

## Overview

This Python code implements Dijkstra's algorithm for pathfinding in a 2D grid-based environment. The primary purpose of this code is to find the optimal path between a user-defined start and goal position on a 2D map containing obstacles.

## Features

1. **Map Input:**
   - The code takes as input a JPEG image representing a 2D map with obstacles outlined in black color. The user can choose the map of their choice.

2. **Obstacle Detection:**
   - The algorithm detects obstacles by identifying black pixels in the input map using a specified intensity threshold.

3. **Dijkstra's Algorithm:**
   - The core of the code is the implementation of Dijkstra's algorithm for finding the shortest path between a start and goal position in the map.

4. **User Interaction:**
   - Users can input the coordinates of the start and goal nodes to find the optimal path.

5. **Visualization:**
   - The code provides visual feedback by displaying the explored nodes in green and the optimal path in red on the original map.

6. **Runtime Measurement:**
   - The runtime of the algorithm is measured and displayed to provide insights into the efficiency of the pathfinding process.

## Usage Instructions

1. **Install Dependencies:**
   - Ensure you have the required dependencies installed, including OpenCV (`cv2`), NumPy (`numpy`), time, heapq

2. **Run the Code:**
   - First run the MapCreator.py code to create the .JPG image of the map with the predetermined obstacles
   - Ensure that the dijkstra_Soroush_Etemad.py script is in the same path as the image created by MapCreator.py (output_image.JPG).
   -  Finally, run dijkstra_Soroush_Etemad.py and the program will prompt you to input the start and goal coordinates.
   -  Once you enter your start and goal input coordinates, the program will output the calculated path
   -  To run the video animation, uncomment the commented code at the bottom which is identical to the code above it but includes videowriting features that will save a video of the animation as output_video.mp4
     

3. **Provide Input:**
   - Enter the x and y coordinates for the start and goal nodes when prompted.

4. **View Results:**
   - The program will display the map with the explored nodes marked in green and the optimal path in red. Additionally, the runtime of the algorithm will be printed.


