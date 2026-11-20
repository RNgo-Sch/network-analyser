"""
This file contains classes designed to model an IoT network
The models are designed to document hosts and the edges between them used for communication
"""

# class defintitions
"""
This class documents the edges between hosts.
For MVP1, it represents the unidirectional flow from one host (a source) to another host (a destination)
"""
class UniFlow:
    # source information
    source_ip: str
    source_port: int
    source_ether: str
    # destination information
    dest_ip: str
    dest_port: int
    # protocol for flow
    protocol: int
    # simple packet stats
    packets_n: int = 0
    first_pkt_id: int = None

    def __init__(self, source_ip, source_port, source_ether, dest_ip, dest_port, first_pkt_id = None, protocol = None):
        self.source_ip = source_ip
        self.source_port = source_port
        self.source_ether = source_ether # should be kept for future identification purposes
        self.dest_ip = dest_ip
        self.dest_port = dest_port
    
        self.first_pkt_id = self.first_pkt_id
        self.protocol = protocol

    def count_packet(self):
        self.packets_n += 1
