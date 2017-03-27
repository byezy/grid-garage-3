import base.base_tool
import base.results
from base.method_decorators import input_output_table, input_tableview

tool_settings = {"label": "Extract Parent Datasource",
                 "description": "Extracts the parent datasource from geodata...",
                 "can_run_background": "True",
                 "category": "Geodata"}


@base.results.result
class ExtractParentGeodataTool(base.base_tool.BaseTool):

    def __init__(self):

        base.base_tool.BaseTool.__init__(self, tool_settings)
        self.execution_list = [self.iterate]

        return

    @input_tableview("geodata_table", "Table for Geodata", False, ["geodata:geodata:"])
    @input_output_table
    def getParameterInfo(self):

        return base.base_tool.BaseTool.getParameterInfo(self)

    def iterate(self):

        self.iterate_function_on_tableview(self.process, "geodata_table", ["geodata"])

        return

    def process(self, data):

        self.send_info(data)
        # self.add_result("TODO")

        return

