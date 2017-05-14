from base.base_tool import BaseTool
from base.class_decorators import geodata, results
from base.method_decorators import input_tableview, input_output_table

tool_settings = {"label": "Tips from Tip Files",
                 "description": "Create a table of tips from tip files...",
                 "can_run_background": "True",
                 "category": "Metadata TODO"}


@geodata
@results
class TipsFromTipFilesMetadataTool(BaseTool):
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


# def init(run):
#     """
#     Initialise parameters as required for following tool code.
#
#     Some run time dictionary objects that remain static are set to globals to
#     reduce look-ups. In addition to that, in this function we manually set up
#     the result fields depending on user's choice of output detail
#     ======== =================================================================
#     Arg1     run - A dictionary of run-time objects
#     Return   None
#     Raises   Nothing explicitly
#     Effect   Adds some k:v's to the runtime dictionary
#     ======== =================================================================
#     """
#     # localise some dict values that remain static
#     # tool.info(run)
#     global tip_template
#     tip_template = run['tip_template']
#
#     global export_fields
#     export_fields = run['export_fields']
#
#     global base_tips
#     base_tips = None
#     if tip_template and tool.geodata_exists(tip_template):
#         with open(tip_template, "r") as tipfile:
#             base_tips = [line.rstrip() for line in tipfile]
#     else:
#         tool.info("Template {0} does not exist".format(tip_template))
#
#     global tip_order
#     tip_order = []
#     if base_tips:
#         base_tips = [t for t in base_tips if t]
#         k = [x.strip() for x in base_tips[0].split(",")]
#         v = [x.strip() for x in base_tips[1].split(",")]
#         base_tips = zip(k, v)
#         tipt = OrderedDict()
#         for t in base_tips:
#             tipt[t[0]] = t[1]
#         base_tips = tipt
#         tip_order = ",".join(base_tips.iterkeys())
#         # tool.info(base_tips)


# def build(run):
#     """
#     Clip raster based on current run parameters.
#
#     #Clip_management (in_raster, rectangle, out_raster, {in_template_dataset},
#     #                                      {nodata_value}, {clipping_geometry})
#     ======== ===================================================================
#     Arg1     run - A dictionary of run-time objects
#     Return   None
#     Raises   None
#     Effect   A new dataset that is a clip of the original
#     ======== ===================================================================
#      """
#     # tool.info(run)
#     geodata = run["item_row"][run["item_row_fields"].index("item")]
#     # tip_file = run["item_row"][run["item_row_fields"].index("tip_file")]
#
#     tool.info("Building tips for {0}".format(geodata))
#
#     global base_tips
#
#     # curr_tips = None
#     # if tip_file and tool.geodata_exists(tip_file):
#     #     with open(tip_file, "r") as tipfile:
#     #         curr_tips = [line.rstrip() for line in tipfile]
#     #
#     # if curr_tips:
#     #     curr_tips = [t for t in curr_tips if t]
#     #     tipd = OrderedDict()
#     #     tipd["Title"] = curr_tips[0]
#     #     for t in curr_tips[1:]:
#     #         a, b = t.split(":", 1)
#     #         tipd[a] = b
#     #     curr_tips = tipd
#
#     new_tips = None
#     # if curr_tips and base_tips:
#
#     if base_tips:
#         new_tips = OrderedDict()  # base_tips
#         for k, v in base_tips.iteritems():
#             new_tips[k] = v
#     #     for k, v in curr_tips.iteritems():
#     #         new_tips[k] = v
#     # elif base_tips:
#     #     new_tips = base_tips
#     # elif curr_tips:
#     #     new_tips = curr_tips
#
#     # here's where updates to default should occur
#
#     # tipfile2 = ""
#     r = {"item": geodata, "tip_order": tip_order}
#     r.update(new_tips)
#
#     return r
        # ,
        #     "existing_tipfile": tipfile,
        #     "base_tips": str(base_tips),
        #     "curr_tips": str(curr_tips),
        #     "new_tips": str(new_tips),
        #     "new_tipfile": tipfile2,
        #     "metadata": "to do"}


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
#     # run an initialisation function
#     tool.run_f_once(init)
#
#     # iterate a function over the items, saving the return
#     tool.run_f_iterate(build, add_to_results=True)
#
#     # finish up
#     tool.finish()
#
#
# if __name__ == '__main__':
#     main()
