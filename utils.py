import numpy as np
from scipy import stats
import math


def fit_line(x: np.ndarray, y: np.ndarray) -> tuple[float, float, np.ndarray]:
    if np.any(x <= 0) or np.any(y <= 0):
        raise ValueError("Все значения X и Y должны быть положительными")
    log_x = np.log(x)
    log_y = np.log(y)
    k, log_b = np.polyfit(log_x, log_y, 1)
    b = np.exp(log_b)
    y_pred = b * x ** k
    return k, b, y_pred


def calculate_k(x, y, n):
    sum_ln_x = sum(math.log(x) for x in x)
    sum_ln_y = sum(math.log(y) for y in y)
    sum_ln_xln_y = sum(math.log(x[i]) * math.log(y[i]) for i in range(n))
    sum_ln_x_squared = sum(math.log(x) ** 2 for x in x)
    numerator = sum_ln_x * sum_ln_y - n * sum_ln_xln_y
    denominator = sum_ln_x ** 2 - n * sum_ln_x_squared

    if denominator == 0:
        return float('inf')

    k = numerator / denominator
    return k


def calculate_sigma(y, yi):
    n = len(yi)
    sum_squared_diff = sum([(y[i] - yi[i]) ** 2 for i in range(n)])
    sigma = math.sqrt(sum_squared_diff / (n - 1))
    return sigma


def calculate_stats(x: np.ndarray, y: np.ndarray, y_pred: np.ndarray) -> tuple[float, float]:
    sigma = calculate_sigma(y, y_pred)
    n = len(x)
    mean_log_x = np.mean(np.log(x))
    se_k = sigma / np.sqrt(np.sum((np.log(x) - mean_log_x) ** 2))
    t = stats.t.ppf(0.975, df=n - 2)
    ci = t * se_k
    return sigma, ci
