# -*- coding: utf-8 -*-
"""
Created on Thu Sep  1 10:48:26 2016

@author: byed
"""
from base import utils
from base import log
from base.log import log_error
import arcpy


class BaseTool(object):

    @log_error
    def __init__(self, settings):

        self.debug = log.debug
        self.info = log.info
        self.warn = log.warn
        self.label = settings.get("label", "label not set")
        self.description = settings.get("description", "description not set")
        self.canRunInBackground = settings.get("can_run_background", False)
        self.category = settings.get("category", False)
        self.parameters = None
        self.run_id = "{0}_{1}".format(type(self).__name__, utils.time_stamp())
        self.execution_list = []

        return

    @log_error
    def get_parameter(self, param_name, raise_not_found_error=False):

        if self.parameters:

            for param in self.parameters:
                if param.name == param_name:
                    return param

        if raise_not_found_error:
            raise ValueError("Parameter {0} not found".format(param_name))

        return

    def getParameterInfo(self):

        return []

    def isLicensed(self):

        return True

    @log_error
    def updateParameters(self, parameters):

        ps = [(i, p.name) for i, p in enumerate(parameters)]
        self.debug("BaseTool.updateParameters {}".format(ps))

        # set default result table name

        out_tbl_par = None
        for p in parameters:
            if p.name == "result_table_name":
                out_tbl_par = p
                break

        if out_tbl_par and out_tbl_par.value == "#run_id#":
            out_tbl_par.value = self.run_id

        # validate workspace and raster format

        out_ws_par = None
        for p in parameters:
            if p.name == "output_workspace":
                out_ws_par = p
                break

        ras_fmt_par = None
        for p in parameters:
            if p.name == "raster_format":
                ras_fmt_par = p
                break

        if out_ws_par and ras_fmt_par:

            out_ws_par.clearMessage()
            ras_fmt_par.clearMessage()

            if out_ws_par.altered or ras_fmt_par.altered:

                ws = out_ws_par.value
                fmt = ras_fmt_par.value

                if utils.is_local_gdb(ws) and fmt != "Esri Grid":
                    ras_fmt_par.setErrorMessage("Invalid raster format for workspace type")

        return

    @log_error
    def updateMessages(self, parameters):

        self.debug("Well, in here anyway...")
        # out_ws_par = None
        # for p in parameters:
        #     if p.name == "output_workspace":
        #         out_ws_par = p
        #         break
        #
        # ras_fmt_par = None
        # for p in parameters:
        #     if p.name == "raster_format":
        #         ras_fmt_par = p
        #         break
        #
        # if out_ws_par and ras_fmt_par:
        #
        #     out_ws_par.clearMessage()
        #     ras_fmt_par.clearMessage()
        #     # self.debug("messages cleared")
        #
        #     if out_ws_par.altered or ras_fmt_par.altered:
        #         # self.debug("out_ws_par.altered or out_rasfmt_par.altered")
        #
        #         ws = out_ws_par.value
        #         fmt = ras_fmt_par.value
        #         # self.debug("ws={} fmt={}".format(ws, fmt))
        #         if base.utils.is_local_gdb(ws) and fmt != "Esri Grid":
        #             ras_fmt_par.setErrorMessage("Invalid raster format for workspace type")
        # try:
        #     # self.debug("updateMessages")
        #
        #     out_ws_par = self.get_parameter_by_name("output_workspace")  # None
        #     out_rasfmt_par = self.get_parameter_by_name("raster_format")  # None
        #
        #     if out_ws_par and out_rasfmt_par:
        #         # self.debug("out_ws_par and out_rasfmt_par")
        #
        #         out_ws_par.clearMessage()
        #         out_rasfmt_par.clearMessage()
        #         # self.debug("messages cleared")
        #
        #         if out_ws_par.altered or out_rasfmt_par.altered:
        #             # self.debug("out_ws_par.altered or out_rasfmt_par.altered")
        #
        #             ws = out_ws_par.value
        #             fmt = out_rasfmt_par.value
        #             # self.debug("ws={} fmt={}".format(ws, fmt))
        #             if base.utils.is_local_gdb(ws) and fmt != "Esri Grid":
        #                 out_rasfmt_par.setErrorMessage("Invalid raster format for workspace type")
        # except Exception as e:
        #     # self.debug("updateMessages error : {}".format(e))
        #     print str(e)

        # BaseTool.updateMessages(self, parameters)
        # stretch = parameters[2].value == 'STRETCH'
        # if stretch and not parameters[3].valueAsText:
        #     parameters[3].setIDMessage("ERROR", 735, parameters[3].displayName)
        # if stretch and not parameters[4].valueAsText:
        #     parameters[4].setIDMessage("ERROR", 735, parameters[4].displayName)

        return

    @log_error
    def execute(self, parameters, messages):

        log.configure_logging(messages)

        if not self.execution_list:
            raise ValueError("Tool execution list is empty")

        self.info("Debugging log file is located at '{}'".format(log.LOG_FILE))

        self.parameters = parameters

        for k, v in self.get_parameter_dict().iteritems():
            setattr(self, k, v)

        self.debug("Tool attributes set {}".format(self.__dict__))

        try:
            init = self.result.initialise(self.get_parameter("result_table"),
                                          self.get_parameter("fail_table"),
                                          self.get_parameter("output_workspace").value,
                                          self.get_parameter("result_table_name").value)
            self.info(init)
        except AttributeError:
            pass

        with log.error_trap(self):
            for f in self.execution_list:
                f()

        try:
            self.result.write()
        except AttributeError:
            pass

        return

    @log_error
    def get_parameter_dict(self, leave_as_object=()):
        """ Create a dictionary of parameters

        Args:
            leave_as_object (): A list of parameter names to leave as objects rather than return strings

        Returns: A dictionary of parameters - strings or parameter objects

        """

        # create the dict
        # TODO make multivalue parameters a list
        # TODO see what binning the bloody '#' does to tools
        pd = {}
        for p in self.parameters:
            name = p.name
            if name in leave_as_object:
                pd[name] = p
            elif p.datatype == "Boolean":
                pd[name] = [False, True][p.valueAsText == "true"]
            elif p.datatype == "Double":
                pd[name] = float(p.valueAsText) if p.valueAsText else None
            elif p.datatype == "Long":
                pd[name] = int(float(p.valueAsText)) if p.valueAsText else None
            else:
                pd[name] = p.valueAsText or "#"

        # now fix some specific parameters
        x = pd.get("raster_format", None)
        if x:
            pd["raster_format"] = "" if x.lower() == "esri grid" else '.' + x

        def set_hash_to_empty(p):
            v = pd.get(p, None)
            if v:
                pd[p] = "" if v == "#" else v
            return

        set_hash_to_empty("output_filename_prefix")
        set_hash_to_empty("output_filename_suffix")

        return pd

    @log_error
    def iterate_function_on_tableview(self, func, parameter_name, key_names, nonkey_names=None, return_to_results=False):
        """ Runs a function over the values in a tableview parameter - a common tool scenario

        Args:
            func (): Function to run
            parameter_name (): Parameter to run on
            key_names (): Fields in the rows to provide

        Returns:

        """
        self.debug("locals = {}".format(locals()))

        param = self.get_parameter(parameter_name)
        if param.datatype != "Table View":
            raise ValueError("That parameter is not a table or table view ({0})".format(param.name))

        multi_val = getattr(param, "multiValue", False)
        if multi_val:
            raise ValueError("Multi-value tableview iteration is not yet implemented")

        gg_in_table_text = param.valueAsText

        gg_in_table = "gg_in_table"
        if arcpy.Exists(gg_in_table):
            arcpy.Delete_management(gg_in_table)
        arcpy.MakeTableView_management(gg_in_table_text, gg_in_table)

        gg_in_table_fields = [f.name for f in arcpy.ListFields(gg_in_table)]
        proc_hist_fieldname = "proc_hist"
        if proc_hist_fieldname not in gg_in_table_fields:
            arcpy.AddField_management(gg_in_table, proc_hist_fieldname, "TEXT", None, None, 500000)

        # map fields
        num_fields = len(key_names)  # [rf1, rf2, ...]
        f_names = ["{0}_field_{1}".format(parameter_name, i) for i in range(0, num_fields)]  # [f_0, f_1, ...]
        f_vals = [self.get_parameter(f_name).valueAsText for f_name in f_names]
        f_vals.append(proc_hist_fieldname)
        if nonkey_names:
            f_vals.extend(nonkey_names)
        rows = [r for r in arcpy.da.SearchCursor(gg_in_table, f_vals)]

        # iterate
        key_names.append(proc_hist_fieldname)
        if nonkey_names:
            key_names.extend(nonkey_names)

        self.do_iteration(func, rows, key_names, return_to_results)

        return

    @log_error
    def iterate_function_on_parameter(self, func, parameter_name, key_names, nonkey_names=None, return_to_results=False):
        """ Runs a function over the values in a parameter - a less common tool scenario

        Args:
            func (): Function to run
            parameter_name (): Parameter to run on
            key_names (): Fields in the rows to provide

        Returns:

        """

        param = self.get_parameter(parameter_name)
        multi_val = getattr(param, "multiValue", False)
        self.debug("multiValue attribute is {}".format(multi_val))

        if param.datatype == "Table View":
            raise ValueError("No, use 'iterate_function_on_tableview'")

        self.debug("param.valueAsText =  {}".format(param.valueAsText))
        self.debug("param.valueAsText.split(';' =  {}".format(param.valueAsText.split(";")))
        rows = param.valueAsText.split(";") if multi_val else [param.valueAsText]

        for row in rows:  # add proc_hist field
            utils.make_tuple(row).append("")

        self.debug("Processing rows will be {}".format(rows))

        # iterate
        key_names.append("proc_hist")
        if nonkey_names:
            key_names.extend(nonkey_names)

        self.do_iteration(func, rows, key_names, return_to_results)

        return

    @log_error
    def do_iteration(self, func, rows, key_names, return_to_results):

        if not rows:
            raise ValueError("No values or records to process.")

        fname = func.__name__
        log_error(func)

        rows = [{k: v for k, v in zip(key_names, utils.make_tuple(row))} for row in rows]
        self.info("{} items to process".format(len(rows)))

        for row in rows:
            try:
                try:
                    self.result.new_proc_hist = "Tool='{}' Parameters={} Row={}".format(self.label, self.get_parameter_dict(), row)
                except AttributeError:
                    pass

                self.debug("Running {} with data={}".format(fname, row))
                res = func(row)
                if return_to_results:
                    try:
                        self.info(self.result.add(res))
                    except AttributeError:
                        raise ValueError("No result attribute for result record")

            except Exception as e:

                log.error("error executing {}: {}".format(fname, str(e)))
                try:
                    self.result.fail(row)
                except AttributeError:
                    pass

        return
