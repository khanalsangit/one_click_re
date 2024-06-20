import os
import cv2
import yaml

def load_yaml_labels(yaml_path):
    with open(yaml_path, 'r') as file:
        data = yaml.safe_load(file)
        return data.get('names', {})

def extract_points_from_string(line, shape):
    values = line.strip().split(' ')
    label = values[0]
    points = [(float(values[i]) * shape[1], float(values[i + 1]) * shape[0]) for i in range(1, len(values), 2)]
    return points, label

def extract_points_from_file(file_path, shape):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    all_points = []
    labels = []
    for line in lines:
        points, label = extract_points_from_string(line, shape)
        all_points.append(points)
        labels.append(label)
    return all_points, labels

def convert(input_folder, yaml_file_path):
    labels_dict = load_yaml_labels(yaml_file_path)

    for filename in os.listdir(input_folder):
        if filename.endswith(".txt"):
            file_path = os.path.join(input_folder, filename)
            image_filename = filename.replace(".txt", ".jpg")
            image_path = os.path.join(input_folder, image_filename)
            
            image = cv2.imread(image_path)
            if image is None:
                print(f"Error: Could not read image {image_path}")
                continue
            
            all_points, label_ids = extract_points_from_file(file_path, image.shape)
            
            with open(file_path, 'w') as file:
                for points, label_id in zip(all_points, label_ids):
                    label_name = labels_dict.get(int(label_id), "unknown")
                    points_str = ', '.join([f"{int(x)}, {int(y)}" for x, y in points])
                    file.write(f"{points_str}, {label_name}\n")
                # print(f"Updated file {file_path}")

    print("All labels updated successfully.")

# # Run the main function
# input_folder = "test1"
# yaml_file_path = "data.yaml"
# rec_main(input_folder, yaml_file_path)
