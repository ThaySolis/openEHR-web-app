from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager

# source: <https://stackoverflow.com/a/22794281/6242158>

# Never check any hostnames
class HostNameIgnoringAdapter(HTTPAdapter):
    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(
            num_pools = connections,
            maxsize = maxsize,
            block = block,
            assert_hostname = False
        )
