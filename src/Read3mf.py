import hou
import Lib3MF
import os
import platform


def import_3mf(file, wrapper_file):
    cd = False
    uv = False

    wrapper_object = ".".join(wrapper_file.split(".")[:-1])
    wrapper = Lib3MF.Wrapper(wrapper_object)

    model = wrapper.CreateModel()

    reader = model.QueryReader("3mf")
    reader.SetStrictModeActive(False)
    reader.ReadFromFile(file)

    mesh_iterator = model.GetMeshObjects()
    point_offset = 0
    while mesh_iterator.MoveNext():
        current_resource = mesh_iterator.GetCurrent()
        resource_id = current_resource.GetUniqueResourceID()
        current_mesh = model.GetMeshObjectByID(resource_id)
        vertices = current_mesh.GetVertices()
        for vertex in vertices:
            coords = vertex.Coordinates
            npt = geo.createPoint()
            npt.setPosition(coords)

        triangles = current_mesh.GetTriangleIndices()
        for i, triangle in enumerate(triangles):
            # print(triangle_id)
            # triangle = current_mesh.GetTriangle(triangle_id)
            indices = triangle.Indices
            p1 = geo.point(point_offset + indices[0])
            p2 = geo.point(point_offset + indices[1])
            p3 = geo.point(point_offset + indices[2])

            nprim = geo.createPolygon()

            v1 = nprim.addVertex(p1)
            v2 = nprim.addVertex(p2)
            v3 = nprim.addVertex(p3)

            prop = current_mesh.GetTriangleProperties(i)

            try:
                prop_type = model.GetPropertyTypeByID(prop.ResourceID)
            except Lib3MF.ELib3MFException:
                continue

            if prop_type:
                if prop_type == Lib3MF.PropertyType.Colors:
                    # print("Vertex color!")
                    if not cd:
                        geo.addAttrib(hou.attribType.Point, "Cd", [1.0, 1.0, 1.0])
                        cd = True

                    color_list = model.GetColorGroupByID(prop.ResourceID)
                    c1 = color_list.GetColor(prop.PropertyIDs[0])
                    c2 = color_list.GetColor(prop.PropertyIDs[1])
                    c3 = color_list.GetColor(prop.PropertyIDs[2])

                    p1.setAttribValue(
                        "Cd",
                        [
                            int(c1.Red) / 255.0,
                            int(c1.Green) / 255.0,
                            int(c1.Blue) / 255.0,
                        ],
                    )
                    p2.setAttribValue(
                        "Cd",
                        [
                            int(c2.Red) / 255.0,
                            int(c2.Green) / 255.0,
                            int(c2.Blue) / 255.0,
                        ],
                    )
                    p3.setAttribValue(
                        "Cd",
                        [
                            int(c3.Red) / 255.0,
                            int(c3.Green) / 255.0,
                            int(c3.Blue) / 255.0,
                        ],
                    )

                if prop_type == Lib3MF.PropertyType.TexCoord:
                    # print("UVs!")
                    if not uv:
                        geo.addAttrib(hou.attribType.Vertex, "uv", [0.0, 0.0])
                        uv = True

                    uv_list = model.GetTexture2DGroupByID(prop.ResourceID)
                    print(uv_list)
                    uv1 = uv_list.GetTex2Coord(prop.PropertyIDs[0])
                    print(f"{uv1.U},{uv1.V}")
                    uv2 = uv_list.GetTex2Coord(prop.PropertyIDs[1])
                    uv3 = uv_list.GetTex2Coord(prop.PropertyIDs[2])

                    v1.setAttribValue("uv", [uv1.U, uv1.V])
                    v2.setAttribValue("uv", [uv2.U, uv2.V])
                    v3.setAttribValue("uv", [uv3.U, uv3.V])

        point_offset += current_mesh.GetVertexCount()


node = hou.pwd()
digital_asset_node = node.parent()
geo = node.geometry()

file = digital_asset_node.parm("file").eval()
wrapper_location = digital_asset_node.parm("wrapper").eval()

file_exists = wrapper_exists = False

if os.path.isfile(file):
    file_exists = True
elif file != "":
    raise hou.Error("Specified file does not exist")

if os.path.exists(wrapper_location):
    system = platform.system()
    if system == "Linux":
        wrapper_file_name = "lib3mf.so"
    elif system == "Windows":
        wrapper_file_name = "lib3mf.dll"

    wrapper_file = os.path.join(wrapper_location, wrapper_file_name)
    if os.path.isfile(wrapper_file):
        wrapper_exists = True

if file_exists and wrapper_exists:
    import_3mf(file, wrapper_file)
