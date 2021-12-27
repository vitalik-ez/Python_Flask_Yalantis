import cv2
from tensorflow.keras.models import load_model
from keras.preprocessing.image import img_to_array
import numpy as np
from PIL import Image
import io

class Dataset:

    def __init__(self, file_path = './final_model.h5'):
        self.file_path = file_path

    def load_data(self):
        self.data = load_model(self.file_path)
        return self.data


CONSTANT_COUNT_IMAGES_IN_DATASET = 855


def load_dataset():
    dataset = Dataset()
    return dataset.load_data()

def increase_dataset():
    return 2 * CONSTANT_COUNT_IMAGES_IN_DATASET


class ImagePreprocessing:
    
    def __init__(self, width = 50, height = 50) -> None:
        self._width = width
        self._height = height

    def prepare_image(self, image):
        image = Image.open(io.BytesIO(image))
        image = np.float32(image.getdata()).reshape(image.size[0], image.size[1], 3)
        image = cv2.resize(image, (self._width, self._height))
        image = image.reshape(1, self._width, self._height, 3)
        image = image / 255.0
        return image

class SelectiveSearch():

    def __init__(self) -> None:
        self._ss = cv2.ximgproc.segmentation.createSelectiveSearchSegmentation()

    def selective_search(self, image):
        self._ss.setBaseImage(image)
        self._ss.switchToSelectiveSearchFast()
        rects = self._ss.process()
        #print("[INFO] {} total region proposals".format(len(rects)))
        return rects



class ObjectDetector():

    def __init__(self, file_path = './final_model.h5', width = 50, height = 50) -> None:
        self._model = load_model(file_path)
        self._width = width
        self._height = height
        self._dim = (width, height)

    def __proposals_objects(self, image, rects):
        self._proposals = []
        self._boxes = []

        for (x, y, w, h) in rects:
            if w / float(self._width) < 0.3 or h / float(self._height) < 0.3: # revise
                continue
            roi = image[y:y + h, x:x + w] # pay attention x y
            
            #Preprocess
            roi = ImagePreprocessing().prepare_image(roi)

            result = self._model.predict(roi)
            if np.argmax(result, axis=-1)[0] == 0 and result[0][0] > 0.98:
                self._proposals.append(roi)
                self._boxes.append((x, y, x+w, y+h, result[0][0])) # add result x+w y+h



    
    def detect_object(self, image, ss: SelectiveSearch = None):
        #rects = ss.selective_search(image)
        #self.__proposals_objects(rects, image)
        image = ImagePreprocessing().prepare_image(image)
    
        result = self._model.predict(image)
        result = {"traffic_cones": str(result[0][0]), "no_traffic_cones": str(result[0][1])}
        return result



    


