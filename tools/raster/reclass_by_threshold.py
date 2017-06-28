from base.base_tool import BaseTool
from base.results import result
from base import utils
from base.method_decorators import input_tableview, input_output_table_with_output_affixes, parameter, data_nodata, raster_formats
import arcpy
from collections import OrderedDict


tool_settings = {"label": "Reclass by Threshold",
                 "description": "Reclass by threshold values found in fields...",
                 "can_run_background": "True",
                 "category": "Raster"}


@result
class ReclassByThresholdRasterTool(BaseTool):

    def __init__(self):

        BaseTool.__init__(self, tool_settings)

        self.execution_list = [self.iterate]

        # self.from_value_field = None
        # self.to_value_field = None
        # self.output_value_field = None

        return

    @input_tableview("raster_table", "Table for Rasters", False, ["thresholds:thresholds:", "raster:geodata:"])
    @parameter("raster_format", "Format for output rasters", "GPString", "Required", False, "Input", raster_formats, None, None, "Esri Grid")
    @input_output_table_with_output_affixes
    def getParameterInfo(self):

        return BaseTool.getParameterInfo(self)

    def iterate(self):

        self.info(self.threshold_field)
        self.iterate_function_on_tableview(self.reclass, "raster_table", ["geodata"], return_to_results=True)

        return

    def reclass(self, data):

        parameter_dictionary = OrderedDict([(p.DisplayName, p.valueAsText) for p in self.parameters])
        parameter_summary = ", ".join(["{}: {}".format(k, v) for k, v in parameter_dictionary.iteritems()])
        self.info("Parameter summary: {}".format(parameter_summary))

        self.info("data : {}".format(data))
        ras = data["geodata"]

        utils.validate_geodata(ras, raster=True)

        ras_out = utils.make_raster_name(ras, self.result.output_workspace, self.raster_format, self.output_filename_prefix, self. output_filename_suffix)

        self.info("Reclassifying {0} -->> {1}...".format(ras, ras_out))

        # self.threshold_field = self.threshold_field.split(",")
        # for field in self.threshold_fields:
        #     # get field values
        #     # sort values
        #     # reflect


        # arcpy.ReclassByTable_3d(ras, self.in_remap_table, self.from_value_field, self.to_value_field, self.output_value_field, ras_out, self.missing_values)

        return {"geodata": ras_out, "source_geodata": ras}

# "http://desktop.arcgis.com/en/arcmap/latest/tools/3d-analyst-toolbox/reclass-by-table.htm"
