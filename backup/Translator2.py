import cv2 as cv
import pyautogui
import numpy as np
import pytesseract 
import time
from pytesseract import Output
import easyocr
import re
import pymorphy2

def check_words(words):
    morph = pymorphy2.MorphAnalyzer()
    words = [x.lower() for x in words]
    f = open("banned_words.txt", 'r', encoding='utf-8')
    result = []
    banned_words = f.read().split()
    category = ""
    i = 0
    while i < len(banned_words):
        if (banned_words[i][-1] == ':'):
            category = banned_words[i]
            i += 1
            continue
        j = 0
        find_flag = False
        forms = morph.parse(banned_words[i])
        while (j < len(forms) and not find_flag):
            variants = forms[j].lexeme
            k = 0
            while (k < len(variants) and not find_flag):
                item = variants[k]
                k += 1
                if (item.word in words):
                    result.append(category.replace(":", "").replace("_", " "))
                    find_flag = True
            j += 1
        if (find_flag):
            i = find_category(banned_words, i + 1)
        else:
            i += 1
    return result

def find_category(banned_words, i):
    j = i
    while (j < len(banned_words)):
        if (banned_words[j][-1] == ":"):
            return j
        else:
            j += 1
    return j

def text_handler(text):
    list_words = list(filter(None, re.split(";| |\.|,|\n", text)))
    return (check_words(list_words))

#(width,height)
# screen_size=pyautogui.size()
pytesseract.pytesseract.tesseract_cmd=r'C:\Programs\Tesseract-OCR\tesseract.exe'
#initialize the object
# video = cv.VideoWriter('Recording.avi',  
#                          cv.VideoWriter_fourcc(*'MJPG'), 
#                          20, screen_size)

# text = open('words.txt','r',encoding="utf8").readlines()
# words = []
# for word in text:
#     words.append(word.split())

reader=easyocr.Reader(['ru'], gpu=True)
######################### обработка изображения
print('Recording.....')
while True:
    #click screen shot
    start_time=time.time()
    screen_shot_img = pyautogui.screenshot()

    frame = np.array(screen_shot_img)

    frame_start_h=frame.shape[0]
    frame_start_w=frame.shape[1]
    coef_to_upscale=3
    # new_frame=np.zeros(frame.shape, dtype='uint8')
    frame=cv.resize(frame,(frame_start_w*coef_to_upscale,frame_start_h*coef_to_upscale))
    
    frame_copy=frame.copy()
    frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    # frame = cv.cvtColor(frame, cv.COLOR_BGR2LAB)
    # frame=cv.bilateralFilter(frame,8,0,8,) #убирает шум но оставляет границы целыми, в отличие от GaussianBlur, но медленнее
    # frame=cv.GaussianBlur(frame,(1,1),0)
    # frame= cv.Canny(frame, 10,10) #рисует очертания
    ret, thresh1 = cv.threshold(frame, 0, 255, cv.THRESH_OTSU | cv.THRESH_BINARY)#конвертируем в бинарное изображение, с динамическим порогом THRESH_OTSU

    thresh1=cv.resize(thresh1,(frame_start_w,frame_start_h))
    frame_copy=cv.resize(frame_copy,(frame_start_w,frame_start_h))
    frame=cv.resize(frame,(frame_start_w,frame_start_h))
#########################
######################### выделяем текст средствами ocv и передаем обрубки на распознавание
    # rect_kernel = cv.getStructuringElement(cv.MORPH_RECT, (11, 3))#матрица для расширения контуров
    # dilation = cv.dilate(thresh1, rect_kernel, iterations = 3)#расширяем контуры
    # contours, hierarchy = cv.findContours(dilation, cv.RETR_EXTERNAL,cv.CHAIN_APPROX_NONE)
    # # contours, heirarchy =cv.findContours(thresh1, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
    # # cv.drawContours(new_frame, contours, -1, (255,255,255), 1)
    # for cnt in contours:
    #     x, y, w, h = cv.boundingRect(cnt)
        
    #     # Рисуем ограничительную рамку на текстовой области
    #     rect=cv.rectangle(frame_copy, (x, y), (x + w, y + h), (0, 255, 0), 2)

    #     # Обрезаем область ограничительной рамки
    #     if w< frame.shape[0] and h<frame.shape[1]/10:
    #         cropped = frame[y:y + h, x:x + w]
    #         config3=r'--psm 6'
    #         text=pytesseract.image_to_string(cropped,)
        
    #         cv.putText(frame_copy, text, (x, y - 10), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 200), 2)
