from base.base_tool import BaseTool
from base import results
from base.method_decorators import input_output_table_with_output_affixes, input_tableview
from os.path import splitext
from base.utils import make_table_name
from arcpy import Copy_management


tool_settings = {"label": "Copy",
                 "description": "Make a simple copy of geodata",
                 "can_run_background": "True",
                 "category": "Geodata"}


@results.result
class CopyGeodataTool(BaseTool):

    def __init__(self):

        BaseTool.__init__(self, tool_settings)
        self.execution_list = [self.iterate]

        return

    @input_tableview("geodata_table", "Table of Geodata", False, ["geodata:geodata:"])
    @input_output_table_with_output_affixes
    def getParameterInfo(self):

        return BaseTool.getParameterInfo(self)

    def iterate(self):

        self.iterate_function_on_tableview(self.copy, "geodata_table", ["geodata"], return_to_results=True)

        return

    def copy(self, data):

        geodata = data["geodata"]

        ext = splitext(geodata)[1]
        new_geodata = make_table_name(geodata, self.result.output_workspace, ext, self.output_filename_prefix, self.output_filename_suffix)

        self.log.info('Copying {0} --> {1}'.format(geodata, new_geodata))
        Copy_management(geodata, new_geodata)

        return {'geodata': new_geodata, 'copied_from': geodata}

# Copy_management(in_data, out_data, {data_type})
# "http://desktop.arcgis.com/en/arcmap/latest/tools/data-management-toolbox/copy.htm"
