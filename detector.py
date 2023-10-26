import tensorflow as tf
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as viz_utils
import numpy as np
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
import random

class Detector:
    def __init__(self):
        PATH_TO_MODEL_DIR = './detection/ssd_mobilenet_v2_320x320_coco17_tpu-8/saved_model'
        self.PATH_TO_MODEL_DIR = PATH_TO_MODEL_DIR
        self.detect_fn = tf.saved_model.load(PATH_TO_MODEL_DIR)
        print("detection model loaded!")

    def run(self, image_path, visualize = False, save_name = 'result3.png'):
        boxes = self.forward(image_path)
        box = self.filter(boxes)
        if visualize:
            visualize(box, image_path, save_name)
            return box
        else:
            return box

    def forward(self,image_path):
        img = Image.open(image_path)
        image_np = np.array(img)
        input_tensor = tf.convert_to_tensor(image_np)
        input_tensor = input_tensor[tf.newaxis, ...]
        detections = self.detect_fn(input_tensor)
        boxes = detections['detection_boxes'][0].numpy()
        return boxes[0:10]

    def filter(self, boxes):
        proposal = []
        for box in boxes:
            if self.area_check(box) and self.ratio_check(box):
                proposal.append(box)
        return proposal[random.randint(0,len(proposal)-1)]

    def visualize(self, box, image_path, save_name = 'result2.png'):
        img = Image.open(image_path)
        draw = ImageDraw.Draw(img)
        width, height = img.size
        top_left = (box[0]*height, box[1]*width)
        bottom_right = (box[2]*height, box[3]*width)
        draw.rectangle([top_left, bottom_right], outline = 'red')
        plt.figure(figsize=(10, 10))
        plt.imshow(img)
        plt.savefig(save_name)
        print(f"picture saved as {save_name}")

    def area_check(self, box, min = 0.01, max = 0.1):
        area = (box[2]-box[0])*(box[3]-box[1])
        if area <= min or area >= max:
            return False
        else:
            return True

    def ratio_check(self, box, min = 0.2, max =0.6):
        width = box[3] - box[1]
        height = box[2] - box[0]
        ratio = width / height
        if ratio <= min or ratio >= max:
            return False
        else:
            return True

if __name__ == "__main__":
    my_detector = Detector()
    print(my_detector.run("./detection/test2.jpg"))
"""
#for testing
if __name__ == "__main__":
    PATH_TO_MODEL_DIR = './detection/ssd_mobilenet_v2_320x320_coco17_tpu-8/saved_model'
    detect_fn = tf.saved_model.load(PATH_TO_MODEL_DIR)
    num_classes = 91
    category_index = {i: {'id': i, 'name': str(i)} for i in range(1, num_classes + 1)}
    IMAGE_PATH = './detection/test2.jpg'
    img = Image.open(IMAGE_PATH)
    image_np = np.array(img)
    input_tensor = tf.convert_to_tensor(image_np)
    input_tensor = input_tensor[tf.newaxis, ...]
    detections = detect_fn(input_tensor)
    viz_utils.visualize_boxes_and_labels_on_image_array(
        image_np,
        detections['detection_boxes'][0].numpy(),
        (detections['detection_classes'][0].numpy() + 1).astype(int),
        detections['detection_scores'][0].numpy(),
        category_index,
        use_normalized_coordinates=True,
        max_boxes_to_draw=200,
        min_score_thresh=.30,
        agnostic_mode=False)
    plt.figure(figsize=(10, 10))
    plt.imshow(image_np)
    plt.savefig('result2.png')
    boxes = detections['detection_boxes'][0].numpy()
    class_ids = (detections['detection_classes'][0].numpy() + 1).astype(int)

    # 遍历每个锚框
    for i in range(len(boxes)):
        box = boxes[i]
        class_id = class_ids[i]
        print(f"Box {i}: {box}, Class ID: {class_id}")
"""