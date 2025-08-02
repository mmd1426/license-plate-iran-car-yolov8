# Import libraries
from ultralytics import YOLO
import cv2
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import arabic_reshaper
from bidi.algorithm import get_display
import numpy as np
import attendance_system


# Load models
model_Chars = YOLO(r'/src/models/chars-model.pt')
model_Plate = YOLO(r'/src/models/plate-model.pt')

# Characters and numbers plate
Chars = ['0','1','2','3','4','5','6','7','8','9','الف','ب','د','دیپلمات','ع','ف','گ','ه','ج','ک','ل','م','ویلچر','ن','پ','ق','س','ص','ش','سیاسی','ت','ط','ث','و','ی','ز']

# Load background
Backg = cv2.imread(r'/src/background/background.png')
Backg = cv2.resize(Backg,(950,750))

# Input image to cap
cap = cv2.VideoCapture(r'test.jpg')

# Resized cap
cap.set(3,635)
cap.set(4,504)

while True:

    # Reading frame
    ret,frame = cap.read()

    # Prediction frame with the plate model
    result = model_Plate(frame)[0]
    
    # Create lists
    chars_plate = []
    list_chars = []
    score_plate = []

    if result:

        # Getting the coordinates of the predicted boxes
        for r in result.boxes.data.tolist():

            x1,y1,x2,y2,score,class_id = r
            x1,y1,x2,y2 = int(x1) , int(y1) , int(x2) , int(y2)

            score_plate.append([score,x1,y1,x2,y2])

        score_plate = sorted(score_plate)
        reversed(score_plate)

        # Cut plate from the image
        Plate = frame[score_plate[0][2]:score_plate[0][4],score_plate[0][1]:score_plate[0][3]]

        # cv2.rectangle(frame,(x1,y1),(x2,y2),(0,0,255),1)
        # cv2.imshow('Plate',Plate)
        
        # Prediction characters and numbers by chars model on plate image
        result_plate = model_Chars(Plate)[0]
        
        
        if result_plate:

            # Getting the coordinates of the predicted boxes
            for r in result_plate.boxes.data.tolist():
                x1,y1,x2,y2,score,class_id = r
                x1,y1,x2,y2 = int(x1) , int(y1) , int(x2) , int(y2)
                # cv2.rectangle(Plate,(x1,y1),(x2,y2),(0,0,255),1)
                list_chars.append([x1,class_id])       

    # Resizing frame
    frame = cv2.resize(frame,(635,504),interpolation=cv2.INTER_AREA)

    # Puting input image in background
    Backg[59:563,16:651] = frame

    if len(list_chars) == 8:

        list_chars.sort()

        for i,j in list_chars:
            chars_plate.append(Chars[int(j)])

        result = ''.join(chars_plate)

        Backg = Image.fromarray(Backg)

        # Position settings output text 
        text_1 = result[:2]
        text_2 = result[3:6]
        text_3 = result[6:9]
        text_4 = result[2]
        
        # Getting actions from attention sustem module
        Attendance_System_Plate = attendance_system.FunctionsQuery(result)
        name = Attendance_System_Plate.name_plate()

        # Reading fonts
        font_orginal = ImageFont.truetype(r'/src/fonts/khorshid.ttf',size=100)
        font_char = ImageFont.truetype(r'/src/fonts/ARIALBD.ttf',size=80)
        font_text = ImageFont.truetype(r'/src/fonts/ARIALBD.ttf',size=50)

        text_name = arabic_reshaper.reshape(name)
        text_name = get_display(text_name)
        
        # Puttinf text in background frame
        drawing_on_img = ImageDraw.Draw(Backg)
        drawing_on_img.text((100,610),text_1,font=font_orginal,fill='black')
        drawing_on_img.text((270,610),text_2,font=font_orginal,fill='black')
        drawing_on_img.text((430,620),text_3,font=font_orginal,fill='black')
        drawing_on_img.text((200,610),text_4,font=font_char,fill='black')
        drawing_on_img.text((662,630),text_name,font=font_text,fill='black')

        Backg = np.asarray(Backg)

        cv2.imshow('Project',Backg)

    else:

        
        font_text = ImageFont.truetype(r'/src/fonts/ARIALBD.ttf',size=50)

        text_not_found = 'پلاک یافت نشد'

        text_name = arabic_reshaper.reshape(text_not_found)
        text_name = get_display(text_name)

        drawing_on_img = ImageDraw.Draw(Backg)
        drawing_on_img.text((662,630),text_name,font=font_text,fill='black')

        Backg = np.asarray(Backg)

        cv2.imshow('Project',Backg)
    

    if cv2.waitKey(0) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()