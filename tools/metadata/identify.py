from base.base_tool import BaseTool
from base.results import result
from base import utils
from base.method_decorators import input_tableview, input_output_table
from base import log
import arcpy
import os
from collections import OrderedDict
import arcpy_metadata as md


tool_settings = {"label": "Identify",
                 "description": "Identify available dataset metadata",
                 "can_run_background": "True",
                 "category": "Metadata"}


@result
class IdentifyMetadataTool(BaseTool):
    def __init__(self):
        BaseTool.__init__(self, tool_settings)
        self.execution_list = [self.iterate]

    @input_tableview("geodata_table", "Table of Geodata", False, ["geodata:geodata:"])
    @input_output_table
    def getParameterInfo(self):

        return BaseTool.getParameterInfo(self)

    def iterate(self):

        self.iterate_function_on_tableview(self.search, "geodata_table", ["geodata"])

        return

    @log.log
    def search(self, data):

        geodata = data["geodata"]

        utils.validate_geodata(geodata)

        # gd_path,  gd_base, gd_name, gd_ext = utils.split_up_filename(geodata)

        self.log.info("Searching {0}".format(geodata))

        desc = arcpy.Describe(geodata)
        metadata_retrieved = desc.metadataRetrieved
        self.log.info("metadataRetrieved: {}".format(metadata_retrieved))

        self.log.info(md.MetadataEditor)
        metadata = md.MetadataEditor(dataset=geodata)  # currently supports Shapefiles, FeatureClasses, RasterDatasets and Layers
        self.log.info(metadata.__dict__)
        metadata.finish()

        # xml_file = os.path.join(gd_path, gd_base + ".xml")
        # xml = None
        # if os.path.exists(xml_file):
        #     with open(xml_file, "r") as xmlfile:
        #         xml = "".join(line.rstrip() for line in xmlfile)
        # else:
        #     xml_file = "{0} does not exist".format(xml_file)
        #
        # html_file = os.path.join(gd_path, gd_base + ".html")
        # html = None
        # if os.path.exists(html_file):
        #     with open(html_file, "r") as htmlfile:
        #         html = "".join(line.rstrip() for line in htmlfile)
        # else:
        #     html_file = "{0} does not exist".format(html_file)

        # pdf_file = os.path.join(gd_path, gd_name + ".pdf")
        # pdf = None
        # if os.path.exists(pdf_file):
        #     pass  # not now
        # else:
        #     pdf_file = "{0} does not exist".format(html_file)

        # tip_file = os.path.join(gd_path, gd_name + ".tip")
        # tip = None
        # if os.path.exists(tip_file):
        #     # lines = [line.rstrip() for line in open(tip_file)]
        #     # lines = [l.replace(":", "=", 1) for l in lines]
        #     # # lines = ["title={0}".format(l) for l in lines if not ":"]
        #     # lined = {}
        #     # for line in lines:
        #     #     if ":" not in line:
        #     #         line = "title={0}".format(line)
        #     #     p = line.split("=")
        #     #     if len(p) == 1:
        #     #         p.insert(0, "title=")
        #     #     elif len(p) > 2:
        #     #         s = ""
        #     #         for i in range(1, len(p)):
        #     #             s += p[i]
        #     #         p[1] = s
        #     #     lined[p[0]] = p[1]
        #     # tip = str(lined)
        #     with open(tip_file, "r") as tipfile:
        #         tips = [line.rstrip() for line in tipfile]
        #     if tips:
        #         tips = [t for t in tips if t]
        #         tipd = OrderedDict()
        #         tipd["title"] = tips[0]
        #         for t in tips[1:]:
        #             a, b = t.split(":", 1)
        #             tipd[a] = b
        #         tip = "{0}".format(tipd)
        # else:
        #     tip_file = None
            # with open(tip_file, "r") as tipfile:
            #     tip = "||".join(line.rstrip() for line in tipfile)
                # tiplines = tip.split("||")
                # title = tiplines[0]
                # tool.info(title)
                # tool.info(tiplines[1:])
                # tool.info([t.split(":") for t in tiplines[1:]])
                # try:
                #     tips = {k: v for k, v in [t.split(":") for t in tiplines[1:]]}
                # except:
                #     tips = "Error parsing tip file"

        #     else:
        #         tip_file = "{0} does not exist".format(tip_file)
        #
        # self.result.add({"geodata": geodata, "metadataRetrieved": metadataRetrieved,
        #                  "tip_file": tip_file, "tip": tip, "xml_file": xml_file, "xml": xml,
        #                  "html_file": html_file, "html": html})  #, "pdf_file": pdf_file})

        return


"""
This script looks through the specified geodatabase and reports the
names of all data elements, their schema owners and their feature
dataset (if applicable). Certain metadata elements such as abstract,
purpose and search keys are also reported.

The output is a CSV file that can be read by Excel, ArcGIS, etc.

Only geodatabases are supported, not folder workspaces.

Note: If run from outside of ArcToolbox, you will need to add
the metadata tool assemblies to the Global Assembly Cache.
See: http://forums.arcgis.com/threads/74468-Python-Errors-in-IDLE-when-processing-metadata

Parameters:
    0 - Input workspace (file geodatabase, personal geodatabase,
            or SDE connection file)
    1 - Output CSV file

Date updated: 2/11/2013
"""

# if __name__ == '__main__':
#     workspace = arcpy.GetParameterAsText(0)
#     csvFile = arcpy.GetParameterAsText(1)
#     headerRow = CreateHeaderRow()
#     print headerRow
#     datasetRows = ListWorkspaceContentsAndMetadata(workspace)
#     WriteCSVFile(csvFile, datasetRows, headerRow)


