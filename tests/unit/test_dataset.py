from pytest_mock import MockerFixture
import object_detector
import cv2
import numpy as np

def test_double_dataset(mocker: MockerFixture):
    mocker.patch.object(object_detector, 'CONSTANT_COUNT_IMAGES_IN_DATASET', 855)
    expected = 1710
    actual = object_detector.increase_dataset()
    assert expected == actual


def test_load_dataset(mocker: MockerFixture):

    def mock_load(self):
        return 'Data'

    mocker.patch('object_detector.Dataset.load_data', mock_load)
    expected = "Data"
    actual = object_detector.load_dataset()
    assert expected == actual



from PIL import Image
import io

  
def test_prepare_image():
    # image into byte's array
    image = Image.open("32.jpeg")
    imgByteArr = io.BytesIO()
    image.save(imgByteArr, format=image.format)
    imgByteArr = imgByteArr.getvalue()
    image_preprocessing = object_detector.ImagePreprocessing()
    actual_image = image_preprocessing.prepare_image(imgByteArr)
    
    expected_size = (1, 50, 50, 3)
    assert expected_size == actual_image.shape



def test_selective_search():
    image = cv2.imread("32.jpeg")
    s_s = object_detector.SelectiveSearch()
    rects = s_s.selective_search(image)
    assert len(rects) >= 1

