
import os
from torchvision import transforms
from PIL import Image

# Define the path to the folder containing images
data_folder = train_dir

# Define the transformations
transform = transforms.Compose([
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(30),
    transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2, hue=0.1),
    transforms.Resize((256, 256)),
    transforms.ToTensor(),
])

for root, dirs, files in os.walk(data_folder):  # Changed to os.walk
    for filename in files:
        if filename.endswith(('.png', '.jpg', '.jpeg')):  # Check for image file types
            img_path = os.path.join(root, filename)  # Use root to get the correct path
            image = Image.open(img_path)

            # Apply the transformations
            augmented_image = transform(image)

            # Save or process the augmented image as needed
            augmented_img_path = os.path.join(root, 'augmented_' + filename)  # Save in the same folder
            # Convert tensor back to PIL Image and save
            augmented_image_pil = transforms.ToPILImage()(augmented_image).convert("RGB")
            augmented_image_pil.save(augmented_img_path)

# # Loop through each image in the folder
# for filename in os.listdir(data_folder):
#     if filename.endswith(('.png', '.jpg', '.jpeg')):  # Check for image file types
#         img_path = os.path.join(data_folder, filename)
#         image = Image.open(img_path)

#         # Apply the transformations
#         augmented_image = train_transforms(image)

#         # Save or process the augmented image as needed
#         # For example, you can save it back to the folder or a new folder
#         augmented_img_path = os.path.join(data_folder, 'augmented_' + filename)
#         # Convert tensor back to PIL Image and save
#         augmented_image_pil = transforms.ToPILImage()(augmented_image)
#         augmented_image_pil.save(augmented_img_path)

print("Image augmentation completed.")