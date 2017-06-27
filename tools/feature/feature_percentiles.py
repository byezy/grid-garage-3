from base.base_tool import BaseTool
from base.results import result
from base import utils
from base.method_decorators import input_tableview, input_output_table_with_output_affixes, parameter
import arcpy
import numpy


tool_settings = {"label": "Slice",
                 "description": "Slice raster",
                 "can_run_background": "True",
                 "category": "Raster"}


@result
class FeaturePercentilesTool(BaseTool):

    def __init__(self):

        BaseTool.__init__(self, tool_settings)

        self.execution_list = [self.iterate]

        return

    @input_tableview("feature_table", "Table for Features", False, ["feature:geodata:"])
    @parameter("value_field", "Value Field", "Field", "Required", False, "Input", None, None, ["feature_table"], 10, None)
    @parameter("ndv", "No Data Value", "GPLong", "Optional", False, "Input", None, None, None, 10, None)
    @input_output_table_with_output_affixes
    def getParameterInfo(self):

        return BaseTool.getParameterInfo(self)

    def iterate(self):

        self.iterate_function_on_tableview(self.percentiles, "raster_table", ["geodata"], return_to_results=True)

        return

    def percentiles(self, data):

        ras = data["geodata"]

        utils.validate_geodata(ras, raster=True)

        ras_out = utils.make_raster_name(ras, self.result.output_workspace, self.raster_format, self.output_filename_prefix, self. output_filename_suffix)

        self.info("Calculating percentiles {0} -->> {1}...".format(ras, ras_out))

        arr = arcpy.da.FeatureClassToNumPyArray(ras, self.value_field).astype(numpy.float32)

        if self.ndv:
            arr = arr[arr != self.ndv]
        # messages.addMessage(arr)

        v = {}
        for i in range(1, 99):
            p = numpy.percentile(arr, i)
            v[i] = p
        self.info("ints = {}, percentiles = {}".format(len(v), v))

        rtn = {"geodata": ras_out, "source_geodata": ras}.update(v)

        return rtn
