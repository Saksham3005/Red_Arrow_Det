import cv2
import numpy as np

cap = cv2.VideoCapture(0)



def calculate_angle(point1, point2):
    angle = np.arctan2(point2[1] - point1[1], point2[0] - point1[0])
    return np.degrees(angle)

while True:
    _, frame = cap.read()
    
    height, width, _ = frame.shape
    center_x = width // 2
    start_point = (center_x, 0)  
    end_point = (center_x, height) 
    color = (0, 0, 255) 
    thickness = 2
    frame_with_line = cv2.line(frame, start_point, end_point, color, thickness)

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    

    
    lower_red1 = np.array([0, 100, 100])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([160, 100, 100])
    upper_red2 = np.array([180, 255, 255])
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    
    mask = cv2.bitwise_or(mask1, mask2)
    res = cv2.bitwise_and(frame, frame, mask=mask)

    
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    print(len(contours))

    
    if contours:
        
        largest_contour = max(contours, key=cv2.contourArea)
        
        
        rect = cv2.minAreaRect(largest_contour)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        
        
        cv2.drawContours(frame, [box], 0, (0, 255, 0), 2)
        
        
        
        angle = calculate_angle(box[0], box[1])
        print("Angle:", angle)
        
        
        cv2.putText(frame, "Angle: {:.2f} degrees".format(angle), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow('frame', frame)
    cv2.imshow('mask', mask)
    cv2.imshow('res', res)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('x'):
        break

cap.release()
cv2.destroyAllWindows()
