#!/usr/bin/env python
# coding: utf-8

# In[1]:


import cv2 as cv
import numpy as np


# In[2]:


def mouse_event_handler(event, x, y, flags, param):
# Change 'mouse_state' (given as 'param') according to the mouse 'event'
 if event == cv.EVENT_LBUTTONDOWN:
  param[0] = True
  param[1] = (x, y)
 elif event == cv.EVENT_LBUTTONUP:
  param[0] = False
 elif event == cv.EVENT_MOUSEMOVE and param[0]:
  param[1] = (x, y)


# In[34]:


def free_drawing(canvas_width=640, canvas_height=480, init_brush_radius=3):
    # Prepare a canvas and palette
    canvas = np.full((canvas_height, canvas_width, 3), 255, dtype=np.uint8)
    b = g = r = 0
    palette = (b % 255 , g % 255, r % 255)

    # Initialize drawing states
    mouse_state = [False, (-1, -1)] # Note) [mouse_left_button_click, mouse_xy]
    brush_color = 0
    color_state = 'r'
    game_mode = "free_drawing"
    brush_radius = init_brush_radius

    # Instantiate a window and register the mouse callback function
    cv.namedWindow('Free Drawing')
    cv.setMouseCallback('Free Drawing', mouse_event_handler, mouse_state)

    while True:
        # Draw a point if necessary
        mouse_left_button_click, mouse_xy = mouse_state
        if mouse_left_button_click:
            if game_mode == 'circle':
                cv.circle(canvas, mouse_xy, 60+brush_radius, (b % 255 , g % 255, r % 255), 5)
            elif game_mode == 'rectangle':
                pt1, pt2 = (mouse_xy[0]-60-brush_radius, mouse_xy[1]-50-brush_radius), (mouse_xy[0]+60+brush_radius, mouse_xy[1]+50+brush_radius)
                cv.rectangle(canvas, pt1, pt2, color=(b % 255 , g % 255, r % 255), thickness=5)
            elif game_mode == 'triangle':
                pts = np.array([(mouse_xy[0], mouse_xy[1]-50-brush_radius), (mouse_xy[0]-55-brush_radius, mouse_xy[1]+50+brush_radius), (mouse_xy[0]+55+brush_radius, mouse_xy[1]+50+brush_radius)], dtype=np.int32).reshape(-1,1,2)
                cv.polylines(canvas, [pts], True, color=(b % 255 , g % 255, r % 255), thickness=5)
            else:
                cv.circle(canvas, mouse_xy, brush_radius, (b % 255 , g % 255, r % 255), -1)
        # Show the canvas
        canvas_copy = canvas.copy()
        info = f'Brush Radius: {brush_radius}'
        cv.putText(canvas_copy, info, (10, 25), cv.FONT_HERSHEY_DUPLEX, 0.6, (0, 0, 0), thickness=2)
        cv.putText(canvas_copy, info, (10, 25), cv.FONT_HERSHEY_DUPLEX, 0.6, (0, 0, 0))
        cv.putText(canvas_copy, 'r', (190, 25), cv.FONT_HERSHEY_DUPLEX, 0.6, (0 , 0, r % 255), thickness=2)
        cv.putText(canvas_copy, 'r', (190, 25), cv.FONT_HERSHEY_DUPLEX, 0.6, (0 , 0, r % 255))
        cv.putText(canvas_copy, '+', (210, 25), cv.FONT_HERSHEY_DUPLEX, 0.6, (0, 0, 0), thickness=2)
        cv.putText(canvas_copy, '+', (210, 25), cv.FONT_HERSHEY_DUPLEX, 0.6, (0, 0, 0))
        cv.putText(canvas_copy, 'g', (230, 25), cv.FONT_HERSHEY_DUPLEX, 0.6, (0 , g % 255, 0), thickness=2)
        cv.putText(canvas_copy, 'g', (230, 25), cv.FONT_HERSHEY_DUPLEX, 0.6, (0 , g % 255, 0))
        cv.putText(canvas_copy, '+', (250, 25), cv.FONT_HERSHEY_DUPLEX, 0.6, (0, 0, 0), thickness=2)
        cv.putText(canvas_copy, '+', (250, 25), cv.FONT_HERSHEY_DUPLEX, 0.6, (0, 0, 0))
        cv.putText(canvas_copy, 'b', (270, 25), cv.FONT_HERSHEY_DUPLEX, 0.6, (b % 255 , 0, 0), thickness=2)
        cv.putText(canvas_copy, 'b', (270, 25), cv.FONT_HERSHEY_DUPLEX, 0.6, (b % 255 , 0, 0))
        cv.putText(canvas_copy, '=', (290, 25), cv.FONT_HERSHEY_DUPLEX, 0.6, (0, 0, 0), thickness=2)
        cv.putText(canvas_copy, '=', (290, 25), cv.FONT_HERSHEY_DUPLEX, 0.6, (0, 0, 0))
        cv.putText(canvas_copy, "color", (310, 25), cv.FONT_HERSHEY_DUPLEX, 0.6, (b % 255 , g % 255, r % 255), thickness=2)
        cv.putText(canvas_copy, "color", (310, 25), cv.FONT_HERSHEY_DUPLEX, 0.6, (b % 255 , g % 255, r % 255))
        cv.putText(canvas_copy, "mode = ", (380, 25), cv.FONT_HERSHEY_DUPLEX, 0.6, (0, 0, 0), thickness=2)
        cv.putText(canvas_copy, "mode = ", (380, 25), cv.FONT_HERSHEY_DUPLEX, 0.6, (0, 0, 0))
        cv.putText(canvas_copy, game_mode, (470, 25), cv.FONT_HERSHEY_DUPLEX, 0.6, (0, 0, 0), thickness=2)
        cv.putText(canvas_copy, game_mode, (470, 25), cv.FONT_HERSHEY_DUPLEX, 0.6, (0, 0, 0))
        
        
        cv.imshow('Free Drawing', canvas_copy)
        # Process the key event
        key = cv.waitKey(1)
        if key == 27: # ESC
          break
        elif key == ord(' '):
            if color_state == 'b':
                b += 1
            elif color_state == 'g':
                g += 1
            else:
                r += 1
        elif key == ord('u'): #up
            if color_state == 'r':
                color_state = 'b'
            elif color_state == 'g':
                color_state = 'r'
            else:
                color_state = 'g'
        elif key == ord('d'): #down
            if color_state == 'r':
                color_state = 'g'
            elif color_state == 'g':
                color_state = 'b'
            else:
                color_state = 'r'        
        elif key == ord('c'):
            game_mode = "circle"
        elif key == ord('r'):
            game_mode = "rectangle"  
        elif key == ord('t'):
            game_mode = "triangle"
        elif key == ord('f'):
            game_mode = "free_drawing"
        elif key == ord('+') or key == ord('='):
          brush_radius += 1
        elif key == ord('-') or key == ord('_'):
          brush_radius = max(brush_radius - 1, 1)
        elif key == ord('e'):
             canvas = np.full((canvas_height, canvas_width, 3), 255, dtype=np.uint8)
    cv.destroyAllWindows()


# In[ ]:


if __name__ == '__main__':
  free_drawing() 


# In[ ]:




