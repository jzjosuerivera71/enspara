import tempfile
import os

import numpy as np

from nose.tools import assert_equal, assert_is
from numpy.testing import assert_array_equal, assert_allclose

from enspara.msm import bace

# transitions counts matrix and expected results for the "simple" model in
# Bowman 2012 JCP paper describing BACE.

TCOUNTS = np.array(
    [[1000,  100,  100,   10,    0,    0,    0,    0,    0],
     [ 100, 1000,  100,    0,    0,    0,    0,    0,    0],
     [ 100,  100, 1000,    0,    1,    0,    0,    0,    0],
     [  10,    0,    0, 1000,  100,  100,   10,    0,    0],
     [   0,    0,    1,  100, 1000,  100,    0,    0,    0],
     [   0,    0,    0,  100,  100, 1000,    0,    1,    0],
     [   0,    0,    0,   10,    0,    0, 1000,  100,  100],
     [   0,    0,    0,    0,    0,    1,  100, 1000,  100],
     [   0,    0,    0,    0,    0,    0,  100,  100, 1000]])

EXP_BAYES_FACTORS = np.array(
    [[8.0, 8.54953122e+02],
     [7.0, 8.54953122e+02],
     [6.0, 8.55428120e+02],
     [5.0, 1.07233398e+03],
     [4.0, 1.07233398e+03],
     [3.0, 1.08250033e+03],
     [2.0, 4.85322085e+03],
     [1.0, 6.72422979e+03]])

EXP_MAPS = np.array(
    [[0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 1, 1, 1],
     [0, 0, 0, 1, 1, 1, 2, 2, 2],
     [0, 0, 0, 1, 2, 2, 3, 3, 3],
     [0, 0, 0, 1, 2, 2, 3, 4, 4],
     [0, 1, 1, 2, 3, 3, 4, 5, 5],
     [0, 1, 1, 2, 3, 4, 5, 6, 6],
     [0, 1, 1, 2, 3, 4, 5, 6, 7]])


def test_bace_integration():

    with tempfile.TemporaryDirectory(dir=os.getcwd()) as d:
        bace.run(TCOUNTS, nMacro=2, nProc=4, multiDist=bace.multiDistDense,
                 outDir=d, filterFunc=bace.filterFuncDense)

        print(os.listdir(d))

        bayes_factors = np.loadtxt(os.path.join(d, 'bayesFactors.dat'))
        assert_allclose(
            bayes_factors[:, 1], EXP_BAYES_FACTORS[:, 1],
            rtol=1e-6)

        maps = []
        for i in range(2, TCOUNTS.shape[0]):
            maps.append(np.loadtxt(os.path.join(d, 'map%s.dat' % i),
                                   dtype='int'))
