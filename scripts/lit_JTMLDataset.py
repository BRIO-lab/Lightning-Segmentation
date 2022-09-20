"""
Sasank Desaraju
9/14/22
"""

"""
*** This actually does NOT have any Lightning in it. (-_-) ***
It is just a standard Pytorch dataset. I still created this newly to
remake it intentionally."""

import torch
from torch.utils.data import Dataset
from skimage import io
import numpy as np
import cv2
import os


class LitJTMLDataset(Dataset):
    def __init__(self, dataset):

        self.img_dir = '/media/sasank/LinuxStorage/Dropbox (UFL)/Canine Kinematics Data/TPLO_Ten_Dogs_grids'
        self.data_dir = ''  # I don't know if this will actually get used if I pass in a loaded dataset

        self.dataset = dataset
        self.images = self.dataset[1:,0]
        self.length = len(self.images)
        
        # image check
        #print('Image directory: ' + self.config.data_constants["IMAGE_DIRECTORY"])
        for idx in range(0,len(self.images)):
            if os.path.isfile(self.img_dir + '/' + self.images[idx]) ==False:
                raise Exception('Error, cannot find file: ' + self.images[idx])
        
        #print(self.config.data_constants['MODEL_TYPE'])
        for i,j in enumerate(self.dataset[0,:]):
            #if j == self.config.data_constants['MODEL_TYPE']:
            if j == 'fem':
                self.labels = self.dataset[1:,i]
        
        # label check
        for idx in range(0,len(self.labels)):
            if os.path.isfile(self.img_dir + '/' + self.labels[idx]) ==False:
                raise Exception('Error, cannot find file: ' + self.labels[idx])
    
    def __len__(self):
        return self.length

    def __getitem__(self, idx):
        image = io.imread(self.img_dir + '/' + self.images[idx], as_gray = True)
        label = io.imread(self.img_dir + '/' + self.labels[idx], as_gray = True)        
    
        label_dst = np.zeros_like(label)
        label_normed = cv2.normalize(label, label_dst, alpha = 0, beta = 1, norm_type = cv2.NORM_MINMAX)
        label = label_normed

    # SUBSET_PIXEL
	# This constrains the bounds of the image to just around the bone
        #if self.config.data_loader_parameters["SUBSET_IMAGES"] == True:
        if True:
            kernel = np.ones((30,30), np.uint8)
            label_dilated = cv2.dilate(label, kernel, iterations = 5)
            image_subsetted = cv2.multiply(label_dilated, image)
            image = image_subsetted
        
        """ implement once we put in transforms
        if self.transform is not None:
            image = np.array(image)
            label = np.array(label)
            transformed = self.transform(image = image, mask = label)
            image = transformed["image"]
            label = transformed["mask"]
        """

        
        image = torch.FloatTensor(image[None, :, :])
        label = torch.FloatTensor(label[None, :, :])
        img_name = self.images[idx]
        sample = {'image': image, 'label': label, 'img_name': img_name}


        return sample