import dlib
import cv2
import numpy as np
import cartoon

class NoFaceFound(Exception):
   """Raised when there is no face found"""
   pass

def get_facial_points(images: list, cartoon_bool, hard_coded) -> list:
    """
    Takes a list of images, finds a face, and returns a 76 point list back.
    68 points for the facial features, and 8 to encorparate a background
    """
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

    facial_points = []
    facial_points_list = []

    if cartoon_bool:
        if hard_coded == 0:
            cartoon_points, _ = cartoon.select_landmarks(images[1])
        # this is for the first time it's called
        elif hard_coded == 1:
            cartoon_points = [(215, 80), (222, 228), (135, 156), (301, 155), (276, 102), (165, 218), (158, 107), (272, 208), (337, 152), (503, 149), (427, 72), (423, 223), (365, 94), (468, 207), (364, 202), (486, 101), (321, 201), (320, 188), (318, 169), (339, 199), (358, 215), (358, 241), (340, 243), (313, 244), (296, 239), (295, 221), (300, 216), (279, 243), (267, 259), (280, 281), (286, 301), (291, 325), (312, 326), (323, 322), (333, 328), (344, 329), (359, 325), (359, 317), (359, 298), (366, 286), (382, 282), (390, 274), (392, 261), (385, 252), (374, 237), (329, 275), (309, 279), (352, 280), (326, 300), (71, 204), (66, 253), (67, 293), (85, 329), (115, 360), (159, 390), (210, 429), (272, 444), (322, 450), (377, 442), (421, 413), (474, 382), (518, 332), (554, 303), (580, 273), (590, 238), (588, 217), (577, 185), (350, 117)]
        # for when it's scaled
        elif hard_coded == 2:
            cartoon_points = [(215, 80), (222, 228), (135, 156), (301, 155), (276, 102), (165, 218), (158, 107), (272, 208), (337, 152), (503, 149), (427, 72), (423, 223), (365, 94), (468, 207), (364, 202), (486, 101), (321, 201), (320, 188), (318, 169), (339, 199), (358, 215), (358, 241), (340, 243), (313, 244), (296, 239), (295, 221), (300, 216), (279, 243), (267, 259), (280, 281), (286, 301), (291, 325), (312, 326), (323, 322), (333, 328), (344, 329), (359, 325), (359, 317), (359, 298), (366, 286), (382, 282), (390, 274), (392, 261), (385, 252), (374, 237), (329, 275), (309, 279), (352, 280), (326, 300), (71, 204), (66, 253), (67, 293), (85, 329), (115, 360), (159, 390), (210, 429), (272, 444), (322, 450), (377, 442), (421, 413), (474, 382), (518, 332), (554, 303), (580, 273), (590, 238), (588, 217), (577, 185), (350, 117)]
        else:
            # for when it's cropped
            cartoon_points = [(215, 80), (222, 228), (135, 156), (301, 155), (276, 102), (165, 218), (158, 107), (272, 208), (337, 152), (503, 149), (427, 72), (423, 223), (365, 94), (468, 207), (364, 202), (486, 101), (321, 201), (320, 188), (318, 169), (339, 199), (358, 215), (358, 241), (340, 243), (313, 244), (296, 239), (295, 221), (300, 216), (279, 243), (267, 259), (280, 281), (286, 301), (291, 325), (312, 326), (323, 322), (333, 328), (344, 329), (359, 325), (359, 317), (359, 298), (366, 286), (382, 282), (390, 274), (392, 261), (385, 252), (374, 237), (329, 275), (309, 279), (352, 280), (326, 300), (71, 204), (66, 253), (67, 293), (85, 329), (115, 360), (159, 390), (210, 429), (272, 444), (322, 450), (377, 442), (421, 413), (474, 382), (518, 332), (554, 303), (580, 273), (590, 238), (588, 217), (577, 185), (350, 117)]
        print(f'cartoon points {cartoon_points}')
    
    for image in images[:-1]:

        facial_bounding_box = detector(image, 1) # returns top left and bottom right coors of a face

        try:
            if len(facial_bounding_box) == 0:
                raise NoFaceFound
        except NoFaceFound:
            print("Sorry, but I couldn't find a face in the image.")

        for k, rect in enumerate(facial_bounding_box):

            # Get the landmarks/parts for the face in rect.
            shape = predictor(image, rect)

            for i in range(0,68):
                x = shape.part(i).x
                y = shape.part(i).y
                facial_points.append((x, y))
                # cv2.circle(image, (x, y), 1, (0, 255, 0), 1)

    facial_points_list.append(facial_points)    # we then add the facial points to a list containing all the fps

    if cartoon_bool: facial_points_list.append(cartoon_points)
    
    return facial_points_list

