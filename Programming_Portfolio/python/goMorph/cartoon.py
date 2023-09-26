import cv2
import numpy as np

# Global variables
selected_points = []
current_point = (-1, -1)
window_name = "Select Landmarks"
drawing_box = False
box_start = (-1, -1)
box_end = (-1, -1)

def mouse_callback(event, x, y, flags, param):
    global selected_points, current_point, drawing_box, box_start, box_end

    if event == cv2.EVENT_LBUTTONDOWN:
        if drawing_box:
            # User confirms the bounding box
            box_end = (x, y)
            drawing_box = False
        else:
            selected_points.append((x, y))
            current_point = (x, y)
    elif event == cv2.EVENT_MOUSEMOVE and drawing_box:
        # Update the end point while drawing the box
        box_end = (x, y)

def select_landmarks(image):
    global selected_points, drawing_box, box_start, box_end
    selected_points= [] # reset the selected points

    # Create a window and set the mouse callback function
    cv2.namedWindow(window_name)
    cv2.setMouseCallback(window_name, mouse_callback)

    # Loop until all landmarks are selected or the user presses 'Esc'
    while True:
        # Display the image with selected landmarks and the bounding box
        temp_image = image.copy()
        for point in selected_points:
            cv2.circle(temp_image, point, 3, (0, 255, 0), -1)
        if current_point != (-1, -1):
            cv2.circle(temp_image, current_point, 3, (0, 0, 255), -1)
        if drawing_box:
            cv2.rectangle(temp_image, box_start, box_end, (0, 0, 255), 2)
        cv2.imshow(window_name, temp_image)

        # Wait for key press
        key = cv2.waitKey(1) & 0xFF

        # Break the loop if 'Esc' key is pressed or all landmarks are selected
        if key == 27 or len(selected_points) == 68:
            break

    # Close the window
    cv2.destroyWindow(window_name)

    # Return the selected landmark points and bounding box coordinates
    return selected_points, (box_start, box_end)