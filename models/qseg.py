# -*- coding: utf-8 -*-

"""
Query-based Scene Segmentation (QSegNet) Network PyTorch implementation.
"""

import torch
import torch.nn as nn

from .vilstm import VILSTM, VILSTMCell
from .psp.pspnet import PSPNet, PSPUpsample


class QSegNet(nn.Module):
    def __init__(self, in_size, vis_size, hid_size, dropout=0.2,
                 num_vlstm_layers=2, pretrained=True, batch_first=True,
                 psp_size=1024, backend='densenet', dict_size=8054,
                 out_features=512, num_lstm_layers=2):
        super().__init__()
        self.psp = PSPNet(n_classes=1, psp_size=psp_size,
                          pretrained=pretrained, backend=backend,
                          out_features=out_features)
        self.emb = nn.Embedding(dict_size, in_size)
        self.lstm = nn.LSTM(in_size, hid_size, dropout=dropout,
                            batch_first=batch_first)

        # self.vlstm = VILSTM(
        #     VILSTMCell, in_size, hid_size, num_layers=num_lstm_layers,
        #     batch_first=batch_first, visual_size=vis_size)

        # self.up_1 = PSPUpsample(out_features, 256)
        # self.up_2 = PSPUpsample(256, 64)
        # self.up_3 = PSPUpsample(64, 64)

        # self.drop_2 = nn.Dropout2d(p=0.15)
        # self.final = nn.Sequential(
        #     nn.Conv2d(64, 1, kernel_size=1),
        #     nn.LogSoftmax()
        # )

    def forward(self, imgs, words):
        psp_features = self.psp(imgs)
        features = psp_features.view(psp_features.size(0), -1)

        word_emb = self.emb(words)
        out, _ = self.lstm(word_emb)

        # x is of size BxLxHxH
        # B: Batch Size
        # L: Phrase length
        # H: Hidden Size
        x = torch.matmul(out.unsqueeze(-1), word_emb.unsqueeze(2))

        # (_, h) = self.vlstm(word_emb, features)
        # mask_map = h.view(psp_features.size())

        # p = self.up_1(mask_map)
        # p = self.drop_2(p)

        # p = self.up_2(p)
        # p = self.drop_2(p)

        # p = self.up_3(p)
        # p = self.drop_2(p)

        return self.final(p)
