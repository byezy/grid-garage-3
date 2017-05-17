from base.base_tool import BaseTool
from base import results
from base.method_decorators import input_output_table, input_tableview
from arcpy import Rename_management

tool_settings = {"label": "Rename",
                 "description": "Renames datasets to a new name specified in the 'new name' field...",
                 "can_run_background": "True",
                 "category": "Geodata"}


@results.result
class RenameGeodataTool(BaseTool):

    def __init__(self):
        BaseTool.__init__(self, tool_settings)
        self.execution_list = [self.iterate]

        return

    @input_tableview("geodata_table", "Table for Geodata", False, ["new name:candidate_name:", "geodata:geodata:"])
    @input_output_table
    def getParameterInfo(self):

        return BaseTool.getParameterInfo(self)

    def iterate(self):

        self.iterate_function_on_tableview(self.rename, "geodata_table", ["geodata", "new name"], return_to_results=True)

        return

    def rename(self, data):

        geodata = data["geodata"]
        new_geodata = data["new name"]

        self.log.info('Renaming {0} --> {1}'.format(geodata, new_geodata))
        Rename_management(geodata, new_geodata)

        return {'geodata': new_geodata, 'previous_name': geodata}

