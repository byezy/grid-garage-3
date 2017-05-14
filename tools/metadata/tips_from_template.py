from base.base_tool import BaseTool
from base.class_decorators import geodata, results
from base.method_decorators import input_tableview, input_output_table

tool_settings = {"label": "Tips from Template",
                 "description": "Create a table of tips from a template",
                 "can_run_background": "True",
                 "category": "Metadata TODO"}


@geodata
@results
class TipsFromTemplateMetadataTool(BaseTool):
    def __init__(self):
        BaseTool.__init__(self, tool_settings)
        self.execution_list = [self.start_iteration]

    @input_tableview("geodata_table", "Table of Geodata", False, ["geodata:geodata:"])
    @input_output_table
    def getParameterInfo(self):
        return BaseTool.getParameterInfo(self)

    def start_iteration(self):
        self.iterate_function_on_parameter(self.process, "geodata_table", ["geodata"])
        return

    def process(self, data):
        self.log.info(data)
        # TODO
        return


def parse(run):
    """
    Clip raster based on current run parameters.

    #Clip_management (in_raster, rectangle, out_raster, {in_template_dataset},
    #                                      {nodata_value}, {clipping_geometry})
    ======== ===================================================================
    Arg1     run - A dictionary of run-time objects
    Return   None
    Raises   None
    Effect   A new dataset that is a clip of the original
    ======== ===================================================================
    """
    # tool.info(run['item_row'])
    tip_file = run['item_row'][1]

    assert tool.geodata_exists(tip_file), "Tip file {0} does not " \
                                          "exist".format(tip_file)

    tool.info("Parsing {0}".format(tip_file))

    tips = ODict()
    tips["header"] = ""

    with open(tip_file, "r") as tipfile:
        buf = "header"
        for line in tipfile:
            s = line.strip().encode("ascii").split(":", 1)
            if len(s) > 1:
                s1, s2 = s
                buf = s1
            else:
                s1 = s[0]
                s2 = None
            if not s2:
                tips[buf] += s1
            else:
                tips[s1] = s2

    tips["field_order"] = tips.keys()

    res = {"item": run["item"], "metadata": "to do", "tip_file": tip_file}
    res.update(tips)

    return res


# ------------------------------------------------------------------------------
# execute


# def main():
#     """Wraps executable code away from naughty loading.
#
#     For standard Grid-Garage tools we build the GridGarageTool class instance
#     with our custom parameters and execute the required methods.
#     ======== ===================================================================
#     Args     Argv entries as described by the global dictionary 'par'
#     Return   A table listing geodata found
#     Raises   Nothing explicitly
#     Effect   Geodata listed and catalogued
#     ======== ===================================================================
#     """
#     # place tool ref in global namespace and construct the tool class instance
#     global tool
#     tool = GridGarageTool(__file__, __version__, par)
#
#     # iterate a function over the items, saving the return
#     tool.run_f_iterate(parse, add_to_results=True)