#########################  
#########################конфиги для ptesseract
    config = r'--oem 3 --psm 6 -с tessedit_char_whitelist=QWERTYUIOPASDFGHJKLZXCVBNM0123456789'
    config2 = r'--psm 13 --oem 1 -c tessedit_char_whitelist=ABCDEFG0123456789'
    config3=r'--psm 13'
    # print(pytesseract.image_to_string(thresh1))
#########################
######################### текст выделяется ptesseract  

    # results = pytesseract.image_to_data(thresh1, output_type=Output.DICT, lang="eng")
    # for i in range (0, len(results['text']) ):
    #     x = results['left'][i]
    #     y = results['top'][i]

    #     w = results['width'][i]
    #     h = results['height'][i]

    #     text = results['text'][i]
    #     conf = int(results['conf'][i])

    #     if conf >=0 and h<thresh1.shape[0]/10 and w<thresh1.shape[1]/4:
    #         # text = ''.join([c if ord(c) < 128 else '' for c in text]).strip()
    #         text = ''.join([c if c in "QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm.?!,;:-" else '' for c in text]).strip()
    #         # cv.rectangle(frame_copy, (x, y), (x + w, y + h), (0, 255, 0), 2)
            
    #     # if text in words:    
    #         # print (text)
    #         if text !='':
    #             frame_copy[y:y + h, x:x + w]=128,128,128
    #             # cv.putText(frame_copy, text, (x, y - 10), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 200), 2)
    #             cv.putText(frame_copy, text, (x, y+10), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
#########################

######################### текст выделяется easyocr

    result=reader.readtext(frame,text_threshold=0.7,paragraph=True)
    for i in result:
        bbox, text=i
        handle_start_time=time.time()
        # if text_handler(text):
        #     x1=round(bbox[0][0])
        #     y1=round(bbox[0][1])
        #     x2=round(bbox[2][0])
        #     y2=round(bbox[2][1])
        # # print(f"x1={x1}, y1={y1}, x2={x2}, y2={y2}, text={text}")
        # # cv.rectangle(frame_copy,(x1,y1) , (x2,y2), (0, 255, 0), 2)
        #     frame_copy[y1:y2, x1:x2]=127,127,127
        #     cv.putText(frame_copy, str(text), (x1, y1+10), cv.FONT_HERSHEY_COMPLEX, 0.35, (255, 255, 255), 1,)
        handle_end_time=time.time()
#########################

    frame_to_show=frame_copy
    name_of_wind='win'
    cv.namedWindow(name_of_wind)
    cv.moveWindow(name_of_wind, frame_start_w,0)
    frame_to_show=cv.resize(frame_to_show,(frame_start_w,frame_start_h))
    cv.imshow(name_of_wind, frame_to_show) 

    # frame_to_show=thresh1
    # name_of_wind='win2'
    # cv.namedWindow(name_of_wind)
    # cv.moveWindow(name_of_wind, frame_start_w,0)
    # frame_to_show=cv.resize(frame_to_show,(frame_start_w,frame_start_h))
    # cv.imshow(name_of_wind, frame_to_show)

    # frame_to_show=frame
    # name_of_wind='win3'
    # cv.namedWindow(name_of_wind)
    # cv.moveWindow(name_of_wind, frame_start_w,0)
    # frame_to_show=cv.resize(frame_to_show,(frame_start_w,frame_start_h))
    # cv.imshow(name_of_wind, frame_to_show)

    # time.sleep(3)
    # #pytesseract.image_to_string(frame)
    #write frame
    # video.write(frame)

    #display the live recording 
    end_time=time.time()
    print("time per frame: ", end_time-start_time)
    print("time lost in text handler: ", handle_end_time-handle_start_time)
    if cv.waitKey(1) == ord('q'):
        break

cv.destroyAllWindows()
# video.release()