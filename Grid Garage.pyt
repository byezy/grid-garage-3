# geodata tools
from tools.geodata.compare_extents import CompareExtentsGeodataTool
from tools.geodata.copy import CopyGeodataTool
from tools.geodata.delete import DeleteGeodataTool
# from tools.geodata.extract_parent import ExtractParentGeodataTool
from tools.geodata.generate_names import GenerateNamesGeodataTool
from tools.geodata.rename import RenameGeodataTool
from tools.geodata.display import DisplayGeodataTool
from tools.geodata.search import SearchGeodataTool
from tools.geodata.select import SelectGeodataTool
from tools.geodata.describe import DescribeGeodataTool
from tools.geodata.list_workspace_tables import ListWorkspaceTablesGeodataTool
# feature tools
from tools.feature.rasterise_by_table import RasteriseByTableTool
from tools.feature.copy import CopyFeatureTool
from tools.feature.clip import ClipFeatureTool
from tools.feature.feature_percentiles import FeaturePercentilesTool
# raster tools
from tools.raster.aggregate import AggregateRasterTool
from tools.raster.block_statistics import BlockStatisticsRasterTool
from tools.raster.build_attribute_table import BuildAttributeTableRasterTool
from tools.raster.calculate_statistics import CalculateStatisticsRasterTool
from tools.raster.clip import ClipRasterTool
from tools.raster.copy import CopyRasterTool
from tools.raster.lookup_by_table import LookupByTableRasterTool
from tools.raster.values_at_points import ValuesAtPointsRasterTool
from tools.raster.reproject import ReprojectRasterTool
from tools.raster.reclass_by_table import ReclassByTableRasterTool
from tools.raster.resample import ResampleRasterTool
from tools.raster.set_no_data_value import SetNodataValueRasterTool
from tools.raster.set_value_to_null import SetValueToNullRasterTool
from tools.raster.transform import TransformRasterTool
from tools.raster.tweak_values import TweakValuesRasterTool
from tools.raster.properties import BandPropetiesRasterTool
from tools.raster.values_to_points import ValuesToPointsRasterTool
from tools.raster.slice import SliceRasterTool
# metadata tools
from tools.metadata.audit import AuditMetadataTool
from tools.metadata.create_tips import CreateTipsTableMetadataTool
from tools.metadata.import_tips import ImportTipFilesToTableMetadataTool
from tools.metadata.export_tips import ExportTipsToFileMetadataTool
from tools.metadata.export_xml import ExportXmlMetadataTool
from tools.metadata.id_from_xml import GetIARIDFromXmlTool
from tools.metadata.import_metadata import ImportMetadataTool


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the .pyt file)."""
        self.label = "Grid Garage"
        self.alias = "GridGarage"

        geodata_tools = {SearchGeodataTool,
                         CopyGeodataTool,
                         DescribeGeodataTool,
                         SelectGeodataTool,
                         DisplayGeodataTool,
                         CompareExtentsGeodataTool,
                         DeleteGeodataTool,
                         GenerateNamesGeodataTool,
                         RenameGeodataTool,
                         ListWorkspaceTablesGeodataTool}

        feature_tools = {RasteriseByTableTool,
                         CopyFeatureTool,
                         ClipFeatureTool,
                         FeaturePercentilesTool}

        raster_tools = {AggregateRasterTool,
                        BlockStatisticsRasterTool,
                        BuildAttributeTableRasterTool,
                        CalculateStatisticsRasterTool,
                        ClipRasterTool,
                        CopyRasterTool,
                        LookupByTableRasterTool,
                        ValuesAtPointsRasterTool,
                        ReprojectRasterTool,
                        ReclassByTableRasterTool,
                        ResampleRasterTool,
                        SetNodataValueRasterTool,
                        SetValueToNullRasterTool,
                        TransformRasterTool,
                        TweakValuesRasterTool,
                        BandPropetiesRasterTool,
                        ValuesToPointsRasterTool,
                        SliceRasterTool}

        metadata_tools = {AuditMetadataTool,
                          CreateTipsTableMetadataTool,
                          ImportTipFilesToTableMetadataTool,
                          ExportTipsToFileMetadataTool,
                          ExportXmlMetadataTool,
                          GetIARIDFromXmlTool,
                          ImportMetadataTool}

        self.tools = list(geodata_tools | feature_tools | raster_tools | metadata_tools)
