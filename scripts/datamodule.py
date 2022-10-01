"""
Sasank Desaraju
9/13/22
"""

import torch
import pytorch_lightning as pl
import numpy as np
import os
from skimage import io
import cv2

from JTMLDataset import LitJTMLDataset


class SegmentationDataModule(pl.LightningDataModule):
    def __init__(self,
    config):
        super().__init__()

        self.img_dir = config.datamodule['IMAGE_DIRECTORY']
        self.train_data = os.getcwd() + '/data/' + config.init['MODEL_NAME'] + '/' + 'train_' + config.init['MODEL_NAME'] + '.csv'
        self.val_data = os.getcwd() + '/data/' + config.init['MODEL_NAME'] + '/' + 'val_' + config.init['MODEL_NAME'] + '.csv'
        self.test_data = os.getcwd() + '/data/' + config.init['MODEL_NAME'] + '/' + 'test_' + config.init['MODEL_NAME'] + '.csv'

        # Data loader parameters
        self.batch_size = config.datamodule['BATCH_SIZE']
        self.num_workers = config.datamodule['NUM_WORKERS']
        self.pin_memory = config.datamodule['PIN_MEMORY']
        self.shuffle = config.datamodule['SHUFFLE']
        self.data_loader_parameters = { 'batch_size': self.batch_size,
                                        'num_workers': self.num_workers,
                                        'pin_memory': self.pin_memory,
                                        'shuffle': self.shuffle}

        #self.log(batch_size=self.batch_size)
        # other constants

        self.train_set = np.genfromtxt(self.train_data, delimiter=',', dtype=str)
        self.val_set = np.genfromtxt(self.val_data, delimiter=',', dtype=str)
        self.test_set = np.genfromtxt(self.test_data, delimiter=',', dtype=str)

        # TODO: check train dataset length and integrity
        # TODO: check val dataset length and integrity

    """
    def prepare_data(self):

        return
    """

    def setup(self, stage):
        # actually do all the stuff here I think
        # naw we just left it in the JTMLDataset from old JTML for now

        """
        dataset = self.train_set

        if stage=='train' or stage is None:
            dataset = self.train_set
            #check dataset length and integrity

        if stage=='val' or stage is None:
            dataset = self.val_set

        created_dataset = LitJTMLDataset(dataset)
        """

        self.training_set = LitJTMLDataset(dataset=self.train_set, img_dir=self.img_dir)
        self.validation_set = LitJTMLDataset(dataset=self.val_set, img_dir=self.img_dir)
        self.test_set = LitJTMLDataset(dataset=self.test_set, img_dir=self.img_dir)

        return

    def train_dataloader(self):
        return torch.utils.data.DataLoader(self.training_set, **self.data_loader_parameters)

    def val_dataloader(self):
        return torch.utils.data.DataLoader(self.validation_set, **self.data_loader_parameters)

    def test_dataloader(self):
        return torch.utils.data.DataLoader(self.test_set, **self.data_loader_parameters)
