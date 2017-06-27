from base.base_tool import BaseTool
from base.results import result
from base import utils
from base.method_decorators import input_tableview, input_output_table_with_output_affixes, parameter
import arcpy
import numpy


tool_settings = {"label": "Field Percentiles",
                 "description": "Calculate numeric field percentiles",
                 "can_run_background": "True",
                 "category": "Feature"}


@result
class FeaturePercentilesTool(BaseTool):

    def __init__(self):

        BaseTool.__init__(self, tool_settings)

        self.execution_list = [self.iterate]

        return

    @input_tableview("feature_table", "Table for Features", False, ["feature:geodata:"])
    @parameter("value_field", "Value Field", "GPSTring", "Required", False, "Input", None, None, None, None, None)
    @parameter("ndv", "No Data Value", "GPLong", "Optional", False, "Input", None, None, None, None, None)
    @input_output_table_with_output_affixes
    def getParameterInfo(self):

        return BaseTool.getParameterInfo(self)

    def iterate(self):

        self.iterate_function_on_tableview(self.percentiles, "feature_table", ["geodata"], return_to_results=True)

        return

    def percentiles(self, data):

        feats = data["geodata"]

        utils.validate_geodata(feats, vector=True)

        if self.value_field not in [f.name for f in arcpy.ListFields(feats)]:
            raise ValueError("Field '{}' is not in '{}' skipping '{}'".format(self.value_field, arcpy.ListFields(feats), feats))

        self.info("Calculating percentiles for {0}".format(feats))

        arr = arcpy.da.FeatureClassToNumPyArray(feats, self.value_field).astype(numpy.float32)

        if self.ndv:
            arr = arr[arr != self.ndv]

        v = {}
        for i in range(1, 99):
            p = numpy.percentile(arr, i)
            v[i] = p
        self.info("ints = {}, percentiles = {}".format(len(v), v))

        rtn = {"geodata": feats, "source_geodata": feats}.update(v)

        return rtn
