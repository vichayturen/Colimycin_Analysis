import math
import random
from typing import Dict, Any, List, Union

import torch
from torch import nn
import pandas as pd
from tqdm import tqdm
import matplotlib.pyplot as plt


class UniversalMlp(nn.Module):
    def __init__(self, hidden_size: int):
        super().__init__()
        self.up_proj = nn.Linear(hidden_size, hidden_size * 4)
        self.act = nn.SiLU()
        self.down_proj = nn.Linear(hidden_size * 4, hidden_size)

    def forward(self, x: torch.Tensor):
        residual = x
        x = self.down_proj(self.act(self.up_proj(x)))
        return x + residual


class UniversalClassificationModel(nn.Module):
    def __init__(self, feature_map: Dict[str, Dict[str, Any]], label_size: int = 2):
        super().__init__()
        self.feature_map = feature_map
        self.label_size = label_size
        self.categorical2id = {}
        categorical_id = 0
        self.numerical2id = {}
        numerical_id = 0
        for name, info in feature_map.items():
            if info["type"] == "categorical":
                for val in info["values"]:
                    self.categorical2id[f"{name}->{val}"] = categorical_id
                    categorical_id += 1
            elif info["type"] == "numerical":
                self.numerical2id[name] = numerical_id
                numerical_id += 1
            else:
                raise Exception("error")
        self.categorical_embed = nn.Embedding(categorical_id, categorical_id // 3)
        self.numerical_norm = nn.LayerNorm(numerical_id)
        self.numerical_embed = nn.Linear(numerical_id, numerical_id // 2)
        hidden_size = categorical_id // 3 + numerical_id // 2
        self.encoder = nn.ModuleList([UniversalMlp(hidden_size) for _ in range(24)])
        self.decoder = nn.Linear(hidden_size, label_size)

    def forward(self, xs: Union[Dict[str, Any], List[Dict[str, Any]]]):
        if isinstance(xs, dict):
            xs = [xs]
        batch_size = len(xs)
        categorical = [[] for _ in range(batch_size)]
        numerical = [[0] * len(self.numerical2id) for _ in range(batch_size)]
        for i, x in enumerate(xs):
            names = list(x.keys())
            for name in names:
                if name not in self.feature_map:
                    continue
                val = x[name]
                if self.feature_map[name]["type"] == "categorical":
                    cid = self.categorical2id[f"{name}->{val}"]
                    categorical[i].append(cid)
                elif self.feature_map[name]["type"] == "numerical":
                    nid = self.numerical2id[name]
                    minimum, mean, maximum = self.feature_map[name]["values"]
                    if pd.isna(val):
                        val = mean
                    norm_val = (val - minimum) / (maximum - minimum)
                    numerical[i][nid] = norm_val
                else:
                    raise Exception("error")
        hidden_states_1 = self.categorical_embed(torch.LongTensor(categorical)).sum(dim=-2)
        hidden_states_2 = self.numerical_embed(self.numerical_norm(torch.Tensor(numerical)))
        hidden_states = torch.cat([hidden_states_1, hidden_states_2], dim=-1)
        for layer in self.encoder:
            hidden_states = layer(hidden_states)
        hidden_states = self.decoder(hidden_states)
        return torch.softmax(hidden_states, dim=-1)

    def self_train(self, data: List[Dict[str, Any]], label_key, epoch_size: int = 10, shuffle: bool = True):
        batch_size = 16
        mini_batch_size = 4
        assert batch_size % mini_batch_size == 0, "batch_size must be divisible by mini_batch_size!"
        data_size = len(data)
        random.seed(369)
        if shuffle:
            random.shuffle(data)
        print("### preprocessing data...")
        labels = []
        for i in range(data_size):
            label = data[i][label_key]
            arr = [0] * self.label_size
            arr[int(label)] = 1
            labels.append(arr)
        labels = torch.Tensor(labels)
        print(f"### preprocessing data finished! data size = {data_size}, label size = {labels.size()}")
        optimizer = torch.optim.AdamW(self.parameters(), lr=1e-5)
        # lr_scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(
        #     optimizer,
        #     T_max=data_size // batch_size * 2
        # )
        if self.label_size <= 2:
            loss_fct = nn.MSELoss()
        else:
            loss_fct = nn.CrossEntropyLoss()
        print("### start training...")
        loss_record = []
        tbar = tqdm(total=epoch_size * math.ceil(data_size / batch_size))
        for epoch in range(epoch_size):
            for step in range(0, data_size, batch_size):
                optimizer.zero_grad()
                for mini_step in range(0, batch_size, mini_batch_size):
                    if step + mini_step >= data_size:
                        break
                    # print(step + mini_step, min(step + mini_step + mini_batch_size, data_size))
                    batch_data = data[step + mini_step: min(step + mini_step + mini_batch_size, data_size)]
                    batch_label = labels[step + mini_step: min(step + mini_step + mini_batch_size, data_size), :]
                    y = self(batch_data)
                    loss = loss_fct(y, batch_label)
                    loss_record.append(float(loss))
                    loss.backward()
                optimizer.step()
                # lr_scheduler.step()
                tbar.update()
        tbar.close()
        print("### training finished!")
        plt.plot(loss_record)
        plt.show()