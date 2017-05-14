from base.base_tool import BaseTool
import base.results
from base.method_decorators import input_tableview, input_output_table
from base.method_decorators import input_tableview, input_output_table_with_output_affixes, parameter, transform_methods, raster_formats
tool_settings = {"label": "Search",
                 "description": "Search for metadata",
                 "can_run_background": "True",
                 "category": "Metadata TODO"}


# @geodata
@base.results.result
class SearchMetadataTool(BaseTool):
    def __init__(self):
        BaseTool.__init__(self, tool_settings)
        self.execution_list = [self.iterate]

    @input_tableview("geodata_table", "Table of Geodata", False, ["geodata:geodata:"])
    @input_output_table
    def getParameterInfo(self):
        return BaseTool.getParameterInfo(self)

    def iterate(self):
        self.iterate_function_on_tableview(self.process, "geodata_table", ["geodata"])
        return

    def process(self, data):
        self.log.info(data)
        # TODO
        return



    # geodata = run['item']
    # base = tool.splitext(geodata)[0]
    #
    # tool.info("Analysing {0}".format(geodata))
    #
    # desc = tool.describe(geodata)
    # arc_retrieved = desc.metadataRetrieved
    #
    #
    # xml_file = base + ".xml"
    # xml = None
    # if tool.geodata_exists(xml_file):
    #     with open(xml_file, "r") as xmlfile:
    #         xml = "".join(line.rstrip() for line in xmlfile)
    # else:
    #     xml_file = "{0} does not exist".format(xml_file)
    #
    # tip_file = base + ".tip"
    # tip = None
    # if tool.geodata_exists(tip_file):
    #     lines = [line.rstrip() for line in open(tip_file)]
    #     lines = [l.replace(":", "=", 1) for l in lines]
    #     # lines = ["title={0}".format(l) for l in lines if not ":"]
    #     lined = {}
    #     for line in lines:
    #         if ":" not in line:
    #             line = "title={0}".format(line)
    #         p = line.split("=")
    #         if len(p) == 1:
    #             p.insert(0, "title=")
    #         elif len(p) > 2:
    #             s = ""
    #             for i in range(1, len(p)):
    #                 s += p[i]
    #             p[1] = s
    #         lined[p[0]] = p[1]
    #     tip = str(lined)
    #     # with open(tip_file, "r") as tipfile:
    #     #     tip = "||".join(line.rstrip() for line in tipfile)
    #         # tiplines = tip.split("||")
    #         # title = tiplines[0]
    #         # tool.info(title)
    #         # tool.info(tiplines[1:])
    #         # tool.info([t.split(":") for t in tiplines[1:]])
    #         # try:
    #         #     tips = {k: v for k, v in [t.split(":") for t in tiplines[1:]]}
    #         # except:
    #         #     tips = "Error parsing tip file"
    #
    # else:
    #     tip_file = "{0} does not exist".format(tip_file)
    #
    #
    # return {"item": geodata, "metadata": "to do",
    #         "arc_retrieved": arc_retrieved, "xml_file": xml_file,
    #          "xml": xml, "tip_file": tip_file, "tip": tip}


