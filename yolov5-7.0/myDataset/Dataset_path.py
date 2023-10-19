import os

def generate_absolute_dataset_txt(image_sets_dir, dataset_path, images_dir):
    # 确保数据集路径存在
    if not os.path.exists(dataset_path):
        os.makedirs(dataset_path)

    # 数据集划分的名称
    sets = ["train", "val", "test"]

    for set_name in sets:
        set_file_path = os.path.join(image_sets_dir, f'{set_name}.txt')
        output_file_path = os.path.join(dataset_path, f'{set_name}.txt')

        # 打开划分文件以及用于保存图像绝对路径的新文件
        with open(set_file_path, 'r') as set_file, open(output_file_path, 'w') as output_file:
            lines = set_file.readlines()
            for line in lines:
                image_name = line.strip()  # 去除换行符

                # 获取图像的绝对路径
                image_path = os.path.abspath(os.path.join(images_dir, f'{image_name}.jpg'))

                # 如果jpg格式的图像不存在，尝试png和jpeg
                if not os.path.exists(image_path):
                    image_path = os.path.abspath(os.path.join(images_dir, f'{image_name}.jpeg'))
                    if not os.path.exists(image_path):
                        image_path = os.path.abspath(os.path.join(images_dir, f'{image_name}.png'))

                # 将图像绝对路径写入新文件
                output_file.write(image_path + '\n')

if __name__ == "__main__":
    image_sets_dir = "ImageSets\\Main"  # 数据集划分文件夹的路径
    dataset_path = "dataSet_path"  # 保存生成的txt文件的文件夹路径
    images_dir = "C:\\Users\\cuime\\Desktop\\yolov5_7_eye\\yolov5-7.0\\myDataset\\images"  # 图像文件夹的绝对路径
    generate_absolute_dataset_txt(image_sets_dir, dataset_path, images_dir)
