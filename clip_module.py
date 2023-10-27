import torch
import clip
from PIL import Image
class Clip:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model, self.transform = clip.load("ViT-B/32", device=self.device)

    def run(self, image_path, text_list):
        image = self.transform(Image.open(image_path)).unsqueeze(0).to(self.device)
        text = clip.tokenize(text_list).to(self.device)
        image_features = self.model.encode_image(image)
        text_features = self.model.encode_text(text)
        similarity = (100.0 * image_features @ text_features.T).softmax(dim=-1)
        return similarity

    def run_with_img(self, imag, text_list):
        image = self.transform(imag).unsqueeze(0).to(self.device)
        text = clip.tokenize(text_list).to(self.device)
        image_features = self.model.encode_image(image)
        text_features = self.model.encode_text(text)
        similarity = (100.0 * image_features @ text_features.T).softmax(dim=-1)
        return similarity
    
if __name__ == "__main__":
    my_detector = Clip()
    print(my_detector.run('./detection/test2.jpg',["a photo of a robot", "a photo of something"]))