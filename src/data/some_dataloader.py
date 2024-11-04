import torch
import numpy as np
from torch.utils.data import DataLoader, Dataset


class SomeDataset(Dataset):
    """
    A dataset implements 2 functions
        - __len__  (returns the number of samples in our dataset)
        - __getitem__ (returns a sample from the dataset at the given index idx)
    """

    def __init__(self, dataset_parameters, **kwargs):
        super().__init__()
        ...


class SomeDatamodule(DataLoader):
     """
    Allows you to sample train/val/test data, to later do training with models.
        
    """
    def __init__(self):
        super().__init__()