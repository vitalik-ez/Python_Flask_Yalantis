import cv2
from tensorflow.keras.models import load_model
from keras.preprocessing.image import img_to_array
import numpy as np
from PIL import Image
import io

class ImagePreprocessing:
    pass

class SelectiveSearch():

    def __init__(self) -> None:
        self._ss = cv2.ximgproc.segmentation.createSelectiveSearchSegmentation()

    def selective_search(self, image):
        self._ss.setBaseImage(image)
        self._ss.switchToSelectiveSearchFast()
        rects = self._ss.process()
        print("[INFO] {} total region proposals".format(len(rects)))
        return rects




class ObjectDetector():

    def __init__(self, file_path = './final_model.h5', width = 50, height = 50) -> None:
        self._model = load_model(file_path)
        self._width = width
        self._height = height
        self._dim = (width, height)
        

    '''
     def __prepare_image(image):
        
        roi = cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)
        roi = cv2.resize(roi, (50, 50))
        roi = img_to_array(roi)
        roi = roi.reshape(1, 50, 50, 3)
        roi = roi / 255.0
    '''
   


    def __proposals_objects(self, image, rects):
        self._proposals = []
        self._boxes = []

        for (x, y, w, h) in rects:
            if w / float(self._width) < 0.3 or h / float(self._height) < 0.3: # revise
                continue
            roi = image[y:y + h, x:x + w] # pay attention x y
            
            #Preprocess
            roi = self.__prepare_image(roi)
            

            result = self._model.predict(roi)
            if np.argmax(result, axis=-1)[0] == 0 and result[0][0] > 0.98:
                self._proposals.append(roi)
                self._boxes.append((x, y, x+w, y+h, result[0][0])) # add result x+w y+h



    
    def detect_object(self, image, ss: SelectiveSearch = None):
        #rects = ss.selective_search(image)
        #self.__proposals_objects(rects, image)
        
        image = Image.open(io.BytesIO(image))
        width, height = image.size[0], image.size[1]
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!", width, height)
        image = np.float32(image.getdata()).reshape(1, image.size[0], image.size[1], 3)
        image = cv2.resize(image[0], (50, 50))
        image = image.reshape(1, 50, 50, 3)
        image = image / 255.0
        print("!!!!!!!!", image.shape)
        

        result = self._model.predict(image)
        result = {"traffic_cones": str(result[0][0]), "no_traffic_cones": str(result[0][1])}
        return result



    


