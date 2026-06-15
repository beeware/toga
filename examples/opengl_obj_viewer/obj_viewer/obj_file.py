"""A very basic Wavefront Obj/Mtl file reader

This handles polygon-face geometries, and basic ambient/diffuse/specular
materials, but not texture maps.
"""

from dataclasses import dataclass, field
from pathlib import Path


def bbox(vertices):
    """Get the bounding box of a collection of vertices.

    Assumes vertices are a list of coordinates `[x0, y0, z0, x1, y1, z1, ...]`.
    """
    x0 = min(vertices[::3])
    y0 = min(vertices[1::3])
    z0 = min(vertices[2::3])
    x1 = max(vertices[::3])
    y1 = max(vertices[1::3])
    z1 = max(vertices[2::3])
    return (x0, y0, z0, x1, y1, z1)


@dataclass
class Material:
    """A simple ambient/diffuse/specular material."""

    name: str | None = None
    shininess: float = 0.0
    ambient: tuple[float, float, float] = (0.0, 0.0, 0.0)
    diffuse: tuple[float, float, float] = (1.0, 1.0, 1.0)
    specular: tuple[float, float, float] = (0.0, 0.0, 0.0)
    emissive: tuple[float, float, float] = (0.0, 0.0, 0.0)
    refraction: float = 1.0
    opacity: float = 1.0
    illum: int = 0
    transmission: tuple[float, float, float] = (0.0, 0.0, 0.0)


@dataclass
class Geometry:
    """A triangulated geometry patch.

    Data is stored as flat lists.
    """

    vertices: list[float] = field(default_factory=list)
    textures: list[float] = field(default_factory=list)
    normals: list[float] = field(default_factory=list)
    colors: list[float] = field(default_factory=list)
    name: str | None = None
    material: Material = field(default_factory=Material)


def parse_mtl_file(path: Path):
    """Material file parser

    :params path: The path to the material file.
    :returns: A dictionary mapping material names to Material objects.
    """
    materials = {}
    print(path)

    with open(path) as f:
        for line in f:
            # discard comments
            line, *comments = line.split("#")
            line = line.strip()
            if not line:
                continue
            match line.split(maxsplit=1):
                case ["newmtl", name]:
                    material = Material(name=name)
                    materials[name] = material
                case ["Ns", args]:
                    material.shininess = float(args)
                case ["Ka", args]:
                    material.ambient = tuple(float(arg) for arg in args.split())
                case ["Kd", args]:
                    material.diffuse = tuple(float(arg) for arg in args.split())
                case ["Ks", args]:
                    material.specular = tuple(float(arg) for arg in args.split())
                case ["Tf", args]:
                    material.filter = tuple(float(arg) for arg in args.split())
                case ["d", args]:
                    material.opacity = float(args)
                case ["Tr", args]:
                    material.opacity = 1 - float(args)
                case ["Ni", args]:
                    material.refraction = float(args)
                case [keyword, *rest]:
                    # unhandled
                    print(f"Unhandled keyword: {keyword}", " ".join(rest))

    print(materials.keys())
    return materials


def parse_face_vertex(face_vertex):
    """Parse vertex indices in a face.

    :params face_vertex: A face index representation like '1/2/3' or '-1//3'.
    :returns: A dictionary mapping index names to pythonic 0-based indices.
    """
    parts = {
        coord: int(value)
        for coord, value in zip(
            ["vertex", "texture", "normal"], face_vertex.split("/"), strict=False
        )
        if value
    }
    # normalize indexing
    indices = {
        coord: index - 1 if index > 0 else index for coord, index in parts.items()
    }
    return indices


def parse_obj_file(path: Path):
    """Obj file parser

    This parser assumes .mtl file paths are relative to the directory the .obj file
    is in.

    :params path: The path to the material file.
    :returns: A list of Geometry objects.
    """
    vertices = []
    colors = []
    textures = []
    normals = []
    geometry = Geometry()
    material = Material()
    materials = {}
    geometries = []

    with open(path) as f:
        for line in f:
            # discard comments
            line, *comments = line.split("#")
            line = line.strip()
            if not line:
                # blank line, skip
                continue
            match line.split(maxsplit=1):
                case ["o", *name]:
                    if geometry.vertices:
                        geometries.append(geometry)
                    if name:
                        geometry = Geometry(name=name[0], material=material)
                    else:
                        geometry = Geometry(material=material)
                case ["g", *name]:
                    # group
                    if geometry.vertices:
                        geometries.append(geometry)
                    if name:
                        geometry = Geometry(name=name[0], material=material)
                    else:
                        geometry = Geometry(material=material)
                case ["mtllib", file]:
                    file = file.strip()
                    print(path.parent, file)
                    materials.update(parse_mtl_file(path.parent / file))
                case ["usemtl", name]:
                    material = materials.get(name, Material(name=name))
                    if geometry.vertices:
                        geometries.append(geometry)
                        geometry = Geometry(material=material)
                    else:
                        geometry.material = material
                case ["v", args]:
                    # vertex
                    values = [float(arg) for arg in args.split()]
                    vertices.append(values[:3])
                    if len(values) == 6:
                        colors.append(values[3:])
                    else:
                        colors.append([1.0, 1.0, 1.0])
                case ["vt", args]:
                    # texture coord
                    textures.append([float(arg) for arg in args.split()])
                case ["vn", args]:
                    # normal vector
                    normals.append([float(arg) for arg in args.split()])
                case ["f", args]:
                    # face
                    indices = [parse_face_vertex(arg) for arg in args.split()]
                    # Obj file spec says faces are *convex* flat polygons,
                    # so fan triangulations should work. If it doesn't it's a
                    # bad file.
                    i = indices[0]
                    for j, k in zip(indices[1:-1], indices[2:], strict=True):
                        geometry.vertices.extend(vertices[i["vertex"]])
                        geometry.vertices.extend(vertices[j["vertex"]])
                        geometry.vertices.extend(vertices[k["vertex"]])
                        geometry.colors.extend(colors[i["vertex"]])
                        geometry.colors.extend(colors[j["vertex"]])
                        geometry.colors.extend(colors[k["vertex"]])
                        if textures and "texture" in i:
                            geometry.textures.extend(textures[i["texture"]])
                            geometry.textures.extend(textures[j["texture"]])
                            geometry.textures.extend(textures[k["texture"]])
                        elif len(textures) == len(vertices):
                            geometry.textures.extend(textures[i["vertex"]])
                            geometry.textures.extend(textures[j["vertex"]])
                            geometry.textures.extend(textures[k["vertex"]])
                        if normals and "normal" in i:
                            geometry.normals.extend(normals[i["normal"]])
                            geometry.normals.extend(normals[j["normal"]])
                            geometry.normals.extend(normals[k["normal"]])
                        elif len(normals) == len(vertices):
                            geometry.normals.extend(normals[i["vertex"]])
                            geometry.normals.extend(normals[j["vertex"]])
                            geometry.normals.extend(normals[k["vertex"]])
                case [keyword, *rest]:
                    # unhandled
                    print(f"Unhandled keyword: {keyword}", " ".join(rest))
    if geometry.vertices:
        geometries.append(geometry)
    return geometries
