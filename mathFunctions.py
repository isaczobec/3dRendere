import numpy as np

def ProjectVectorOnVector(vector: np.ndarray, projectOnVector: np.ndarray):
    """Projects vector on projectOnVector and returns it."""
    return (np.dot(vector,projectOnVector) / (np.linalg.norm(projectOnVector) ** 2)) * projectOnVector

def PerpetualVectorOnVector(vector: np.ndarray, projectOnVector: np.ndarray):
    """Gets the perpetual component of vector in comparasion to projectOnVector."""

    return vector - ProjectVectorOnVector(vector,projectOnVector)