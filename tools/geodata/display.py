from base.base_tool import BaseTool
from base import arcmap
from base.method_decorators import input_tableview


tool_settings = {"label": "Display",
                 "description": "Adds geodata to ArcMap document",
                 "can_run_background": False,
                 "category": "Geodata"}


class DisplayGeodataTool(BaseTool):

    def __init__(self):

        BaseTool.__init__(self, tool_settings)
        self.execution_list = [self.iterate]

        return

    @input_tableview("geodata_table", "Table of Geodata", False, ["geodata:geodata:"])
    def getParameterInfo(self):

        return BaseTool.getParameterInfo(self)

    def iterate(self):

        self.iterate_function_on_tableview(self.display_geodata, "geodata_table", ["geodata"])

        return

    def display_geodata(self, data):

        geodata = data["geodata"]
        try:
            # see if it's a layer
            arcmap.add_layer(geodata, "BOTTOM")
            self.log.info("Added layer {0} to display".format(geodata))
        except Exception:
            try:
                # see if it's a table
                arcmap.add_tableview(geodata)
                self.log.info("Added table {0} to display".format(geodata))
            except Exception as e:
                # bugger it for now
                self.log.warn("Could not add {0} to display: {1}".format(geodata, str(e)))
        finally:
            # Refresh things
            arcmap.refresh_active_view()
            arcmap.refresh_toc()

