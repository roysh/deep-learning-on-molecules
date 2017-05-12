import argparse
from util import preprocess, partition, oversample
import h5py
import re


def get_arguments():
    parser = argparse.ArgumentParser(description='Prepares the data set for training')
    parser.add_argument('data', type=str, help='The data set containing the SMILES, class probability and partitioning')
    parser.add_argument('--oversample', action='store_true',
                        help='Oversample underrepresented classes in the training dataset')
    return parser.parse_args()


args = get_arguments()
prefix = args.data[:args.data.rfind('.')]
preprocess.preprocess(args.data, prefix + '-indices.h5', prefix + '-smiles_matrices.h5')
ids = []
source_hdf5 = h5py.File(args.data, 'r')
regex = re.compile('[0-9]+-classes')
for dataset in source_hdf5.keys():
    dataset = str(dataset)
    if regex.match(dataset):
        ids.append(dataset[:-8])
source_hdf5.close()
for id in ids:
    partition.write_partitions(args.data, prefix + '-smiles_matrices.h5', {1: 'train', 2: 'test', 3: 'validate'}, id)
if args.oversample:
    for id in ids:
        oversample.oversample(prefix + '-' + id + '-train.h5')