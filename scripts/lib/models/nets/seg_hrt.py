import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np

import pytorch_lightning as pl
import wandb

from lib.models.backbones.hrt.hrt_backbone import HighResolutionTransformer
from lib.models.backbones.hrt.hrt_config import MODEL_CONFIGS as model_configs
from lib.models.loss.loss_selector import LossSelector 

# cobbling together hrt for now TODO: Cleanup
class SegmentationNetModule(pl.LightningModule):    
    def __init__(self, config, wandb_run, learning_rate=1e-3):
        super().__init__()
        self.save_hyperparameters("learning_rate")
        self.config = config    
        self.pose_hrt = HighResolutionTransformer(cfg = model_configs[self.config.hrt_segmentation_net['MODEL_CONFIG']])
        print("Pose HRT is on device " + str(next(self.pose_hrt.parameters()).get_device()))     # testing line
        print("Is Pose HRT on GPU? " + str(next(self.pose_hrt.parameters()).is_cuda))            # testing line
        self.pose_hrt.to(device='cuda', dtype=torch.float32)                          # added recently and may fix a lot
        # *** IF the above line causes an error because you do not have CUDA, then just comment it out and the model should run, albeit on the CPU ***
        print("Pose HRT is on device " + str(next(self.pose_hrt.parameters()).get_device()))     # testing line
        print("Is Pose HRT on GPU? " + str(next(self.pose_hrt.parameters()).is_cuda))            # testing line
        self.wandb_run = wandb_run
        self.loss_fn = LossSelector(config = self.config, module_dict = config.hrt_segmentation_net).get_loss()
        self.loss_fn.to(device='cuda', dtype=torch.float32)

    def forward(self, x):
        """This performs a forward pass on the dataset

        Args:
            x (this_type): This is a tensor containing the information yaya

        Returns:
            the forward pass of the dataset: using a certain type of input
        """
        return self.pose_hrt(x)

    def configure_optimizers(self):
        #optimizer = torch.optim.Adam(self.parameters, lr=1e-3)
        optimizer = torch.optim.Adam(self.parameters(), lr=self.hparams.learning_rate)
        return optimizer

    def training_step(self, train_batch, batch_idx):
        training_batch, training_batch_labels = train_batch['image'], train_batch['label']
        x = training_batch
        print("Training batch is on device " + str(x.get_device()))         # testing line
        training_output = self.forward(x.cuda())
        #print(x.shape)
        #print(training_output[1].shape)
        #print(training_batch_labels.shape)
        t = torch.zeros(2,2,1024,1024)
        t[:,0,:,:] = (training_batch_labels[:,0,:,:]==0).float()
        t[:,1,:,:] = (training_batch_labels[:,0,:,:]==1).float()
        loss = self.loss_fn(training_output[1], t.cuda())
        #self.log('exp_train/loss', loss, on_step=True)
        #self.wandb_run.log('train/loss', loss, on_step=True)
        print(loss)
        self.wandb_run.log({'train/loss': loss})
        #self.log(name="train/loss", value=loss)
        return loss

    def validation_step(self, validation_batch, batch_idx):
        val_batch, val_batch_labels = validation_batch['image'], validation_batch['label']
        x = val_batch
        print("Validation batch is on device " + str(x.get_device()))       # testing line
        val_output = self.pose_hrt(x.cuda())
        t = torch.zeros(2,2,1024,1024)
        t[:,0,:,:] = (val_batch_labels[:,0,:,:]==0).float()
        t[:,1,:,:] = (val_batch_labels[:,0,:,:]==1).float()
        loss = self.loss_fn(val_output[1], t.cuda())
        #self.log('validation/loss', loss)
        #self.wandb_run.log('validation/loss', loss, on_step=True)
        self.wandb_run.log({'validation/loss': loss})
        #self.log('validation/loss', loss)
        image = wandb.Image(val_output[1], caption='Validation output')
        print(val_output[1])
        print(torch.nn.functional.softmax(val_output[1][0]))
        print(torch.nn.functional.softmax(val_output[1][1]))
        self.wandb_run.log({'val_output': image})
        return loss

    def test_step(self, test_batch, batch_idx):
        test_batch, test_batch_labels = test_batch['image'], test_batch['label']
        x = test_batch
        test_output = self.pose_hrt(x)
        loss = self.loss_fn(test_output, test_batch_labels)
        #self.log('test/loss', loss)
        #self.wandb_run.log('test/loss', loss, on_step=True)
        #self.wandb_run.log({'test/loss': loss})
        #self.on_test_batch_end(self, outputs=test_output, batch=test_batch, batch_idx=batch_idx)
        #self.on_test_batch_end(outputs=test_output, batch=test_batch, batch_idx=batch_idx, dataloader_idx=0)
        return loss
    
