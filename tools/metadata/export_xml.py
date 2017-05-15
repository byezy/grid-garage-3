from base.base_tool import BaseTool
from base import results
from base import utils
from base.method_decorators import input_tableview, input_output_table, parameter
import arcpy
import os

tool_settings = {"label": "Export XML",
                 "description": "Exports XML...",
                 "can_run_background": "True",
                 "category": "Metadata"}


def get_install_dir():

    return arcpy.GetInstallInfo("desktop")["InstallDir"]


def get_default_translator():

    return os.path.join(get_install_dir(), "Metadata/Translator/ARCGIS2ISO19139.xml")  # ESRI_ISO2ISO19139.xml")


def get_default_stylesheet():

    return os.path.join(get_install_dir(), "Metadata/Stylesheets/ArcGIS.xsl")  # ESRI_ISO2ISO19139.xml")


@results.result
class ExportXmlMetadataTool(BaseTool):

    def __init__(self):

        BaseTool.__init__(self, tool_settings)
        self.execution_list = [self.iterate]

    @input_tableview("geodata_table", "Table of Geodata", False, ["geodata:geodata:"])
    @parameter("xml_folder", "XML Folder", "DEFolder", "Required", False, "Input", None, None, None, None)
    @parameter("translator", "Translator", "DEFile", "Required", False, "Input", None, None, None, get_default_translator(), None)
    @parameter("stylesheet", "Style Sheet", "DEFile", "Required", False, "Input", None, None, None, get_default_stylesheet(), None)
    @input_output_table
    def getParameterInfo(self):

        return BaseTool.getParameterInfo(self)

    def iterate(self):

        self.iterate_function_on_parameter(self.export, "geodata_table", ["geodata"])

        return

    def export(self, data):

        geodata = data["geodata"]
        self.log.info("Creating XML/HTML files for {}".format(geodata))

        fpath, fname, fbase, fext = utils.split_up_filename.split_up(geodata)

        xml_file = utils.join_up_filename(fpath, fbase, ".xml")
        arcpy.ExportMetadata_conversion(geodata, self.translator, xml_file)
        self.log.info("XML file '{}' created".format(xml_file))

        html_file = utils.join_up_filename(self.xml_folder, fbase, ".html")
        arcpy.XSLTransform_conversion(geodata, self.stylesheet, html_file, "#")
        self.log.info("HTML file '{}' created".format(html_file))

        return {"item": geodata, "xml_file": xml_file, "html_file": html_file}


# import arcpy
# from arcpy import env
# env.workspace = "C:/data"
# # set local variables
# dir = arcpy.GetInstallInfo("desktop")["InstallDir"]
# translator = dir + "Metadata/Translator/ESRI_ISO2ISO19139.xml"
# arcpy.ExportMetadata_conversion("data.gdb/roads", translator,
#                                 "roads_19139.xml")

# import arcpy
# from arcpy import env
# env.workspace = "C:/data"
# #set local variables
# dir = arcpy.GetInstallInfo("desktop")["InstallDir"]
# xslt = dir + "Metadata/Stylesheets/ArcGIS.xsl"
# arcpy.XSLTransform_conversion("vegetation", xslt, "vegetation.html", "#")

