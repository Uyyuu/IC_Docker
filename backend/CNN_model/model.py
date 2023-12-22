import torch
import torch
import torchvision
import torchvision.transforms as transforms
import torch.nn as nn
import torch.nn.functional as F

# CNNの定義
#ver2.0のネットワーク
class CNN(nn.Module):
  def __init__(self, n_output, n_hidden):
    super(CNN,self).__init__()
    self.conv1 = nn.Conv2d(in_channels=3,out_channels=96,kernel_size=3,padding=1)
    self.maxpool1 = nn.MaxPool2d((2,2))
    self.conv2 = nn.Conv2d(in_channels=96,out_channels=256,kernel_size=3,padding=1)
    self.maxpool2 = nn.MaxPool2d((2,2))
    self.conv3 = nn.Conv2d(in_channels=256,out_channels=384,kernel_size=3,padding=1)
    self.conv4 = nn.Conv2d(in_channels=384,out_channels=256,kernel_size=3,padding=1)
    self.conv5 = nn.Conv2d(in_channels=256,out_channels=256,kernel_size=3)
    self.flatten = nn.Flatten()
    self.l1 = nn.Linear(9216,4096)
    self.relu1 = nn.ReLU(inplace=True)
    self.l2 = nn.Linear(4096,n_hidden)
    self.relu2 = nn.ReLU(inplace=True)
    self.l3 = nn.Linear(n_hidden,n_output)

    self.features = nn.Sequential(
        self.conv1,
        self.maxpool1,
        self.conv2,
        self.maxpool2,
        self.conv3,
        self.conv4,
        self.conv5

    )

    self.classifire = nn.Sequential(
        self.l1,
        self.relu1,
        self.l2,
        self.relu2
    )

  def forward(self, x):
    x1 = self.features(x)
    x2 = self.flatten(x1)
    x3 = self.classifire(x2)

    return x3

# 画像の前処理クラス
class DataTransform():
    def __init__(self):
        self.transform = transforms.Compose(
          # Resize()はintで引数渡すと
            [ transforms.Resize([32,32]),
              transforms.ToTensor(),
              transforms.Normalize((0.5,0.5,0.5),(0.5,0.5,0.5)) ]
        )

    def __call__(self,data):
        return self.transform(data)