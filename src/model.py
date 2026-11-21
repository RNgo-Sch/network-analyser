"""
This file contains classes designed to model an IoT network
The models are designed to document hosts and the edges between them used for communication
"""

# class defintitions
class UniFlow:
    """
    This class documents the edges between hosts.
    For MVP1, it represents the unidirectional flow from one host (a source) to another host (a destination)
    """
    def __init__(self, source_ip, source_port, source_ether, dest_ip, dest_port,
                 first_pkt_id=None, protocol=None):
        # connection identifiers
        self.source_ip = source_ip
        self.source_port = source_port
        self.source_ether = source_ether
        self.dest_ip = dest_ip
        self.dest_port = dest_port
        
        # packet information
        self.first_pkt_id = first_pkt_id
        self.packets_n = 0

        # other information
        self.protocol = protocol

    def add_packet(self):
        self.packets_n += 1

    def key(self):
        # key contains routing information and protocol under assumption that this identifies a given convo
        # does not contain first packet id, as it does not make sense to match
        return (self.source_ip, self.source_port, self.source_ether,
                self.dest_ip, self.dest_port, self.protocol)

    def __hash__(self):
        return hash(self.key())

    def __eq__(self, other):
        # check if the flow is from the same conversation according to key
        if isinstance(other, UniFlow):
            return self.key() == other.key()
        return NotImplemented


class Host:
    """Summary of an individual host."""
    def __init__(self, ip):
        self.ip = ip
        self.outbound_flows = set()

    def add_edge(self, flow: UniFlow):
        self.outbound_flows.add(flow)

    def get_ether_addr(self):
        """Get all source ethernet addresses from outbound flows"""
        return set(flow.source_ether for flow in self.outbound_flows)

    def get_ports(self):
        """Get all source ports from outbound flows"""
        return set(flow.source_port for flow in self.outbound_flows)
        
    def key(self):
        return (self.ip, self.ether)

    def __hash__(self):
        return hash(self.ip)

    def __eq__(self, other):
        if isinstance(other, Host):
            return self.ip == other.ip
        elif isinstance(other, str):
            return self.ip == other
        else:
            return NotImplemented


class Network:
    """
    This class documents the overall network, focusing on storing information in terms of edges
    From stored edges, is can derive profiles of each individual host
    """
    def __init__(self):
        # create empty sets
        self.edges: list[UniFlow] = []
        self.hosts: list[Host] = []

    def add_edge(self, flow: UniFlow):
        if flow not in self.edges:
            self.edges.append(flow)
        flow.add_packet()

    def enumerate_hosts(self):
        """This function creates a list of hosts, based on source IDs compiled among all edges"""
        for edge in self.edges:
            if edge.source_ip not in self.hosts:
                self.hosts.append(Host(edge.source_ip))
                self.hosts[-1].add_edge(edge)
            else: 
                for host in self.hosts:
                    if edge.source_ip == host.ip:
                        host.add_edge(edge)
                        break
    