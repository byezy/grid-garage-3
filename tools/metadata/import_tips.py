from base.base_tool import BaseTool
import base.results
import base.utils
from base.method_decorators import input_tableview, input_output_table

tool_settings = {"label": "Import Tips",
                 "description": "Create a table of tips from existing tip files",
                 "can_run_background": "True",
                 "category": "Metadata"}


@base.results.result
class ImportTipsMetadataTool(BaseTool):
    def __init__(self):

        BaseTool.__init__(self, tool_settings)
        self.execution_list = [self.iterate]

    @input_tableview("geodata_table", "Table of Geodata", False, ["geodata:geodata:"])
    @input_output_table
    def getParameterInfo(self):

        return BaseTool.getParameterInfo(self)

    def iterate(self):

        self.iterate_function_on_parameter(self.create, "geodata_table", ["geodata"])

        return

    def create(self, data):

        geodata = data["geodata"]

        base.utils.validate_geodata(geodata)

        return


# def parse(run):
#     """
#     Clip raster based on current run parameters.
#
#     #Clip_management (in_raster, rectangle, out_raster, {in_template_dataset},
#     #                                      {nodata_value}, {clipping_geometry})
#     ======== ===================================================================
#     Arg1     run - A dictionary of run-time objects
#     Return   None
#     Raises   None
#     Effect   A new dataset that is a clip of the original
#     ======== ===================================================================
#     """
#     # tool.info(run['item_row'])
#     tip_file = run['item_row'][1]
#     err = None
#
#     if not tool.geodata_exists(tip_file):
#         err = "Tip file '{0}' does not exist".format(tip_file)
#         tool.info(err)
#         return {"item": run["item"], "err": err, "tip_file": tip_file}
#
#     tool.info("Parsing {0}".format(tip_file))
#
#     tips = ODict()
#     tips["header"] = ""
#
#     with open(tip_file, "r") as tipfile:
#         buf = "header"
#         for line in tipfile:
#             s = line.strip().encode("ascii").split(":", 1)
#             if len(s) > 1:
#                 s1, s2 = s
#                 buf = s1
#             else:
#                 s1 = s[0]
#                 s2 = None
#             if not s2:
#                 tips[buf] += s1
#             else:
#                 tips[s1] = s2
#
#     tips["field_order"] = tips.keys()
#
#     res = {"item": run["item"], "metadata": "to do", "tip_file": tip_file}
#     res.update(tips)
#
#     return res
#

