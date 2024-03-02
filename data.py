from pytorch_lightning.utilities.types import TRAIN_DATALOADERS
import torch
from torch import nn, tensor
from torch.utils.data import Dataset, DataLoader
import pytorch_lightning as pl
import os
from tqdm import tqdm

class PEGData(Dataset):
    """
    Create training, validation and testing data for any of the languages
    for which passing and failing strings have already been enumerated
    in the corresponding directory.
    For each string, each character is mapped to a value in {0, 1, 2}.
    0 means that the string is still being parsed.
    1 means that the string has passed.
    2 means that the string has failed.

    Note that if any character maps to 1 or 2, all subsequent characters
    map to the same value.
    """
    def __init__(self, language, split):
        super().__init__()
        self.data_dir = language
        self.split = split
        match(language):
            case 'star':
                self.vocab = ['a', 'b']
            case 'brack':
                self.vocab = ['a', 'b', '[', ']']
            case 'expr':
                self.vocab = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '+', '×', '^', '[', ']']
            case 'triple':
                self.vocab = ['a', 'b', 'c']
            case 'dyck1':
                self.vocab = ['[', ']']
            case 'dyck3':
                self.vocab = ['[', ']', '(', ')', '{', '}']
        self.ctoi = self.vocab.index

        lines = 0
        with open(os.path.join(self.data_dir, f'{split}.txt'), 'r') as f:
            for line in f:
                lines += 1
                L = len(line)-2
        self.input = torch.zeros(lines, L).int()
        self.output = torch.zeros(lines, L).long()

    def get_data(self):
        filename = os.path.join(self.data_dir, f'{self.split}.txt')

        lines = 0
        with open(filename, 'r') as f:
            for line in f: lines += 1

        with open(filename, 'r') as f:
            i = 0
            for line in tqdm(f, total=lines, desc=f"Creating {self.split} dataloader"):
                s = line[:-1]
                self.input[i] = tensor([self.ctoi(c) for c in s if c not in [',', '|']])
                if '|' in s:
                    l = s.index('|')
                    self.output[i, l+1:] = 1
                else:
                    l = s.index(',')
                    self.output[i, l+1:] = 2
                self.output[i, :l+1] = 0
                i += 1

    def __len__(self):
        return self.input.shape[0]
    
    def __getitem__(self, i):
        return self.input[i], self.output[i]

class PEGDataModule(pl.LightningDataModule):
    def __init__(self, language, batch_size=32):
        super().__init__()
        self.language = language
        self.batch_size = batch_size

        self.train_dataset = PEGData(self.language, 'train')
        self.val_dataset = PEGData(self.language, 'val')
        self.test_dataset = PEGData(self.language, 'test')

        self.train_dataset.get_data()
        self.val_dataset.get_data()
        self.test_dataset.get_data()

    def train_dataloader(self):
        return DataLoader(self.train_dataset, batch_size=self.batch_size, shuffle=True)
    def val_dataloader(self):
        return DataLoader(self.val_dataset, batch_size=self.batch_size, shuffle=True)
    def test_dataloader(self):
        return DataLoader(self.test_dataset, batch_size=self.batch_size, shuffle=True)