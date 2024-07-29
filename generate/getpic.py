import os
from flask import Flask, send_file
from flask_cors import CORS
import matplotlib.pyplot as plt
import numpy as np
import torch
import torch.nn as nn
from PIL import Image
from torchvision import transforms

class FeatureAttention(nn.Module):
    def __init__(self, in_channel, n_head=1, reduction_ratio=8):
        super().__init__()
        self.n_head = n_head
        self.head_dim = in_channel // n_head
        self.reduction_ratio = reduction_ratio

        self.scale = self.head_dim ** -0.5

        self.query = nn.Conv2d(in_channel, in_channel // reduction_ratio, 1, bias=False)
        self.key = nn.Conv2d(in_channel, in_channel // reduction_ratio, 1, bias=False)
        self.value = nn.Conv2d(in_channel, in_channel, 1, bias=False)
        self.out = nn.Conv2d(in_channel, in_channel, 1)

        self.gamma = nn.Parameter(torch.zeros(1))

    def forward(self, x):
        batch, channel, height, width = x.shape
        reduced_dim = channel // self.n_head // self.reduction_ratio

        query = self.query(x).view(batch, self.n_head, reduced_dim, height * width)
        key = self.key(x).view(batch, self.n_head, reduced_dim, height * width)
        value = self.value(x).view(batch, self.n_head, self.head_dim, height * width)

        query = query.permute(0, 1, 3, 2)  # (batch, n_head, height * width, head_dim)
        key = key.permute(0, 1, 3, 2)  # (batch, n_head, height * width, head_dim)
        value = value.permute(0, 1, 3, 2)  # (batch, n_head, height * width, head_dim)

        # print(query.shape, key.shape, value.shape)

        dots = torch.einsum('bnhd,bnwd->bnhw', query, key) * self.scale
        attn = dots.softmax(dim=-1)

        # print(attn.shape, value.shape)

        out = torch.einsum('bnhw,bnwd->bnhd', attn, value)
        out = out.permute(0, 1, 3, 2).contiguous().view(batch, channel, height, width)

        out = self.gamma * self.out(out) + x

        return out

class UNet(nn.Module):
    def __init__(self, in_channels=3, out_channels=3):
        super(UNet, self).__init__()
        self.down1 = self.contract_block(in_channels, 64, 3, 1)
        self.down2 = self.contract_block(64, 128, 3, 1)
        self.down3 = self.contract_block(128, 256, 3, 1)
        self.down4 = self.contract_block(256, 512, 3, 1)
        self.down5 = self.contract_block(512, 1024, 3, 1)

        self.up1 = self.expand_block(1024, 512, 3, 1)
        self.up2 = self.expand_block(512 * 2, 256, 3, 1)
        self.up3 = self.expand_block(256 * 2, 128, 3, 1)
        self.up4 = self.expand_block(128 * 2, 64, 3, 1)
        self.up5 = nn.ConvTranspose2d(64 * 2, 64, kernel_size=3, stride=2, padding=1, output_padding=1)

        self.final_conv = nn.Conv2d(64, out_channels, kernel_size=3, padding=1)

        self.attn_d4 = FeatureAttention(512, n_head=2, reduction_ratio=64)
        self.attn_d5 = FeatureAttention(1024, n_head=2, reduction_ratio=8)
        self.attn_u1 = FeatureAttention(512, n_head=2, reduction_ratio=16)
        self.attn_u2 = FeatureAttention(256, n_head=2, reduction_ratio=64)


    def contract_block(self, in_channels, out_channels, kernel_size, padding):
        block = nn.Sequential(
            nn.Conv2d(in_channels, out_channels, kernel_size, padding=padding),
            nn.ReLU(),
            nn.BatchNorm2d(out_channels),
            nn.Conv2d(out_channels, out_channels, kernel_size, padding=padding),
            nn.ReLU(),
            nn.BatchNorm2d(out_channels),
            nn.MaxPool2d(kernel_size=2, stride=2)
        )
        return block

    def expand_block(self, in_channels, out_channels, kernel_size, padding):
        block = nn.Sequential(
            nn.ConvTranspose2d(in_channels, out_channels, kernel_size=3, stride=2, padding=1, output_padding=1),
            nn.ReLU(),
            nn.BatchNorm2d(out_channels),
            nn.Conv2d(out_channels, out_channels, kernel_size, padding=padding),
            nn.ReLU(),
            nn.BatchNorm2d(out_channels),
            nn.Conv2d(out_channels, out_channels, kernel_size, padding=padding),
            nn.ReLU(),
            nn.BatchNorm2d(out_channels),
        )
        return block

    def forward(self, x):
        d1 = self.down1(x)
        d2 = self.down2(d1)
        d3 = self.down3(d2)

        d4 = self.down4(d3)
        d4 = self.attn_d4(d4)

        d5 = self.down5(d4)
        d5 = self.attn_d5(d5)

        u1 = self.up1(d5)
        u1 = self.attn_u1(u1)

        u2 = self.up2(torch.cat([u1, d4], dim=1))
        u2 = self.attn_u2(u2)

        u3 = self.up3(torch.cat([u2, d3], dim=1))
        u4 = self.up4(torch.cat([u3, d2], dim=1))
        u5 = self.up5(torch.cat([u4, d1], dim=1))

        out = self.final_conv(u5)
        return out


def getpic(input_image_path):
    transform = transforms.Compose([
        transforms.Resize((1024, 1024)),
        transforms.ToTensor(),
    ])
    
    input_image_path = input_image_path
    input_image = transform(Image.open(input_image_path).convert('RGB')).unsqueeze(0)

    model = UNet()
    model_weights = torch.load('Unet_weights.pth')
    model.load_state_dict(model_weights)
    model = model.eval()

    with torch.no_grad():
        outputs = model(input_image).squeeze(0)
        outputs_np = outputs.permute(1,2,0).numpy() * 255
        outputs_np = outputs_np.astype(np.uint8)
        plt.imshow(outputs_np)
        plt.axis('off')
        plt.savefig("output.png")

app = Flask(__name__)
from flask import request, jsonify
CORS(app)
@app.route('/getpic', methods=['POST'])
def upload():
    # 检查是否存在上传文件
    if 'file' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    file = request.files['file']
    # 检查上传文件是否为空
    if file.filename == '':
        return jsonify({'error': 'No image selected'}), 400

    # 保存上传文件
    file.save('./' + file.filename)
    getpic(file.filename)
    return send_file("./output.png", mimetype='image/png')
if __name__ == '__main__' :
    app.run(host='0.0.0.0',port=5000)