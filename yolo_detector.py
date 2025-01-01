import torch

class YOLODetector:
    def __init__(self, model_path):
        self.model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_path)
    
    def detect(self, frame):
        # Perform object detection on the frame
        results = self.model(frame)
        return results.xyxy[0].cpu().numpy()  # Bounding box coordinates

    def get_hand_coordinates(self, frame):
        detections = self.detect(frame)
        for det in detections:
            # Assuming that 'hand' is class id 0 (you can fine-tune based on your YOLO model)
            if int(det[5]) == 0:
                # Return center of bounding box (hand coordinates)
                x_center = (det[0] + det[2]) / 2
                y_center = (det[1] + det[3]) / 2
                return int(x_center), int(y_center)
        return None
