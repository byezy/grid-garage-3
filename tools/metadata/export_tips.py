from base.base_tool import BaseTool
import base.results
from base.method_decorators import input_tableview, input_output_table

tool_settings = {"label": "Export tips",
                 "description": "Exports tips...",
                 "can_run_background": "True",
                 "category": "Metadata"}


@base.results.result
class ExportTipsMetadataTool(BaseTool):
    def __init__(self):
        BaseTool.__init__(self, tool_settings)

        self.execution_list = [self.iterate]

    @input_tableview("geodata_table", "Table of Geodata", False, ["geodata:geodata:"])
    @input_output_table
    def getParameterInfo(self):

        return BaseTool.getParameterInfo(self)

    def iterate(self):

        self.iterate_function_on_parameter(self.export, "geodata_table", ["geodata"])

        return

    def export(self, data):

        geodata = data["geodata"]

        base.utils.validate_geodata(geodata)

    # geodata = run['item']
    # tool.info("Creating TIP file for {0}".format(geodata))
    #
    # row = run["item_row"]
    # row_fields = run["item_row_fields"]
    # tool.info(row_fields)
    # tip_order = row[row_fields.index("tip_order")]
    # tip_order = tip_order.split(",")
    # tool.info(tip_order)
    # ordered_fields = [f for f in tip_order if f in tip_fields]
    # tip_dic = OrderedDict()
    # for tf in ordered_fields:
    #     tip_dic[tf] = row[row_fields.index(tf)]
    # # tip_dic = {tf: row[row_fields.index(tf)] for tf in ordered_fields}
    #
    # fpath, fname, fbase, fext = tool.split_up(geodata)
    #
    # tip_file = tool.join_up(tip_folder, fbase, ".tip")
    # tool.info(tip_file)
    # with open(tip_file, "w") as tipfile:
    #     for k, v in tip_dic.iteritems():
    #         tipfile.write("{0}: {1}\n".format(k, v))
    #
    # return {"item": geodata, "metadata": "to do", "tip_file": tip_file}

