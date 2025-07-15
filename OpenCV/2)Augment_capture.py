import cv2
import os
from PIL import Image, ImageEnhance, ImageFilter
import numpy as np
import random

input_path = "C:\\Users\\Amith\\OneDrive\\Desktop\\ML\\dataset"
output_path = "C:\\Users\\Amith\\OneDrive\\Desktop\\ML\\augment_dataset"

if not os.path.exists(output_path):
    os.makedirs(output_path)

def augment_image(img_path, output_dir, count=5):
    img = Image.open(img_path).convert('L')
    basename = os.path.basename(img_path)
    name, ext = os.path.splitext(basename)

    for i in range(count):
        aug = img.copy()

        # Random rotation
        angle = random.randint(-15, 15)
        aug = aug.rotate(angle)

        # Brightness
        enhancer = ImageEnhance.Brightness(aug)
        aug = enhancer.enhance(random.uniform(0.7, 1.3))

        # Add noise
        np_img = np.array(aug)
        noise = np.random.normal(0, 10, np_img.shape).astype('uint8')
        np_img = cv2.add(np_img, noise)
        aug = Image.fromarray(np_img)

        # Save augmented image
        new_name = f"{name}_aug{i}{ext}"
        aug.save(os.path.join(output_dir, new_name))

# Apply augmentation to all images
for file in os.listdir(input_path):
    if file.endswith(('.jpg', '.png', '.jpeg')):
        augment_image(os.path.join(input_path, file), output_path, count=10)

print("[INFO] Augmentation complete. Images saved to 'augmented_dataset'")
