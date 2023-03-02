import numpy as np
import pydicom
from pydicom.pixel_data_handlers.util import apply_windowing


def read_dicom_with_windowing(dcm_file):
    # from: https://www.kaggle.com/code/davidbroberts/mammography-apply-windowing/
    im = pydicom.dcmread(dcm_file)
    data = im.pixel_array
    
    # This line is the only difference in the two functions
    data = apply_windowing(data, im)
    
    if im.PhotometricInterpretation == "MONOCHROME1":
        data = np.amax(data) - data
    else:
        data = data - np.min(data)
        
    if np.max(data) != 0:
        data = data / np.max(data)
    data=(data * 255).astype(np.uint8)

    return data

def quadrant_text_to_array(x: str) -> np.array:
    """
    This function will return a 5 numbered array

    Examples of x:

    '["ÜST İÇ",  "ÜST DIŞ"]',
    '["ÜST İÇ"]',
    'nan'

    The order is:
    ALT DIŞ, ALT İÇ, MERKEZ, ÜST DIŞ, ÜST İÇ
    """
    mapping = {
        "ALT DIŞ": 0,
        "ALT İÇ": 1,
        "MERKEZ": 2,
        "ÜST DIŞ": 3,
        "ÜST İÇ": 4,
    }

    result = np.zeros(5)

    if x == "nan":
        return result
    # now read this string as a list
    x = eval(x)

    for quadrant in x:
        index = mapping[quadrant]
        result[index] = 1
    return result


def get_label_from_ordinal_breast_composition(ordinal_value: float) -> str:
    classes = ["A", "B", "C", "D"]
    # class_seperators = [i/num_labels for i in range(1, num_labels)]
    class_seperators = [0.25, 0.5, 0.75]
    for i, class_seperator in enumerate(class_seperators):
        if ordinal_value < class_seperator:
            return classes[i]
    return classes[-1]

def get_label_from_ordinal_birads(ordinal_value: float) -> str:
    classes = ["BI-RADS0", "BI-RADS1-2", "BI-RADS4-5"]
    class_seperators = [0.33, 0.66]
    for i, class_seperator in enumerate(class_seperators):
        if ordinal_value < class_seperator:
            return classes[i]
    return classes[-1]

