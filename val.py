from __future__ import print_function
from __future__ import division
import os
import argparse
import torch
import torch.nn as nn
import torch.optim as optim
import torchvision
# from torchvision import datasets

from utils import data_transform, predict, ImageFolderWithPaths, plot_matrix
from sklearn.metrics import confusion_matrix, accuracy_score

print("PyTorch Version: ",torch.__version__)
print("Torchvision Version: ",torchvision.__version__)

def parse_opt(known=False):
    parser = argparse.ArgumentParser()
    parser.add_argument('--weights', type=str, default=None, help='initial weights path')
    parser.add_argument('--data', type=str, default=None, help='dataset directory path')
    parser.add_argument('--batch-size', type=int, default=16, help='total batch size for all GPUs')
    parser.add_argument('--device', default='', help='cuda device, i.e. 0 or 0,1,2,3 or cpu')
    parser.add_argument('--imgsz', '--img', '--img-size', type=int, default=640, help='inference size (pixels)')
    parser.add_argument('--name', type=str, default=None, help="model's name")

    opt = parser.parse_args()
    return opt

def main(opt):
    weights = opt.weights
    data_dir = opt.data
    batch_size = opt.batch_size
    device = opt.device
    image_size = opt.imgsz
    model_name = opt.name

    model = torch.load(weights)
    model = model.to(device)
    model.eval()

    data_transforms = data_transform(image_size)
    test_dataset = ImageFolderWithPaths(f"{data_dir}/test", data_transforms["val"])
    pred, true, paths = predict(test_dataset, model, batch_size, device)
    
    acc_score = accuracy_score(true, pred)
    cm = confusion_matrix(true, pred)
    nor_cm = confusion_matrix(true, pred, normalize="true")
    print(f'Accuracy : {acc_score}')
    print(f'Confusion Matrix :\n {cm}')

    # image_datasets = {x: datasets.ImageFolder(os.path.join(data_dir, x), data_transforms[x]) for x in ['test']}
    new_val_classes = test_dataset.classes

    plot_matrix(nor_cm, new_val_classes, model_name)



if __name__ == "__main__":
    opt = parse_opt()
    main(opt)