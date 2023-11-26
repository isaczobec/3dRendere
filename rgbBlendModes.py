"""Class with functions for operations on rgb values."""

def Multiply(rgb1:tuple[float,float,float],rgb2:tuple[float,float,float]):
    """Multiplies every rgb channel of two colors with each other."""
    return (
        rgb1[0]*rgb2[0]/255,
        rgb1[1]*rgb2[1]/255,
        rgb1[2]*rgb2[2]/255,
        )

def ScalarMultiply(rgb1:tuple[float,float,float],scalar:float):
    """Multiplies every rgb channel of a color with a scalar."""
    return (
        rgb1[0]*scalar,
        rgb1[1]*scalar,
        rgb1[2]*scalar,
        )