from __future__ import absolute_import

from mxnet.gluon import nn, HybridBlock
from mxnet import init
from mxnet.gluon.model_zoo import vision


class ResNet(HybridBlock):
    __factory = {
        18: vision.resnet18_v1,
        34: vision.resnet34_v1,
        50: vision.resnet50_v1,
        101: vision.resnet101_v1,
        152: vision.resnet152_v1,
    }

    def __init__(self, depth, ctx, pretrained=True, num_classes=0):
        super(ResNet, self).__init__()
        self.pretrained = pretrained

        with self.name_scope():
            self.base = ResNet.__factory[depth](pretrained=pretrained, ctx=ctx).features
            self.base[-2][0].body[0]._kwargs['stride'] = (1, 1)
            self.base[-2][0].downsample[0]._kwargs['stride'] = (1, 1)
            self.base.add(nn.Flatten())
            bn = nn.BatchNorm(center=False, scale=True)
            bn.initialize(init=init.Zero(), ctx=ctx)
            self.base.add(bn)

            self.classifier = nn.Dense(num_classes, use_bias=False)
            self.classifier.initialize(init=init.Normal(0.001), ctx=ctx)


    def hybrid_forward(self, F, x):
        x = self.base(x)
        if self.pretrained:
            x = self.classifier(x)
        return x


def resnet18(**kwargs):
    return ResNet(18, **kwargs)


def resnet34(**kwargs):
    return ResNet(34, **kwargs)


def resnet50(**kwargs):
    return ResNet(50, **kwargs)


def resnet101(**kwargs):
    return ResNet(101, **kwargs)


def resnet152(**kwargs):
    return ResNet(152, **kwargs)