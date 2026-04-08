from math import cos, pi, sin, tan


# try to avoid a NumPy dependency in an example
class Matrix:
    data: list[list[int]]
    shape: tuple[int, int]
    strides: tuple[int, int]

    def __init__(self, data=None, shape=None, strides=None):
        if shape is None:
            rows = len(data)
            cols = max(len(row) for row in data)
            shape = (rows, cols)
        self.shape = tuple(shape)
        if strides is None:
            strides = (shape[1], 1)
        self.strides = tuple(strides)
        self.data = [0.0] * (
            (shape[0] - 1) * strides[0] + (shape[1] - 1) * strides[1] + 1
        )
        if data is not None:
            for i, row in enumerate(data):
                if i >= shape[0]:
                    break
                for j, value in enumerate(row):
                    if j >= shape[1]:
                        break
                    self[i, j] = value

    def __getitem__(self, index):
        return self.data[index[0] * self.strides[0] + index[1] * self.strides[1]]

    def __setitem__(self, index, value):
        self.data[index[0] * self.strides[0] + index[1] * self.strides[1]] = value

    def __mul__(self, other):
        if isinstance(other, (int, float, complex)):
            result = Matrix(shape=self.shape)
            result.data = [other * value for value in self.data]
        else:
            return NotImplemented

    def __rmul__(self, other):
        if isinstance(other, (int, float, complex)):
            result = Matrix(shape=self.shape)
            result.data = [other * value for value in self.data]
        else:
            return NotImplemented

    def __matmul__(self, other):
        if isinstance(other, Matrix) and self.shape[1] == other.shape[0]:
            result = Matrix(shape=(self.shape[0], other.shape[1]))
            for i in range(self.shape[0]):
                for j in range(other.shape[1]):
                    result[i, j] = sum(
                        self[i, k] * other[k, j] for k in range(self.shape[1])
                    )
            return result
        elif isinstance(other, (int, float, complex)):
            return self * other
        else:
            return NotImplemented

    def __rmatmul__(self, other):
        if isinstance(other, (int, float, complex)):
            return self * other
        else:
            return NotImplemented

    def __iter__(self):
        yield from self.data

    def __str__(self):
        return "\n".join(
            ", ".join(f"{self[i, j]:5.2f}" for j in range(self.shape[1]))
            for i in range(self.shape[0])
        )

    def transpose(self):
        result = Matrix(shape=self.shape[::-1], strides=self.strides[::-1])
        result.data = self.data.copy()
        return result

    @classmethod
    def identity(cls, n):
        result = cls(shape=(n, n))
        for i in range(n):
            result[i, i] = 1.0
        return result

    @classmethod
    def translation(cls, *v):
        n = len(v)
        result = cls.identity(n + 1)
        for i in range(n):
            result[n, i] = v[i]
        return result

    @classmethod
    def skewing(cls, *v):
        n = len(v)
        result = cls.identity(n + 1)
        for i in range(n):
            result[i, n] = v[i]
        return result

    @classmethod
    def scaling(cls, *v):
        n = len(v)
        result = cls.identity(n + 1)
        for i in range(n):
            result[i, i] = v[i]
        return result

    @classmethod
    def rotation(cls, angle, d0=0, d1=1, n=4):
        c = cos(angle)
        s = sin(angle)
        result = cls.identity(n)
        result[d0, d0] = c
        result[d0, d1] = s
        result[d1, d0] = -s
        result[d1, d1] = c
        return result

    @classmethod
    def rotation_x(cls, angle):
        return cls.rotation(angle, 1, 2)

    @classmethod
    def rotation_y(cls, angle):
        return cls.rotation(angle, 0, 2)

    @classmethod
    def rotation_z(cls, angle):
        return cls.rotation(angle, 0, 1)

    @classmethod
    def perspective(self, fov, aspect, near_clip, far_clip):
        f = tan((pi - fov) / 2)
        scale = 1 / (near_clip - far_clip)
        return Matrix(
            [
                [f / aspect, 0.0, 0.0],
                [0.0, f, 0.0, 0.0],
                [0.0, 0.0, (near_clip + far_clip) * scale, -1.0],
                [0.0, 0.0, near_clip * far_clip * scale / 2, 0.0],
            ],
            shape=(4, 4),
        )

    @classmethod
    def projection(self, width, height, depth):
        return Matrix(
            [
                [2 / width, 0.0, 0.0],
                [0.0, 2 / height, 0.0, 0.0],
                [0.0, 0.0, 1 / depth, 0.0],
                [0.0, 0.0, 0.0, 1.0],
            ],
            shape=(4, 4),
        )
