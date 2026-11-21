import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
from model import Host, UniFlow, Network

class TestUniFlow:
    # test data formatted in 
    # (source ip, source port, source ether, dest ip, dest port, first packet id, protocol)
    example_data = (('10.10.32.1', 80, '02:00:00:00:00:01', '10.10.32.128', 33333, 11, 1),
    ('10.10.32.128', 33333, '02:00:00:00:00:FE', '10.10.32.1', 80, 10, 1),
    ('10.10.32.1', 80, '02:00:00:00:00:01', '10.10.32.129', 44444, 21, 1),
    ('10.10.32.129', 44444, '02:00:00:00:00:FE', '10.10.32.1', 80, 20, 1))

    # initiate 4 test flows
    def get_example(self, idx: int = None):
        # all if nothing specified or out of index
        if idx is None or (0 > idx  and len(self.example_data) <= idx):
            return (UniFlow(*data) for data in self.example_data)
        else:
            return UniFlow(*self.example_data[idx])

    def test_defaults(self):
        example = self.get_example(0)
        assert example.packets_n == 1

    def test_hash_compare(self):
        # hashing
        example_1 = self.get_example(0)
        example_2 = self.get_example(0)
        assert hash(example_1) == hash(example_2)
        # eq
        assert example_1 == example_2


class TestNetwork:
    def __init__(self):
        self.network: Network = Network()
        for edge in TestUniFlow().get_example():
            self.network.add_edge(edge)

    def test_enum_hosts(self):
        self.network.enumerate_hosts()
        assert len(self.network.hosts) == 3


if __name__ == "__main__":
    TestUniFlow().test_defaults()
    TestUniFlow().test_hash_compare()
    TestNetwork().test_enum_hosts()