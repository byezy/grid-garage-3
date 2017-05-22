from test_geodata_tools import TestGeodataToolsTool


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the .pyt file)."""
        self.label = "Grid Garage Test Tools"
        self.alias = "GridGarageTestToolbox"
        self.tools = [TestGeodataToolsTool]

