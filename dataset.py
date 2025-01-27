import torch
from torch.utils.data import Dataset, DataLoader
import torchvision.transforms as transforms
import os 
import h5py


class ZaloLandscapeTrainValDataset(Dataset):
	def __init__(self, hdf5_file, root_dir, train, transform=None):
		if os.path.isfile(hdf5_file):
			self.hdf5_file = h5py.File(hdf5_file)
			self.train = train
			if train:
				self.train_imgs = self.hdf5_file["train_imgs"]
				self.train_labels = self.hdf5_file["train_labels"]
			else:
				self.val_imgs = self.hdf5_file["val_imgs"]
				self.val_labels = self.hdf5_file["val_labels"]
			self.root_dir = root_dir
			self.transform = transform
		else:
			print('Data path is not available!')
			exit(1)

	def __len__(self):
		if self.train:
			return (len(self.train_imgs))
		else: 
			return (len(self.val_imgs))

	def __getitem__(self, idx):
		if self.train:
			image = self.train_imgs[idx, ...]
			label = self.train_labels[idx]
		else:
			image = self.val_imgs[idx, ...]
			label = self.val_labels[idx]

		if self.transform:
			image = self.transform(image)

		return image, label

class ZaloLandScapeTestDataset(Dataset):
	"""Class for loading data"""
	def __init__(self, hdf5_file, root_dir, transform=None):	
		if os.path.isfile(hdf5_file):
			self.hdf5_file = h5py.File(hdf5_file)
			self.test_imgs = self.hdf5_file["test_imgs"]
			self.test_ids = self.hdf5_file["test_ids"]
			self.root_dir = root_dir
			self.transform = transform
		else:
			print('Data path is not available!')
			exit(1)

	def  __len__(self):
		return len(self.test_imgs)

	def  __getitem__(self, idx):
		image = self.test_imgs[idx, ...]
		image_id = self.test_ids[idx]

		if self.transform:
			image = self.transform(image)

		return image, image_id
		