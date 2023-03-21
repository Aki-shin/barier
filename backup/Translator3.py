import cv2 as cv
import pyautogui
import numpy as np
import time
import easyocr
import re
import pymorphy2
from multiprocessing import Process, Pipe, Value
import image
import GUI

reader=easyocr.Reader(['ru'], gpu=True)
banned_words=[]



def init():
    f = open("banned words.txt", 'r', encoding='utf-8')
    global banned_words
    banned_words = f.read().split()
    morph = pymorphy2.MorphAnalyzer()
    result = []
    i = 0
    while i < len(banned_words):
        if banned_words[i][-1] == ':':
            result.append(banned_words[i].replace("_", " "))
            i += 1
        forms = morph.parse(banned_words[i])
        for form in forms:
            for x in form.lexeme:
                if (x.word not in result):
                    result.append(x.word)
        i += 1
    banned_words = result

def check_words(words):
    
    if isinstance(words, str):
        words = list(filter(None, re.split(";| |\.|,|\n", words)))
    words = list(map(str.lower, words))
    result = []
    category = ""
    i = 0
    while i < len(banned_words):
        if (banned_words[i][-1] == ':'):
            category = banned_words[i]
            i += 1
        j = 0
        find_flag = False
        if (banned_words[i] in words):
            result.append(category[:-1].replace("_", " "))
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

def proc_screen(ocr_io):
    while True:
        start=time.time()
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
        
        if ocr_io.poll():
            while ocr_io.poll():    
                ocr_io.recv()
                # print("ps accept")
            # print("ps send")
            ocr_io.send((frame,frame_copy))
        end=time.time()
        # print("ps time ",end-start)

def ocr_screen(ps_io,pr_io):
    while True:
        start=time.time()
        ps_io.send(True)
        ps_io.poll(timeout=None)
        frame,frame_copy=ps_io.recv()
        # print("ocr accept")
        result=reader.readtext(frame,text_threshold=0.7,paragraph=True)
        # print("ocr send")
        pr_io.send((result,frame_copy))
        end=time.time()
        print("ocr time ",end-start)

def proc_result(ocr_io,tumb_for_sound, tumb_for_disc, tumb_for_blur):
    init()
    while True:
        # print("pr start")
        ocr_io.poll(timeout=None)
        start=time.time()
        result,frame_copy=ocr_io.recv()
        # print("pr accep")
        categories=set()
        for i in result:
            bbox, text=i
            categories_temp=check_words(text)
            if categories_temp:
                categories.update(set(categories_temp))
                x1=round(bbox[0][0])
                y1=round(bbox[0][1])
                x2=round(bbox[2][0])
                y2=round(bbox[2][1])
            # print(f"x1={x1}, y1={y1}, x2={x2}, y2={y2}, text={text}")
            # cv.rectangle(frame_copy,(x1,y1) , (x2,y2), (0, 255, 0), 2)
                frame_copy[y1:y2, x1:x2]=127,127,127
        if categories:
            image.disclaimer(list(categories),tumb_for_sound, tumb_for_disc)
        

        frame_to_show=frame_copy
        name_of_wind='win'
        cv.namedWindow(name_of_wind)
        cv.moveWindow(name_of_wind, 1920,0)
        frame_to_show=cv.resize(frame_to_show,(1920,1080))
        cv.imshow(name_of_wind, frame_to_show)

        if cv.waitKey(1) == ord('q'):
            break 
        end=time.time()
        print("pr time ",end-start)
    cv.destroyAllWindows()

def view_result():
    
    pass

if __name__=="__main__":
    print('Recording.....')
    ps_io,ocr_io=Pipe()
    ocr_io2,pr_io=Pipe()

    tumb_for_sound=Value("i",0)
    tumb_for_disc=Value("i",0)
    tumb_for_blur=Value("i",0)

    ps=Process(target=proc_screen,args=(ocr_io,))
    ocr=Process(target=ocr_screen,args=(ps_io,pr_io,))
    pr=Process(target=proc_result,args=(ocr_io2,tumb_for_sound, tumb_for_disc, tumb_for_blur,))

    ps.start()
    ocr.start()
    pr.start()

    autorization_window = GUI.App(tumb_for_sound, tumb_for_disc, tumb_for_blur)
    autorization_window.mainloop()

    ps.join()
    ocr.join()
    pr.join()