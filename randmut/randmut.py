"""
Main function of the random mutations optimization algorithm

Author: Andrey Chernyavskiy
E-mail: andrey.chernyavskiy@gmail.com
License: GPL-3.0
"""

import math
import time
from collections import namedtuple
from multiprocessing import Pool
from typing import List, Callable, NamedTuple, Any

import numpy as np
import numpy.random as rnd

from .visualization import print_init, print_status

ResultRM = namedtuple("ResultRM", "x f steps")

class StatusRM(NamedTuple):
    iteration: int
    time: int
    last_best_f: float
    stall: int
    n_stall: int
    fevals: int
    i: int = None
    n: int = None
    callback_result: Any = None


def randmut(fun,
            bounds: List[tuple],
            x0=None,
            scale: float = 1.0,
            n_pop: int = 50,
            n_des: int = 10,
            p_max: int = 2,
            p_min: int = -10,
            max_mut: int = 5,
            n_stall: int = 10,
            eps: float = 1e-6,
            max_iter: int = 1000,
            include_ancestor: bool = True,  # Guarantee monotonicity of result for non-stochastic functions
            disp: bool = True,
            disp_multiline: bool = True,  # Display status in a multilines or permanent single line
            callback: Callable[[StatusRM], str] = None,
            b=10):
    """

    :param callback: function to call after each iteration
    :param fun: function to minimize
    :param bounds: bounds of variables
    :param x0: initial state
    :param scale: mutations are multiplied by scale, initial state is in x0+-scale
    :param n_pop: population size; linearly increases computation time, increases the probability of finding the global minimum
    :param n_des: number of descendants;  linearly increases computation time, increases the speed of convergence nearby the obtained minimum
    :param p_max: maximal magnitude of mutation
    :param p_min: minimal magnitude of mutations
    :param max_mut: maximal number of mutations
    :param n_stall: number of "non-changing" (<eps) iterations to stop
    :param eps: precision of "non-changing" iteration
    :param max_iter: maximal number of iterations
    :param include_ancestor: add ancestor to its descendants, guarantee monotonicity for non-stochastic fun
    :param disp: display information
    :param disp_multiline: multiline or single-line regime of displaying info
    :param b: base of power of mutation
    :return: ResultRM
    """
    # timer
    start_time = time.time()
    elapsed = lambda: time.time() - start_time

    # inits
    n = len(bounds)
    iteration = 0
    fevals = 0
    stall = 0  # number of iteration with changes of best_f <eps
    steps = list()
    last_best_f = math.inf
    global_fs = n_pop * [math.inf]  # best values for all lines
    last_best_x = None

    # Bounds
    lb = np.array([b[0] for b in bounds])
    rb = np.array([b[1] for b in bounds])
    sb = rb - lb
    bound = lambda v: (v - lb) % sb + lb

    # Generating initial population
    if x0 is not None:
        gen_init = lambda: bound(x0 - scale + 2 * scale * rnd.random(n))
    else:
        gen_init = lambda: lb + sb * rnd.random(n)
    population = [gen_init() for _ in range(0, n_pop)]

    def gen_descendant(x):
        d = x.copy()
        mutnumb = rnd.randint(1, max_mut + 1)
        for _ in range(0, mutnumb):
            pos = rnd.randint(0, n)
            d[pos] += scale * sb[pos] * b ** rnd.randint(p_min, p_max + 1) * 2 * (rnd.rand() - 0.5)
        d = bound(d)
        return d

    with_callback = callback is not None
    if disp:
        print_init(with_callback)

    while (stall < n_stall) and (iteration < max_iter):
        iteration += 1
        for i in range(0, n_pop):
            ancestor = population[i]
            descendants = list(gen_descendant(ancestor) for _ in range(n_des))
            if include_ancestor:
                descendants.append(ancestor)

            # calculating values
            fs = [fun(d) for d in descendants]
            fevals += len(descendants)

            ind = np.argmin(fs)
            global_fs[i] = fs[ind]
            population[i] = descendants[ind]

            status = StatusRM(iteration=iteration, time=elapsed(), last_best_f=last_best_f,
                              stall=stall, n_stall=n_stall, fevals=fevals, i=i, n=n_pop)
            if disp:
                print_status(disp_multiline, with_callback, status)

        ind = np.argmin(global_fs)
        new_best_f = global_fs[ind]
        last_best_x = population[ind]
        if abs(last_best_f - new_best_f) < eps:
            stall += 1
        else:
            stall = 0
        last_best_f = new_best_f

        status = status._replace(last_best_f=last_best_f, stall=stall, i=None)

        if callback is not None:
            callback_result = callback(status)
            status = status._replace(callback_result=callback_result)

        steps.append(status)
        if disp:
            print_status(disp_multiline, with_callback, status)

    if (disp):
        print()
    return ResultRM(last_best_x, last_best_f, steps)

def std_bounds(n, radius=1):
    return n * [(-radius, radius)]


