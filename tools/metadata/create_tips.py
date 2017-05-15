from base.base_tool import BaseTool
import base.results
import base.utils
from base.method_decorators import input_tableview, input_output_table, parameter
from collections import OrderedDict
import os

tool_settings = {"label": "Create Tips",
                 "description": "Create a table of tips from a tip file template",
                 "can_run_background": "True",
                 "category": "Metadata"}


@base.results.result
class CreateTipFilesMetadataTool(BaseTool):
    def __init__(self):

        BaseTool.__init__(self, tool_settings)
        self.execution_list = [self.initialise, self.iterate]
        self.base_tips = None
        self.tip_order = []

    @input_tableview("geodata_table", "Table of Geodata", False, ["geodata:geodata:"])
    @parameter("tip_template", "Tip Template", "DEFile", "Required", False, "Input", None, None, None, None, None)
    @parameter("include_fields", "Include Fields", "DEFile", "Required", True, "Input", None, None, ["tip_template"], None, None)
    @input_output_table
    def getParameterInfo(self):

        return BaseTool.getParameterInfo(self)

    def initialise(self):

        if os.path.exists(self.tip_template):
            with open(self.tip_template, "r") as tipfile:
                self.base_tips = [line.rstrip() for line in tipfile]
        else:
            raise ValueError("Template {0} does not exist".format(self.tip_template))

        if self.base_tips:
            base_tips = [t for t in self.base_tips if t]
            k = [x.strip() for x in base_tips[0].split(",")]
            v = [x.strip() for x in base_tips[1].split(",")]
            base_tips = zip(k, v)
            tipt = OrderedDict()
            for t in base_tips:
                tipt[t[0]] = t[1]
            self.base_tips = tipt
            self.tip_order = ",".join(self.base_tips.iterkeys())

        return

    def iterate(self):

        self.iterate_function_on_parameter(self.create, "geodata_table", ["geodata"])

        return

    def create(self, data):

        geodata = data["geodata"]

        base.utils.validate_geodata(geodata)

        self.log.info("Building tips for {0}".format(geodata))

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
