class GObj(object):
    next_uuid = 1
    def __init__(self, uuid = None, attr = {}):
        if uuid == None:
            uuid = GObj.create_uuid()
        elif uuid >= GObj.next_uuid:
            GObj.next_uuid = uuid + 1
        self.uuid = uuid
        self.attr = attr
        
    def set_attr(self, k, v):
        self.attr[k] = v
    
    def get_attr(self, k):
        return self.attr[k]

    @classmethod
    def create_uuid(cls):
        cur_uuid = cls.next_uuid
        cls.next_uuid += 1
        return cur_uuid

    def __str__(self):
        return 'Obj ' + str(self.uuid)

class GNode(GObj):
    def __init__(self, graph, uuid = None, attr = {}):
        super().__init__(uuid, attr)
        self.graph = graph
        self.in_edges = {}
        self.out_edges = {}
        
    def add_in_edge(self, edge):
        self.in_edges[edge.uuid] = edge
    
    def add_out_edge(self, edge):
        self.out_edges[edge.uuid] = edge
        
    def forward(self, edge_uuid):
        edge = self.out_edges[edge_uuid]
        return edge.target()
        
    def backward(self, edge_uuid):
        edge = self.in_edges[edge_uuid]
        return edge.source()
        
    def __str__(self):
        return 'Node ' + str(self.uuid)

class GEdge(GObj):
    def __init__(self, graph, source, target, uuid = None, attr = {}):
        super().__init__(uuid, attr)
        self.graph = graph
        self.source = source
        self.target = target
        
    def source(self):
        return self.source
    
    def target(self):
        return self.target
    
    def __str__(self):
        return 'Edge ' + str(self.uuid) + ': ' + self.source.__str__() + ' -> ' + self.target.__str__()
        

class Graph(GObj):
    def __init__(self, uuid = None, attr = {}):
        super().__init__(uuid, attr)
        self.node_dict = {}
        self.edge_dict = {}
        
    def __str__(self):
        s = 'Graph ' + str(self.uuid) + ':\n'
        
        s += 'Nodes: ['
        for k,v in self.node_dict.items():
            s += v.__str__() + ', '
        s += ']\n'
        
        s += 'Edges: ['
        for k,v in self.edge_dict.items():
            s += v.__str__() + ', '
        s += ']'
        
        return s
        
    def create_node(self, uuid = None, attr = {}):
        node = GNode(self, uuid, attr)
        self.node_dict[node.uuid] = node
        return node
    
    def create_edge(self, uuid_s, uuid_t, uuid = None, attr={}):
        node_s = self.node_dict[uuid_s]
        node_t = self.node_dict[uuid_t]
        edge = GEdge(self, node_s, node_t, uuid, attr)
        node_s.add_out_edge(edge)
        node_t.add_in_edge(edge)
        self.edge_dict[edge.uuid] = edge
        return edge
    
    def get_node(self, uuid):
        return self.node_dict[uuid]
        
    def get_edge(self, uuid):
        return self.edge_dict[uuid]
    
    def nodes(self):
        return self.node_dict
    
    def edges(self):
        return self.edge_dict
