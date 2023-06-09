import math

import pytest

from randmut import randmut
from numpy.testing import assert_array_almost_equal


def fun(x):
    return sum([math.sin(v) for v in x])

@pytest.mark.parametrize("n", [3, 5, 10])
def test_sinsum(n):
    (x, f, _) = randmut(fun, n * [(-math.pi, math.pi)], disp=False)
    x_true = n * [-math.pi/2]
    f_true = -n
    assert_array_almost_equal(x, x_true, decimal=2)
    assert_array_almost_equal(f, f_true, decimal=2)
