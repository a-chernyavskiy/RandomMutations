# RandMut
Random mutations evolutionary optimization algorithm (https://arxiv.org/abs/1304.3703)

Before using the library, please read the [terms of use](#terms-of-use).

## Getting started

### Installation
To install the package download the files and run
```commandline
python setup.py install
```
or without downloading
```commandline
pip install git+https://github.com/a-chernyavskit/randmut.git
```

### Simple usage example
```python
import math
from randmut import randmut

def fun(x):
    return sum([math.sin(v) for v in x])

#Minimizing the sum of three sinuses in [-pi, pi]
(x, f, _) = randmut(fun, 3 * [(-math.pi, math.pi)])
```
More examples can be found [here](examples/)

## Documentation

Minimization is carried out by calling the `runmut` function.



#### Main parameters of `randmut`:
* `fun` - function to minimize
* `bounds` - a list of tuples setting bounds of variables; 
* `n_pop` - population size; linearly increases computation time, increases the probability of finding the global minimum
* `n_des` - number of descendants;  linearly increases computation time, increases the speed of convergence nearby the obtained minimum


The parameter `n_pop` is the main hyperparameter of the algorithm. Increase it according to the problem complexity. Increase `n_des` to have faster (in terms of iterations) local convergengence. Both parameters linearly increase the computational time of each iteration.

Bounds can be set like `3 * [(0, 1)]`. Also, `std_bounds(n, r)` can be used, which is equivalent to `n * [(-r, r)]`.

#### Termination
* `eps` - precision of "non-changing" iteration (default: `1e-6`)
* `n_stall` - number of "non-changing" (<`eps`) iterations to stop
* `max_iter` - maximal number of iterations

#### Return value
Function `ranmut` returns a named tuple of the type `ResultRM = namedtuple("ResultRM", "x f steps")`:
* `x` - found point
* `f` - found value
* `steps` - detailed information about algorithm steps

#### Output
* `disp`- print output iterations information or not (default: `True`)
* `multiline` - multiline or single-line regime of displaying iterations info (default: `True`)

#### Callback
* `callback` - function, which is called after ever iteration (default:`None`); see an [example](examples/callback.ipynb)

#### Additional parameters:
* `x0` - initial point (default: `None`) 
* `scale` - scale of the algorithm (default: `1.0`)
* `p_min` - minimal magnitude of mutations (default: `-10`)
* `p_max`- maximal magnitude of mutations (default: `2`)
* `maxmut`: maximal number of mutations(default: `5`); must be `>1`
* `include_ancestor`: add ancestor to its descendants (default: `True`); guarantee monotonicity for non-stochastic fun 
* `b`: base of power of mutation (default: `10`)

In each random mutation of parameters vectors, from `1` to `maxmut` parameters are being chosen. Varying parameter is being changed by a factor `m*b**p`, where `m` is uniformly distributed from `-1` to `1`, `p` is an integer uniformly distributed from `p_min` to `p_max`. 

The parameters`scale` and `x0` can be used together in a following scenario: find some minima with crude parameters, restart the algorithm from this point with e.g. bigger `n_pop` and lower `scale`.  Mutations are multiplied by scale, initial state is in `x0`±`scale`. 





## License
All code found in this repository is licensed under GPL v3.

For using the library in research work, please cite as:
> [1] Chernyavskiy A. Yu., Calculation of quantum discord and entanglement measures using the random mutations optimization algorithm, arXiv:1304.3703 [quant-ph], 2013.  
> [2] Chernyavskiy A. Yu., Global optimization solver for MATLAB, URL: https://github.com/PQCLab/RandomMutations
