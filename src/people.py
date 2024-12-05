import cv2
import numpy as np

# Load the pre-trained MobileNet SSD model
prototxt_path = 'deploy.prototxt'  # Path to the deploy.prototxt file
caffe_model_path = 'mobilenet_iter_73000.caffemodel'  # Path to the caffemodel file

# Load the class labels
# MobileNet SSD class labels (80 classes)
class_labels = [
    'background', 'aeroplane', 'bicycle', 'bird', 'boat', 'bottle', 'bus', 'car', 
    'cat', 'chair', 'cow', 'diningtable', 'dog', 'horse', 'motorbike', 'person', 
    'pottedplant', 'sheep', 'sofa', 'train', 'tvmonitor'
]

# Load the model
net = cv2.dnn.readNetFromCaffe(prototxt_path, caffe_model_path)

# Load the image
image_path = 'people3.jpg'  # Path to your image
image = cv2.imread(image_path)

# Check if image is loaded correctly
if image is None:
    print("Error loading image")
    exit()

height, width = image.shape[:2]

# Prepare the image for detection
# Ensure the image is in the correct format and scale
blob = cv2.dnn.blobFromImage(image, 0.007843, (300, 300), (127.5, 127.5, 127.5), swapRB=True, crop=False)

net.setInput(blob)
detections = net.forward()

# Initialize a counter for detected people
person_count = 0

# Iterate over the detections
for i in range(detections.shape[2]):
    confidence = detections[0, 0, i, 2]  # Confidence score for the detection
    if confidence > 0.2:  # You can adjust this threshold
        class_id = int(detections[0, 0, i, 1])  # Class ID
        if class_labels[class_id] == 'person':  # Check if the detected object is a person
            person_count += 1
            box = detections[0, 0, i, 3:7] * np.array([width, height, width, height])
            (startX, startY, endX, endY) = box.astype("int")
            # Draw a bounding box around the detected person
            cv2.rectangle(image, (startX, startY), (endX, endY), (0, 255, 0), 2)

# Display the result
print(f"Number of people detected: {person_count}")
cv2.imshow("Detected People", image)
cv2.waitKey(0)
cv2.destroyAllWindows()