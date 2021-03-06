from base.base_tool import BaseTool
from base import utils
from base.decorators import input_tableview, input_output_table, parameter, data_nodata, raster_formats
import arcpy
from collections import OrderedDict


tool_settings = {"label": "Reclass by Threshold",
                 "description": "Reclass by threshold values found in fields...",
                 "can_run_background": "True",
                 "category": "Raster"}


class ReclassByThresholdRasterTool(BaseTool):
    """
    """

    def __init__(self):
        """

        Returns:

        """

        BaseTool.__init__(self, tool_settings)

        self.execution_list = [self.iterate]

        return

    @input_tableview(data_type="raster", other_fields="thresholds Thresholds Required thresholds")
    @parameter("raster_format", "Format for output rasters", "GPString", "Required", False, "Input", raster_formats, None, None, "Esri Grid")
    @input_output_table(affixing=True)
    def getParameterInfo(self):
        """

        Returns:

        """

        return BaseTool.getParameterInfo(self)

    def iterate(self):
        """

        Returns:

        """

        try:
            self.info(self.thresholds)
        except:
            pass

        self.iterate_function_on_tableview(self.reclass, return_to_results=True)

        return

    # def make_remap(self, value, minv, maxv):
    #     self.info(locals())
    #
    #     if not value:
    #         raise ValueError("No threshold string")
    #
    #     thresholds = value.strip().split(";")
    #
    #     if not thresholds:
    #         raise ValueError("\tNo thresholds set")
    #
    #     thresholds = [(float(x), float(y), float(z)) for x, y, z in thresholds]
    #
    #     flattened = [x for x in y for y in thresholds]  # if isinstance(x, int) else min(x) for x in list2)
    #
    #     mint, maxt = min([flattened]), max(flattened)
    #
    #     if mint < minv:
    #         raise ValueError("\tMin threshold under min value {} < {}".format(mint, minv))
    #
    #     if maxt > maxv:
    #         raise ValueError("\tMax threshold over max value {} > {}".format(maxt, maxv))
    #
    #     self.info(thresholds)
    #
    #     remap = ";".join(thresholds)
    #
    #     self.info(remap)
    #     return thresholds

    def reclass(self, data):
        """

        Args:
            data:

        Returns:

        """

        ras = data["raster"]

        utils.validate_geodata(ras, raster=True)

        ws = self.output_file_workspace or self.output_workspace

        ras_out = utils.make_table_name(ras, ws, self.raster_format, self.output_filename_prefix, self. output_filename_suffix)

        self.info("Reclassifying {} -->> {}...".format(ras, ras_out))

        # remap = data["thresholds"]
        if not data["thresholds"]:
            raise ValueError("\tNo thresholds set")

        self.info("\tUpdating RAT...")
        arcpy.BuildRasterAttributeTable_management(ras, "Overwrite")

        self.info("\tUpdating statistics...")
        arcpy.CalculateStatistics_management(ras)

        # "0 5 1;5.01 7.5 2;7.5 10 3"  from, to, new
        minv = float(arcpy.GetRasterProperties_management(ras, "MINIMUM").getOutput(0))
        maxv = float(arcpy.GetRasterProperties_management(ras, "MAXIMUM").getOutput(0))
        mean = float(arcpy.GetRasterProperties_management(ras, "MEAN").getOutput(0))
        std = float(arcpy.GetRasterProperties_management(ras, "STD").getOutput(0))

        remap = data["thresholds"].replace("MIN", str(minv)).replace("MAX", str(maxv))

        self.info(["Args=", ras, "Value", remap, ras_out, "NODATA"])

        self.info("Reclassifying...")

        arcpy.Reclassify_3d(ras, "Value", remap, ras_out, "NODATA")

        self.info("Done")
        # self.info("Adding ")
        #
        # # AddField_management(in_table, field_name, field_type, {field_precision}, {field_scale}, {field_length}, {field_alias}, {field_is_nullable}, {field_is_required}, {field_domain})
        # arcpy.AddField_management(ras_out, "asdst_value", "TEXT", 50)
        #
        # v = ["no", "Low", "Medium", "High"]
        #
        # with arcpy.da.UpdateCursor(ras_out, ["asdst_value", "Value"]) as cursor:
        #     for row in cursor:
        #         row[0] = v[row[1]]
        #         cursor.updateRow(row)

        return {"raster": ras_out, "source_geodata": ras, "min_max_mean_std": "{}_{}_{}_{}".format(minv, maxv, mean, std), "remap": remap}

