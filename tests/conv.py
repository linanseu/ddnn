import os
import sys
sys.path.append('..')
import argparse

import numpy as np

import chainer_sequential.binary.utils.binary_util as bu
from chainer_sequential.binary.links.link_binary_convolution import BinaryConvolution2D
from chainer_sequential.binary.links.link_batch_normalization import BatchNormalization

x = np.random.random((2,2,5,5)).astype(np.float32)
bconv = BinaryConvolution2D(2, 2, ksize=3, stride=1, pad=1)
bconv.b.data = np.array([0.004, 0.006], dtype=np.float32)
bn = BatchNormalization(2)
bn.beta.data = np.array([-0.06, 0.01], dtype=np.float32)
bn.gamma.data = np.array([1.02, 1.2], dtype=np.float32)
bn(bconv(x)) #init mean and var
res = bn(bconv(x), test=True)
W = bconv.W.data
print bu.np_to_floatC(x.astype(np.float16), 'A_in', 'row_major')
print bu.np_to_uint8C(bu.binarize_real(W.reshape(2, -1)), 'F_in', 'row_major', pad='1')
print bu.np_to_packed_uint8C(bu.binarize_real(res.data.flatten()), 'C_actual', 'row_major', pad='0')

print bu.np_to_floatC(bconv.b.data.astype(np.float16), 'Bias', 'row_major')
print bu.np_to_floatC(bn.beta.data.astype(np.float16), 'Beta', 'row_major')
print bu.np_to_floatC(bn.gamma.data.astype(np.float16), 'Gamma', 'row_major')
print bu.np_to_floatC(bn.avg_mean.astype(np.float16), 'Mean', 'row_major')
print bu.np_to_floatC(np.sqrt(bn.avg_var).astype(np.float16), 'Std', 'row_major')
