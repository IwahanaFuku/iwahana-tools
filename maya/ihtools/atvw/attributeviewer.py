from maya import cmds

class SearchAttribute():
    def search_attr_name(self, **kwargs):
        destination_node = kwargs["destination_node"]
        source_node = kwargs["source_node"]

        print(destination_node)
        print(source_node)

        destination_node_attrs = cmds.listAttr(destination_node)
        lis_attached_node = [source_node]

        attr_list = []
        for material_attr in destination_node_attrs:
            try:
                connected_attr = cmds.listConnections("{}.{}".format(destination_node, material_attr), d = True)
            except ValueError:
                pass
            if lis_attached_node == connected_attr:
                attr_list.append(material_attr)

        return attr_list
    
    