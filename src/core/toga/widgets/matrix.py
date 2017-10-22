from .base import Widget


class Matrix(Widget):
    """Defines the transformation from user-space to device-space coordinates

    Args:

        xx (float): xx component of the affine transformation
        yx (float): yx component of the affine transformation
        xy (float): xy component of the affine transformation
        yy (float): yy component of the affine transformation
        x0 (float): X translation component of the affine transformation
        y0 (float): Y translation component of the affine transformation

    """

    def __init__(self, id=None, style=None, xx=1.0, yx=0.0, xy=0.0, yy=1.0, x0=0.0, y0=0.0, factory=None):
        super().__init__(id=id, style=style, factory=factory)

        # Create a platform specific implementation of Matrix
        self._impl = self.factory.Matrix(interface=self)

    def transform_point(self, x, y):
        """Transforms the point (x, y) by Matrix

        Args:
            x (float): X position
            y (float): Y position

        Returns:
            tuple: the transformed point (x, y)

        """
        return self._impl.transform_point(x, y)

