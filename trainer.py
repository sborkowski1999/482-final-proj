import os
import yaml
from tensorflow.keras import layers
from tensorflow.keras import Model
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.optimizers import RMSprop

def read_dataset(folder_path):
    dataset = []
    for item_name in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item_name)
        item_label = item_name[0]
        item_images = []
        for image_name in os.listdir(folder_path):
            item_images.append(item_path)
            
        dataset.append({
            'label': item_label,
            'images': item_images
        })
    return dataset

def create_yaml_file(dataset, output_file):
    with open(output_file, 'w') as file:
        yaml.dump(dataset, file)

# Provide the path to your dataset folder
organic_folder = r'C:\Users\steve\Downloads\DATASET\TRAIN\O'
recycle_folder = r'C:\Users\steve\Downloads\DATASET\TRAIN\R'
# Read the dataset from the folder
organic_dataset = read_dataset(organic_folder)
recycling_dataset = read_dataset(recycle_folder)

final_dataset = []
final_dataset.append(organic_dataset)
final_dataset.append(recycling_dataset)

# Provide the desired output file path
output_yaml_file = r'C:\Users\steve\Desktop\482 final proj\trained.yaml'

# Create the YAML file
create_yaml_file(final_dataset, output_yaml_file)