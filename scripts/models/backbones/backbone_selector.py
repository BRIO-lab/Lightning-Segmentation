##+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
## Created by: Donny You, RainbowSecret
## Microsoft Research
## yuyua@microsoft.com
## Copyright (c) 2019
##
## This source code is licensed under the MIT-style license found in the
## LICENSE file in the root directory of this source tree
##+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

#from lib.models.backbones.resnet.resnet_backbone import ResNetBackbone
#from lib.models.backbones.hrnet.hrnet_backbone import HRNetBackbone
from lib.models.backbones.hrt.hrt_backbone import HRTBackbone
#from lib.models.backbones.swin.swin_backbone import SwinTransformerBackbone
from lib.utils.tools.logger import Logger as Log


class BackboneSelector(object):
    def __init__(self, configer):
        self.configer = configer

    def get_backbone(self, **params):
        backbone = self.configer.get("network", "backbone")

        model = None

        if "hrt" in backbone:
            model = HRTBackbone(self.configer)(**params)

        elif "hrnet" in backbone:
            model = None

        else:
            Log.error("Backbone {} is invalid.".format(backbone))
            exit(1)

        return model
