from base.base_tool import BaseTool
from base import results
from base import utils
from base.method_decorators import input_tableview, input_output_table
import arcpy
import os
from collections import OrderedDict


tool_settings = {"label": "Search for Metadata",
                 "description": "Search for identifiable metadata",
                 "can_run_background": "True",
                 "category": "Metadata"}


@results.result
class SearchMetadataTool(BaseTool):
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

    def search(self, data):

        geodata = data["geodata"]

        utils.validate_geodata(geodata)

        gd_path,  basename, gd_name, gd_ext = utils.split_up_filename(geodata)[0]

        self.log.info("Searching {0}".format(geodata))

        desc = arcpy.Describe(geodata)
        arc_retrieved = desc.metadataRetrieved

        xml_file = os.path.join(gd_path, basename + ".xml")
        xml = None
        if os.path.exists(xml_file):
            with open(xml_file, "r") as xmlfile:
                xml = "".join(line.rstrip() for line in xmlfile)
        else:
            xml_file = "{0} does not exist".format(xml_file)

        html_file = os.path.join(gd_path, basename + ".html")
        html = None
        if os.path.exists(html_file):
            with open(html_file, "r") as htmlfile:
                html = "".join(line.rstrip() for line in htmlfile)
        else:
            html_file = "{0} does not exist".format(html_file)

        pdf_file = os.path.join(gd_path, basename + ".pdf")
        pdf = None
        if os.path.exists(pdf_file):
            pass  # not now
        else:
            pdf_file = "{0} does not exist".format(html_file)

        tip_file = os.path.join(gd_path, basename + ".tip")
        tip = None
        if os.path.exists(tip_file):
            # lines = [line.rstrip() for line in open(tip_file)]
            # lines = [l.replace(":", "=", 1) for l in lines]
            # # lines = ["title={0}".format(l) for l in lines if not ":"]
            # lined = {}
            # for line in lines:
            #     if ":" not in line:
            #         line = "title={0}".format(line)
            #     p = line.split("=")
            #     if len(p) == 1:
            #         p.insert(0, "title=")
            #     elif len(p) > 2:
            #         s = ""
            #         for i in range(1, len(p)):
            #             s += p[i]
            #         p[1] = s
            #     lined[p[0]] = p[1]
            # tip = str(lined)
            with open(tip_file, "r") as tipfile:
                tips = [line.rstrip() for line in tipfile]
            if tips:
                tips = [t for t in tips if t]
                tipd = OrderedDict()
                tipd["title"] = tips[0]
                for t in tips[1:]:
                    a, b = t.split(":", 1)
                    tipd[a] = b
                tip = "{0}".format(tipd)
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

            else:
                tip_file = "{0} does not exist".format(tip_file)

        self.result.add({"geodata": geodata, "arc_retrieved": arc_retrieved,
                         "tip_file": tip_file, "tip": tip, "xml_file": xml_file, "xml": xml,
                         "html_file": html_file, "html": html, "pdf_file": pdf_file})

        return


