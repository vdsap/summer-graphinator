import numpy as np


def fit_line(x, y):
    k, b = np.polyfit(x, y, 1)
    y_pred = k * x + b
    return k, b, y_pred


def calculate_stats(x, y, y_pred):
    mse = np.mean((y - y_pred) ** 2)
    std_dev = np.sqrt(mse)
    ci = 1.96 * std_dev / np.sqrt(len(x))
    return std_dev, ci
