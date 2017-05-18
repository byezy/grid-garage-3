from base.base_tool import BaseTool
from base.results import result
from base.method_decorators import input_output_table, parameter
from base.utils import datatype_list
import arcpy
from os.path import join
import os
import csv
import tempfile
import codecs
import cStringIO
from xml.etree.ElementTree import ElementTree


tool_settings = {"label": "Search",
                 "description": "Search for identifiable geodata",
                 "can_run_background": "True",
                 "category": "Geodata"}


@result
class SearchGeodataTool(BaseTool):

    def __init__(self):

        BaseTool.__init__(self, tool_settings)

        self.execution_list = [self.iterate]

        return

    @parameter("workspaces", "Workspaces to Search", "DEWorkspace", "Required", True, "Input", None, None, None, None)
    @parameter("data_type", "Data Type", "GPString", "Required", True, "Input", datatype_list, None, None, None)
    @input_output_table
    def getParameterInfo(self):

        return BaseTool.getParameterInfo(self)

    def iterate(self):

        datatype = self.data_type.split(";")
        datatype = ["Any"] if "Any" in datatype else datatype
        self.data_type = datatype

        self.iterate_function_on_parameter(self.search, "workspaces", ["workspace"])

        return

    def search(self, data):

        workspace = data["workspace"].strip("'")

        if not arcpy.Exists(workspace):
            raise ValueError("Workspace '{}' does not exist".format(workspace))

        self.info("Searching for {} geodata types in {}".format(self.data_type, workspace))

        for root, dirs, files in arcpy.da.Walk(workspace, datatype=self.data_type, type=None, followlinks=True):
            for f in files:
                self.info(self.result.add({"geodata": join(root, f)}))

        #         x.append(os.path.join(root, f))
        # return x
        # found = [{"geodata": v} for v in walk(workspace, data_types=dt)]
        # if not found:
        #     self.log.info("Nothing found")
        # else:
        #     self.log.info(self.result.add(found))

        return



def ListWorkspaceContentsAndMetadata(workspace):
    """Generator function that lists the contents of the geodatabase including those within feature datasets.
       Certain metadata elements are also listed. Only geodatabases are supported, not folder workspaces."""

    if not arcpy.Exists(workspace):
        raise ValueError("Workspace %s does not exist!" % workspace)

    desc = arcpy.Describe(workspace)

    if not desc.dataType in ['Workspace', 'FeatureDataset']:
        if not hasattr(desc, "workspaceType") or not desc.workspaceType in ["LocalDatabase", "RemoteDatabase"]:
            raise ValueError("Workspace %s is not a geodatabase!" % workspace)

    children = desc.children
    if desc.dataType == 'FeatureDataset':
        validationWorkspace = os.path.dirname(workspace)
        fdsName = arcpy.ParseTableName(desc.name, validationWorkspace).split(",")[2].strip() # Get the short name of the feature dataset (sans database/owner name)
    else:
        validationWorkspace = workspace
        fdsName = ""

    for child in children:
        # Parse the full table name into database, owner, table name
        database, owner, tableName = [i.strip() if i.strip() != "(null)" else "" for i in arcpy.ParseTableName(child.name, validationWorkspace).split(",")]
        datasetType = child.datasetType if hasattr(child, "datasetType") else ""
        alias = child.aliasName if hasattr(child, "aliasName") else ""
        outrow = [owner, tableName, alias, fdsName, datasetType]
        try:
            outrow.extend(GetMetadataItems(child.catalogPath))
        except:
            pass
        print ",".join(outrow)
        yield outrow

        # Recurse to get the contents of feature datasets
        if datasetType == 'FeatureDataset':
            for outrow in ListWorkspaceContentsAndMetadata(child.catalogPath):
                yield outrow


def WriteCSVFile(csvfile, rows, header=None):
    """Creates a CSV file from the input header and row sequences"""
    with open(csvfile, 'wb') as f:
        f.write(codecs.BOM_UTF8) # Write Byte Order Mark character so Excel knows this is a UTF-8 file
        w = UnicodeWriter(f, dialect='excel', encoding='utf-8')
        if header:
            w.writerow(header)
        w.writerows(rows)


def CreateHeaderRow():
    """Specifies the column names (header row) for the CSV file"""
    return ("OWNER", "TABLE_NAME", "ALIAS", "FEATURE_DATASET", "DATASET_TYPE", "ORIGINATOR", "CONTACT_ORG", "ABSTRACT", "PURPOSE", "SEARCH_KEYS", "THEME_KEYS")


def CreateDummyXMLFile():
    """Creates an XML file with the required root element 'metadata' in
    the user's temporary files directory. Returns the path to the file.
    The calling code is responsible for deleting the temporary file."""
    tempdir = tempfile.gettempdir()
    fd, filepath = tempfile.mkstemp(".xml", text=True)
    with os.fdopen(fd, "w") as f:
        f.write("<metadata />")
        f.close()
    return filepath


def GetMetadataElementTree(dataset):
    """Creates and returns an ElementTree object from the specified
    dataset's metadata"""
    xmlfile = CreateDummyXMLFile()
    arcpy.MetadataImporter_conversion(dataset, xmlfile)
    tree = ElementTree()
    tree.parse(xmlfile)
    os.remove(xmlfile)
    return tree


def GetElementText(tree, elementPath):
    """Returns the specified element's text if it exists or an empty
    string if not."""
    element = tree.find(elementPath)
    return element.text if element != None else ""


def GetFirstElementText(tree, elementPaths):
    """Returns the first found element matching one of the specified
    element paths"""
    result = ""
    for elementPath in elementPaths:
        element = tree.find(elementPath)
        if element != None:
            result = element.text
            break
    return result


def ListElementsText(tree, elementPath):
    """Returns a comma+space-separated list of the text values of all
    instances of the specified element, or an empty string if none are
    found."""
    elements = tree.findall(elementPath)
    if elements:
        return ", ".join([element.text for element in elements])
    else:
        return ""


def GetMetadataItems(dataset):
    """Retrieves certain metadata text elements from the specified dataset"""
    tree = GetMetadataElementTree(dataset)
    originator = GetElementText(tree, "idinfo/citation/citeinfo/origin") # Originator
    pocorg = GetFirstElementText(tree, ("idinfo/ptcontac/cntinfo/cntperp/cntorg", # Point of contact organization (person primary contact)
                                        "idinfo/ptcontac/cntinfo/cntorgp/cntorg")) # Point of contact organization (organization primary contact)
    abstract = GetElementText(tree, "idinfo/descript/abstract") # Abstract
    purpose = GetElementText(tree, "idinfo/descript/purpose") # Purpose
    searchkeys = ListElementsText(tree, "dataIdInfo/searchKeys/keyword") # Search keywords
    themekeys = ListElementsText(tree, "idinfo/keywords/theme/themekey") # Theme keywords
    del tree
    metadataItems = (originator, pocorg, abstract, purpose, searchkeys, themekeys)
    return metadataItems


class UnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)

