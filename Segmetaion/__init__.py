from ultralytics import YOLO
import cv2
import numpy as np

class Segmetation:
    model = YOLO("yolo11n-seg.pt",verbose=False)
    @classmethod
    def getPersonSegment(cls,frame):
        results = cls.model.predict(frame, verbose=False)

        person_class_id = 0  # 'person' class ID from the names dictionary
        combined_mask = np.zeros((frame.shape[0], frame.shape[1]), dtype=np.uint8)
        for result in results:
            if result.masks is None:
                continue
            masks = result.masks.data.cpu().numpy()  # Convert tensor to numpy array
            for j, box in enumerate(result.boxes):
                if box.cls[0] == person_class_id:  # If the mask belongs to the 'person' class
                    resized_mask = cv2.resize(masks[j], (result.orig_img.shape[1], result.orig_img.shape[0]))
                    combined_mask = cv2.bitwise_or(combined_mask, (resized_mask > 0.5).astype(np.uint8))


        binary_mask = (combined_mask > 0.5).astype(np.uint8)  
        # masked_image = cv2.bitwise_and(frame, frame, mask=binary_mask)

        rgba_image = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)

        rgba_image[:, :, 3] = binary_mask * 255

        return rgba_image