def add_background_points(height, width) -> list:

    """
    Adds 8 points to a list, the four corners and the 4 midpoints between them, and returns the list based on the width and height of an image
    """

    facial_points = []

    TOP_LEFT = (0,0)
    TOP_MIDDLE = (width//2, 0)
    TOP_RIGHT = (width-1, 0)
    LEFT_MIDDLE = (0, height//2-1)
    RIGHT_MIDDLE = (width-1, height//2-1)
    BOTTOM_LEFT = (0, height-1)
    BOTTOM_MIDDLE = (width//2, height-1)
    BOTTOM_RIGHT = (width-1, height-1)

    # Add back the background
    facial_points.append(TOP_LEFT)
    facial_points.append(TOP_MIDDLE)
    facial_points.append(TOP_RIGHT)
    facial_points.append(LEFT_MIDDLE)
    facial_points.append(RIGHT_MIDDLE)
    facial_points.append(BOTTOM_LEFT)
    facial_points.append(BOTTOM_MIDDLE)
    facial_points.append(BOTTOM_RIGHT)

    return facial_points
    

def find_facial_center(facial_points_list: list) -> list:
    """
    Returns a list of rectanges that bound the points given in the facial_points_list
    """
    center_points_list = []

    for facial_point in facial_points_list:
        center_points_list.append(cv2.boundingRect(np.array(facial_point))) 
    return center_points_list

def get_bounding_rects(facial_points: list):
    bounding_rects = []

    for facial_point in facial_points:
        x,y,w,h =cv2.boundingRect(np.array(facial_point))
        bounding_rects.append((x,y,w,h))

    return bounding_rects

def scale_by_facial_rectangle(bounding_rects, images, cartoon_bool):
    sizes_x, sizes_y = {}, {}
    for i, (_, _, w, h) in enumerate(bounding_rects):
        # take the width and height of the bounding rects, add them to a list, so we have a list of x and ys
        sizes_x[i] = w
        sizes_y[i] = h

    # determine the minimum x and y
    minimum_res_x = min(sizes_x.values())
    minimum_res_y = min(sizes_y.values())
    # calc the aspect ratio
    min_aspect_ratio = 1/(minimum_res_x / minimum_res_y)
    print(f'minx: {minimum_res_x}, miny: {minimum_res_y}, aspect ratio: {min_aspect_ratio}')

    scaled_images = []

    for i, image in enumerate(images):
        curr_aspect_ratio = sizes_x[i] / sizes_y[i]
        print(f'current aspect ratio of image {i}, is {curr_aspect_ratio}')
        if curr_aspect_ratio > min_aspect_ratio:
            scale_factor = minimum_res_y / sizes_y[i]
        else:
            scale_factor = minimum_res_x / sizes_x[i]
        print(f'new aspect ratio is {scale_factor}')
        scaled_images.append(cv2.resize(image, None, fx=scale_factor, fy=scale_factor))

    scaled_facial_points_list = get_facial_points(scaled_images, cartoon_bool, hard_coded=0) #2

    scaled_bounding_rects_list = get_bounding_rects(scaled_facial_points_list)

    return scaled_images, scaled_facial_points_list, scaled_bounding_rects_list

def get_rect_centroid(bounding_rect):
    x,y,w,h = bounding_rect
    # get centroid
    centroid_x = x + (w/2)
    centroid_y = y + (h/2)

    return centroid_x, centroid_y