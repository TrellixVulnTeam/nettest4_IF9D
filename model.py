from torch import nn
from torchvision.models import resnet18

class FaceModel(nn.Module):

    def __init__(self, num_classes):
        super().__init__()
        self.base = resnet18()
        self.extract_feature = nn.Linear(512*4*3, 512)
        self.classifier = nn.Linear(512, num_classes)

    def forward(self, x):
        x = self.base.conv1(x)
        x = self.base.bn1(x)
        x = self.base.relu(x)
        x = self.base.maxpool(x)
        x = self.base.layer1(x)
        x = self.base.layer2(x)
        x = self.base.layer3(x)
        x = self.base.layer4(x)

        x = x.view(x.size(0), -1)
        feature = self.extract_feature(x)
        logits = self.classifier(feature)

        return logits, feature