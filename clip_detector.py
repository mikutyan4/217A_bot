from clip_module import Clip
from detector import Detector
from PIL import Image

class Clip_detector(Detector):
    def __init__(self):
        super().__init__()
        self.clip = Clip()

    def run(self, image_path, visualize = False, save_name = 'result3.png'):
        boxes = super().forward(image_path)
        box = self.filter(boxes,image_path)
        if visualize:
            super().visualize(box, image_path, save_name)
            return box
        else:
            return box

    def filter(self, boxes, image_path):
        image = Image.open(image_path)
        for box in boxes:
            img = self.clipper(box, image)
            if self.bot_checker(img):
                return box
        return [0,0,0,0]

    def clipper(self,box, image):
        width, height = image.size
        y1 = box[0]*height
        x1 = box[1]*width
        y2 = box[2]*height
        x2 = box[3]*width
        cropped_img = image.crop((x1,y1,x2,y2))
        return cropped_img

    def bot_checker(self, img):
        simpicity = self.clip.run_with_img(img, text_list = ["white robot", 'people', 'sofa', 'bag','white chair' , 'something else'])
        #print(simpicity)
        if simpicity[0][0]:
            return True
        else:
            return False

if __name__ == "__main__":
    my_detector = Clip_detector()
    for index in range(6):
        print(my_detector.run(f"./test_pic/p{index+1}.jpg", visualize = True, save_name = f'test_p{index+1}.jpg'))