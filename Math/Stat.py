__author__ = 'Arnaud KOPP'

import numpy as np


def kl(p, q):
    """Kullback-Leibler divergence D(P || Q) for discrete distributions

    or we can use scipy.stats.entropy with some parameters that became equal to that functions
    scipy.stats.entropy(pk, qk=None, base=None)
    If qk is not None, then compute a relative entropy (also known as Kullback-Leibler divergence or Kullback-Leibler
    distance) S = sum(pk * log(pk / qk), axis=0).

    Parameters
    ----------
    p, q : array-like, dtype=float, shape=n
        Discrete probability distributions.
    """
    p = np.asarray(p, dtype=np.float)
    q = np.asarray(q, dtype=np.float)

    return np.sum(np.where(p != 0, p * np.log(p / q), 0))