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

    def count_packet(self):
        self.packets_n += 1

    def key(self):
        return (self.source_ip, self.source_port, self.source_ether,
                self.dest_ip, self.dest_port, self.protocol)


"""
This class exists as a method to summarise individual host information.
"""
class Host:
    """Summary of an individual host."""
    def __init__(self, ip):
        self.ip = ip
        self.ether = set()
        self.outbound_flows = set()

    def add_edge(self, flow: UniFlow):
        self.outbound_flows.add(flow)

    def enumerate_ether_addr(self):
        """Collect source ethernet addresses from outbound flows into self.ether."""
        for flow in self.outbound_flows:
            self.ether.add(flow.source_ether)

