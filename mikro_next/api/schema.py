from mikro_next.traits import IsVectorizableTrait, HasDownloadAccessor, Lensable, MikroFetchable, HasParquetStoreAccesor, DatasetTrait, FileTrait, DataArrayTrait, CreateADatasetTrait, HasZarrStoreTrait, HasZarrStoreAccessor, HasParquestStoreTrait, HasPresignedDownloadAccessor
from mikro_next.funcs import subscribe, aexecute, asubscribe, execute
from mikro_next.scalars import ImageLike, FileLike, FiveDVector, Milliseconds, ThreeDVector, MeshCoercible, LabelsLike, ImageFileLike, Micrometers, ArrayLike, MeshLike, ParquetLike, ImageFileCoercible, ImageCoercible, ArrayCoercible, FourByFourMatrix, ParquetCoercible
from datetime import datetime
from pydantic import Field, BaseModel, ConfigDict
from rath.scalars import ID, IDCoercible
from typing import Iterator, Iterable, Tuple, AsyncIterator, Optional, Union, Literal, Any, Annotated, List
from enum import Enum
from mikro_next.rath import MikroNextRath

class Blending(str, Enum):
    """The blending mode used to combine multiple channels or layers into a composite image."""
    ADDITIVE = 'ADDITIVE'
    'Additive blending, where the color values of overlapping layers are summed.'
    MULTIPLICATIVE = 'MULTIPLICATIVE'
    'Multiplicative blending, where the color values of overlapping layers are multiplied.'

class ChannelKind(str, Enum):
    """No documentation"""
    FREE_SPACE = 'FREE_SPACE'
    FIBER_SM = 'FIBER_SM'
    FIBER_MM = 'FIBER_MM'
    WAVEGUIDE = 'WAVEGUIDE'

class ColorMap(str, Enum):
    """The colormap used to map intensity values of a channel to display colors."""
    VIRIDIS = 'VIRIDIS'
    'The perceptually uniform viridis colormap, ranging from dark purple to yellow.'
    PLASMA = 'PLASMA'
    'The perceptually uniform plasma colormap, ranging from dark blue to yellow.'
    INFERNO = 'INFERNO'
    'The perceptually uniform inferno colormap, ranging from black through red to yellow.'
    MAGMA = 'MAGMA'
    'The perceptually uniform magma colormap, ranging from black through purple to light yellow.'
    RED = 'RED'
    'A monochromatic colormap from black to pure red.'
    GREEN = 'GREEN'
    'A monochromatic colormap from black to pure green.'
    BLUE = 'BLUE'
    'A monochromatic colormap from black to pure blue.'
    INTENSITY = 'INTENSITY'
    'A grayscale colormap mapping intensity values directly to brightness.'
    CYAN = 'CYAN'
    'A monochromatic colormap from black to cyan.'
    MAGENTA = 'MAGENTA'
    'A monochromatic colormap from black to magenta.'
    YELLOW = 'YELLOW'
    'A monochromatic colormap from black to yellow.'
    BLACK = 'BLACK'
    'A colormap rendering all values as black.'
    WHITE = 'WHITE'
    'A monochromatic colormap from black to white.'
    ORANGE = 'ORANGE'
    'A monochromatic colormap from black to orange.'
    PURPLE = 'PURPLE'
    'A monochromatic colormap from black to purple.'
    PINK = 'PINK'
    'A monochromatic colormap from black to pink.'
    BROWN = 'BROWN'
    'A monochromatic colormap from black to brown.'
    GREY = 'GREY'
    'A grayscale colormap from black to white.'
    RAINBOW = 'RAINBOW'
    'A multi-hue rainbow colormap cycling through the visible spectrum.'
    SPECTRAL = 'SPECTRAL'
    'A diverging colormap spanning the spectral colors from red to blue.'
    COOL = 'COOL'
    'A colormap of cool tones ranging from cyan to magenta.'
    WARM = 'WARM'
    'A colormap of warm tones ranging from yellow to red.'

class DimensionKind(str, Enum):
    """No documentation"""
    SPACE = 'SPACE'
    CHANNEL = 'CHANNEL'
    TIME = 'TIME'
    FREQUENCY = 'FREQUENCY'

class ElementKind(str, Enum):
    """No documentation"""
    LASER = 'LASER'
    PINHOLE = 'PINHOLE'
    LAMP = 'LAMP'
    OTHER_SOURCE = 'OTHER_SOURCE'
    DETECTOR = 'DETECTOR'
    CCD = 'CCD'
    MIRROR = 'MIRROR'
    BEAM_SPLITTER = 'BEAM_SPLITTER'
    LENS = 'LENS'
    OBJECTIVE = 'OBJECTIVE'
    FILTER = 'FILTER'
    POLARIZER = 'POLARIZER'
    WAVEPLATE = 'WAVEPLATE'
    APERTURE = 'APERTURE'
    SHUTTER = 'SHUTTER'
    SAMPLE = 'SAMPLE'
    OTHER = 'OTHER'

class ImageKind(str, Enum):
    """No documentation"""
    MASK = 'MASK'
    VOXEL = 'VOXEL'
    RGB = 'RGB'
    UNKNOWN = 'UNKNOWN'

class ObjectiveImmersion(str, Enum):
    """No documentation"""
    OIL = 'OIL'
    WATER = 'WATER'
    WATER_DIPPING = 'WATER_DIPPING'
    AIR = 'AIR'
    MULTI = 'MULTI'
    GLYCEROL = 'GLYCEROL'
    OTHER = 'OTHER'

class PortRole(str, Enum):
    """No documentation"""
    INPUT = 'INPUT'
    OUTPUT = 'OUTPUT'

class PulseKind(str, Enum):
    """No documentation"""
    CW = 'CW'
    SINGLE = 'SINGLE'
    QSWITCHED = 'QSWITCHED'
    REPETITIVE = 'REPETITIVE'
    MODE_LOCKED = 'MODE_LOCKED'
    OTHER = 'OTHER'

class RenderNodeKind(str, Enum):
    """No documentation"""
    CONTEXT = 'CONTEXT'
    OVERLAY = 'OVERLAY'
    GRID = 'GRID'
    SPIT = 'SPIT'

class RoiKind(str, Enum):
    """The geometric kind of a region of interest (ROI), defining how its vectors are interpreted."""
    ELLIPSIS = 'ELLIPSIS'
    'An elliptical region in the XY plane.'
    POLYGON = 'POLYGON'
    'A closed polygon defined by a sequence of vertices.'
    LINE = 'LINE'
    'A straight line between two points.'
    RECTANGLE = 'RECTANGLE'
    'An axis-aligned rectangle in the XY plane.'
    SPECTRAL_RECTANGLE = 'SPECTRAL_RECTANGLE'
    'A rectangle extended along the channel axis (XYC).'
    TEMPORAL_RECTANGLE = 'TEMPORAL_RECTANGLE'
    'A rectangle extended along the time axis (XYT).'
    CUBE = 'CUBE'
    'A three-dimensional cuboid spanning the spatial axes (XYZ).'
    SPECTRAL_CUBE = 'SPECTRAL_CUBE'
    'A cuboid extended along the channel axis (XYZC).'
    TEMPORAL_CUBE = 'TEMPORAL_CUBE'
    'A cuboid extended along the time axis (XYZT).'
    HYPERCUBE = 'HYPERCUBE'
    'A four-dimensional region spanning space and time (XYZT).'
    SPECTRAL_HYPERCUBE = 'SPECTRAL_HYPERCUBE'
    'A five-dimensional region spanning space, time and channels (XYZTC).'
    PATH = 'PATH'
    'An open path defined by a sequence of connected points.'
    FRAME = 'FRAME'
    'A single frame of the image, e.g. one timepoint.'
    SLICE = 'SLICE'
    'A single slice of the image, e.g. one Z plane.'
    POINT = 'POINT'
    'A single point.'

class ScanDirection(str, Enum):
    """The axis traversal order of a continuous scan, i.e. the order in which rows, columns and slices are acquired."""
    ROW_COLUMN_SLICE = 'ROW_COLUMN_SLICE'
    'Scan rows first, then columns, then slices (Row -> Column -> Slice).'
    COLUMN_ROW_SLICE = 'COLUMN_ROW_SLICE'
    'Scan columns first, then rows, then slices (Column -> Row -> Slice).'
    SLICE_ROW_COLUMN = 'SLICE_ROW_COLUMN'
    'Scan slices first, then rows, then columns (Slice -> Row -> Column).'
    ROW_COLUMN_SLICE_SNAKE = 'ROW_COLUMN_SLICE_SNAKE'
    'Scan rows, then columns, then slices, reversing direction on alternate lines (Row -> Column -> Slice, snake).'
    COLUMN_ROW_SLICE_SNAKE = 'COLUMN_ROW_SLICE_SNAKE'
    'Scan columns, then rows, then slices, reversing direction on alternate lines (Column -> Row -> Slice, snake).'
    SLICE_ROW_COLUMN_SNAKE = 'SLICE_ROW_COLUMN_SNAKE'
    'Scan slices, then rows, then columns, reversing direction on alternate lines (Slice -> Row -> Column, snake).'

class ScopeKind(str, Enum):
    """The visibility scope of an object, determining which users can see it."""
    PUBLIC = 'PUBLIC'
    'The object is visible to everyone.'
    ORG = 'ORG'
    'The object is visible to everyone in the organization.'
    SHARED = 'SHARED'
    'The object is visible only to users it was explicitly shared with.'
    ME = 'ME'
    'The object is visible only to its creator.'

class SpatialUnit(str, Enum):
    """The physical unit used to express spatial dimensions, e.g. of pixel sizes or stage positions."""
    MICROMETERS = 'MICROMETERS'
    'Micrometers (1e-6 meters), the typical scale of cells in light microscopy.'
    NANOMETERS = 'NANOMETERS'
    'Nanometers (1e-9 meters), the typical scale of subcellular structures.'
    ANGSTROMS = 'ANGSTROMS'
    'Angstroms (1e-10 meters), the typical scale of atomic and molecular structures.'
    PIXELS = 'PIXELS'
    'Raw pixel units without a calibrated physical size.'
    UNKNOWN = 'UNKNOWN'
    'The spatial unit is not known or not specified.'

class TemporalUnit(str, Enum):
    """The physical unit used to express temporal dimensions, e.g. of time-lapse intervals."""
    NANOSECONDS = 'NANOSECONDS'
    'Nanoseconds (1e-9 seconds).'
    MILLISECONDS = 'MILLISECONDS'
    'Milliseconds (1e-3 seconds).'
    SECONDS = 'SECONDS'
    'Seconds, the SI base unit of time.'
    MINUTES = 'MINUTES'
    'Minutes (60 seconds).'
    HOURS = 'HOURS'
    'Hours (3600 seconds).'
    DAYS = 'DAYS'
    'Days (86400 seconds).'
    UNKNOWN = 'UNKNOWN'
    'The temporal unit is not known or not specified.'

class AffineTransformationViewFilter(BaseModel):
    """No documentation"""
    ids: Optional[Tuple[ID, ...]] = None
    'Filter by list of IDs'
    is_global: Optional[bool] = Field(alias='isGlobal', default=None)
    image: Optional[ID] = None
    'Filter by the image this view belongs to'
    images: Optional[Tuple[ID, ...]] = None
    'Filter by a list of images this view belongs to'
    search: Optional[str] = None
    'Search by the name of the image this view belongs to'
    id: Optional[ID] = None
    stage: Optional['StageFilter'] = None
    and_: Optional['AffineTransformationViewFilter'] = Field(alias='AND', default=None)
    or_: Optional['AffineTransformationViewFilter'] = Field(alias='OR', default=None)
    not_: Optional['AffineTransformationViewFilter'] = Field(alias='NOT', default=None)
    distinct: Optional[bool] = Field(alias='DISTINCT', default=None)
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class BeamStateInput(BaseModel):
    """State of the optical beam on a particular path segment."""
    wavelength_nm: Optional[float] = Field(alias='wavelengthNm', default=None)
    power_mw: Optional[float] = Field(alias='powerMw', default=None)
    polarization: Optional[str] = None
    mode_hint: Optional[str] = Field(alias='modeHint', default=None)
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class CameraInput(BaseModel):
    """Input for creating or ensuring a camera"""
    serial_number: str = Field(alias='serialNumber')
    'The unique serial number of the camera'
    name: Optional[str] = None
    'The name of the camera'
    model: Optional[str] = None
    'The model of the camera'
    bit_depth: Optional[int] = Field(alias='bitDepth', default=None)
    'The bit depth of the camera sensor'
    sensor_size_x: Optional[int] = Field(alias='sensorSizeX', default=None)
    'The sensor size in x direction (pixels)'
    sensor_size_y: Optional[int] = Field(alias='sensorSizeY', default=None)
    'The sensor size in y direction (pixels)'
    pixel_size_x: Optional[Micrometers] = Field(alias='pixelSizeX', default=None)
    'The physical pixel size in x direction (micrometers)'
    pixel_size_y: Optional[Micrometers] = Field(alias='pixelSizeY', default=None)
    'The physical pixel size in y direction (micrometers)'
    manufacturer: Optional[str] = None
    'The manufacturer of the camera'
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class ChangeDatasetInput(BaseModel):
    """Input for changing an existing dataset's name or parent"""
    name: str
    'The name of the dataset'
    parent: Optional[ID] = None
    'The ID of the parent dataset to nest this dataset under'
    id: ID
    'The ID of the dataset to change'
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class CoordinateAnchorInput(BaseModel):
    """Input type for a coordinate anchor, which specifies a list of dimension anchors to anchor to"""
    dim_anchors: Tuple['DimAnchorInput', ...] = Field(alias='dimAnchors')
    ome_metadata: Optional['OmeMetadataInput'] = Field(alias='omeMetadata', default=None)
    value_histogram: Optional['ValueHistogramInput'] = Field(alias='valueHistogram', default=None)
    label: Optional['LabelInput'] = None
    light_graph: Optional['LightpathGraphInput'] = Field(alias='lightGraph', default=None)
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class CreateADatasetInput(CreateADatasetTrait, BaseModel):
    """Input type for creating an image from an array-like object"""
    data: ArrayLike
    scales: Tuple['ScaleInput', ...]
    name: str
    dim_descriptors: Tuple['DimensionDescriptorInput', ...] = Field(alias='dimDescriptors')
    anchors: Optional[Tuple[CoordinateAnchorInput, ...]] = None
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class CreateDataRoiInput(BaseModel):
    """Input type for creating an image from an array-like object"""
    dataset: ID
    kind: RoiKind
    x_dim: str = Field(alias='xDim')
    y_dim: str = Field(alias='yDim')
    z_dim: Optional[str] = Field(alias='zDim', default=None)
    vectors: Tuple[ThreeDVector, ...]
    slices: Tuple['SliceInput', ...]
    drawn_on_lens: Optional[ID] = Field(alias='drawnOnLens', default=None)
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class CreateDatasetInput(BaseModel):
    """Input for creating a new dataset to organize images and files"""
    name: str
    'The name of the dataset'
    parent: Optional[ID] = None
    'The ID of the parent dataset to nest this dataset under'
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class CreateLayerInput(BaseModel):
    """Input type for creating an image from an array-like object"""
    lens: ID
    scene: ID
    affine_matrix: Optional[Tuple[Tuple[float, ...], ...]] = Field(alias='affineMatrix', default=None)
    colormap: Optional[ColorMap] = None
    color: Optional[Tuple[int, ...]] = None
    clim_min: Optional[float] = Field(alias='climMin', default=None)
    clim_max: Optional[float] = Field(alias='climMax', default=None)
    x_dim: Optional[str] = Field(alias='xDim', default=None)
    y_dim: Optional[str] = Field(alias='yDim', default=None)
    z_dim: Optional[str] = Field(alias='zDim', default=None)
    t_dim: Optional[str] = Field(alias='tDim', default=None)
    intensity_dim: Optional[str] = Field(alias='intensityDim', default=None)
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class CreateLensInput(BaseModel):
    """Input type for creating an image from an array-like object"""
    dataset: ID
    slices: Tuple['SliceInput', ...]
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class CreateRGBContextInput(BaseModel):
    """Input for creating an RGB render context for an image"""
    name: Optional[str] = None
    'The name of the RGB context'
    thumbnail: Optional[ID] = None
    'The ID of an uploaded media store to use as the thumbnail snapshot'
    image: ID
    'The ID of the image this RGB context renders'
    views: Optional[Tuple['PartialRGBViewInput', ...]] = None
    'The RGB views (channel rendering settings) to attach to the context'
    z: Optional[int] = None
    'The z plane the context renders'
    t: Optional[int] = None
    'The timepoint the context renders'
    c: Optional[int] = None
    'The channel the context renders'
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class CreateSceneInput(BaseModel):
    """Input type for creating a scene from an array-like object"""
    name: str
    blending: Optional[Blending] = None
    spatial_unit: Optional[SpatialUnit] = Field(alias='spatialUnit', default=None)
    temporal_unit: Optional[TemporalUnit] = Field(alias='temporalUnit', default=None)
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class DatasetFilter(BaseModel):
    """No documentation"""
    ids: Optional[Tuple[ID, ...]] = None
    'Filter by list of IDs'
    search: Optional[str] = None
    'Search by name (full-text search)'
    created_before: Optional[datetime] = Field(alias='createdBefore', default=None)
    'Filter for items created before this datetime'
    created_after: Optional[datetime] = Field(alias='createdAfter', default=None)
    'Filter for items created after this datetime'
    owner: Optional[ID] = None
    "Filter by the creator's subject ID"
    scope: Optional[ScopeKind] = None
    'Filter by visibility scope'
    pinned: Optional[bool] = None
    'Filter by whether the current user has pinned the item'
    tags: Optional[Tuple[str, ...]] = None
    'Filter by tag names'
    created_through_task: Optional[str] = Field(alias='createdThroughTask', default=None)
    'Filter by the rekuest task id the item was created through'
    created_through: Optional[ID] = Field(alias='createdThrough', default=None)
    'Filter by the database ID of the task the item was created through (the `createdThrough { id }` field)'
    assigned_by: Optional[ID] = Field(alias='assignedBy', default=None)
    'Filter by the sub of the user that assigned the creating task'
    created_through_by: Optional[ID] = Field(alias='createdThroughBy', default=None)
    'Filter by the database ID of the user that assigned the creating task (the `createdThroughBy { id }` field)'
    id: Optional[ID] = None
    name: Optional['StrFilterLookup'] = None
    description: Optional['StrFilterLookup'] = None
    is_default: Optional[bool] = Field(alias='isDefault', default=None)
    and_: Optional['DatasetFilter'] = Field(alias='AND', default=None)
    or_: Optional['DatasetFilter'] = Field(alias='OR', default=None)
    not_: Optional['DatasetFilter'] = Field(alias='NOT', default=None)
    distinct: Optional[bool] = Field(alias='DISTINCT', default=None)
    parentless: Optional[bool] = None
    'Filter for datasets with (true) or without (false) a parent'
    parent: Optional[ID] = None
    'Filter by the parent dataset (list the children of a dataset)'
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class DeleteRoiInput(BaseModel):
    """Input for deleting a ROI by ID"""
    id: ID
    'The ID of the ROI to delete'
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class DimAnchorInput(BaseModel):
    """Input type for a dimension anchor, which specifies a dimension and a value to anchor to"""
    dim: str
    value: int
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class DimensionDescriptorInput(BaseModel):
    """Input type for a dimension descriptor, which specifies a key and a kind for a dimension"""
    key: str
    kind: str
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class EraFilter(BaseModel):
    """No documentation"""
    ids: Optional[Tuple[ID, ...]] = None
    'Filter by list of IDs'
    search: Optional[str] = None
    'Search by name (case-insensitive substring)'
    created_before: Optional[datetime] = Field(alias='createdBefore', default=None)
    'Filter for items created before this datetime'
    created_after: Optional[datetime] = Field(alias='createdAfter', default=None)
    'Filter for items created after this datetime'
    owner: Optional[ID] = None
    "Filter by the creator's subject ID"
    pinned: Optional[bool] = None
    'Filter by whether the current user has pinned the item'
    created_through_task: Optional[str] = Field(alias='createdThroughTask', default=None)
    'Filter by the rekuest task id the item was created through'
    created_through: Optional[ID] = Field(alias='createdThrough', default=None)
    'Filter by the database ID of the task the item was created through (the `createdThrough { id }` field)'
    assigned_by: Optional[ID] = Field(alias='assignedBy', default=None)
    'Filter by the sub of the user that assigned the creating task'
    created_through_by: Optional[ID] = Field(alias='createdThroughBy', default=None)
    'Filter by the database ID of the user that assigned the creating task (the `createdThroughBy { id }` field)'
    id: Optional[ID] = None
    name: Optional['StrFilterLookup'] = None
    begin: Optional[datetime] = None
    end: Optional[datetime] = None
    and_: Optional['EraFilter'] = Field(alias='AND', default=None)
    or_: Optional['EraFilter'] = Field(alias='OR', default=None)
    not_: Optional['EraFilter'] = Field(alias='NOT', default=None)
    distinct: Optional[bool] = Field(alias='DISTINCT', default=None)
    instrument: Optional[ID] = None
    'Filter by the instrument this era belongs to'
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class EraInput(BaseModel):
    """Input for creating an era, a time period to which timepoint views relate"""
    name: str
    'The name of the era'
    begin: Optional[datetime] = None
    'The datetime at which the era begins'
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class EulerInput(BaseModel):
    """Euler angles representing rotation in 3D space."""
    rx: Optional[float] = None
    ry: Optional[float] = None
    rz: Optional[float] = None
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class FinishBigFileUploadInput(BaseModel):
    """No documentation"""
    store_id: str = Field(alias='storeId')
    valid: bool
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class FinishMediaUploadInput(BaseModel):
    """No documentation"""
    store_id: str = Field(alias='storeId')
    valid: bool
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class FinishParquetUploadInput(BaseModel):
    """No documentation"""
    store_id: str = Field(alias='storeId')
    valid: bool
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class FinishZarrUploadInput(BaseModel):
    """No documentation"""
    store_id: str = Field(alias='storeId')
    valid: bool
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class FromArrayLikeInput(BaseModel):
    """Input type for creating an image from an array-like object"""
    array: ImageLike
    'The array-like object to create the image from'
    name: str
    'The name of the image'
    dataset: Optional[ID] = None
    'Optional dataset ID to associate the image with'
    channel_views: Optional[Tuple['PartialChannelViewInput', ...]] = Field(alias='channelViews', default=None)
    'Optional list of channel views'
    transformation_views: Optional[Tuple['PartialAffineTransformationViewInput', ...]] = Field(alias='transformationViews', default=None)
    'Optional list of affine transformation views'
    acquisition_views: Optional[Tuple['PartialAcquisitionViewInput', ...]] = Field(alias='acquisitionViews', default=None)
    'Optional list of acquisition views'
    mask_views: Optional[Tuple['PartialMaskViewInput', ...]] = Field(alias='maskViews', default=None)
    'Optional list of mask views'
    reference_views: Optional[Tuple['PartialReferenceViewInput', ...]] = Field(alias='referenceViews', default=None)
    'Optional list of reference views'
    instance_mask_views: Optional[Tuple['PartialInstanceMaskViewInput', ...]] = Field(alias='instanceMaskViews', default=None)
    'Optional list of instance mask views'
    rgb_views: Optional[Tuple['PartialRGBViewInput', ...]] = Field(alias='rgbViews', default=None)
    'Optional list of RGB views'
    timepoint_views: Optional[Tuple['PartialTimepointViewInput', ...]] = Field(alias='timepointViews', default=None)
    'Optional list of timepoint views'
    optics_views: Optional[Tuple['PartialOpticsViewInput', ...]] = Field(alias='opticsViews', default=None)
    'Optional list of optics views'
    scale_views: Optional[Tuple['PartialScaleViewInput', ...]] = Field(alias='scaleViews', default=None)
    'Optional list of scale views'
    tags: Optional[Tuple[str, ...]] = None
    'Optional list of tags to associate with the image'
    roi_views: Optional[Tuple['PartialROIViewInput', ...]] = Field(alias='roiViews', default=None)
    'Optional list of ROI views'
    file_views: Optional[Tuple['PartialFileViewInput', ...]] = Field(alias='fileViews', default=None)
    'Optional list of file views'
    derived_views: Optional[Tuple['PartialDerivedViewInput', ...]] = Field(alias='derivedViews', default=None)
    'Optional list of derived views'
    lightpath_views: Optional[Tuple['PartialLightpathViewInput', ...]] = Field(alias='lightpathViews', default=None)
    'Optional list of lightpath views'
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class FromFileLike(BaseModel):
    """Input for creating a file record from an uploaded big-file store"""
    file: FileLike
    'The uploaded big-file store to create the file from'
    file_name: str = Field(alias='fileName')
    'The name of the file'
    dataset: Optional[ID] = None
    'The ID of the dataset to put the file in (defaults to the current default dataset)'
    origins: Optional[Tuple[ID, ...]] = None
    'The IDs of entities this file was derived from'
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class FromParquetLike(BaseModel):
    """Input for creating a table from an uploaded parquet store"""
    dataframe: ParquetLike
    'The parquet dataframe to create the table from'
    name: str
    'The name of the table'
    origins: Optional[Tuple[ID, ...]] = None
    'The IDs of tables this table was derived from'
    dataset: Optional[ID] = None
    'The dataset ID this table belongs to'
    label_accessors: Optional[Tuple['PartialLabelAccessorInput', ...]] = Field(alias='labelAccessors', default=None)
    'Label accessors to create for this table'
    image_accessors: Optional[Tuple['PartialImageAccessorInput', ...]] = Field(alias='imageAccessors', default=None)
    'Image accessors to create for this table'
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class HistogramViewInput(BaseModel):
    """Input for creating a histogram view on an existing image, referenced by ID"""
    collection: Optional[ID] = None
    'The collection this view belongs to'
    z_min: Optional[int] = Field(alias='zMin', default=None)
    'The minimum z coordinate of the view'
    z_max: Optional[int] = Field(alias='zMax', default=None)
    'The maximum z coordinate of the view'
    x_min: Optional[int] = Field(alias='xMin', default=None)
    'The minimum x coordinate of the view'
    x_max: Optional[int] = Field(alias='xMax', default=None)
    'The maximum x coordinate of the view'
    y_min: Optional[int] = Field(alias='yMin', default=None)
    'The minimum y coordinate of the view'
    y_max: Optional[int] = Field(alias='yMax', default=None)
    'The maximum y coordinate of the view'
    t_min: Optional[int] = Field(alias='tMin', default=None)
    'The minimum t coordinate of the view'
    t_max: Optional[int] = Field(alias='tMax', default=None)
    'The maximum t coordinate of the view'
    c_min: Optional[int] = Field(alias='cMin', default=None)
    'The minimum c (channel) coordinate of the view'
    c_max: Optional[int] = Field(alias='cMax', default=None)
    'The maximum c (channel) coordinate of the view'
    histogram: Tuple[float, ...]
    'The histogram of the image (y values)'
    bins: Tuple[float, ...]
    'The bin indices of the histogram (x values)'
    min: float
    'The minimum pixel value of the histogram'
    max: float
    'The maximum pixel value of the histogram'
    image: ID
    'The ID of the image this view is for'
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class ImageFilter(BaseModel):
    """No documentation"""
    ids: Optional[Tuple[ID, ...]] = None
    'Filter by list of IDs'
    search: Optional[str] = None
    'Search by name (full-text search)'
    created_before: Optional[datetime] = Field(alias='createdBefore', default=None)
    'Filter for items created before this datetime'
    created_after: Optional[datetime] = Field(alias='createdAfter', default=None)
    'Filter for items created after this datetime'
    owner: Optional[ID] = None
    "Filter by the creator's subject ID"
    scope: Optional[ScopeKind] = None
    'Filter by visibility scope'
    pinned: Optional[bool] = None
    'Filter by whether the current user has pinned the item'
    tags: Optional[Tuple[str, ...]] = None
    'Filter by tag names'
    created_through_task: Optional[str] = Field(alias='createdThroughTask', default=None)
    'Filter by the rekuest task id the item was created through'
    created_through: Optional[ID] = Field(alias='createdThrough', default=None)
    'Filter by the database ID of the task the item was created through (the `createdThrough { id }` field)'
    assigned_by: Optional[ID] = Field(alias='assignedBy', default=None)
    'Filter by the sub of the user that assigned the creating task'
    created_through_by: Optional[ID] = Field(alias='createdThroughBy', default=None)
    'Filter by the database ID of the user that assigned the creating task (the `createdThroughBy { id }` field)'
    id: Optional[ID] = None
    name: Optional['StrFilterLookup'] = None
    description: Optional['StrFilterLookup'] = None
    kind: Optional[ImageKind] = None
    store: Optional['ZarrStoreFilter'] = None
    dataset: Optional[DatasetFilter] = None
    transformation_views: Optional[AffineTransformationViewFilter] = Field(alias='transformationViews', default=None)
    timepoint_views: Optional['TimepointViewFilter'] = Field(alias='timepointViews', default=None)
    and_: Optional['ImageFilter'] = Field(alias='AND', default=None)
    or_: Optional['ImageFilter'] = Field(alias='OR', default=None)
    not_: Optional['ImageFilter'] = Field(alias='NOT', default=None)
    distinct: Optional[bool] = Field(alias='DISTINCT', default=None)
    datasets: Optional[Tuple[ID, ...]] = None
    'Filter by a list of dataset IDs'
    not_derived: Optional[bool] = Field(alias='notDerived', default=None)
    'Filter for images that are not derived from another image'
    has_rois: Optional[bool] = Field(alias='hasRois', default=None)
    'Filter for images that have (or have no) ROIs'
    file: Optional[ID] = None
    'Filter for images converted from this file (through their file views)'
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class InstanceMaskViewInput(BaseModel):
    """Input for creating an instance mask view on an existing image, referenced by ID"""
    collection: Optional[ID] = None
    'The collection this view belongs to'
    z_min: Optional[int] = Field(alias='zMin', default=None)
    'The minimum z coordinate of the view'
    z_max: Optional[int] = Field(alias='zMax', default=None)
    'The maximum z coordinate of the view'
    x_min: Optional[int] = Field(alias='xMin', default=None)
    'The minimum x coordinate of the view'
    x_max: Optional[int] = Field(alias='xMax', default=None)
    'The maximum x coordinate of the view'
    y_min: Optional[int] = Field(alias='yMin', default=None)
    'The minimum y coordinate of the view'
    y_max: Optional[int] = Field(alias='yMax', default=None)
    'The maximum y coordinate of the view'
    t_min: Optional[int] = Field(alias='tMin', default=None)
    'The minimum t coordinate of the view'
    t_max: Optional[int] = Field(alias='tMax', default=None)
    'The maximum t coordinate of the view'
    c_min: Optional[int] = Field(alias='cMin', default=None)
    'The minimum c (channel) coordinate of the view'
    c_max: Optional[int] = Field(alias='cMax', default=None)
    'The maximum c (channel) coordinate of the view'
    reference_view: Optional[ID] = Field(alias='referenceView', default=None)
    'The ID of the view that is masked by this instance mask'
    labels: Optional[LabelsLike] = None
    'The instance labels of the mask and their corresponding colors'
    image: ID
    'The ID of the image this view is for'
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class InstrumentInput(BaseModel):
    """Input for creating or ensuring a microscope instrument"""
    serial_number: str = Field(alias='serialNumber')
    'The unique serial number of the instrument'
    manufacturer: Optional[str] = None
    'The manufacturer of the instrument'
    name: Optional[str] = None
    'The name of the instrument'
    model: Optional[str] = None
    'The model of the instrument'
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class IntFilterLookup(BaseModel):
    """No documentation"""
    exact: Optional[int] = None
    i_exact: Optional[int] = Field(alias='iExact', default=None)
    contains: Optional[int] = None
    i_contains: Optional[int] = Field(alias='iContains', default=None)
    in_list: Optional[Tuple[int, ...]] = Field(alias='inList', default=None)
    gt: Optional[int] = None
    gte: Optional[int] = None
    lt: Optional[int] = None
    lte: Optional[int] = None
    starts_with: Optional[int] = Field(alias='startsWith', default=None)
    i_starts_with: Optional[int] = Field(alias='iStartsWith', default=None)
    ends_with: Optional[int] = Field(alias='endsWith', default=None)
    i_ends_with: Optional[int] = Field(alias='iEndsWith', default=None)
    range: Optional[Tuple[int, ...]] = None
    is_null: Optional[bool] = Field(alias='isNull', default=None)
    regex: Optional[str] = None
    i_regex: Optional[str] = Field(alias='iRegex', default=None)
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class LabelInput(BaseModel):
    """Input type for a label, which specifies a label to associate with a coordinate anchor or an image"""
    label: str
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class LightEdgeInput(BaseModel):
    """Input for connecting two optical ports."""
    id: str
    source_element_id: ID = Field(alias='sourceElementId')
    source_port_id: ID = Field(alias='sourcePortId')
    target_element_id: ID = Field(alias='targetElementId')
    target_port_id: ID = Field(alias='targetPortId')
    path_length_mm: Optional[float] = Field(alias='pathLengthMm', default=None)
    medium: Optional[str] = None
    loss_db: Optional[float] = Field(alias='lossDb', default=None)
    beam: Optional[BeamStateInput] = None
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class LightPortInput(BaseModel):
    """Input definition for an optical port on an element."""
    id: ID
    name: str
    role: PortRole
    channel: ChannelKind
    spectrum: Optional['SpectrumInput'] = None
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class LightpathGraphInput(BaseModel):
    """Bulk input for a full lightpath graph, including elements and edges."""
    elements: Tuple['OpticalElementInput', ...]
    edges: Tuple[LightEdgeInput, ...]
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class MaskViewInput(BaseModel):
    """Input for creating a mask view on an existing image, referenced by ID"""
    collection: Optional[ID] = None
    'The collection this view belongs to'
    z_min: Optional[int] = Field(alias='zMin', default=None)
    'The minimum z coordinate of the view'
    z_max: Optional[int] = Field(alias='zMax', default=None)
    'The maximum z coordinate of the view'
    x_min: Optional[int] = Field(alias='xMin', default=None)
    'The minimum x coordinate of the view'
    x_max: Optional[int] = Field(alias='xMax', default=None)
    'The maximum x coordinate of the view'
    y_min: Optional[int] = Field(alias='yMin', default=None)
    'The minimum y coordinate of the view'
    y_max: Optional[int] = Field(alias='yMax', default=None)
    'The maximum y coordinate of the view'
    t_min: Optional[int] = Field(alias='tMin', default=None)
    'The minimum t coordinate of the view'
    t_max: Optional[int] = Field(alias='tMax', default=None)
    'The maximum t coordinate of the view'
    c_min: Optional[int] = Field(alias='cMin', default=None)
    'The minimum c (channel) coordinate of the view'
    c_max: Optional[int] = Field(alias='cMax', default=None)
    'The maximum c (channel) coordinate of the view'
    reference_view: Optional[ID] = Field(alias='referenceView', default=None)
    'The ID of the view that is masked by this mask'
    labels: Optional[LabelsLike] = None
    'The labels of the mask and their corresponding colors'
    image: ID
    'The ID of the image this view is for'
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class MeshInput(BaseModel):
    """Input for creating a 3D mesh from an uploaded mesh file"""
    mesh: MeshLike
    'The uploaded mesh file store to create the mesh from'
    name: str
    'The name of the mesh'
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class ObjectiveInput(BaseModel):
    """Input for creating or ensuring a microscope objective"""
    serial_number: str = Field(alias='serialNumber')
    'The unique serial number of the objective'
    name: Optional[str] = None
    'The name of the objective'
    na: Optional[float] = None
    'The numerical aperture of the objective'
    magnification: Optional[float] = None
    'The magnification of the objective'
    immersion: Optional[str] = None
    'The immersion medium of the objective (e.g. oil, water, air)'
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class OffsetPaginationInput(BaseModel):
    """No documentation"""
    offset: int
    limit: Optional[int] = None
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class OmeMetadataInput(BaseModel):
    """Input type for OME metadata"""
    metadata_string: str = Field(alias='metadataString')
    'The OME metadata as a JSON string'
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class OpticalElementInput(BaseModel):
    """Input for creating or updating any optical element. Fill only fields relevant to the chosen `kind`."""
    id: ID
    label: str
    kind: ElementKind
    pose: Optional['Pose3DInput'] = None
    ports: Tuple[LightPortInput, ...]
    manufacturer: Optional[str] = None
    model: Optional[str] = None
    serial_number: Optional[str] = Field(alias='serialNumber', default=None)
    nominal_wavelength_nm: Optional[float] = Field(alias='nominalWavelengthNm', default=None)
    channel: Optional[ChannelKind] = None
    diameter_um: Optional[float] = Field(alias='diameterUm', default=None)
    nepd_w_per_sqrt_hz: Optional[float] = Field(alias='nepdWPerSqrtHz', default=None)
    angle_deg: Optional[float] = Field(alias='angleDeg', default=None)
    band_min_nm: Optional[float] = Field(alias='bandMinNm', default=None)
    band_max_nm: Optional[float] = Field(alias='bandMaxNm', default=None)
    r_fraction: Optional[float] = Field(alias='rFraction', default=None)
    t_fraction: Optional[float] = Field(alias='tFraction', default=None)
    focal_length_mm: Optional[float] = Field(alias='focalLengthMm', default=None)
    magnification: Optional[float] = None
    numerical_aperture: Optional[float] = Field(alias='numericalAperture', default=None)
    brand: Optional[str] = None
    working_distance_mm: Optional[float] = Field(alias='workingDistanceMm', default=None)
    immersion_medium: Optional[ObjectiveImmersion] = Field(alias='immersionMedium', default=None)
    iris: Optional[bool] = None
    amplifier_gain_db: Optional[float] = Field(alias='amplifierGainDb', default=None)
    gain: Optional[float] = None
    pixel_size_um: Optional[float] = Field(alias='pixelSizeUm', default=None)
    resolution: Optional[Tuple[int, ...]] = None
    power_mw: Optional[float] = Field(alias='powerMw', default=None)
    laser_medium: Optional[str] = Field(alias='laserMedium', default=None)
    pulse_kind: Optional[PulseKind] = Field(alias='pulseKind', default=None)
    repetition_rate_hz: Optional[float] = Field(alias='repetitionRateHz', default=None)
    has_pockels_cell: Optional[bool] = Field(alias='hasPockelsCell', default=None)
    has_q_switch: Optional[bool] = Field(alias='hasQSwitch', default=None)
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class PartialAcquisitionViewInput(BaseModel):
    """Input for creating an acquisition view (when and by whom the image was acquired) as part of creating an image; the image is taken from the surrounding input"""
    collection: Optional[ID] = None
    'The collection this view belongs to'
    z_min: Optional[int] = Field(alias='zMin', default=None)
    'The minimum z coordinate of the view'
    z_max: Optional[int] = Field(alias='zMax', default=None)
    'The maximum z coordinate of the view'
    x_min: Optional[int] = Field(alias='xMin', default=None)
    'The minimum x coordinate of the view'
    x_max: Optional[int] = Field(alias='xMax', default=None)
    'The maximum x coordinate of the view'
    y_min: Optional[int] = Field(alias='yMin', default=None)
    'The minimum y coordinate of the view'
    y_max: Optional[int] = Field(alias='yMax', default=None)
    'The maximum y coordinate of the view'
    t_min: Optional[int] = Field(alias='tMin', default=None)
    'The minimum t coordinate of the view'
    t_max: Optional[int] = Field(alias='tMax', default=None)
    'The maximum t coordinate of the view'
    c_min: Optional[int] = Field(alias='cMin', default=None)
    'The minimum c (channel) coordinate of the view'
    c_max: Optional[int] = Field(alias='cMax', default=None)
    'The maximum c (channel) coordinate of the view'
    description: Optional[str] = None
    'A cleartext description of the image acquisition'
    acquired_at: Optional[datetime] = Field(alias='acquiredAt', default=None)
    'The time the image was acquired'
    operator: Optional[ID] = None
    'The ID of the user that acquired the image'
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class PartialAffineTransformationViewInput(BaseModel):
    """Input for creating an affine transformation view (mapping the image onto a stage) as part of creating an image; the image is taken from the surrounding input"""
    collection: Optional[ID] = None
    'The collection this view belongs to'
    z_min: Optional[int] = Field(alias='zMin', default=None)
    'The minimum z coordinate of the view'
    z_max: Optional[int] = Field(alias='zMax', default=None)
    'The maximum z coordinate of the view'
    x_min: Optional[int] = Field(alias='xMin', default=None)
    'The minimum x coordinate of the view'
    x_max: Optional[int] = Field(alias='xMax', default=None)
    'The maximum x coordinate of the view'
    y_min: Optional[int] = Field(alias='yMin', default=None)
    'The minimum y coordinate of the view'
    y_max: Optional[int] = Field(alias='yMax', default=None)
    'The maximum y coordinate of the view'
    t_min: Optional[int] = Field(alias='tMin', default=None)
    'The minimum t coordinate of the view'
    t_max: Optional[int] = Field(alias='tMax', default=None)
    'The maximum t coordinate of the view'
    c_min: Optional[int] = Field(alias='cMin', default=None)
    'The minimum c (channel) coordinate of the view'
    c_max: Optional[int] = Field(alias='cMax', default=None)
    'The maximum c (channel) coordinate of the view'
    stage: Optional[ID] = None
    'The ID of the stage this transformation maps the image onto'
    affine_matrix: FourByFourMatrix = Field(alias='affineMatrix')
    'The 4x4 affine matrix mapping image coordinates to stage coordinates'
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class PartialChannelViewInput(BaseModel):
    """Input for creating a channel view (channel metadata such as name and wavelengths) as part of creating an image; the image is taken from the surrounding input"""
    collection: Optional[ID] = None
    'The collection this view belongs to'
    z_min: Optional[int] = Field(alias='zMin', default=None)
    'The minimum z coordinate of the view'
    z_max: Optional[int] = Field(alias='zMax', default=None)
    'The maximum z coordinate of the view'
    x_min: Optional[int] = Field(alias='xMin', default=None)
    'The minimum x coordinate of the view'
    x_max: Optional[int] = Field(alias='xMax', default=None)
    'The maximum x coordinate of the view'
    y_min: Optional[int] = Field(alias='yMin', default=None)
    'The minimum y coordinate of the view'
    y_max: Optional[int] = Field(alias='yMax', default=None)
    'The maximum y coordinate of the view'
    t_min: Optional[int] = Field(alias='tMin', default=None)
    'The minimum t coordinate of the view'
    t_max: Optional[int] = Field(alias='tMax', default=None)
    'The maximum t coordinate of the view'
    c_min: Optional[int] = Field(alias='cMin', default=None)
    'The minimum c (channel) coordinate of the view'
    c_max: Optional[int] = Field(alias='cMax', default=None)
    'The maximum c (channel) coordinate of the view'
    emission_wavelength: Optional[float] = Field(alias='emissionWavelength', default=None)
    'The emission wavelength of the channel in nanometers'
    excitation_wavelength: Optional[float] = Field(alias='excitationWavelength', default=None)
    'The excitation wavelength of the channel in nanometers'
    acquisition_mode: Optional[str] = Field(alias='acquisitionMode', default=None)
    'The acquisition mode of the channel'
    name: Optional[str] = None
    'The name of the channel'
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class PartialDerivedViewInput(BaseModel):
    """Input for creating a derived view (recording the image this image was derived from) as part of creating an image; the image is taken from the surrounding input"""
    collection: Optional[ID] = None
    'The collection this view belongs to'
    z_min: Optional[int] = Field(alias='zMin', default=None)
    'The minimum z coordinate of the view'
    z_max: Optional[int] = Field(alias='zMax', default=None)
    'The maximum z coordinate of the view'
    x_min: Optional[int] = Field(alias='xMin', default=None)
    'The minimum x coordinate of the view'
    x_max: Optional[int] = Field(alias='xMax', default=None)
    'The maximum x coordinate of the view'
    y_min: Optional[int] = Field(alias='yMin', default=None)
    'The minimum y coordinate of the view'
    y_max: Optional[int] = Field(alias='yMax', default=None)
    'The maximum y coordinate of the view'
    t_min: Optional[int] = Field(alias='tMin', default=None)
    'The minimum t coordinate of the view'
    t_max: Optional[int] = Field(alias='tMax', default=None)
    'The maximum t coordinate of the view'
    c_min: Optional[int] = Field(alias='cMin', default=None)
    'The minimum c (channel) coordinate of the view'
    c_max: Optional[int] = Field(alias='cMax', default=None)
    'The maximum c (channel) coordinate of the view'
    origin_image: ID = Field(alias='originImage')
    'The ID of the image this image was derived from'
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class PartialFileViewInput(BaseModel):
    """Input for creating a file view (linking the image region to the originating file) as part of creating an image; the image is taken from the surrounding input"""
    collection: Optional[ID] = None
    'The collection this view belongs to'
    z_min: Optional[int] = Field(alias='zMin', default=None)
    'The minimum z coordinate of the view'
    z_max: Optional[int] = Field(alias='zMax', default=None)
    'The maximum z coordinate of the view'
    x_min: Optional[int] = Field(alias='xMin', default=None)
    'The minimum x coordinate of the view'
    x_max: Optional[int] = Field(alias='xMax', default=None)
    'The maximum x coordinate of the view'
    y_min: Optional[int] = Field(alias='yMin', default=None)
    'The minimum y coordinate of the view'
    y_max: Optional[int] = Field(alias='yMax', default=None)
    'The maximum y coordinate of the view'
    t_min: Optional[int] = Field(alias='tMin', default=None)
    'The minimum t coordinate of the view'
    t_max: Optional[int] = Field(alias='tMax', default=None)
    'The maximum t coordinate of the view'
    c_min: Optional[int] = Field(alias='cMin', default=None)
    'The minimum c (channel) coordinate of the view'
    c_max: Optional[int] = Field(alias='cMax', default=None)
    'The maximum c (channel) coordinate of the view'
    file: ID
    'The ID of the file this view represents'
    series_identifier: Optional[str] = Field(alias='seriesIdentifier', default=None)
    'The series identifier of the file'
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class PartialImageAccessorInput(BaseModel):
    """Input for an image accessor on a table, linking columns to an image (without the table reference)"""
    keys: Tuple[str, ...]
    'The column keys of the table this accessor refers to'
    min_index: Optional[int] = Field(alias='minIndex', default=None)
    'The minimum row index this accessor applies to'
    max_index: Optional[int] = Field(alias='maxIndex', default=None)
    'The maximum row index this accessor applies to'
    image: ID
    'The ID of the image the accessor values refer to'
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class PartialInstanceMaskViewInput(BaseModel):
    """Input for creating an instance mask view (an instance mask of another image) as part of creating an image; the image is taken from the surrounding input"""
    collection: Optional[ID] = None
    'The collection this view belongs to'
    z_min: Optional[int] = Field(alias='zMin', default=None)
    'The minimum z coordinate of the view'
    z_max: Optional[int] = Field(alias='zMax', default=None)
    'The maximum z coordinate of the view'
    x_min: Optional[int] = Field(alias='xMin', default=None)
    'The minimum x coordinate of the view'
    x_max: Optional[int] = Field(alias='xMax', default=None)
    'The maximum x coordinate of the view'
    y_min: Optional[int] = Field(alias='yMin', default=None)
    'The minimum y coordinate of the view'
    y_max: Optional[int] = Field(alias='yMax', default=None)
    'The maximum y coordinate of the view'
    t_min: Optional[int] = Field(alias='tMin', default=None)
    'The minimum t coordinate of the view'
    t_max: Optional[int] = Field(alias='tMax', default=None)
    'The maximum t coordinate of the view'
    c_min: Optional[int] = Field(alias='cMin', default=None)
    'The minimum c (channel) coordinate of the view'
    c_max: Optional[int] = Field(alias='cMax', default=None)
    'The maximum c (channel) coordinate of the view'
    reference_view: Optional[ID] = Field(alias='referenceView', default=None)
    'The ID of the view that is masked by this instance mask'
    labels: Optional[LabelsLike] = None
    'The instance labels of the mask and their corresponding colors'
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class PartialLabelAccessorInput(BaseModel):
    """Input for a label accessor on a table, linking columns to a pixel view (without the table reference)"""
    keys: Tuple[str, ...]
    'The column keys of the table this accessor refers to'
    min_index: Optional[int] = Field(alias='minIndex', default=None)
    'The minimum row index this accessor applies to'
    max_index: Optional[int] = Field(alias='maxIndex', default=None)
    'The maximum row index this accessor applies to'
    pixel_view: ID = Field(alias='pixelView')
    'The ID of the pixel view the label values refer to'
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class PartialLightpathViewInput(BaseModel):
    """Input for creating a lightpath view (the optical path of the instrument) as part of creating an image; the image is taken from the surrounding input"""
    collection: Optional[ID] = None
    'The collection this view belongs to'
    z_min: Optional[int] = Field(alias='zMin', default=None)
    'The minimum z coordinate of the view'
    z_max: Optional[int] = Field(alias='zMax', default=None)
    'The maximum z coordinate of the view'
    x_min: Optional[int] = Field(alias='xMin', default=None)
    'The minimum x coordinate of the view'
    x_max: Optional[int] = Field(alias='xMax', default=None)
    'The maximum x coordinate of the view'
    y_min: Optional[int] = Field(alias='yMin', default=None)
    'The minimum y coordinate of the view'
    y_max: Optional[int] = Field(alias='yMax', default=None)
    'The maximum y coordinate of the view'
    t_min: Optional[int] = Field(alias='tMin', default=None)
    'The minimum t coordinate of the view'
    t_max: Optional[int] = Field(alias='tMax', default=None)
    'The maximum t coordinate of the view'
    c_min: Optional[int] = Field(alias='cMin', default=None)
    'The minimum c (channel) coordinate of the view'
    c_max: Optional[int] = Field(alias='cMax', default=None)
    'The maximum c (channel) coordinate of the view'
    graph: LightpathGraphInput
    'The lightpath graph of the instrument'
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class PartialMaskViewInput(BaseModel):
    """Input for creating a mask view (a label mask of another image) as part of creating an image; the image is taken from the surrounding input"""
    collection: Optional[ID] = None
    'The collection this view belongs to'
    z_min: Optional[int] = Field(alias='zMin', default=None)
    'The minimum z coordinate of the view'
    z_max: Optional[int] = Field(alias='zMax', default=None)
    'The maximum z coordinate of the view'
    x_min: Optional[int] = Field(alias='xMin', default=None)
    'The minimum x coordinate of the view'
    x_max: Optional[int] = Field(alias='xMax', default=None)
    'The maximum x coordinate of the view'
    y_min: Optional[int] = Field(alias='yMin', default=None)
    'The minimum y coordinate of the view'
    y_max: Optional[int] = Field(alias='yMax', default=None)
    'The maximum y coordinate of the view'
    t_min: Optional[int] = Field(alias='tMin', default=None)
    'The minimum t coordinate of the view'
    t_max: Optional[int] = Field(alias='tMax', default=None)
    'The maximum t coordinate of the view'
    c_min: Optional[int] = Field(alias='cMin', default=None)
    'The minimum c (channel) coordinate of the view'
    c_max: Optional[int] = Field(alias='cMax', default=None)
    'The maximum c (channel) coordinate of the view'
    reference_view: Optional[ID] = Field(alias='referenceView', default=None)
    'The ID of the view that is masked by this mask'
    labels: Optional[LabelsLike] = None
    'The labels of the mask and their corresponding colors'
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class PartialOpticsViewInput(BaseModel):
    """Input for creating an optics view (instrument, objective and camera used) as part of creating an image; the image is taken from the surrounding input"""
    collection: Optional[ID] = None
    'The collection this view belongs to'
    z_min: Optional[int] = Field(alias='zMin', default=None)
    'The minimum z coordinate of the view'
    z_max: Optional[int] = Field(alias='zMax', default=None)
    'The maximum z coordinate of the view'
    x_min: Optional[int] = Field(alias='xMin', default=None)
    'The minimum x coordinate of the view'
    x_max: Optional[int] = Field(alias='xMax', default=None)
    'The maximum x coordinate of the view'
    y_min: Optional[int] = Field(alias='yMin', default=None)
    'The minimum y coordinate of the view'
    y_max: Optional[int] = Field(alias='yMax', default=None)
    'The maximum y coordinate of the view'
    t_min: Optional[int] = Field(alias='tMin', default=None)
    'The minimum t coordinate of the view'
    t_max: Optional[int] = Field(alias='tMax', default=None)
    'The maximum t coordinate of the view'
    c_min: Optional[int] = Field(alias='cMin', default=None)
    'The minimum c (channel) coordinate of the view'
    c_max: Optional[int] = Field(alias='cMax', default=None)
    'The maximum c (channel) coordinate of the view'
    instrument: Optional[ID] = None
    'The ID of the instrument used to acquire the image'
    objective: Optional[ID] = None
    'The ID of the objective used to acquire the image'
    camera: Optional[ID] = None
    'The ID of the camera used to acquire the image'
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class PartialRGBViewInput(BaseModel):
    """Input for creating an RGB render view (how a channel is rendered in an RGB context) as part of creating an image; the image is taken from the surrounding input"""
    collection: Optional[ID] = None
    'The collection this view belongs to'
    z_min: Optional[int] = Field(alias='zMin', default=None)
    'The minimum z coordinate of the view'
    z_max: Optional[int] = Field(alias='zMax', default=None)
    'The maximum z coordinate of the view'
    x_min: Optional[int] = Field(alias='xMin', default=None)
    'The minimum x coordinate of the view'
    x_max: Optional[int] = Field(alias='xMax', default=None)
    'The maximum x coordinate of the view'
    y_min: Optional[int] = Field(alias='yMin', default=None)
    'The minimum y coordinate of the view'
    y_max: Optional[int] = Field(alias='yMax', default=None)
    'The maximum y coordinate of the view'
    t_min: Optional[int] = Field(alias='tMin', default=None)
    'The minimum t coordinate of the view'
    t_max: Optional[int] = Field(alias='tMax', default=None)
    'The maximum t coordinate of the view'
    c_min: Optional[int] = Field(alias='cMin', default=None)
    'The minimum c (channel) coordinate of the view'
    c_max: Optional[int] = Field(alias='cMax', default=None)
    'The maximum c (channel) coordinate of the view'
    context: Optional[ID] = None
    'The ID of the RGB render context this view belongs to'
    gamma: Optional[float] = None
    'The gamma correction applied to the channel'
    contrast_limit_min: Optional[float] = Field(alias='contrastLimitMin', default=None)
    'The minimum contrast limit of the channel'
    contrast_limit_max: Optional[float] = Field(alias='contrastLimitMax', default=None)
    'The maximum contrast limit of the channel'
    rescale: Optional[bool] = None
    'Whether to rescale the channel data to the contrast limits'
    scale: Optional[float] = None
    'The scale factor applied to the channel when rendering'
    active: Optional[bool] = None
    'Whether the view is active'
    color_map: Optional[ColorMap] = Field(alias='colorMap', default=None)
    'The color map applied to the channel'
    base_color: Optional[Tuple[float, ...]] = Field(alias='baseColor', default=None)
    'The base color of the channel as RGBA values (if using a mapped scaler)'
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class PartialROIViewInput(BaseModel):
    """Input for creating a ROI view (marking the image as a cutout of a parent image's ROI) as part of creating an image; the image is taken from the surrounding input"""
    collection: Optional[ID] = None
    'The collection this view belongs to'
    z_min: Optional[int] = Field(alias='zMin', default=None)
    'The minimum z coordinate of the view'
    z_max: Optional[int] = Field(alias='zMax', default=None)
    'The maximum z coordinate of the view'
    x_min: Optional[int] = Field(alias='xMin', default=None)
    'The minimum x coordinate of the view'
    x_max: Optional[int] = Field(alias='xMax', default=None)
    'The maximum x coordinate of the view'
    y_min: Optional[int] = Field(alias='yMin', default=None)
    'The minimum y coordinate of the view'
    y_max: Optional[int] = Field(alias='yMax', default=None)
    'The maximum y coordinate of the view'
    t_min: Optional[int] = Field(alias='tMin', default=None)
    'The minimum t coordinate of the view'
    t_max: Optional[int] = Field(alias='tMax', default=None)
    'The maximum t coordinate of the view'
    c_min: Optional[int] = Field(alias='cMin', default=None)
    'The minimum c (channel) coordinate of the view'
    c_max: Optional[int] = Field(alias='cMax', default=None)
    'The maximum c (channel) coordinate of the view'
    roi: ID
    'The ID of the ROI of the parent image this view is a cutout of'
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class PartialReferenceViewInput(BaseModel):
    """Input for creating a reference view (marking the region as a reference for other views) as part of creating an image; the image is taken from the surrounding input"""
    collection: Optional[ID] = None
    'The collection this view belongs to'
    z_min: Optional[int] = Field(alias='zMin', default=None)
    'The minimum z coordinate of the view'
    z_max: Optional[int] = Field(alias='zMax', default=None)
    'The maximum z coordinate of the view'
    x_min: Optional[int] = Field(alias='xMin', default=None)
    'The minimum x coordinate of the view'
    x_max: Optional[int] = Field(alias='xMax', default=None)
    'The maximum x coordinate of the view'
    y_min: Optional[int] = Field(alias='yMin', default=None)
    'The minimum y coordinate of the view'
    y_max: Optional[int] = Field(alias='yMax', default=None)
    'The maximum y coordinate of the view'
    t_min: Optional[int] = Field(alias='tMin', default=None)
    'The minimum t coordinate of the view'
    t_max: Optional[int] = Field(alias='tMax', default=None)
    'The maximum t coordinate of the view'
    c_min: Optional[int] = Field(alias='cMin', default=None)
    'The minimum c (channel) coordinate of the view'
    c_max: Optional[int] = Field(alias='cMax', default=None)
    'The maximum c (channel) coordinate of the view'
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class PartialScaleViewInput(BaseModel):
    """Input for creating a scale view (the scale factors relative to a parent view) as part of creating an image; the image is taken from the surrounding input"""
    collection: Optional[ID] = None
    'The collection this view belongs to'
    z_min: Optional[int] = Field(alias='zMin', default=None)
    'The minimum z coordinate of the view'
    z_max: Optional[int] = Field(alias='zMax', default=None)
    'The maximum z coordinate of the view'
    x_min: Optional[int] = Field(alias='xMin', default=None)
    'The minimum x coordinate of the view'
    x_max: Optional[int] = Field(alias='xMax', default=None)
    'The maximum x coordinate of the view'
    y_min: Optional[int] = Field(alias='yMin', default=None)
    'The minimum y coordinate of the view'
    y_max: Optional[int] = Field(alias='yMax', default=None)
    'The maximum y coordinate of the view'
    t_min: Optional[int] = Field(alias='tMin', default=None)
    'The minimum t coordinate of the view'
    t_max: Optional[int] = Field(alias='tMax', default=None)
    'The maximum t coordinate of the view'
    c_min: Optional[int] = Field(alias='cMin', default=None)
    'The minimum c (channel) coordinate of the view'
    c_max: Optional[int] = Field(alias='cMax', default=None)
    'The maximum c (channel) coordinate of the view'
    parent: Optional[ID] = None
    'The ID of the parent view this scale view is derived from'
    scale_x: Optional[float] = Field(alias='scaleX', default=None)
    'The scale in x direction'
    scale_y: Optional[float] = Field(alias='scaleY', default=None)
    'The scale in y direction'
    scale_z: Optional[float] = Field(alias='scaleZ', default=None)
    'The scale in z direction'
    scale_t: Optional[float] = Field(alias='scaleT', default=None)
    'The scale in t direction'
    scale_c: Optional[float] = Field(alias='scaleC', default=None)
    'The scale in c direction'
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class PartialTimepointViewInput(BaseModel):
    """Input for creating a timepoint view (placing the region in time relative to an era) as part of creating an image; the image is taken from the surrounding input"""
    collection: Optional[ID] = None
    'The collection this view belongs to'
    z_min: Optional[int] = Field(alias='zMin', default=None)
    'The minimum z coordinate of the view'
    z_max: Optional[int] = Field(alias='zMax', default=None)
    'The maximum z coordinate of the view'
    x_min: Optional[int] = Field(alias='xMin', default=None)
    'The minimum x coordinate of the view'
    x_max: Optional[int] = Field(alias='xMax', default=None)
    'The maximum x coordinate of the view'
    y_min: Optional[int] = Field(alias='yMin', default=None)
    'The minimum y coordinate of the view'
    y_max: Optional[int] = Field(alias='yMax', default=None)
    'The maximum y coordinate of the view'
    t_min: Optional[int] = Field(alias='tMin', default=None)
    'The minimum t coordinate of the view'
    t_max: Optional[int] = Field(alias='tMax', default=None)
    'The maximum t coordinate of the view'
    c_min: Optional[int] = Field(alias='cMin', default=None)
    'The minimum c (channel) coordinate of the view'
    c_max: Optional[int] = Field(alias='cMax', default=None)
    'The maximum c (channel) coordinate of the view'
    era: Optional[ID] = None
    'The ID of the era this timepoint belongs to'
    ms_since_start: Optional[Milliseconds] = Field(alias='msSinceStart', default=None)
    'The time in ms since the start of the era'
    index_since_start: Optional[int] = Field(alias='indexSinceStart', default=None)
    'The index of the timepoint since the start of the era'
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class Pose3DInput(BaseModel):
    """A 3D pose consisting of position and orientation."""
    position: Optional['Vec3Input'] = None
    orientation: Optional[EulerInput] = None
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class RGBViewInput(BaseModel):
    """Input for creating an RGB render view on an existing image, referenced by ID"""
    collection: Optional[ID] = None
    'The collection this view belongs to'
    z_min: Optional[int] = Field(alias='zMin', default=None)
    'The minimum z coordinate of the view'
    z_max: Optional[int] = Field(alias='zMax', default=None)
    'The maximum z coordinate of the view'
    x_min: Optional[int] = Field(alias='xMin', default=None)
    'The minimum x coordinate of the view'
    x_max: Optional[int] = Field(alias='xMax', default=None)
    'The maximum x coordinate of the view'
    y_min: Optional[int] = Field(alias='yMin', default=None)
    'The minimum y coordinate of the view'
    y_max: Optional[int] = Field(alias='yMax', default=None)
    'The maximum y coordinate of the view'
    t_min: Optional[int] = Field(alias='tMin', default=None)
    'The minimum t coordinate of the view'
    t_max: Optional[int] = Field(alias='tMax', default=None)
    'The maximum t coordinate of the view'
    c_min: Optional[int] = Field(alias='cMin', default=None)
    'The minimum c (channel) coordinate of the view'
    c_max: Optional[int] = Field(alias='cMax', default=None)
    'The maximum c (channel) coordinate of the view'
    context: ID
    'The ID of the RGB render context this view belongs to'
    gamma: Optional[float] = None
    'The gamma correction applied to the channel'
    contrast_limit_min: Optional[float] = Field(alias='contrastLimitMin', default=None)
    'The minimum contrast limit of the channel'
    contrast_limit_max: Optional[float] = Field(alias='contrastLimitMax', default=None)
    'The maximum contrast limit of the channel'
    rescale: Optional[bool] = None
    'Whether to rescale the channel data to the contrast limits'
    scale: Optional[float] = None
    'The scale factor applied to the channel when rendering'
    active: Optional[bool] = None
    'Whether the view is active'
    color_map: Optional[ColorMap] = Field(alias='colorMap', default=None)
    'The color map applied to the channel'
    base_color: Optional[Tuple[float, ...]] = Field(alias='baseColor', default=None)
    'The base color of the channel as RGBA values (if using a mapped scaler)'
    image: ID
    'The ID of the image this view is for'
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class ReferenceViewInput(BaseModel):
    """Input for creating a reference view on an existing image, referenced by ID"""
    collection: Optional[ID] = None
    'The collection this view belongs to'
    z_min: Optional[int] = Field(alias='zMin', default=None)
    'The minimum z coordinate of the view'
    z_max: Optional[int] = Field(alias='zMax', default=None)
    'The maximum z coordinate of the view'
    x_min: Optional[int] = Field(alias='xMin', default=None)
    'The minimum x coordinate of the view'
    x_max: Optional[int] = Field(alias='xMax', default=None)
    'The maximum x coordinate of the view'
    y_min: Optional[int] = Field(alias='yMin', default=None)
    'The minimum y coordinate of the view'
    y_max: Optional[int] = Field(alias='yMax', default=None)
    'The maximum y coordinate of the view'
    t_min: Optional[int] = Field(alias='tMin', default=None)
    'The minimum t coordinate of the view'
    t_max: Optional[int] = Field(alias='tMax', default=None)
    'The maximum t coordinate of the view'
    c_min: Optional[int] = Field(alias='cMin', default=None)
    'The minimum c (channel) coordinate of the view'
    c_max: Optional[int] = Field(alias='cMax', default=None)
    'The maximum c (channel) coordinate of the view'
    image: ID
    'The ID of the image this view is for'
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class RenderTreeInput(BaseModel):
    """No documentation"""
    tree: 'TreeInput'
    name: str
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class RequestBigFileAccessInput(BaseModel):
    """No documentation"""
    store_id: str = Field(alias='storeId')
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class RequestBigFileUploadInput(BaseModel):
    """No documentation"""
    original_file_name: str = Field(alias='originalFileName')
    file_size: Optional[int] = Field(alias='fileSize', default=None)
    content_type: Optional[str] = Field(alias='contentType', default=None)
    host: Optional[str] = None
    port: Optional[int] = None
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class RequestMediaAccessInput(BaseModel):
    """No documentation"""
    store_id: str = Field(alias='storeId')
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class RequestMediaUploadInput(BaseModel):
    """No documentation"""
    original_file_name: str = Field(alias='originalFileName')
    file_size: Optional[int] = Field(alias='fileSize', default=None)
    content_type: Optional[str] = Field(alias='contentType', default=None)
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class RequestParquetAccessInput(BaseModel):
    """No documentation"""
    store_id: str = Field(alias='storeId')
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class RequestParquetUploadInput(BaseModel):
    """No documentation"""
    content_type: Optional[str] = Field(alias='contentType', default=None)
    host: Optional[str] = None
    port: Optional[int] = None
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class RequestZarrAccessInput(BaseModel):
    """No documentation"""
    store_id: str = Field(alias='storeId')
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class RequestZarrUploadInput(BaseModel):
    """No documentation"""
    shape: Optional[Tuple[int, ...]] = None
    chunks: Optional[Tuple[int, ...]] = None
    version: Optional[str] = None
    host: Optional[str] = None
    port: Optional[int] = None
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class RevertInput(BaseModel):
    """Input for reverting a dataset to a previous history revision"""
    id: ID
    'The ID of the dataset to revert'
    history_id: ID = Field(alias='historyId')
    'The ID of the provenance history entry to revert the dataset to'
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class RoiInput(BaseModel):
    """Input for creating a region of interest (ROI) on an image"""
    image: ID
    'The image this ROI belongs to'
    vectors: Tuple[FiveDVector, ...]
    'The vector coordinates defining the ROI'
    kind: RoiKind
    'The type/kind of ROI'
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class ScaleInput(BaseModel):
    """Input type for a scale, which specifies an array-like object to create the image from and optional scale factors for each dimension of the image"""
    scale_method: Optional[str] = Field(alias='scaleMethod', default=None)
    "The method used to create the scale, e.g. 'nearest', 'bilinear', 'bicubic', etc. This can be used to provide additional context about how the scale was created and the expected quality of the scale"
    level: int
    array: ArrayLike
    'The array-like object to create the image from'
    scale_factors: Optional[Tuple[float, ...]] = Field(alias='scaleFactors', default=None)
    'The scale factors for each dimension of the image, which specify the physical size of each pixel along each dimension and can be used to provide additional context about the spatial resolution of the image'
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class SliceInput(BaseModel):
    """Input type for a dimension descriptor, which specifies a key and a kind for a dimension"""
    dim: str
    start: Optional[int] = None
    stop: Optional[int] = None
    step: Optional[int] = None
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class SnapshotInput(BaseModel):
    """Input for creating a snapshot (pre-rendered thumbnail) of an image from an uploaded media file"""
    file: ImageFileLike
    'The uploaded media file store containing the rendered snapshot'
    image: ID
    'The ID of the image this snapshot belongs to'
    name: Optional[str] = None
    'The name of the snapshot'
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class SpectrumInput(BaseModel):
    """Spectral window in nanometers for wavelength-dependent components."""
    min_nm: float = Field(alias='minNm')
    max_nm: float = Field(alias='maxNm')
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class StageFilter(BaseModel):
    """No documentation"""
    ids: Optional[Tuple[ID, ...]] = None
    'Filter by list of IDs'
    search: Optional[str] = None
    'Search by name (case-insensitive substring)'
    created_before: Optional[datetime] = Field(alias='createdBefore', default=None)
    'Filter for items created before this datetime'
    created_after: Optional[datetime] = Field(alias='createdAfter', default=None)
    'Filter for items created after this datetime'
    owner: Optional[ID] = None
    "Filter by the creator's subject ID"
    pinned: Optional[bool] = None
    'Filter by whether the current user has pinned the item'
    created_through_task: Optional[str] = Field(alias='createdThroughTask', default=None)
    'Filter by the rekuest task id the item was created through'
    created_through: Optional[ID] = Field(alias='createdThrough', default=None)
    'Filter by the database ID of the task the item was created through (the `createdThrough { id }` field)'
    assigned_by: Optional[ID] = Field(alias='assignedBy', default=None)
    'Filter by the sub of the user that assigned the creating task'
    created_through_by: Optional[ID] = Field(alias='createdThroughBy', default=None)
    'Filter by the database ID of the user that assigned the creating task (the `createdThroughBy { id }` field)'
    id: Optional[ID] = None
    kind: Optional[str] = None
    name: Optional['StrFilterLookup'] = None
    and_: Optional['StageFilter'] = Field(alias='AND', default=None)
    or_: Optional['StageFilter'] = Field(alias='OR', default=None)
    not_: Optional['StageFilter'] = Field(alias='NOT', default=None)
    distinct: Optional[bool] = Field(alias='DISTINCT', default=None)
    instrument: Optional[ID] = None
    'Filter by the instrument this stage belongs to'
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class StageInput(BaseModel):
    """Input for creating a stage, a physical coordinate system for positioning images"""
    name: str
    'The name of the stage'
    instrument: Optional[ID] = None
    'The ID of the instrument this stage belongs to'
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class StrFilterLookup(BaseModel):
    """No documentation"""
    exact: Optional[str] = None
    i_exact: Optional[str] = Field(alias='iExact', default=None)
    contains: Optional[str] = None
    i_contains: Optional[str] = Field(alias='iContains', default=None)
    in_list: Optional[Tuple[str, ...]] = Field(alias='inList', default=None)
    gt: Optional[str] = None
    gte: Optional[str] = None
    lt: Optional[str] = None
    lte: Optional[str] = None
    starts_with: Optional[str] = Field(alias='startsWith', default=None)
    i_starts_with: Optional[str] = Field(alias='iStartsWith', default=None)
    ends_with: Optional[str] = Field(alias='endsWith', default=None)
    i_ends_with: Optional[str] = Field(alias='iEndsWith', default=None)
    range: Optional[Tuple[str, ...]] = None
    is_null: Optional[bool] = Field(alias='isNull', default=None)
    regex: Optional[str] = None
    i_regex: Optional[str] = Field(alias='iRegex', default=None)
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class TimepointViewFilter(BaseModel):
    """No documentation"""
    ids: Optional[Tuple[ID, ...]] = None
    'Filter by list of IDs'
    is_global: Optional[bool] = Field(alias='isGlobal', default=None)
    image: Optional[ID] = None
    'Filter by the image this view belongs to'
    images: Optional[Tuple[ID, ...]] = None
    'Filter by a list of images this view belongs to'
    search: Optional[str] = None
    'Search by the name of the image this view belongs to'
    id: Optional[ID] = None
    era: Optional[EraFilter] = None
    ms_since_start: Optional[float] = Field(alias='msSinceStart', default=None)
    index_since_start: Optional[int] = Field(alias='indexSinceStart', default=None)
    and_: Optional['TimepointViewFilter'] = Field(alias='AND', default=None)
    or_: Optional['TimepointViewFilter'] = Field(alias='OR', default=None)
    not_: Optional['TimepointViewFilter'] = Field(alias='NOT', default=None)
    distinct: Optional[bool] = Field(alias='DISTINCT', default=None)
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class TreeInput(BaseModel):
    """No documentation"""
    id: Optional[str] = None
    children: Tuple['TreeNodeInput', ...]
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class TreeNodeInput(BaseModel):
    """No documentation"""
    kind: RenderNodeKind
    label: Optional[str] = None
    context: Optional[str] = None
    gap: Optional[int] = None
    children: Optional[Tuple['TreeNodeInput', ...]] = None
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class UpdateRGBContextInput(BaseModel):
    """Input for updating an existing RGB render context"""
    id: ID
    'The ID of the RGB context to update'
    name: Optional[str] = None
    'The new name of the RGB context'
    thumbnail: Optional[ID] = None
    'The ID of an uploaded media store to use as the thumbnail snapshot'
    views: Optional[Tuple[PartialRGBViewInput, ...]] = None
    "The RGB views (channel rendering settings) to replace the context's views with"
    z: Optional[int] = None
    'The z plane the context renders'
    t: Optional[int] = None
    'The timepoint the context renders'
    c: Optional[int] = None
    'The channel the context renders'
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class UpdateRGBViewInput(BaseModel):
    """Input for updating an existing RGB view, referenced by ID"""
    collection: Optional[ID] = None
    'The collection this view belongs to'
    z_min: Optional[int] = Field(alias='zMin', default=None)
    'The minimum z coordinate of the view'
    z_max: Optional[int] = Field(alias='zMax', default=None)
    'The maximum z coordinate of the view'
    x_min: Optional[int] = Field(alias='xMin', default=None)
    'The minimum x coordinate of the view'
    x_max: Optional[int] = Field(alias='xMax', default=None)
    'The maximum x coordinate of the view'
    y_min: Optional[int] = Field(alias='yMin', default=None)
    'The minimum y coordinate of the view'
    y_max: Optional[int] = Field(alias='yMax', default=None)
    'The maximum y coordinate of the view'
    t_min: Optional[int] = Field(alias='tMin', default=None)
    'The minimum t coordinate of the view'
    t_max: Optional[int] = Field(alias='tMax', default=None)
    'The maximum t coordinate of the view'
    c_min: Optional[int] = Field(alias='cMin', default=None)
    'The minimum c (channel) coordinate of the view'
    c_max: Optional[int] = Field(alias='cMax', default=None)
    'The maximum c (channel) coordinate of the view'
    context: Optional[ID] = None
    'The ID of the RGB render context this view belongs to'
    gamma: Optional[float] = None
    'The gamma correction applied to the channel'
    contrast_limit_min: Optional[float] = Field(alias='contrastLimitMin', default=None)
    'The minimum contrast limit of the channel'
    contrast_limit_max: Optional[float] = Field(alias='contrastLimitMax', default=None)
    'The maximum contrast limit of the channel'
    rescale: Optional[bool] = None
    'Whether to rescale the channel data to the contrast limits'
    scale: Optional[float] = None
    'The scale factor applied to the channel when rendering'
    active: Optional[bool] = None
    'Whether the view is active'
    color_map: Optional[ColorMap] = Field(alias='colorMap', default=None)
    'The color map applied to the channel'
    base_color: Optional[Tuple[float, ...]] = Field(alias='baseColor', default=None)
    'The base color of the channel as RGBA values (if using a mapped scaler)'
    id: ID
    'The ID of the RGB view to update'
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class UpdateRoiInput(BaseModel):
    """Input for updating an existing region of interest (ROI)"""
    roi: ID
    'The ID of the ROI to update'
    vectors: Optional[Tuple[FiveDVector, ...]] = None
    'The new vector coordinates defining the ROI'
    kind: Optional[RoiKind] = None
    'The new type/kind of ROI'
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class ValueHistogramInput(BaseModel):
    """Input type for a value histogram, which specifies the histogram of pixel values along certain dimensions to provide additional context about the distribution of pixel values in an image"""
    histogram: Tuple[float, ...]
    'The histogram of the pixel values (y values)'
    bins: Tuple[float, ...]
    'The bin indices of the histogram (x values)'
    min: Optional[float] = None
    'The minimum pixel value of the histogram'
    max: Optional[float] = None
    'The maximum pixel value of the histogram'
    p1: Optional[float] = None
    'The 1st percentile pixel value of the histogram'
    p99: Optional[float] = None
    'The 99th percentile pixel value of the histogram'
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class Vec3Input(BaseModel):
    """A 3D vector representing a point or offset in space."""
    x: Optional[float] = None
    y: Optional[float] = None
    z: Optional[float] = None
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class ViewCollectionInput(BaseModel):
    """Input for creating a view collection to group views"""
    name: str
    'The name of the view collection'
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class ViewFilter(BaseModel):
    """No documentation"""
    ids: Optional[Tuple[ID, ...]] = None
    'Filter by list of IDs'
    is_global: Optional[bool] = Field(alias='isGlobal', default=None)
    and_: Optional['ViewFilter'] = Field(alias='AND', default=None)
    or_: Optional['ViewFilter'] = Field(alias='OR', default=None)
    not_: Optional['ViewFilter'] = Field(alias='NOT', default=None)
    distinct: Optional[bool] = Field(alias='DISTINCT', default=None)
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class ZarrStoreFilter(BaseModel):
    """No documentation"""
    shape: Optional[IntFilterLookup] = None
    and_: Optional['ZarrStoreFilter'] = Field(alias='AND', default=None)
    or_: Optional['ZarrStoreFilter'] = Field(alias='OR', default=None)
    not_: Optional['ZarrStoreFilter'] = Field(alias='NOT', default=None)
    distinct: Optional[bool] = Field(alias='DISTINCT', default=None)
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class ViewBase(BaseModel):
    """A view is a subset of an image, delimited by its coordinates (c, t, z, x, y) within the 5D array. Views attach metadata (channels, labels, transformations, timepoints, ...) to that subregion of the image."""
    x_min: Optional[int] = Field(default=None, alias='xMin')
    x_max: Optional[int] = Field(default=None, alias='xMax')
    y_min: Optional[int] = Field(default=None, alias='yMin')
    y_max: Optional[int] = Field(default=None, alias='yMax')
    t_min: Optional[int] = Field(default=None, alias='tMin')
    t_max: Optional[int] = Field(default=None, alias='tMax')
    c_min: Optional[int] = Field(default=None, alias='cMin')
    c_max: Optional[int] = Field(default=None, alias='cMax')
    z_min: Optional[int] = Field(default=None, alias='zMin')
    z_max: Optional[int] = Field(default=None, alias='zMax')

class ViewCatch(ViewBase):
    """Catch all class for ViewBase"""
    typename: str = Field(alias='__typename', exclude=True)
    'A view is a subset of an image, delimited by its coordinates (c, t, z, x, y) within the 5D array. Views attach metadata (channels, labels, transformations, timepoints, ...) to that subregion of the image.'
    x_min: Optional[int] = Field(default=None, alias='xMin')
    x_max: Optional[int] = Field(default=None, alias='xMax')
    y_min: Optional[int] = Field(default=None, alias='yMin')
    y_max: Optional[int] = Field(default=None, alias='yMax')
    t_min: Optional[int] = Field(default=None, alias='tMin')
    t_max: Optional[int] = Field(default=None, alias='tMax')
    c_min: Optional[int] = Field(default=None, alias='cMin')
    c_max: Optional[int] = Field(default=None, alias='cMax')
    z_min: Optional[int] = Field(default=None, alias='zMin')
    z_max: Optional[int] = Field(default=None, alias='zMax')

class ViewAcquisitionView(ViewBase, BaseModel):
    """A view recording when and by whom an image region was acquired at the microscope. Use it to trace an image back to its acquisition session and operator."""
    typename: Literal['AcquisitionView'] = Field(alias='__typename', default='AcquisitionView', exclude=True)

class ViewAffineTransformationView(ViewBase, BaseModel):
    """A view placing an image region in physical space: a 4x4 affine matrix maps pixel coordinates onto a stage, encoding position and pixel size."""
    typename: Literal['AffineTransformationView'] = Field(alias='__typename', default='AffineTransformationView', exclude=True)

class ViewChannelView(ViewBase, BaseModel):
    """A channel view describes an acquisition channel of an image, carrying its name and optical properties such as emission and excitation wavelengths."""
    typename: Literal['ChannelView'] = Field(alias='__typename', default='ChannelView', exclude=True)

class ViewContinousScanView(ViewBase, BaseModel):
    """A view marking an image region as acquired by a continuous scan, recording the direction the scan traversed the axes in."""
    typename: Literal['ContinousScanView'] = Field(alias='__typename', default='ContinousScanView', exclude=True)

class ViewDerivedView(ViewBase, BaseModel):
    """A derived view establishes a processing relationship between two images, guaranteeing that the derived image shares the same coordinate system as its origin image so the two can be trivially overlayed and compared (e.g. a segmentation over its source image). Cropped or projected images are not derived views, as they do not share the coordinate system."""
    typename: Literal['DerivedView'] = Field(alias='__typename', default='DerivedView', exclude=True)

class ViewFileView(ViewBase, BaseModel):
    """A file view establishes a relationship between an image and a file: it records that this view of the image was originally part of the file (optionally a specific series within it) and links back to the source file."""
    typename: Literal['FileView'] = Field(alias='__typename', default='FileView', exclude=True)

class ViewHistogramView(ViewBase, BaseModel):
    """A histogram view describes the distribution of pixel values in a subset of an image, providing bins, min/max bounds and the histogram counts. Useful for clients that want to display or auto-scale contrast."""
    typename: Literal['HistogramView'] = Field(alias='__typename', default='HistogramView', exclude=True)

class ViewInstanceMaskView(ViewBase, BaseModel):
    """A view marking an image region as an instance segmentation mask, where each pixel value identifies an individual object instance. It points to the reference view it was computed from and can carry a per-instance label table."""
    typename: Literal['InstanceMaskView'] = Field(alias='__typename', default='InstanceMaskView', exclude=True)

class ViewLabelView(ViewBase, BaseModel):
    """A label view gives a label to a specific image channel, e.g. mapping an antibody to the channel it stains, so the labeling agent can be easily identified. Labels can also be used for other purposes, such as marking a channel as poor quality."""
    typename: Literal['LabelView'] = Field(alias='__typename', default='LabelView', exclude=True)

class ViewLightpathView(ViewBase, BaseModel):
    """A view attaching the optical path (light sources, filters, detectors and their connections) that light travelled through when this image region was acquired."""
    typename: Literal['LightpathView'] = Field(alias='__typename', default='LightpathView', exclude=True)

class ViewMaskView(ViewBase, BaseModel):
    """A view marking an image region as a semantic segmentation mask, where pixel values are class labels. It points to the reference view it was computed from and can carry a label table."""
    typename: Literal['MaskView'] = Field(alias='__typename', default='MaskView', exclude=True)

class ViewOpticsView(ViewBase, BaseModel):
    """A view describing the optics used to acquire an image region: the instrument, objective and camera. Use it to inspect or compare acquisition hardware settings."""
    typename: Literal['OpticsView'] = Field(alias='__typename', default='OpticsView', exclude=True)

class ViewRGBView(ViewBase, BaseModel):
    """An RGB view describes how a subset of an image (typically a channel) is rendered in RGB within an RGB context, carrying color map, gamma and contrast limit settings."""
    typename: Literal['RGBView'] = Field(alias='__typename', default='RGBView', exclude=True)

class ViewROIView(ViewBase, BaseModel):
    """A ROI view establishes a relationship between an image region and a region of interest, e.g. recording that this image was cropped from the area described by the ROI on another image."""
    typename: Literal['ROIView'] = Field(alias='__typename', default='ROIView', exclude=True)

class ViewReferenceView(ViewBase, BaseModel):
    """A view marking an image region as the reference that other views (e.g. mask views) point back to, for example the raw channel a segmentation mask was computed from."""
    typename: Literal['ReferenceView'] = Field(alias='__typename', default='ReferenceView', exclude=True)

class ViewScaleView(ViewBase, BaseModel):
    """A view linking an image to a downscaled version of another image. Scale views form the levels of a multiscale pyramid: the parent is the full-resolution image and the scale factors give the downsampling per dimension."""
    typename: Literal['ScaleView'] = Field(alias='__typename', default='ScaleView', exclude=True)

class ViewTimepointView(ViewBase, BaseModel):
    """A view anchoring an image region in real time: it places the region within an era (a named time epoch on the microscope) at a millisecond offset or frame index since its start."""
    typename: Literal['TimepointView'] = Field(alias='__typename', default='TimepointView', exclude=True)

class ViewWellPositionView(ViewBase, BaseModel):
    """A view mapping an image region to a well (row/column) of a multi well plate, so plate-based acquisitions can be traced back to their well."""
    typename: Literal['WellPositionView'] = Field(alias='__typename', default='WellPositionView', exclude=True)

class ADatasetDataarrays(DataArrayTrait, BaseModel):
    """A single scale of a dataset's multiscale pyramid: a zarr-backed array described by its shape, chunk shape, scale factors and pyramid level"""
    typename: Literal['DataArray'] = Field(alias='__typename', default='DataArray', exclude=True)
    level: int
    shape: Tuple[int, ...]
    chunk_shape: Tuple[int, ...] = Field(alias='chunkShape')
    scale_factors: Optional[Tuple[float, ...]] = Field(default=None, alias='scaleFactors')
    model_config = ConfigDict(frozen=True)

class ADataset(DatasetTrait, MikroFetchable, BaseModel):
    """A multi-dimensional array dataset with named dimensions. It can have multiple scales attached to it, which are represented as DataArrays"""
    typename: Literal['ADataset'] = Field(alias='__typename', default='ADataset', exclude=True)
    id: ID
    name: str
    dims: Tuple[str, ...]
    data_arrays: Tuple[ADatasetDataarrays, ...] = Field(alias='dataArrays')
    'The multiscale data arrays belonging to this dataset'
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for ADataset"""
        document = 'fragment ADataset on ADataset {\n  id\n  name\n  dims\n  dataArrays {\n    level\n    shape\n    chunkShape\n    scaleFactors\n    __typename\n  }\n  __typename\n}'
        name = 'ADataset'
        type = 'ADataset'

class Camera(MikroFetchable, BaseModel):
    """A camera (detector) on a microscope, described by its sensor dimensions, pixel sizes and bit depth. Clients use it through optics views to record which detector acquired an image."""
    typename: Literal['Camera'] = Field(alias='__typename', default='Camera', exclude=True)
    sensor_size_x: Optional[int] = Field(default=None, alias='sensorSizeX')
    sensor_size_y: Optional[int] = Field(default=None, alias='sensorSizeY')
    pixel_size_x: Optional[Micrometers] = Field(default=None, alias='pixelSizeX')
    pixel_size_y: Optional[Micrometers] = Field(default=None, alias='pixelSizeY')
    name: str
    serial_number: str = Field(alias='serialNumber')
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for Camera"""
        document = 'fragment Camera on Camera {\n  sensorSizeX\n  sensorSizeY\n  pixelSizeX\n  pixelSizeY\n  name\n  serialNumber\n  __typename\n}'
        name = 'Camera'
        type = 'Camera'

class BigFileUploadGrant(MikroFetchable, BaseModel):
    """Temporary S3 credentials for uploading a big file."""
    typename: Literal['BigFileUploadGrant'] = Field(alias='__typename', default='BigFileUploadGrant', exclude=True)
    access_key: str = Field(alias='accessKey')
    secret_key: str = Field(alias='secretKey')
    session_token: str = Field(alias='sessionToken')
    path: str
    key: str
    bucket: str
    expires_in: int = Field(alias='expiresIn')
    store: str
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for BigFileUploadGrant"""
        document = 'fragment BigFileUploadGrant on BigFileUploadGrant {\n  accessKey\n  secretKey\n  sessionToken\n  path\n  key\n  bucket\n  expiresIn\n  store\n  __typename\n}'
        name = 'BigFileUploadGrant'
        type = 'BigFileUploadGrant'

class MediaUploadGrant(MikroFetchable, BaseModel):
    """A presigned PUT grant for uploading a media object."""
    typename: Literal['MediaUploadGrant'] = Field(alias='__typename', default='MediaUploadGrant', exclude=True)
    access_key: str = Field(alias='accessKey')
    secret_key: str = Field(alias='secretKey')
    session_token: str = Field(alias='sessionToken')
    path: str
    key: str
    bucket: str
    expires_in: int = Field(alias='expiresIn')
    max_bytes: int = Field(alias='maxBytes')
    store: str
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for MediaUploadGrant"""
        document = 'fragment MediaUploadGrant on MediaUploadGrant {\n  accessKey\n  secretKey\n  sessionToken\n  path\n  key\n  bucket\n  expiresIn\n  maxBytes\n  store\n  __typename\n}'
        name = 'MediaUploadGrant'
        type = 'MediaUploadGrant'

class ZarrUploadGrant(MikroFetchable, BaseModel):
    """Temporary S3 credentials for uploading a Zarr store."""
    typename: Literal['ZarrUploadGrant'] = Field(alias='__typename', default='ZarrUploadGrant', exclude=True)
    access_key: str = Field(alias='accessKey')
    secret_key: str = Field(alias='secretKey')
    session_token: str = Field(alias='sessionToken')
    path: str
    key: str
    bucket: str
    expires_in: int = Field(alias='expiresIn')
    max_bytes: int = Field(alias='maxBytes')
    store: str
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for ZarrUploadGrant"""
        document = 'fragment ZarrUploadGrant on ZarrUploadGrant {\n  accessKey\n  secretKey\n  sessionToken\n  path\n  key\n  bucket\n  expiresIn\n  maxBytes\n  store\n  __typename\n}'
        name = 'ZarrUploadGrant'
        type = 'ZarrUploadGrant'

class ParquetUploadGrant(MikroFetchable, BaseModel):
    """Temporary S3 credentials for uploading a parquet store."""
    typename: Literal['ParquetUploadGrant'] = Field(alias='__typename', default='ParquetUploadGrant', exclude=True)
    access_key: str = Field(alias='accessKey')
    secret_key: str = Field(alias='secretKey')
    session_token: str = Field(alias='sessionToken')
    path: str
    key: str
    bucket: str
    expires_in: int = Field(alias='expiresIn')
    max_bytes: int = Field(alias='maxBytes')
    store: str
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for ParquetUploadGrant"""
        document = 'fragment ParquetUploadGrant on ParquetUploadGrant {\n  accessKey\n  secretKey\n  sessionToken\n  path\n  key\n  bucket\n  expiresIn\n  maxBytes\n  store\n  __typename\n}'
        name = 'ParquetUploadGrant'
        type = 'ParquetUploadGrant'

class BigFileAccessGrant(MikroFetchable, BaseModel):
    """Temporary S3 credentials for reading a big file."""
    typename: Literal['BigFileAccessGrant'] = Field(alias='__typename', default='BigFileAccessGrant', exclude=True)
    access_key: str = Field(alias='accessKey')
    secret_key: str = Field(alias='secretKey')
    session_token: str = Field(alias='sessionToken')
    expires_in: int = Field(alias='expiresIn')
    path: str
    key: str
    bucket: str
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for BigFileAccessGrant"""
        document = 'fragment BigFileAccessGrant on BigFileAccessGrant {\n  accessKey\n  secretKey\n  sessionToken\n  expiresIn\n  path\n  key\n  bucket\n  __typename\n}'
        name = 'BigFileAccessGrant'
        type = 'BigFileAccessGrant'

class MediaAccessGrant(MikroFetchable, BaseModel):
    """Temporary S3 credentials for reading a media object."""
    typename: Literal['MediaAccessGrant'] = Field(alias='__typename', default='MediaAccessGrant', exclude=True)
    access_key: str = Field(alias='accessKey')
    secret_key: str = Field(alias='secretKey')
    session_token: str = Field(alias='sessionToken')
    expires_in: int = Field(alias='expiresIn')
    path: str
    key: str
    bucket: str
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for MediaAccessGrant"""
        document = 'fragment MediaAccessGrant on MediaAccessGrant {\n  accessKey\n  secretKey\n  sessionToken\n  expiresIn\n  path\n  key\n  bucket\n  __typename\n}'
        name = 'MediaAccessGrant'
        type = 'MediaAccessGrant'

class ZarrAccessGrant(MikroFetchable, BaseModel):
    """Temporary S3 credentials for reading a Zarr store."""
    typename: Literal['ZarrAccessGrant'] = Field(alias='__typename', default='ZarrAccessGrant', exclude=True)
    access_key: str = Field(alias='accessKey')
    secret_key: str = Field(alias='secretKey')
    session_token: str = Field(alias='sessionToken')
    expires_in: int = Field(alias='expiresIn')
    path: str
    key: str
    bucket: str
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for ZarrAccessGrant"""
        document = 'fragment ZarrAccessGrant on ZarrAccessGrant {\n  accessKey\n  secretKey\n  sessionToken\n  expiresIn\n  path\n  key\n  bucket\n  __typename\n}'
        name = 'ZarrAccessGrant'
        type = 'ZarrAccessGrant'

class ParquetAccessGrant(MikroFetchable, BaseModel):
    """Temporary S3 credentials for reading a parquet object."""
    typename: Literal['ParquetAccessGrant'] = Field(alias='__typename', default='ParquetAccessGrant', exclude=True)
    access_key: str = Field(alias='accessKey')
    secret_key: str = Field(alias='secretKey')
    session_token: str = Field(alias='sessionToken')
    expires_in: int = Field(alias='expiresIn')
    path: str
    key: str
    bucket: str
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for ParquetAccessGrant"""
        document = 'fragment ParquetAccessGrant on ParquetAccessGrant {\n  accessKey\n  secretKey\n  sessionToken\n  expiresIn\n  path\n  key\n  bucket\n  __typename\n}'
        name = 'ParquetAccessGrant'
        type = 'ParquetAccessGrant'

class DatasetParent(BaseModel):
    """A dataset is a collection of images and files. It mimics the concept of a folder in a file system and is the top-level container for organising data in mikro."""
    typename: Literal['Dataset'] = Field(alias='__typename', default='Dataset', exclude=True)
    id: ID
    name: str
    model_config = ConfigDict(frozen=True)

class Dataset(MikroFetchable, BaseModel):
    """A dataset is a collection of images and files. It mimics the concept of a folder in a file system and is the top-level container for organising data in mikro."""
    typename: Literal['Dataset'] = Field(alias='__typename', default='Dataset', exclude=True)
    id: ID
    name: str
    description: Optional[str] = Field(default=None)
    parent: Optional[DatasetParent] = Field(default=None)
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for Dataset"""
        document = 'fragment Dataset on Dataset {\n  id\n  name\n  description\n  parent {\n    id\n    name\n    __typename\n  }\n  __typename\n}'
        name = 'Dataset'
        type = 'Dataset'

class DimDescriptor(MikroFetchable, BaseModel):
    """A descriptor for a single named dimension of a dataset, recording its key, size and kind"""
    typename: Literal['DimDescriptor'] = Field(alias='__typename', default='DimDescriptor', exclude=True)
    key: str
    "The key of the dimension, e.g. 'x', 'y', 'z', 'c', or 't'"
    kind: DimensionKind
    "The kind of the dimension, e.g. 'space', 'channel', or 'time'"
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for DimDescriptor"""
        document = 'fragment DimDescriptor on DimDescriptor {\n  key\n  kind\n  __typename\n}'
        name = 'DimDescriptor'
        type = 'DimDescriptor'

class Era(MikroFetchable, BaseModel):
    """An era is a time space corresponding to an epoch on a microscope during an experiment. Clients use eras to contextualize images in real-world time via timepoint views."""
    typename: Literal['Era'] = Field(alias='__typename', default='Era', exclude=True)
    id: ID
    begin: Optional[datetime] = Field(default=None)
    name: str
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for Era"""
        document = 'fragment Era on Era {\n  id\n  begin\n  name\n  __typename\n}'
        name = 'Era'
        type = 'Era'

class ImageWithDataDatasetParent(BaseModel):
    """A dataset is a collection of images and files. It mimics the concept of a folder in a file system and is the top-level container for organising data in mikro."""
    typename: Literal['Dataset'] = Field(alias='__typename', default='Dataset', exclude=True)
    name: str
    model_config = ConfigDict(frozen=True)

class ImageWithDataDataset(BaseModel):
    """A dataset is a collection of images and files. It mimics the concept of a folder in a file system and is the top-level container for organising data in mikro."""
    typename: Literal['Dataset'] = Field(alias='__typename', default='Dataset', exclude=True)
    name: str
    parent: Optional[ImageWithDataDatasetParent] = Field(default=None)
    model_config = ConfigDict(frozen=True)

class ImageWithData(HasZarrStoreTrait, MikroFetchable, BaseModel):
    """An image. Images are the central data type in mikro: a single 5D bioimage whose binary data is stored in a ZarrStore. Images can be annotated with views (coordinate-ordered subsets of the image) and are the primary container that rois, metrics, renders and generated tables are bound to."""
    typename: Literal['Image'] = Field(alias='__typename', default='Image', exclude=True)
    id: ID
    dataset: Optional[ImageWithDataDataset] = Field(default=None)
    'The dataset this image belongs to'
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for ImageWithData"""
        document = 'fragment ImageWithData on Image {\n  id\n  dataset {\n    name\n    parent {\n      name\n      __typename\n    }\n    __typename\n  }\n  __typename\n}'
        name = 'ImageWithData'
        type = 'Image'

class Instrument(MikroFetchable, BaseModel):
    """A microscope or other instrument, identified by its manufacturer, model and serial number. Clients use it through optics views to record which instrument acquired an image."""
    typename: Literal['Instrument'] = Field(alias='__typename', default='Instrument', exclude=True)
    id: ID
    model: Optional[str] = Field(default=None)
    name: str
    serial_number: str = Field(alias='serialNumber')
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for Instrument"""
        document = 'fragment Instrument on Instrument {\n  id\n  model\n  name\n  serialNumber\n  __typename\n}'
        name = 'Instrument'
        type = 'Instrument'

class LayerScene(BaseModel):
    """The absolute coordinate universe in which layers are placed, with defined spatial and temporal base units"""
    typename: Literal['Scene'] = Field(alias='__typename', default='Scene', exclude=True)
    id: ID
    name: str
    model_config = ConfigDict(frozen=True)

class LayerLens(Lensable, BaseModel):
    """A Lens is a way of looking at a dataset: a dimensional selection (slices) over a dataset that defines a view of its data"""
    typename: Literal['Lens'] = Field(alias='__typename', default='Lens', exclude=True)
    id: ID
    model_config = ConfigDict(frozen=True)

class Layer(MikroFetchable, BaseModel):
    """The placement of a lens in a scene, including rendering settings such as colormap, contrast limits and an affine transformation matrix"""
    typename: Literal['Layer'] = Field(alias='__typename', default='Layer', exclude=True)
    scene: LayerScene
    lens: LayerLens
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for Layer"""
        document = 'fragment Layer on Layer {\n  scene {\n    id\n    name\n    __typename\n  }\n  lens {\n    id\n    __typename\n  }\n  __typename\n}'
        name = 'Layer'
        type = 'Layer'

class Slice(MikroFetchable, BaseModel):
    """A slice along a named dimension, with optional start, stop and step"""
    typename: Literal['Slice'] = Field(alias='__typename', default='Slice', exclude=True)
    dim: str
    "The key of the dimension, e.g. 'x', 'y', 'z', 'c', or 't'"
    start: Optional[int] = Field(default=None)
    'The starting index of the slice, or None to start from the beginning'
    stop: Optional[int] = Field(default=None)
    'The stopping index of the slice, or None to go to the end'
    step: Optional[int] = Field(default=None)
    'The step size of the slice, or None to use the default step'
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for Slice"""
        document = 'fragment Slice on Slice {\n  dim\n  start\n  stop\n  step\n  __typename\n}'
        name = 'Slice'
        type = 'Slice'

class Objective(MikroFetchable, BaseModel):
    """A microscope objective, described by its magnification, numerical aperture and immersion medium. Clients use it through optics views to record which objective an image was acquired with."""
    typename: Literal['Objective'] = Field(alias='__typename', default='Objective', exclude=True)
    id: ID
    na: Optional[float] = Field(default=None)
    name: str
    serial_number: str = Field(alias='serialNumber')
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for Objective"""
        document = 'fragment Objective on Objective {\n  id\n  na\n  name\n  serialNumber\n  __typename\n}'
        name = 'Objective'
        type = 'Objective'

class Scene(MikroFetchable, BaseModel):
    """The absolute coordinate universe in which layers are placed, with defined spatial and temporal base units"""
    typename: Literal['Scene'] = Field(alias='__typename', default='Scene', exclude=True)
    name: str
    id: ID
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for Scene"""
        document = 'fragment Scene on Scene {\n  name\n  id\n  __typename\n}'
        name = 'Scene'
        type = 'Scene'

class SnapshotStore(HasPresignedDownloadAccessor, BaseModel):
    """No documentation"""
    typename: Literal['MediaStore'] = Field(alias='__typename', default='MediaStore', exclude=True)
    key: str
    presigned_url: str = Field(alias='presignedUrl')
    'Compatibility field returning the canonical S3 object path.'
    model_config = ConfigDict(frozen=True)

class Snapshot(MikroFetchable, BaseModel):
    """A snapshot is a pre-rendered thumbnail image of an image. Clients use snapshots to display previews without loading the full underlying data."""
    typename: Literal['Snapshot'] = Field(alias='__typename', default='Snapshot', exclude=True)
    id: ID
    store: SnapshotStore
    name: str
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for Snapshot"""
        document = 'fragment Snapshot on Snapshot {\n  id\n  store {\n    key\n    presignedUrl\n    __typename\n  }\n  name\n  __typename\n}'
        name = 'Snapshot'
        type = 'Snapshot'

class StageAffineviewsImage(HasZarrStoreTrait, BaseModel):
    """An image. Images are the central data type in mikro: a single 5D bioimage whose binary data is stored in a ZarrStore. Images can be annotated with views (coordinate-ordered subsets of the image) and are the primary container that rois, metrics, renders and generated tables are bound to."""
    typename: Literal['Image'] = Field(alias='__typename', default='Image', exclude=True)
    id: ID
    model_config = ConfigDict(frozen=True)

class StageAffineviews(BaseModel):
    """A view placing an image region in physical space: a 4x4 affine matrix maps pixel coordinates onto a stage, encoding position and pixel size."""
    typename: Literal['AffineTransformationView'] = Field(alias='__typename', default='AffineTransformationView', exclude=True)
    affine_matrix: FourByFourMatrix = Field(alias='affineMatrix')
    image: StageAffineviewsImage
    model_config = ConfigDict(frozen=True)

class Stage(MikroFetchable, BaseModel):
    """A stage is a 3D space corresponding to the physical space on a microscope during an experiment. Clients use stages to contextualize images according to their real-world physical location via affine transformation views."""
    typename: Literal['Stage'] = Field(alias='__typename', default='Stage', exclude=True)
    id: ID
    name: str
    affine_views: Tuple[StageAffineviews, ...] = Field(alias='affineViews')
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for Stage"""
        document = 'fragment Stage on Stage {\n  id\n  name\n  affineViews {\n    affineMatrix\n    image {\n      id\n      __typename\n    }\n    __typename\n  }\n  __typename\n}'
        name = 'Stage'
        type = 'Stage'

class ZarrStore(HasZarrStoreAccessor, MikroFetchable, BaseModel):
    """No documentation"""
    typename: Literal['ZarrStore'] = Field(alias='__typename', default='ZarrStore', exclude=True)
    id: ID
    key: str
    bucket: str
    path: str
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for ZarrStore"""
        document = 'fragment ZarrStore on ZarrStore {\n  id\n  key\n  bucket\n  path\n  __typename\n}'
        name = 'ZarrStore'
        type = 'ZarrStore'

class ParquetStore(HasParquetStoreAccesor, MikroFetchable, BaseModel):
    """No documentation"""
    typename: Literal['ParquetStore'] = Field(alias='__typename', default='ParquetStore', exclude=True)
    id: ID
    key: str
    bucket: str
    path: str
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for ParquetStore"""
        document = 'fragment ParquetStore on ParquetStore {\n  id\n  key\n  bucket\n  path\n  __typename\n}'
        name = 'ParquetStore'
        type = 'ParquetStore'

class BigFileStore(HasDownloadAccessor, MikroFetchable, BaseModel):
    """A BigFileStore represents a large object stored behind the S3 datalayer."""
    typename: Literal['BigFileStore'] = Field(alias='__typename', default='BigFileStore', exclude=True)
    id: ID
    key: str
    bucket: str
    path: str
    presigned_url: str = Field(alias='presignedUrl')
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for BigFileStore"""
        document = 'fragment BigFileStore on BigFileStore {\n  id\n  key\n  bucket\n  path\n  presignedUrl\n  __typename\n}'
        name = 'BigFileStore'
        type = 'BigFileStore'

class MediaStore(HasPresignedDownloadAccessor, MikroFetchable, BaseModel):
    """No documentation"""
    typename: Literal['MediaStore'] = Field(alias='__typename', default='MediaStore', exclude=True)
    id: ID
    key: str
    bucket: str
    path: str
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for MediaStore"""
        document = 'fragment MediaStore on MediaStore {\n  id\n  key\n  bucket\n  path\n  __typename\n}'
        name = 'MediaStore'
        type = 'MediaStore'

class TableCellTable(HasParquestStoreTrait, BaseModel):
    """A table of tabular data, stored as a Parquet file. Tables are typically derived from images (e.g. measurements or localisations) and can be queried column- and row-wise through the API."""
    typename: Literal['Table'] = Field(alias='__typename', default='Table', exclude=True)
    id: ID
    model_config = ConfigDict(frozen=True)

class TableCellColumn(BaseModel):
    """A column descriptor"""
    typename: Literal['TableColumn'] = Field(alias='__typename', default='TableColumn', exclude=True)
    name: str
    model_config = ConfigDict(frozen=True)

class TableCell(MikroFetchable, BaseModel):
    """A cell of a table"""
    typename: Literal['TableCell'] = Field(alias='__typename', default='TableCell', exclude=True)
    id: ID
    table: TableCellTable
    value: Any
    column: TableCellColumn
    'The column this cell belongs to'
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for TableCell"""
        document = 'fragment TableCell on TableCell {\n  id\n  table {\n    id\n    __typename\n  }\n  value\n  column {\n    name\n    __typename\n  }\n  __typename\n}'
        name = 'TableCell'
        type = 'TableCell'

class TableRowTable(HasParquestStoreTrait, BaseModel):
    """A table of tabular data, stored as a Parquet file. Tables are typically derived from images (e.g. measurements or localisations) and can be queried column- and row-wise through the API."""
    typename: Literal['Table'] = Field(alias='__typename', default='Table', exclude=True)
    id: ID
    model_config = ConfigDict(frozen=True)

class TableRowColumns(BaseModel):
    """A column descriptor"""
    typename: Literal['TableColumn'] = Field(alias='__typename', default='TableColumn', exclude=True)
    name: str
    model_config = ConfigDict(frozen=True)

class TableRow(MikroFetchable, BaseModel):
    """A row of a table"""
    typename: Literal['TableRow'] = Field(alias='__typename', default='TableRow', exclude=True)
    id: ID
    values: Tuple[Any, ...]
    'The values of this row, one per column'
    table: TableRowTable
    columns: Tuple[TableRowColumns, ...]
    'The column descriptors of the table'
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for TableRow"""
        document = 'fragment TableRow on TableRow {\n  id\n  values\n  table {\n    id\n    __typename\n  }\n  columns {\n    name\n    __typename\n  }\n  __typename\n}'
        name = 'TableRow'
        type = 'TableRow'

class ChannelView(ViewChannelView, MikroFetchable, BaseModel):
    """A channel view describes an acquisition channel of an image, carrying its name and optical properties such as emission and excitation wavelengths."""
    typename: Literal['ChannelView'] = Field(alias='__typename', default='ChannelView', exclude=True)
    id: ID
    emission_wavelength: Optional[float] = Field(default=None, alias='emissionWavelength')
    'The emission wavelength of the channel in nanometers'
    excitation_wavelength: Optional[float] = Field(default=None, alias='excitationWavelength')
    'The excitation wavelength of the channel in nanometers'
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for ChannelView"""
        document = 'fragment View on View {\n  xMin\n  xMax\n  yMin\n  yMax\n  tMin\n  tMax\n  cMin\n  cMax\n  zMin\n  zMax\n  __typename\n}\n\nfragment ChannelView on ChannelView {\n  ...View\n  id\n  emissionWavelength\n  excitationWavelength\n  __typename\n}'
        name = 'ChannelView'
        type = 'ChannelView'

class ReferenceView(ViewReferenceView, MikroFetchable, BaseModel):
    """A view marking an image region as the reference that other views (e.g. mask views) point back to, for example the raw channel a segmentation mask was computed from."""
    typename: Literal['ReferenceView'] = Field(alias='__typename', default='ReferenceView', exclude=True)
    id: ID
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for ReferenceView"""
        document = 'fragment View on View {\n  xMin\n  xMax\n  yMin\n  yMax\n  tMin\n  tMax\n  cMin\n  cMax\n  zMin\n  zMax\n  __typename\n}\n\nfragment ReferenceView on ReferenceView {\n  ...View\n  id\n  __typename\n}'
        name = 'ReferenceView'
        type = 'ReferenceView'

class DerivedViewOriginimage(HasZarrStoreTrait, BaseModel):
    """An image. Images are the central data type in mikro: a single 5D bioimage whose binary data is stored in a ZarrStore. Images can be annotated with views (coordinate-ordered subsets of the image) and are the primary container that rois, metrics, renders and generated tables are bound to."""
    typename: Literal['Image'] = Field(alias='__typename', default='Image', exclude=True)
    id: ID
    name: str
    'The name of the image'
    model_config = ConfigDict(frozen=True)

class DerivedView(ViewDerivedView, MikroFetchable, BaseModel):
    """A derived view establishes a processing relationship between two images, guaranteeing that the derived image shares the same coordinate system as its origin image so the two can be trivially overlayed and compared (e.g. a segmentation over its source image). Cropped or projected images are not derived views, as they do not share the coordinate system."""
    typename: Literal['DerivedView'] = Field(alias='__typename', default='DerivedView', exclude=True)
    id: ID
    origin_image: DerivedViewOriginimage = Field(alias='originImage')
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for DerivedView"""
        document = 'fragment View on View {\n  xMin\n  xMax\n  yMin\n  yMax\n  tMin\n  tMax\n  cMin\n  cMax\n  zMin\n  zMax\n  __typename\n}\n\nfragment DerivedView on DerivedView {\n  ...View\n  id\n  originImage {\n    id\n    name\n    __typename\n  }\n  __typename\n}'
        name = 'DerivedView'
        type = 'DerivedView'

class HistogramView(ViewHistogramView, MikroFetchable, BaseModel):
    """A histogram view describes the distribution of pixel values in a subset of an image, providing bins, min/max bounds and the histogram counts. Useful for clients that want to display or auto-scale contrast."""
    typename: Literal['HistogramView'] = Field(alias='__typename', default='HistogramView', exclude=True)
    id: ID
    histogram: Tuple[float, ...]
    bins: Tuple[float, ...]
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for HistogramView"""
        document = 'fragment View on View {\n  xMin\n  xMax\n  yMin\n  yMax\n  tMin\n  tMax\n  cMin\n  cMax\n  zMin\n  zMax\n  __typename\n}\n\nfragment HistogramView on HistogramView {\n  ...View\n  id\n  histogram\n  bins\n  __typename\n}'
        name = 'HistogramView'
        type = 'HistogramView'

class ROIViewRoi(IsVectorizableTrait, BaseModel):
    """A region of interest drawn on an image, defined by a list of 5D vectors (c, t, z, y, x) and a kind (rectangle, path, point, ...). Use ROIs to mark and share structures of interest."""
    typename: Literal['ROI'] = Field(alias='__typename', default='ROI', exclude=True)
    id: ID
    name: str
    model_config = ConfigDict(frozen=True)

class ROIView(ViewROIView, MikroFetchable, BaseModel):
    """A ROI view establishes a relationship between an image region and a region of interest, e.g. recording that this image was cropped from the area described by the ROI on another image."""
    typename: Literal['ROIView'] = Field(alias='__typename', default='ROIView', exclude=True)
    id: ID
    roi: ROIViewRoi
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for ROIView"""
        document = 'fragment View on View {\n  xMin\n  xMax\n  yMin\n  yMax\n  tMin\n  tMax\n  cMin\n  cMax\n  zMin\n  zMax\n  __typename\n}\n\nfragment ROIView on ROIView {\n  ...View\n  id\n  roi {\n    id\n    name\n    __typename\n  }\n  __typename\n}'
        name = 'ROIView'
        type = 'ROIView'

class FileViewFile(FileTrait, BaseModel):
    """A file in its original format (e.g. a microscopy vendor file), stored in a BigFileStore. Files are the raw sources that images are converted from, and file views link back to the images that originated from them."""
    typename: Literal['File'] = Field(alias='__typename', default='File', exclude=True)
    id: ID
    name: str
    model_config = ConfigDict(frozen=True)

class FileView(ViewFileView, MikroFetchable, BaseModel):
    """A file view establishes a relationship between an image and a file: it records that this view of the image was originally part of the file (optionally a specific series within it) and links back to the source file."""
    typename: Literal['FileView'] = Field(alias='__typename', default='FileView', exclude=True)
    id: ID
    series_identifier: Optional[str] = Field(default=None, alias='seriesIdentifier')
    file: FileViewFile
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for FileView"""
        document = 'fragment View on View {\n  xMin\n  xMax\n  yMin\n  yMax\n  tMin\n  tMax\n  cMin\n  cMax\n  zMin\n  zMax\n  __typename\n}\n\nfragment FileView on FileView {\n  ...View\n  id\n  seriesIdentifier\n  file {\n    id\n    name\n    __typename\n  }\n  __typename\n}'
        name = 'FileView'
        type = 'FileView'

class AffineTransformationViewStage(BaseModel):
    """A stage is a 3D space corresponding to the physical space on a microscope during an experiment. Clients use stages to contextualize images according to their real-world physical location via affine transformation views."""
    typename: Literal['Stage'] = Field(alias='__typename', default='Stage', exclude=True)
    id: ID
    name: str
    model_config = ConfigDict(frozen=True)

class AffineTransformationView(ViewAffineTransformationView, MikroFetchable, BaseModel):
    """A view placing an image region in physical space: a 4x4 affine matrix maps pixel coordinates onto a stage, encoding position and pixel size."""
    typename: Literal['AffineTransformationView'] = Field(alias='__typename', default='AffineTransformationView', exclude=True)
    id: ID
    affine_matrix: FourByFourMatrix = Field(alias='affineMatrix')
    stage: AffineTransformationViewStage
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for AffineTransformationView"""
        document = 'fragment View on View {\n  xMin\n  xMax\n  yMin\n  yMax\n  tMin\n  tMax\n  cMin\n  cMax\n  zMin\n  zMax\n  __typename\n}\n\nfragment AffineTransformationView on AffineTransformationView {\n  ...View\n  id\n  affineMatrix\n  stage {\n    id\n    name\n    __typename\n  }\n  __typename\n}'
        name = 'AffineTransformationView'
        type = 'AffineTransformationView'

class OpticsViewObjective(BaseModel):
    """A microscope objective, described by its magnification, numerical aperture and immersion medium. Clients use it through optics views to record which objective an image was acquired with."""
    typename: Literal['Objective'] = Field(alias='__typename', default='Objective', exclude=True)
    id: ID
    name: str
    serial_number: str = Field(alias='serialNumber')
    model_config = ConfigDict(frozen=True)

class OpticsViewCamera(BaseModel):
    """A camera (detector) on a microscope, described by its sensor dimensions, pixel sizes and bit depth. Clients use it through optics views to record which detector acquired an image."""
    typename: Literal['Camera'] = Field(alias='__typename', default='Camera', exclude=True)
    id: ID
    name: str
    serial_number: str = Field(alias='serialNumber')
    model_config = ConfigDict(frozen=True)

class OpticsViewInstrument(BaseModel):
    """A microscope or other instrument, identified by its manufacturer, model and serial number. Clients use it through optics views to record which instrument acquired an image."""
    typename: Literal['Instrument'] = Field(alias='__typename', default='Instrument', exclude=True)
    id: ID
    name: str
    serial_number: str = Field(alias='serialNumber')
    model_config = ConfigDict(frozen=True)

class OpticsView(ViewOpticsView, MikroFetchable, BaseModel):
    """A view describing the optics used to acquire an image region: the instrument, objective and camera. Use it to inspect or compare acquisition hardware settings."""
    typename: Literal['OpticsView'] = Field(alias='__typename', default='OpticsView', exclude=True)
    id: ID
    objective: Optional[OpticsViewObjective] = Field(default=None)
    camera: Optional[OpticsViewCamera] = Field(default=None)
    instrument: Optional[OpticsViewInstrument] = Field(default=None)
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for OpticsView"""
        document = 'fragment View on View {\n  xMin\n  xMax\n  yMin\n  yMax\n  tMin\n  tMax\n  cMin\n  cMax\n  zMin\n  zMax\n  __typename\n}\n\nfragment OpticsView on OpticsView {\n  ...View\n  id\n  objective {\n    id\n    name\n    serialNumber\n    __typename\n  }\n  camera {\n    id\n    name\n    serialNumber\n    __typename\n  }\n  instrument {\n    id\n    name\n    serialNumber\n    __typename\n  }\n  __typename\n}'
        name = 'OpticsView'
        type = 'OpticsView'

class AcquisitionViewOperator(BaseModel):
    """A user account. The sub is the stable subject identifier from the identity provider; creator and assigner fields across the API reference this type."""
    typename: Literal['User'] = Field(alias='__typename', default='User', exclude=True)
    sub: str
    model_config = ConfigDict(frozen=True)

class AcquisitionView(ViewAcquisitionView, MikroFetchable, BaseModel):
    """A view recording when and by whom an image region was acquired at the microscope. Use it to trace an image back to its acquisition session and operator."""
    typename: Literal['AcquisitionView'] = Field(alias='__typename', default='AcquisitionView', exclude=True)
    id: ID
    description: Optional[str] = Field(default=None)
    acquired_at: Optional[datetime] = Field(default=None, alias='acquiredAt')
    operator: Optional[AcquisitionViewOperator] = Field(default=None)
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for AcquisitionView"""
        document = 'fragment View on View {\n  xMin\n  xMax\n  yMin\n  yMax\n  tMin\n  tMax\n  cMin\n  cMax\n  zMin\n  zMax\n  __typename\n}\n\nfragment AcquisitionView on AcquisitionView {\n  ...View\n  id\n  description\n  acquiredAt\n  operator {\n    sub\n    __typename\n  }\n  __typename\n}'
        name = 'AcquisitionView'
        type = 'AcquisitionView'

class WellPositionViewWell(BaseModel):
    """A multi-well plate with a grid of rows and columns used during acquisition. Clients use it to locate images within specific wells via well position views."""
    typename: Literal['MultiWellPlate'] = Field(alias='__typename', default='MultiWellPlate', exclude=True)
    id: ID
    rows: Optional[int] = Field(default=None)
    columns: Optional[int] = Field(default=None)
    name: Optional[str] = Field(default=None)
    model_config = ConfigDict(frozen=True)

class WellPositionView(ViewWellPositionView, MikroFetchable, BaseModel):
    """A view mapping an image region to a well (row/column) of a multi well plate, so plate-based acquisitions can be traced back to their well."""
    typename: Literal['WellPositionView'] = Field(alias='__typename', default='WellPositionView', exclude=True)
    id: ID
    column: Optional[int] = Field(default=None)
    row: Optional[int] = Field(default=None)
    well: Optional[WellPositionViewWell] = Field(default=None)
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for WellPositionView"""
        document = 'fragment View on View {\n  xMin\n  xMax\n  yMin\n  yMax\n  tMin\n  tMax\n  cMin\n  cMax\n  zMin\n  zMax\n  __typename\n}\n\nfragment WellPositionView on WellPositionView {\n  ...View\n  id\n  column\n  row\n  well {\n    id\n    rows\n    columns\n    name\n    __typename\n  }\n  __typename\n}'
        name = 'WellPositionView'
        type = 'WellPositionView'

class ContinousScanView(ViewContinousScanView, MikroFetchable, BaseModel):
    """A view marking an image region as acquired by a continuous scan, recording the direction the scan traversed the axes in."""
    typename: Literal['ContinousScanView'] = Field(alias='__typename', default='ContinousScanView', exclude=True)
    id: ID
    direction: ScanDirection
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for ContinousScanView"""
        document = 'fragment View on View {\n  xMin\n  xMax\n  yMin\n  yMax\n  tMin\n  tMax\n  cMin\n  cMax\n  zMin\n  zMax\n  __typename\n}\n\nfragment ContinousScanView on ContinousScanView {\n  ...View\n  id\n  direction\n  __typename\n}'
        name = 'ContinousScanView'
        type = 'ContinousScanView'

class TimepointView(ViewTimepointView, MikroFetchable, BaseModel):
    """A view anchoring an image region in real time: it places the region within an era (a named time epoch on the microscope) at a millisecond offset or frame index since its start."""
    typename: Literal['TimepointView'] = Field(alias='__typename', default='TimepointView', exclude=True)
    id: ID
    ms_since_start: Optional[Milliseconds] = Field(default=None, alias='msSinceStart')
    index_since_start: Optional[int] = Field(default=None, alias='indexSinceStart')
    era: Era
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for TimepointView"""
        document = 'fragment Era on Era {\n  id\n  begin\n  name\n  __typename\n}\n\nfragment View on View {\n  xMin\n  xMax\n  yMin\n  yMax\n  tMin\n  tMax\n  cMin\n  cMax\n  zMin\n  zMax\n  __typename\n}\n\nfragment TimepointView on TimepointView {\n  ...View\n  id\n  msSinceStart\n  indexSinceStart\n  era {\n    ...Era\n    __typename\n  }\n  __typename\n}'
        name = 'TimepointView'
        type = 'TimepointView'

class RGBViewContexts(BaseModel):
    """An RGB context is a collection of RGB views that together describe how an image should be rendered in RGB, e.g. grouping the views that represent each channel with its color map and contrast settings."""
    typename: Literal['RGBContext'] = Field(alias='__typename', default='RGBContext', exclude=True)
    id: ID
    name: str
    model_config = ConfigDict(frozen=True)

class RGBViewImageDerivedscaleviewsImage(HasZarrStoreTrait, BaseModel):
    """An image. Images are the central data type in mikro: a single 5D bioimage whose binary data is stored in a ZarrStore. Images can be annotated with views (coordinate-ordered subsets of the image) and are the primary container that rois, metrics, renders and generated tables are bound to."""
    typename: Literal['Image'] = Field(alias='__typename', default='Image', exclude=True)
    id: ID
    store: ZarrStore
    'The store where the image data is stored.'
    model_config = ConfigDict(frozen=True)

class RGBViewImageDerivedscaleviews(BaseModel):
    """A view linking an image to a downscaled version of another image. Scale views form the levels of a multiscale pyramid: the parent is the full-resolution image and the scale factors give the downsampling per dimension."""
    typename: Literal['ScaleView'] = Field(alias='__typename', default='ScaleView', exclude=True)
    id: ID
    image: RGBViewImageDerivedscaleviewsImage
    scale_x: float = Field(alias='scaleX')
    scale_y: float = Field(alias='scaleY')
    scale_z: float = Field(alias='scaleZ')
    scale_t: float = Field(alias='scaleT')
    scale_c: float = Field(alias='scaleC')
    model_config = ConfigDict(frozen=True)

class RGBViewImage(HasZarrStoreTrait, BaseModel):
    """An image. Images are the central data type in mikro: a single 5D bioimage whose binary data is stored in a ZarrStore. Images can be annotated with views (coordinate-ordered subsets of the image) and are the primary container that rois, metrics, renders and generated tables are bound to."""
    typename: Literal['Image'] = Field(alias='__typename', default='Image', exclude=True)
    id: ID
    store: ZarrStore
    'The store where the image data is stored.'
    derived_scale_views: Tuple[RGBViewImageDerivedscaleviews, ...] = Field(alias='derivedScaleViews')
    'Scale views derived from this image'
    model_config = ConfigDict(frozen=True)

class RGBView(ViewRGBView, MikroFetchable, BaseModel):
    """An RGB view describes how a subset of an image (typically a channel) is rendered in RGB within an RGB context, carrying color map, gamma and contrast limit settings."""
    typename: Literal['RGBView'] = Field(alias='__typename', default='RGBView', exclude=True)
    id: ID
    contexts: Tuple[RGBViewContexts, ...]
    name: str
    image: RGBViewImage
    color_map: ColorMap = Field(alias='colorMap')
    contrast_limit_min: Optional[float] = Field(default=None, alias='contrastLimitMin')
    contrast_limit_max: Optional[float] = Field(default=None, alias='contrastLimitMax')
    gamma: Optional[float] = Field(default=None)
    active: bool
    full_colour: str = Field(alias='fullColour')
    base_color: Optional[Tuple[int, ...]] = Field(default=None, alias='baseColor')
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for RGBView"""
        document = 'fragment View on View {\n  xMin\n  xMax\n  yMin\n  yMax\n  tMin\n  tMax\n  cMin\n  cMax\n  zMin\n  zMax\n  __typename\n}\n\nfragment ZarrStore on ZarrStore {\n  id\n  key\n  bucket\n  path\n  __typename\n}\n\nfragment RGBView on RGBView {\n  ...View\n  id\n  contexts {\n    id\n    name\n    __typename\n  }\n  name\n  image {\n    id\n    store {\n      ...ZarrStore\n      __typename\n    }\n    derivedScaleViews {\n      id\n      image {\n        id\n        store {\n          ...ZarrStore\n          __typename\n        }\n        __typename\n      }\n      scaleX\n      scaleY\n      scaleZ\n      scaleT\n      scaleC\n      __typename\n    }\n    __typename\n  }\n  colorMap\n  contrastLimitMin\n  contrastLimitMax\n  gamma\n  active\n  fullColour\n  baseColor\n  __typename\n}'
        name = 'RGBView'
        type = 'RGBView'

class DataRoiDatasetDataarrays(DataArrayTrait, BaseModel):
    """A single scale of a dataset's multiscale pyramid: a zarr-backed array described by its shape, chunk shape, scale factors and pyramid level"""
    typename: Literal['DataArray'] = Field(alias='__typename', default='DataArray', exclude=True)
    id: ID
    store: ZarrStore
    model_config = ConfigDict(frozen=True)

class DataRoiDataset(DatasetTrait, BaseModel):
    """A multi-dimensional array dataset with named dimensions. It can have multiple scales attached to it, which are represented as DataArrays"""
    typename: Literal['ADataset'] = Field(alias='__typename', default='ADataset', exclude=True)
    id: ID
    dim_descriptors: Tuple[DimDescriptor, ...] = Field(alias='dimDescriptors')
    data_arrays: Tuple[DataRoiDatasetDataarrays, ...] = Field(alias='dataArrays')
    'The multiscale data arrays belonging to this dataset'
    model_config = ConfigDict(frozen=True)

class DataRoi(MikroFetchable, BaseModel):
    """A region of interest in a data array, described by its vectors and per-dimension constraints"""
    typename: Literal['DataRoi'] = Field(alias='__typename', default='DataRoi', exclude=True)
    id: str
    dataset: DataRoiDataset
    vectors: Tuple[Tuple[float, ...], ...]
    kind: RoiKind
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for DataRoi"""
        document = 'fragment DimDescriptor on DimDescriptor {\n  key\n  kind\n  __typename\n}\n\nfragment ZarrStore on ZarrStore {\n  id\n  key\n  bucket\n  path\n  __typename\n}\n\nfragment DataRoi on DataRoi {\n  id\n  dataset {\n    id\n    dimDescriptors {\n      ...DimDescriptor\n      __typename\n    }\n    dataArrays {\n      id\n      store {\n        ...ZarrStore\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  vectors\n  kind\n  __typename\n}'
        name = 'DataRoi'
        type = 'DataRoi'

class LensDatasetDataarrays(DataArrayTrait, BaseModel):
    """A single scale of a dataset's multiscale pyramid: a zarr-backed array described by its shape, chunk shape, scale factors and pyramid level"""
    typename: Literal['DataArray'] = Field(alias='__typename', default='DataArray', exclude=True)
    id: ID
    level: int
    store: ZarrStore
    model_config = ConfigDict(frozen=True)

class LensDataset(DatasetTrait, BaseModel):
    """A multi-dimensional array dataset with named dimensions. It can have multiple scales attached to it, which are represented as DataArrays"""
    typename: Literal['ADataset'] = Field(alias='__typename', default='ADataset', exclude=True)
    id: ID
    dims: Tuple[str, ...]
    data_arrays: Tuple[LensDatasetDataarrays, ...] = Field(alias='dataArrays')
    'The multiscale data arrays belonging to this dataset'
    model_config = ConfigDict(frozen=True)

class Lens(Lensable, MikroFetchable, BaseModel):
    """A Lens is a way of looking at a dataset: a dimensional selection (slices) over a dataset that defines a view of its data"""
    typename: Literal['Lens'] = Field(alias='__typename', default='Lens', exclude=True)
    id: ID
    dataset: LensDataset
    shape: Tuple[int, ...]
    dims: Tuple[str, ...]
    dim_descriptors: Tuple[DimDescriptor, ...] = Field(alias='dimDescriptors')
    slices: Tuple[Slice, ...]
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for Lens"""
        document = 'fragment DimDescriptor on DimDescriptor {\n  key\n  kind\n  __typename\n}\n\nfragment Slice on Slice {\n  dim\n  start\n  stop\n  step\n  __typename\n}\n\nfragment ZarrStore on ZarrStore {\n  id\n  key\n  bucket\n  path\n  __typename\n}\n\nfragment Lens on Lens {\n  id\n  dataset {\n    id\n    dims\n    dataArrays {\n      id\n      level\n      store {\n        ...ZarrStore\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  shape\n  dims\n  dimDescriptors {\n    ...DimDescriptor\n    __typename\n  }\n  slices {\n    ...Slice\n    __typename\n  }\n  __typename\n}'
        name = 'Lens'
        type = 'Lens'

class ROIImage(HasZarrStoreTrait, BaseModel):
    """An image. Images are the central data type in mikro: a single 5D bioimage whose binary data is stored in a ZarrStore. Images can be annotated with views (coordinate-ordered subsets of the image) and are the primary container that rois, metrics, renders and generated tables are bound to."""
    typename: Literal['Image'] = Field(alias='__typename', default='Image', exclude=True)
    id: ID
    store: ZarrStore
    'The store where the image data is stored.'
    model_config = ConfigDict(frozen=True)

class ROI(IsVectorizableTrait, MikroFetchable, BaseModel):
    """A region of interest drawn on an image, defined by a list of 5D vectors (c, t, z, y, x) and a kind (rectangle, path, point, ...). Use ROIs to mark and share structures of interest."""
    typename: Literal['ROI'] = Field(alias='__typename', default='ROI', exclude=True)
    id: ID
    image: ROIImage
    vectors: Tuple[FiveDVector, ...]
    kind: RoiKind
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for ROI"""
        document = 'fragment ZarrStore on ZarrStore {\n  id\n  key\n  bucket\n  path\n  __typename\n}\n\nfragment ROI on ROI {\n  id\n  image {\n    id\n    store {\n      ...ZarrStore\n      __typename\n    }\n    __typename\n  }\n  vectors\n  kind\n  __typename\n}'
        name = 'ROI'
        type = 'ROI'

class TableOrigins(HasZarrStoreTrait, BaseModel):
    """An image. Images are the central data type in mikro: a single 5D bioimage whose binary data is stored in a ZarrStore. Images can be annotated with views (coordinate-ordered subsets of the image) and are the primary container that rois, metrics, renders and generated tables are bound to."""
    typename: Literal['Image'] = Field(alias='__typename', default='Image', exclude=True)
    id: ID
    model_config = ConfigDict(frozen=True)

class Table(HasParquestStoreTrait, MikroFetchable, BaseModel):
    """A table of tabular data, stored as a Parquet file. Tables are typically derived from images (e.g. measurements or localisations) and can be queried column- and row-wise through the API."""
    typename: Literal['Table'] = Field(alias='__typename', default='Table', exclude=True)
    origins: Tuple[TableOrigins, ...]
    id: ID
    name: str
    store: ParquetStore
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for Table"""
        document = 'fragment ParquetStore on ParquetStore {\n  id\n  key\n  bucket\n  path\n  __typename\n}\n\nfragment Table on Table {\n  origins {\n    id\n    __typename\n  }\n  id\n  name\n  store {\n    ...ParquetStore\n    __typename\n  }\n  __typename\n}'
        name = 'Table'
        type = 'Table'

class FileOrigins(HasZarrStoreTrait, BaseModel):
    """An image. Images are the central data type in mikro: a single 5D bioimage whose binary data is stored in a ZarrStore. Images can be annotated with views (coordinate-ordered subsets of the image) and are the primary container that rois, metrics, renders and generated tables are bound to."""
    typename: Literal['Image'] = Field(alias='__typename', default='Image', exclude=True)
    id: ID
    model_config = ConfigDict(frozen=True)

class File(FileTrait, MikroFetchable, BaseModel):
    """A file in its original format (e.g. a microscopy vendor file), stored in a BigFileStore. Files are the raw sources that images are converted from, and file views link back to the images that originated from them."""
    typename: Literal['File'] = Field(alias='__typename', default='File', exclude=True)
    origins: Tuple[FileOrigins, ...]
    id: ID
    name: str
    store: BigFileStore
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for File"""
        document = 'fragment BigFileStore on BigFileStore {\n  id\n  key\n  bucket\n  path\n  presignedUrl\n  __typename\n}\n\nfragment File on File {\n  origins {\n    id\n    __typename\n  }\n  id\n  name\n  store {\n    ...BigFileStore\n    __typename\n  }\n  __typename\n}'
        name = 'File'
        type = 'File'

class Mesh(MikroFetchable, BaseModel):
    """A 3D mesh belonging to a dataset, with its geometry kept in a big file store. Clients use it to download or visualize surface reconstructions derived from image data."""
    typename: Literal['Mesh'] = Field(alias='__typename', default='Mesh', exclude=True)
    id: ID
    name: str
    store: BigFileStore
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for Mesh"""
        document = 'fragment BigFileStore on BigFileStore {\n  id\n  key\n  bucket\n  path\n  presignedUrl\n  __typename\n}\n\nfragment Mesh on Mesh {\n  id\n  name\n  store {\n    ...BigFileStore\n    __typename\n  }\n  __typename\n}'
        name = 'Mesh'
        type = 'Mesh'

class MaskView(ViewMaskView, MikroFetchable, BaseModel):
    """A view marking an image region as a semantic segmentation mask, where pixel values are class labels. It points to the reference view it was computed from and can carry a label table."""
    typename: Literal['MaskView'] = Field(alias='__typename', default='MaskView', exclude=True)
    id: ID
    reference_view: ReferenceView = Field(alias='referenceView')
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for MaskView"""
        document = 'fragment ReferenceView on ReferenceView {\n  ...View\n  id\n  __typename\n}\n\nfragment View on View {\n  xMin\n  xMax\n  yMin\n  yMax\n  tMin\n  tMax\n  cMin\n  cMax\n  zMin\n  zMax\n  __typename\n}\n\nfragment MaskView on MaskView {\n  ...View\n  id\n  referenceView {\n    ...ReferenceView\n    __typename\n  }\n  __typename\n}'
        name = 'MaskView'
        type = 'MaskView'

class InstanceMaskView(ViewInstanceMaskView, MikroFetchable, BaseModel):
    """A view marking an image region as an instance segmentation mask, where each pixel value identifies an individual object instance. It points to the reference view it was computed from and can carry a per-instance label table."""
    typename: Literal['InstanceMaskView'] = Field(alias='__typename', default='InstanceMaskView', exclude=True)
    id: ID
    reference_view: ReferenceView = Field(alias='referenceView')
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for InstanceMaskView"""
        document = 'fragment ReferenceView on ReferenceView {\n  ...View\n  id\n  __typename\n}\n\nfragment View on View {\n  xMin\n  xMax\n  yMin\n  yMax\n  tMin\n  tMax\n  cMin\n  cMax\n  zMin\n  zMax\n  __typename\n}\n\nfragment InstanceMaskView on InstanceMaskView {\n  ...View\n  id\n  referenceView {\n    ...ReferenceView\n    __typename\n  }\n  __typename\n}'
        name = 'InstanceMaskView'
        type = 'InstanceMaskView'

class RGBContextImage(HasZarrStoreTrait, BaseModel):
    """An image. Images are the central data type in mikro: a single 5D bioimage whose binary data is stored in a ZarrStore. Images can be annotated with views (coordinate-ordered subsets of the image) and are the primary container that rois, metrics, renders and generated tables are bound to."""
    typename: Literal['Image'] = Field(alias='__typename', default='Image', exclude=True)
    id: ID
    store: ZarrStore
    'The store where the image data is stored.'
    model_config = ConfigDict(frozen=True)

class RGBContext(MikroFetchable, BaseModel):
    """An RGB context is a collection of RGB views that together describe how an image should be rendered in RGB, e.g. grouping the views that represent each channel with its color map and contrast settings."""
    typename: Literal['RGBContext'] = Field(alias='__typename', default='RGBContext', exclude=True)
    id: ID
    views: Tuple[RGBView, ...]
    image: RGBContextImage
    pinned: bool
    name: str
    z: int
    t: int
    c: int
    blending: Blending
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for RGBContext"""
        document = 'fragment View on View {\n  xMin\n  xMax\n  yMin\n  yMax\n  tMin\n  tMax\n  cMin\n  cMax\n  zMin\n  zMax\n  __typename\n}\n\nfragment RGBView on RGBView {\n  ...View\n  id\n  contexts {\n    id\n    name\n    __typename\n  }\n  name\n  image {\n    id\n    store {\n      ...ZarrStore\n      __typename\n    }\n    derivedScaleViews {\n      id\n      image {\n        id\n        store {\n          ...ZarrStore\n          __typename\n        }\n        __typename\n      }\n      scaleX\n      scaleY\n      scaleZ\n      scaleT\n      scaleC\n      __typename\n    }\n    __typename\n  }\n  colorMap\n  contrastLimitMin\n  contrastLimitMax\n  gamma\n  active\n  fullColour\n  baseColor\n  __typename\n}\n\nfragment ZarrStore on ZarrStore {\n  id\n  key\n  bucket\n  path\n  __typename\n}\n\nfragment RGBContext on RGBContext {\n  id\n  views {\n    ...RGBView\n    __typename\n  }\n  image {\n    id\n    store {\n      ...ZarrStore\n      __typename\n    }\n    __typename\n  }\n  pinned\n  name\n  z\n  t\n  c\n  blending\n  __typename\n}'
        name = 'RGBContext'
        type = 'RGBContext'

class ImageViewsBase(BaseModel):
    """A view is a subset of an image, delimited by its coordinates (c, t, z, x, y) within the 5D array. Views attach metadata (channels, labels, transformations, timepoints, ...) to that subregion of the image."""
    model_config = ConfigDict(frozen=True)

class ImageViewsBaseAcquisitionView(AcquisitionView, ImageViewsBase, BaseModel):
    """A view recording when and by whom an image region was acquired at the microscope. Use it to trace an image back to its acquisition session and operator."""
    typename: Literal['AcquisitionView'] = Field(alias='__typename', default='AcquisitionView', exclude=True)

class ImageViewsBaseAffineTransformationView(AffineTransformationView, ImageViewsBase, BaseModel):
    """A view placing an image region in physical space: a 4x4 affine matrix maps pixel coordinates onto a stage, encoding position and pixel size."""
    typename: Literal['AffineTransformationView'] = Field(alias='__typename', default='AffineTransformationView', exclude=True)

class ImageViewsBaseChannelView(ChannelView, ImageViewsBase, BaseModel):
    """A channel view describes an acquisition channel of an image, carrying its name and optical properties such as emission and excitation wavelengths."""
    typename: Literal['ChannelView'] = Field(alias='__typename', default='ChannelView', exclude=True)

class ImageViewsBaseContinousScanView(ContinousScanView, ImageViewsBase, BaseModel):
    """A view marking an image region as acquired by a continuous scan, recording the direction the scan traversed the axes in."""
    typename: Literal['ContinousScanView'] = Field(alias='__typename', default='ContinousScanView', exclude=True)

class ImageViewsBaseDerivedView(DerivedView, ImageViewsBase, BaseModel):
    """A derived view establishes a processing relationship between two images, guaranteeing that the derived image shares the same coordinate system as its origin image so the two can be trivially overlayed and compared (e.g. a segmentation over its source image). Cropped or projected images are not derived views, as they do not share the coordinate system."""
    typename: Literal['DerivedView'] = Field(alias='__typename', default='DerivedView', exclude=True)

class ImageViewsBaseFileView(FileView, ImageViewsBase, BaseModel):
    """A file view establishes a relationship between an image and a file: it records that this view of the image was originally part of the file (optionally a specific series within it) and links back to the source file."""
    typename: Literal['FileView'] = Field(alias='__typename', default='FileView', exclude=True)

class ImageViewsBaseHistogramView(ImageViewsBase, BaseModel):
    """A histogram view describes the distribution of pixel values in a subset of an image, providing bins, min/max bounds and the histogram counts. Useful for clients that want to display or auto-scale contrast."""
    typename: Literal['HistogramView'] = Field(alias='__typename', default='HistogramView', exclude=True)

class ImageViewsBaseInstanceMaskView(ImageViewsBase, BaseModel):
    """A view marking an image region as an instance segmentation mask, where each pixel value identifies an individual object instance. It points to the reference view it was computed from and can carry a per-instance label table."""
    typename: Literal['InstanceMaskView'] = Field(alias='__typename', default='InstanceMaskView', exclude=True)

class ImageViewsBaseLabelView(ImageViewsBase, BaseModel):
    """A label view gives a label to a specific image channel, e.g. mapping an antibody to the channel it stains, so the labeling agent can be easily identified. Labels can also be used for other purposes, such as marking a channel as poor quality."""
    typename: Literal['LabelView'] = Field(alias='__typename', default='LabelView', exclude=True)

class ImageViewsBaseLightpathView(ImageViewsBase, BaseModel):
    """A view attaching the optical path (light sources, filters, detectors and their connections) that light travelled through when this image region was acquired."""
    typename: Literal['LightpathView'] = Field(alias='__typename', default='LightpathView', exclude=True)

class ImageViewsBaseMaskView(ImageViewsBase, BaseModel):
    """A view marking an image region as a semantic segmentation mask, where pixel values are class labels. It points to the reference view it was computed from and can carry a label table."""
    typename: Literal['MaskView'] = Field(alias='__typename', default='MaskView', exclude=True)

class ImageViewsBaseOpticsView(OpticsView, ImageViewsBase, BaseModel):
    """A view describing the optics used to acquire an image region: the instrument, objective and camera. Use it to inspect or compare acquisition hardware settings."""
    typename: Literal['OpticsView'] = Field(alias='__typename', default='OpticsView', exclude=True)

class ImageViewsBaseRGBView(RGBView, ImageViewsBase, BaseModel):
    """An RGB view describes how a subset of an image (typically a channel) is rendered in RGB within an RGB context, carrying color map, gamma and contrast limit settings."""
    typename: Literal['RGBView'] = Field(alias='__typename', default='RGBView', exclude=True)

class ImageViewsBaseROIView(ROIView, ImageViewsBase, BaseModel):
    """A ROI view establishes a relationship between an image region and a region of interest, e.g. recording that this image was cropped from the area described by the ROI on another image."""
    typename: Literal['ROIView'] = Field(alias='__typename', default='ROIView', exclude=True)

class ImageViewsBaseReferenceView(ImageViewsBase, BaseModel):
    """A view marking an image region as the reference that other views (e.g. mask views) point back to, for example the raw channel a segmentation mask was computed from."""
    typename: Literal['ReferenceView'] = Field(alias='__typename', default='ReferenceView', exclude=True)

class ImageViewsBaseScaleView(ImageViewsBase, BaseModel):
    """A view linking an image to a downscaled version of another image. Scale views form the levels of a multiscale pyramid: the parent is the full-resolution image and the scale factors give the downsampling per dimension."""
    typename: Literal['ScaleView'] = Field(alias='__typename', default='ScaleView', exclude=True)

class ImageViewsBaseTimepointView(TimepointView, ImageViewsBase, BaseModel):
    """A view anchoring an image region in real time: it places the region within an era (a named time epoch on the microscope) at a millisecond offset or frame index since its start."""
    typename: Literal['TimepointView'] = Field(alias='__typename', default='TimepointView', exclude=True)

class ImageViewsBaseWellPositionView(WellPositionView, ImageViewsBase, BaseModel):
    """A view mapping an image region to a well (row/column) of a multi well plate, so plate-based acquisitions can be traced back to their well."""
    typename: Literal['WellPositionView'] = Field(alias='__typename', default='WellPositionView', exclude=True)

class ImageViewsBaseCatchAll(ImageViewsBase, BaseModel):
    """Catch all class for ImageViewsBase"""
    typename: str = Field(alias='__typename', exclude=True)

class ImageRgbcontexts(BaseModel):
    """An RGB context is a collection of RGB views that together describe how an image should be rendered in RGB, e.g. grouping the views that represent each channel with its color map and contrast settings."""
    typename: Literal['RGBContext'] = Field(alias='__typename', default='RGBContext', exclude=True)
    id: ID
    name: str
    views: Tuple[RGBView, ...]
    model_config = ConfigDict(frozen=True)

class Image(HasZarrStoreTrait, MikroFetchable, BaseModel):
    """An image. Images are the central data type in mikro: a single 5D bioimage whose binary data is stored in a ZarrStore. Images can be annotated with views (coordinate-ordered subsets of the image) and are the primary container that rois, metrics, renders and generated tables are bound to."""
    typename: Literal['Image'] = Field(alias='__typename', default='Image', exclude=True)
    id: ID
    name: str
    'The name of the image'
    store: ZarrStore
    'The store where the image data is stored.'
    views: Tuple[Union[Annotated[Union[ImageViewsBaseAcquisitionView, ImageViewsBaseAffineTransformationView, ImageViewsBaseChannelView, ImageViewsBaseContinousScanView, ImageViewsBaseDerivedView, ImageViewsBaseFileView, ImageViewsBaseHistogramView, ImageViewsBaseInstanceMaskView, ImageViewsBaseLabelView, ImageViewsBaseLightpathView, ImageViewsBaseMaskView, ImageViewsBaseOpticsView, ImageViewsBaseRGBView, ImageViewsBaseROIView, ImageViewsBaseReferenceView, ImageViewsBaseScaleView, ImageViewsBaseTimepointView, ImageViewsBaseWellPositionView], Field(discriminator='typename')], ImageViewsBaseCatchAll], ...]
    'All views of this image'
    mask_views: Tuple[MaskView, ...] = Field(alias='maskViews')
    'Structure views relating other Arkitekt types to a subsection of the image'
    instance_mask_views: Tuple[InstanceMaskView, ...] = Field(alias='instanceMaskViews')
    'Instance mask views relating other Arkitekt types to a subsection of the image'
    rgb_contexts: Tuple[ImageRgbcontexts, ...] = Field(alias='rgbContexts')
    'RGB rendering contexts'
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for Image"""
        document = 'fragment Era on Era {\n  id\n  begin\n  name\n  __typename\n}\n\nfragment ReferenceView on ReferenceView {\n  ...View\n  id\n  __typename\n}\n\nfragment View on View {\n  xMin\n  xMax\n  yMin\n  yMax\n  tMin\n  tMax\n  cMin\n  cMax\n  zMin\n  zMax\n  __typename\n}\n\nfragment AcquisitionView on AcquisitionView {\n  ...View\n  id\n  description\n  acquiredAt\n  operator {\n    sub\n    __typename\n  }\n  __typename\n}\n\nfragment AffineTransformationView on AffineTransformationView {\n  ...View\n  id\n  affineMatrix\n  stage {\n    id\n    name\n    __typename\n  }\n  __typename\n}\n\nfragment ChannelView on ChannelView {\n  ...View\n  id\n  emissionWavelength\n  excitationWavelength\n  __typename\n}\n\nfragment ContinousScanView on ContinousScanView {\n  ...View\n  id\n  direction\n  __typename\n}\n\nfragment DerivedView on DerivedView {\n  ...View\n  id\n  originImage {\n    id\n    name\n    __typename\n  }\n  __typename\n}\n\nfragment FileView on FileView {\n  ...View\n  id\n  seriesIdentifier\n  file {\n    id\n    name\n    __typename\n  }\n  __typename\n}\n\nfragment InstanceMaskView on InstanceMaskView {\n  ...View\n  id\n  referenceView {\n    ...ReferenceView\n    __typename\n  }\n  __typename\n}\n\nfragment MaskView on MaskView {\n  ...View\n  id\n  referenceView {\n    ...ReferenceView\n    __typename\n  }\n  __typename\n}\n\nfragment OpticsView on OpticsView {\n  ...View\n  id\n  objective {\n    id\n    name\n    serialNumber\n    __typename\n  }\n  camera {\n    id\n    name\n    serialNumber\n    __typename\n  }\n  instrument {\n    id\n    name\n    serialNumber\n    __typename\n  }\n  __typename\n}\n\nfragment RGBView on RGBView {\n  ...View\n  id\n  contexts {\n    id\n    name\n    __typename\n  }\n  name\n  image {\n    id\n    store {\n      ...ZarrStore\n      __typename\n    }\n    derivedScaleViews {\n      id\n      image {\n        id\n        store {\n          ...ZarrStore\n          __typename\n        }\n        __typename\n      }\n      scaleX\n      scaleY\n      scaleZ\n      scaleT\n      scaleC\n      __typename\n    }\n    __typename\n  }\n  colorMap\n  contrastLimitMin\n  contrastLimitMax\n  gamma\n  active\n  fullColour\n  baseColor\n  __typename\n}\n\nfragment ROIView on ROIView {\n  ...View\n  id\n  roi {\n    id\n    name\n    __typename\n  }\n  __typename\n}\n\nfragment TimepointView on TimepointView {\n  ...View\n  id\n  msSinceStart\n  indexSinceStart\n  era {\n    ...Era\n    __typename\n  }\n  __typename\n}\n\nfragment WellPositionView on WellPositionView {\n  ...View\n  id\n  column\n  row\n  well {\n    id\n    rows\n    columns\n    name\n    __typename\n  }\n  __typename\n}\n\nfragment ZarrStore on ZarrStore {\n  id\n  key\n  bucket\n  path\n  __typename\n}\n\nfragment Image on Image {\n  id\n  name\n  store {\n    ...ZarrStore\n    __typename\n  }\n  views {\n    ...ChannelView\n    ...AffineTransformationView\n    ...TimepointView\n    ...OpticsView\n    ...AcquisitionView\n    ...RGBView\n    ...WellPositionView\n    ...DerivedView\n    ...ROIView\n    ...FileView\n    ...ContinousScanView\n    __typename\n  }\n  maskViews {\n    ...MaskView\n    __typename\n  }\n  instanceMaskViews {\n    ...InstanceMaskView\n    __typename\n  }\n  rgbContexts {\n    id\n    name\n    views {\n      ...RGBView\n      __typename\n    }\n    __typename\n  }\n  __typename\n}'
        name = 'Image'
        type = 'Image'

class CreateADatasetMutation(BaseModel):
    """No documentation found for this operation."""
    create_adataset: ADataset = Field(alias='createAdataset')
    'Create a new dataset from array-like data with optional choordinate anchors and OME  metadata'

    class Arguments(BaseModel):
        """Arguments for CreateADataset """
        input: CreateADatasetInput
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for CreateADataset """
        document = 'fragment ADataset on ADataset {\n  id\n  name\n  dims\n  dataArrays {\n    level\n    shape\n    chunkShape\n    scaleFactors\n    __typename\n  }\n  __typename\n}\n\nmutation CreateADataset($input: CreateADatasetInput!) {\n  createAdataset(input: $input) {\n    ...ADataset\n    __typename\n  }\n}'

class CreateCameraMutationCreatecamera(BaseModel):
    """A camera (detector) on a microscope, described by its sensor dimensions, pixel sizes and bit depth. Clients use it through optics views to record which detector acquired an image."""
    typename: Literal['Camera'] = Field(alias='__typename', default='Camera', exclude=True)
    id: ID
    name: str
    model_config = ConfigDict(frozen=True)

class CreateCameraMutation(BaseModel):
    """No documentation found for this operation."""
    create_camera: CreateCameraMutationCreatecamera = Field(alias='createCamera')
    'Create a new camera configuration'

    class Arguments(BaseModel):
        """Arguments for CreateCamera """
        input: CameraInput
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for CreateCamera """
        document = 'mutation CreateCamera($input: CameraInput!) {\n  createCamera(input: $input) {\n    id\n    name\n    __typename\n  }\n}'

class EnsureCameraMutationEnsurecamera(BaseModel):
    """A camera (detector) on a microscope, described by its sensor dimensions, pixel sizes and bit depth. Clients use it through optics views to record which detector acquired an image."""
    typename: Literal['Camera'] = Field(alias='__typename', default='Camera', exclude=True)
    id: ID
    name: str
    model_config = ConfigDict(frozen=True)

class EnsureCameraMutation(BaseModel):
    """No documentation found for this operation."""
    ensure_camera: EnsureCameraMutationEnsurecamera = Field(alias='ensureCamera')
    'Ensure a camera exists, creating if needed'

    class Arguments(BaseModel):
        """Arguments for EnsureCamera """
        input: CameraInput
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for EnsureCamera """
        document = 'mutation EnsureCamera($input: CameraInput!) {\n  ensureCamera(input: $input) {\n    id\n    name\n    __typename\n  }\n}'

class CreateDataRoiMutation(BaseModel):
    """No documentation found for this operation."""
    create_data_roi: DataRoi = Field(alias='createDataRoi')
    'Create a new data ROI from vector or slice definitions with optional choordinate anchors and OME metadata'

    class Arguments(BaseModel):
        """Arguments for CreateDataRoi """
        input: CreateDataRoiInput
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for CreateDataRoi """
        document = 'fragment DimDescriptor on DimDescriptor {\n  key\n  kind\n  __typename\n}\n\nfragment ZarrStore on ZarrStore {\n  id\n  key\n  bucket\n  path\n  __typename\n}\n\nfragment DataRoi on DataRoi {\n  id\n  dataset {\n    id\n    dimDescriptors {\n      ...DimDescriptor\n      __typename\n    }\n    dataArrays {\n      id\n      store {\n        ...ZarrStore\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  vectors\n  kind\n  __typename\n}\n\nmutation CreateDataRoi($input: CreateDataRoiInput!) {\n  createDataRoi(input: $input) {\n    ...DataRoi\n    __typename\n  }\n}'

class RequestBigfileUploadMutation(BaseModel):
    """No documentation found for this operation."""
    request_bigfile_upload: BigFileUploadGrant = Field(alias='requestBigfileUpload')
    'Request an upload grant for a big file store'

    class Arguments(BaseModel):
        """Arguments for RequestBigfileUpload """
        input: RequestBigFileUploadInput
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for RequestBigfileUpload """
        document = 'fragment BigFileUploadGrant on BigFileUploadGrant {\n  accessKey\n  secretKey\n  sessionToken\n  path\n  key\n  bucket\n  expiresIn\n  store\n  __typename\n}\n\nmutation RequestBigfileUpload($input: RequestBigFileUploadInput!) {\n  requestBigfileUpload(input: $input) {\n    ...BigFileUploadGrant\n    __typename\n  }\n}'

class FinishBigfileUploadMutation(BaseModel):
    """No documentation found for this operation."""
    finish_bigfile_upload: BigFileStore = Field(alias='finishBigfileUpload')
    'Finalize a big file upload after the client has written the object'

    class Arguments(BaseModel):
        """Arguments for FinishBigfileUpload """
        input: FinishBigFileUploadInput
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for FinishBigfileUpload """
        document = 'fragment BigFileStore on BigFileStore {\n  id\n  key\n  bucket\n  path\n  presignedUrl\n  __typename\n}\n\nmutation FinishBigfileUpload($input: FinishBigFileUploadInput!) {\n  finishBigfileUpload(input: $input) {\n    ...BigFileStore\n    __typename\n  }\n}'

class RequestBigfileAccessMutation(BaseModel):
    """No documentation found for this operation."""
    request_bigfile_access: BigFileAccessGrant = Field(alias='requestBigfileAccess')
    'Request temporary S3 read credentials for a big file'

    class Arguments(BaseModel):
        """Arguments for RequestBigfileAccess """
        input: RequestBigFileAccessInput
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for RequestBigfileAccess """
        document = 'fragment BigFileAccessGrant on BigFileAccessGrant {\n  accessKey\n  secretKey\n  sessionToken\n  expiresIn\n  path\n  key\n  bucket\n  __typename\n}\n\nmutation RequestBigfileAccess($input: RequestBigFileAccessInput!) {\n  requestBigfileAccess(input: $input) {\n    ...BigFileAccessGrant\n    __typename\n  }\n}'

class RequestMediaUploadMutation(BaseModel):
    """No documentation found for this operation."""
    request_media_upload: MediaUploadGrant = Field(alias='requestMediaUpload')
    'Upload media and return a URL for access'

    class Arguments(BaseModel):
        """Arguments for RequestMediaUpload """
        input: RequestMediaUploadInput
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for RequestMediaUpload """
        document = 'fragment MediaUploadGrant on MediaUploadGrant {\n  accessKey\n  secretKey\n  sessionToken\n  path\n  key\n  bucket\n  expiresIn\n  maxBytes\n  store\n  __typename\n}\n\nmutation RequestMediaUpload($input: RequestMediaUploadInput!) {\n  requestMediaUpload(input: $input) {\n    ...MediaUploadGrant\n    __typename\n  }\n}'

class FinishMediaUploadMutation(BaseModel):
    """No documentation found for this operation."""
    finish_media_upload: MediaStore = Field(alias='finishMediaUpload')
    'Finalize a media upload after the client has written the object'

    class Arguments(BaseModel):
        """Arguments for FinishMediaUpload """
        input: FinishMediaUploadInput
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for FinishMediaUpload """
        document = 'fragment MediaStore on MediaStore {\n  id\n  key\n  bucket\n  path\n  __typename\n}\n\nmutation FinishMediaUpload($input: FinishMediaUploadInput!) {\n  finishMediaUpload(input: $input) {\n    ...MediaStore\n    __typename\n  }\n}'

class RequestMediaAccessMutation(BaseModel):
    """No documentation found for this operation."""
    request_media_access: MediaAccessGrant = Field(alias='requestMediaAccess')
    'Request temporary S3 read credentials for a media file'

    class Arguments(BaseModel):
        """Arguments for RequestMediaAccess """
        input: RequestMediaAccessInput
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for RequestMediaAccess """
        document = 'fragment MediaAccessGrant on MediaAccessGrant {\n  accessKey\n  secretKey\n  sessionToken\n  expiresIn\n  path\n  key\n  bucket\n  __typename\n}\n\nmutation RequestMediaAccess($input: RequestMediaAccessInput!) {\n  requestMediaAccess(input: $input) {\n    ...MediaAccessGrant\n    __typename\n  }\n}'

class RequestParquetUploadMutation(BaseModel):
    """No documentation found for this operation."""
    request_parquet_upload: ParquetUploadGrant = Field(alias='requestParquetUpload')
    'Request an upload grant for a Parquet store'

    class Arguments(BaseModel):
        """Arguments for RequestParquetUpload """
        input: RequestParquetUploadInput
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for RequestParquetUpload """
        document = 'fragment ParquetUploadGrant on ParquetUploadGrant {\n  accessKey\n  secretKey\n  sessionToken\n  path\n  key\n  bucket\n  expiresIn\n  maxBytes\n  store\n  __typename\n}\n\nmutation RequestParquetUpload($input: RequestParquetUploadInput!) {\n  requestParquetUpload(input: $input) {\n    ...ParquetUploadGrant\n    __typename\n  }\n}'

class FinishParquetUploadMutation(BaseModel):
    """No documentation found for this operation."""
    finish_parquet_upload: ParquetStore = Field(alias='finishParquetUpload')
    'Finalize a Parquet upload after the client has written the object'

    class Arguments(BaseModel):
        """Arguments for FinishParquetUpload """
        input: FinishParquetUploadInput
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for FinishParquetUpload """
        document = 'fragment ParquetStore on ParquetStore {\n  id\n  key\n  bucket\n  path\n  __typename\n}\n\nmutation FinishParquetUpload($input: FinishParquetUploadInput!) {\n  finishParquetUpload(input: $input) {\n    ...ParquetStore\n    __typename\n  }\n}'

class RequestParquetAccessMutation(BaseModel):
    """No documentation found for this operation."""
    request_parquet_access: ParquetAccessGrant = Field(alias='requestParquetAccess')
    'Request temporary S3 read credentials for a Parquet file'

    class Arguments(BaseModel):
        """Arguments for RequestParquetAccess """
        input: RequestParquetAccessInput
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for RequestParquetAccess """
        document = 'fragment ParquetAccessGrant on ParquetAccessGrant {\n  accessKey\n  secretKey\n  sessionToken\n  expiresIn\n  path\n  key\n  bucket\n  __typename\n}\n\nmutation RequestParquetAccess($input: RequestParquetAccessInput!) {\n  requestParquetAccess(input: $input) {\n    ...ParquetAccessGrant\n    __typename\n  }\n}'

class RequestZarrUploadMutation(BaseModel):
    """No documentation found for this operation."""
    request_zarr_upload: ZarrUploadGrant = Field(alias='requestZarrUpload')
    'Request an upload grant for a Zarr store'

    class Arguments(BaseModel):
        """Arguments for RequestZarrUpload """
        input: RequestZarrUploadInput
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for RequestZarrUpload """
        document = 'fragment ZarrUploadGrant on ZarrUploadGrant {\n  accessKey\n  secretKey\n  sessionToken\n  path\n  key\n  bucket\n  expiresIn\n  maxBytes\n  store\n  __typename\n}\n\nmutation RequestZarrUpload($input: RequestZarrUploadInput!) {\n  requestZarrUpload(input: $input) {\n    ...ZarrUploadGrant\n    __typename\n  }\n}'

class FinishZarrUploadMutation(BaseModel):
    """No documentation found for this operation."""
    finish_zarr_upload: ZarrStore = Field(alias='finishZarrUpload')
    'Finalize a Zarr upload after the client has written the object'

    class Arguments(BaseModel):
        """Arguments for FinishZarrUpload """
        input: FinishZarrUploadInput
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for FinishZarrUpload """
        document = 'fragment ZarrStore on ZarrStore {\n  id\n  key\n  bucket\n  path\n  __typename\n}\n\nmutation FinishZarrUpload($input: FinishZarrUploadInput!) {\n  finishZarrUpload(input: $input) {\n    ...ZarrStore\n    __typename\n  }\n}'

class RequestZarrAccessMutation(BaseModel):
    """No documentation found for this operation."""
    request_zarr_access: ZarrAccessGrant = Field(alias='requestZarrAccess')
    'Request temporary S3 read credentials for a Zarr store'

    class Arguments(BaseModel):
        """Arguments for RequestZarrAccess """
        input: RequestZarrAccessInput
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for RequestZarrAccess """
        document = 'fragment ZarrAccessGrant on ZarrAccessGrant {\n  accessKey\n  secretKey\n  sessionToken\n  expiresIn\n  path\n  key\n  bucket\n  __typename\n}\n\nmutation RequestZarrAccess($input: RequestZarrAccessInput!) {\n  requestZarrAccess(input: $input) {\n    ...ZarrAccessGrant\n    __typename\n  }\n}'

class CreateDatasetMutation(BaseModel):
    """No documentation found for this operation."""
    create_dataset: Dataset = Field(alias='createDataset')
    'Create a new dataset to organize data'

    class Arguments(BaseModel):
        """Arguments for CreateDataset """
        input: CreateDatasetInput
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for CreateDataset """
        document = 'fragment Dataset on Dataset {\n  id\n  name\n  description\n  parent {\n    id\n    name\n    __typename\n  }\n  __typename\n}\n\nmutation CreateDataset($input: CreateDatasetInput!) {\n  createDataset(input: $input) {\n    ...Dataset\n    __typename\n  }\n}'

class EnsureDatasetMutation(BaseModel):
    """No documentation found for this operation."""
    ensure_dataset: Dataset = Field(alias='ensureDataset')
    'Create a new dataset to organize data'

    class Arguments(BaseModel):
        """Arguments for EnsureDataset """
        input: CreateDatasetInput
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for EnsureDataset """
        document = 'fragment Dataset on Dataset {\n  id\n  name\n  description\n  parent {\n    id\n    name\n    __typename\n  }\n  __typename\n}\n\nmutation EnsureDataset($input: CreateDatasetInput!) {\n  ensureDataset(input: $input) {\n    ...Dataset\n    __typename\n  }\n}'

class UpdateDatasetMutation(BaseModel):
    """No documentation found for this operation."""
    update_dataset: Dataset = Field(alias='updateDataset')
    'Update dataset metadata'

    class Arguments(BaseModel):
        """Arguments for UpdateDataset """
        input: ChangeDatasetInput
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for UpdateDataset """
        document = 'fragment Dataset on Dataset {\n  id\n  name\n  description\n  parent {\n    id\n    name\n    __typename\n  }\n  __typename\n}\n\nmutation UpdateDataset($input: ChangeDatasetInput!) {\n  updateDataset(input: $input) {\n    ...Dataset\n    __typename\n  }\n}'

class RevertDatasetMutation(BaseModel):
    """No documentation found for this operation."""
    revert_dataset: Dataset = Field(alias='revertDataset')
    'Revert dataset to a previous version'

    class Arguments(BaseModel):
        """Arguments for RevertDataset """
        input: RevertInput
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for RevertDataset """
        document = 'fragment Dataset on Dataset {\n  id\n  name\n  description\n  parent {\n    id\n    name\n    __typename\n  }\n  __typename\n}\n\nmutation RevertDataset($input: RevertInput!) {\n  revertDataset(input: $input) {\n    ...Dataset\n    __typename\n  }\n}'

class CreateEraMutationCreateera(BaseModel):
    """An era is a time space corresponding to an epoch on a microscope during an experiment. Clients use eras to contextualize images in real-world time via timepoint views."""
    typename: Literal['Era'] = Field(alias='__typename', default='Era', exclude=True)
    id: ID
    begin: Optional[datetime] = Field(default=None)
    model_config = ConfigDict(frozen=True)

class CreateEraMutation(BaseModel):
    """No documentation found for this operation."""
    create_era: CreateEraMutationCreateera = Field(alias='createEra')
    'Create a new era for temporal organization'

    class Arguments(BaseModel):
        """Arguments for CreateEra """
        input: EraInput
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for CreateEra """
        document = 'mutation CreateEra($input: EraInput!) {\n  createEra(input: $input) {\n    id\n    begin\n    __typename\n  }\n}'

class FromFileLikeMutation(BaseModel):
    """No documentation found for this operation."""
    from_file_like: File = Field(alias='fromFileLike')
    'Create a file from file-like data'

    class Arguments(BaseModel):
        """Arguments for FromFileLike """
        input: FromFileLike
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for FromFileLike """
        document = 'fragment BigFileStore on BigFileStore {\n  id\n  key\n  bucket\n  path\n  presignedUrl\n  __typename\n}\n\nfragment File on File {\n  origins {\n    id\n    __typename\n  }\n  id\n  name\n  store {\n    ...BigFileStore\n    __typename\n  }\n  __typename\n}\n\nmutation FromFileLike($input: FromFileLike!) {\n  fromFileLike(input: $input) {\n    ...File\n    __typename\n  }\n}'

class From_array_likeMutation(BaseModel):
    """No documentation found for this operation."""
    from_array_like: Image = Field(alias='fromArrayLike')
    'Create an image from array-like data'

    class Arguments(BaseModel):
        """Arguments for from_array_like """
        input: FromArrayLikeInput
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for from_array_like """
        document = 'fragment Era on Era {\n  id\n  begin\n  name\n  __typename\n}\n\nfragment ReferenceView on ReferenceView {\n  ...View\n  id\n  __typename\n}\n\nfragment View on View {\n  xMin\n  xMax\n  yMin\n  yMax\n  tMin\n  tMax\n  cMin\n  cMax\n  zMin\n  zMax\n  __typename\n}\n\nfragment AcquisitionView on AcquisitionView {\n  ...View\n  id\n  description\n  acquiredAt\n  operator {\n    sub\n    __typename\n  }\n  __typename\n}\n\nfragment AffineTransformationView on AffineTransformationView {\n  ...View\n  id\n  affineMatrix\n  stage {\n    id\n    name\n    __typename\n  }\n  __typename\n}\n\nfragment ChannelView on ChannelView {\n  ...View\n  id\n  emissionWavelength\n  excitationWavelength\n  __typename\n}\n\nfragment ContinousScanView on ContinousScanView {\n  ...View\n  id\n  direction\n  __typename\n}\n\nfragment DerivedView on DerivedView {\n  ...View\n  id\n  originImage {\n    id\n    name\n    __typename\n  }\n  __typename\n}\n\nfragment FileView on FileView {\n  ...View\n  id\n  seriesIdentifier\n  file {\n    id\n    name\n    __typename\n  }\n  __typename\n}\n\nfragment InstanceMaskView on InstanceMaskView {\n  ...View\n  id\n  referenceView {\n    ...ReferenceView\n    __typename\n  }\n  __typename\n}\n\nfragment MaskView on MaskView {\n  ...View\n  id\n  referenceView {\n    ...ReferenceView\n    __typename\n  }\n  __typename\n}\n\nfragment OpticsView on OpticsView {\n  ...View\n  id\n  objective {\n    id\n    name\n    serialNumber\n    __typename\n  }\n  camera {\n    id\n    name\n    serialNumber\n    __typename\n  }\n  instrument {\n    id\n    name\n    serialNumber\n    __typename\n  }\n  __typename\n}\n\nfragment RGBView on RGBView {\n  ...View\n  id\n  contexts {\n    id\n    name\n    __typename\n  }\n  name\n  image {\n    id\n    store {\n      ...ZarrStore\n      __typename\n    }\n    derivedScaleViews {\n      id\n      image {\n        id\n        store {\n          ...ZarrStore\n          __typename\n        }\n        __typename\n      }\n      scaleX\n      scaleY\n      scaleZ\n      scaleT\n      scaleC\n      __typename\n    }\n    __typename\n  }\n  colorMap\n  contrastLimitMin\n  contrastLimitMax\n  gamma\n  active\n  fullColour\n  baseColor\n  __typename\n}\n\nfragment ROIView on ROIView {\n  ...View\n  id\n  roi {\n    id\n    name\n    __typename\n  }\n  __typename\n}\n\nfragment TimepointView on TimepointView {\n  ...View\n  id\n  msSinceStart\n  indexSinceStart\n  era {\n    ...Era\n    __typename\n  }\n  __typename\n}\n\nfragment WellPositionView on WellPositionView {\n  ...View\n  id\n  column\n  row\n  well {\n    id\n    rows\n    columns\n    name\n    __typename\n  }\n  __typename\n}\n\nfragment ZarrStore on ZarrStore {\n  id\n  key\n  bucket\n  path\n  __typename\n}\n\nfragment Image on Image {\n  id\n  name\n  store {\n    ...ZarrStore\n    __typename\n  }\n  views {\n    ...ChannelView\n    ...AffineTransformationView\n    ...TimepointView\n    ...OpticsView\n    ...AcquisitionView\n    ...RGBView\n    ...WellPositionView\n    ...DerivedView\n    ...ROIView\n    ...FileView\n    ...ContinousScanView\n    __typename\n  }\n  maskViews {\n    ...MaskView\n    __typename\n  }\n  instanceMaskViews {\n    ...InstanceMaskView\n    __typename\n  }\n  rgbContexts {\n    id\n    name\n    views {\n      ...RGBView\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nmutation from_array_like($input: FromArrayLikeInput!) {\n  fromArrayLike(input: $input) {\n    ...Image\n    __typename\n  }\n}'

class CreateInstrumentMutationCreateinstrument(BaseModel):
    """A microscope or other instrument, identified by its manufacturer, model and serial number. Clients use it through optics views to record which instrument acquired an image."""
    typename: Literal['Instrument'] = Field(alias='__typename', default='Instrument', exclude=True)
    id: ID
    name: str
    model_config = ConfigDict(frozen=True)

class CreateInstrumentMutation(BaseModel):
    """No documentation found for this operation."""
    create_instrument: CreateInstrumentMutationCreateinstrument = Field(alias='createInstrument')
    'Create a new instrument configuration'

    class Arguments(BaseModel):
        """Arguments for CreateInstrument """
        input: InstrumentInput
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for CreateInstrument """
        document = 'mutation CreateInstrument($input: InstrumentInput!) {\n  createInstrument(input: $input) {\n    id\n    name\n    __typename\n  }\n}'

class EnsureInstrumentMutationEnsureinstrument(BaseModel):
    """A microscope or other instrument, identified by its manufacturer, model and serial number. Clients use it through optics views to record which instrument acquired an image."""
    typename: Literal['Instrument'] = Field(alias='__typename', default='Instrument', exclude=True)
    id: ID
    name: str
    model_config = ConfigDict(frozen=True)

class EnsureInstrumentMutation(BaseModel):
    """No documentation found for this operation."""
    ensure_instrument: EnsureInstrumentMutationEnsureinstrument = Field(alias='ensureInstrument')
    'Ensure an instrument exists, creating if needed'

    class Arguments(BaseModel):
        """Arguments for EnsureInstrument """
        input: InstrumentInput
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for EnsureInstrument """
        document = 'mutation EnsureInstrument($input: InstrumentInput!) {\n  ensureInstrument(input: $input) {\n    id\n    name\n    __typename\n  }\n}'

class CreateLayerMutation(BaseModel):
    """No documentation found for this operation."""
    create_layer: Layer = Field(alias='createLayer')
    'Create a new layer from an existing lens with optional affine transformation and colormap settings'

    class Arguments(BaseModel):
        """Arguments for CreateLayer """
        input: CreateLayerInput
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for CreateLayer """
        document = 'fragment Layer on Layer {\n  scene {\n    id\n    name\n    __typename\n  }\n  lens {\n    id\n    __typename\n  }\n  __typename\n}\n\nmutation CreateLayer($input: CreateLayerInput!) {\n  createLayer(input: $input) {\n    ...Layer\n    __typename\n  }\n}'

class CreateLensMutation(BaseModel):
    """No documentation found for this operation."""
    create_lens: Lens = Field(alias='createLens')
    'Create a new lens from an existing dataset and slicing constraints'

    class Arguments(BaseModel):
        """Arguments for CreateLens """
        input: CreateLensInput
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for CreateLens """
        document = 'fragment DimDescriptor on DimDescriptor {\n  key\n  kind\n  __typename\n}\n\nfragment Slice on Slice {\n  dim\n  start\n  stop\n  step\n  __typename\n}\n\nfragment ZarrStore on ZarrStore {\n  id\n  key\n  bucket\n  path\n  __typename\n}\n\nfragment Lens on Lens {\n  id\n  dataset {\n    id\n    dims\n    dataArrays {\n      id\n      level\n      store {\n        ...ZarrStore\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  shape\n  dims\n  dimDescriptors {\n    ...DimDescriptor\n    __typename\n  }\n  slices {\n    ...Slice\n    __typename\n  }\n  __typename\n}\n\nmutation CreateLens($input: CreateLensInput!) {\n  createLens(input: $input) {\n    ...Lens\n    __typename\n  }\n}'

class CreateMeshMutation(BaseModel):
    """No documentation found for this operation."""
    create_mesh: Mesh = Field(alias='createMesh')
    'Create a new mesh'

    class Arguments(BaseModel):
        """Arguments for CreateMesh """
        input: MeshInput
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for CreateMesh """
        document = 'fragment BigFileStore on BigFileStore {\n  id\n  key\n  bucket\n  path\n  presignedUrl\n  __typename\n}\n\nfragment Mesh on Mesh {\n  id\n  name\n  store {\n    ...BigFileStore\n    __typename\n  }\n  __typename\n}\n\nmutation CreateMesh($input: MeshInput!) {\n  createMesh(input: $input) {\n    ...Mesh\n    __typename\n  }\n}'

class CreateObjectiveMutationCreateobjective(BaseModel):
    """A microscope objective, described by its magnification, numerical aperture and immersion medium. Clients use it through optics views to record which objective an image was acquired with."""
    typename: Literal['Objective'] = Field(alias='__typename', default='Objective', exclude=True)
    id: ID
    name: str
    model_config = ConfigDict(frozen=True)

class CreateObjectiveMutation(BaseModel):
    """No documentation found for this operation."""
    create_objective: CreateObjectiveMutationCreateobjective = Field(alias='createObjective')
    'Create a new microscope objective configuration'

    class Arguments(BaseModel):
        """Arguments for CreateObjective """
        input: ObjectiveInput
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for CreateObjective """
        document = 'mutation CreateObjective($input: ObjectiveInput!) {\n  createObjective(input: $input) {\n    id\n    name\n    __typename\n  }\n}'

class EnsureObjectiveMutationEnsureobjective(BaseModel):
    """A microscope objective, described by its magnification, numerical aperture and immersion medium. Clients use it through optics views to record which objective an image was acquired with."""
    typename: Literal['Objective'] = Field(alias='__typename', default='Objective', exclude=True)
    id: ID
    name: str
    model_config = ConfigDict(frozen=True)

class EnsureObjectiveMutation(BaseModel):
    """No documentation found for this operation."""
    ensure_objective: EnsureObjectiveMutationEnsureobjective = Field(alias='ensureObjective')
    'Ensure an objective exists, creating if needed'

    class Arguments(BaseModel):
        """Arguments for EnsureObjective """
        input: ObjectiveInput
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for EnsureObjective """
        document = 'mutation EnsureObjective($input: ObjectiveInput!) {\n  ensureObjective(input: $input) {\n    id\n    name\n    __typename\n  }\n}'

class CreateRenderTreeMutationCreaterendertree(BaseModel):
    """A render tree is a tree structure that describes the rendering of multiple images together, by linking several RGB contexts into one composite visualization."""
    typename: Literal['RenderTree'] = Field(alias='__typename', default='RenderTree', exclude=True)
    id: ID
    model_config = ConfigDict(frozen=True)

class CreateRenderTreeMutation(BaseModel):
    """No documentation found for this operation."""
    create_render_tree: CreateRenderTreeMutationCreaterendertree = Field(alias='createRenderTree')
    'Create a new render tree for image visualization'

    class Arguments(BaseModel):
        """Arguments for CreateRenderTree """
        input: RenderTreeInput
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for CreateRenderTree """
        document = 'mutation CreateRenderTree($input: RenderTreeInput!) {\n  createRenderTree(input: $input) {\n    id\n    __typename\n  }\n}'

class CreateRGBContextMutation(BaseModel):
    """No documentation found for this operation."""
    create_rgb_context: RGBContext = Field(alias='createRgbContext')
    'Create a new RGB context for image visualization'

    class Arguments(BaseModel):
        """Arguments for CreateRGBContext """
        input: CreateRGBContextInput
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for CreateRGBContext """
        document = 'fragment View on View {\n  xMin\n  xMax\n  yMin\n  yMax\n  tMin\n  tMax\n  cMin\n  cMax\n  zMin\n  zMax\n  __typename\n}\n\nfragment RGBView on RGBView {\n  ...View\n  id\n  contexts {\n    id\n    name\n    __typename\n  }\n  name\n  image {\n    id\n    store {\n      ...ZarrStore\n      __typename\n    }\n    derivedScaleViews {\n      id\n      image {\n        id\n        store {\n          ...ZarrStore\n          __typename\n        }\n        __typename\n      }\n      scaleX\n      scaleY\n      scaleZ\n      scaleT\n      scaleC\n      __typename\n    }\n    __typename\n  }\n  colorMap\n  contrastLimitMin\n  contrastLimitMax\n  gamma\n  active\n  fullColour\n  baseColor\n  __typename\n}\n\nfragment ZarrStore on ZarrStore {\n  id\n  key\n  bucket\n  path\n  __typename\n}\n\nfragment RGBContext on RGBContext {\n  id\n  views {\n    ...RGBView\n    __typename\n  }\n  image {\n    id\n    store {\n      ...ZarrStore\n      __typename\n    }\n    __typename\n  }\n  pinned\n  name\n  z\n  t\n  c\n  blending\n  __typename\n}\n\nmutation CreateRGBContext($input: CreateRGBContextInput!) {\n  createRgbContext(input: $input) {\n    ...RGBContext\n    __typename\n  }\n}'

class UpdateRGBContextMutation(BaseModel):
    """No documentation found for this operation."""
    update_rgb_context: RGBContext = Field(alias='updateRgbContext')
    'Update settings of an existing RGB context'

    class Arguments(BaseModel):
        """Arguments for UpdateRGBContext """
        input: UpdateRGBContextInput
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for UpdateRGBContext """
        document = 'fragment View on View {\n  xMin\n  xMax\n  yMin\n  yMax\n  tMin\n  tMax\n  cMin\n  cMax\n  zMin\n  zMax\n  __typename\n}\n\nfragment RGBView on RGBView {\n  ...View\n  id\n  contexts {\n    id\n    name\n    __typename\n  }\n  name\n  image {\n    id\n    store {\n      ...ZarrStore\n      __typename\n    }\n    derivedScaleViews {\n      id\n      image {\n        id\n        store {\n          ...ZarrStore\n          __typename\n        }\n        __typename\n      }\n      scaleX\n      scaleY\n      scaleZ\n      scaleT\n      scaleC\n      __typename\n    }\n    __typename\n  }\n  colorMap\n  contrastLimitMin\n  contrastLimitMax\n  gamma\n  active\n  fullColour\n  baseColor\n  __typename\n}\n\nfragment ZarrStore on ZarrStore {\n  id\n  key\n  bucket\n  path\n  __typename\n}\n\nfragment RGBContext on RGBContext {\n  id\n  views {\n    ...RGBView\n    __typename\n  }\n  image {\n    id\n    store {\n      ...ZarrStore\n      __typename\n    }\n    __typename\n  }\n  pinned\n  name\n  z\n  t\n  c\n  blending\n  __typename\n}\n\nmutation UpdateRGBContext($input: UpdateRGBContextInput!) {\n  updateRgbContext(input: $input) {\n    ...RGBContext\n    __typename\n  }\n}'

class CreateRoiMutation(BaseModel):
    """No documentation found for this operation."""
    create_roi: ROI = Field(alias='createRoi')
    'Create a new region of interest'

    class Arguments(BaseModel):
        """Arguments for CreateRoi """
        input: RoiInput
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for CreateRoi """
        document = 'fragment ZarrStore on ZarrStore {\n  id\n  key\n  bucket\n  path\n  __typename\n}\n\nfragment ROI on ROI {\n  id\n  image {\n    id\n    store {\n      ...ZarrStore\n      __typename\n    }\n    __typename\n  }\n  vectors\n  kind\n  __typename\n}\n\nmutation CreateRoi($input: RoiInput!) {\n  createRoi(input: $input) {\n    ...ROI\n    __typename\n  }\n}'

class DeleteRoiMutation(BaseModel):
    """No documentation found for this operation."""
    delete_roi: ID = Field(alias='deleteRoi')
    'Delete an existing region of interest'

    class Arguments(BaseModel):
        """Arguments for DeleteRoi """
        input: DeleteRoiInput
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for DeleteRoi """
        document = 'mutation DeleteRoi($input: DeleteRoiInput!) {\n  deleteRoi(input: $input)\n}'

class UpdateRoiMutation(BaseModel):
    """No documentation found for this operation."""
    update_roi: ROI = Field(alias='updateRoi')
    'Update an existing region of interest'

    class Arguments(BaseModel):
        """Arguments for UpdateRoi """
        input: UpdateRoiInput
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for UpdateRoi """
        document = 'fragment ZarrStore on ZarrStore {\n  id\n  key\n  bucket\n  path\n  __typename\n}\n\nfragment ROI on ROI {\n  id\n  image {\n    id\n    store {\n      ...ZarrStore\n      __typename\n    }\n    __typename\n  }\n  vectors\n  kind\n  __typename\n}\n\nmutation UpdateRoi($input: UpdateRoiInput!) {\n  updateRoi(input: $input) {\n    ...ROI\n    __typename\n  }\n}'

class CreateSceneMutation(BaseModel):
    """No documentation found for this operation."""
    create_scene: Scene = Field(alias='createScene')
    'Create a new scene from an existing lens with optional blending mode'

    class Arguments(BaseModel):
        """Arguments for CreateScene """
        input: CreateSceneInput
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for CreateScene """
        document = 'fragment Scene on Scene {\n  name\n  id\n  __typename\n}\n\nmutation CreateScene($input: CreateSceneInput!) {\n  createScene(input: $input) {\n    ...Scene\n    __typename\n  }\n}'

class CreateSnapshotMutation(BaseModel):
    """No documentation found for this operation."""
    create_snapshot: Snapshot = Field(alias='createSnapshot')
    'Create a new state snapshot'

    class Arguments(BaseModel):
        """Arguments for CreateSnapshot """
        input: SnapshotInput
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for CreateSnapshot """
        document = 'fragment Snapshot on Snapshot {\n  id\n  store {\n    key\n    presignedUrl\n    __typename\n  }\n  name\n  __typename\n}\n\nmutation CreateSnapshot($input: SnapshotInput!) {\n  createSnapshot(input: $input) {\n    ...Snapshot\n    __typename\n  }\n}'

class CreateStageMutation(BaseModel):
    """No documentation found for this operation."""
    create_stage: Stage = Field(alias='createStage')
    'Create a new stage for organizing data'

    class Arguments(BaseModel):
        """Arguments for CreateStage """
        input: StageInput
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for CreateStage """
        document = 'fragment Stage on Stage {\n  id\n  name\n  affineViews {\n    affineMatrix\n    image {\n      id\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nmutation CreateStage($input: StageInput!) {\n  createStage(input: $input) {\n    ...Stage\n    __typename\n  }\n}'

class From_parquet_likeMutation(BaseModel):
    """No documentation found for this operation."""
    from_parquet_like: Table = Field(alias='fromParquetLike')
    'Create a table from parquet-like data'

    class Arguments(BaseModel):
        """Arguments for from_parquet_like """
        input: FromParquetLike
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for from_parquet_like """
        document = 'fragment ParquetStore on ParquetStore {\n  id\n  key\n  bucket\n  path\n  __typename\n}\n\nfragment Table on Table {\n  origins {\n    id\n    __typename\n  }\n  id\n  name\n  store {\n    ...ParquetStore\n    __typename\n  }\n  __typename\n}\n\nmutation from_parquet_like($input: FromParquetLike!) {\n  fromParquetLike(input: $input) {\n    ...Table\n    __typename\n  }\n}'

class CreateRgbViewMutationCreatergbview(BaseModel):
    """An RGB view describes how a subset of an image (typically a channel) is rendered in RGB within an RGB context, carrying color map, gamma and contrast limit settings."""
    typename: Literal['RGBView'] = Field(alias='__typename', default='RGBView', exclude=True)
    id: ID
    model_config = ConfigDict(frozen=True)

class CreateRgbViewMutation(BaseModel):
    """No documentation found for this operation."""
    create_rgb_view: CreateRgbViewMutationCreatergbview = Field(alias='createRgbView')
    'Create a new view for RGB image data'

    class Arguments(BaseModel):
        """Arguments for CreateRgbView """
        input: RGBViewInput
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for CreateRgbView """
        document = 'mutation CreateRgbView($input: RGBViewInput!) {\n  createRgbView(input: $input) {\n    id\n    __typename\n  }\n}'

class UpdateRgbViewMutationUpdatergbview(BaseModel):
    """An RGB view describes how a subset of an image (typically a channel) is rendered in RGB within an RGB context, carrying color map, gamma and contrast limit settings."""
    typename: Literal['RGBView'] = Field(alias='__typename', default='RGBView', exclude=True)
    id: ID
    model_config = ConfigDict(frozen=True)

class UpdateRgbViewMutation(BaseModel):
    """No documentation found for this operation."""
    update_rgb_view: UpdateRgbViewMutationUpdatergbview = Field(alias='updateRgbView')
    'Update an existing RGB view'

    class Arguments(BaseModel):
        """Arguments for UpdateRgbView """
        input: UpdateRGBViewInput
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for UpdateRgbView """
        document = 'mutation UpdateRgbView($input: UpdateRGBViewInput!) {\n  updateRgbView(input: $input) {\n    id\n    __typename\n  }\n}'

class CreateHistogramViewMutation(BaseModel):
    """No documentation found for this operation."""
    create_histogram_view: HistogramView = Field(alias='createHistogramView')
    'Create a new view for histogram data'

    class Arguments(BaseModel):
        """Arguments for CreateHistogramView """
        input: HistogramViewInput
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for CreateHistogramView """
        document = 'fragment View on View {\n  xMin\n  xMax\n  yMin\n  yMax\n  tMin\n  tMax\n  cMin\n  cMax\n  zMin\n  zMax\n  __typename\n}\n\nfragment HistogramView on HistogramView {\n  ...View\n  id\n  histogram\n  bins\n  __typename\n}\n\nmutation CreateHistogramView($input: HistogramViewInput!) {\n  createHistogramView(input: $input) {\n    ...HistogramView\n    __typename\n  }\n}'

class CreateMaskViewMutation(BaseModel):
    """No documentation found for this operation."""
    create_mask_view: MaskView = Field(alias='createMaskView')
    'Create a new view for masked data'

    class Arguments(BaseModel):
        """Arguments for CreateMaskView """
        input: MaskViewInput
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for CreateMaskView """
        document = 'fragment ReferenceView on ReferenceView {\n  ...View\n  id\n  __typename\n}\n\nfragment View on View {\n  xMin\n  xMax\n  yMin\n  yMax\n  tMin\n  tMax\n  cMin\n  cMax\n  zMin\n  zMax\n  __typename\n}\n\nfragment MaskView on MaskView {\n  ...View\n  id\n  referenceView {\n    ...ReferenceView\n    __typename\n  }\n  __typename\n}\n\nmutation CreateMaskView($input: MaskViewInput!) {\n  createMaskView(input: $input) {\n    ...MaskView\n    __typename\n  }\n}'

class CreateInstanceMaskViewMutation(BaseModel):
    """No documentation found for this operation."""
    create_instance_mask_view: InstanceMaskView = Field(alias='createInstanceMaskView')
    'Create a new view for instance mask data'

    class Arguments(BaseModel):
        """Arguments for CreateInstanceMaskView """
        input: InstanceMaskViewInput
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for CreateInstanceMaskView """
        document = 'fragment ReferenceView on ReferenceView {\n  ...View\n  id\n  __typename\n}\n\nfragment View on View {\n  xMin\n  xMax\n  yMin\n  yMax\n  tMin\n  tMax\n  cMin\n  cMax\n  zMin\n  zMax\n  __typename\n}\n\nfragment InstanceMaskView on InstanceMaskView {\n  ...View\n  id\n  referenceView {\n    ...ReferenceView\n    __typename\n  }\n  __typename\n}\n\nmutation CreateInstanceMaskView($input: InstanceMaskViewInput!) {\n  createInstanceMaskView(input: $input) {\n    ...InstanceMaskView\n    __typename\n  }\n}'

class CreateReferenceViewMutation(BaseModel):
    """No documentation found for this operation."""
    create_reference_view: ReferenceView = Field(alias='createReferenceView')
    'Create a new reference view for image data'

    class Arguments(BaseModel):
        """Arguments for CreateReferenceView """
        input: ReferenceViewInput
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for CreateReferenceView """
        document = 'fragment View on View {\n  xMin\n  xMax\n  yMin\n  yMax\n  tMin\n  tMax\n  cMin\n  cMax\n  zMin\n  zMax\n  __typename\n}\n\nfragment ReferenceView on ReferenceView {\n  ...View\n  id\n  __typename\n}\n\nmutation CreateReferenceView($input: ReferenceViewInput!) {\n  createReferenceView(input: $input) {\n    ...ReferenceView\n    __typename\n  }\n}'

class CreateViewCollectionMutationCreateviewcollection(BaseModel):
    """A collection of views. View collections provide overarching views on your data that are not bound to a specific image, e.g. all middle-z views of all images with a certain tag. They are a pure metadata construct and do not map to an ordering of binary data."""
    typename: Literal['ViewCollection'] = Field(alias='__typename', default='ViewCollection', exclude=True)
    id: ID
    name: str
    model_config = ConfigDict(frozen=True)

class CreateViewCollectionMutation(BaseModel):
    """No documentation found for this operation."""
    create_view_collection: CreateViewCollectionMutationCreateviewcollection = Field(alias='createViewCollection')
    'Create a new collection of views to organize related views'

    class Arguments(BaseModel):
        """Arguments for CreateViewCollection """
        input: ViewCollectionInput
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for CreateViewCollection """
        document = 'mutation CreateViewCollection($input: ViewCollectionInput!) {\n  createViewCollection(input: $input) {\n    id\n    name\n    __typename\n  }\n}'

class GetCameraQuery(BaseModel):
    """No documentation found for this operation."""
    camera: Camera
    'Get a single camera by ID'

    class Arguments(BaseModel):
        """Arguments for GetCamera """
        id: ID
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for GetCamera """
        document = 'fragment Camera on Camera {\n  sensorSizeX\n  sensorSizeY\n  pixelSizeX\n  pixelSizeY\n  name\n  serialNumber\n  __typename\n}\n\nquery GetCamera($id: ID!) {\n  camera(id: $id) {\n    ...Camera\n    __typename\n  }\n}'

class GetDatasetQuery(BaseModel):
    """No documentation found for this operation."""
    dataset: Dataset
    'Get a single dataset by ID'

    class Arguments(BaseModel):
        """Arguments for GetDataset """
        id: ID
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for GetDataset """
        document = 'fragment Dataset on Dataset {\n  id\n  name\n  description\n  parent {\n    id\n    name\n    __typename\n  }\n  __typename\n}\n\nquery GetDataset($id: ID!) {\n  dataset(id: $id) {\n    ...Dataset\n    __typename\n  }\n}'

class SearchDatasetsQueryOptions(BaseModel):
    """A dataset is a collection of images and files. It mimics the concept of a folder in a file system and is the top-level container for organising data in mikro."""
    typename: Literal['Dataset'] = Field(alias='__typename', default='Dataset', exclude=True)
    value: ID
    label: str
    model_config = ConfigDict(frozen=True)

class SearchDatasetsQuery(BaseModel):
    """No documentation found for this operation."""
    options: Tuple[SearchDatasetsQueryOptions, ...]
    'List datasets (folder-like collections of images, files and tables)'

    class Arguments(BaseModel):
        """Arguments for SearchDatasets """
        search: Optional[str] = Field(default=None)
        values: Optional[List[ID]] = Field(default=None)
        limit: Optional[int] = Field(default=None)
        offset: Optional[int] = Field(default=0)
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for SearchDatasets """
        document = 'query SearchDatasets($search: String, $values: [ID!], $limit: Int, $offset: Int = 0) {\n  options: datasets(\n    filters: {search: $search, ids: $values}\n    pagination: {limit: $limit, offset: $offset}\n  ) {\n    value: id\n    label: name\n    __typename\n  }\n}'

class GetFileQuery(BaseModel):
    """No documentation found for this operation."""
    file: File
    'Get a single file by ID'

    class Arguments(BaseModel):
        """Arguments for GetFile """
        id: ID
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for GetFile """
        document = 'fragment BigFileStore on BigFileStore {\n  id\n  key\n  bucket\n  path\n  presignedUrl\n  __typename\n}\n\nfragment File on File {\n  origins {\n    id\n    __typename\n  }\n  id\n  name\n  store {\n    ...BigFileStore\n    __typename\n  }\n  __typename\n}\n\nquery GetFile($id: ID!) {\n  file(id: $id) {\n    ...File\n    __typename\n  }\n}'

class SearchFilesQueryOptions(FileTrait, BaseModel):
    """A file in its original format (e.g. a microscopy vendor file), stored in a BigFileStore. Files are the raw sources that images are converted from, and file views link back to the images that originated from them."""
    typename: Literal['File'] = Field(alias='__typename', default='File', exclude=True)
    value: ID
    label: str
    model_config = ConfigDict(frozen=True)

class SearchFilesQuery(BaseModel):
    """No documentation found for this operation."""
    options: Tuple[SearchFilesQueryOptions, ...]
    'List files (raw microscopy files such as .czi or .ome.tiff)'

    class Arguments(BaseModel):
        """Arguments for SearchFiles """
        search: Optional[str] = Field(default=None)
        values: Optional[List[ID]] = Field(default=None)
        limit: Optional[int] = Field(default=None)
        offset: Optional[int] = Field(default=0)
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for SearchFiles """
        document = 'query SearchFiles($search: String, $values: [ID!], $limit: Int, $offset: Int = 0) {\n  options: files(\n    filters: {search: $search, ids: $values}\n    pagination: {limit: $limit, offset: $offset}\n  ) {\n    value: id\n    label: name\n    __typename\n  }\n}'

class GetImageQuery(BaseModel):
    """No documentation found for this operation."""
    image: Image
    'Returns a single image by ID'

    class Arguments(BaseModel):
        """Arguments for GetImage """
        id: ID
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for GetImage """
        document = 'fragment Era on Era {\n  id\n  begin\n  name\n  __typename\n}\n\nfragment ReferenceView on ReferenceView {\n  ...View\n  id\n  __typename\n}\n\nfragment View on View {\n  xMin\n  xMax\n  yMin\n  yMax\n  tMin\n  tMax\n  cMin\n  cMax\n  zMin\n  zMax\n  __typename\n}\n\nfragment AcquisitionView on AcquisitionView {\n  ...View\n  id\n  description\n  acquiredAt\n  operator {\n    sub\n    __typename\n  }\n  __typename\n}\n\nfragment AffineTransformationView on AffineTransformationView {\n  ...View\n  id\n  affineMatrix\n  stage {\n    id\n    name\n    __typename\n  }\n  __typename\n}\n\nfragment ChannelView on ChannelView {\n  ...View\n  id\n  emissionWavelength\n  excitationWavelength\n  __typename\n}\n\nfragment ContinousScanView on ContinousScanView {\n  ...View\n  id\n  direction\n  __typename\n}\n\nfragment DerivedView on DerivedView {\n  ...View\n  id\n  originImage {\n    id\n    name\n    __typename\n  }\n  __typename\n}\n\nfragment FileView on FileView {\n  ...View\n  id\n  seriesIdentifier\n  file {\n    id\n    name\n    __typename\n  }\n  __typename\n}\n\nfragment InstanceMaskView on InstanceMaskView {\n  ...View\n  id\n  referenceView {\n    ...ReferenceView\n    __typename\n  }\n  __typename\n}\n\nfragment MaskView on MaskView {\n  ...View\n  id\n  referenceView {\n    ...ReferenceView\n    __typename\n  }\n  __typename\n}\n\nfragment OpticsView on OpticsView {\n  ...View\n  id\n  objective {\n    id\n    name\n    serialNumber\n    __typename\n  }\n  camera {\n    id\n    name\n    serialNumber\n    __typename\n  }\n  instrument {\n    id\n    name\n    serialNumber\n    __typename\n  }\n  __typename\n}\n\nfragment RGBView on RGBView {\n  ...View\n  id\n  contexts {\n    id\n    name\n    __typename\n  }\n  name\n  image {\n    id\n    store {\n      ...ZarrStore\n      __typename\n    }\n    derivedScaleViews {\n      id\n      image {\n        id\n        store {\n          ...ZarrStore\n          __typename\n        }\n        __typename\n      }\n      scaleX\n      scaleY\n      scaleZ\n      scaleT\n      scaleC\n      __typename\n    }\n    __typename\n  }\n  colorMap\n  contrastLimitMin\n  contrastLimitMax\n  gamma\n  active\n  fullColour\n  baseColor\n  __typename\n}\n\nfragment ROIView on ROIView {\n  ...View\n  id\n  roi {\n    id\n    name\n    __typename\n  }\n  __typename\n}\n\nfragment TimepointView on TimepointView {\n  ...View\n  id\n  msSinceStart\n  indexSinceStart\n  era {\n    ...Era\n    __typename\n  }\n  __typename\n}\n\nfragment WellPositionView on WellPositionView {\n  ...View\n  id\n  column\n  row\n  well {\n    id\n    rows\n    columns\n    name\n    __typename\n  }\n  __typename\n}\n\nfragment ZarrStore on ZarrStore {\n  id\n  key\n  bucket\n  path\n  __typename\n}\n\nfragment Image on Image {\n  id\n  name\n  store {\n    ...ZarrStore\n    __typename\n  }\n  views {\n    ...ChannelView\n    ...AffineTransformationView\n    ...TimepointView\n    ...OpticsView\n    ...AcquisitionView\n    ...RGBView\n    ...WellPositionView\n    ...DerivedView\n    ...ROIView\n    ...FileView\n    ...ContinousScanView\n    __typename\n  }\n  maskViews {\n    ...MaskView\n    __typename\n  }\n  instanceMaskViews {\n    ...InstanceMaskView\n    __typename\n  }\n  rgbContexts {\n    id\n    name\n    views {\n      ...RGBView\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nquery GetImage($id: ID!) {\n  image(id: $id) {\n    ...Image\n    __typename\n  }\n}'

class GetRandomImageQuery(BaseModel):
    """No documentation found for this operation."""
    random_image: Image = Field(alias='randomImage')
    'Get a random image of the current organization'

    class Arguments(BaseModel):
        """Arguments for GetRandomImage """
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for GetRandomImage """
        document = 'fragment Era on Era {\n  id\n  begin\n  name\n  __typename\n}\n\nfragment ReferenceView on ReferenceView {\n  ...View\n  id\n  __typename\n}\n\nfragment View on View {\n  xMin\n  xMax\n  yMin\n  yMax\n  tMin\n  tMax\n  cMin\n  cMax\n  zMin\n  zMax\n  __typename\n}\n\nfragment AcquisitionView on AcquisitionView {\n  ...View\n  id\n  description\n  acquiredAt\n  operator {\n    sub\n    __typename\n  }\n  __typename\n}\n\nfragment AffineTransformationView on AffineTransformationView {\n  ...View\n  id\n  affineMatrix\n  stage {\n    id\n    name\n    __typename\n  }\n  __typename\n}\n\nfragment ChannelView on ChannelView {\n  ...View\n  id\n  emissionWavelength\n  excitationWavelength\n  __typename\n}\n\nfragment ContinousScanView on ContinousScanView {\n  ...View\n  id\n  direction\n  __typename\n}\n\nfragment DerivedView on DerivedView {\n  ...View\n  id\n  originImage {\n    id\n    name\n    __typename\n  }\n  __typename\n}\n\nfragment FileView on FileView {\n  ...View\n  id\n  seriesIdentifier\n  file {\n    id\n    name\n    __typename\n  }\n  __typename\n}\n\nfragment InstanceMaskView on InstanceMaskView {\n  ...View\n  id\n  referenceView {\n    ...ReferenceView\n    __typename\n  }\n  __typename\n}\n\nfragment MaskView on MaskView {\n  ...View\n  id\n  referenceView {\n    ...ReferenceView\n    __typename\n  }\n  __typename\n}\n\nfragment OpticsView on OpticsView {\n  ...View\n  id\n  objective {\n    id\n    name\n    serialNumber\n    __typename\n  }\n  camera {\n    id\n    name\n    serialNumber\n    __typename\n  }\n  instrument {\n    id\n    name\n    serialNumber\n    __typename\n  }\n  __typename\n}\n\nfragment RGBView on RGBView {\n  ...View\n  id\n  contexts {\n    id\n    name\n    __typename\n  }\n  name\n  image {\n    id\n    store {\n      ...ZarrStore\n      __typename\n    }\n    derivedScaleViews {\n      id\n      image {\n        id\n        store {\n          ...ZarrStore\n          __typename\n        }\n        __typename\n      }\n      scaleX\n      scaleY\n      scaleZ\n      scaleT\n      scaleC\n      __typename\n    }\n    __typename\n  }\n  colorMap\n  contrastLimitMin\n  contrastLimitMax\n  gamma\n  active\n  fullColour\n  baseColor\n  __typename\n}\n\nfragment ROIView on ROIView {\n  ...View\n  id\n  roi {\n    id\n    name\n    __typename\n  }\n  __typename\n}\n\nfragment TimepointView on TimepointView {\n  ...View\n  id\n  msSinceStart\n  indexSinceStart\n  era {\n    ...Era\n    __typename\n  }\n  __typename\n}\n\nfragment WellPositionView on WellPositionView {\n  ...View\n  id\n  column\n  row\n  well {\n    id\n    rows\n    columns\n    name\n    __typename\n  }\n  __typename\n}\n\nfragment ZarrStore on ZarrStore {\n  id\n  key\n  bucket\n  path\n  __typename\n}\n\nfragment Image on Image {\n  id\n  name\n  store {\n    ...ZarrStore\n    __typename\n  }\n  views {\n    ...ChannelView\n    ...AffineTransformationView\n    ...TimepointView\n    ...OpticsView\n    ...AcquisitionView\n    ...RGBView\n    ...WellPositionView\n    ...DerivedView\n    ...ROIView\n    ...FileView\n    ...ContinousScanView\n    __typename\n  }\n  maskViews {\n    ...MaskView\n    __typename\n  }\n  instanceMaskViews {\n    ...InstanceMaskView\n    __typename\n  }\n  rgbContexts {\n    id\n    name\n    views {\n      ...RGBView\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nquery GetRandomImage {\n  randomImage {\n    ...Image\n    __typename\n  }\n}'

class SearchImagesQueryOptions(HasZarrStoreTrait, BaseModel):
    """An image. Images are the central data type in mikro: a single 5D bioimage whose binary data is stored in a ZarrStore. Images can be annotated with views (coordinate-ordered subsets of the image) and are the primary container that rois, metrics, renders and generated tables are bound to."""
    typename: Literal['Image'] = Field(alias='__typename', default='Image', exclude=True)
    value: ID
    label: str
    'The name of the image'
    model_config = ConfigDict(frozen=True)

class SearchImagesQuery(BaseModel):
    """No documentation found for this operation."""
    options: Tuple[SearchImagesQueryOptions, ...]
    'List images in the current organization, filterable and orderable'

    class Arguments(BaseModel):
        """Arguments for SearchImages """
        search: Optional[str] = Field(default=None)
        values: Optional[List[ID]] = Field(default=None)
        limit: Optional[int] = Field(default=None)
        offset: Optional[int] = Field(default=0)
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for SearchImages """
        document = 'query SearchImages($search: String, $values: [ID!], $limit: Int, $offset: Int = 0) {\n  options: images(\n    filters: {name: {contains: $search}, ids: $values}\n    pagination: {limit: $limit, offset: $offset}\n  ) {\n    value: id\n    label: name\n    __typename\n  }\n}'

class ImagesQuery(BaseModel):
    """No documentation found for this operation."""
    images: Tuple[Image, ...]
    'List images in the current organization, filterable and orderable'

    class Arguments(BaseModel):
        """Arguments for Images """
        filter: Optional[ImageFilter] = Field(default=None)
        pagination: Optional[OffsetPaginationInput] = Field(default=None)
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for Images """
        document = 'fragment Era on Era {\n  id\n  begin\n  name\n  __typename\n}\n\nfragment ReferenceView on ReferenceView {\n  ...View\n  id\n  __typename\n}\n\nfragment View on View {\n  xMin\n  xMax\n  yMin\n  yMax\n  tMin\n  tMax\n  cMin\n  cMax\n  zMin\n  zMax\n  __typename\n}\n\nfragment AcquisitionView on AcquisitionView {\n  ...View\n  id\n  description\n  acquiredAt\n  operator {\n    sub\n    __typename\n  }\n  __typename\n}\n\nfragment AffineTransformationView on AffineTransformationView {\n  ...View\n  id\n  affineMatrix\n  stage {\n    id\n    name\n    __typename\n  }\n  __typename\n}\n\nfragment ChannelView on ChannelView {\n  ...View\n  id\n  emissionWavelength\n  excitationWavelength\n  __typename\n}\n\nfragment ContinousScanView on ContinousScanView {\n  ...View\n  id\n  direction\n  __typename\n}\n\nfragment DerivedView on DerivedView {\n  ...View\n  id\n  originImage {\n    id\n    name\n    __typename\n  }\n  __typename\n}\n\nfragment FileView on FileView {\n  ...View\n  id\n  seriesIdentifier\n  file {\n    id\n    name\n    __typename\n  }\n  __typename\n}\n\nfragment InstanceMaskView on InstanceMaskView {\n  ...View\n  id\n  referenceView {\n    ...ReferenceView\n    __typename\n  }\n  __typename\n}\n\nfragment MaskView on MaskView {\n  ...View\n  id\n  referenceView {\n    ...ReferenceView\n    __typename\n  }\n  __typename\n}\n\nfragment OpticsView on OpticsView {\n  ...View\n  id\n  objective {\n    id\n    name\n    serialNumber\n    __typename\n  }\n  camera {\n    id\n    name\n    serialNumber\n    __typename\n  }\n  instrument {\n    id\n    name\n    serialNumber\n    __typename\n  }\n  __typename\n}\n\nfragment RGBView on RGBView {\n  ...View\n  id\n  contexts {\n    id\n    name\n    __typename\n  }\n  name\n  image {\n    id\n    store {\n      ...ZarrStore\n      __typename\n    }\n    derivedScaleViews {\n      id\n      image {\n        id\n        store {\n          ...ZarrStore\n          __typename\n        }\n        __typename\n      }\n      scaleX\n      scaleY\n      scaleZ\n      scaleT\n      scaleC\n      __typename\n    }\n    __typename\n  }\n  colorMap\n  contrastLimitMin\n  contrastLimitMax\n  gamma\n  active\n  fullColour\n  baseColor\n  __typename\n}\n\nfragment ROIView on ROIView {\n  ...View\n  id\n  roi {\n    id\n    name\n    __typename\n  }\n  __typename\n}\n\nfragment TimepointView on TimepointView {\n  ...View\n  id\n  msSinceStart\n  indexSinceStart\n  era {\n    ...Era\n    __typename\n  }\n  __typename\n}\n\nfragment WellPositionView on WellPositionView {\n  ...View\n  id\n  column\n  row\n  well {\n    id\n    rows\n    columns\n    name\n    __typename\n  }\n  __typename\n}\n\nfragment ZarrStore on ZarrStore {\n  id\n  key\n  bucket\n  path\n  __typename\n}\n\nfragment Image on Image {\n  id\n  name\n  store {\n    ...ZarrStore\n    __typename\n  }\n  views {\n    ...ChannelView\n    ...AffineTransformationView\n    ...TimepointView\n    ...OpticsView\n    ...AcquisitionView\n    ...RGBView\n    ...WellPositionView\n    ...DerivedView\n    ...ROIView\n    ...FileView\n    ...ContinousScanView\n    __typename\n  }\n  maskViews {\n    ...MaskView\n    __typename\n  }\n  instanceMaskViews {\n    ...InstanceMaskView\n    __typename\n  }\n  rgbContexts {\n    id\n    name\n    views {\n      ...RGBView\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nquery Images($filter: ImageFilter, $pagination: OffsetPaginationInput) {\n  images(filters: $filter, pagination: $pagination) {\n    ...Image\n    __typename\n  }\n}'

class ViewImageQueryImageStore(HasZarrStoreAccessor, BaseModel):
    """No documentation"""
    typename: Literal['ZarrStore'] = Field(alias='__typename', default='ZarrStore', exclude=True)
    id: ID
    key: str
    bucket: str
    model_config = ConfigDict(frozen=True)

class ViewImageQueryImageViewsBase(BaseModel):
    """A view is a subset of an image, delimited by its coordinates (c, t, z, x, y) within the 5D array. Views attach metadata (channels, labels, transformations, timepoints, ...) to that subregion of the image."""
    model_config = ConfigDict(frozen=True)

class ViewImageQueryImageViewsBaseAcquisitionView(ViewImageQueryImageViewsBase, BaseModel):
    """A view recording when and by whom an image region was acquired at the microscope. Use it to trace an image back to its acquisition session and operator."""
    typename: Literal['AcquisitionView'] = Field(alias='__typename', default='AcquisitionView', exclude=True)

class ViewImageQueryImageViewsBaseAffineTransformationView(ViewImageQueryImageViewsBase, BaseModel):
    """A view placing an image region in physical space: a 4x4 affine matrix maps pixel coordinates onto a stage, encoding position and pixel size."""
    typename: Literal['AffineTransformationView'] = Field(alias='__typename', default='AffineTransformationView', exclude=True)

class ViewImageQueryImageViewsBaseChannelView(ViewImageQueryImageViewsBase, BaseModel):
    """A channel view describes an acquisition channel of an image, carrying its name and optical properties such as emission and excitation wavelengths."""
    typename: Literal['ChannelView'] = Field(alias='__typename', default='ChannelView', exclude=True)

class ViewImageQueryImageViewsBaseContinousScanView(ViewImageQueryImageViewsBase, BaseModel):
    """A view marking an image region as acquired by a continuous scan, recording the direction the scan traversed the axes in."""
    typename: Literal['ContinousScanView'] = Field(alias='__typename', default='ContinousScanView', exclude=True)

class ViewImageQueryImageViewsBaseDerivedView(ViewImageQueryImageViewsBase, BaseModel):
    """A derived view establishes a processing relationship between two images, guaranteeing that the derived image shares the same coordinate system as its origin image so the two can be trivially overlayed and compared (e.g. a segmentation over its source image). Cropped or projected images are not derived views, as they do not share the coordinate system."""
    typename: Literal['DerivedView'] = Field(alias='__typename', default='DerivedView', exclude=True)

class ViewImageQueryImageViewsBaseFileView(ViewImageQueryImageViewsBase, BaseModel):
    """A file view establishes a relationship between an image and a file: it records that this view of the image was originally part of the file (optionally a specific series within it) and links back to the source file."""
    typename: Literal['FileView'] = Field(alias='__typename', default='FileView', exclude=True)

class ViewImageQueryImageViewsBaseHistogramView(ViewImageQueryImageViewsBase, BaseModel):
    """A histogram view describes the distribution of pixel values in a subset of an image, providing bins, min/max bounds and the histogram counts. Useful for clients that want to display or auto-scale contrast."""
    typename: Literal['HistogramView'] = Field(alias='__typename', default='HistogramView', exclude=True)

class ViewImageQueryImageViewsBaseInstanceMaskView(ViewImageQueryImageViewsBase, BaseModel):
    """A view marking an image region as an instance segmentation mask, where each pixel value identifies an individual object instance. It points to the reference view it was computed from and can carry a per-instance label table."""
    typename: Literal['InstanceMaskView'] = Field(alias='__typename', default='InstanceMaskView', exclude=True)

class ViewImageQueryImageViewsBaseLabelView(ViewImageQueryImageViewsBase, BaseModel):
    """A label view gives a label to a specific image channel, e.g. mapping an antibody to the channel it stains, so the labeling agent can be easily identified. Labels can also be used for other purposes, such as marking a channel as poor quality."""
    typename: Literal['LabelView'] = Field(alias='__typename', default='LabelView', exclude=True)

class ViewImageQueryImageViewsBaseLightpathView(ViewImageQueryImageViewsBase, BaseModel):
    """A view attaching the optical path (light sources, filters, detectors and their connections) that light travelled through when this image region was acquired."""
    typename: Literal['LightpathView'] = Field(alias='__typename', default='LightpathView', exclude=True)

class ViewImageQueryImageViewsBaseMaskView(ViewImageQueryImageViewsBase, BaseModel):
    """A view marking an image region as a semantic segmentation mask, where pixel values are class labels. It points to the reference view it was computed from and can carry a label table."""
    typename: Literal['MaskView'] = Field(alias='__typename', default='MaskView', exclude=True)

class ViewImageQueryImageViewsBaseOpticsView(ViewImageQueryImageViewsBase, BaseModel):
    """A view describing the optics used to acquire an image region: the instrument, objective and camera. Use it to inspect or compare acquisition hardware settings."""
    typename: Literal['OpticsView'] = Field(alias='__typename', default='OpticsView', exclude=True)

class ViewImageQueryImageViewsBaseRGBView(ViewImageQueryImageViewsBase, BaseModel):
    """An RGB view describes how a subset of an image (typically a channel) is rendered in RGB within an RGB context, carrying color map, gamma and contrast limit settings."""
    typename: Literal['RGBView'] = Field(alias='__typename', default='RGBView', exclude=True)
    id: ID

class ViewImageQueryImageViewsBaseROIView(ViewImageQueryImageViewsBase, BaseModel):
    """A ROI view establishes a relationship between an image region and a region of interest, e.g. recording that this image was cropped from the area described by the ROI on another image."""
    typename: Literal['ROIView'] = Field(alias='__typename', default='ROIView', exclude=True)

class ViewImageQueryImageViewsBaseReferenceView(ViewImageQueryImageViewsBase, BaseModel):
    """A view marking an image region as the reference that other views (e.g. mask views) point back to, for example the raw channel a segmentation mask was computed from."""
    typename: Literal['ReferenceView'] = Field(alias='__typename', default='ReferenceView', exclude=True)

class ViewImageQueryImageViewsBaseScaleView(ViewImageQueryImageViewsBase, BaseModel):
    """A view linking an image to a downscaled version of another image. Scale views form the levels of a multiscale pyramid: the parent is the full-resolution image and the scale factors give the downsampling per dimension."""
    typename: Literal['ScaleView'] = Field(alias='__typename', default='ScaleView', exclude=True)

class ViewImageQueryImageViewsBaseTimepointView(ViewImageQueryImageViewsBase, BaseModel):
    """A view anchoring an image region in real time: it places the region within an era (a named time epoch on the microscope) at a millisecond offset or frame index since its start."""
    typename: Literal['TimepointView'] = Field(alias='__typename', default='TimepointView', exclude=True)

class ViewImageQueryImageViewsBaseWellPositionView(ViewImageQueryImageViewsBase, BaseModel):
    """A view mapping an image region to a well (row/column) of a multi well plate, so plate-based acquisitions can be traced back to their well."""
    typename: Literal['WellPositionView'] = Field(alias='__typename', default='WellPositionView', exclude=True)

class ViewImageQueryImageViewsBaseCatchAll(ViewImageQueryImageViewsBase, BaseModel):
    """Catch all class for ViewImageQueryImageViewsBase"""
    typename: str = Field(alias='__typename', exclude=True)

class ViewImageQueryImage(HasZarrStoreTrait, BaseModel):
    """An image. Images are the central data type in mikro: a single 5D bioimage whose binary data is stored in a ZarrStore. Images can be annotated with views (coordinate-ordered subsets of the image) and are the primary container that rois, metrics, renders and generated tables are bound to."""
    typename: Literal['Image'] = Field(alias='__typename', default='Image', exclude=True)
    id: ID
    store: ViewImageQueryImageStore
    'The store where the image data is stored.'
    views: Tuple[Union[Annotated[Union[ViewImageQueryImageViewsBaseAcquisitionView, ViewImageQueryImageViewsBaseAffineTransformationView, ViewImageQueryImageViewsBaseChannelView, ViewImageQueryImageViewsBaseContinousScanView, ViewImageQueryImageViewsBaseDerivedView, ViewImageQueryImageViewsBaseFileView, ViewImageQueryImageViewsBaseHistogramView, ViewImageQueryImageViewsBaseInstanceMaskView, ViewImageQueryImageViewsBaseLabelView, ViewImageQueryImageViewsBaseLightpathView, ViewImageQueryImageViewsBaseMaskView, ViewImageQueryImageViewsBaseOpticsView, ViewImageQueryImageViewsBaseRGBView, ViewImageQueryImageViewsBaseROIView, ViewImageQueryImageViewsBaseReferenceView, ViewImageQueryImageViewsBaseScaleView, ViewImageQueryImageViewsBaseTimepointView, ViewImageQueryImageViewsBaseWellPositionView], Field(discriminator='typename')], ViewImageQueryImageViewsBaseCatchAll], ...]
    'All views of this image'
    model_config = ConfigDict(frozen=True)

class ViewImageQuery(BaseModel):
    """No documentation found for this operation."""
    image: ViewImageQueryImage
    'Returns a single image by ID'

    class Arguments(BaseModel):
        """Arguments for ViewImage """
        id: ID
        filtersggg: Optional[ViewFilter] = Field(default=None)
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for ViewImage """
        document = 'query ViewImage($id: ID!, $filtersggg: ViewFilter) {\n  image(id: $id) {\n    id\n    store {\n      id\n      key\n      bucket\n      __typename\n    }\n    views(filters: $filtersggg) {\n      ... on RGBView {\n        id\n      }\n      __typename\n    }\n    __typename\n  }\n}'

class ArtemiyImagesQueryImagesChannels(BaseModel):
    """A channel descriptor"""
    typename: Literal['ChannelInfo'] = Field(alias='__typename', default='ChannelInfo', exclude=True)
    label: str
    model_config = ConfigDict(frozen=True)

class ArtemiyImagesQueryImages(HasZarrStoreTrait, BaseModel):
    """An image. Images are the central data type in mikro: a single 5D bioimage whose binary data is stored in a ZarrStore. Images can be annotated with views (coordinate-ordered subsets of the image) and are the primary container that rois, metrics, renders and generated tables are bound to."""
    typename: Literal['Image'] = Field(alias='__typename', default='Image', exclude=True)
    id: ID
    name: str
    'The name of the image'
    channels: Tuple[ArtemiyImagesQueryImagesChannels, ...]
    'The channels of this image'
    model_config = ConfigDict(frozen=True)

class ArtemiyImagesQuery(BaseModel):
    """No documentation found for this operation."""
    images: Tuple[ArtemiyImagesQueryImages, ...]
    'List images in the current organization, filterable and orderable'

    class Arguments(BaseModel):
        """Arguments for ArtemiyImages """
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for ArtemiyImages """
        document = 'query ArtemiyImages {\n  images {\n    id\n    name\n    channels {\n      label\n      __typename\n    }\n    __typename\n  }\n}'

class GetInstrumentQuery(BaseModel):
    """No documentation found for this operation."""
    instrument: Instrument
    'Get a single instrument by ID'

    class Arguments(BaseModel):
        """Arguments for GetInstrument """
        id: ID
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for GetInstrument """
        document = 'fragment Instrument on Instrument {\n  id\n  model\n  name\n  serialNumber\n  __typename\n}\n\nquery GetInstrument($id: ID!) {\n  instrument(id: $id) {\n    ...Instrument\n    __typename\n  }\n}'

class GetLensQuery(BaseModel):
    """No documentation found for this operation."""
    lens: Lens
    'Get a single lens by ID'

    class Arguments(BaseModel):
        """Arguments for GetLens """
        id: ID
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for GetLens """
        document = 'fragment DimDescriptor on DimDescriptor {\n  key\n  kind\n  __typename\n}\n\nfragment Slice on Slice {\n  dim\n  start\n  stop\n  step\n  __typename\n}\n\nfragment ZarrStore on ZarrStore {\n  id\n  key\n  bucket\n  path\n  __typename\n}\n\nfragment Lens on Lens {\n  id\n  dataset {\n    id\n    dims\n    dataArrays {\n      id\n      level\n      store {\n        ...ZarrStore\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  shape\n  dims\n  dimDescriptors {\n    ...DimDescriptor\n    __typename\n  }\n  slices {\n    ...Slice\n    __typename\n  }\n  __typename\n}\n\nquery GetLens($id: ID!) {\n  lens(id: $id) {\n    ...Lens\n    __typename\n  }\n}'

class GetMeshQuery(BaseModel):
    """No documentation found for this operation."""
    mesh: Mesh
    'Get a single 3D mesh by ID'

    class Arguments(BaseModel):
        """Arguments for GetMesh """
        id: ID
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for GetMesh """
        document = 'fragment BigFileStore on BigFileStore {\n  id\n  key\n  bucket\n  path\n  presignedUrl\n  __typename\n}\n\nfragment Mesh on Mesh {\n  id\n  name\n  store {\n    ...BigFileStore\n    __typename\n  }\n  __typename\n}\n\nquery GetMesh($id: ID!) {\n  mesh(id: $id) {\n    ...Mesh\n    __typename\n  }\n}'

class SearchMeshesQueryOptions(BaseModel):
    """A 3D mesh belonging to a dataset, with its geometry kept in a big file store. Clients use it to download or visualize surface reconstructions derived from image data."""
    typename: Literal['Mesh'] = Field(alias='__typename', default='Mesh', exclude=True)
    value: ID
    label: str
    model_config = ConfigDict(frozen=True)

class SearchMeshesQuery(BaseModel):
    """No documentation found for this operation."""
    options: Tuple[SearchMeshesQueryOptions, ...]
    'List 3D meshes'

    class Arguments(BaseModel):
        """Arguments for SearchMeshes """
        search: Optional[str] = Field(default=None)
        values: Optional[List[ID]] = Field(default=None)
        limit: Optional[int] = Field(default=None)
        offset: Optional[int] = Field(default=0)
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for SearchMeshes """
        document = 'query SearchMeshes($search: String, $values: [ID!], $limit: Int, $offset: Int = 0) {\n  options: meshes(\n    filters: {search: $search, ids: $values}\n    pagination: {limit: $limit, offset: $offset}\n  ) {\n    value: id\n    label: name\n    __typename\n  }\n}'

class GetObjectiveQuery(BaseModel):
    """No documentation found for this operation."""
    objective: Objective
    'Get a single objective by ID'

    class Arguments(BaseModel):
        """Arguments for GetObjective """
        id: ID
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for GetObjective """
        document = 'fragment Objective on Objective {\n  id\n  na\n  name\n  serialNumber\n  __typename\n}\n\nquery GetObjective($id: ID!) {\n  objective(id: $id) {\n    ...Objective\n    __typename\n  }\n}'

class GetRGBContextQuery(BaseModel):
    """No documentation found for this operation."""
    rgbcontext: RGBContext
    'Get a single RGB render context by ID'

    class Arguments(BaseModel):
        """Arguments for GetRGBContext """
        id: ID
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for GetRGBContext """
        document = 'fragment View on View {\n  xMin\n  xMax\n  yMin\n  yMax\n  tMin\n  tMax\n  cMin\n  cMax\n  zMin\n  zMax\n  __typename\n}\n\nfragment RGBView on RGBView {\n  ...View\n  id\n  contexts {\n    id\n    name\n    __typename\n  }\n  name\n  image {\n    id\n    store {\n      ...ZarrStore\n      __typename\n    }\n    derivedScaleViews {\n      id\n      image {\n        id\n        store {\n          ...ZarrStore\n          __typename\n        }\n        __typename\n      }\n      scaleX\n      scaleY\n      scaleZ\n      scaleT\n      scaleC\n      __typename\n    }\n    __typename\n  }\n  colorMap\n  contrastLimitMin\n  contrastLimitMax\n  gamma\n  active\n  fullColour\n  baseColor\n  __typename\n}\n\nfragment ZarrStore on ZarrStore {\n  id\n  key\n  bucket\n  path\n  __typename\n}\n\nfragment RGBContext on RGBContext {\n  id\n  views {\n    ...RGBView\n    __typename\n  }\n  image {\n    id\n    store {\n      ...ZarrStore\n      __typename\n    }\n    __typename\n  }\n  pinned\n  name\n  z\n  t\n  c\n  blending\n  __typename\n}\n\nquery GetRGBContext($id: ID!) {\n  rgbcontext(id: $id) {\n    ...RGBContext\n    __typename\n  }\n}'

class GetRoisQuery(BaseModel):
    """No documentation found for this operation."""
    rois: Tuple[ROI, ...]
    'List regions of interest drawn on images'

    class Arguments(BaseModel):
        """Arguments for GetRois """
        image: ID
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for GetRois """
        document = 'fragment ZarrStore on ZarrStore {\n  id\n  key\n  bucket\n  path\n  __typename\n}\n\nfragment ROI on ROI {\n  id\n  image {\n    id\n    store {\n      ...ZarrStore\n      __typename\n    }\n    __typename\n  }\n  vectors\n  kind\n  __typename\n}\n\nquery GetRois($image: ID!) {\n  rois(filters: {image: $image}) {\n    ...ROI\n    __typename\n  }\n}'

class GetRoiQuery(BaseModel):
    """No documentation found for this operation."""
    roi: ROI
    'Get a single region of interest by ID'

    class Arguments(BaseModel):
        """Arguments for GetRoi """
        id: ID
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for GetRoi """
        document = 'fragment ZarrStore on ZarrStore {\n  id\n  key\n  bucket\n  path\n  __typename\n}\n\nfragment ROI on ROI {\n  id\n  image {\n    id\n    store {\n      ...ZarrStore\n      __typename\n    }\n    __typename\n  }\n  vectors\n  kind\n  __typename\n}\n\nquery GetRoi($id: ID!) {\n  roi(id: $id) {\n    ...ROI\n    __typename\n  }\n}'

class SearchRoisQueryOptions(IsVectorizableTrait, BaseModel):
    """A region of interest drawn on an image, defined by a list of 5D vectors (c, t, z, y, x) and a kind (rectangle, path, point, ...). Use ROIs to mark and share structures of interest."""
    typename: Literal['ROI'] = Field(alias='__typename', default='ROI', exclude=True)
    value: ID
    label: str
    model_config = ConfigDict(frozen=True)

class SearchRoisQuery(BaseModel):
    """No documentation found for this operation."""
    options: Tuple[SearchRoisQueryOptions, ...]
    'List regions of interest drawn on images'

    class Arguments(BaseModel):
        """Arguments for SearchRois """
        search: Optional[str] = Field(default=None)
        values: Optional[List[ID]] = Field(default=None)
        limit: Optional[int] = Field(default=None)
        offset: Optional[int] = Field(default=0)
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for SearchRois """
        document = 'query SearchRois($search: String, $values: [ID!], $limit: Int, $offset: Int = 0) {\n  options: rois(\n    filters: {search: $search, ids: $values}\n    pagination: {limit: $limit, offset: $offset}\n  ) {\n    value: id\n    label: name\n    __typename\n  }\n}'

class GetSceneQuery(BaseModel):
    """No documentation found for this operation."""
    scene: Scene
    'Get a single scene by ID'

    class Arguments(BaseModel):
        """Arguments for GetScene """
        id: ID
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for GetScene """
        document = 'fragment Scene on Scene {\n  name\n  id\n  __typename\n}\n\nquery GetScene($id: ID!) {\n  scene(id: $id) {\n    ...Scene\n    __typename\n  }\n}'

class SearchScenesQueryOptions(BaseModel):
    """The absolute coordinate universe in which layers are placed, with defined spatial and temporal base units"""
    typename: Literal['Scene'] = Field(alias='__typename', default='Scene', exclude=True)
    value: ID
    label: str
    model_config = ConfigDict(frozen=True)

class SearchScenesQuery(BaseModel):
    """No documentation found for this operation."""
    options: Tuple[SearchScenesQueryOptions, ...]
    'List scenes (compositions of layers over array datasets)'

    class Arguments(BaseModel):
        """Arguments for SearchScenes """
        search: Optional[str] = Field(default=None)
        values: Optional[List[ID]] = Field(default=None)
        limit: Optional[int] = Field(default=None)
        offset: Optional[int] = Field(default=0)
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for SearchScenes """
        document = 'query SearchScenes($search: String, $values: [ID!], $limit: Int, $offset: Int = 0) {\n  options: scenes(\n    filters: {search: $search, ids: $values}\n    pagination: {limit: $limit, offset: $offset}\n  ) {\n    value: id\n    label: name\n    __typename\n  }\n}'

class GetSnapshotQuery(BaseModel):
    """No documentation found for this operation."""
    snapshot: Snapshot
    'Get a single snapshot by ID'

    class Arguments(BaseModel):
        """Arguments for GetSnapshot """
        id: ID
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for GetSnapshot """
        document = 'fragment Snapshot on Snapshot {\n  id\n  store {\n    key\n    presignedUrl\n    __typename\n  }\n  name\n  __typename\n}\n\nquery GetSnapshot($id: ID!) {\n  snapshot(id: $id) {\n    ...Snapshot\n    __typename\n  }\n}'

class SearchSnapshotsQueryOptions(BaseModel):
    """A snapshot is a pre-rendered thumbnail image of an image. Clients use snapshots to display previews without loading the full underlying data."""
    typename: Literal['Snapshot'] = Field(alias='__typename', default='Snapshot', exclude=True)
    value: ID
    label: str
    model_config = ConfigDict(frozen=True)

class SearchSnapshotsQuery(BaseModel):
    """No documentation found for this operation."""
    options: Tuple[SearchSnapshotsQueryOptions, ...]
    'List snapshots (pre-rendered thumbnail images of images)'

    class Arguments(BaseModel):
        """Arguments for SearchSnapshots """
        search: Optional[str] = Field(default=None)
        values: Optional[List[ID]] = Field(default=None)
        limit: Optional[int] = Field(default=None)
        offset: Optional[int] = Field(default=0)
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for SearchSnapshots """
        document = 'query SearchSnapshots($search: String, $values: [ID!], $limit: Int, $offset: Int = 0) {\n  options: snapshots(\n    filters: {name: {contains: $search}, ids: $values}\n    pagination: {limit: $limit, offset: $offset}\n  ) {\n    value: id\n    label: name\n    __typename\n  }\n}'

class GetStageQuery(BaseModel):
    """No documentation found for this operation."""
    stage: Stage
    'Get a single stage by ID'

    class Arguments(BaseModel):
        """Arguments for GetStage """
        id: ID
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for GetStage """
        document = 'fragment Stage on Stage {\n  id\n  name\n  affineViews {\n    affineMatrix\n    image {\n      id\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nquery GetStage($id: ID!) {\n  stage(id: $id) {\n    ...Stage\n    __typename\n  }\n}'

class SearchStagesQueryOptions(BaseModel):
    """A stage is a 3D space corresponding to the physical space on a microscope during an experiment. Clients use stages to contextualize images according to their real-world physical location via affine transformation views."""
    typename: Literal['Stage'] = Field(alias='__typename', default='Stage', exclude=True)
    value: ID
    label: str
    model_config = ConfigDict(frozen=True)

class SearchStagesQuery(BaseModel):
    """No documentation found for this operation."""
    options: Tuple[SearchStagesQueryOptions, ...]
    'List stages (the 3D physical spaces images are positioned in)'

    class Arguments(BaseModel):
        """Arguments for SearchStages """
        search: Optional[str] = Field(default=None)
        values: Optional[List[ID]] = Field(default=None)
        limit: Optional[int] = Field(default=None)
        offset: Optional[int] = Field(default=0)
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for SearchStages """
        document = 'query SearchStages($search: String, $values: [ID!], $limit: Int, $offset: Int = 0) {\n  options: stages(\n    filters: {search: $search, ids: $values}\n    pagination: {limit: $limit, offset: $offset}\n  ) {\n    value: id\n    label: name\n    __typename\n  }\n}'

class GetTableQuery(BaseModel):
    """No documentation found for this operation."""
    table: Table
    'Get a single table by ID'

    class Arguments(BaseModel):
        """Arguments for GetTable """
        id: ID
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for GetTable """
        document = 'fragment ParquetStore on ParquetStore {\n  id\n  key\n  bucket\n  path\n  __typename\n}\n\nfragment Table on Table {\n  origins {\n    id\n    __typename\n  }\n  id\n  name\n  store {\n    ...ParquetStore\n    __typename\n  }\n  __typename\n}\n\nquery GetTable($id: ID!) {\n  table(id: $id) {\n    ...Table\n    __typename\n  }\n}'

class SearchTablesQueryOptions(HasParquestStoreTrait, BaseModel):
    """A table of tabular data, stored as a Parquet file. Tables are typically derived from images (e.g. measurements or localisations) and can be queried column- and row-wise through the API."""
    typename: Literal['Table'] = Field(alias='__typename', default='Table', exclude=True)
    value: ID
    label: str
    model_config = ConfigDict(frozen=True)

class SearchTablesQuery(BaseModel):
    """No documentation found for this operation."""
    options: Tuple[SearchTablesQueryOptions, ...]
    'List tables (tabular data backed by parquet stores)'

    class Arguments(BaseModel):
        """Arguments for SearchTables """
        search: Optional[str] = Field(default=None)
        values: Optional[List[ID]] = Field(default=None)
        limit: Optional[int] = Field(default=None)
        offset: Optional[int] = Field(default=0)
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for SearchTables """
        document = 'query SearchTables($search: String, $values: [ID!], $limit: Int, $offset: Int = 0) {\n  options: tables(\n    filters: {search: $search, ids: $values}\n    pagination: {limit: $limit, offset: $offset}\n  ) {\n    value: id\n    label: name\n    __typename\n  }\n}'

class GetTableCellQuery(BaseModel):
    """No documentation found for this operation."""
    table_cell: TableCell = Field(alias='tableCell')
    'Get a single table cell by its compound ID (tableId-rowId-columnId)'

    class Arguments(BaseModel):
        """Arguments for GetTableCell """
        id: ID
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for GetTableCell """
        document = 'fragment TableCell on TableCell {\n  id\n  table {\n    id\n    __typename\n  }\n  value\n  column {\n    name\n    __typename\n  }\n  __typename\n}\n\nquery GetTableCell($id: ID!) {\n  tableCell(id: $id) {\n    ...TableCell\n    __typename\n  }\n}'

class SearchTableCellsQueryOptions(BaseModel):
    """A cell of a table"""
    typename: Literal['TableCell'] = Field(alias='__typename', default='TableCell', exclude=True)
    value: ID
    label: str
    'The name of the column this cell belongs to'
    model_config = ConfigDict(frozen=True)

class SearchTableCellsQuery(BaseModel):
    """No documentation found for this operation."""
    options: Tuple[SearchTableCellsQueryOptions, ...]
    "List the cells of a table, row-major over the table's parquet data"

    class Arguments(BaseModel):
        """Arguments for SearchTableCells """
        search: Optional[str] = Field(default=None)
        values: Optional[List[ID]] = Field(default=None)
        table: ID
        limit: Optional[int] = Field(default=None)
        offset: Optional[int] = Field(default=0)
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for SearchTableCells """
        document = 'query SearchTableCells($search: String, $values: [ID!], $table: ID!, $limit: Int, $offset: Int = 0) {\n  options: tableCells(\n    table: $table\n    filters: {search: $search, ids: $values}\n    pagination: {limit: $limit, offset: $offset}\n  ) {\n    value: id\n    label: name\n    __typename\n  }\n}'

class GetTableRowQuery(BaseModel):
    """No documentation found for this operation."""
    table_row: TableRow = Field(alias='tableRow')
    'Get a single table row by its compound ID (tableId-rowId)'

    class Arguments(BaseModel):
        """Arguments for GetTableRow """
        id: ID
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for GetTableRow """
        document = 'fragment TableRow on TableRow {\n  id\n  values\n  table {\n    id\n    __typename\n  }\n  columns {\n    name\n    __typename\n  }\n  __typename\n}\n\nquery GetTableRow($id: ID!) {\n  tableRow(id: $id) {\n    ...TableRow\n    __typename\n  }\n}'

class SearchTableRowsQueryOptions(BaseModel):
    """A row of a table"""
    typename: Literal['TableRow'] = Field(alias='__typename', default='TableRow', exclude=True)
    value: ID
    label: str
    'The display name of this row'
    model_config = ConfigDict(frozen=True)

class SearchTableRowsQuery(BaseModel):
    """No documentation found for this operation."""
    options: Tuple[SearchTableRowsQueryOptions, ...]
    "List the rows of a table, paginated over the table's parquet data"

    class Arguments(BaseModel):
        """Arguments for SearchTableRows """
        search: Optional[str] = Field(default=None)
        values: Optional[List[ID]] = Field(default=None)
        table: ID
        limit: Optional[int] = Field(default=None)
        offset: Optional[int] = Field(default=0)
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for SearchTableRows """
        document = 'query SearchTableRows($search: String, $values: [ID!], $table: ID!, $limit: Int, $offset: Int = 0) {\n  options: tableRows(\n    table: $table\n    filters: {search: $search, ids: $values}\n    pagination: {limit: $limit, offset: $offset}\n  ) {\n    value: id\n    label: name\n    __typename\n  }\n}'

class GetRGBViewQuery(BaseModel):
    """No documentation found for this operation."""
    rgb_view: RGBView = Field(alias='rgbView')
    'Get a single RGB render view by ID'

    class Arguments(BaseModel):
        """Arguments for GetRGBView """
        id: ID
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for GetRGBView """
        document = 'fragment View on View {\n  xMin\n  xMax\n  yMin\n  yMax\n  tMin\n  tMax\n  cMin\n  cMax\n  zMin\n  zMax\n  __typename\n}\n\nfragment ZarrStore on ZarrStore {\n  id\n  key\n  bucket\n  path\n  __typename\n}\n\nfragment RGBView on RGBView {\n  ...View\n  id\n  contexts {\n    id\n    name\n    __typename\n  }\n  name\n  image {\n    id\n    store {\n      ...ZarrStore\n      __typename\n    }\n    derivedScaleViews {\n      id\n      image {\n        id\n        store {\n          ...ZarrStore\n          __typename\n        }\n        __typename\n      }\n      scaleX\n      scaleY\n      scaleZ\n      scaleT\n      scaleC\n      __typename\n    }\n    __typename\n  }\n  colorMap\n  contrastLimitMin\n  contrastLimitMax\n  gamma\n  active\n  fullColour\n  baseColor\n  __typename\n}\n\nquery GetRGBView($id: ID!) {\n  rgbView(id: $id) {\n    ...RGBView\n    __typename\n  }\n}'

class SearchRGBViewsQueryOptions(BaseModel):
    """An RGB view describes how a subset of an image (typically a channel) is rendered in RGB within an RGB context, carrying color map, gamma and contrast limit settings."""
    typename: Literal['RGBView'] = Field(alias='__typename', default='RGBView', exclude=True)
    value: ID
    label: str
    model_config = ConfigDict(frozen=True)

class SearchRGBViewsQuery(BaseModel):
    """No documentation found for this operation."""
    options: Tuple[SearchRGBViewsQueryOptions, ...]
    'List RGB render views (per-channel display settings)'

    class Arguments(BaseModel):
        """Arguments for SearchRGBViews """
        search: Optional[str] = Field(default=None)
        values: Optional[List[ID]] = Field(default=None)
        limit: Optional[int] = Field(default=None)
        offset: Optional[int] = Field(default=0)
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for SearchRGBViews """
        document = 'query SearchRGBViews($search: String, $values: [ID!], $limit: Int, $offset: Int = 0) {\n  options: rgbViews(\n    filters: {search: $search, ids: $values}\n    pagination: {limit: $limit, offset: $offset}\n  ) {\n    value: id\n    label: name\n    __typename\n  }\n}'

class WatchFilesSubscriptionFiles(BaseModel):
    """No documentation"""
    typename: Literal['FileEvent'] = Field(alias='__typename', default='FileEvent', exclude=True)
    create: Optional[File] = Field(default=None)
    delete: Optional[ID] = Field(default=None)
    update: Optional[File] = Field(default=None)
    model_config = ConfigDict(frozen=True)

class WatchFilesSubscription(BaseModel):
    """No documentation found for this operation."""
    files: WatchFilesSubscriptionFiles
    'Subscribe to real-time file updates'

    class Arguments(BaseModel):
        """Arguments for WatchFiles """
        dataset: Optional[ID] = Field(default=None)
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for WatchFiles """
        document = 'fragment BigFileStore on BigFileStore {\n  id\n  key\n  bucket\n  path\n  presignedUrl\n  __typename\n}\n\nfragment File on File {\n  origins {\n    id\n    __typename\n  }\n  id\n  name\n  store {\n    ...BigFileStore\n    __typename\n  }\n  __typename\n}\n\nsubscription WatchFiles($dataset: ID) {\n  files(dataset: $dataset) {\n    create {\n      ...File\n      __typename\n    }\n    delete\n    update {\n      ...File\n      __typename\n    }\n    __typename\n  }\n}'

class WatchImagesSubscriptionImages(BaseModel):
    """No documentation"""
    typename: Literal['ImageEvent'] = Field(alias='__typename', default='ImageEvent', exclude=True)
    create: Optional[Image] = Field(default=None)
    delete: Optional[ID] = Field(default=None)
    update: Optional[Image] = Field(default=None)
    model_config = ConfigDict(frozen=True)

class WatchImagesSubscription(BaseModel):
    """No documentation found for this operation."""
    images: WatchImagesSubscriptionImages
    'Subscribe to real-time image updates'

    class Arguments(BaseModel):
        """Arguments for WatchImages """
        dataset: Optional[ID] = Field(default=None)
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for WatchImages """
        document = 'fragment Era on Era {\n  id\n  begin\n  name\n  __typename\n}\n\nfragment ReferenceView on ReferenceView {\n  ...View\n  id\n  __typename\n}\n\nfragment View on View {\n  xMin\n  xMax\n  yMin\n  yMax\n  tMin\n  tMax\n  cMin\n  cMax\n  zMin\n  zMax\n  __typename\n}\n\nfragment AcquisitionView on AcquisitionView {\n  ...View\n  id\n  description\n  acquiredAt\n  operator {\n    sub\n    __typename\n  }\n  __typename\n}\n\nfragment AffineTransformationView on AffineTransformationView {\n  ...View\n  id\n  affineMatrix\n  stage {\n    id\n    name\n    __typename\n  }\n  __typename\n}\n\nfragment ChannelView on ChannelView {\n  ...View\n  id\n  emissionWavelength\n  excitationWavelength\n  __typename\n}\n\nfragment ContinousScanView on ContinousScanView {\n  ...View\n  id\n  direction\n  __typename\n}\n\nfragment DerivedView on DerivedView {\n  ...View\n  id\n  originImage {\n    id\n    name\n    __typename\n  }\n  __typename\n}\n\nfragment FileView on FileView {\n  ...View\n  id\n  seriesIdentifier\n  file {\n    id\n    name\n    __typename\n  }\n  __typename\n}\n\nfragment InstanceMaskView on InstanceMaskView {\n  ...View\n  id\n  referenceView {\n    ...ReferenceView\n    __typename\n  }\n  __typename\n}\n\nfragment MaskView on MaskView {\n  ...View\n  id\n  referenceView {\n    ...ReferenceView\n    __typename\n  }\n  __typename\n}\n\nfragment OpticsView on OpticsView {\n  ...View\n  id\n  objective {\n    id\n    name\n    serialNumber\n    __typename\n  }\n  camera {\n    id\n    name\n    serialNumber\n    __typename\n  }\n  instrument {\n    id\n    name\n    serialNumber\n    __typename\n  }\n  __typename\n}\n\nfragment RGBView on RGBView {\n  ...View\n  id\n  contexts {\n    id\n    name\n    __typename\n  }\n  name\n  image {\n    id\n    store {\n      ...ZarrStore\n      __typename\n    }\n    derivedScaleViews {\n      id\n      image {\n        id\n        store {\n          ...ZarrStore\n          __typename\n        }\n        __typename\n      }\n      scaleX\n      scaleY\n      scaleZ\n      scaleT\n      scaleC\n      __typename\n    }\n    __typename\n  }\n  colorMap\n  contrastLimitMin\n  contrastLimitMax\n  gamma\n  active\n  fullColour\n  baseColor\n  __typename\n}\n\nfragment ROIView on ROIView {\n  ...View\n  id\n  roi {\n    id\n    name\n    __typename\n  }\n  __typename\n}\n\nfragment TimepointView on TimepointView {\n  ...View\n  id\n  msSinceStart\n  indexSinceStart\n  era {\n    ...Era\n    __typename\n  }\n  __typename\n}\n\nfragment WellPositionView on WellPositionView {\n  ...View\n  id\n  column\n  row\n  well {\n    id\n    rows\n    columns\n    name\n    __typename\n  }\n  __typename\n}\n\nfragment ZarrStore on ZarrStore {\n  id\n  key\n  bucket\n  path\n  __typename\n}\n\nfragment Image on Image {\n  id\n  name\n  store {\n    ...ZarrStore\n    __typename\n  }\n  views {\n    ...ChannelView\n    ...AffineTransformationView\n    ...TimepointView\n    ...OpticsView\n    ...AcquisitionView\n    ...RGBView\n    ...WellPositionView\n    ...DerivedView\n    ...ROIView\n    ...FileView\n    ...ContinousScanView\n    __typename\n  }\n  maskViews {\n    ...MaskView\n    __typename\n  }\n  instanceMaskViews {\n    ...InstanceMaskView\n    __typename\n  }\n  rgbContexts {\n    id\n    name\n    views {\n      ...RGBView\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nsubscription WatchImages($dataset: ID) {\n  images(dataset: $dataset) {\n    create {\n      ...Image\n      __typename\n    }\n    delete\n    update {\n      ...Image\n      __typename\n    }\n    __typename\n  }\n}'

class WatchRoisSubscriptionRois(BaseModel):
    """No documentation"""
    typename: Literal['RoiEvent'] = Field(alias='__typename', default='RoiEvent', exclude=True)
    create: Optional[ROI] = Field(default=None)
    delete: Optional[ID] = Field(default=None)
    update: Optional[ROI] = Field(default=None)
    model_config = ConfigDict(frozen=True)

class WatchRoisSubscription(BaseModel):
    """No documentation found for this operation."""
    rois: WatchRoisSubscriptionRois
    'Subscribe to real-time ROI updates'

    class Arguments(BaseModel):
        """Arguments for WatchRois """
        image: ID
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for WatchRois """
        document = 'fragment ZarrStore on ZarrStore {\n  id\n  key\n  bucket\n  path\n  __typename\n}\n\nfragment ROI on ROI {\n  id\n  image {\n    id\n    store {\n      ...ZarrStore\n      __typename\n    }\n    __typename\n  }\n  vectors\n  kind\n  __typename\n}\n\nsubscription WatchRois($image: ID!) {\n  rois(image: $image) {\n    create {\n      ...ROI\n      __typename\n    }\n    delete\n    update {\n      ...ROI\n      __typename\n    }\n    __typename\n  }\n}'

async def acreate_a_dataset(data: ArrayCoercible, scales: Iterable[ScaleInput], name: str, dim_descriptors: Iterable[DimensionDescriptorInput], anchors: Optional[Iterable[CoordinateAnchorInput]]=None, rath: Optional[MikroNextRath]=None) -> ADataset:
    """CreateADataset 

Create a new dataset from array-like data with optional choordinate anchors and OME  metadata

Args:
    data: The `ArrayLike` scalar type represents a reference to a store previously created by the user n a datalayer (required)
    scales: Input type for a scale, which specifies an array-like object to create the image from and optional scale factors for each dimension of the image (required) (list) (required)
    name: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text. (required)
    dim_descriptors: Input type for a dimension descriptor, which specifies a key and a kind for a dimension (required) (list) (required)
    anchors: Input type for a coordinate anchor, which specifies a list of dimension anchors to anchor to (required) (list)
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    ADataset
"""
    return (await aexecute(CreateADatasetMutation, {'input': {'data': data, 'scales': scales, 'name': name, 'dimDescriptors': dim_descriptors, 'anchors': anchors}}, rath=rath)).create_adataset

def create_a_dataset(data: ArrayCoercible, scales: Iterable[ScaleInput], name: str, dim_descriptors: Iterable[DimensionDescriptorInput], anchors: Optional[Iterable[CoordinateAnchorInput]]=None, rath: Optional[MikroNextRath]=None) -> ADataset:
    """CreateADataset 

Create a new dataset from array-like data with optional choordinate anchors and OME  metadata

Args:
    data: The `ArrayLike` scalar type represents a reference to a store previously created by the user n a datalayer (required)
    scales: Input type for a scale, which specifies an array-like object to create the image from and optional scale factors for each dimension of the image (required) (list) (required)
    name: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text. (required)
    dim_descriptors: Input type for a dimension descriptor, which specifies a key and a kind for a dimension (required) (list) (required)
    anchors: Input type for a coordinate anchor, which specifies a list of dimension anchors to anchor to (required) (list)
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    ADataset
"""
    return execute(CreateADatasetMutation, {'input': {'data': data, 'scales': scales, 'name': name, 'dimDescriptors': dim_descriptors, 'anchors': anchors}}, rath=rath).create_adataset

async def acreate_camera(serial_number: str, name: Optional[str]=None, model: Optional[str]=None, bit_depth: Optional[int]=None, sensor_size_x: Optional[int]=None, sensor_size_y: Optional[int]=None, pixel_size_x: Optional[Micrometers]=None, pixel_size_y: Optional[Micrometers]=None, manufacturer: Optional[str]=None, rath: Optional[MikroNextRath]=None) -> CreateCameraMutationCreatecamera:
    """CreateCamera 

Create a new camera configuration

Args:
    serial_number: The unique serial number of the camera
    name: The name of the camera
    model: The model of the camera
    bit_depth: The bit depth of the camera sensor
    sensor_size_x: The sensor size in x direction (pixels)
    sensor_size_y: The sensor size in y direction (pixels)
    pixel_size_x: The physical pixel size in x direction (micrometers)
    pixel_size_y: The physical pixel size in y direction (micrometers)
    manufacturer: The manufacturer of the camera
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    CreateCameraMutationCreatecamera
"""
    return (await aexecute(CreateCameraMutation, {'input': {'serialNumber': serial_number, 'name': name, 'model': model, 'bitDepth': bit_depth, 'sensorSizeX': sensor_size_x, 'sensorSizeY': sensor_size_y, 'pixelSizeX': pixel_size_x, 'pixelSizeY': pixel_size_y, 'manufacturer': manufacturer}}, rath=rath)).create_camera

def create_camera(serial_number: str, name: Optional[str]=None, model: Optional[str]=None, bit_depth: Optional[int]=None, sensor_size_x: Optional[int]=None, sensor_size_y: Optional[int]=None, pixel_size_x: Optional[Micrometers]=None, pixel_size_y: Optional[Micrometers]=None, manufacturer: Optional[str]=None, rath: Optional[MikroNextRath]=None) -> CreateCameraMutationCreatecamera:
    """CreateCamera 

Create a new camera configuration

Args:
    serial_number: The unique serial number of the camera
    name: The name of the camera
    model: The model of the camera
    bit_depth: The bit depth of the camera sensor
    sensor_size_x: The sensor size in x direction (pixels)
    sensor_size_y: The sensor size in y direction (pixels)
    pixel_size_x: The physical pixel size in x direction (micrometers)
    pixel_size_y: The physical pixel size in y direction (micrometers)
    manufacturer: The manufacturer of the camera
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    CreateCameraMutationCreatecamera
"""
    return execute(CreateCameraMutation, {'input': {'serialNumber': serial_number, 'name': name, 'model': model, 'bitDepth': bit_depth, 'sensorSizeX': sensor_size_x, 'sensorSizeY': sensor_size_y, 'pixelSizeX': pixel_size_x, 'pixelSizeY': pixel_size_y, 'manufacturer': manufacturer}}, rath=rath).create_camera

async def aensure_camera(serial_number: str, name: Optional[str]=None, model: Optional[str]=None, bit_depth: Optional[int]=None, sensor_size_x: Optional[int]=None, sensor_size_y: Optional[int]=None, pixel_size_x: Optional[Micrometers]=None, pixel_size_y: Optional[Micrometers]=None, manufacturer: Optional[str]=None, rath: Optional[MikroNextRath]=None) -> EnsureCameraMutationEnsurecamera:
    """EnsureCamera 

Ensure a camera exists, creating if needed

Args:
    serial_number: The unique serial number of the camera
    name: The name of the camera
    model: The model of the camera
    bit_depth: The bit depth of the camera sensor
    sensor_size_x: The sensor size in x direction (pixels)
    sensor_size_y: The sensor size in y direction (pixels)
    pixel_size_x: The physical pixel size in x direction (micrometers)
    pixel_size_y: The physical pixel size in y direction (micrometers)
    manufacturer: The manufacturer of the camera
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    EnsureCameraMutationEnsurecamera
"""
    return (await aexecute(EnsureCameraMutation, {'input': {'serialNumber': serial_number, 'name': name, 'model': model, 'bitDepth': bit_depth, 'sensorSizeX': sensor_size_x, 'sensorSizeY': sensor_size_y, 'pixelSizeX': pixel_size_x, 'pixelSizeY': pixel_size_y, 'manufacturer': manufacturer}}, rath=rath)).ensure_camera

def ensure_camera(serial_number: str, name: Optional[str]=None, model: Optional[str]=None, bit_depth: Optional[int]=None, sensor_size_x: Optional[int]=None, sensor_size_y: Optional[int]=None, pixel_size_x: Optional[Micrometers]=None, pixel_size_y: Optional[Micrometers]=None, manufacturer: Optional[str]=None, rath: Optional[MikroNextRath]=None) -> EnsureCameraMutationEnsurecamera:
    """EnsureCamera 

Ensure a camera exists, creating if needed

Args:
    serial_number: The unique serial number of the camera
    name: The name of the camera
    model: The model of the camera
    bit_depth: The bit depth of the camera sensor
    sensor_size_x: The sensor size in x direction (pixels)
    sensor_size_y: The sensor size in y direction (pixels)
    pixel_size_x: The physical pixel size in x direction (micrometers)
    pixel_size_y: The physical pixel size in y direction (micrometers)
    manufacturer: The manufacturer of the camera
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    EnsureCameraMutationEnsurecamera
"""
    return execute(EnsureCameraMutation, {'input': {'serialNumber': serial_number, 'name': name, 'model': model, 'bitDepth': bit_depth, 'sensorSizeX': sensor_size_x, 'sensorSizeY': sensor_size_y, 'pixelSizeX': pixel_size_x, 'pixelSizeY': pixel_size_y, 'manufacturer': manufacturer}}, rath=rath).ensure_camera

async def acreate_data_roi(dataset: IDCoercible, kind: RoiKind, x_dim: str, y_dim: str, vectors: Iterable[ThreeDVector], slices: Iterable[SliceInput], z_dim: Optional[str]=None, drawn_on_lens: Optional[IDCoercible]=None, rath: Optional[MikroNextRath]=None) -> DataRoi:
    """CreateDataRoi 

Create a new data ROI from vector or slice definitions with optional choordinate anchors and OME metadata

Args:
    dataset: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID. (required)
    kind: RoiKind (required)
    x_dim: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text. (required)
    y_dim: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text. (required)
    z_dim: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.
    vectors: The `Vector` scalar type represents a matrix values as specified by (required) (list) (required)
    slices: Input type for a dimension descriptor, which specifies a key and a kind for a dimension (required) (list) (required)
    drawn_on_lens: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID.
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    DataRoi
"""
    return (await aexecute(CreateDataRoiMutation, {'input': {'dataset': dataset, 'kind': kind, 'xDim': x_dim, 'yDim': y_dim, 'zDim': z_dim, 'vectors': vectors, 'slices': slices, 'drawnOnLens': drawn_on_lens}}, rath=rath)).create_data_roi

def create_data_roi(dataset: IDCoercible, kind: RoiKind, x_dim: str, y_dim: str, vectors: Iterable[ThreeDVector], slices: Iterable[SliceInput], z_dim: Optional[str]=None, drawn_on_lens: Optional[IDCoercible]=None, rath: Optional[MikroNextRath]=None) -> DataRoi:
    """CreateDataRoi 

Create a new data ROI from vector or slice definitions with optional choordinate anchors and OME metadata

Args:
    dataset: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID. (required)
    kind: RoiKind (required)
    x_dim: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text. (required)
    y_dim: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text. (required)
    z_dim: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.
    vectors: The `Vector` scalar type represents a matrix values as specified by (required) (list) (required)
    slices: Input type for a dimension descriptor, which specifies a key and a kind for a dimension (required) (list) (required)
    drawn_on_lens: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID.
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    DataRoi
"""
    return execute(CreateDataRoiMutation, {'input': {'dataset': dataset, 'kind': kind, 'xDim': x_dim, 'yDim': y_dim, 'zDim': z_dim, 'vectors': vectors, 'slices': slices, 'drawnOnLens': drawn_on_lens}}, rath=rath).create_data_roi

async def arequest_bigfile_upload(original_file_name: str, file_size: Optional[int]=None, content_type: Optional[str]=None, host: Optional[str]=None, port: Optional[int]=None, rath: Optional[MikroNextRath]=None) -> BigFileUploadGrant:
    """RequestBigfileUpload 

Request an upload grant for a big file store

Args:
    original_file_name: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text. (required)
    file_size: The `Int` scalar type represents non-fractional signed whole numeric values. Int can represent values between -(2^31) and 2^31 - 1.
    content_type: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.
    host: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.
    port: The `Int` scalar type represents non-fractional signed whole numeric values. Int can represent values between -(2^31) and 2^31 - 1.
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    BigFileUploadGrant
"""
    return (await aexecute(RequestBigfileUploadMutation, {'input': {'originalFileName': original_file_name, 'fileSize': file_size, 'contentType': content_type, 'host': host, 'port': port}}, rath=rath)).request_bigfile_upload

def request_bigfile_upload(original_file_name: str, file_size: Optional[int]=None, content_type: Optional[str]=None, host: Optional[str]=None, port: Optional[int]=None, rath: Optional[MikroNextRath]=None) -> BigFileUploadGrant:
    """RequestBigfileUpload 

Request an upload grant for a big file store

Args:
    original_file_name: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text. (required)
    file_size: The `Int` scalar type represents non-fractional signed whole numeric values. Int can represent values between -(2^31) and 2^31 - 1.
    content_type: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.
    host: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.
    port: The `Int` scalar type represents non-fractional signed whole numeric values. Int can represent values between -(2^31) and 2^31 - 1.
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    BigFileUploadGrant
"""
    return execute(RequestBigfileUploadMutation, {'input': {'originalFileName': original_file_name, 'fileSize': file_size, 'contentType': content_type, 'host': host, 'port': port}}, rath=rath).request_bigfile_upload

async def afinish_bigfile_upload(store_id: str, valid: bool, rath: Optional[MikroNextRath]=None) -> BigFileStore:
    """FinishBigfileUpload 

Finalize a big file upload after the client has written the object

Args:
    store_id: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text. (required)
    valid: The `Boolean` scalar type represents `true` or `false`. (required)
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    BigFileStore
"""
    return (await aexecute(FinishBigfileUploadMutation, {'input': {'storeId': store_id, 'valid': valid}}, rath=rath)).finish_bigfile_upload

def finish_bigfile_upload(store_id: str, valid: bool, rath: Optional[MikroNextRath]=None) -> BigFileStore:
    """FinishBigfileUpload 

Finalize a big file upload after the client has written the object

Args:
    store_id: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text. (required)
    valid: The `Boolean` scalar type represents `true` or `false`. (required)
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    BigFileStore
"""
    return execute(FinishBigfileUploadMutation, {'input': {'storeId': store_id, 'valid': valid}}, rath=rath).finish_bigfile_upload

async def arequest_bigfile_access(store_id: str, rath: Optional[MikroNextRath]=None) -> BigFileAccessGrant:
    """RequestBigfileAccess 

Request temporary S3 read credentials for a big file

Args:
    store_id: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text. (required)
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    BigFileAccessGrant
"""
    return (await aexecute(RequestBigfileAccessMutation, {'input': {'storeId': store_id}}, rath=rath)).request_bigfile_access

def request_bigfile_access(store_id: str, rath: Optional[MikroNextRath]=None) -> BigFileAccessGrant:
    """RequestBigfileAccess 

Request temporary S3 read credentials for a big file

Args:
    store_id: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text. (required)
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    BigFileAccessGrant
"""
    return execute(RequestBigfileAccessMutation, {'input': {'storeId': store_id}}, rath=rath).request_bigfile_access

async def arequest_media_upload(original_file_name: str, file_size: Optional[int]=None, content_type: Optional[str]=None, rath: Optional[MikroNextRath]=None) -> MediaUploadGrant:
    """RequestMediaUpload 

Upload media and return a URL for access

Args:
    original_file_name: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text. (required)
    file_size: The `Int` scalar type represents non-fractional signed whole numeric values. Int can represent values between -(2^31) and 2^31 - 1.
    content_type: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    MediaUploadGrant
"""
    return (await aexecute(RequestMediaUploadMutation, {'input': {'originalFileName': original_file_name, 'fileSize': file_size, 'contentType': content_type}}, rath=rath)).request_media_upload

def request_media_upload(original_file_name: str, file_size: Optional[int]=None, content_type: Optional[str]=None, rath: Optional[MikroNextRath]=None) -> MediaUploadGrant:
    """RequestMediaUpload 

Upload media and return a URL for access

Args:
    original_file_name: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text. (required)
    file_size: The `Int` scalar type represents non-fractional signed whole numeric values. Int can represent values between -(2^31) and 2^31 - 1.
    content_type: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    MediaUploadGrant
"""
    return execute(RequestMediaUploadMutation, {'input': {'originalFileName': original_file_name, 'fileSize': file_size, 'contentType': content_type}}, rath=rath).request_media_upload

async def afinish_media_upload(store_id: str, valid: bool, rath: Optional[MikroNextRath]=None) -> MediaStore:
    """FinishMediaUpload 

Finalize a media upload after the client has written the object

Args:
    store_id: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text. (required)
    valid: The `Boolean` scalar type represents `true` or `false`. (required)
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    MediaStore
"""
    return (await aexecute(FinishMediaUploadMutation, {'input': {'storeId': store_id, 'valid': valid}}, rath=rath)).finish_media_upload

def finish_media_upload(store_id: str, valid: bool, rath: Optional[MikroNextRath]=None) -> MediaStore:
    """FinishMediaUpload 

Finalize a media upload after the client has written the object

Args:
    store_id: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text. (required)
    valid: The `Boolean` scalar type represents `true` or `false`. (required)
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    MediaStore
"""
    return execute(FinishMediaUploadMutation, {'input': {'storeId': store_id, 'valid': valid}}, rath=rath).finish_media_upload

async def arequest_media_access(store_id: str, rath: Optional[MikroNextRath]=None) -> MediaAccessGrant:
    """RequestMediaAccess 

Request temporary S3 read credentials for a media file

Args:
    store_id: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text. (required)
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    MediaAccessGrant
"""
    return (await aexecute(RequestMediaAccessMutation, {'input': {'storeId': store_id}}, rath=rath)).request_media_access

def request_media_access(store_id: str, rath: Optional[MikroNextRath]=None) -> MediaAccessGrant:
    """RequestMediaAccess 

Request temporary S3 read credentials for a media file

Args:
    store_id: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text. (required)
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    MediaAccessGrant
"""
    return execute(RequestMediaAccessMutation, {'input': {'storeId': store_id}}, rath=rath).request_media_access

async def arequest_parquet_upload(content_type: Optional[str]=None, host: Optional[str]=None, port: Optional[int]=None, rath: Optional[MikroNextRath]=None) -> ParquetUploadGrant:
    """RequestParquetUpload 

Request an upload grant for a Parquet store

Args:
    content_type: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.
    host: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.
    port: The `Int` scalar type represents non-fractional signed whole numeric values. Int can represent values between -(2^31) and 2^31 - 1.
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    ParquetUploadGrant
"""
    return (await aexecute(RequestParquetUploadMutation, {'input': {'contentType': content_type, 'host': host, 'port': port}}, rath=rath)).request_parquet_upload

def request_parquet_upload(content_type: Optional[str]=None, host: Optional[str]=None, port: Optional[int]=None, rath: Optional[MikroNextRath]=None) -> ParquetUploadGrant:
    """RequestParquetUpload 

Request an upload grant for a Parquet store

Args:
    content_type: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.
    host: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.
    port: The `Int` scalar type represents non-fractional signed whole numeric values. Int can represent values between -(2^31) and 2^31 - 1.
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    ParquetUploadGrant
"""
    return execute(RequestParquetUploadMutation, {'input': {'contentType': content_type, 'host': host, 'port': port}}, rath=rath).request_parquet_upload

async def afinish_parquet_upload(store_id: str, valid: bool, rath: Optional[MikroNextRath]=None) -> ParquetStore:
    """FinishParquetUpload 

Finalize a Parquet upload after the client has written the object

Args:
    store_id: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text. (required)
    valid: The `Boolean` scalar type represents `true` or `false`. (required)
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    ParquetStore
"""
    return (await aexecute(FinishParquetUploadMutation, {'input': {'storeId': store_id, 'valid': valid}}, rath=rath)).finish_parquet_upload

def finish_parquet_upload(store_id: str, valid: bool, rath: Optional[MikroNextRath]=None) -> ParquetStore:
    """FinishParquetUpload 

Finalize a Parquet upload after the client has written the object

Args:
    store_id: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text. (required)
    valid: The `Boolean` scalar type represents `true` or `false`. (required)
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    ParquetStore
"""
    return execute(FinishParquetUploadMutation, {'input': {'storeId': store_id, 'valid': valid}}, rath=rath).finish_parquet_upload

async def arequest_parquet_access(store_id: str, rath: Optional[MikroNextRath]=None) -> ParquetAccessGrant:
    """RequestParquetAccess 

Request temporary S3 read credentials for a Parquet file

Args:
    store_id: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text. (required)
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    ParquetAccessGrant
"""
    return (await aexecute(RequestParquetAccessMutation, {'input': {'storeId': store_id}}, rath=rath)).request_parquet_access

def request_parquet_access(store_id: str, rath: Optional[MikroNextRath]=None) -> ParquetAccessGrant:
    """RequestParquetAccess 

Request temporary S3 read credentials for a Parquet file

Args:
    store_id: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text. (required)
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    ParquetAccessGrant
"""
    return execute(RequestParquetAccessMutation, {'input': {'storeId': store_id}}, rath=rath).request_parquet_access

async def arequest_zarr_upload(shape: Optional[Iterable[int]]=None, chunks: Optional[Iterable[int]]=None, version: Optional[str]=None, host: Optional[str]=None, port: Optional[int]=None, rath: Optional[MikroNextRath]=None) -> ZarrUploadGrant:
    """RequestZarrUpload 

Request an upload grant for a Zarr store

Args:
    shape: The `Int` scalar type represents non-fractional signed whole numeric values. Int can represent values between -(2^31) and 2^31 - 1. (required) (list)
    chunks: The `Int` scalar type represents non-fractional signed whole numeric values. Int can represent values between -(2^31) and 2^31 - 1. (required) (list)
    version: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.
    host: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.
    port: The `Int` scalar type represents non-fractional signed whole numeric values. Int can represent values between -(2^31) and 2^31 - 1.
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    ZarrUploadGrant
"""
    return (await aexecute(RequestZarrUploadMutation, {'input': {'shape': shape, 'chunks': chunks, 'version': version, 'host': host, 'port': port}}, rath=rath)).request_zarr_upload

def request_zarr_upload(shape: Optional[Iterable[int]]=None, chunks: Optional[Iterable[int]]=None, version: Optional[str]=None, host: Optional[str]=None, port: Optional[int]=None, rath: Optional[MikroNextRath]=None) -> ZarrUploadGrant:
    """RequestZarrUpload 

Request an upload grant for a Zarr store

Args:
    shape: The `Int` scalar type represents non-fractional signed whole numeric values. Int can represent values between -(2^31) and 2^31 - 1. (required) (list)
    chunks: The `Int` scalar type represents non-fractional signed whole numeric values. Int can represent values between -(2^31) and 2^31 - 1. (required) (list)
    version: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.
    host: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.
    port: The `Int` scalar type represents non-fractional signed whole numeric values. Int can represent values between -(2^31) and 2^31 - 1.
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    ZarrUploadGrant
"""
    return execute(RequestZarrUploadMutation, {'input': {'shape': shape, 'chunks': chunks, 'version': version, 'host': host, 'port': port}}, rath=rath).request_zarr_upload

async def afinish_zarr_upload(store_id: str, valid: bool, rath: Optional[MikroNextRath]=None) -> ZarrStore:
    """FinishZarrUpload 

Finalize a Zarr upload after the client has written the object

Args:
    store_id: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text. (required)
    valid: The `Boolean` scalar type represents `true` or `false`. (required)
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    ZarrStore
"""
    return (await aexecute(FinishZarrUploadMutation, {'input': {'storeId': store_id, 'valid': valid}}, rath=rath)).finish_zarr_upload

def finish_zarr_upload(store_id: str, valid: bool, rath: Optional[MikroNextRath]=None) -> ZarrStore:
    """FinishZarrUpload 

Finalize a Zarr upload after the client has written the object

Args:
    store_id: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text. (required)
    valid: The `Boolean` scalar type represents `true` or `false`. (required)
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    ZarrStore
"""
    return execute(FinishZarrUploadMutation, {'input': {'storeId': store_id, 'valid': valid}}, rath=rath).finish_zarr_upload

async def arequest_zarr_access(store_id: str, rath: Optional[MikroNextRath]=None) -> ZarrAccessGrant:
    """RequestZarrAccess 

Request temporary S3 read credentials for a Zarr store

Args:
    store_id: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text. (required)
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    ZarrAccessGrant
"""
    return (await aexecute(RequestZarrAccessMutation, {'input': {'storeId': store_id}}, rath=rath)).request_zarr_access

def request_zarr_access(store_id: str, rath: Optional[MikroNextRath]=None) -> ZarrAccessGrant:
    """RequestZarrAccess 

Request temporary S3 read credentials for a Zarr store

Args:
    store_id: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text. (required)
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    ZarrAccessGrant
"""
    return execute(RequestZarrAccessMutation, {'input': {'storeId': store_id}}, rath=rath).request_zarr_access

async def acreate_dataset(name: str, parent: Optional[IDCoercible]=None, rath: Optional[MikroNextRath]=None) -> Dataset:
    """CreateDataset 

Create a new dataset to organize data

Args:
    name: The name of the dataset
    parent: The ID of the parent dataset to nest this dataset under
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    Dataset
"""
    return (await aexecute(CreateDatasetMutation, {'input': {'name': name, 'parent': parent}}, rath=rath)).create_dataset

def create_dataset(name: str, parent: Optional[IDCoercible]=None, rath: Optional[MikroNextRath]=None) -> Dataset:
    """CreateDataset 

Create a new dataset to organize data

Args:
    name: The name of the dataset
    parent: The ID of the parent dataset to nest this dataset under
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    Dataset
"""
    return execute(CreateDatasetMutation, {'input': {'name': name, 'parent': parent}}, rath=rath).create_dataset

async def aensure_dataset(name: str, parent: Optional[IDCoercible]=None, rath: Optional[MikroNextRath]=None) -> Dataset:
    """EnsureDataset 

Create a new dataset to organize data

Args:
    name: The name of the dataset
    parent: The ID of the parent dataset to nest this dataset under
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    Dataset
"""
    return (await aexecute(EnsureDatasetMutation, {'input': {'name': name, 'parent': parent}}, rath=rath)).ensure_dataset

def ensure_dataset(name: str, parent: Optional[IDCoercible]=None, rath: Optional[MikroNextRath]=None) -> Dataset:
    """EnsureDataset 

Create a new dataset to organize data

Args:
    name: The name of the dataset
    parent: The ID of the parent dataset to nest this dataset under
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    Dataset
"""
    return execute(EnsureDatasetMutation, {'input': {'name': name, 'parent': parent}}, rath=rath).ensure_dataset

async def aupdate_dataset(name: str, id: IDCoercible, parent: Optional[IDCoercible]=None, rath: Optional[MikroNextRath]=None) -> Dataset:
    """UpdateDataset 

Update dataset metadata

Args:
    name: The name of the dataset
    parent: The ID of the parent dataset to nest this dataset under
    id: The ID of the dataset to change
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    Dataset
"""
    return (await aexecute(UpdateDatasetMutation, {'input': {'name': name, 'parent': parent, 'id': id}}, rath=rath)).update_dataset

def update_dataset(name: str, id: IDCoercible, parent: Optional[IDCoercible]=None, rath: Optional[MikroNextRath]=None) -> Dataset:
    """UpdateDataset 

Update dataset metadata

Args:
    name: The name of the dataset
    parent: The ID of the parent dataset to nest this dataset under
    id: The ID of the dataset to change
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    Dataset
"""
    return execute(UpdateDatasetMutation, {'input': {'name': name, 'parent': parent, 'id': id}}, rath=rath).update_dataset

async def arevert_dataset(id: IDCoercible, history_id: IDCoercible, rath: Optional[MikroNextRath]=None) -> Dataset:
    """RevertDataset 

Revert dataset to a previous version

Args:
    id: The ID of the dataset to revert
    history_id: The ID of the provenance history entry to revert the dataset to
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    Dataset
"""
    return (await aexecute(RevertDatasetMutation, {'input': {'id': id, 'historyId': history_id}}, rath=rath)).revert_dataset

def revert_dataset(id: IDCoercible, history_id: IDCoercible, rath: Optional[MikroNextRath]=None) -> Dataset:
    """RevertDataset 

Revert dataset to a previous version

Args:
    id: The ID of the dataset to revert
    history_id: The ID of the provenance history entry to revert the dataset to
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    Dataset
"""
    return execute(RevertDatasetMutation, {'input': {'id': id, 'historyId': history_id}}, rath=rath).revert_dataset

async def acreate_era(name: str, begin: Optional[datetime]=None, rath: Optional[MikroNextRath]=None) -> CreateEraMutationCreateera:
    """CreateEra 

Create a new era for temporal organization

Args:
    name: The name of the era
    begin: The datetime at which the era begins
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    CreateEraMutationCreateera
"""
    return (await aexecute(CreateEraMutation, {'input': {'name': name, 'begin': begin}}, rath=rath)).create_era

def create_era(name: str, begin: Optional[datetime]=None, rath: Optional[MikroNextRath]=None) -> CreateEraMutationCreateera:
    """CreateEra 

Create a new era for temporal organization

Args:
    name: The name of the era
    begin: The datetime at which the era begins
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    CreateEraMutationCreateera
"""
    return execute(CreateEraMutation, {'input': {'name': name, 'begin': begin}}, rath=rath).create_era

async def afrom_file_like(file: ImageFileCoercible, file_name: str, dataset: Optional[IDCoercible]=None, origins: Optional[Iterable[IDCoercible]]=None, rath: Optional[MikroNextRath]=None) -> File:
    """FromFileLike 

Create a file from file-like data

Args:
    file: The uploaded big-file store to create the file from
    file_name: The name of the file
    dataset: The ID of the dataset to put the file in (defaults to the current default dataset)
    origins: The IDs of entities this file was derived from
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    File
"""
    return (await aexecute(FromFileLikeMutation, {'input': {'file': file, 'fileName': file_name, 'dataset': dataset, 'origins': origins}}, rath=rath)).from_file_like

def from_file_like(file: ImageFileCoercible, file_name: str, dataset: Optional[IDCoercible]=None, origins: Optional[Iterable[IDCoercible]]=None, rath: Optional[MikroNextRath]=None) -> File:
    """FromFileLike 

Create a file from file-like data

Args:
    file: The uploaded big-file store to create the file from
    file_name: The name of the file
    dataset: The ID of the dataset to put the file in (defaults to the current default dataset)
    origins: The IDs of entities this file was derived from
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    File
"""
    return execute(FromFileLikeMutation, {'input': {'file': file, 'fileName': file_name, 'dataset': dataset, 'origins': origins}}, rath=rath).from_file_like

async def afrom_array_like(array: ImageCoercible, name: str, dataset: Optional[IDCoercible]=None, channel_views: Optional[Iterable[PartialChannelViewInput]]=None, transformation_views: Optional[Iterable[PartialAffineTransformationViewInput]]=None, acquisition_views: Optional[Iterable[PartialAcquisitionViewInput]]=None, mask_views: Optional[Iterable[PartialMaskViewInput]]=None, reference_views: Optional[Iterable[PartialReferenceViewInput]]=None, instance_mask_views: Optional[Iterable[PartialInstanceMaskViewInput]]=None, rgb_views: Optional[Iterable[PartialRGBViewInput]]=None, timepoint_views: Optional[Iterable[PartialTimepointViewInput]]=None, optics_views: Optional[Iterable[PartialOpticsViewInput]]=None, scale_views: Optional[Iterable[PartialScaleViewInput]]=None, tags: Optional[Iterable[str]]=None, roi_views: Optional[Iterable[PartialROIViewInput]]=None, file_views: Optional[Iterable[PartialFileViewInput]]=None, derived_views: Optional[Iterable[PartialDerivedViewInput]]=None, lightpath_views: Optional[Iterable[PartialLightpathViewInput]]=None, rath: Optional[MikroNextRath]=None) -> Image:
    """from_array_like 

Create an image from array-like data

Args:
    array: The array-like object to create the image from
    name: The name of the image
    dataset: Optional dataset ID to associate the image with
    channel_views: Optional list of channel views
    transformation_views: Optional list of affine transformation views
    acquisition_views: Optional list of acquisition views
    mask_views: Optional list of mask views
    reference_views: Optional list of reference views
    instance_mask_views: Optional list of instance mask views
    rgb_views: Optional list of RGB views
    timepoint_views: Optional list of timepoint views
    optics_views: Optional list of optics views
    scale_views: Optional list of scale views
    tags: Optional list of tags to associate with the image
    roi_views: Optional list of ROI views
    file_views: Optional list of file views
    derived_views: Optional list of derived views
    lightpath_views: Optional list of lightpath views
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    Image
"""
    return (await aexecute(From_array_likeMutation, {'input': {'array': array, 'name': name, 'dataset': dataset, 'channelViews': channel_views, 'transformationViews': transformation_views, 'acquisitionViews': acquisition_views, 'maskViews': mask_views, 'referenceViews': reference_views, 'instanceMaskViews': instance_mask_views, 'rgbViews': rgb_views, 'timepointViews': timepoint_views, 'opticsViews': optics_views, 'scaleViews': scale_views, 'tags': tags, 'roiViews': roi_views, 'fileViews': file_views, 'derivedViews': derived_views, 'lightpathViews': lightpath_views}}, rath=rath)).from_array_like

def from_array_like(array: ImageCoercible, name: str, dataset: Optional[IDCoercible]=None, channel_views: Optional[Iterable[PartialChannelViewInput]]=None, transformation_views: Optional[Iterable[PartialAffineTransformationViewInput]]=None, acquisition_views: Optional[Iterable[PartialAcquisitionViewInput]]=None, mask_views: Optional[Iterable[PartialMaskViewInput]]=None, reference_views: Optional[Iterable[PartialReferenceViewInput]]=None, instance_mask_views: Optional[Iterable[PartialInstanceMaskViewInput]]=None, rgb_views: Optional[Iterable[PartialRGBViewInput]]=None, timepoint_views: Optional[Iterable[PartialTimepointViewInput]]=None, optics_views: Optional[Iterable[PartialOpticsViewInput]]=None, scale_views: Optional[Iterable[PartialScaleViewInput]]=None, tags: Optional[Iterable[str]]=None, roi_views: Optional[Iterable[PartialROIViewInput]]=None, file_views: Optional[Iterable[PartialFileViewInput]]=None, derived_views: Optional[Iterable[PartialDerivedViewInput]]=None, lightpath_views: Optional[Iterable[PartialLightpathViewInput]]=None, rath: Optional[MikroNextRath]=None) -> Image:
    """from_array_like 

Create an image from array-like data

Args:
    array: The array-like object to create the image from
    name: The name of the image
    dataset: Optional dataset ID to associate the image with
    channel_views: Optional list of channel views
    transformation_views: Optional list of affine transformation views
    acquisition_views: Optional list of acquisition views
    mask_views: Optional list of mask views
    reference_views: Optional list of reference views
    instance_mask_views: Optional list of instance mask views
    rgb_views: Optional list of RGB views
    timepoint_views: Optional list of timepoint views
    optics_views: Optional list of optics views
    scale_views: Optional list of scale views
    tags: Optional list of tags to associate with the image
    roi_views: Optional list of ROI views
    file_views: Optional list of file views
    derived_views: Optional list of derived views
    lightpath_views: Optional list of lightpath views
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    Image
"""
    return execute(From_array_likeMutation, {'input': {'array': array, 'name': name, 'dataset': dataset, 'channelViews': channel_views, 'transformationViews': transformation_views, 'acquisitionViews': acquisition_views, 'maskViews': mask_views, 'referenceViews': reference_views, 'instanceMaskViews': instance_mask_views, 'rgbViews': rgb_views, 'timepointViews': timepoint_views, 'opticsViews': optics_views, 'scaleViews': scale_views, 'tags': tags, 'roiViews': roi_views, 'fileViews': file_views, 'derivedViews': derived_views, 'lightpathViews': lightpath_views}}, rath=rath).from_array_like

async def acreate_instrument(serial_number: str, manufacturer: Optional[str]=None, name: Optional[str]=None, model: Optional[str]=None, rath: Optional[MikroNextRath]=None) -> CreateInstrumentMutationCreateinstrument:
    """CreateInstrument 

Create a new instrument configuration

Args:
    serial_number: The unique serial number of the instrument
    manufacturer: The manufacturer of the instrument
    name: The name of the instrument
    model: The model of the instrument
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    CreateInstrumentMutationCreateinstrument
"""
    return (await aexecute(CreateInstrumentMutation, {'input': {'serialNumber': serial_number, 'manufacturer': manufacturer, 'name': name, 'model': model}}, rath=rath)).create_instrument

def create_instrument(serial_number: str, manufacturer: Optional[str]=None, name: Optional[str]=None, model: Optional[str]=None, rath: Optional[MikroNextRath]=None) -> CreateInstrumentMutationCreateinstrument:
    """CreateInstrument 

Create a new instrument configuration

Args:
    serial_number: The unique serial number of the instrument
    manufacturer: The manufacturer of the instrument
    name: The name of the instrument
    model: The model of the instrument
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    CreateInstrumentMutationCreateinstrument
"""
    return execute(CreateInstrumentMutation, {'input': {'serialNumber': serial_number, 'manufacturer': manufacturer, 'name': name, 'model': model}}, rath=rath).create_instrument

async def aensure_instrument(serial_number: str, manufacturer: Optional[str]=None, name: Optional[str]=None, model: Optional[str]=None, rath: Optional[MikroNextRath]=None) -> EnsureInstrumentMutationEnsureinstrument:
    """EnsureInstrument 

Ensure an instrument exists, creating if needed

Args:
    serial_number: The unique serial number of the instrument
    manufacturer: The manufacturer of the instrument
    name: The name of the instrument
    model: The model of the instrument
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    EnsureInstrumentMutationEnsureinstrument
"""
    return (await aexecute(EnsureInstrumentMutation, {'input': {'serialNumber': serial_number, 'manufacturer': manufacturer, 'name': name, 'model': model}}, rath=rath)).ensure_instrument

def ensure_instrument(serial_number: str, manufacturer: Optional[str]=None, name: Optional[str]=None, model: Optional[str]=None, rath: Optional[MikroNextRath]=None) -> EnsureInstrumentMutationEnsureinstrument:
    """EnsureInstrument 

Ensure an instrument exists, creating if needed

Args:
    serial_number: The unique serial number of the instrument
    manufacturer: The manufacturer of the instrument
    name: The name of the instrument
    model: The model of the instrument
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    EnsureInstrumentMutationEnsureinstrument
"""
    return execute(EnsureInstrumentMutation, {'input': {'serialNumber': serial_number, 'manufacturer': manufacturer, 'name': name, 'model': model}}, rath=rath).ensure_instrument

async def acreate_layer(lens: IDCoercible, scene: IDCoercible, affine_matrix: Optional[Iterable[Iterable[float]]]=None, colormap: Optional[ColorMap]=None, color: Optional[Iterable[int]]=None, clim_min: Optional[float]=None, clim_max: Optional[float]=None, x_dim: Optional[str]=None, y_dim: Optional[str]=None, z_dim: Optional[str]=None, t_dim: Optional[str]=None, intensity_dim: Optional[str]=None, rath: Optional[MikroNextRath]=None) -> Layer:
    """CreateLayer 

Create a new layer from an existing lens with optional affine transformation and colormap settings

Args:
    lens: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID. (required)
    scene: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID. (required)
    affine_matrix: The `Float` scalar type represents signed double-precision fractional values as specified by [IEEE 754](https://en.wikipedia.org/wiki/IEEE_floating_point). (required) (list) (required) (list)
    colormap: ColorMap
    color: The `Int` scalar type represents non-fractional signed whole numeric values. Int can represent values between -(2^31) and 2^31 - 1. (required) (list)
    clim_min: The `Float` scalar type represents signed double-precision fractional values as specified by [IEEE 754](https://en.wikipedia.org/wiki/IEEE_floating_point).
    clim_max: The `Float` scalar type represents signed double-precision fractional values as specified by [IEEE 754](https://en.wikipedia.org/wiki/IEEE_floating_point).
    x_dim: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.
    y_dim: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.
    z_dim: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.
    t_dim: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.
    intensity_dim: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    Layer
"""
    return (await aexecute(CreateLayerMutation, {'input': {'lens': lens, 'scene': scene, 'affineMatrix': affine_matrix, 'colormap': colormap, 'color': color, 'climMin': clim_min, 'climMax': clim_max, 'xDim': x_dim, 'yDim': y_dim, 'zDim': z_dim, 'tDim': t_dim, 'intensityDim': intensity_dim}}, rath=rath)).create_layer

def create_layer(lens: IDCoercible, scene: IDCoercible, affine_matrix: Optional[Iterable[Iterable[float]]]=None, colormap: Optional[ColorMap]=None, color: Optional[Iterable[int]]=None, clim_min: Optional[float]=None, clim_max: Optional[float]=None, x_dim: Optional[str]=None, y_dim: Optional[str]=None, z_dim: Optional[str]=None, t_dim: Optional[str]=None, intensity_dim: Optional[str]=None, rath: Optional[MikroNextRath]=None) -> Layer:
    """CreateLayer 

Create a new layer from an existing lens with optional affine transformation and colormap settings

Args:
    lens: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID. (required)
    scene: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID. (required)
    affine_matrix: The `Float` scalar type represents signed double-precision fractional values as specified by [IEEE 754](https://en.wikipedia.org/wiki/IEEE_floating_point). (required) (list) (required) (list)
    colormap: ColorMap
    color: The `Int` scalar type represents non-fractional signed whole numeric values. Int can represent values between -(2^31) and 2^31 - 1. (required) (list)
    clim_min: The `Float` scalar type represents signed double-precision fractional values as specified by [IEEE 754](https://en.wikipedia.org/wiki/IEEE_floating_point).
    clim_max: The `Float` scalar type represents signed double-precision fractional values as specified by [IEEE 754](https://en.wikipedia.org/wiki/IEEE_floating_point).
    x_dim: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.
    y_dim: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.
    z_dim: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.
    t_dim: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.
    intensity_dim: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    Layer
"""
    return execute(CreateLayerMutation, {'input': {'lens': lens, 'scene': scene, 'affineMatrix': affine_matrix, 'colormap': colormap, 'color': color, 'climMin': clim_min, 'climMax': clim_max, 'xDim': x_dim, 'yDim': y_dim, 'zDim': z_dim, 'tDim': t_dim, 'intensityDim': intensity_dim}}, rath=rath).create_layer

async def acreate_lens(dataset: IDCoercible, slices: Iterable[SliceInput], rath: Optional[MikroNextRath]=None) -> Lens:
    """CreateLens 

Create a new lens from an existing dataset and slicing constraints

Args:
    dataset: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID. (required)
    slices: Input type for a dimension descriptor, which specifies a key and a kind for a dimension (required) (list) (required)
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    Lens
"""
    return (await aexecute(CreateLensMutation, {'input': {'dataset': dataset, 'slices': slices}}, rath=rath)).create_lens

def create_lens(dataset: IDCoercible, slices: Iterable[SliceInput], rath: Optional[MikroNextRath]=None) -> Lens:
    """CreateLens 

Create a new lens from an existing dataset and slicing constraints

Args:
    dataset: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID. (required)
    slices: Input type for a dimension descriptor, which specifies a key and a kind for a dimension (required) (list) (required)
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    Lens
"""
    return execute(CreateLensMutation, {'input': {'dataset': dataset, 'slices': slices}}, rath=rath).create_lens

async def acreate_mesh(mesh: MeshCoercible, name: str, rath: Optional[MikroNextRath]=None) -> Mesh:
    """CreateMesh 

Create a new mesh

Args:
    mesh: The uploaded mesh file store to create the mesh from
    name: The name of the mesh
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    Mesh
"""
    return (await aexecute(CreateMeshMutation, {'input': {'mesh': mesh, 'name': name}}, rath=rath)).create_mesh

def create_mesh(mesh: MeshCoercible, name: str, rath: Optional[MikroNextRath]=None) -> Mesh:
    """CreateMesh 

Create a new mesh

Args:
    mesh: The uploaded mesh file store to create the mesh from
    name: The name of the mesh
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    Mesh
"""
    return execute(CreateMeshMutation, {'input': {'mesh': mesh, 'name': name}}, rath=rath).create_mesh

async def acreate_objective(serial_number: str, name: Optional[str]=None, na: Optional[float]=None, magnification: Optional[float]=None, immersion: Optional[str]=None, rath: Optional[MikroNextRath]=None) -> CreateObjectiveMutationCreateobjective:
    """CreateObjective 

Create a new microscope objective configuration

Args:
    serial_number: The unique serial number of the objective
    name: The name of the objective
    na: The numerical aperture of the objective
    magnification: The magnification of the objective
    immersion: The immersion medium of the objective (e.g. oil, water, air)
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    CreateObjectiveMutationCreateobjective
"""
    return (await aexecute(CreateObjectiveMutation, {'input': {'serialNumber': serial_number, 'name': name, 'na': na, 'magnification': magnification, 'immersion': immersion}}, rath=rath)).create_objective

def create_objective(serial_number: str, name: Optional[str]=None, na: Optional[float]=None, magnification: Optional[float]=None, immersion: Optional[str]=None, rath: Optional[MikroNextRath]=None) -> CreateObjectiveMutationCreateobjective:
    """CreateObjective 

Create a new microscope objective configuration

Args:
    serial_number: The unique serial number of the objective
    name: The name of the objective
    na: The numerical aperture of the objective
    magnification: The magnification of the objective
    immersion: The immersion medium of the objective (e.g. oil, water, air)
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    CreateObjectiveMutationCreateobjective
"""
    return execute(CreateObjectiveMutation, {'input': {'serialNumber': serial_number, 'name': name, 'na': na, 'magnification': magnification, 'immersion': immersion}}, rath=rath).create_objective

async def aensure_objective(serial_number: str, name: Optional[str]=None, na: Optional[float]=None, magnification: Optional[float]=None, immersion: Optional[str]=None, rath: Optional[MikroNextRath]=None) -> EnsureObjectiveMutationEnsureobjective:
    """EnsureObjective 

Ensure an objective exists, creating if needed

Args:
    serial_number: The unique serial number of the objective
    name: The name of the objective
    na: The numerical aperture of the objective
    magnification: The magnification of the objective
    immersion: The immersion medium of the objective (e.g. oil, water, air)
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    EnsureObjectiveMutationEnsureobjective
"""
    return (await aexecute(EnsureObjectiveMutation, {'input': {'serialNumber': serial_number, 'name': name, 'na': na, 'magnification': magnification, 'immersion': immersion}}, rath=rath)).ensure_objective

def ensure_objective(serial_number: str, name: Optional[str]=None, na: Optional[float]=None, magnification: Optional[float]=None, immersion: Optional[str]=None, rath: Optional[MikroNextRath]=None) -> EnsureObjectiveMutationEnsureobjective:
    """EnsureObjective 

Ensure an objective exists, creating if needed

Args:
    serial_number: The unique serial number of the objective
    name: The name of the objective
    na: The numerical aperture of the objective
    magnification: The magnification of the objective
    immersion: The immersion medium of the objective (e.g. oil, water, air)
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    EnsureObjectiveMutationEnsureobjective
"""
    return execute(EnsureObjectiveMutation, {'input': {'serialNumber': serial_number, 'name': name, 'na': na, 'magnification': magnification, 'immersion': immersion}}, rath=rath).ensure_objective

async def acreate_render_tree(tree: TreeInput, name: str, rath: Optional[MikroNextRath]=None) -> CreateRenderTreeMutationCreaterendertree:
    """CreateRenderTree 

Create a new render tree for image visualization

Args:
    tree:  (required)
    name: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text. (required)
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    CreateRenderTreeMutationCreaterendertree
"""
    return (await aexecute(CreateRenderTreeMutation, {'input': {'tree': tree, 'name': name}}, rath=rath)).create_render_tree

def create_render_tree(tree: TreeInput, name: str, rath: Optional[MikroNextRath]=None) -> CreateRenderTreeMutationCreaterendertree:
    """CreateRenderTree 

Create a new render tree for image visualization

Args:
    tree:  (required)
    name: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text. (required)
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    CreateRenderTreeMutationCreaterendertree
"""
    return execute(CreateRenderTreeMutation, {'input': {'tree': tree, 'name': name}}, rath=rath).create_render_tree

async def acreate_rgb_context(image: IDCoercible, name: Optional[str]=None, thumbnail: Optional[IDCoercible]=None, views: Optional[Iterable[PartialRGBViewInput]]=None, z: Optional[int]=None, t: Optional[int]=None, c: Optional[int]=None, rath: Optional[MikroNextRath]=None) -> RGBContext:
    """CreateRGBContext 

Create a new RGB context for image visualization

Args:
    name: The name of the RGB context
    thumbnail: The ID of an uploaded media store to use as the thumbnail snapshot
    image: The ID of the image this RGB context renders
    views: The RGB views (channel rendering settings) to attach to the context
    z: The z plane the context renders
    t: The timepoint the context renders
    c: The channel the context renders
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    RGBContext
"""
    return (await aexecute(CreateRGBContextMutation, {'input': {'name': name, 'thumbnail': thumbnail, 'image': image, 'views': views, 'z': z, 't': t, 'c': c}}, rath=rath)).create_rgb_context

def create_rgb_context(image: IDCoercible, name: Optional[str]=None, thumbnail: Optional[IDCoercible]=None, views: Optional[Iterable[PartialRGBViewInput]]=None, z: Optional[int]=None, t: Optional[int]=None, c: Optional[int]=None, rath: Optional[MikroNextRath]=None) -> RGBContext:
    """CreateRGBContext 

Create a new RGB context for image visualization

Args:
    name: The name of the RGB context
    thumbnail: The ID of an uploaded media store to use as the thumbnail snapshot
    image: The ID of the image this RGB context renders
    views: The RGB views (channel rendering settings) to attach to the context
    z: The z plane the context renders
    t: The timepoint the context renders
    c: The channel the context renders
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    RGBContext
"""
    return execute(CreateRGBContextMutation, {'input': {'name': name, 'thumbnail': thumbnail, 'image': image, 'views': views, 'z': z, 't': t, 'c': c}}, rath=rath).create_rgb_context

async def aupdate_rgb_context(id: IDCoercible, name: Optional[str]=None, thumbnail: Optional[IDCoercible]=None, views: Optional[Iterable[PartialRGBViewInput]]=None, z: Optional[int]=None, t: Optional[int]=None, c: Optional[int]=None, rath: Optional[MikroNextRath]=None) -> RGBContext:
    """UpdateRGBContext 

Update settings of an existing RGB context

Args:
    id: The ID of the RGB context to update
    name: The new name of the RGB context
    thumbnail: The ID of an uploaded media store to use as the thumbnail snapshot
    views: The RGB views (channel rendering settings) to replace the context's views with
    z: The z plane the context renders
    t: The timepoint the context renders
    c: The channel the context renders
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    RGBContext
"""
    return (await aexecute(UpdateRGBContextMutation, {'input': {'id': id, 'name': name, 'thumbnail': thumbnail, 'views': views, 'z': z, 't': t, 'c': c}}, rath=rath)).update_rgb_context

def update_rgb_context(id: IDCoercible, name: Optional[str]=None, thumbnail: Optional[IDCoercible]=None, views: Optional[Iterable[PartialRGBViewInput]]=None, z: Optional[int]=None, t: Optional[int]=None, c: Optional[int]=None, rath: Optional[MikroNextRath]=None) -> RGBContext:
    """UpdateRGBContext 

Update settings of an existing RGB context

Args:
    id: The ID of the RGB context to update
    name: The new name of the RGB context
    thumbnail: The ID of an uploaded media store to use as the thumbnail snapshot
    views: The RGB views (channel rendering settings) to replace the context's views with
    z: The z plane the context renders
    t: The timepoint the context renders
    c: The channel the context renders
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    RGBContext
"""
    return execute(UpdateRGBContextMutation, {'input': {'id': id, 'name': name, 'thumbnail': thumbnail, 'views': views, 'z': z, 't': t, 'c': c}}, rath=rath).update_rgb_context

async def acreate_roi(image: IDCoercible, vectors: Iterable[FiveDVector], kind: RoiKind, rath: Optional[MikroNextRath]=None) -> ROI:
    """CreateRoi 

Create a new region of interest

Args:
    image: The image this ROI belongs to
    vectors: The vector coordinates defining the ROI
    kind: The type/kind of ROI
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    ROI
"""
    return (await aexecute(CreateRoiMutation, {'input': {'image': image, 'vectors': vectors, 'kind': kind}}, rath=rath)).create_roi

def create_roi(image: IDCoercible, vectors: Iterable[FiveDVector], kind: RoiKind, rath: Optional[MikroNextRath]=None) -> ROI:
    """CreateRoi 

Create a new region of interest

Args:
    image: The image this ROI belongs to
    vectors: The vector coordinates defining the ROI
    kind: The type/kind of ROI
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    ROI
"""
    return execute(CreateRoiMutation, {'input': {'image': image, 'vectors': vectors, 'kind': kind}}, rath=rath).create_roi

async def adelete_roi(id: IDCoercible, rath: Optional[MikroNextRath]=None) -> ID:
    """DeleteRoi 

Delete an existing region of interest

Args:
    id: The ID of the ROI to delete
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    ID
"""
    return (await aexecute(DeleteRoiMutation, {'input': {'id': id}}, rath=rath)).delete_roi

def delete_roi(id: IDCoercible, rath: Optional[MikroNextRath]=None) -> ID:
    """DeleteRoi 

Delete an existing region of interest

Args:
    id: The ID of the ROI to delete
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    ID
"""
    return execute(DeleteRoiMutation, {'input': {'id': id}}, rath=rath).delete_roi

async def aupdate_roi(roi: IDCoercible, vectors: Optional[Iterable[FiveDVector]]=None, kind: Optional[RoiKind]=None, rath: Optional[MikroNextRath]=None) -> ROI:
    """UpdateRoi 

Update an existing region of interest

Args:
    roi: The ID of the ROI to update
    vectors: The new vector coordinates defining the ROI
    kind: The new type/kind of ROI
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    ROI
"""
    return (await aexecute(UpdateRoiMutation, {'input': {'roi': roi, 'vectors': vectors, 'kind': kind}}, rath=rath)).update_roi

def update_roi(roi: IDCoercible, vectors: Optional[Iterable[FiveDVector]]=None, kind: Optional[RoiKind]=None, rath: Optional[MikroNextRath]=None) -> ROI:
    """UpdateRoi 

Update an existing region of interest

Args:
    roi: The ID of the ROI to update
    vectors: The new vector coordinates defining the ROI
    kind: The new type/kind of ROI
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    ROI
"""
    return execute(UpdateRoiMutation, {'input': {'roi': roi, 'vectors': vectors, 'kind': kind}}, rath=rath).update_roi

async def acreate_scene(name: str, blending: Optional[Blending]=None, spatial_unit: Optional[SpatialUnit]=None, temporal_unit: Optional[TemporalUnit]=None, rath: Optional[MikroNextRath]=None) -> Scene:
    """CreateScene 

Create a new scene from an existing lens with optional blending mode

Args:
    name: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text. (required)
    blending: Blending
    spatial_unit: SpatialUnit
    temporal_unit: TemporalUnit
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    Scene
"""
    return (await aexecute(CreateSceneMutation, {'input': {'name': name, 'blending': blending, 'spatialUnit': spatial_unit, 'temporalUnit': temporal_unit}}, rath=rath)).create_scene

def create_scene(name: str, blending: Optional[Blending]=None, spatial_unit: Optional[SpatialUnit]=None, temporal_unit: Optional[TemporalUnit]=None, rath: Optional[MikroNextRath]=None) -> Scene:
    """CreateScene 

Create a new scene from an existing lens with optional blending mode

Args:
    name: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text. (required)
    blending: Blending
    spatial_unit: SpatialUnit
    temporal_unit: TemporalUnit
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    Scene
"""
    return execute(CreateSceneMutation, {'input': {'name': name, 'blending': blending, 'spatialUnit': spatial_unit, 'temporalUnit': temporal_unit}}, rath=rath).create_scene

async def acreate_snapshot(file: ImageFileCoercible, image: IDCoercible, name: Optional[str]=None, rath: Optional[MikroNextRath]=None) -> Snapshot:
    """CreateSnapshot 

Create a new state snapshot

Args:
    file: The uploaded media file store containing the rendered snapshot
    image: The ID of the image this snapshot belongs to
    name: The name of the snapshot
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    Snapshot
"""
    return (await aexecute(CreateSnapshotMutation, {'input': {'file': file, 'image': image, 'name': name}}, rath=rath)).create_snapshot

def create_snapshot(file: ImageFileCoercible, image: IDCoercible, name: Optional[str]=None, rath: Optional[MikroNextRath]=None) -> Snapshot:
    """CreateSnapshot 

Create a new state snapshot

Args:
    file: The uploaded media file store containing the rendered snapshot
    image: The ID of the image this snapshot belongs to
    name: The name of the snapshot
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    Snapshot
"""
    return execute(CreateSnapshotMutation, {'input': {'file': file, 'image': image, 'name': name}}, rath=rath).create_snapshot

async def acreate_stage(name: str, instrument: Optional[IDCoercible]=None, rath: Optional[MikroNextRath]=None) -> Stage:
    """CreateStage 

Create a new stage for organizing data

Args:
    name: The name of the stage
    instrument: The ID of the instrument this stage belongs to
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    Stage
"""
    return (await aexecute(CreateStageMutation, {'input': {'name': name, 'instrument': instrument}}, rath=rath)).create_stage

def create_stage(name: str, instrument: Optional[IDCoercible]=None, rath: Optional[MikroNextRath]=None) -> Stage:
    """CreateStage 

Create a new stage for organizing data

Args:
    name: The name of the stage
    instrument: The ID of the instrument this stage belongs to
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    Stage
"""
    return execute(CreateStageMutation, {'input': {'name': name, 'instrument': instrument}}, rath=rath).create_stage

async def afrom_parquet_like(dataframe: ParquetCoercible, name: str, origins: Optional[Iterable[IDCoercible]]=None, dataset: Optional[IDCoercible]=None, label_accessors: Optional[Iterable[PartialLabelAccessorInput]]=None, image_accessors: Optional[Iterable[PartialImageAccessorInput]]=None, rath: Optional[MikroNextRath]=None) -> Table:
    """from_parquet_like 

Create a table from parquet-like data

Args:
    dataframe: The parquet dataframe to create the table from
    name: The name of the table
    origins: The IDs of tables this table was derived from
    dataset: The dataset ID this table belongs to
    label_accessors: Label accessors to create for this table
    image_accessors: Image accessors to create for this table
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    Table
"""
    return (await aexecute(From_parquet_likeMutation, {'input': {'dataframe': dataframe, 'name': name, 'origins': origins, 'dataset': dataset, 'labelAccessors': label_accessors, 'imageAccessors': image_accessors}}, rath=rath)).from_parquet_like

def from_parquet_like(dataframe: ParquetCoercible, name: str, origins: Optional[Iterable[IDCoercible]]=None, dataset: Optional[IDCoercible]=None, label_accessors: Optional[Iterable[PartialLabelAccessorInput]]=None, image_accessors: Optional[Iterable[PartialImageAccessorInput]]=None, rath: Optional[MikroNextRath]=None) -> Table:
    """from_parquet_like 

Create a table from parquet-like data

Args:
    dataframe: The parquet dataframe to create the table from
    name: The name of the table
    origins: The IDs of tables this table was derived from
    dataset: The dataset ID this table belongs to
    label_accessors: Label accessors to create for this table
    image_accessors: Image accessors to create for this table
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    Table
"""
    return execute(From_parquet_likeMutation, {'input': {'dataframe': dataframe, 'name': name, 'origins': origins, 'dataset': dataset, 'labelAccessors': label_accessors, 'imageAccessors': image_accessors}}, rath=rath).from_parquet_like

async def acreate_rgb_view(context: IDCoercible, image: IDCoercible, collection: Optional[IDCoercible]=None, z_min: Optional[int]=None, z_max: Optional[int]=None, x_min: Optional[int]=None, x_max: Optional[int]=None, y_min: Optional[int]=None, y_max: Optional[int]=None, t_min: Optional[int]=None, t_max: Optional[int]=None, c_min: Optional[int]=None, c_max: Optional[int]=None, gamma: Optional[float]=None, contrast_limit_min: Optional[float]=None, contrast_limit_max: Optional[float]=None, rescale: Optional[bool]=None, scale: Optional[float]=None, active: Optional[bool]=None, color_map: Optional[ColorMap]=None, base_color: Optional[Iterable[float]]=None, rath: Optional[MikroNextRath]=None) -> CreateRgbViewMutationCreatergbview:
    """CreateRgbView 

Create a new view for RGB image data

Args:
    collection: The collection this view belongs to
    z_min: The minimum z coordinate of the view
    z_max: The maximum z coordinate of the view
    x_min: The minimum x coordinate of the view
    x_max: The maximum x coordinate of the view
    y_min: The minimum y coordinate of the view
    y_max: The maximum y coordinate of the view
    t_min: The minimum t coordinate of the view
    t_max: The maximum t coordinate of the view
    c_min: The minimum c (channel) coordinate of the view
    c_max: The maximum c (channel) coordinate of the view
    context: The ID of the RGB render context this view belongs to
    gamma: The gamma correction applied to the channel
    contrast_limit_min: The minimum contrast limit of the channel
    contrast_limit_max: The maximum contrast limit of the channel
    rescale: Whether to rescale the channel data to the contrast limits
    scale: The scale factor applied to the channel when rendering
    active: Whether the view is active
    color_map: The color map applied to the channel
    base_color: The base color of the channel as RGBA values (if using a mapped scaler)
    image: The ID of the image this view is for
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    CreateRgbViewMutationCreatergbview
"""
    return (await aexecute(CreateRgbViewMutation, {'input': {'collection': collection, 'zMin': z_min, 'zMax': z_max, 'xMin': x_min, 'xMax': x_max, 'yMin': y_min, 'yMax': y_max, 'tMin': t_min, 'tMax': t_max, 'cMin': c_min, 'cMax': c_max, 'context': context, 'gamma': gamma, 'contrastLimitMin': contrast_limit_min, 'contrastLimitMax': contrast_limit_max, 'rescale': rescale, 'scale': scale, 'active': active, 'colorMap': color_map, 'baseColor': base_color, 'image': image}}, rath=rath)).create_rgb_view

def create_rgb_view(context: IDCoercible, image: IDCoercible, collection: Optional[IDCoercible]=None, z_min: Optional[int]=None, z_max: Optional[int]=None, x_min: Optional[int]=None, x_max: Optional[int]=None, y_min: Optional[int]=None, y_max: Optional[int]=None, t_min: Optional[int]=None, t_max: Optional[int]=None, c_min: Optional[int]=None, c_max: Optional[int]=None, gamma: Optional[float]=None, contrast_limit_min: Optional[float]=None, contrast_limit_max: Optional[float]=None, rescale: Optional[bool]=None, scale: Optional[float]=None, active: Optional[bool]=None, color_map: Optional[ColorMap]=None, base_color: Optional[Iterable[float]]=None, rath: Optional[MikroNextRath]=None) -> CreateRgbViewMutationCreatergbview:
    """CreateRgbView 

Create a new view for RGB image data

Args:
    collection: The collection this view belongs to
    z_min: The minimum z coordinate of the view
    z_max: The maximum z coordinate of the view
    x_min: The minimum x coordinate of the view
    x_max: The maximum x coordinate of the view
    y_min: The minimum y coordinate of the view
    y_max: The maximum y coordinate of the view
    t_min: The minimum t coordinate of the view
    t_max: The maximum t coordinate of the view
    c_min: The minimum c (channel) coordinate of the view
    c_max: The maximum c (channel) coordinate of the view
    context: The ID of the RGB render context this view belongs to
    gamma: The gamma correction applied to the channel
    contrast_limit_min: The minimum contrast limit of the channel
    contrast_limit_max: The maximum contrast limit of the channel
    rescale: Whether to rescale the channel data to the contrast limits
    scale: The scale factor applied to the channel when rendering
    active: Whether the view is active
    color_map: The color map applied to the channel
    base_color: The base color of the channel as RGBA values (if using a mapped scaler)
    image: The ID of the image this view is for
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    CreateRgbViewMutationCreatergbview
"""
    return execute(CreateRgbViewMutation, {'input': {'collection': collection, 'zMin': z_min, 'zMax': z_max, 'xMin': x_min, 'xMax': x_max, 'yMin': y_min, 'yMax': y_max, 'tMin': t_min, 'tMax': t_max, 'cMin': c_min, 'cMax': c_max, 'context': context, 'gamma': gamma, 'contrastLimitMin': contrast_limit_min, 'contrastLimitMax': contrast_limit_max, 'rescale': rescale, 'scale': scale, 'active': active, 'colorMap': color_map, 'baseColor': base_color, 'image': image}}, rath=rath).create_rgb_view

async def aupdate_rgb_view(id: IDCoercible, collection: Optional[IDCoercible]=None, z_min: Optional[int]=None, z_max: Optional[int]=None, x_min: Optional[int]=None, x_max: Optional[int]=None, y_min: Optional[int]=None, y_max: Optional[int]=None, t_min: Optional[int]=None, t_max: Optional[int]=None, c_min: Optional[int]=None, c_max: Optional[int]=None, context: Optional[IDCoercible]=None, gamma: Optional[float]=None, contrast_limit_min: Optional[float]=None, contrast_limit_max: Optional[float]=None, rescale: Optional[bool]=None, scale: Optional[float]=None, active: Optional[bool]=None, color_map: Optional[ColorMap]=None, base_color: Optional[Iterable[float]]=None, rath: Optional[MikroNextRath]=None) -> UpdateRgbViewMutationUpdatergbview:
    """UpdateRgbView 

Update an existing RGB view

Args:
    collection: The collection this view belongs to
    z_min: The minimum z coordinate of the view
    z_max: The maximum z coordinate of the view
    x_min: The minimum x coordinate of the view
    x_max: The maximum x coordinate of the view
    y_min: The minimum y coordinate of the view
    y_max: The maximum y coordinate of the view
    t_min: The minimum t coordinate of the view
    t_max: The maximum t coordinate of the view
    c_min: The minimum c (channel) coordinate of the view
    c_max: The maximum c (channel) coordinate of the view
    context: The ID of the RGB render context this view belongs to
    gamma: The gamma correction applied to the channel
    contrast_limit_min: The minimum contrast limit of the channel
    contrast_limit_max: The maximum contrast limit of the channel
    rescale: Whether to rescale the channel data to the contrast limits
    scale: The scale factor applied to the channel when rendering
    active: Whether the view is active
    color_map: The color map applied to the channel
    base_color: The base color of the channel as RGBA values (if using a mapped scaler)
    id: The ID of the RGB view to update
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    UpdateRgbViewMutationUpdatergbview
"""
    return (await aexecute(UpdateRgbViewMutation, {'input': {'collection': collection, 'zMin': z_min, 'zMax': z_max, 'xMin': x_min, 'xMax': x_max, 'yMin': y_min, 'yMax': y_max, 'tMin': t_min, 'tMax': t_max, 'cMin': c_min, 'cMax': c_max, 'context': context, 'gamma': gamma, 'contrastLimitMin': contrast_limit_min, 'contrastLimitMax': contrast_limit_max, 'rescale': rescale, 'scale': scale, 'active': active, 'colorMap': color_map, 'baseColor': base_color, 'id': id}}, rath=rath)).update_rgb_view

def update_rgb_view(id: IDCoercible, collection: Optional[IDCoercible]=None, z_min: Optional[int]=None, z_max: Optional[int]=None, x_min: Optional[int]=None, x_max: Optional[int]=None, y_min: Optional[int]=None, y_max: Optional[int]=None, t_min: Optional[int]=None, t_max: Optional[int]=None, c_min: Optional[int]=None, c_max: Optional[int]=None, context: Optional[IDCoercible]=None, gamma: Optional[float]=None, contrast_limit_min: Optional[float]=None, contrast_limit_max: Optional[float]=None, rescale: Optional[bool]=None, scale: Optional[float]=None, active: Optional[bool]=None, color_map: Optional[ColorMap]=None, base_color: Optional[Iterable[float]]=None, rath: Optional[MikroNextRath]=None) -> UpdateRgbViewMutationUpdatergbview:
    """UpdateRgbView 

Update an existing RGB view

Args:
    collection: The collection this view belongs to
    z_min: The minimum z coordinate of the view
    z_max: The maximum z coordinate of the view
    x_min: The minimum x coordinate of the view
    x_max: The maximum x coordinate of the view
    y_min: The minimum y coordinate of the view
    y_max: The maximum y coordinate of the view
    t_min: The minimum t coordinate of the view
    t_max: The maximum t coordinate of the view
    c_min: The minimum c (channel) coordinate of the view
    c_max: The maximum c (channel) coordinate of the view
    context: The ID of the RGB render context this view belongs to
    gamma: The gamma correction applied to the channel
    contrast_limit_min: The minimum contrast limit of the channel
    contrast_limit_max: The maximum contrast limit of the channel
    rescale: Whether to rescale the channel data to the contrast limits
    scale: The scale factor applied to the channel when rendering
    active: Whether the view is active
    color_map: The color map applied to the channel
    base_color: The base color of the channel as RGBA values (if using a mapped scaler)
    id: The ID of the RGB view to update
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    UpdateRgbViewMutationUpdatergbview
"""
    return execute(UpdateRgbViewMutation, {'input': {'collection': collection, 'zMin': z_min, 'zMax': z_max, 'xMin': x_min, 'xMax': x_max, 'yMin': y_min, 'yMax': y_max, 'tMin': t_min, 'tMax': t_max, 'cMin': c_min, 'cMax': c_max, 'context': context, 'gamma': gamma, 'contrastLimitMin': contrast_limit_min, 'contrastLimitMax': contrast_limit_max, 'rescale': rescale, 'scale': scale, 'active': active, 'colorMap': color_map, 'baseColor': base_color, 'id': id}}, rath=rath).update_rgb_view

async def acreate_histogram_view(histogram: Iterable[float], bins: Iterable[float], min: float, max: float, image: IDCoercible, collection: Optional[IDCoercible]=None, z_min: Optional[int]=None, z_max: Optional[int]=None, x_min: Optional[int]=None, x_max: Optional[int]=None, y_min: Optional[int]=None, y_max: Optional[int]=None, t_min: Optional[int]=None, t_max: Optional[int]=None, c_min: Optional[int]=None, c_max: Optional[int]=None, rath: Optional[MikroNextRath]=None) -> HistogramView:
    """CreateHistogramView 

Create a new view for histogram data

Args:
    collection: The collection this view belongs to
    z_min: The minimum z coordinate of the view
    z_max: The maximum z coordinate of the view
    x_min: The minimum x coordinate of the view
    x_max: The maximum x coordinate of the view
    y_min: The minimum y coordinate of the view
    y_max: The maximum y coordinate of the view
    t_min: The minimum t coordinate of the view
    t_max: The maximum t coordinate of the view
    c_min: The minimum c (channel) coordinate of the view
    c_max: The maximum c (channel) coordinate of the view
    histogram: The histogram of the image (y values)
    bins: The bin indices of the histogram (x values)
    min: The minimum pixel value of the histogram
    max: The maximum pixel value of the histogram
    image: The ID of the image this view is for
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    HistogramView
"""
    return (await aexecute(CreateHistogramViewMutation, {'input': {'collection': collection, 'zMin': z_min, 'zMax': z_max, 'xMin': x_min, 'xMax': x_max, 'yMin': y_min, 'yMax': y_max, 'tMin': t_min, 'tMax': t_max, 'cMin': c_min, 'cMax': c_max, 'histogram': histogram, 'bins': bins, 'min': min, 'max': max, 'image': image}}, rath=rath)).create_histogram_view

def create_histogram_view(histogram: Iterable[float], bins: Iterable[float], min: float, max: float, image: IDCoercible, collection: Optional[IDCoercible]=None, z_min: Optional[int]=None, z_max: Optional[int]=None, x_min: Optional[int]=None, x_max: Optional[int]=None, y_min: Optional[int]=None, y_max: Optional[int]=None, t_min: Optional[int]=None, t_max: Optional[int]=None, c_min: Optional[int]=None, c_max: Optional[int]=None, rath: Optional[MikroNextRath]=None) -> HistogramView:
    """CreateHistogramView 

Create a new view for histogram data

Args:
    collection: The collection this view belongs to
    z_min: The minimum z coordinate of the view
    z_max: The maximum z coordinate of the view
    x_min: The minimum x coordinate of the view
    x_max: The maximum x coordinate of the view
    y_min: The minimum y coordinate of the view
    y_max: The maximum y coordinate of the view
    t_min: The minimum t coordinate of the view
    t_max: The maximum t coordinate of the view
    c_min: The minimum c (channel) coordinate of the view
    c_max: The maximum c (channel) coordinate of the view
    histogram: The histogram of the image (y values)
    bins: The bin indices of the histogram (x values)
    min: The minimum pixel value of the histogram
    max: The maximum pixel value of the histogram
    image: The ID of the image this view is for
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    HistogramView
"""
    return execute(CreateHistogramViewMutation, {'input': {'collection': collection, 'zMin': z_min, 'zMax': z_max, 'xMin': x_min, 'xMax': x_max, 'yMin': y_min, 'yMax': y_max, 'tMin': t_min, 'tMax': t_max, 'cMin': c_min, 'cMax': c_max, 'histogram': histogram, 'bins': bins, 'min': min, 'max': max, 'image': image}}, rath=rath).create_histogram_view

async def acreate_mask_view(image: IDCoercible, collection: Optional[IDCoercible]=None, z_min: Optional[int]=None, z_max: Optional[int]=None, x_min: Optional[int]=None, x_max: Optional[int]=None, y_min: Optional[int]=None, y_max: Optional[int]=None, t_min: Optional[int]=None, t_max: Optional[int]=None, c_min: Optional[int]=None, c_max: Optional[int]=None, reference_view: Optional[IDCoercible]=None, labels: Optional[LabelsLike]=None, rath: Optional[MikroNextRath]=None) -> MaskView:
    """CreateMaskView 

Create a new view for masked data

Args:
    collection: The collection this view belongs to
    z_min: The minimum z coordinate of the view
    z_max: The maximum z coordinate of the view
    x_min: The minimum x coordinate of the view
    x_max: The maximum x coordinate of the view
    y_min: The minimum y coordinate of the view
    y_max: The maximum y coordinate of the view
    t_min: The minimum t coordinate of the view
    t_max: The maximum t coordinate of the view
    c_min: The minimum c (channel) coordinate of the view
    c_max: The maximum c (channel) coordinate of the view
    reference_view: The ID of the view that is masked by this mask
    labels: The labels of the mask and their corresponding colors
    image: The ID of the image this view is for
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    MaskView
"""
    return (await aexecute(CreateMaskViewMutation, {'input': {'collection': collection, 'zMin': z_min, 'zMax': z_max, 'xMin': x_min, 'xMax': x_max, 'yMin': y_min, 'yMax': y_max, 'tMin': t_min, 'tMax': t_max, 'cMin': c_min, 'cMax': c_max, 'referenceView': reference_view, 'labels': labels, 'image': image}}, rath=rath)).create_mask_view

def create_mask_view(image: IDCoercible, collection: Optional[IDCoercible]=None, z_min: Optional[int]=None, z_max: Optional[int]=None, x_min: Optional[int]=None, x_max: Optional[int]=None, y_min: Optional[int]=None, y_max: Optional[int]=None, t_min: Optional[int]=None, t_max: Optional[int]=None, c_min: Optional[int]=None, c_max: Optional[int]=None, reference_view: Optional[IDCoercible]=None, labels: Optional[LabelsLike]=None, rath: Optional[MikroNextRath]=None) -> MaskView:
    """CreateMaskView 

Create a new view for masked data

Args:
    collection: The collection this view belongs to
    z_min: The minimum z coordinate of the view
    z_max: The maximum z coordinate of the view
    x_min: The minimum x coordinate of the view
    x_max: The maximum x coordinate of the view
    y_min: The minimum y coordinate of the view
    y_max: The maximum y coordinate of the view
    t_min: The minimum t coordinate of the view
    t_max: The maximum t coordinate of the view
    c_min: The minimum c (channel) coordinate of the view
    c_max: The maximum c (channel) coordinate of the view
    reference_view: The ID of the view that is masked by this mask
    labels: The labels of the mask and their corresponding colors
    image: The ID of the image this view is for
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    MaskView
"""
    return execute(CreateMaskViewMutation, {'input': {'collection': collection, 'zMin': z_min, 'zMax': z_max, 'xMin': x_min, 'xMax': x_max, 'yMin': y_min, 'yMax': y_max, 'tMin': t_min, 'tMax': t_max, 'cMin': c_min, 'cMax': c_max, 'referenceView': reference_view, 'labels': labels, 'image': image}}, rath=rath).create_mask_view

async def acreate_instance_mask_view(image: IDCoercible, collection: Optional[IDCoercible]=None, z_min: Optional[int]=None, z_max: Optional[int]=None, x_min: Optional[int]=None, x_max: Optional[int]=None, y_min: Optional[int]=None, y_max: Optional[int]=None, t_min: Optional[int]=None, t_max: Optional[int]=None, c_min: Optional[int]=None, c_max: Optional[int]=None, reference_view: Optional[IDCoercible]=None, labels: Optional[LabelsLike]=None, rath: Optional[MikroNextRath]=None) -> InstanceMaskView:
    """CreateInstanceMaskView 

Create a new view for instance mask data

Args:
    collection: The collection this view belongs to
    z_min: The minimum z coordinate of the view
    z_max: The maximum z coordinate of the view
    x_min: The minimum x coordinate of the view
    x_max: The maximum x coordinate of the view
    y_min: The minimum y coordinate of the view
    y_max: The maximum y coordinate of the view
    t_min: The minimum t coordinate of the view
    t_max: The maximum t coordinate of the view
    c_min: The minimum c (channel) coordinate of the view
    c_max: The maximum c (channel) coordinate of the view
    reference_view: The ID of the view that is masked by this instance mask
    labels: The instance labels of the mask and their corresponding colors
    image: The ID of the image this view is for
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    InstanceMaskView
"""
    return (await aexecute(CreateInstanceMaskViewMutation, {'input': {'collection': collection, 'zMin': z_min, 'zMax': z_max, 'xMin': x_min, 'xMax': x_max, 'yMin': y_min, 'yMax': y_max, 'tMin': t_min, 'tMax': t_max, 'cMin': c_min, 'cMax': c_max, 'referenceView': reference_view, 'labels': labels, 'image': image}}, rath=rath)).create_instance_mask_view

def create_instance_mask_view(image: IDCoercible, collection: Optional[IDCoercible]=None, z_min: Optional[int]=None, z_max: Optional[int]=None, x_min: Optional[int]=None, x_max: Optional[int]=None, y_min: Optional[int]=None, y_max: Optional[int]=None, t_min: Optional[int]=None, t_max: Optional[int]=None, c_min: Optional[int]=None, c_max: Optional[int]=None, reference_view: Optional[IDCoercible]=None, labels: Optional[LabelsLike]=None, rath: Optional[MikroNextRath]=None) -> InstanceMaskView:
    """CreateInstanceMaskView 

Create a new view for instance mask data

Args:
    collection: The collection this view belongs to
    z_min: The minimum z coordinate of the view
    z_max: The maximum z coordinate of the view
    x_min: The minimum x coordinate of the view
    x_max: The maximum x coordinate of the view
    y_min: The minimum y coordinate of the view
    y_max: The maximum y coordinate of the view
    t_min: The minimum t coordinate of the view
    t_max: The maximum t coordinate of the view
    c_min: The minimum c (channel) coordinate of the view
    c_max: The maximum c (channel) coordinate of the view
    reference_view: The ID of the view that is masked by this instance mask
    labels: The instance labels of the mask and their corresponding colors
    image: The ID of the image this view is for
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    InstanceMaskView
"""
    return execute(CreateInstanceMaskViewMutation, {'input': {'collection': collection, 'zMin': z_min, 'zMax': z_max, 'xMin': x_min, 'xMax': x_max, 'yMin': y_min, 'yMax': y_max, 'tMin': t_min, 'tMax': t_max, 'cMin': c_min, 'cMax': c_max, 'referenceView': reference_view, 'labels': labels, 'image': image}}, rath=rath).create_instance_mask_view

async def acreate_reference_view(image: IDCoercible, collection: Optional[IDCoercible]=None, z_min: Optional[int]=None, z_max: Optional[int]=None, x_min: Optional[int]=None, x_max: Optional[int]=None, y_min: Optional[int]=None, y_max: Optional[int]=None, t_min: Optional[int]=None, t_max: Optional[int]=None, c_min: Optional[int]=None, c_max: Optional[int]=None, rath: Optional[MikroNextRath]=None) -> ReferenceView:
    """CreateReferenceView 

Create a new reference view for image data

Args:
    collection: The collection this view belongs to
    z_min: The minimum z coordinate of the view
    z_max: The maximum z coordinate of the view
    x_min: The minimum x coordinate of the view
    x_max: The maximum x coordinate of the view
    y_min: The minimum y coordinate of the view
    y_max: The maximum y coordinate of the view
    t_min: The minimum t coordinate of the view
    t_max: The maximum t coordinate of the view
    c_min: The minimum c (channel) coordinate of the view
    c_max: The maximum c (channel) coordinate of the view
    image: The ID of the image this view is for
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    ReferenceView
"""
    return (await aexecute(CreateReferenceViewMutation, {'input': {'collection': collection, 'zMin': z_min, 'zMax': z_max, 'xMin': x_min, 'xMax': x_max, 'yMin': y_min, 'yMax': y_max, 'tMin': t_min, 'tMax': t_max, 'cMin': c_min, 'cMax': c_max, 'image': image}}, rath=rath)).create_reference_view

def create_reference_view(image: IDCoercible, collection: Optional[IDCoercible]=None, z_min: Optional[int]=None, z_max: Optional[int]=None, x_min: Optional[int]=None, x_max: Optional[int]=None, y_min: Optional[int]=None, y_max: Optional[int]=None, t_min: Optional[int]=None, t_max: Optional[int]=None, c_min: Optional[int]=None, c_max: Optional[int]=None, rath: Optional[MikroNextRath]=None) -> ReferenceView:
    """CreateReferenceView 

Create a new reference view for image data

Args:
    collection: The collection this view belongs to
    z_min: The minimum z coordinate of the view
    z_max: The maximum z coordinate of the view
    x_min: The minimum x coordinate of the view
    x_max: The maximum x coordinate of the view
    y_min: The minimum y coordinate of the view
    y_max: The maximum y coordinate of the view
    t_min: The minimum t coordinate of the view
    t_max: The maximum t coordinate of the view
    c_min: The minimum c (channel) coordinate of the view
    c_max: The maximum c (channel) coordinate of the view
    image: The ID of the image this view is for
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    ReferenceView
"""
    return execute(CreateReferenceViewMutation, {'input': {'collection': collection, 'zMin': z_min, 'zMax': z_max, 'xMin': x_min, 'xMax': x_max, 'yMin': y_min, 'yMax': y_max, 'tMin': t_min, 'tMax': t_max, 'cMin': c_min, 'cMax': c_max, 'image': image}}, rath=rath).create_reference_view

async def acreate_view_collection(name: str, rath: Optional[MikroNextRath]=None) -> CreateViewCollectionMutationCreateviewcollection:
    """CreateViewCollection 

Create a new collection of views to organize related views

Args:
    name: The name of the view collection
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    CreateViewCollectionMutationCreateviewcollection
"""
    return (await aexecute(CreateViewCollectionMutation, {'input': {'name': name}}, rath=rath)).create_view_collection

def create_view_collection(name: str, rath: Optional[MikroNextRath]=None) -> CreateViewCollectionMutationCreateviewcollection:
    """CreateViewCollection 

Create a new collection of views to organize related views

Args:
    name: The name of the view collection
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    CreateViewCollectionMutationCreateviewcollection
"""
    return execute(CreateViewCollectionMutation, {'input': {'name': name}}, rath=rath).create_view_collection

async def aget_camera(id: ID, rath: Optional[MikroNextRath]=None) -> Camera:
    """GetCamera 

Get a single camera by ID

Args:
    id (ID): The unique identifier of an object
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    Camera
"""
    return (await aexecute(GetCameraQuery, {'id': id}, rath=rath)).camera

def get_camera(id: ID, rath: Optional[MikroNextRath]=None) -> Camera:
    """GetCamera 

Get a single camera by ID

Args:
    id (ID): The unique identifier of an object
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    Camera
"""
    return execute(GetCameraQuery, {'id': id}, rath=rath).camera

async def aget_dataset(id: ID, rath: Optional[MikroNextRath]=None) -> Dataset:
    """GetDataset 

Get a single dataset by ID

Args:
    id (ID): The unique identifier of an object
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    Dataset
"""
    return (await aexecute(GetDatasetQuery, {'id': id}, rath=rath)).dataset

def get_dataset(id: ID, rath: Optional[MikroNextRath]=None) -> Dataset:
    """GetDataset 

Get a single dataset by ID

Args:
    id (ID): The unique identifier of an object
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    Dataset
"""
    return execute(GetDatasetQuery, {'id': id}, rath=rath).dataset

async def asearch_datasets(search: Optional[str]=None, values: Optional[List[ID]]=None, limit: Optional[int]=None, offset: Optional[int]=0, rath: Optional[MikroNextRath]=None) -> Tuple[SearchDatasetsQueryOptions, ...]:
    """SearchDatasets 

List datasets (folder-like collections of images, files and tables)

Args:
    search (Optional[str], optional): No description. 
    values (Optional[List[ID]], optional): No description. 
    limit (Optional[int], optional): No description. 
    offset (Optional[int], optional): No description. Defaults to 0
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    List[SearchDatasetsQueryDatasets]
"""
    return (await aexecute(SearchDatasetsQuery, {'search': search, 'values': values, 'limit': limit, 'offset': offset}, rath=rath)).options

def search_datasets(search: Optional[str]=None, values: Optional[List[ID]]=None, limit: Optional[int]=None, offset: Optional[int]=0, rath: Optional[MikroNextRath]=None) -> Tuple[SearchDatasetsQueryOptions, ...]:
    """SearchDatasets 

List datasets (folder-like collections of images, files and tables)

Args:
    search (Optional[str], optional): No description. 
    values (Optional[List[ID]], optional): No description. 
    limit (Optional[int], optional): No description. 
    offset (Optional[int], optional): No description. Defaults to 0
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    List[SearchDatasetsQueryDatasets]
"""
    return execute(SearchDatasetsQuery, {'search': search, 'values': values, 'limit': limit, 'offset': offset}, rath=rath).options

async def aget_file(id: ID, rath: Optional[MikroNextRath]=None) -> File:
    """GetFile 

Get a single file by ID

Args:
    id (ID): The unique identifier of an object
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    File
"""
    return (await aexecute(GetFileQuery, {'id': id}, rath=rath)).file

def get_file(id: ID, rath: Optional[MikroNextRath]=None) -> File:
    """GetFile 

Get a single file by ID

Args:
    id (ID): The unique identifier of an object
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    File
"""
    return execute(GetFileQuery, {'id': id}, rath=rath).file

async def asearch_files(search: Optional[str]=None, values: Optional[List[ID]]=None, limit: Optional[int]=None, offset: Optional[int]=0, rath: Optional[MikroNextRath]=None) -> Tuple[SearchFilesQueryOptions, ...]:
    """SearchFiles 

List files (raw microscopy files such as .czi or .ome.tiff)

Args:
    search (Optional[str], optional): No description. 
    values (Optional[List[ID]], optional): No description. 
    limit (Optional[int], optional): No description. 
    offset (Optional[int], optional): No description. Defaults to 0
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    List[SearchFilesQueryFiles]
"""
    return (await aexecute(SearchFilesQuery, {'search': search, 'values': values, 'limit': limit, 'offset': offset}, rath=rath)).options

def search_files(search: Optional[str]=None, values: Optional[List[ID]]=None, limit: Optional[int]=None, offset: Optional[int]=0, rath: Optional[MikroNextRath]=None) -> Tuple[SearchFilesQueryOptions, ...]:
    """SearchFiles 

List files (raw microscopy files such as .czi or .ome.tiff)

Args:
    search (Optional[str], optional): No description. 
    values (Optional[List[ID]], optional): No description. 
    limit (Optional[int], optional): No description. 
    offset (Optional[int], optional): No description. Defaults to 0
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    List[SearchFilesQueryFiles]
"""
    return execute(SearchFilesQuery, {'search': search, 'values': values, 'limit': limit, 'offset': offset}, rath=rath).options

async def aget_image(id: ID, rath: Optional[MikroNextRath]=None) -> Image:
    """GetImage 

Returns a single image by ID

Args:
    id (ID): The unique identifier of an object
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    Image
"""
    return (await aexecute(GetImageQuery, {'id': id}, rath=rath)).image

def get_image(id: ID, rath: Optional[MikroNextRath]=None) -> Image:
    """GetImage 

Returns a single image by ID

Args:
    id (ID): The unique identifier of an object
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    Image
"""
    return execute(GetImageQuery, {'id': id}, rath=rath).image

async def aget_random_image(rath: Optional[MikroNextRath]=None) -> Image:
    """GetRandomImage 

Get a random image of the current organization

Args:
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    Image
"""
    return (await aexecute(GetRandomImageQuery, {}, rath=rath)).random_image

def get_random_image(rath: Optional[MikroNextRath]=None) -> Image:
    """GetRandomImage 

Get a random image of the current organization

Args:
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    Image
"""
    return execute(GetRandomImageQuery, {}, rath=rath).random_image

async def asearch_images(search: Optional[str]=None, values: Optional[List[ID]]=None, limit: Optional[int]=None, offset: Optional[int]=0, rath: Optional[MikroNextRath]=None) -> Tuple[SearchImagesQueryOptions, ...]:
    """SearchImages 

List images in the current organization, filterable and orderable

Args:
    search (Optional[str], optional): No description. 
    values (Optional[List[ID]], optional): No description. 
    limit (Optional[int], optional): No description. 
    offset (Optional[int], optional): No description. Defaults to 0
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    List[SearchImagesQueryImages]
"""
    return (await aexecute(SearchImagesQuery, {'search': search, 'values': values, 'limit': limit, 'offset': offset}, rath=rath)).options

def search_images(search: Optional[str]=None, values: Optional[List[ID]]=None, limit: Optional[int]=None, offset: Optional[int]=0, rath: Optional[MikroNextRath]=None) -> Tuple[SearchImagesQueryOptions, ...]:
    """SearchImages 

List images in the current organization, filterable and orderable

Args:
    search (Optional[str], optional): No description. 
    values (Optional[List[ID]], optional): No description. 
    limit (Optional[int], optional): No description. 
    offset (Optional[int], optional): No description. Defaults to 0
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    List[SearchImagesQueryImages]
"""
    return execute(SearchImagesQuery, {'search': search, 'values': values, 'limit': limit, 'offset': offset}, rath=rath).options

async def aimages(filter: Optional[ImageFilter]=None, pagination: Optional[OffsetPaginationInput]=None, rath: Optional[MikroNextRath]=None) -> Tuple[Image, ...]:
    """Images 

List images in the current organization, filterable and orderable

Args:
    filter (Optional[ImageFilter], optional): No description. 
    pagination (Optional[OffsetPaginationInput], optional): No description. 
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    List[Image]
"""
    return (await aexecute(ImagesQuery, {'filter': filter, 'pagination': pagination}, rath=rath)).images

def images(filter: Optional[ImageFilter]=None, pagination: Optional[OffsetPaginationInput]=None, rath: Optional[MikroNextRath]=None) -> Tuple[Image, ...]:
    """Images 

List images in the current organization, filterable and orderable

Args:
    filter (Optional[ImageFilter], optional): No description. 
    pagination (Optional[OffsetPaginationInput], optional): No description. 
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    List[Image]
"""
    return execute(ImagesQuery, {'filter': filter, 'pagination': pagination}, rath=rath).images

async def aview_image(id: ID, filtersggg: Optional[ViewFilter]=None, rath: Optional[MikroNextRath]=None) -> ViewImageQueryImage:
    """ViewImage 

Returns a single image by ID

Args:
    id (ID): The unique identifier of an object
    filtersggg (Optional[ViewFilter], optional): No description. 
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    ViewImageQueryImage
"""
    return (await aexecute(ViewImageQuery, {'id': id, 'filtersggg': filtersggg}, rath=rath)).image

def view_image(id: ID, filtersggg: Optional[ViewFilter]=None, rath: Optional[MikroNextRath]=None) -> ViewImageQueryImage:
    """ViewImage 

Returns a single image by ID

Args:
    id (ID): The unique identifier of an object
    filtersggg (Optional[ViewFilter], optional): No description. 
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    ViewImageQueryImage
"""
    return execute(ViewImageQuery, {'id': id, 'filtersggg': filtersggg}, rath=rath).image

async def aartemiy_images(rath: Optional[MikroNextRath]=None) -> Tuple[ArtemiyImagesQueryImages, ...]:
    """ArtemiyImages 

List images in the current organization, filterable and orderable

Args:
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    List[ArtemiyImagesQueryImages]
"""
    return (await aexecute(ArtemiyImagesQuery, {}, rath=rath)).images

def artemiy_images(rath: Optional[MikroNextRath]=None) -> Tuple[ArtemiyImagesQueryImages, ...]:
    """ArtemiyImages 

List images in the current organization, filterable and orderable

Args:
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    List[ArtemiyImagesQueryImages]
"""
    return execute(ArtemiyImagesQuery, {}, rath=rath).images

async def aget_instrument(id: ID, rath: Optional[MikroNextRath]=None) -> Instrument:
    """GetInstrument 

Get a single instrument by ID

Args:
    id (ID): The unique identifier of an object
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    Instrument
"""
    return (await aexecute(GetInstrumentQuery, {'id': id}, rath=rath)).instrument

def get_instrument(id: ID, rath: Optional[MikroNextRath]=None) -> Instrument:
    """GetInstrument 

Get a single instrument by ID

Args:
    id (ID): The unique identifier of an object
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    Instrument
"""
    return execute(GetInstrumentQuery, {'id': id}, rath=rath).instrument

async def aget_lens(id: ID, rath: Optional[MikroNextRath]=None) -> Lens:
    """GetLens 

Get a single lens by ID

Args:
    id (ID): No description
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    Lens
"""
    return (await aexecute(GetLensQuery, {'id': id}, rath=rath)).lens

def get_lens(id: ID, rath: Optional[MikroNextRath]=None) -> Lens:
    """GetLens 

Get a single lens by ID

Args:
    id (ID): No description
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    Lens
"""
    return execute(GetLensQuery, {'id': id}, rath=rath).lens

async def aget_mesh(id: ID, rath: Optional[MikroNextRath]=None) -> Mesh:
    """GetMesh 

Get a single 3D mesh by ID

Args:
    id (ID): The unique identifier of an object
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    Mesh
"""
    return (await aexecute(GetMeshQuery, {'id': id}, rath=rath)).mesh

def get_mesh(id: ID, rath: Optional[MikroNextRath]=None) -> Mesh:
    """GetMesh 

Get a single 3D mesh by ID

Args:
    id (ID): The unique identifier of an object
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    Mesh
"""
    return execute(GetMeshQuery, {'id': id}, rath=rath).mesh

async def asearch_meshes(search: Optional[str]=None, values: Optional[List[ID]]=None, limit: Optional[int]=None, offset: Optional[int]=0, rath: Optional[MikroNextRath]=None) -> Tuple[SearchMeshesQueryOptions, ...]:
    """SearchMeshes 

List 3D meshes

Args:
    search (Optional[str], optional): No description. 
    values (Optional[List[ID]], optional): No description. 
    limit (Optional[int], optional): No description. 
    offset (Optional[int], optional): No description. Defaults to 0
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    List[SearchMeshesQueryMeshes]
"""
    return (await aexecute(SearchMeshesQuery, {'search': search, 'values': values, 'limit': limit, 'offset': offset}, rath=rath)).options

def search_meshes(search: Optional[str]=None, values: Optional[List[ID]]=None, limit: Optional[int]=None, offset: Optional[int]=0, rath: Optional[MikroNextRath]=None) -> Tuple[SearchMeshesQueryOptions, ...]:
    """SearchMeshes 

List 3D meshes

Args:
    search (Optional[str], optional): No description. 
    values (Optional[List[ID]], optional): No description. 
    limit (Optional[int], optional): No description. 
    offset (Optional[int], optional): No description. Defaults to 0
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    List[SearchMeshesQueryMeshes]
"""
    return execute(SearchMeshesQuery, {'search': search, 'values': values, 'limit': limit, 'offset': offset}, rath=rath).options

async def aget_objective(id: ID, rath: Optional[MikroNextRath]=None) -> Objective:
    """GetObjective 

Get a single objective by ID

Args:
    id (ID): The unique identifier of an object
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    Objective
"""
    return (await aexecute(GetObjectiveQuery, {'id': id}, rath=rath)).objective

def get_objective(id: ID, rath: Optional[MikroNextRath]=None) -> Objective:
    """GetObjective 

Get a single objective by ID

Args:
    id (ID): The unique identifier of an object
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    Objective
"""
    return execute(GetObjectiveQuery, {'id': id}, rath=rath).objective

async def aget_rgb_context(id: ID, rath: Optional[MikroNextRath]=None) -> RGBContext:
    """GetRGBContext 

Get a single RGB render context by ID

Args:
    id (ID): The unique identifier of an object
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    RGBContext
"""
    return (await aexecute(GetRGBContextQuery, {'id': id}, rath=rath)).rgbcontext

def get_rgb_context(id: ID, rath: Optional[MikroNextRath]=None) -> RGBContext:
    """GetRGBContext 

Get a single RGB render context by ID

Args:
    id (ID): The unique identifier of an object
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    RGBContext
"""
    return execute(GetRGBContextQuery, {'id': id}, rath=rath).rgbcontext

async def aget_rois(image: ID, rath: Optional[MikroNextRath]=None) -> Tuple[ROI, ...]:
    """GetRois 

List regions of interest drawn on images

Args:
    image (ID): No description
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    List[ROI]
"""
    return (await aexecute(GetRoisQuery, {'image': image}, rath=rath)).rois

def get_rois(image: ID, rath: Optional[MikroNextRath]=None) -> Tuple[ROI, ...]:
    """GetRois 

List regions of interest drawn on images

Args:
    image (ID): No description
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    List[ROI]
"""
    return execute(GetRoisQuery, {'image': image}, rath=rath).rois

async def aget_roi(id: ID, rath: Optional[MikroNextRath]=None) -> ROI:
    """GetRoi 

Get a single region of interest by ID

Args:
    id (ID): The unique identifier of an object
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    ROI
"""
    return (await aexecute(GetRoiQuery, {'id': id}, rath=rath)).roi

def get_roi(id: ID, rath: Optional[MikroNextRath]=None) -> ROI:
    """GetRoi 

Get a single region of interest by ID

Args:
    id (ID): The unique identifier of an object
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    ROI
"""
    return execute(GetRoiQuery, {'id': id}, rath=rath).roi

async def asearch_rois(search: Optional[str]=None, values: Optional[List[ID]]=None, limit: Optional[int]=None, offset: Optional[int]=0, rath: Optional[MikroNextRath]=None) -> Tuple[SearchRoisQueryOptions, ...]:
    """SearchRois 

List regions of interest drawn on images

Args:
    search (Optional[str], optional): No description. 
    values (Optional[List[ID]], optional): No description. 
    limit (Optional[int], optional): No description. 
    offset (Optional[int], optional): No description. Defaults to 0
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    List[SearchRoisQueryRois]
"""
    return (await aexecute(SearchRoisQuery, {'search': search, 'values': values, 'limit': limit, 'offset': offset}, rath=rath)).options

def search_rois(search: Optional[str]=None, values: Optional[List[ID]]=None, limit: Optional[int]=None, offset: Optional[int]=0, rath: Optional[MikroNextRath]=None) -> Tuple[SearchRoisQueryOptions, ...]:
    """SearchRois 

List regions of interest drawn on images

Args:
    search (Optional[str], optional): No description. 
    values (Optional[List[ID]], optional): No description. 
    limit (Optional[int], optional): No description. 
    offset (Optional[int], optional): No description. Defaults to 0
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    List[SearchRoisQueryRois]
"""
    return execute(SearchRoisQuery, {'search': search, 'values': values, 'limit': limit, 'offset': offset}, rath=rath).options

async def aget_scene(id: ID, rath: Optional[MikroNextRath]=None) -> Scene:
    """GetScene 

Get a single scene by ID

Args:
    id (ID): No description
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    Scene
"""
    return (await aexecute(GetSceneQuery, {'id': id}, rath=rath)).scene

def get_scene(id: ID, rath: Optional[MikroNextRath]=None) -> Scene:
    """GetScene 

Get a single scene by ID

Args:
    id (ID): No description
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    Scene
"""
    return execute(GetSceneQuery, {'id': id}, rath=rath).scene

async def asearch_scenes(search: Optional[str]=None, values: Optional[List[ID]]=None, limit: Optional[int]=None, offset: Optional[int]=0, rath: Optional[MikroNextRath]=None) -> Tuple[SearchScenesQueryOptions, ...]:
    """SearchScenes 

List scenes (compositions of layers over array datasets)

Args:
    search (Optional[str], optional): No description. 
    values (Optional[List[ID]], optional): No description. 
    limit (Optional[int], optional): No description. 
    offset (Optional[int], optional): No description. Defaults to 0
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    List[SearchScenesQueryScenes]
"""
    return (await aexecute(SearchScenesQuery, {'search': search, 'values': values, 'limit': limit, 'offset': offset}, rath=rath)).options

def search_scenes(search: Optional[str]=None, values: Optional[List[ID]]=None, limit: Optional[int]=None, offset: Optional[int]=0, rath: Optional[MikroNextRath]=None) -> Tuple[SearchScenesQueryOptions, ...]:
    """SearchScenes 

List scenes (compositions of layers over array datasets)

Args:
    search (Optional[str], optional): No description. 
    values (Optional[List[ID]], optional): No description. 
    limit (Optional[int], optional): No description. 
    offset (Optional[int], optional): No description. Defaults to 0
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    List[SearchScenesQueryScenes]
"""
    return execute(SearchScenesQuery, {'search': search, 'values': values, 'limit': limit, 'offset': offset}, rath=rath).options

async def aget_snapshot(id: ID, rath: Optional[MikroNextRath]=None) -> Snapshot:
    """GetSnapshot 

Get a single snapshot by ID

Args:
    id (ID): The unique identifier of an object
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    Snapshot
"""
    return (await aexecute(GetSnapshotQuery, {'id': id}, rath=rath)).snapshot

def get_snapshot(id: ID, rath: Optional[MikroNextRath]=None) -> Snapshot:
    """GetSnapshot 

Get a single snapshot by ID

Args:
    id (ID): The unique identifier of an object
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    Snapshot
"""
    return execute(GetSnapshotQuery, {'id': id}, rath=rath).snapshot

async def asearch_snapshots(search: Optional[str]=None, values: Optional[List[ID]]=None, limit: Optional[int]=None, offset: Optional[int]=0, rath: Optional[MikroNextRath]=None) -> Tuple[SearchSnapshotsQueryOptions, ...]:
    """SearchSnapshots 

List snapshots (pre-rendered thumbnail images of images)

Args:
    search (Optional[str], optional): No description. 
    values (Optional[List[ID]], optional): No description. 
    limit (Optional[int], optional): No description. 
    offset (Optional[int], optional): No description. Defaults to 0
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    List[SearchSnapshotsQuerySnapshots]
"""
    return (await aexecute(SearchSnapshotsQuery, {'search': search, 'values': values, 'limit': limit, 'offset': offset}, rath=rath)).options

def search_snapshots(search: Optional[str]=None, values: Optional[List[ID]]=None, limit: Optional[int]=None, offset: Optional[int]=0, rath: Optional[MikroNextRath]=None) -> Tuple[SearchSnapshotsQueryOptions, ...]:
    """SearchSnapshots 

List snapshots (pre-rendered thumbnail images of images)

Args:
    search (Optional[str], optional): No description. 
    values (Optional[List[ID]], optional): No description. 
    limit (Optional[int], optional): No description. 
    offset (Optional[int], optional): No description. Defaults to 0
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    List[SearchSnapshotsQuerySnapshots]
"""
    return execute(SearchSnapshotsQuery, {'search': search, 'values': values, 'limit': limit, 'offset': offset}, rath=rath).options

async def aget_stage(id: ID, rath: Optional[MikroNextRath]=None) -> Stage:
    """GetStage 

Get a single stage by ID

Args:
    id (ID): The unique identifier of an object
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    Stage
"""
    return (await aexecute(GetStageQuery, {'id': id}, rath=rath)).stage

def get_stage(id: ID, rath: Optional[MikroNextRath]=None) -> Stage:
    """GetStage 

Get a single stage by ID

Args:
    id (ID): The unique identifier of an object
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    Stage
"""
    return execute(GetStageQuery, {'id': id}, rath=rath).stage

async def asearch_stages(search: Optional[str]=None, values: Optional[List[ID]]=None, limit: Optional[int]=None, offset: Optional[int]=0, rath: Optional[MikroNextRath]=None) -> Tuple[SearchStagesQueryOptions, ...]:
    """SearchStages 

List stages (the 3D physical spaces images are positioned in)

Args:
    search (Optional[str], optional): No description. 
    values (Optional[List[ID]], optional): No description. 
    limit (Optional[int], optional): No description. 
    offset (Optional[int], optional): No description. Defaults to 0
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    List[SearchStagesQueryStages]
"""
    return (await aexecute(SearchStagesQuery, {'search': search, 'values': values, 'limit': limit, 'offset': offset}, rath=rath)).options

def search_stages(search: Optional[str]=None, values: Optional[List[ID]]=None, limit: Optional[int]=None, offset: Optional[int]=0, rath: Optional[MikroNextRath]=None) -> Tuple[SearchStagesQueryOptions, ...]:
    """SearchStages 

List stages (the 3D physical spaces images are positioned in)

Args:
    search (Optional[str], optional): No description. 
    values (Optional[List[ID]], optional): No description. 
    limit (Optional[int], optional): No description. 
    offset (Optional[int], optional): No description. Defaults to 0
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    List[SearchStagesQueryStages]
"""
    return execute(SearchStagesQuery, {'search': search, 'values': values, 'limit': limit, 'offset': offset}, rath=rath).options

async def aget_table(id: ID, rath: Optional[MikroNextRath]=None) -> Table:
    """GetTable 

Get a single table by ID

Args:
    id (ID): The unique identifier of an object
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    Table
"""
    return (await aexecute(GetTableQuery, {'id': id}, rath=rath)).table

def get_table(id: ID, rath: Optional[MikroNextRath]=None) -> Table:
    """GetTable 

Get a single table by ID

Args:
    id (ID): The unique identifier of an object
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    Table
"""
    return execute(GetTableQuery, {'id': id}, rath=rath).table

async def asearch_tables(search: Optional[str]=None, values: Optional[List[ID]]=None, limit: Optional[int]=None, offset: Optional[int]=0, rath: Optional[MikroNextRath]=None) -> Tuple[SearchTablesQueryOptions, ...]:
    """SearchTables 

List tables (tabular data backed by parquet stores)

Args:
    search (Optional[str], optional): No description. 
    values (Optional[List[ID]], optional): No description. 
    limit (Optional[int], optional): No description. 
    offset (Optional[int], optional): No description. Defaults to 0
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    List[SearchTablesQueryTables]
"""
    return (await aexecute(SearchTablesQuery, {'search': search, 'values': values, 'limit': limit, 'offset': offset}, rath=rath)).options

def search_tables(search: Optional[str]=None, values: Optional[List[ID]]=None, limit: Optional[int]=None, offset: Optional[int]=0, rath: Optional[MikroNextRath]=None) -> Tuple[SearchTablesQueryOptions, ...]:
    """SearchTables 

List tables (tabular data backed by parquet stores)

Args:
    search (Optional[str], optional): No description. 
    values (Optional[List[ID]], optional): No description. 
    limit (Optional[int], optional): No description. 
    offset (Optional[int], optional): No description. Defaults to 0
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    List[SearchTablesQueryTables]
"""
    return execute(SearchTablesQuery, {'search': search, 'values': values, 'limit': limit, 'offset': offset}, rath=rath).options

async def aget_table_cell(id: ID, rath: Optional[MikroNextRath]=None) -> TableCell:
    """GetTableCell 

Get a single table cell by its compound ID (tableId-rowId-columnId)

Args:
    id (ID): The unique identifier of an object
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    TableCell
"""
    return (await aexecute(GetTableCellQuery, {'id': id}, rath=rath)).table_cell

def get_table_cell(id: ID, rath: Optional[MikroNextRath]=None) -> TableCell:
    """GetTableCell 

Get a single table cell by its compound ID (tableId-rowId-columnId)

Args:
    id (ID): The unique identifier of an object
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    TableCell
"""
    return execute(GetTableCellQuery, {'id': id}, rath=rath).table_cell

async def asearch_table_cells(table: ID, search: Optional[str]=None, values: Optional[List[ID]]=None, limit: Optional[int]=None, offset: Optional[int]=0, rath: Optional[MikroNextRath]=None) -> Tuple[SearchTableCellsQueryOptions, ...]:
    """SearchTableCells 

List the cells of a table, row-major over the table's parquet data

Args:
    table (ID): The unique identifier of an object
    search (Optional[str], optional): No description. 
    values (Optional[List[ID]], optional): No description. 
    limit (Optional[int], optional): No description. 
    offset (Optional[int], optional): No description. Defaults to 0
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    List[SearchTableCellsQueryTablecells]
"""
    return (await aexecute(SearchTableCellsQuery, {'search': search, 'values': values, 'table': table, 'limit': limit, 'offset': offset}, rath=rath)).options

def search_table_cells(table: ID, search: Optional[str]=None, values: Optional[List[ID]]=None, limit: Optional[int]=None, offset: Optional[int]=0, rath: Optional[MikroNextRath]=None) -> Tuple[SearchTableCellsQueryOptions, ...]:
    """SearchTableCells 

List the cells of a table, row-major over the table's parquet data

Args:
    table (ID): The unique identifier of an object
    search (Optional[str], optional): No description. 
    values (Optional[List[ID]], optional): No description. 
    limit (Optional[int], optional): No description. 
    offset (Optional[int], optional): No description. Defaults to 0
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    List[SearchTableCellsQueryTablecells]
"""
    return execute(SearchTableCellsQuery, {'search': search, 'values': values, 'table': table, 'limit': limit, 'offset': offset}, rath=rath).options

async def aget_table_row(id: ID, rath: Optional[MikroNextRath]=None) -> TableRow:
    """GetTableRow 

Get a single table row by its compound ID (tableId-rowId)

Args:
    id (ID): The unique identifier of an object
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    TableRow
"""
    return (await aexecute(GetTableRowQuery, {'id': id}, rath=rath)).table_row

def get_table_row(id: ID, rath: Optional[MikroNextRath]=None) -> TableRow:
    """GetTableRow 

Get a single table row by its compound ID (tableId-rowId)

Args:
    id (ID): The unique identifier of an object
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    TableRow
"""
    return execute(GetTableRowQuery, {'id': id}, rath=rath).table_row

async def asearch_table_rows(table: ID, search: Optional[str]=None, values: Optional[List[ID]]=None, limit: Optional[int]=None, offset: Optional[int]=0, rath: Optional[MikroNextRath]=None) -> Tuple[SearchTableRowsQueryOptions, ...]:
    """SearchTableRows 

List the rows of a table, paginated over the table's parquet data

Args:
    table (ID): The unique identifier of an object
    search (Optional[str], optional): No description. 
    values (Optional[List[ID]], optional): No description. 
    limit (Optional[int], optional): No description. 
    offset (Optional[int], optional): No description. Defaults to 0
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    List[SearchTableRowsQueryTablerows]
"""
    return (await aexecute(SearchTableRowsQuery, {'search': search, 'values': values, 'table': table, 'limit': limit, 'offset': offset}, rath=rath)).options

def search_table_rows(table: ID, search: Optional[str]=None, values: Optional[List[ID]]=None, limit: Optional[int]=None, offset: Optional[int]=0, rath: Optional[MikroNextRath]=None) -> Tuple[SearchTableRowsQueryOptions, ...]:
    """SearchTableRows 

List the rows of a table, paginated over the table's parquet data

Args:
    table (ID): The unique identifier of an object
    search (Optional[str], optional): No description. 
    values (Optional[List[ID]], optional): No description. 
    limit (Optional[int], optional): No description. 
    offset (Optional[int], optional): No description. Defaults to 0
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    List[SearchTableRowsQueryTablerows]
"""
    return execute(SearchTableRowsQuery, {'search': search, 'values': values, 'table': table, 'limit': limit, 'offset': offset}, rath=rath).options

async def aget_rgb_view(id: ID, rath: Optional[MikroNextRath]=None) -> RGBView:
    """GetRGBView 

Get a single RGB render view by ID

Args:
    id (ID): The unique identifier of an object
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    RGBView
"""
    return (await aexecute(GetRGBViewQuery, {'id': id}, rath=rath)).rgb_view

def get_rgb_view(id: ID, rath: Optional[MikroNextRath]=None) -> RGBView:
    """GetRGBView 

Get a single RGB render view by ID

Args:
    id (ID): The unique identifier of an object
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    RGBView
"""
    return execute(GetRGBViewQuery, {'id': id}, rath=rath).rgb_view

async def asearch_rgb_views(search: Optional[str]=None, values: Optional[List[ID]]=None, limit: Optional[int]=None, offset: Optional[int]=0, rath: Optional[MikroNextRath]=None) -> Tuple[SearchRGBViewsQueryOptions, ...]:
    """SearchRGBViews 

List RGB render views (per-channel display settings)

Args:
    search (Optional[str], optional): No description. 
    values (Optional[List[ID]], optional): No description. 
    limit (Optional[int], optional): No description. 
    offset (Optional[int], optional): No description. Defaults to 0
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    List[SearchRGBViewsQueryRgbviews]
"""
    return (await aexecute(SearchRGBViewsQuery, {'search': search, 'values': values, 'limit': limit, 'offset': offset}, rath=rath)).options

def search_rgb_views(search: Optional[str]=None, values: Optional[List[ID]]=None, limit: Optional[int]=None, offset: Optional[int]=0, rath: Optional[MikroNextRath]=None) -> Tuple[SearchRGBViewsQueryOptions, ...]:
    """SearchRGBViews 

List RGB render views (per-channel display settings)

Args:
    search (Optional[str], optional): No description. 
    values (Optional[List[ID]], optional): No description. 
    limit (Optional[int], optional): No description. 
    offset (Optional[int], optional): No description. Defaults to 0
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    List[SearchRGBViewsQueryRgbviews]
"""
    return execute(SearchRGBViewsQuery, {'search': search, 'values': values, 'limit': limit, 'offset': offset}, rath=rath).options

async def awatch_files(dataset: Optional[ID]=None, rath: Optional[MikroNextRath]=None) -> AsyncIterator[WatchFilesSubscriptionFiles]:
    """WatchFiles 

Subscribe to real-time file updates

Args:
    dataset (Optional[ID], optional): No description. 
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    WatchFilesSubscriptionFiles
"""
    async for event in asubscribe(WatchFilesSubscription, {'dataset': dataset}, rath=rath):
        yield event.files

def watch_files(dataset: Optional[ID]=None, rath: Optional[MikroNextRath]=None) -> Iterator[WatchFilesSubscriptionFiles]:
    """WatchFiles 

Subscribe to real-time file updates

Args:
    dataset (Optional[ID], optional): No description. 
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    WatchFilesSubscriptionFiles
"""
    for event in subscribe(WatchFilesSubscription, {'dataset': dataset}, rath=rath):
        yield event.files

async def awatch_images(dataset: Optional[ID]=None, rath: Optional[MikroNextRath]=None) -> AsyncIterator[WatchImagesSubscriptionImages]:
    """WatchImages 

Subscribe to real-time image updates

Args:
    dataset (Optional[ID], optional): No description. 
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    WatchImagesSubscriptionImages
"""
    async for event in asubscribe(WatchImagesSubscription, {'dataset': dataset}, rath=rath):
        yield event.images

def watch_images(dataset: Optional[ID]=None, rath: Optional[MikroNextRath]=None) -> Iterator[WatchImagesSubscriptionImages]:
    """WatchImages 

Subscribe to real-time image updates

Args:
    dataset (Optional[ID], optional): No description. 
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    WatchImagesSubscriptionImages
"""
    for event in subscribe(WatchImagesSubscription, {'dataset': dataset}, rath=rath):
        yield event.images

async def awatch_rois(image: ID, rath: Optional[MikroNextRath]=None) -> AsyncIterator[WatchRoisSubscriptionRois]:
    """WatchRois 

Subscribe to real-time ROI updates

Args:
    image (ID): No description
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    WatchRoisSubscriptionRois
"""
    async for event in asubscribe(WatchRoisSubscription, {'image': image}, rath=rath):
        yield event.rois

def watch_rois(image: ID, rath: Optional[MikroNextRath]=None) -> Iterator[WatchRoisSubscriptionRois]:
    """WatchRois 

Subscribe to real-time ROI updates

Args:
    image (ID): No description
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    WatchRoisSubscriptionRois
"""
    for event in subscribe(WatchRoisSubscription, {'image': image}, rath=rath):
        yield event.rois
AffineTransformationViewFilter.model_rebuild()
CoordinateAnchorInput.model_rebuild()
CreateADatasetInput.model_rebuild()
CreateDataRoiInput.model_rebuild()
CreateLensInput.model_rebuild()
CreateRGBContextInput.model_rebuild()
DatasetFilter.model_rebuild()
EraFilter.model_rebuild()
FromArrayLikeInput.model_rebuild()
FromParquetLike.model_rebuild()
ImageFilter.model_rebuild()
LightPortInput.model_rebuild()
LightpathGraphInput.model_rebuild()
OpticalElementInput.model_rebuild()
Pose3DInput.model_rebuild()
RenderTreeInput.model_rebuild()
StageFilter.model_rebuild()
TimepointViewFilter.model_rebuild()
TreeInput.model_rebuild()
TreeNodeInput.model_rebuild()
ViewFilter.model_rebuild()
ZarrStoreFilter.model_rebuild()