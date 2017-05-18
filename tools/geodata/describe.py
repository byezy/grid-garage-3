from base.base_tool import BaseTool
from base.results import result
from base import utils
from base.method_decorators import input_output_table, input_tableview

tool_settings = {"label": "Describe",
                 "description": "Describes geodata",
                 "can_run_background": "True",
                 "category": "Geodata"}


@result
class DescribeGeodataTool(BaseTool):

    def __init__(self):

        BaseTool.__init__(self, tool_settings)
        self.execution_list = [self.iterate]

        return

    @input_tableview("geodata_table", "Table for Geodata", False, ["geodata:geodata:none"])
    @input_output_table
    def getParameterInfo(self):

        return BaseTool.getParameterInfo(self)

    def iterate(self):

        self.iterate_function_on_tableview(self.describe, "geodata_table", ["geodata"], return_to_results=True)

        return

    def describe(self, data):

        item = data["geodata"]

        self.info("Describing {0}".format(item))

        return utils.describe(item)

