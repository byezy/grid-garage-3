from base.base_tool import BaseTool
from base import results
from base.method_decorators import input_output_table, parameter
from base.utils import datatype_list, walk, validate_geodata
import arcpy
from os.path import join


tool_settings = {"label": "Search",
                 "description": "Search for identifiable geodata",
                 "can_run_background": "True",
                 "category": "Geodata"}


@results.result
class SearchGeodataTool(BaseTool):

    def __init__(self):

        BaseTool.__init__(self, tool_settings)
        self.execution_list = [self.iterate]

        return

    @parameter("workspaces", "Workspaces to Search", "DEWorkspace", "Required", True, "Input", None, None, None, None)
    @parameter("geodata_types", "Data Types", "GPString", "Required", True, "Input", datatype_list, None, None, None)
    @input_output_table
    def getParameterInfo(self):

        return BaseTool.getParameterInfo(self)

    def iterate(self):

        gt = self.geodata_types.split(";")
        gt = ["Any"] if "Any" in gt else gt
        self.geodata_types = gt

        self.iterate_function_on_parameter(self.search, "workspaces", ["workspace"])

        return

    def search(self, data):

        workspace = data["workspace"].strip("'")

        if not arcpy.Exists(workspace):
            raise ValueError("Workspace '{}' does not exist".format(workspace))

        self.log.info("Searching for {} geodata types in {}".format(self.geodata_types, workspace))

        for root, dirs, files in arcpy.da.Walk(workspace, datatype=self.geodata_types, type=None, followlinks=True):
            for f in files:
                self.log.info(self.result.add({"geodata": join(root, f)}))

        #         x.append(os.path.join(root, f))
        # return x
        # found = [{"geodata": v} for v in walk(workspace, data_types=dt)]
        # if not found:
        #     self.log.info("Nothing found")
        # else:
        #     self.log.info(self.result.add(found))

        return
