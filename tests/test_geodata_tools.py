import arcpy
from os.path import join
import sys

# # geodata tools
from tools.geodata.compare_extents import CompareExtentsGeodataTool
from tools.geodata.delete import DeleteGeodataTool
from tools.geodata.extract_parent import ExtractParentGeodataTool
from tools.geodata.generate_names import GenerateNamesGeodataTool
from tools.geodata.rename import RenameGeodataTool
from tools.geodata.display import DisplayGeodataTool
from tools.geodata.search import SearchGeodataTool
from tools.geodata.select import SelectGeodataTool
from tools.geodata.describe import DescribeGeodataTool

geodata_tools = {SearchGeodataTool,
                 DescribeGeodataTool,
                 SelectGeodataTool,
                 DisplayGeodataTool,
                 CompareExtentsGeodataTool,
                 DeleteGeodataTool,
                 ExtractParentGeodataTool,
                 GenerateNamesGeodataTool,
                 RenameGeodataTool}


class TestGeodataToolsTool(SearchGeodataTool):

    def __init__(self):
        SearchGeodataTool.__init__(self)
        self.label = u'Test Grid Garage Geodata Tools'
        self.description = u'Tests all of the currently implemented Grid Garage geodata tools'
        self.canRunInBackground = True

        return

    def getParameterInfo(self):

        # param0 = arcpy.Parameter()
        # param0.name = u'output_workspace'
        # param0.displayName = u'Output Data Workspace'
        # param0.parameterType = 'Required'
        # param0.direction = 'Input'
        # param0.datatype = u'DEWorkspace'
        #
        # param1 = arcpy.Parameter()
        # param1.name = u'input_workspace'
        # param1.displayName = u'Input Data Workspace'
        # param1.parameterType = 'Required'
        # param1.direction = 'Input'
        # param1.datatype = u'DEWorkspace'

        # search = SearchGeodataTool()
        gg_excludes = ["output_workspace", "result_table_name"]

        def exclude(item_list, exclude_list):
            return [item for item in item_list if item not in exclude_list]

        def catgorise_parameters(parameter_list, category):
            for p in parameter_list:
                p.category = category
            return

        search_pars = exclude(SearchGeodataTool.getParameterInfo(self), gg_excludes)
        catgorise_parameters(search_pars, "Search")

        return search_pars

    def isLicensed(self):

        return True

    def updateParameters(self, parameters):

        return

    def updateMessages(self, parameters):

        return

    def execute(self, parameters, messages):

        out_ws = parameters[0].valueAsText
        in_ws = parameters[1].valueAsText
        fail_ws = join(out_ws, "fails.gdb")  # "C:\\Data\\grid-garage-tests\\models-test-tools\\FAILS.gdb"

        search = SearchGeodataTool()
        arguments = [out_ws, in_ws, 100]

        result = getattr(search, "execute")(*arguments)

        messages.addResult(result)

        # StudyArea_Armidale = "C:\\Data\\grid-garage-sample-data\\StudyArea_Armidale"
        # Result_Table_Search__6_ = "C:\\Data\\grid-garage-tests\\models-test-tools\\test.gdb\\T0110_01Search_20170518_114437"
        # Result_Table_Search__9_ = Result_Table_Search__6_
        # Result_Table_Search__7_ = Result_Table_Search__9_
        # Result_Table_Search__8_ = Result_Table_Search__7_
        # Result_Table_Search__10_ = Result_Table_Search__8_
        # Result_Table_Search__11_ = Result_Table_Search__10_
        # Result_Table_Search__20_ = Result_Table_Search__11_
        # Result_Table_Search__12_ = Result_Table_Search__20_
        # Result_Table_Search__16_ = Result_Table_Search__12_
        # Result_Table_Search__13_ = Result_Table_Search__16_
        # Result_Table_Search__14_ = Result_Table_Search__13_
        # Result_Table_Search__15_ = Result_Table_Search__14_
        # Result_Table_Search__17_ = Result_Table_Search__15_
        # Result_Table_Search__18_ = Result_Table_Search__17_
        # Result_Table_Search__19_ = Result_Table_Search__18_
        # Result_Table_Search = Result_Table_Search__19_
        # Result_Table_Search__2_ = Result_Table_Search
        # T0310_01Search_20170516_094116 = Result_Table_Search__2_
        # T0320_01Search_20170516_094141 = T0310_01Search_20170516_094116
        # Result_Table_Search__3_ = T0320_01Search_20170516_094141
        # Result_Table_Search__4_ = Result_Table_Search__3_
        # Result_Table_Search__5_ = Result_Table_Search__4_
        # T0430_01_GeodataSelect_20170518_095728 = Result_Table_Search__5_
        # T0170_04__LookupByTableRaster_20170517_174859_FAIL = T0430_01_GeodataSelect_20170518_095728
        #
        # # Process: GG3_Test_Raster_Aggregate (110)
        # arcpy.Model3103_GGV3_005("C:\\Data\\grid-garage-tests\\models-test-tools_sample-data;C:\\Data\\grid-garage-sample-data\\StudyArea_Armidale",
        #                          "raster_band_meanCellHeight = 25", "NODATA", "TRUNCATE", "10", v_Workspace_, "T0110")
        #
        # # Process: GG3_Test_Raster_Block_Statistics (120)
        # arcpy.Model311_GGV3_005("C:\\Data\\grid-garage-tests\\models-test-tools_sample-data;C:\\Data\\grid-garage-sample-data\\StudyArea_Armidale",
        #                         "raster_band_meanCellHeight = 25", v_Workspace_, "T0120")
        #
        # # Process: GG3_Test_Raster_Build_Attribute_Table (130)
        # arcpy.Model312322_GGV3_005("C:\\Data\\grid-garage-tests\\models-test-tools_sample-data;C:\\Data\\grid-garage-sample-data\\StudyArea_Armidale",
        #                            v_Workspace_, "T0130", "raster_band_meanCellHeight = 30")
        #
        # # Process: GG3_Test_Raster_Calculate_Statistic (140)
        # arcpy.Model313_GGV3_005("C:\\Data\\grid-garage-tests\\models-test-tools_sample-data;C:\\Data\\grid-garage-sample-data\\StudyArea_Armidale",
        #                         "raster_band_meanCellHeight = 30", v_Workspace_, "T0140")
        #
        # # Process: GG3_Test_Raster_Clip (150)
        # arcpy.Model314_GGV3_005("C:\\Data\\grid-garage-tests\\models-test-tools_sample-data;C:\\Data\\grid-garage-sample-data\\StudyArea_Armidale",
        #                         v_Workspace_, "T0150")
        #
        # # Process: GG3_Test_Raster_Copy (160)
        # arcpy.Model315_GGV3_005("C:\\Data\\grid-garage-tests\\models-test-tools_sample-data;C:\\Data\\grid-garage-sample-data\\StudyArea_Armidale",
        #                         "dataset_datasetType = 'RasterDataset'", v_Workspace_, "T0160")
        #
        # # Process: GG3_Test_Raster_Lookup_by_Table (170)
        # arcpy.Model32_GGV3_005("C:\\Data\\grid-garage-tests\\models-test-tools_sample-data;C:\\Data\\grid-garage-sample-data\\StudyArea_Armidale",
        #                        "general_baseName = 'demfill25m'", v_Workspace_, "T0170")
        #
        # # Process: GG3_Test_Raster_Reclass_by_Table  (180)
        # arcpy.Model33_GGV3_005("C:\\Data\\grid-garage-tests\\models-test-tools_sample-data;C:\\Data\\grid-garage-sample-data\\StudyArea_Armidale",
        #                        "raster_band_meanCellHeight = 25", v_Workspace_, "T0180")
        #
        # # Process: GG3_Test_Raster_Reproject (190)
        # arcpy.Model34_GGV3_005("C:\\Data\\grid-garage-tests\\models-test-tools_sample-data;C:\\Data\\grid-garage-sample-data\\StudyArea_Armidale",
        #                        "raster_band_meanCellHeight = 25", v_Workspace_, "T0190")
        #
        # # Process: GG3_Test_Raster_Resample (200)
        # arcpy.Model35_GGV3_005("C:\\Data\\grid-garage-tests\\models-test-tools_sample-data;C:\\Data\\grid-garage-sample-data\\StudyArea_Armidale",
        #                        "dataset_spatialReference = 'GDA_1994_MGA_Zone_56'", v_Workspace_, "T0200")
        #
        # # Process: GG3_Test_Raster_Set_NoData_Value (210)
        # arcpy.Model36_GGV3_005("C:\\Data\\grid-garage-tests\\models-test-tools_sample-data;C:\\Data\\grid-garage-sample-data\\StudyArea_Armidale",
        #                        "general_baseName = 'SPOT5_WoodyExtent_Armidale_sml'", v_Workspace_, "T0210")
        #
        # # Process: GG3_Test_Raster_Set_Value_to_Null (220)
        # arcpy.Model37_GGV3_005("C:\\Data\\grid-garage-tests\\models-test-tools_sample-data;C:\\Data\\grid-garage-sample-data\\StudyArea_Armidale",
        #                        "general_baseName = 'netvegkc100m_sml'", v_Workspace_, "T0220")
        #
        # # Process: GG3_Test_Raster_Transform (230)
        # arcpy.Model38_GGV3_005("C:\\Data\\grid-garage-tests\\models-test-tools_sample-data;C:\\Data\\grid-garage-sample-data\\StudyArea_Armidale",
        #                        "general_baseName = 'netvegkc100m_sml'", v_Workspace_, "T0230")
        #
        # # Process: GG3_Test_Raster_Tweak_Values (240)
        # arcpy.Model39_GGV3_005("C:\\Data\\grid-garage-tests\\models-test-tools_sample-data;C:\\Data\\grid-garage-sample-data\\StudyArea_Armidale",
        #                        "general_baseName = 'demfill25m'", v_Workspace_, "T0240")
        #
        # # Process: GG3_Test_Raster_Tweak_Values_INT (250)
        # arcpy.Model393_GGV3_005("C:\\Data\\grid-garage-tests\\models-test-tools_sample-data;C:\\Data\\grid-garage-sample-data\\StudyArea_Armidale",
        #                         "general_baseName = 'demfill25m'", v_Workspace_, "T0250")
        #
        # # Process: GG3_Test_Raster_Values_at_Points (260)
        # arcpy.Model392_GGV3_005("C:\\Data\\grid-garage-tests\\models-test-tools_sample-data;C:\\Data\\grid-garage-sample-data\\StudyArea_Armidale",
        #                         "dataset_spatialReference = 'GDA_1994_MGA_Zone_56'", v_Workspace_, "T0260")
        #
        # # Process: GG3_Test_Feature_Clip (300)
        # arcpy.Model5_GGV3_005("C:\\Data\\grid-garage-tests\\models-test-tools_sample-data",
        #                       "general_name = 'netvegkc100m_sml.shp' OR general_name = 'Armidale_Dumaresq_Council_GDAz56.shp' OR general_name = 'VegBorderRiversGwydir_Comp09_VIS3801.shp'",
        #                       "T0300", v_Workspace_)
        #
        # # Process: GG3_Test_Feature_Copy
        # arcpy.Model6_GGV3_005("T0310", v_Workspace_)
        #
        # # Process: GG3_Test_Feature_RasteriseByTable
        # arcpy.Model7_GGV3_005("C:\\Data\\grid-garage-tests\\models-test-tools_sample-data;C:\\Data\\grid-garage-sample-data\\StudyArea_Armidale", "T0320",
        #                       v_Workspace_)
        #
        # # Process: GG3_Test_Geodata_CompareExtents (400)
        # arcpy.Model52_GGV3_005("C:\\Data\\grid-garage-tests\\models-test-tools_sample-data;C:\\Data\\grid-garage-sample-data\\StudyArea_Armidale", "", "T0400",
        #                        v_Workspace_)
        #
        # # Process: GG3_Test_Geodata_Copy_Delete (410)
        # arcpy.Model522_GGV3_005("T0410", v_Workspace_)
        #
        # # Process: GG3_Test_Geodata_GenerateNamesRenameDisplay (420)
        # arcpy.Model523_GGV3_005("dataset_spatialReference = 'GDA_1994_MGA_Zone_56'", "T0420", v_Workspace_)
        #
        # # Process: GG3_Test_Geodata_Select_ListWorkspaceTables
        # arcpy.Model1_GGV3_005("T0430", FAILS_gdb, v_Workspace_)
        #
        # # Process: GG3_Iterate_Tables_FAILS
        # arcpy.Model42_GGV3_005(FAILS_gdb, "*_FAIL", v_Workspace_)
        #
        # # Process: GG3_Iterate_Tables
        # arcpy.Model4_GGV3_005(FAILS_gdb, "*__*", v_Workspace_)


