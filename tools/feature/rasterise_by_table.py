from base.base_tool import BaseTool
from base.results import result
from base import utils
from base.method_decorators import input_output_table_with_output_affixes, input_tableview, parameter, raster_formats
from os.path import splitext
from arcpy import FeatureToRaster_conversion, ImportMetadata_conversion


tool_settings = {"label": "Rasterise by Table",
                 "description": "Rasterise features by a 'field of fields'",
                 "can_run_background": "True",
                 "category": "Feature"}


@result
class RasteriseByTableTool(BaseTool):

    def __init__(self):

        BaseTool.__init__(self, tool_settings)
        self.execution_list = [self.iterate]

        return

    @input_tableview("features_table", "Table for Features and Fields", False, ["feature:geodata:", "fields:table_fields:"])
    @parameter("cell_size", "Cell Size", "GPSACellSize", "Required", False, "Input", None, "cellSize", None, None)
    @parameter("raster_format", "Format for output rasters", "GPString", "Required", False, "Input", raster_formats, None, None, None)
    @input_output_table_with_output_affixes
    def getParameterInfo(self):

        return BaseTool.getParameterInfo(self)

    def iterate(self):

        self.iterate_function_on_tableview(self.rasterise, "features_table", ["geodata", "table_fields"])

        return

    def rasterise(self, data):

        feat_ds = data["geodata"]

        utils.validate_geodata(feat_ds, vector=True)

        fields_string = data["table_fields"].strip().strip("[").strip("]")
        try:
            target_fields = [field.strip() for field in fields_string.split(",")]
        except:
            raise ValueError("Could not evaluate fields string '{0}'".format(fields_string))

        if not target_fields:
            raise ValueError("No target fields '{0}'".format(target_fields))

        for field in target_fields:
            try:

                r_out = utils.make_raster_name("{0}_{1}".format(splitext(feat_ds)[0], field), self.result.output_workspace, self.raster_format, self.output_filename_prefix, self.output_filename_suffix)
                self.info("Rasterising {0} on {1} -> {2}".format(feat_ds, field, r_out))
                FeatureToRaster_conversion(feat_ds, field, r_out)
                self.result.add_pass({"geodata": r_out, "source_geodata": feat_ds, "source_field": field})

                try:
                    ImportMetadata_conversion(feat_ds, "FROM_ARCGIS", r_out, "ENABLED")
                except:
                    self.warn("ImportMetadata_conversion - FROM_ARCGIS - failed")
                    try:
                        ImportMetadata_conversion(feat_ds, "FROM_ESRIISO", r_out, "ENABLED")
                    except:
                        self.warn("ImportMetadata_conversion - FROM_ESRIISO - failed")
                        try:
                            ImportMetadata_conversion(feat_ds, "FROM_FGDC", r_out, "ENABLED")
                        except:
                            self.warn("ImportMetadata_conversion - FROM_FGDC - failed")
                            try:
                                ImportMetadata_conversion(feat_ds, "FROM_ISO_19139", r_out, "ENABLED")
                            except:
                                self.warn("Looks like all 'ImportMetadata_conversion' variant calls failed.")

            except Exception as e:

                self.error("FAILED rasterising {0} on {1}: {2}".format(feat_ds, field, str(e)))
                self.result.add_fail(data)

