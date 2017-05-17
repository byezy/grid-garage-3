from base.base_tool import BaseTool
from base import results
from base import utils
from base.method_decorators import input_tableview, input_output_table, parameter
import arcpy
from os.path import join, exists
import arcpy_metadata as md

tool_settings = {"label": "Export XML",
                 "description": "Exports XML...",
                 "can_run_background": "True",
                 "category": "Metadata"}


install_dir = arcpy.GetInstallInfo("desktop")["InstallDir"]
default_translator = join(install_dir, "Metadata", "Translator", "ARCGIS2ISO19139.xml")  # ESRI_ISO2ISO19139.xml")
default_stylesheet = join(install_dir, "Metadata", "Stylesheets", "ArcGIS.xsl")  # ESRI_ISO2ISO19139.xml")


@results.result
class ExportXmlMetadataTool(BaseTool):

    def __init__(self):

        BaseTool.__init__(self, tool_settings)
        self.execution_list = [self.iterate]

    @input_tableview("geodata_table", "Table of Geodata", False, ["geodata:geodata:"])
    @parameter("xml_folder", "XML Folder", "DEFolder", "Required", False, "Input", None, None, None, None)
    @parameter("translator", "Translator", "DEFile", "Required", False, "Input", None, None, None, default_translator, None)
    @parameter("stylesheet", "Style Sheet", "DEFile", "Required", False, "Input", None, None, None, default_stylesheet, None)
    @input_output_table
    def getParameterInfo(self):

        return BaseTool.getParameterInfo(self)

    def iterate(self):

        if not exists(self.translator):
            raise ValueError("Translator '{}' does not exist".format(self.translator))

        if not exists(self.stylesheet):
            raise ValueError("Stylesheet '{}' does not exist".format(self.stylesheet))

        self.iterate_function_on_tableview(self.export, "geodata_table", ["geodata"], return_to_results=True)

        return

    def export(self, data):

        geodata = data["geodata"]

        self.log.info("Creating XML/HTML files for {}".format(geodata))

        fpath, fname, fbase, fext = utils.split_up_filename(geodata)

        xml_file = utils.join_up_filename(self.xml_folder, fname, ".xml")

        # metadata = md.MetadataEditor(geodata)  # currently supports Shapefiles, FeatureClasses, RasterDatasets and Layers
        # self.log.info(metadata.__dict__)
        # metadata.finish()
        try:
            arcpy.ExportMetadata_conversion(geodata, self.translator, xml_file)
            self.log.info("XML file '{}' created".format(xml_file))
        except Exception as e:
            xml_file = "Error creating '{}': {}".format(xml_file, e)

        html_file = utils.join_up_filename(self.xml_folder, fbase, ".html")

        try:
            arcpy.XSLTransform_conversion(geodata, self.stylesheet, html_file, "")
            self.log.info("HTML file '{}' created".format(html_file))
        except:
            html_file = "Error creating '{}': {}".format(html_file, e)

        return {"geodata": geodata, "xml_file": xml_file, "html_file": html_file}


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

