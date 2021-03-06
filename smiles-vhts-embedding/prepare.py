import argparse
from util import preprocess, partition, oversample
from os import path


def get_arguments():
    parser = argparse.ArgumentParser(description='Prepares the data set for training')
    parser.add_argument('data', type=str, help='The data set containing the SMILES, class probability and partitioning')
    return parser.parse_args()


args = get_arguments()
prefix = args.data[:args.data.rfind('.')]
preprocess.preprocess(args.data, prefix + '-indices.h5', prefix + '-smiles_matrices.h5')
partition.write_partition(args.data, prefix + '-train.h5', prefix + '-smiles_matrices.h5', 1)
partition.write_partition(args.data, prefix + '-test.h5', prefix + '-smiles_matrices.h5', 2)
partition.write_partition(args.data, prefix + '-validate.h5', prefix + '-smiles_matrices.h5', 3)
oversample.oversample(prefix + '-train.h5')
#if path.isfile(prefix + '-validate.h5'):
#    oversample.oversample(prefix + '-validate.h5')
