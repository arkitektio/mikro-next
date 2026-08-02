from mikro_next.scalars import FileLike, FiveDVector, ArrayLike, ImageLike, ParquetCoercible, ParquetLike, ImageFileCoercible, LabelsLike, ArrayCoercible, ImageFileLike, FourByFourMatrix, ImageCoercible, ThreeDVector
from pydantic import Field, BaseModel, ConfigDict
from rath.scalars import IDCoercible, ID
from mikro_next.traits import ValueHistogramInputTrait, MikroFetchable, CoordinateAnchorInputTrait, FileTrait, TransformationTrait, DatasetTrait, CreateADatasetTrait, IsVectorizableTrait, HasZarrStoreAccessor, HasParquetStoreAccesor, HasZarrStoreTrait, AxisInputTrait, DataArrayTrait, Lensable, HasPresignedDownloadAccessor, HasParquestStoreTrait, HasDownloadAccessor, SceneTrait, CoordinateSystemTrait
from mikro_next.funcs import execute, subscribe, asubscribe, aexecute
from kanne.scalars import Duration, Temperature, GenericQuantity, Frequency, Length, Power, Unit
from typing import Optional, Dict, Union, Literal, AsyncIterator, Any, Iterator, Iterable, Tuple, Annotated, List
from mikro_next.rath import MikroNextRath
from enum import Enum
from datetime import datetime

class GraphQLDefault:
    """Records a GraphQL field schema default value. The client omits the field so the server applies its own default; this preserves the value for introspection."""

    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return 'GraphQLDefault(' + repr(self.value) + ')'

class UnsetType:
    """Sentinel for arguments the caller did not provide. Such fields are omitted on serialization so the GraphQL server applies its own default."""
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __repr__(self):
        return 'UNSET'

    def __bool__(self):
        return False
UNSET = UnsetType()

class ADatasetSpec(str, Enum):
    """What a dataset structurally is, materialized from the axes of its intrinsic coordinate system at creation. Specs stack: a 3D timelapse is VOLUME, TIMESERIES and MULTICHANNEL at once. Exactly one spatial member (SCALAR/PROFILE/IMAGE/VOLUME/HYPERVOLUME) ever holds."""
    SCALAR = 'SCALAR'
    'No spatial extent: the array carries no SPACE axis at all.'
    PROFILE = 'PROFILE'
    'One spatial axis -- a line profile, a depth trace.'
    IMAGE = 'IMAGE'
    'Two spatial axes: a plane. The ordinary micrograph.'
    VOLUME = 'VOLUME'
    'Three spatial axes: a stack. Holds whenever a z axis is present, even if it carries a single plane.'
    HYPERVOLUME = 'HYPERVOLUME'
    'Four or more spatial axes.'
    TIMESERIES = 'TIMESERIES'
    'Carries a TIME axis -- a timelapse. Presence only: a single-frame time axis still counts.'
    MULTICHANNEL = 'MULTICHANNEL'
    'Carries a CHANNEL axis. Presence only: a one-channel axis still counts.'
    SPECTRAL = 'SPECTRAL'
    'Carries a SPECTRUM axis: a spectrally resolved acquisition, a lambda stack.'
    FLIM = 'FLIM'
    'Carries a MICROTIME axis: fluorescence-lifetime arrival-time bins.'

class AxisType(str, Enum):
    """The semantic kind of an axis. A system's axes must be ordered by type: time first, then channel and custom types, then space."""
    SPACE = 'SPACE'
    'A spatial axis. Unitless pixel indices in a pixel-grid system; carries a physical length unit in a unit-carrying system.'
    TIME = 'TIME'
    'A time axis. Frame indices in a pixel-grid system; carries a physical duration unit in a unit-carrying system.'
    CHANNEL = 'CHANNEL'
    'A categorical channel axis: its coordinates index acquisitions, not positions. Never downsampled.'
    COORDINATE = 'COORDINATE'
    'The value axis of a coordinate-valued array: its positions enumerate the components of an absolute output position. This is what makes the array readable as the `field` of a FIELD edge. A scalar-valued field (a label mask, whose one value is an object id) carries no value axis at all -- absent means scalar, and scalar means COORDINATE.'
    DISPLACEMENT = 'DISPLACEMENT'
    'The value axis of a displacement-valued array: its positions enumerate the components of a per-point OFFSET, where COORDINATE enumerates absolute positions. Stating it here rather than on the edge is deliberate: it is a property of the array, and an array that says it twice can disagree with itself.'
    MICROTIME = 'MICROTIME'
    'A FLIM arrival-time bin. Continuous, so a pyramid may re-bin it, and a phasor may be taken over it.'
    SPECTRUM = 'SPECTRUM'
    'A wavelength bin of a spectrally resolved acquisition. Continuous -- unlike a CHANNEL axis, whose coordinates index acquisitions rather than positions -- so a pyramid may re-bin it, and a phasor may be taken over it.'
    INDEX = 'INDEX'
    'An enumerating axis with no metric: an object id, a row number. It has no unit because there is nothing to measure — the distance between object 3 and object 4 means nothing.'

class Blending(str, Enum):
    """The blending mode used to combine multiple channels or layers into a composite image."""
    ADDITIVE = 'ADDITIVE'
    'Additive blending, where the color values of overlapping layers are summed.'
    MULTIPLICATIVE = 'MULTIPLICATIVE'
    'Multiplicative blending, where the color values of overlapping layers are multiplied.'
    NORMAL = 'NORMAL'
    'Alpha-over compositing: the layer is blended over the layers below using its opacity.'

class BootstrapLayerKind(str, Enum):
    """The render recipe an image layer carries: which default graph createSceneFromCoordinateSystem builds, via `ScenePolicyInput.kind`."""
    RGB = 'RGB'
    'Composite three channels as red, green and blue. Inferred for a 2D dataset whose channel axis has exactly three positions -- a photograph, a brightfield slide.'
    INTENSITY = 'INTENSITY'
    'One colormapped source per channel, additively blended (grey for a single channel). The fluorescence default, and the fallback when nothing else is inferred.'
    VOLUME = 'VOLUME'
    'The channel sources under a maximum-intensity projection over z. Inferred when the dataset has a z axis with more than one plane.'
    LABEL = 'LABEL'
    'A single categorical source mapping discrete integer labels to distinct colors. Never inferred from structure -- nothing about an array distinguishes a label map from an image -- so it comes either from a derivation declared CATEGORIZED or from stating it outright.'

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

class CreatableTransformKind(str, Enum):
    """The kind of a transformation a client can author directly: the discriminator of `TransformInput`. SEQUENCE and BIJECTION are absent on purpose -- they are wrappers the ingest builds together with their children (pyramid levels, stepped lenses), never authored empty."""
    IDENTITY = 'IDENTITY'
    'The identity map. Input and output coordinates are the same, so it takes no parameters.'
    SCALE = 'SCALE'
    'A per-axis multiplication. Takes `scale`, one entry per input axis.'
    TRANSLATION = 'TRANSLATION'
    'A per-axis offset. Takes `translation`, one entry per input axis.'
    MAP_AXIS = 'MAP_AXIS'
    'A permutation of axes, mapping each input axis to an output axis by name. Takes `inputAxes` and `outputAxes`; the matrix is synthesized from them.'
    AFFINE = 'AFFINE'
    'A general affine map. Takes `affine`, an M x (N+1) matrix with rows outermost.'
    ROTATION = 'ROTATION'
    'A rotation. Takes `affine`: the orthonormal matrix, in the same layout an AFFINE uses.'
    BY_DIMENSION = 'BY_DIMENSION'
    'A map acting on a named subset of the axes and saying nothing about the rest. Takes `inputAxes` and `outputAxes`, and optionally `scale`, `translation` or `affine` acting on the named axes.'
    FIELD = 'FIELD'
    "A non-affine map given by the values of an array rather than by a formula. Takes `field` (the array's coordinate system), `inputAxes` and `outputAxes`."
    UNMAPPABLE = 'UNMAPPABLE'
    'A declared NON-correspondence: no point of either space maps to a point of the other. Takes only an optional `reason`.'

class DerivationSourceKind(str, Enum):
    """Which kind of thing a derivation names as the source its data was computed from: the discriminator of `DerivedFromInput`. The edge itself is the same whichever is chosen -- child space in, source space out -- so a table named as TABLE_DATASET and the same table named as COORDINATE_SYSTEM write the identical row; the read side reports what lives at the far end through `CoordinateSystem.residents`, not which member was used to say it"""
    LENS = 'LENS'
    "A selection over an array dataset, and the preferred way to name one: a lens' own edge back to its dataset already carries the crop, so pointing at it gets the rest of the chain for free."
    DATASET = 'DATASET'
    'An array dataset as a whole, through its intrinsic pixel grid. Use it when the source is the entire image and there is no lens worth minting.'
    TABLE_DATASET = 'TABLE_DATASET'
    'A table dataset, through the space its coordinate columns declare -- the direction an image reconstructed from a table of SMLM localizations is derived. A table with no coordinate columns enumerates objects rather than places them, and its only honest edge is UNMAPPABLE.'
    MESH_COLLECTION = 'MESH_COLLECTION'
    'A mesh collection, through its vertex coordinate system.'
    ANNOTATION_COLLECTION = 'ANNOTATION_COLLECTION'
    'An annotation collection, through the space its shapes are drawn in.'
    COORDINATE_SYSTEM = 'COORDINATE_SYSTEM'
    'A coordinate system directly, when the source is a space rather than a container -- a physical space, or a world.'

class Easing(str, Enum):
    """How a viewer eases the camera along the travel into an animation waypoint."""
    LINEAR = 'LINEAR'
    'Constant speed the whole way. Right for a leg in the middle of a continuous move, where an ease would read as a stutter.'
    EASE_IN = 'EASE_IN'
    'Start slow, arrive at full speed. Right for the first leg, pulling away from rest.'
    EASE_OUT = 'EASE_OUT'
    'Start at full speed, arrive slowly. Right for the last leg, settling onto the final pose.'
    EASE_IN_OUT = 'EASE_IN_OUT'
    'Slow at both ends, quick in the middle. The default: it reads as deliberate on a leg that stands alone.'

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

class FilterKind(str, Enum):
    """No documentation"""
    DICHROIC = 'DICHROIC'
    LONG_PASS = 'LONG_PASS'
    SHORT_PASS = 'SHORT_PASS'
    BAND_PASS = 'BAND_PASS'
    MULTI_PASS = 'MULTI_PASS'
    NEUTRAL_DENSITY = 'NEUTRAL_DENSITY'
    TUNEABLE = 'TUNEABLE'
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

class PhasorColorMode(str, Enum):
    """What a phasor render node derives a pixel's color from."""
    PHASE = 'PHASE'
    'The angle of the phasor. Over a microtime axis this is the phase lifetime (tau_phi); over a spectrum axis, the spectral centre of mass.'
    MODULATION = 'MODULATION'
    'The modulus of the phasor. Over a microtime axis this is the modulation lifetime (tau_m); it exceeds tau_phi exactly when the decay is multi-exponential.'
    AVERAGE = 'AVERAGE'
    'The mean of the phase- and modulation-derived values.'

class PhasorCursorKind(str, Enum):
    """The shape of a region selected in phasor space."""
    CIRCLE = 'CIRCLE'
    'A disc, given by its centre (g, s) and a radius.'
    POLYGON = 'POLYGON'
    'An arbitrary closed region, given by at least three (g, s) vertices.'

class PlacementValidity(str, Enum):
    """How much a transformation edge's map is actually known: guessed, inferred from metadata, authored by someone, or validated against the data. A layer's validity is derived from it, never stored: the weakest edge on its path to world."""
    MANUAL = 'MANUAL'
    'Someone authored this map -- a registration pipeline, a human with a matrix. It exists on purpose, but nothing has checked it against the data.'
    INFERRED = 'INFERRED'
    'The numbers were read from acquisition metadata (a pixel size, a stage pose). As right as the metadata is.'
    VALIDATED = 'VALIDATED'
    'Exact or checked: either the server derived the map from shapes and slices, so it cannot be wrong, or someone validated an authored registration against the data.'
    UNKNOWN = 'UNKNOWN'
    'This map was assumed, never measured -- badge it. The server writes it nowhere: nothing fabricates a placement any more, so an edge wears UNKNOWN only because a client said so on `createTransformation`, or because it is a historical auto-registered edge.'

class PortRole(str, Enum):
    """No documentation"""
    INPUT = 'INPUT'
    OUTPUT = 'OUTPUT'

class PreferredView(str, Enum):
    """How a viewer should open a scene: flat, volumetric, or its own choice."""
    TWO_D = 'TWO_D'
    'Open flat: the cross-section view, one slice at a time.'
    THREE_D = 'THREE_D'
    'Open volumetric: the projection view, looking at the data as a body.'
    AUTO = 'AUTO'
    'No preference stated -- the viewer decides, e.g. from whether the data has a z axis with depth. The default: a scene nobody has expressed a preference for should not claim one.'

class ProjectionMode(str, Enum):
    """The 3D projection / rendering mode applied to a volumetric (z-stacked) render node."""
    MIP = 'MIP'
    'Maximum intensity projection: each output pixel takes the maximum value along the z-axis.'
    ATTENUATED_MIP = 'ATTENUATED_MIP'
    'Attenuated maximum intensity projection, weighting samples by depth so nearer samples dominate.'
    VOLUME = 'VOLUME'
    'Alpha volume rendering: samples along z are alpha-composited front-to-back.'
    ISOSURFACE = 'ISOSURFACE'
    'Isosurface rendering: a surface is extracted at a threshold value.'

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
    "An ellipse in the XY plane, with a radius per axis. Vectors are the two opposite corners of its bounding rectangle; each semi-axis is half that axis' extent."
    POLYGON = 'POLYGON'
    'A closed polygon defined by a sequence of vertices.'
    LINE = 'LINE'
    'A straight line between two points.'
    CIRCLE = 'CIRCLE'
    'A circle in the XY plane. Vectors are the two opposite corners of its bounding square; the radius is half the (uniform by construction) extent.'
    SPHERE = 'SPHERE'
    'A sphere spanning the spatial axes (XYZ). Vectors are the two opposite corners of its bounding cube; the radius is half the (uniform by construction) extent.'
    ELLIPSOID = 'ELLIPSOID'
    "An ellipsoid spanning the spatial axes (XYZ), with a radius per axis. Vectors are the two opposite corners of its bounding cuboid; each semi-axis is half that axis' extent."
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
    MULTI_POINT = 'MULTI_POINT'
    'A set of unconnected points drawn as one region, e.g. a counting click set. Vectors are the points themselves, in no particular order and with no connectivity implied.'

class RoiKindChoices(str, Enum):
    """No documentation"""
    ELLIPSIS = 'ELLIPSIS'
    POLYGON = 'POLYGON'
    LINE = 'LINE'
    CIRCLE = 'CIRCLE'
    SPHERE = 'SPHERE'
    ELLIPSOID = 'ELLIPSOID'
    RECTANGLE = 'RECTANGLE'
    SPECTRAL_RECTANGLE = 'SPECTRAL_RECTANGLE'
    TEMPORAL_RECTANGLE = 'TEMPORAL_RECTANGLE'
    CUBE = 'CUBE'
    SPECTRAL_CUBE = 'SPECTRAL_CUBE'
    TEMPORAL_CUBE = 'TEMPORAL_CUBE'
    HYPERCUBE = 'HYPERCUBE'
    SPECTRAL_HYPERCUBE = 'SPECTRAL_HYPERCUBE'
    PATH = 'PATH'
    UNKNOWN = 'UNKNOWN'
    FRAME = 'FRAME'
    SLICE = 'SLICE'
    POINT = 'POINT'
    MULTI_POINT = 'MULTI_POINT'

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

class TableColumnRole(str, Enum):
    """What a table dataset's column is for: a coordinate that places the row, or data hanging off it."""
    COORDINATE = 'COORDINATE'
    "A spatial or temporal column whose values are coordinates. The coordinate columns become the axes of the table's own coordinate system, which is what makes the table placeable."
    ATTRIBUTE = 'ATTRIBUTE'
    'A measurement or property column — area, an intensity, a marker level. Data only; it does not place the row.'
    ID = 'ID'
    'A per-row identifier.'
    TRACK_ID = 'TRACK_ID'
    'Groups rows into a trajectory. Required to render a table as tracks.'
    LABEL = 'LABEL'
    'A per-row text label.'
    COLOR = 'COLOR'
    'A per-row color, or a value a layer colors the rows by.'

class TransformKind(str, Enum):
    """The kind of a coordinate transformation, discriminating how its parameters are interpreted. Direction is always forward: input -> output."""
    IDENTITY = 'IDENTITY'
    'The identity map. Input and output coordinates are the same.'
    SCALE = 'SCALE'
    'A per-axis multiplication. Its `scale` has one entry per input axis.'
    TRANSLATION = 'TRANSLATION'
    'A per-axis offset. Its `translation` has one entry per input axis.'
    MAP_AXIS = 'MAP_AXIS'
    'A permutation of axes, mapping each input axis to an output axis by name.'
    AFFINE = 'AFFINE'
    'A general affine map, given as an M x (N+1) matrix with rows outermost.'
    ROTATION = 'ROTATION'
    'A rotation, given as an orthonormal matrix.'
    SEQUENCE = 'SEQUENCE'
    'An ordered composition of child transformations, applied first to last.'
    BY_DIMENSION = 'BY_DIMENSION'
    'A composition of child transformations, each acting on a named subset of the axes.'
    FIELD = 'FIELD'
    'A non-affine map given by the values of an array rather than by a formula. The array is a `field`: a coordinate system, and so a node of this graph, not a payload on this edge. Whether its values are absolute POSITIONS or per-point OFFSETS is read from the value axis of that node -- COORDINATE or DISPLACEMENT -- never restated here. A label mask is the case where the field IS the input: its own pixels are the map. Not invertible in closed form, so a placement path never walks it backwards -- which is also the right semantics for a dereference, an object being a set of pixels.'
    BIJECTION = 'BIJECTION'
    'A pair of child transformations giving an explicit forward and inverse map. This is how an inverse that cannot be derived is instead *given*.'
    UNMAPPABLE = 'UNMAPPABLE'
    'A declared NON-correspondence: the two systems are related — one was derived from the other — and no point of either maps to a point of the other. It carries no parameters, is constrained by no rank, has no matrix, and is never walked by a placement search, in either direction. Recording an IDENTITY instead would be a lie; recording nothing would lose the lineage.'

class TransformKindChoices(str, Enum):
    """No documentation"""
    IDENTITY = 'IDENTITY'
    SCALE = 'SCALE'
    TRANSLATION = 'TRANSLATION'
    MAP_AXIS = 'MAP_AXIS'
    AFFINE = 'AFFINE'
    ROTATION = 'ROTATION'
    SEQUENCE = 'SEQUENCE'
    BY_DIMENSION = 'BY_DIMENSION'
    FIELD = 'FIELD'
    BIJECTION = 'BIJECTION'
    UNMAPPABLE = 'UNMAPPABLE'

class ValueRelation(str, Enum):
    """What a derivation did to the values -- the axis the spatial kind says nothing about. A threshold is spatially IDENTITY with categorized values; a crop is value-identical. Stated on the derivation edge (one event, one row, two orthogonal statements); the algorithm and its parameters belong to task provenance, not here."""
    IDENTICAL = 'IDENTICAL'
    "The target's numbers are the source's numbers (a crop, an axis reorder): value statistics -- histograms, contrast limits -- transfer across the edge."
    TRANSFORMED = 'TRANSFORMED'
    "The same quantity with new numbers (a deconvolution, a normalization, a denoise): still an intensity, but nothing computed on the source's values transfers."
    CATEGORIZED = 'CATEGORIZED'
    'The values became labels or classes (a threshold, a segmentation): a different value domain. This is the structural signal that lets a bootstrapped scene render the data as a label map.'

class AffineTransformInput(BaseModel):
    """The fields an AFFINE member of TransformInput reads. Published for codegen; the wire type is the flat TransformInput"""
    kind: Literal['AFFINE'] = Field(default='AFFINE')
    affine: Tuple[Tuple[float, ...], ...]

    def model_post_init(self, context):
        self.__pydantic_fields_set__.update({'kind'})
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class AnnotationCollectionDerivedFromInput(BaseModel):
    """The fields an ANNOTATION_COLLECTION derivation reads. Published for codegen; the wire type is the flat DerivedFromInput"""
    kind: Literal['ANNOTATION_COLLECTION'] = Field(default='ANNOTATION_COLLECTION')
    transform: Optional['TransformInput'] = None
    value_relation: Optional[ValueRelation] = Field(alias='valueRelation', default=None)
    annotation_collection: ID = Field(alias='annotationCollection')

    def model_post_init(self, context):
        self.__pydantic_fields_set__.update({'kind'})
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class ApertureElementInput(BaseModel):
    """The fields an APERTURE element reads. Published for codegen; the wire type is the flat OpticalElementInput"""
    kind: Literal['APERTURE'] = Field(default='APERTURE')
    id: Optional[ID] = None
    label: str
    pose: Optional['Pose3DInput'] = None
    ports: Annotated[Optional[Tuple['LightPortInput', ...]], GraphQLDefault('[]')] = None
    'Default: []'
    manufacturer: Optional[str] = None
    model: Optional[str] = None
    serial_number: Optional[str] = Field(alias='serialNumber', default=None)
    diameter: Optional[Length] = None

    def model_post_init(self, context):
        self.__pydantic_fields_set__.update({'kind'})
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class BeamSplitterElementInput(BaseModel):
    """The fields a BEAM_SPLITTER element reads. Published for codegen; the wire type is the flat OpticalElementInput"""
    kind: Literal['BEAM_SPLITTER'] = Field(default='BEAM_SPLITTER')
    id: Optional[ID] = None
    label: str
    pose: Optional['Pose3DInput'] = None
    ports: Annotated[Optional[Tuple['LightPortInput', ...]], GraphQLDefault('[]')] = None
    'Default: []'
    manufacturer: Optional[str] = None
    model: Optional[str] = None
    serial_number: Optional[str] = Field(alias='serialNumber', default=None)
    r_fraction: Optional[float] = Field(alias='rFraction', default=None)
    t_fraction: Optional[float] = Field(alias='tFraction', default=None)
    band_min: Optional[Length] = Field(alias='bandMin', default=None)
    band_max: Optional[Length] = Field(alias='bandMax', default=None)

    def model_post_init(self, context):
        self.__pydantic_fields_set__.update({'kind'})
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class ByDimensionTransformInput(BaseModel):
    """The fields a BY_DIMENSION member of TransformInput reads. Published for codegen; the wire type is the flat TransformInput"""
    kind: Literal['BY_DIMENSION'] = Field(default='BY_DIMENSION')
    input_axes: Tuple[str, ...] = Field(alias='inputAxes')
    output_axes: Tuple[str, ...] = Field(alias='outputAxes')
    scale: Optional[Tuple[float, ...]] = None
    translation: Optional[Tuple[float, ...]] = None
    affine: Optional[Tuple[Tuple[float, ...], ...]] = None

    def model_post_init(self, context):
        self.__pydantic_fields_set__.update({'kind'})
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class CCDElementInput(BaseModel):
    """The fields a CCD element reads. Published for codegen; the wire type is the flat OpticalElementInput"""
    kind: Literal['CCD'] = Field(default='CCD')
    id: Optional[ID] = None
    label: str
    pose: Optional['Pose3DInput'] = None
    ports: Annotated[Optional[Tuple['LightPortInput', ...]], GraphQLDefault('[]')] = None
    'Default: []'
    manufacturer: Optional[str] = None
    model: Optional[str] = None
    serial_number: Optional[str] = Field(alias='serialNumber', default=None)
    pixel_size: Optional[Length] = Field(alias='pixelSize', default=None)
    resolution: Optional[Tuple[int, ...]] = None

    def model_post_init(self, context):
        self.__pydantic_fields_set__.update({'kind'})
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class CoordinateSystemDerivedFromInput(BaseModel):
    """The fields a COORDINATE_SYSTEM derivation reads. Published for codegen; the wire type is the flat DerivedFromInput"""
    kind: Literal['COORDINATE_SYSTEM'] = Field(default='COORDINATE_SYSTEM')
    transform: Optional['TransformInput'] = None
    value_relation: Optional[ValueRelation] = Field(alias='valueRelation', default=None)
    coordinate_system: ID = Field(alias='coordinateSystem')

    def model_post_init(self, context):
        self.__pydantic_fields_set__.update({'kind'})
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class DatasetDerivedFromInput(BaseModel):
    """The fields a DATASET derivation reads. Published for codegen; the wire type is the flat DerivedFromInput"""
    kind: Literal['DATASET'] = Field(default='DATASET')
    transform: Optional['TransformInput'] = None
    value_relation: Optional[ValueRelation] = Field(alias='valueRelation', default=None)
    dataset: ID

    def model_post_init(self, context):
        self.__pydantic_fields_set__.update({'kind'})
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class DetectorElementInput(BaseModel):
    """The fields a DETECTOR element reads. Published for codegen; the wire type is the flat OpticalElementInput"""
    kind: Literal['DETECTOR'] = Field(default='DETECTOR')
    id: Optional[ID] = None
    label: str
    pose: Optional['Pose3DInput'] = None
    ports: Annotated[Optional[Tuple['LightPortInput', ...]], GraphQLDefault('[]')] = None
    'Default: []'
    manufacturer: Optional[str] = None
    model: Optional[str] = None
    serial_number: Optional[str] = Field(alias='serialNumber', default=None)
    nepd_w_per_sqrt_hz: Optional[float] = Field(alias='nepdWPerSqrtHz', default=None)
    amplifier_gain_db: Optional[float] = Field(alias='amplifierGainDb', default=None)
    gain: Optional[float] = None

    def model_post_init(self, context):
        self.__pydantic_fields_set__.update({'kind'})
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class FieldTransformInput(BaseModel):
    """The fields a FIELD member of TransformInput reads. Published for codegen; the wire type is the flat TransformInput"""
    kind: Literal['FIELD'] = Field(default='FIELD')
    field: ID
    input_axes: Tuple[str, ...] = Field(alias='inputAxes')
    output_axes: Tuple[str, ...] = Field(alias='outputAxes')

    def model_post_init(self, context):
        self.__pydantic_fields_set__.update({'kind'})
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class FilterElementInput(BaseModel):
    """The fields a FILTER element reads. Published for codegen; the wire type is the flat OpticalElementInput"""
    kind: Literal['FILTER'] = Field(default='FILTER')
    id: Optional[ID] = None
    label: str
    pose: Optional['Pose3DInput'] = None
    ports: Annotated[Optional[Tuple['LightPortInput', ...]], GraphQLDefault('[]')] = None
    'Default: []'
    manufacturer: Optional[str] = None
    model: Optional[str] = None
    serial_number: Optional[str] = Field(alias='serialNumber', default=None)
    description: Optional[str] = None
    filter_kind: Optional[FilterKind] = Field(alias='filterKind', default=None)
    transmittance: Optional[float] = None

    def model_post_init(self, context):
        self.__pydantic_fields_set__.update({'kind'})
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class LampElementInput(BaseModel):
    """The fields a LAMP element reads. Published for codegen; the wire type is the flat OpticalElementInput"""
    kind: Literal['LAMP'] = Field(default='LAMP')
    id: Optional[ID] = None
    label: str
    pose: Optional['Pose3DInput'] = None
    ports: Annotated[Optional[Tuple['LightPortInput', ...]], GraphQLDefault('[]')] = None
    'Default: []'
    manufacturer: Optional[str] = None
    model: Optional[str] = None
    serial_number: Optional[str] = Field(alias='serialNumber', default=None)
    channel: Optional[ChannelKind] = None
    lamp_type: Optional[str] = Field(alias='lampType', default=None)

    def model_post_init(self, context):
        self.__pydantic_fields_set__.update({'kind'})
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class LaserElementInput(BaseModel):
    """The fields a LASER element reads. Published for codegen; the wire type is the flat OpticalElementInput"""
    kind: Literal['LASER'] = Field(default='LASER')
    id: Optional[ID] = None
    label: str
    pose: Optional['Pose3DInput'] = None
    ports: Annotated[Optional[Tuple['LightPortInput', ...]], GraphQLDefault('[]')] = None
    'Default: []'
    manufacturer: Optional[str] = None
    model: Optional[str] = None
    serial_number: Optional[str] = Field(alias='serialNumber', default=None)
    nominal_wavelength: Length = Field(alias='nominalWavelength')
    power: Optional[Power] = None
    channel: Optional[ChannelKind] = None
    laser_medium: Optional[str] = Field(alias='laserMedium', default=None)
    pulse_kind: Optional[PulseKind] = Field(alias='pulseKind', default=None)
    repetition_rate: Optional[Frequency] = Field(alias='repetitionRate', default=None)
    has_pockels_cell: Optional[bool] = Field(alias='hasPockelsCell', default=None)
    has_q_switch: Optional[bool] = Field(alias='hasQSwitch', default=None)

    def model_post_init(self, context):
        self.__pydantic_fields_set__.update({'kind'})
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class LensDerivedFromInput(BaseModel):
    """The fields a LENS derivation reads. Published for codegen; the wire type is the flat DerivedFromInput"""
    kind: Literal['LENS'] = Field(default='LENS')
    transform: Optional['TransformInput'] = None
    value_relation: Optional[ValueRelation] = Field(alias='valueRelation', default=None)
    lens: ID

    def model_post_init(self, context):
        self.__pydantic_fields_set__.update({'kind'})
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class LensElementInput(BaseModel):
    """The fields a LENS element reads. Published for codegen; the wire type is the flat OpticalElementInput"""
    kind: Literal['LENS'] = Field(default='LENS')
    id: Optional[ID] = None
    label: str
    pose: Optional['Pose3DInput'] = None
    ports: Annotated[Optional[Tuple['LightPortInput', ...]], GraphQLDefault('[]')] = None
    'Default: []'
    manufacturer: Optional[str] = None
    model: Optional[str] = None
    serial_number: Optional[str] = Field(alias='serialNumber', default=None)
    focal_length: Optional[Length] = Field(alias='focalLength', default=None)

    def model_post_init(self, context):
        self.__pydantic_fields_set__.update({'kind'})
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class MapAxisTransformInput(BaseModel):
    """The fields a MAP_AXIS member of TransformInput reads. Published for codegen; the wire type is the flat TransformInput"""
    kind: Literal['MAP_AXIS'] = Field(default='MAP_AXIS')
    input_axes: Tuple[str, ...] = Field(alias='inputAxes')
    output_axes: Tuple[str, ...] = Field(alias='outputAxes')

    def model_post_init(self, context):
        self.__pydantic_fields_set__.update({'kind'})
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class MeshCollectionDerivedFromInput(BaseModel):
    """The fields a MESH_COLLECTION derivation reads. Published for codegen; the wire type is the flat DerivedFromInput"""
    kind: Literal['MESH_COLLECTION'] = Field(default='MESH_COLLECTION')
    transform: Optional['TransformInput'] = None
    value_relation: Optional[ValueRelation] = Field(alias='valueRelation', default=None)
    mesh_collection: ID = Field(alias='meshCollection')

    def model_post_init(self, context):
        self.__pydantic_fields_set__.update({'kind'})
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class MirrorElementInput(BaseModel):
    """The fields a MIRROR element reads. Published for codegen; the wire type is the flat OpticalElementInput"""
    kind: Literal['MIRROR'] = Field(default='MIRROR')
    id: Optional[ID] = None
    label: str
    pose: Optional['Pose3DInput'] = None
    ports: Annotated[Optional[Tuple['LightPortInput', ...]], GraphQLDefault('[]')] = None
    'Default: []'
    manufacturer: Optional[str] = None
    model: Optional[str] = None
    serial_number: Optional[str] = Field(alias='serialNumber', default=None)
    angle_deg: Optional[float] = Field(alias='angleDeg', default=None)
    band_min: Optional[Length] = Field(alias='bandMin', default=None)
    band_max: Optional[Length] = Field(alias='bandMax', default=None)

    def model_post_init(self, context):
        self.__pydantic_fields_set__.update({'kind'})
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class ObjectiveElementInput(BaseModel):
    """The fields an OBJECTIVE element reads. Published for codegen; the wire type is the flat OpticalElementInput"""
    kind: Literal['OBJECTIVE'] = Field(default='OBJECTIVE')
    id: Optional[ID] = None
    label: str
    pose: Optional['Pose3DInput'] = None
    ports: Annotated[Optional[Tuple['LightPortInput', ...]], GraphQLDefault('[]')] = None
    'Default: []'
    manufacturer: Optional[str] = None
    model: Optional[str] = None
    serial_number: Optional[str] = Field(alias='serialNumber', default=None)
    magnification: Optional[float] = None
    numerical_aperture: Optional[float] = Field(alias='numericalAperture', default=None)
    brand: Optional[str] = None
    working_distance: Optional[Length] = Field(alias='workingDistance', default=None)
    immersion_medium: Optional[ObjectiveImmersion] = Field(alias='immersionMedium', default=None)
    iris: Optional[bool] = None

    def model_post_init(self, context):
        self.__pydantic_fields_set__.update({'kind'})
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class OtherElementInput(BaseModel):
    """The fields an OTHER element reads. Published for codegen; the wire type is the flat OpticalElementInput"""
    kind: Literal['OTHER'] = Field(default='OTHER')
    id: Optional[ID] = None
    label: str
    pose: Optional['Pose3DInput'] = None
    ports: Annotated[Optional[Tuple['LightPortInput', ...]], GraphQLDefault('[]')] = None
    'Default: []'
    manufacturer: Optional[str] = None
    model: Optional[str] = None
    serial_number: Optional[str] = Field(alias='serialNumber', default=None)
    description: Optional[str] = None

    def model_post_init(self, context):
        self.__pydantic_fields_set__.update({'kind'})
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class OtherSourceElementInput(BaseModel):
    """The fields an OTHER_SOURCE element reads. Published for codegen; the wire type is the flat OpticalElementInput"""
    kind: Literal['OTHER_SOURCE'] = Field(default='OTHER_SOURCE')
    id: Optional[ID] = None
    label: str
    pose: Optional['Pose3DInput'] = None
    ports: Annotated[Optional[Tuple['LightPortInput', ...]], GraphQLDefault('[]')] = None
    'Default: []'
    manufacturer: Optional[str] = None
    model: Optional[str] = None
    serial_number: Optional[str] = Field(alias='serialNumber', default=None)
    channel: Optional[ChannelKind] = None
    lamp_type: Optional[str] = Field(alias='lampType', default=None)

    def model_post_init(self, context):
        self.__pydantic_fields_set__.update({'kind'})
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class PinholeElementInput(BaseModel):
    """The fields a PINHOLE element reads. Published for codegen; the wire type is the flat OpticalElementInput"""
    kind: Literal['PINHOLE'] = Field(default='PINHOLE')
    id: Optional[ID] = None
    label: str
    pose: Optional['Pose3DInput'] = None
    ports: Annotated[Optional[Tuple['LightPortInput', ...]], GraphQLDefault('[]')] = None
    'Default: []'
    manufacturer: Optional[str] = None
    model: Optional[str] = None
    serial_number: Optional[str] = Field(alias='serialNumber', default=None)
    diameter: Optional[Length] = None

    def model_post_init(self, context):
        self.__pydantic_fields_set__.update({'kind'})
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class PolarizerElementInput(BaseModel):
    """The fields a POLARIZER element reads. Published for codegen; the wire type is the flat OpticalElementInput"""
    kind: Literal['POLARIZER'] = Field(default='POLARIZER')
    id: Optional[ID] = None
    label: str
    pose: Optional['Pose3DInput'] = None
    ports: Annotated[Optional[Tuple['LightPortInput', ...]], GraphQLDefault('[]')] = None
    'Default: []'
    manufacturer: Optional[str] = None
    model: Optional[str] = None
    serial_number: Optional[str] = Field(alias='serialNumber', default=None)
    angle_deg: Optional[float] = Field(alias='angleDeg', default=None)
    extinction_ratio: Optional[float] = Field(alias='extinctionRatio', default=None)

    def model_post_init(self, context):
        self.__pydantic_fields_set__.update({'kind'})
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class RotationTransformInput(BaseModel):
    """The fields a ROTATION member of TransformInput reads. Published for codegen; the wire type is the flat TransformInput"""
    kind: Literal['ROTATION'] = Field(default='ROTATION')
    affine: Tuple[Tuple[float, ...], ...]

    def model_post_init(self, context):
        self.__pydantic_fields_set__.update({'kind'})
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class SampleElementInput(BaseModel):
    """The fields a SAMPLE element reads. Published for codegen; the wire type is the flat OpticalElementInput"""
    kind: Literal['SAMPLE'] = Field(default='SAMPLE')
    id: Optional[ID] = None
    label: str
    pose: Optional['Pose3DInput'] = None
    ports: Annotated[Optional[Tuple['LightPortInput', ...]], GraphQLDefault('[]')] = None
    'Default: []'
    manufacturer: Optional[str] = None
    model: Optional[str] = None
    serial_number: Optional[str] = Field(alias='serialNumber', default=None)
    description: Optional[str] = None

    def model_post_init(self, context):
        self.__pydantic_fields_set__.update({'kind'})
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class ScaleTransformInput(BaseModel):
    """The fields a SCALE member of TransformInput reads. Published for codegen; the wire type is the flat TransformInput"""
    kind: Literal['SCALE'] = Field(default='SCALE')
    scale: Tuple[float, ...]

    def model_post_init(self, context):
        self.__pydantic_fields_set__.update({'kind'})
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class ShutterElementInput(BaseModel):
    """The fields a SHUTTER element reads. Published for codegen; the wire type is the flat OpticalElementInput"""
    kind: Literal['SHUTTER'] = Field(default='SHUTTER')
    id: Optional[ID] = None
    label: str
    pose: Optional['Pose3DInput'] = None
    ports: Annotated[Optional[Tuple['LightPortInput', ...]], GraphQLDefault('[]')] = None
    'Default: []'
    manufacturer: Optional[str] = None
    model: Optional[str] = None
    serial_number: Optional[str] = Field(alias='serialNumber', default=None)
    is_open: Optional[bool] = Field(alias='isOpen', default=None)
    shutter_type: Optional[str] = Field(alias='shutterType', default=None)
    gain: Optional[float] = None

    def model_post_init(self, context):
        self.__pydantic_fields_set__.update({'kind'})
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class TableDatasetDerivedFromInput(BaseModel):
    """The fields a TABLE_DATASET derivation reads. Published for codegen; the wire type is the flat DerivedFromInput"""
    kind: Literal['TABLE_DATASET'] = Field(default='TABLE_DATASET')
    transform: Optional['TransformInput'] = None
    value_relation: Optional[ValueRelation] = Field(alias='valueRelation', default=None)
    table_dataset: ID = Field(alias='tableDataset')

    def model_post_init(self, context):
        self.__pydantic_fields_set__.update({'kind'})
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class TranslationTransformInput(BaseModel):
    """The fields a TRANSLATION member of TransformInput reads. Published for codegen; the wire type is the flat TransformInput"""
    kind: Literal['TRANSLATION'] = Field(default='TRANSLATION')
    translation: Tuple[float, ...]

    def model_post_init(self, context):
        self.__pydantic_fields_set__.update({'kind'})
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class UnmappableTransformInput(BaseModel):
    """The fields an UNMAPPABLE member of TransformInput reads. Published for codegen; the wire type is the flat TransformInput"""
    kind: Literal['UNMAPPABLE'] = Field(default='UNMAPPABLE')
    reason: Optional[str] = None

    def model_post_init(self, context):
        self.__pydantic_fields_set__.update({'kind'})
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class WaveplateElementInput(BaseModel):
    """The fields a WAVEPLATE element reads. Published for codegen; the wire type is the flat OpticalElementInput"""
    kind: Literal['WAVEPLATE'] = Field(default='WAVEPLATE')
    id: Optional[ID] = None
    label: str
    pose: Optional['Pose3DInput'] = None
    ports: Annotated[Optional[Tuple['LightPortInput', ...]], GraphQLDefault('[]')] = None
    'Default: []'
    manufacturer: Optional[str] = None
    model: Optional[str] = None
    serial_number: Optional[str] = Field(alias='serialNumber', default=None)
    angle_deg: Optional[float] = Field(alias='angleDeg', default=None)
    retardance: Optional[float] = None
    design_wavelength: Optional[Length] = Field(alias='designWavelength', default=None)

    def model_post_init(self, context):
        self.__pydantic_fields_set__.update({'kind'})
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class ADatasetFilter(BaseModel):
    """No documentation"""
    ids: Optional[Tuple[ID, ...]] = Field(default=None, description='Filter by list of IDs')
    search: Optional[str] = Field(default=None, description='Search by name (case-insensitive substring)')
    created_before: Optional[datetime] = Field(alias='createdBefore', default=None, description='Filter for items created before this datetime')
    created_after: Optional[datetime] = Field(alias='createdAfter', default=None, description='Filter for items created after this datetime')
    owner: Optional[ID] = Field(default=None, description="Filter by the creator's subject ID")
    created_through_task: Optional[str] = Field(alias='createdThroughTask', default=None, description='Filter by the rekuest task id the item was created through')
    created_through: Optional[ID] = Field(alias='createdThrough', default=None, description='Filter by the database ID of the task the item was created through (the `createdThrough { id }` field)')
    assigned_by: Optional[ID] = Field(alias='assignedBy', default=None, description='Filter by the sub of the user that assigned the creating task')
    created_through_by: Optional[ID] = Field(alias='createdThroughBy', default=None, description='Filter by the database ID of the user that assigned the creating task (the `createdThroughBy { id }` field)')
    id: Optional[ID] = None
    name: Optional['StrFilterLookup'] = None
    description: Optional['StrFilterLookup'] = None
    and_: Optional['ADatasetFilter'] = Field(alias='AND', default=None)
    or_: Optional['ADatasetFilter'] = Field(alias='OR', default=None)
    not_: Optional['ADatasetFilter'] = Field(alias='NOT', default=None)
    distinct: Optional[bool] = Field(alias='DISTINCT', default=None)
    spec: Optional[Tuple[ADatasetSpec, ...]] = Field(default=None, description='Filter to datasets satisfying every one of these specs, e.g. [VOLUME, TIMESERIES] for 3D timelapses. Materialized from the axes of the intrinsic coordinate system at creation. A dataset carries one spatial spec (by how many SPACE axes it has) plus a modifier per acquisition axis present, so two spatial specs together match nothing')
    has_axis_types: Optional[Tuple[AxisType, ...]] = Field(alias='hasAxisTypes', default=None, description='Filter to datasets whose intrinsic coordinate system carries every one of these axis types, e.g. [TIME, CHANNEL]. The raw form of `spec`, for the types no spec names: COORDINATE, DISPLACEMENT, INDEX')
    multiscale: Optional[bool] = Field(default=None, description='Filter by whether the dataset carries a resolution pyramid: true for the multiscale ones, false for those with a single level')
    has_physical_space: Optional[bool] = Field(alias='hasPhysicalSpace', default=None, description="Filter by whether the dataset has an edge into a space with real units. False finds the data that is still only pixels, with no pixel size or stage pose recorded. Unrelated to a phasor histogram's `calibrated`, which is about reference correction")
    scene: Optional[ID] = Field(default=None, description="Filter to datasets rendered in this scene, through their lenses' layers. What is actually staged there -- for what merely could be, use `placeableIn`")
    placeable_in: Optional[ID] = Field(alias='placeableIn', default=None, description='Filter to datasets placeable into this coordinate system: those with a lens whose space has a traversable path into it, walking the transformation edges. Takes a *space*, not a scene, because that is all the answer depends on -- every scene over one world offers the same candidates. Pass `scene.worldCoordinateSystem.id` to ask it of a scene. What could be staged there -- for what already is, use `scene`')
    derived_from: Optional[ID] = Field(alias='derivedFrom', default=None, description='Filter to the datasets computed from this one -- the deconvolutions, segmentations and projections that named a space of it as their parent. Every child, not just the ones it places: a fusion that named it second is listed, and so is a child whose derivation is UNMAPPABLE, since it still came from here')
    not_derived: Optional[bool] = Field(alias='notDerived', default=None, description="Filter for datasets that were acquired rather than computed: true for the roots, those with no derivation edge into another dataset's space")
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class AffineTransformationViewFilter(BaseModel):
    """No documentation"""
    ids: Optional[Tuple[ID, ...]] = Field(default=None, description='Filter by list of IDs')
    is_global: Optional[bool] = Field(alias='isGlobal', default=None)
    image: Optional[ID] = Field(default=None, description='Filter by the image this view belongs to')
    images: Optional[Tuple[ID, ...]] = Field(default=None, description='Filter by a list of images this view belongs to')
    search: Optional[str] = Field(default=None, description='Search by the name of the image this view belongs to')
    id: Optional[ID] = None
    stage: Optional['StageFilter'] = None
    and_: Optional['AffineTransformationViewFilter'] = Field(alias='AND', default=None)
    or_: Optional['AffineTransformationViewFilter'] = Field(alias='OR', default=None)
    not_: Optional['AffineTransformationViewFilter'] = Field(alias='NOT', default=None)
    distinct: Optional[bool] = Field(alias='DISTINCT', default=None)
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class AnimationFilter(BaseModel):
    """No documentation"""
    ids: Optional[Tuple[ID, ...]] = Field(default=None, description='Filter by list of IDs')
    search: Optional[str] = Field(default=None, description='Search by name (case-insensitive substring)')
    created_before: Optional[datetime] = Field(alias='createdBefore', default=None, description='Filter for items created before this datetime')
    created_after: Optional[datetime] = Field(alias='createdAfter', default=None, description='Filter for items created after this datetime')
    owner: Optional[ID] = Field(default=None, description="Filter by the creator's subject ID")
    created_through_task: Optional[str] = Field(alias='createdThroughTask', default=None, description='Filter by the rekuest task id the item was created through')
    created_through: Optional[ID] = Field(alias='createdThrough', default=None, description='Filter by the database ID of the task the item was created through (the `createdThrough { id }` field)')
    assigned_by: Optional[ID] = Field(alias='assignedBy', default=None, description='Filter by the sub of the user that assigned the creating task')
    created_through_by: Optional[ID] = Field(alias='createdThroughBy', default=None, description='Filter by the database ID of the user that assigned the creating task (the `createdThroughBy { id }` field)')
    id: Optional[ID] = None
    name: Optional['StrFilterLookup'] = None
    and_: Optional['AnimationFilter'] = Field(alias='AND', default=None)
    or_: Optional['AnimationFilter'] = Field(alias='OR', default=None)
    not_: Optional['AnimationFilter'] = Field(alias='NOT', default=None)
    distinct: Optional[bool] = Field(alias='DISTINCT', default=None)
    scene: Optional[ID] = Field(default=None, description='Filter by the scene this tour flies through')
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class AnimationWaypointInput(BaseModel):
    """One camera pose in a tour, and how the viewer travels to it. Its position in the tour is its position in the `waypoints` list -- there is no order field to pass"""
    camera: 'CameraStateInput' = Field(description='Where the camera is at this stop')
    name: Optional[str] = Field(default=None, description='What this stop shows')
    duration_ms: Optional[int] = Field(alias='durationMs', default=None, description='How long the viewer takes to travel to this stop, in milliseconds')
    easing: Optional[Easing] = Field(default=None, description='How the viewer eases the camera along that travel')
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class AnnotationCollectionFilter(BaseModel):
    """No documentation"""
    ids: Optional[Tuple[ID, ...]] = Field(default=None, description='Filter by list of IDs')
    created_before: Optional[datetime] = Field(alias='createdBefore', default=None, description='Filter for items created before this datetime')
    created_after: Optional[datetime] = Field(alias='createdAfter', default=None, description='Filter for items created after this datetime')
    owner: Optional[ID] = Field(default=None, description="Filter by the creator's subject ID")
    id: Optional[ID] = None
    name: Optional['StrFilterLookup'] = None
    and_: Optional['AnnotationCollectionFilter'] = Field(alias='AND', default=None)
    or_: Optional['AnnotationCollectionFilter'] = Field(alias='OR', default=None)
    not_: Optional['AnnotationCollectionFilter'] = Field(alias='NOT', default=None)
    distinct: Optional[bool] = Field(alias='DISTINCT', default=None)
    scene: Optional[ID] = Field(default=None, description='Filter by the scene this collection was minted for as its default drawing surface')
    coordinate_system: Optional[ID] = Field(alias='coordinateSystem', default=None, description="Filter by the coordinate system the annotations are drawn in (the collection's own)")
    dataset: Optional[ID] = Field(default=None, description='Filter by the dataset the shapes are drawn over, following the derivation edge')
    search: Optional[str] = Field(default=None, description='Search by name (case-insensitive substring)')
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class AnnotationFilter(BaseModel):
    """No documentation"""
    ids: Optional[Tuple[ID, ...]] = Field(default=None, description='Filter by list of IDs')
    id: Optional[str] = None
    name: Optional['StrFilterLookup'] = None
    description: Optional['StrFilterLookup'] = None
    kind: Optional[RoiKindChoices] = None
    and_: Optional['AnnotationFilter'] = Field(alias='AND', default=None)
    or_: Optional['AnnotationFilter'] = Field(alias='OR', default=None)
    not_: Optional['AnnotationFilter'] = Field(alias='NOT', default=None)
    distinct: Optional[bool] = Field(alias='DISTINCT', default=None)
    collection: Optional[ID] = Field(default=None, description='Filter by the collection this annotation belongs to')
    coordinate_system: Optional[ID] = Field(alias='coordinateSystem', default=None, description="Filter by the coordinate system this annotation is drawn in (its collection's own)")
    dataset: Optional[ID] = Field(default=None, description="Filter by the dataset the annotations are drawn over, following the collection's derivation edge")
    search: Optional[str] = Field(default=None, description='Search by name (case-insensitive substring)')
    pinned_to: Optional[Tuple['CoordinateInput', ...]] = Field(alias='pinnedTo', default=None, description="Filter to annotations pinned to every one of these coordinates, e.g. [{name: 't', value: 3}]. GIN-backed containment on the stored coordinate dict; an annotation that spans a coordinate does not match a pin on it")
    intersects: Optional['BoundingBoxInput'] = Field(default=None, description='Filter to annotations whose intrinsic bounding box overlaps this box (GiST-backed). Only meaningful within one frame: pass `collection` or `coordinateSystem` alongside. A box of lower rank is zero-filled on the missing coordinates')
    contains_point: Optional[Tuple[float, ...]] = Field(alias='containsPoint', default=None, description='Filter to annotations whose intrinsic bounding box contains this point (GiST-backed). Only meaningful within one frame: pass `collection` or `coordinateSystem` alongside')
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class AnnotationSpecInput(BaseModel):
    """One shape of a bulk draw: the per-annotation subset of CreateAnnotationInput, without the collection/scene target"""
    kind: RoiKind
    vectors: Tuple[ThreeDVector, ...]
    stroke_color: Optional[Tuple[int, ...]] = Field(alias='strokeColor', default=None)
    fill_color: Optional[Tuple[int, ...]] = Field(alias='fillColor', default=None)
    name: Optional[str] = None
    description: Optional[str] = None
    coordinates: Optional[Tuple['CoordinateInput', ...]] = None
    stroke_width: Optional[float] = Field(alias='strokeWidth', default=None)
    filled: Optional[bool] = None
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class AxisAnchorInput(BaseModel):
    """Input type for an axis anchor, which pins one axis to one discrete position"""
    axis: str
    value: int
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class AxisInput(AxisInputTrait, BaseModel):
    """Input type for one structural axis of a dataset's pixel grid: its name and its semantic kind. Units and spacings do not belong here -- they belong to a physical space, a separate coordinate system plus one edge"""
    name: str
    type: AxisType
    long_name: Optional[str] = Field(alias='longName', default=None)
    description: Optional[str] = None
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class BeamStateInput(BaseModel):
    """State of the optical beam on a particular path segment."""
    wavelength: Optional[Length] = None
    power: Optional[Power] = None
    polarization: Optional[str] = None
    mode_hint: Optional[str] = Field(alias='modeHint', default=None)
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class BoundingBoxInput(BaseModel):
    """An axis-aligned box as a min and a max corner, in the coordinate order of the frame it is asked in"""
    min: Tuple[float, ...]
    max: Tuple[float, ...]
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class CameraInput(BaseModel):
    """Input for creating or ensuring a camera"""
    serial_number: str = Field(alias='serialNumber', description='The unique serial number of the camera')
    name: Optional[str] = Field(default=None, description='The name of the camera')
    model: Optional[str] = Field(default=None, description='The model of the camera')
    bit_depth: Optional[int] = Field(alias='bitDepth', default=None, description='The bit depth of the camera sensor')
    sensor_size_x: Optional[int] = Field(alias='sensorSizeX', default=None, description='The sensor size in x direction (pixels)')
    sensor_size_y: Optional[int] = Field(alias='sensorSizeY', default=None, description='The sensor size in y direction (pixels)')
    pixel_size_x: Optional[Length] = Field(alias='pixelSizeX', default=None, description="The physical pixel size in x direction (e.g. '6.5 µm')")
    pixel_size_y: Optional[Length] = Field(alias='pixelSizeY', default=None, description="The physical pixel size in y direction (e.g. '6.5 µm')")
    manufacturer: Optional[str] = Field(default=None, description='The manufacturer of the camera')
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class CameraStateInput(BaseModel):
    """Where a viewer's camera is in a scene, and how it is looking at it. Give the flat view, the volumetric view, or both -- one pose serves either, and `Scene.preferredView` picks which a viewer opens. Every number is read against the scene's world coordinate system, whose axes carry the units, so they are bare numbers here"""
    position: Any = Field(description="Where the camera is centred, keyed by the world's axis names. Keyed rather than a positional list because the world's axes are named and a tour through a timelapse moves in t as much as in z -- a list would silently depend on axis order. Axes the pose does not name are left wherever the viewer already had them.")
    cross_section_orientation: Optional[Tuple[float, ...]] = Field(alias='crossSectionOrientation', default=None, description="The flat view's orientation, as a quaternion. Null to leave it to the viewer.")
    cross_section_scale: Optional[float] = Field(alias='crossSectionScale', default=None, description="The flat view's zoom, in world units per screen pixel. Null to leave it to the viewer.")
    projection_orientation: Optional[Tuple[float, ...]] = Field(alias='projectionOrientation', default=None, description="The volumetric view's orientation, as a quaternion. Null to leave it to the viewer.")
    projection_scale: Optional[float] = Field(alias='projectionScale', default=None, description="The volumetric view's zoom, in world units per screen pixel. Null to leave it to the viewer.")
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class ChangeDatasetInput(BaseModel):
    """Input for changing an existing dataset's name or parent"""
    name: str = Field(description='The name of the dataset')
    parent: Optional[ID] = Field(default=None, description='The ID of the parent dataset to nest this dataset under')
    id: ID = Field(description='The ID of the dataset to change')
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class ClearCoordinateSystemInput(BaseModel):
    """Input for clearing a shared coordinate system: delete every registration INTO it in one call, keeping the space, its scenes, and its own claims into wider spaces"""
    id: ID = Field(description='The ID of the shared coordinate system to clear')
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class ClearSceneInput(BaseModel):
    """Input for clearing a scene: delete every layer, keep the scene and everything it composes over"""
    id: ID = Field(description='The ID of the scene to clear')
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class CoordinateAnchorInput(CoordinateAnchorInputTrait, BaseModel):
    """Input type for a coordinate anchor, which specifies a list of dimension anchors to anchor to"""
    axis_anchors: Tuple[AxisAnchorInput, ...] = Field(alias='axisAnchors')
    microscope: Optional['OptikitStateInput'] = None
    ome_metadata: Optional['OmeMetadataInput'] = Field(alias='omeMetadata', default=None)
    value_histogram: Optional['ValueHistogramInput'] = Field(alias='valueHistogram', default=None)
    label: Optional['LabelInput'] = None
    light_graph: Optional['LightpathGraphInput'] = Field(alias='lightGraph', default=None)
    phasor_histogram: Optional['PhasorHistogramInput'] = Field(alias='phasorHistogram', default=None)
    phasor_calibration: Optional['PhasorCalibrationInput'] = Field(alias='phasorCalibration', default=None)
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class CoordinateInput(BaseModel):
    """A discrete coordinate an annotation is pinned to, e.g. a timepoint or a channel"""
    name: str
    value: int
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class CoordinateSystemFilter(BaseModel):
    """No documentation"""
    ids: Optional[Tuple[ID, ...]] = Field(default=None, description='Filter by list of IDs')
    search: Optional[str] = Field(default=None, description='Search by name (case-insensitive substring)')
    created_before: Optional[datetime] = Field(alias='createdBefore', default=None, description='Filter for items created before this datetime')
    created_after: Optional[datetime] = Field(alias='createdAfter', default=None, description='Filter for items created after this datetime')
    owner: Optional[ID] = Field(default=None, description="Filter by the creator's subject ID")
    id: Optional[ID] = None
    name: Optional['StrFilterLookup'] = None
    and_: Optional['CoordinateSystemFilter'] = Field(alias='AND', default=None)
    or_: Optional['CoordinateSystemFilter'] = Field(alias='OR', default=None)
    not_: Optional['CoordinateSystemFilter'] = Field(alias='NOT', default=None)
    distinct: Optional[bool] = Field(alias='DISTINCT', default=None)
    uninhabited: Optional[bool] = Field(default=None, description='Filter to the spaces nothing lives in: pure reference frames, the worlds and atlases sources are registered into. False finds the spaces some data actually occupies')
    dataset: Optional[ID] = Field(default=None, description="Filter to the spaces this dataset's data lives in: its own grid, and the grids of its pyramid levels and lenses")
    scene: Optional[ID] = Field(default=None, description='Filter by a scene composing over this system as its world')
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class CreateADatasetInput(CreateADatasetTrait, BaseModel):
    """Input type for creating an array dataset. Its axes are structural (name and kind); physical units, if known, arrive afterwards through createCoordinateSystem with a registrations entry naming the dataset"""
    data: ArrayLike
    scales: Tuple['ScaleInput', ...]
    name: str
    axes: Tuple[AxisInput, ...]
    anchors: Optional[Tuple[CoordinateAnchorInput, ...]] = None
    derived_from: Optional[Tuple['DerivedFromInput', ...]] = Field(alias='derivedFrom', default=None)
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class CreateAnimationInput(BaseModel):
    """Input for creating a named camera tour of a scene. The waypoints are given in tour order and that order is what is stored -- a tour is authored as a whole, never a stop at a time"""
    scene: ID = Field(description='The ID of the scene this tour flies through')
    name: str = Field(description='The name of the tour')
    description: Optional[str] = Field(default=None, description='What the tour shows')
    waypoints: Tuple[AnimationWaypointInput, ...] = Field(description='The poses the viewer pans through, in tour order')
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class CreateAnnotationCollectionInput(BaseModel):
    """Input for creating an annotation collection. The collection gets a coordinate system of its own, and an edge relates it to the space the shapes are drawn over"""
    name: str
    description: Optional[str] = None
    axes: Tuple[AxisInput, ...]
    derived_from: Optional[Tuple['DerivedFromInput', ...]] = Field(alias='derivedFrom', default=None)
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class CreateAnnotationInput(BaseModel):
    """Input for drawing an annotation. Provide exactly one of `collection` (append to it) or `scene` (draw on the scene: its annotation collection is found, or minted on first use together with its coordinate system, its registration into the world, and its layer)"""
    kind: RoiKind
    vectors: Tuple[ThreeDVector, ...]
    stroke_color: Optional[Tuple[int, ...]] = Field(alias='strokeColor', default=None)
    fill_color: Optional[Tuple[int, ...]] = Field(alias='fillColor', default=None)
    collection: Optional[ID] = None
    scene: Optional[ID] = None
    name: Optional[str] = None
    description: Optional[str] = None
    coordinates: Optional[Tuple[CoordinateInput, ...]] = None
    stroke_width: Optional[float] = Field(alias='strokeWidth', default=None)
    filled: Optional[bool] = None
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class CreateAnnotationsInput(BaseModel):
    """Input for drawing many annotations in one call. Provide exactly one of `collection` or `scene` (same semantics as createAnnotation); the transform chain and version resolve once for the whole batch"""
    collection: Optional[ID] = None
    scene: Optional[ID] = None
    annotations: Tuple[AnnotationSpecInput, ...]
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class CreateCoordinateSystemInput(BaseModel):
    """Create a SHARED coordinate system -- a reference space with no owner, e.g. a world or an atlas -- and, in the same call, author the edges registering any number of sources (datasets, table datasets, mesh collections, coordinate systems) into it. Every other system is owned by a container and created with it, so a shared space is the only system created directly. createSceneFromCoordinateSystem later builds a scene over it and materializes those sources as layers"""
    name: str
    axes: Tuple['PhysicalAxisInput', ...]
    epoch: Optional[datetime] = None
    registrations: Annotated[Optional[Tuple['RegistrationPathInput', ...]], GraphQLDefault('[]')] = None
    'Default: []'
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class CreateDatasetInput(BaseModel):
    """Input for creating a new dataset to organize images and files"""
    name: str = Field(description='The name of the dataset')
    parent: Optional[ID] = Field(default=None, description='The ID of the parent dataset to nest this dataset under')
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class CreateLayerInput(BaseModel):
    """Input type for creating an image from an array-like object"""
    lens: ID
    scene: ID
    blending: Optional[Blending] = None
    opacity: Optional[float] = None
    visible: Optional[bool] = None
    order: Optional[int] = None
    render_graph: 'LayerRenderGraphInput' = Field(alias='renderGraph')
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class CreateLensInput(BaseModel):
    """Input type for creating an image from an array-like object"""
    dataset: ID
    slices: Tuple['SliceInput', ...]
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class CreateMeshCollectionInput(BaseModel):
    """Input for registering an immutable, versioned mesh collection. The collection gets a coordinate system of its own, and an edge relates it to the space the meshes were extracted from"""
    version: str
    spec_version: str = Field(alias='specVersion')
    catalog: ParquetLike
    geometry: Optional[Tuple[ParquetLike, ...]] = None
    axes: Tuple[AxisInput, ...]
    derived_from: Optional[Tuple['DerivedFromInput', ...]] = Field(alias='derivedFrom', default=None)
    grid: Optional[Any] = None
    encoding: Optional[Any] = None
    provenance_metadata: Optional[Any] = Field(alias='provenanceMetadata', default=None)
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class CreatePhasorCalibrationInput(BaseModel):
    """Attach an instrument-response correction to a dataset, taking a raw phasor to a calibrated one. Measured once per detector from a reference acquisition. Its absence is legitimate: an uncalibrated phasor still renders, its hue is just not traceable to an absolute lifetime"""
    axis: str = Field(description='The axis the correction applies to')
    harmonic: Optional[int] = Field(default=None, description='The harmonic the correction applies at')
    phase_offset: Optional[float] = Field(alias='phaseOffset', default=None, description='The phase correction in radians')
    modulation_factor: Optional[float] = Field(alias='modulationFactor', default=None, description='The modulation correction')
    reference: Optional[str] = Field(default=None, description='What the correction was measured against')
    dataset: ID = Field(description='The ID of the dataset the correction applies to')
    axis_anchors: Optional[Tuple[AxisAnchorInput, ...]] = Field(alias='axisAnchors', default=None, description='The coordinates the correction is pinned to')
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class CreatePhasorHistogramInput(BaseModel):
    """Attach a phasor distribution to a dataset: the 2D (g, s) density of a phasor taken over one axis at one harmonic. Computed after ingest by a task that reads the cube; recomputing at the same harmonic replaces it, while a second harmonic lands beside the first"""
    axis: str = Field(description='The axis the phasor was taken over')
    counts: Tuple[float, ...] = Field(description='The flattened bins x bins density')
    harmonic: Optional[int] = Field(default=None, description='The harmonic the phasor was taken at')
    bins: Optional[int] = Field(default=None, description='The resolution of the square (g, s) density grid')
    g_min: Optional[float] = Field(alias='gMin', default=None)
    g_max: Optional[float] = Field(alias='gMax', default=None)
    s_min: Optional[float] = Field(alias='sMin', default=None)
    s_max: Optional[float] = Field(alias='sMax', default=None)
    total: Optional[int] = None
    calibrated: Optional[bool] = None
    profile: Optional[Tuple[float, ...]] = None
    dataset: ID = Field(description='The ID of the dataset the phasor was computed from')
    axis_anchors: Optional[Tuple[AxisAnchorInput, ...]] = Field(alias='axisAnchors', default=None, description='The coordinates the distribution is pinned to')
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class CreatePhasorLayerInput(BaseModel):
    """Create a layer that reduces one axis of a lens to a phasor and colors each pixel by it -- a lifetime overlay over a FLIM cube, or a spectral one over a hyperspectral cube"""
    lens: ID
    scene: ID
    phasor_axis: Optional[str] = Field(alias='phasorAxis', default=None)
    intensity_axis: Optional[str] = Field(alias='intensityAxis', default=None)
    intensity_index: Annotated[Optional[int], GraphQLDefault('0')] = Field(alias='intensityIndex', default=None)
    'Default: 0'
    harmonic: Optional[int] = None
    transfer: Optional['PhasorTransferInput'] = None
    blending: Optional[Blending] = None
    opacity: Optional[float] = None
    visible: Optional[bool] = None
    order: Optional[int] = None
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class CreateRGBContextInput(BaseModel):
    """Input for creating an RGB render context for an image"""
    name: Optional[str] = Field(default=None, description='The name of the RGB context')
    thumbnail: Optional[ID] = Field(default=None, description='The ID of an uploaded media store to use as the thumbnail snapshot')
    image: ID = Field(description='The ID of the image this RGB context renders')
    views: Optional[Tuple['PartialRGBViewInput', ...]] = Field(default=None, description='The RGB views (channel rendering settings) to attach to the context')
    z: Optional[int] = Field(default=None, description='The z plane the context renders')
    t: Optional[int] = Field(default=None, description='The timepoint the context renders')
    c: Optional[int] = Field(default=None, description='The channel the context renders')
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class CreateSceneFromCoordinateSystemInput(BaseModel):
    """Bootstrap a renderable scene over an existing coordinate system. Over an ownerless SHARED space the sources already registered into it become layers, up to the policy's nchildren -- each source's path to world is the one registration createCoordinateSystem authored. Over an owned system (a dataset's intrinsic pixels, a physical space, a collection's space) the container's own data becomes the layer: it is in its own space by construction, so no edge exists or is authored. Rerunning makes another scene over the same space, which outlives them all"""
    coordinate_system: ID = Field(alias='coordinateSystem')
    name: Optional[str] = None
    policy: Annotated[Optional['ScenePolicyInput'], GraphQLDefault("{'nchildren': 8, 'transformTables': False, 'includeMeshes': True, 'kind': None}")] = None
    "Default: {'nchildren': 8, 'transformTables': False, 'includeMeshes': True, 'kind': None}"
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class CreateSceneInput(BaseModel):
    """Input type for creating a scene over a world coordinate system: an adopted existing system (a shared space, a dataset's intrinsic grid, a physical space), or one created for it"""
    name: str
    blending: Optional[Blending] = None
    preferred_view: Optional[PreferredView] = Field(alias='preferredView', default=None)
    background_color: Optional[Tuple[float, ...]] = Field(alias='backgroundColor', default=None)
    axes: Optional[Tuple['PhysicalAxisInput', ...]] = None
    epoch: Optional[datetime] = None
    coordinate_system: Optional[ID] = Field(alias='coordinateSystem', default=None)
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class CreateTableDatasetInput(BaseModel):
    """Input for creating a table dataset from a Parquet store. Its coordinate columns become the axes of a coordinate system it owns; declare no coordinate columns for a pure measurement table (its rows enumerate objects and its lineage edge is UNMAPPABLE)"""
    name: str
    data: ParquetLike
    columns: Annotated[Optional[Tuple['TableColumnInput', ...]], GraphQLDefault('[]')] = None
    'Default: []'
    description: Optional[str] = None
    derived_from: Optional[Tuple['DerivedFromInput', ...]] = Field(alias='derivedFrom', default=None)
    validate_schema: Annotated[Optional[bool], GraphQLDefault('False')] = Field(alias='validateSchema', default=None)
    'Default: False'
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class CreateTransformationInput(BaseModel):
    """Input for creating one edge of the coordinate graph, mapping an input coordinate system to an output one"""
    input: ID
    output: ID
    transform: 'TransformInput'
    name: Optional[str] = None
    validity: Optional[PlacementValidity] = None
    value_relation: Optional[ValueRelation] = Field(alias='valueRelation', default=None)
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class DatasetFilter(BaseModel):
    """No documentation"""
    ids: Optional[Tuple[ID, ...]] = Field(default=None, description='Filter by list of IDs')
    search: Optional[str] = Field(default=None, description='Search by name (full-text search)')
    created_before: Optional[datetime] = Field(alias='createdBefore', default=None, description='Filter for items created before this datetime')
    created_after: Optional[datetime] = Field(alias='createdAfter', default=None, description='Filter for items created after this datetime')
    owner: Optional[ID] = Field(default=None, description="Filter by the creator's subject ID")
    pinned: Optional[bool] = Field(default=None, description='Filter by whether the current user has pinned the item')
    tags: Optional[Tuple[str, ...]] = Field(default=None, description='Filter by tag names')
    created_through_task: Optional[str] = Field(alias='createdThroughTask', default=None, description='Filter by the rekuest task id the item was created through')
    created_through: Optional[ID] = Field(alias='createdThrough', default=None, description='Filter by the database ID of the task the item was created through (the `createdThrough { id }` field)')
    assigned_by: Optional[ID] = Field(alias='assignedBy', default=None, description='Filter by the sub of the user that assigned the creating task')
    created_through_by: Optional[ID] = Field(alias='createdThroughBy', default=None, description='Filter by the database ID of the user that assigned the creating task (the `createdThroughBy { id }` field)')
    id: Optional[ID] = None
    name: Optional['StrFilterLookup'] = None
    description: Optional['StrFilterLookup'] = None
    is_default: Optional[bool] = Field(alias='isDefault', default=None)
    and_: Optional['DatasetFilter'] = Field(alias='AND', default=None)
    or_: Optional['DatasetFilter'] = Field(alias='OR', default=None)
    not_: Optional['DatasetFilter'] = Field(alias='NOT', default=None)
    distinct: Optional[bool] = Field(alias='DISTINCT', default=None)
    parentless: Optional[bool] = Field(default=None, description='Filter for datasets with (true) or without (false) a parent')
    parent: Optional[ID] = Field(default=None, description='Filter by the parent dataset (list the children of a dataset)')
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class DeleteAnimationInput(BaseModel):
    """Input for deleting a camera tour by ID"""
    id: ID = Field(description='The ID of the tour to delete')
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class DeleteAnnotationCollectionInput(BaseModel):
    """Input for deleting an annotation collection by ID"""
    id: ID = Field(description='The ID of the annotation collection to delete')
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class DeleteAnnotationInput(BaseModel):
    """Input for deleting an annotation by ID"""
    id: ID
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class DeleteCoordinateSystemInput(BaseModel):
    """Input for deleting a shared coordinate system by ID"""
    id: ID = Field(description='The ID of the shared coordinate system to delete')
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class DeleteMeshCollectionInput(BaseModel):
    """Input for deleting a mesh collection by ID"""
    id: ID = Field(description='The ID of the mesh collection to delete')
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class DeleteRegistrationInput(BaseModel):
    """Input for un-registering a source from a shared space by naming the source and the space, not the edge. Provide exactly one source -- the same selector registering it took"""
    dataset: Optional[ID] = None
    table_dataset: Optional[ID] = Field(alias='tableDataset', default=None)
    mesh_collection: Optional[ID] = Field(alias='meshCollection', default=None)
    annotation_collection: Optional[ID] = Field(alias='annotationCollection', default=None)
    coordinate_system: Optional[ID] = Field(alias='coordinateSystem', default=None)
    world: ID = Field(description='The shared space the registration goes into')
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class DeleteRoiInput(BaseModel):
    """Input for deleting a ROI by ID"""
    id: ID = Field(description='The ID of the ROI to delete')
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class DeleteSceneInput(BaseModel):
    """Input for deleting a scene by ID"""
    id: ID = Field(description='The ID of the scene to delete')
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class DeleteSceneSnapshotInput(BaseModel):
    """Input for deleting a lens snapshot by ID"""
    id: ID = Field(description='The ID of the snapshot to delete')
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class DeleteTableDatasetInput(BaseModel):
    """Input for deleting a table dataset by ID"""
    id: ID = Field(description='The ID of the table dataset to delete')
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class DeleteTransformationInput(BaseModel):
    """Input for deleting a transformation by ID"""
    id: ID = Field(description='The ID of the transformation to delete')
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)
DerivedFromInput = Annotated[Union[AnnotationCollectionDerivedFromInput, CoordinateSystemDerivedFromInput, DatasetDerivedFromInput, LensDerivedFromInput, MeshCollectionDerivedFromInput, TableDatasetDerivedFromInput], Field(discriminator='kind')]

class DeviceStateInput(BaseModel):
    """One hardware device's recorded state: its identity in the setup plus its settings at this coordinate"""
    label: str = Field(description="The device's identity in the setup, e.g. 'filter-wheel-1'")
    kind: Optional[str] = Field(default=None, description="A free-form device kind, e.g. 'laser', 'filter-wheel'")
    settings: Annotated[Optional[Tuple['SettingInput', ...]], GraphQLDefault('[]')] = None
    'Default: []'
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class EraFilter(BaseModel):
    """No documentation"""
    ids: Optional[Tuple[ID, ...]] = Field(default=None, description='Filter by list of IDs')
    search: Optional[str] = Field(default=None, description='Search by name (case-insensitive substring)')
    created_before: Optional[datetime] = Field(alias='createdBefore', default=None, description='Filter for items created before this datetime')
    created_after: Optional[datetime] = Field(alias='createdAfter', default=None, description='Filter for items created after this datetime')
    owner: Optional[ID] = Field(default=None, description="Filter by the creator's subject ID")
    pinned: Optional[bool] = Field(default=None, description='Filter by whether the current user has pinned the item')
    created_through_task: Optional[str] = Field(alias='createdThroughTask', default=None, description='Filter by the rekuest task id the item was created through')
    created_through: Optional[ID] = Field(alias='createdThrough', default=None, description='Filter by the database ID of the task the item was created through (the `createdThrough { id }` field)')
    assigned_by: Optional[ID] = Field(alias='assignedBy', default=None, description='Filter by the sub of the user that assigned the creating task')
    created_through_by: Optional[ID] = Field(alias='createdThroughBy', default=None, description='Filter by the database ID of the user that assigned the creating task (the `createdThroughBy { id }` field)')
    id: Optional[ID] = None
    name: Optional['StrFilterLookup'] = None
    begin: Optional[datetime] = None
    end: Optional[datetime] = None
    and_: Optional['EraFilter'] = Field(alias='AND', default=None)
    or_: Optional['EraFilter'] = Field(alias='OR', default=None)
    not_: Optional['EraFilter'] = Field(alias='NOT', default=None)
    distinct: Optional[bool] = Field(alias='DISTINCT', default=None)
    instrument: Optional[ID] = Field(default=None, description='Filter by the instrument this era belongs to')
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class EraInput(BaseModel):
    """Input for creating an era, a time period to which timepoint views relate"""
    name: str = Field(description='The name of the era')
    begin: Optional[datetime] = Field(default=None, description='The datetime at which the era begins')
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
    valid: Annotated[Optional[bool], GraphQLDefault('True')] = None
    'Default: True'
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class FinishMediaUploadInput(BaseModel):
    """No documentation"""
    store_id: str = Field(alias='storeId')
    valid: Annotated[Optional[bool], GraphQLDefault('True')] = None
    'Default: True'
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class FinishParquetUploadInput(BaseModel):
    """No documentation"""
    store_id: str = Field(alias='storeId')
    valid: Annotated[Optional[bool], GraphQLDefault('True')] = None
    'Default: True'
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class FinishZarrUploadInput(BaseModel):
    """No documentation"""
    store_id: str = Field(alias='storeId')
    valid: Annotated[Optional[bool], GraphQLDefault('True')] = None
    'Default: True'
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class FromArrayLikeInput(BaseModel):
    """Input type for creating an image from an array-like object"""
    array: ImageLike = Field(description='The array-like object to create the image from')
    name: str = Field(description='The name of the image')
    dataset: Optional[ID] = Field(default=None, description='Optional dataset ID to associate the image with')
    channel_views: Optional[Tuple['PartialChannelViewInput', ...]] = Field(alias='channelViews', default=None, description='Optional list of channel views')
    transformation_views: Optional[Tuple['PartialAffineTransformationViewInput', ...]] = Field(alias='transformationViews', default=None, description='Optional list of affine transformation views')
    acquisition_views: Optional[Tuple['PartialAcquisitionViewInput', ...]] = Field(alias='acquisitionViews', default=None, description='Optional list of acquisition views')
    mask_views: Optional[Tuple['PartialMaskViewInput', ...]] = Field(alias='maskViews', default=None, description='Optional list of mask views')
    reference_views: Optional[Tuple['PartialReferenceViewInput', ...]] = Field(alias='referenceViews', default=None, description='Optional list of reference views')
    instance_mask_views: Optional[Tuple['PartialInstanceMaskViewInput', ...]] = Field(alias='instanceMaskViews', default=None, description='Optional list of instance mask views')
    rgb_views: Optional[Tuple['PartialRGBViewInput', ...]] = Field(alias='rgbViews', default=None, description='Optional list of RGB views')
    timepoint_views: Optional[Tuple['PartialTimepointViewInput', ...]] = Field(alias='timepointViews', default=None, description='Optional list of timepoint views')
    optics_views: Optional[Tuple['PartialOpticsViewInput', ...]] = Field(alias='opticsViews', default=None, description='Optional list of optics views')
    scale_views: Optional[Tuple['PartialScaleViewInput', ...]] = Field(alias='scaleViews', default=None, description='Optional list of scale views')
    tags: Optional[Tuple[str, ...]] = Field(default=None, description='Optional list of tags to associate with the image')
    roi_views: Optional[Tuple['PartialROIViewInput', ...]] = Field(alias='roiViews', default=None, description='Optional list of ROI views')
    file_views: Optional[Tuple['PartialFileViewInput', ...]] = Field(alias='fileViews', default=None, description='Optional list of file views')
    derived_views: Optional[Tuple['PartialDerivedViewInput', ...]] = Field(alias='derivedViews', default=None, description='Optional list of derived views')
    lightpath_views: Optional[Tuple['PartialLightpathViewInput', ...]] = Field(alias='lightpathViews', default=None, description='Optional list of lightpath views')
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class FromFileLike(BaseModel):
    """Input for creating a file record from an uploaded big-file store"""
    file: FileLike = Field(description='The uploaded big-file store to create the file from')
    file_name: str = Field(alias='fileName', description='The name of the file')
    dataset: Optional[ID] = Field(default=None, description='The ID of the dataset to put the file in (defaults to the current default dataset)')
    origins: Optional[Tuple[ID, ...]] = Field(default=None, description='The IDs of entities this file was derived from')
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class FromParquetLike(BaseModel):
    """Input for creating a table from an uploaded parquet store"""
    dataframe: ParquetLike = Field(description='The parquet dataframe to create the table from')
    name: str = Field(description='The name of the table')
    origins: Optional[Tuple[ID, ...]] = Field(default=None, description='The IDs of tables this table was derived from')
    dataset: Optional[ID] = Field(default=None, description='The dataset ID this table belongs to')
    label_accessors: Optional[Tuple['PartialLabelAccessorInput', ...]] = Field(alias='labelAccessors', default=None, description='Label accessors to create for this table')
    image_accessors: Optional[Tuple['PartialImageAccessorInput', ...]] = Field(alias='imageAccessors', default=None, description='Image accessors to create for this table')
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class HistogramViewInput(BaseModel):
    """Input for creating a histogram view on an existing image, referenced by ID"""
    collection: Optional[ID] = Field(default=None, description='The collection this view belongs to')
    z_min: Optional[int] = Field(alias='zMin', default=None, description='The minimum z coordinate of the view')
    z_max: Optional[int] = Field(alias='zMax', default=None, description='The maximum z coordinate of the view')
    x_min: Optional[int] = Field(alias='xMin', default=None, description='The minimum x coordinate of the view')
    x_max: Optional[int] = Field(alias='xMax', default=None, description='The maximum x coordinate of the view')
    y_min: Optional[int] = Field(alias='yMin', default=None, description='The minimum y coordinate of the view')
    y_max: Optional[int] = Field(alias='yMax', default=None, description='The maximum y coordinate of the view')
    t_min: Optional[int] = Field(alias='tMin', default=None, description='The minimum t coordinate of the view')
    t_max: Optional[int] = Field(alias='tMax', default=None, description='The maximum t coordinate of the view')
    c_min: Optional[int] = Field(alias='cMin', default=None, description='The minimum c (channel) coordinate of the view')
    c_max: Optional[int] = Field(alias='cMax', default=None, description='The maximum c (channel) coordinate of the view')
    histogram: Tuple[float, ...] = Field(description='The histogram of the image (y values)')
    bins: Tuple[float, ...] = Field(description='The bin indices of the histogram (x values)')
    min: float = Field(description='The minimum pixel value of the histogram')
    max: float = Field(description='The maximum pixel value of the histogram')
    image: ID = Field(description='The ID of the image this view is for')
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class ImageFilter(BaseModel):
    """No documentation"""
    ids: Optional[Tuple[ID, ...]] = Field(default=None, description='Filter by list of IDs')
    search: Optional[str] = Field(default=None, description='Search by name (full-text search)')
    created_before: Optional[datetime] = Field(alias='createdBefore', default=None, description='Filter for items created before this datetime')
    created_after: Optional[datetime] = Field(alias='createdAfter', default=None, description='Filter for items created after this datetime')
    owner: Optional[ID] = Field(default=None, description="Filter by the creator's subject ID")
    pinned: Optional[bool] = Field(default=None, description='Filter by whether the current user has pinned the item')
    tags: Optional[Tuple[str, ...]] = Field(default=None, description='Filter by tag names')
    created_through_task: Optional[str] = Field(alias='createdThroughTask', default=None, description='Filter by the rekuest task id the item was created through')
    created_through: Optional[ID] = Field(alias='createdThrough', default=None, description='Filter by the database ID of the task the item was created through (the `createdThrough { id }` field)')
    assigned_by: Optional[ID] = Field(alias='assignedBy', default=None, description='Filter by the sub of the user that assigned the creating task')
    created_through_by: Optional[ID] = Field(alias='createdThroughBy', default=None, description='Filter by the database ID of the user that assigned the creating task (the `createdThroughBy { id }` field)')
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
    datasets: Optional[Tuple[ID, ...]] = Field(default=None, description='Filter by a list of dataset IDs')
    not_derived: Optional[bool] = Field(alias='notDerived', default=None, description='Filter for images that are not derived from another image')
    has_rois: Optional[bool] = Field(alias='hasRois', default=None, description='Filter for images that have (or have no) ROIs')
    file: Optional[ID] = Field(default=None, description='Filter for images converted from this file (through their file views)')
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class InstanceMaskViewInput(BaseModel):
    """Input for creating an instance mask view on an existing image, referenced by ID"""
    collection: Optional[ID] = Field(default=None, description='The collection this view belongs to')
    z_min: Optional[int] = Field(alias='zMin', default=None, description='The minimum z coordinate of the view')
    z_max: Optional[int] = Field(alias='zMax', default=None, description='The maximum z coordinate of the view')
    x_min: Optional[int] = Field(alias='xMin', default=None, description='The minimum x coordinate of the view')
    x_max: Optional[int] = Field(alias='xMax', default=None, description='The maximum x coordinate of the view')
    y_min: Optional[int] = Field(alias='yMin', default=None, description='The minimum y coordinate of the view')
    y_max: Optional[int] = Field(alias='yMax', default=None, description='The maximum y coordinate of the view')
    t_min: Optional[int] = Field(alias='tMin', default=None, description='The minimum t coordinate of the view')
    t_max: Optional[int] = Field(alias='tMax', default=None, description='The maximum t coordinate of the view')
    c_min: Optional[int] = Field(alias='cMin', default=None, description='The minimum c (channel) coordinate of the view')
    c_max: Optional[int] = Field(alias='cMax', default=None, description='The maximum c (channel) coordinate of the view')
    reference_view: Optional[ID] = Field(alias='referenceView', default=None, description='The ID of the view that is masked by this instance mask')
    labels: Optional[LabelsLike] = Field(default=None, description='The instance labels of the mask and their corresponding colors')
    image: ID = Field(description='The ID of the image this view is for')
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class InstrumentInput(BaseModel):
    """Input for creating or ensuring a microscope instrument"""
    serial_number: str = Field(alias='serialNumber', description='The unique serial number of the instrument')
    manufacturer: Optional[str] = Field(default=None, description='The manufacturer of the instrument')
    name: Optional[str] = Field(default=None, description='The name of the instrument')
    model: Optional[str] = Field(default=None, description='The model of the instrument')
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

class LayerNodeInput(BaseModel):
    """A node in a layer's internal render graph. A 'channel' node carries an intensity source and transfer function; a 'phasor' node reduces an axis to a phasor and colors the pixel by it; a 'blend' node composites its children; a 'projection' node projects theirs over z."""
    kind: str
    label: Optional[str] = None
    intensity_axis: Optional[str] = Field(alias='intensityAxis', default=None)
    intensity_index: Optional[int] = Field(alias='intensityIndex', default=None)
    visible: Optional[bool] = None
    transfer: Optional['TransferFunctionInput'] = None
    blending: Optional[Blending] = None
    mode: Optional[ProjectionMode] = None
    phasor_axis: Optional[str] = Field(alias='phasorAxis', default=None)
    harmonic: Optional[int] = None
    phasor_transfer: Optional['PhasorTransferInput'] = Field(alias='phasorTransfer', default=None)
    children: Optional[Tuple['LayerNodeInput', ...]] = None
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class LayerRenderGraphInput(BaseModel):
    """The composable render recipe inside a single layer, rooted at a blend node"""
    root: LayerNodeInput
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class LightEdgeInput(BaseModel):
    """Input for connecting two optical ports."""
    id: str
    source_element_id: ID = Field(alias='sourceElementId')
    source_port_id: ID = Field(alias='sourcePortId')
    target_element_id: ID = Field(alias='targetElementId')
    target_port_id: ID = Field(alias='targetPortId')
    path_length: Optional[Length] = Field(alias='pathLength', default=None)
    medium: Annotated[Optional[str], GraphQLDefault('AIR')] = None
    'Default: AIR'
    loss_db: Annotated[Optional[float], GraphQLDefault('0.0')] = Field(alias='lossDb', default=None)
    'Default: 0.0'
    beam: Optional[BeamStateInput] = None
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class LightPortInput(BaseModel):
    """Input definition for an optical port on an element."""
    id: ID
    name: str
    role: PortRole
    channel: Annotated[Optional[ChannelKind], GraphQLDefault('FREE_SPACE')] = None
    'Default: FREE_SPACE'
    spectrum: Optional['SpectrumInput'] = None
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class LightpathGraphInput(BaseModel):
    """Bulk input for a full lightpath graph, including elements and edges."""
    elements: Tuple['OpticalElementInput', ...]
    edges: Tuple[LightEdgeInput, ...]
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class MaskViewInput(BaseModel):
    """Input for creating a mask view on an existing image, referenced by ID"""
    collection: Optional[ID] = Field(default=None, description='The collection this view belongs to')
    z_min: Optional[int] = Field(alias='zMin', default=None, description='The minimum z coordinate of the view')
    z_max: Optional[int] = Field(alias='zMax', default=None, description='The maximum z coordinate of the view')
    x_min: Optional[int] = Field(alias='xMin', default=None, description='The minimum x coordinate of the view')
    x_max: Optional[int] = Field(alias='xMax', default=None, description='The maximum x coordinate of the view')
    y_min: Optional[int] = Field(alias='yMin', default=None, description='The minimum y coordinate of the view')
    y_max: Optional[int] = Field(alias='yMax', default=None, description='The maximum y coordinate of the view')
    t_min: Optional[int] = Field(alias='tMin', default=None, description='The minimum t coordinate of the view')
    t_max: Optional[int] = Field(alias='tMax', default=None, description='The maximum t coordinate of the view')
    c_min: Optional[int] = Field(alias='cMin', default=None, description='The minimum c (channel) coordinate of the view')
    c_max: Optional[int] = Field(alias='cMax', default=None, description='The maximum c (channel) coordinate of the view')
    reference_view: Optional[ID] = Field(alias='referenceView', default=None, description='The ID of the view that is masked by this mask')
    labels: Optional[LabelsLike] = Field(default=None, description='The labels of the mask and their corresponding colors')
    image: ID = Field(description='The ID of the image this view is for')
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class MeshCollectionFilter(BaseModel):
    """No documentation"""
    ids: Optional[Tuple[ID, ...]] = Field(default=None, description='Filter by list of IDs')
    created_before: Optional[datetime] = Field(alias='createdBefore', default=None, description='Filter for items created before this datetime')
    created_after: Optional[datetime] = Field(alias='createdAfter', default=None, description='Filter for items created after this datetime')
    owner: Optional[ID] = Field(default=None, description="Filter by the creator's subject ID")
    id: Optional[ID] = None
    version: Optional['StrFilterLookup'] = None
    and_: Optional['MeshCollectionFilter'] = Field(alias='AND', default=None)
    or_: Optional['MeshCollectionFilter'] = Field(alias='OR', default=None)
    not_: Optional['MeshCollectionFilter'] = Field(alias='NOT', default=None)
    distinct: Optional[bool] = Field(alias='DISTINCT', default=None)
    coordinate_system: Optional[ID] = Field(alias='coordinateSystem', default=None, description="Filter by the coordinate system the mesh geometry is expressed in (the collection's own)")
    dataset: Optional[ID] = Field(default=None, description='Filter by the dataset the meshes were extracted from, following the derivation edge')
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class ObjectiveInput(BaseModel):
    """Input for creating or ensuring a microscope objective"""
    serial_number: str = Field(alias='serialNumber', description='The unique serial number of the objective')
    name: Optional[str] = Field(default=None, description='The name of the objective')
    na: Optional[float] = Field(default=None, description='The numerical aperture of the objective')
    magnification: Optional[float] = Field(default=None, description='The magnification of the objective')
    immersion: Optional[str] = Field(default=None, description='The immersion medium of the objective (e.g. oil, water, air)')
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class OffsetPaginationInput(BaseModel):
    """No documentation"""
    offset: Annotated[Optional[int], GraphQLDefault('0')] = None
    'Default: 0'
    limit: Optional[int] = None
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class OmeMetadataInput(BaseModel):
    """Input type for OME metadata"""
    metadata_string: str = Field(alias='metadataString', description='The OME metadata as a JSON string')
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)
OpticalElementInput = Annotated[Union[ApertureElementInput, BeamSplitterElementInput, CCDElementInput, DetectorElementInput, FilterElementInput, LampElementInput, LaserElementInput, LensElementInput, MirrorElementInput, ObjectiveElementInput, OtherElementInput, OtherSourceElementInput, PinholeElementInput, PolarizerElementInput, SampleElementInput, ShutterElementInput, WaveplateElementInput], Field(discriminator='kind')]

class OptikitStateInput(BaseModel):
    """The recorded microscope (Optikit) state: the hardware truth at the moment of acquisition. The common facts (stage, environment) are first-class and quantity-typed; everything else is per-device named settings"""
    stage: Optional['StageStateInput'] = None
    temperature: Optional[Temperature] = None
    devices: Annotated[Optional[Tuple[DeviceStateInput, ...]], GraphQLDefault('[]')] = None
    'Default: []'
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class PartialAcquisitionViewInput(BaseModel):
    """Input for creating an acquisition view (when and by whom the image was acquired) as part of creating an image; the image is taken from the surrounding input"""
    collection: Optional[ID] = Field(default=None, description='The collection this view belongs to')
    z_min: Optional[int] = Field(alias='zMin', default=None, description='The minimum z coordinate of the view')
    z_max: Optional[int] = Field(alias='zMax', default=None, description='The maximum z coordinate of the view')
    x_min: Optional[int] = Field(alias='xMin', default=None, description='The minimum x coordinate of the view')
    x_max: Optional[int] = Field(alias='xMax', default=None, description='The maximum x coordinate of the view')
    y_min: Optional[int] = Field(alias='yMin', default=None, description='The minimum y coordinate of the view')
    y_max: Optional[int] = Field(alias='yMax', default=None, description='The maximum y coordinate of the view')
    t_min: Optional[int] = Field(alias='tMin', default=None, description='The minimum t coordinate of the view')
    t_max: Optional[int] = Field(alias='tMax', default=None, description='The maximum t coordinate of the view')
    c_min: Optional[int] = Field(alias='cMin', default=None, description='The minimum c (channel) coordinate of the view')
    c_max: Optional[int] = Field(alias='cMax', default=None, description='The maximum c (channel) coordinate of the view')
    description: Optional[str] = Field(default=None, description='A cleartext description of the image acquisition')
    acquired_at: Optional[datetime] = Field(alias='acquiredAt', default=None, description='The time the image was acquired')
    operator: Optional[ID] = Field(default=None, description='The ID of the user that acquired the image')
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class PartialAffineTransformationViewInput(BaseModel):
    """Input for creating an affine transformation view (mapping the image onto a stage) as part of creating an image; the image is taken from the surrounding input"""
    collection: Optional[ID] = Field(default=None, description='The collection this view belongs to')
    z_min: Optional[int] = Field(alias='zMin', default=None, description='The minimum z coordinate of the view')
    z_max: Optional[int] = Field(alias='zMax', default=None, description='The maximum z coordinate of the view')
    x_min: Optional[int] = Field(alias='xMin', default=None, description='The minimum x coordinate of the view')
    x_max: Optional[int] = Field(alias='xMax', default=None, description='The maximum x coordinate of the view')
    y_min: Optional[int] = Field(alias='yMin', default=None, description='The minimum y coordinate of the view')
    y_max: Optional[int] = Field(alias='yMax', default=None, description='The maximum y coordinate of the view')
    t_min: Optional[int] = Field(alias='tMin', default=None, description='The minimum t coordinate of the view')
    t_max: Optional[int] = Field(alias='tMax', default=None, description='The maximum t coordinate of the view')
    c_min: Optional[int] = Field(alias='cMin', default=None, description='The minimum c (channel) coordinate of the view')
    c_max: Optional[int] = Field(alias='cMax', default=None, description='The maximum c (channel) coordinate of the view')
    stage: Optional[ID] = Field(default=None, description='The ID of the stage this transformation maps the image onto')
    affine_matrix: FourByFourMatrix = Field(alias='affineMatrix', description='The 4x4 affine matrix mapping image coordinates to stage coordinates')
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class PartialChannelViewInput(BaseModel):
    """Input for creating a channel view (channel metadata such as name and wavelengths) as part of creating an image; the image is taken from the surrounding input"""
    collection: Optional[ID] = Field(default=None, description='The collection this view belongs to')
    z_min: Optional[int] = Field(alias='zMin', default=None, description='The minimum z coordinate of the view')
    z_max: Optional[int] = Field(alias='zMax', default=None, description='The maximum z coordinate of the view')
    x_min: Optional[int] = Field(alias='xMin', default=None, description='The minimum x coordinate of the view')
    x_max: Optional[int] = Field(alias='xMax', default=None, description='The maximum x coordinate of the view')
    y_min: Optional[int] = Field(alias='yMin', default=None, description='The minimum y coordinate of the view')
    y_max: Optional[int] = Field(alias='yMax', default=None, description='The maximum y coordinate of the view')
    t_min: Optional[int] = Field(alias='tMin', default=None, description='The minimum t coordinate of the view')
    t_max: Optional[int] = Field(alias='tMax', default=None, description='The maximum t coordinate of the view')
    c_min: Optional[int] = Field(alias='cMin', default=None, description='The minimum c (channel) coordinate of the view')
    c_max: Optional[int] = Field(alias='cMax', default=None, description='The maximum c (channel) coordinate of the view')
    emission_wavelength: Optional[Length] = Field(alias='emissionWavelength', default=None, description="The emission wavelength of the channel (e.g. '509 nm')")
    excitation_wavelength: Optional[Length] = Field(alias='excitationWavelength', default=None, description="The excitation wavelength of the channel (e.g. '488 nm')")
    acquisition_mode: Optional[str] = Field(alias='acquisitionMode', default=None, description='The acquisition mode of the channel')
    name: Optional[str] = Field(default=None, description='The name of the channel')
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class PartialDerivedViewInput(BaseModel):
    """Input for creating a derived view (recording the image this image was derived from) as part of creating an image; the image is taken from the surrounding input"""
    collection: Optional[ID] = Field(default=None, description='The collection this view belongs to')
    z_min: Optional[int] = Field(alias='zMin', default=None, description='The minimum z coordinate of the view')
    z_max: Optional[int] = Field(alias='zMax', default=None, description='The maximum z coordinate of the view')
    x_min: Optional[int] = Field(alias='xMin', default=None, description='The minimum x coordinate of the view')
    x_max: Optional[int] = Field(alias='xMax', default=None, description='The maximum x coordinate of the view')
    y_min: Optional[int] = Field(alias='yMin', default=None, description='The minimum y coordinate of the view')
    y_max: Optional[int] = Field(alias='yMax', default=None, description='The maximum y coordinate of the view')
    t_min: Optional[int] = Field(alias='tMin', default=None, description='The minimum t coordinate of the view')
    t_max: Optional[int] = Field(alias='tMax', default=None, description='The maximum t coordinate of the view')
    c_min: Optional[int] = Field(alias='cMin', default=None, description='The minimum c (channel) coordinate of the view')
    c_max: Optional[int] = Field(alias='cMax', default=None, description='The maximum c (channel) coordinate of the view')
    origin_image: ID = Field(alias='originImage', description='The ID of the image this image was derived from')
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class PartialFileViewInput(BaseModel):
    """Input for creating a file view (linking the image region to the originating file) as part of creating an image; the image is taken from the surrounding input"""
    collection: Optional[ID] = Field(default=None, description='The collection this view belongs to')
    z_min: Optional[int] = Field(alias='zMin', default=None, description='The minimum z coordinate of the view')
    z_max: Optional[int] = Field(alias='zMax', default=None, description='The maximum z coordinate of the view')
    x_min: Optional[int] = Field(alias='xMin', default=None, description='The minimum x coordinate of the view')
    x_max: Optional[int] = Field(alias='xMax', default=None, description='The maximum x coordinate of the view')
    y_min: Optional[int] = Field(alias='yMin', default=None, description='The minimum y coordinate of the view')
    y_max: Optional[int] = Field(alias='yMax', default=None, description='The maximum y coordinate of the view')
    t_min: Optional[int] = Field(alias='tMin', default=None, description='The minimum t coordinate of the view')
    t_max: Optional[int] = Field(alias='tMax', default=None, description='The maximum t coordinate of the view')
    c_min: Optional[int] = Field(alias='cMin', default=None, description='The minimum c (channel) coordinate of the view')
    c_max: Optional[int] = Field(alias='cMax', default=None, description='The maximum c (channel) coordinate of the view')
    file: ID = Field(description='The ID of the file this view represents')
    series_identifier: Optional[str] = Field(alias='seriesIdentifier', default=None, description='The series identifier of the file')
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class PartialImageAccessorInput(BaseModel):
    """Input for an image accessor on a table, linking columns to an image (without the table reference)"""
    keys: Tuple[str, ...] = Field(description='The column keys of the table this accessor refers to')
    min_index: Optional[int] = Field(alias='minIndex', default=None, description='The minimum row index this accessor applies to')
    max_index: Optional[int] = Field(alias='maxIndex', default=None, description='The maximum row index this accessor applies to')
    image: ID = Field(description='The ID of the image the accessor values refer to')
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class PartialInstanceMaskViewInput(BaseModel):
    """Input for creating an instance mask view (an instance mask of another image) as part of creating an image; the image is taken from the surrounding input"""
    collection: Optional[ID] = Field(default=None, description='The collection this view belongs to')
    z_min: Optional[int] = Field(alias='zMin', default=None, description='The minimum z coordinate of the view')
    z_max: Optional[int] = Field(alias='zMax', default=None, description='The maximum z coordinate of the view')
    x_min: Optional[int] = Field(alias='xMin', default=None, description='The minimum x coordinate of the view')
    x_max: Optional[int] = Field(alias='xMax', default=None, description='The maximum x coordinate of the view')
    y_min: Optional[int] = Field(alias='yMin', default=None, description='The minimum y coordinate of the view')
    y_max: Optional[int] = Field(alias='yMax', default=None, description='The maximum y coordinate of the view')
    t_min: Optional[int] = Field(alias='tMin', default=None, description='The minimum t coordinate of the view')
    t_max: Optional[int] = Field(alias='tMax', default=None, description='The maximum t coordinate of the view')
    c_min: Optional[int] = Field(alias='cMin', default=None, description='The minimum c (channel) coordinate of the view')
    c_max: Optional[int] = Field(alias='cMax', default=None, description='The maximum c (channel) coordinate of the view')
    reference_view: Optional[ID] = Field(alias='referenceView', default=None, description='The ID of the view that is masked by this instance mask')
    labels: Optional[LabelsLike] = Field(default=None, description='The instance labels of the mask and their corresponding colors')
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class PartialLabelAccessorInput(BaseModel):
    """Input for a label accessor on a table, linking columns to a pixel view (without the table reference)"""
    keys: Tuple[str, ...] = Field(description='The column keys of the table this accessor refers to')
    min_index: Optional[int] = Field(alias='minIndex', default=None, description='The minimum row index this accessor applies to')
    max_index: Optional[int] = Field(alias='maxIndex', default=None, description='The maximum row index this accessor applies to')
    pixel_view: ID = Field(alias='pixelView', description='The ID of the pixel view the label values refer to')
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class PartialLightpathViewInput(BaseModel):
    """Input for creating a lightpath view (the optical path of the instrument) as part of creating an image; the image is taken from the surrounding input"""
    collection: Optional[ID] = Field(default=None, description='The collection this view belongs to')
    z_min: Optional[int] = Field(alias='zMin', default=None, description='The minimum z coordinate of the view')
    z_max: Optional[int] = Field(alias='zMax', default=None, description='The maximum z coordinate of the view')
    x_min: Optional[int] = Field(alias='xMin', default=None, description='The minimum x coordinate of the view')
    x_max: Optional[int] = Field(alias='xMax', default=None, description='The maximum x coordinate of the view')
    y_min: Optional[int] = Field(alias='yMin', default=None, description='The minimum y coordinate of the view')
    y_max: Optional[int] = Field(alias='yMax', default=None, description='The maximum y coordinate of the view')
    t_min: Optional[int] = Field(alias='tMin', default=None, description='The minimum t coordinate of the view')
    t_max: Optional[int] = Field(alias='tMax', default=None, description='The maximum t coordinate of the view')
    c_min: Optional[int] = Field(alias='cMin', default=None, description='The minimum c (channel) coordinate of the view')
    c_max: Optional[int] = Field(alias='cMax', default=None, description='The maximum c (channel) coordinate of the view')
    graph: LightpathGraphInput = Field(description='The lightpath graph of the instrument')
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class PartialMaskViewInput(BaseModel):
    """Input for creating a mask view (a label mask of another image) as part of creating an image; the image is taken from the surrounding input"""
    collection: Optional[ID] = Field(default=None, description='The collection this view belongs to')
    z_min: Optional[int] = Field(alias='zMin', default=None, description='The minimum z coordinate of the view')
    z_max: Optional[int] = Field(alias='zMax', default=None, description='The maximum z coordinate of the view')
    x_min: Optional[int] = Field(alias='xMin', default=None, description='The minimum x coordinate of the view')
    x_max: Optional[int] = Field(alias='xMax', default=None, description='The maximum x coordinate of the view')
    y_min: Optional[int] = Field(alias='yMin', default=None, description='The minimum y coordinate of the view')
    y_max: Optional[int] = Field(alias='yMax', default=None, description='The maximum y coordinate of the view')
    t_min: Optional[int] = Field(alias='tMin', default=None, description='The minimum t coordinate of the view')
    t_max: Optional[int] = Field(alias='tMax', default=None, description='The maximum t coordinate of the view')
    c_min: Optional[int] = Field(alias='cMin', default=None, description='The minimum c (channel) coordinate of the view')
    c_max: Optional[int] = Field(alias='cMax', default=None, description='The maximum c (channel) coordinate of the view')
    reference_view: Optional[ID] = Field(alias='referenceView', default=None, description='The ID of the view that is masked by this mask')
    labels: Optional[LabelsLike] = Field(default=None, description='The labels of the mask and their corresponding colors')
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class PartialOpticsViewInput(BaseModel):
    """Input for creating an optics view (instrument, objective and camera used) as part of creating an image; the image is taken from the surrounding input"""
    collection: Optional[ID] = Field(default=None, description='The collection this view belongs to')
    z_min: Optional[int] = Field(alias='zMin', default=None, description='The minimum z coordinate of the view')
    z_max: Optional[int] = Field(alias='zMax', default=None, description='The maximum z coordinate of the view')
    x_min: Optional[int] = Field(alias='xMin', default=None, description='The minimum x coordinate of the view')
    x_max: Optional[int] = Field(alias='xMax', default=None, description='The maximum x coordinate of the view')
    y_min: Optional[int] = Field(alias='yMin', default=None, description='The minimum y coordinate of the view')
    y_max: Optional[int] = Field(alias='yMax', default=None, description='The maximum y coordinate of the view')
    t_min: Optional[int] = Field(alias='tMin', default=None, description='The minimum t coordinate of the view')
    t_max: Optional[int] = Field(alias='tMax', default=None, description='The maximum t coordinate of the view')
    c_min: Optional[int] = Field(alias='cMin', default=None, description='The minimum c (channel) coordinate of the view')
    c_max: Optional[int] = Field(alias='cMax', default=None, description='The maximum c (channel) coordinate of the view')
    instrument: Optional[ID] = Field(default=None, description='The ID of the instrument used to acquire the image')
    objective: Optional[ID] = Field(default=None, description='The ID of the objective used to acquire the image')
    camera: Optional[ID] = Field(default=None, description='The ID of the camera used to acquire the image')
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class PartialRGBViewInput(BaseModel):
    """Input for creating an RGB render view (how a channel is rendered in an RGB context) as part of creating an image; the image is taken from the surrounding input"""
    collection: Optional[ID] = Field(default=None, description='The collection this view belongs to')
    z_min: Optional[int] = Field(alias='zMin', default=None, description='The minimum z coordinate of the view')
    z_max: Optional[int] = Field(alias='zMax', default=None, description='The maximum z coordinate of the view')
    x_min: Optional[int] = Field(alias='xMin', default=None, description='The minimum x coordinate of the view')
    x_max: Optional[int] = Field(alias='xMax', default=None, description='The maximum x coordinate of the view')
    y_min: Optional[int] = Field(alias='yMin', default=None, description='The minimum y coordinate of the view')
    y_max: Optional[int] = Field(alias='yMax', default=None, description='The maximum y coordinate of the view')
    t_min: Optional[int] = Field(alias='tMin', default=None, description='The minimum t coordinate of the view')
    t_max: Optional[int] = Field(alias='tMax', default=None, description='The maximum t coordinate of the view')
    c_min: Optional[int] = Field(alias='cMin', default=None, description='The minimum c (channel) coordinate of the view')
    c_max: Optional[int] = Field(alias='cMax', default=None, description='The maximum c (channel) coordinate of the view')
    context: Optional[ID] = Field(default=None, description='The ID of the RGB render context this view belongs to')
    gamma: Optional[float] = Field(default=None, description='The gamma correction applied to the channel')
    contrast_limit_min: Optional[float] = Field(alias='contrastLimitMin', default=None, description='The minimum contrast limit of the channel')
    contrast_limit_max: Optional[float] = Field(alias='contrastLimitMax', default=None, description='The maximum contrast limit of the channel')
    rescale: Optional[bool] = Field(default=None, description='Whether to rescale the channel data to the contrast limits')
    scale: Optional[float] = Field(default=None, description='The scale factor applied to the channel when rendering')
    active: Optional[bool] = Field(default=None, description='Whether the view is active')
    color_map: Optional[ColorMap] = Field(alias='colorMap', default=None, description='The color map applied to the channel')
    base_color: Optional[Tuple[float, ...]] = Field(alias='baseColor', default=None, description='The base color of the channel as RGBA values (if using a mapped scaler)')
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class PartialROIViewInput(BaseModel):
    """Input for creating a ROI view (marking the image as a cutout of a parent image's ROI) as part of creating an image; the image is taken from the surrounding input"""
    collection: Optional[ID] = Field(default=None, description='The collection this view belongs to')
    z_min: Optional[int] = Field(alias='zMin', default=None, description='The minimum z coordinate of the view')
    z_max: Optional[int] = Field(alias='zMax', default=None, description='The maximum z coordinate of the view')
    x_min: Optional[int] = Field(alias='xMin', default=None, description='The minimum x coordinate of the view')
    x_max: Optional[int] = Field(alias='xMax', default=None, description='The maximum x coordinate of the view')
    y_min: Optional[int] = Field(alias='yMin', default=None, description='The minimum y coordinate of the view')
    y_max: Optional[int] = Field(alias='yMax', default=None, description='The maximum y coordinate of the view')
    t_min: Optional[int] = Field(alias='tMin', default=None, description='The minimum t coordinate of the view')
    t_max: Optional[int] = Field(alias='tMax', default=None, description='The maximum t coordinate of the view')
    c_min: Optional[int] = Field(alias='cMin', default=None, description='The minimum c (channel) coordinate of the view')
    c_max: Optional[int] = Field(alias='cMax', default=None, description='The maximum c (channel) coordinate of the view')
    roi: ID = Field(description='The ID of the ROI of the parent image this view is a cutout of')
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class PartialReferenceViewInput(BaseModel):
    """Input for creating a reference view (marking the region as a reference for other views) as part of creating an image; the image is taken from the surrounding input"""
    collection: Optional[ID] = Field(default=None, description='The collection this view belongs to')
    z_min: Optional[int] = Field(alias='zMin', default=None, description='The minimum z coordinate of the view')
    z_max: Optional[int] = Field(alias='zMax', default=None, description='The maximum z coordinate of the view')
    x_min: Optional[int] = Field(alias='xMin', default=None, description='The minimum x coordinate of the view')
    x_max: Optional[int] = Field(alias='xMax', default=None, description='The maximum x coordinate of the view')
    y_min: Optional[int] = Field(alias='yMin', default=None, description='The minimum y coordinate of the view')
    y_max: Optional[int] = Field(alias='yMax', default=None, description='The maximum y coordinate of the view')
    t_min: Optional[int] = Field(alias='tMin', default=None, description='The minimum t coordinate of the view')
    t_max: Optional[int] = Field(alias='tMax', default=None, description='The maximum t coordinate of the view')
    c_min: Optional[int] = Field(alias='cMin', default=None, description='The minimum c (channel) coordinate of the view')
    c_max: Optional[int] = Field(alias='cMax', default=None, description='The maximum c (channel) coordinate of the view')
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class PartialScaleViewInput(BaseModel):
    """Input for creating a scale view (the scale factors relative to a parent view) as part of creating an image; the image is taken from the surrounding input"""
    collection: Optional[ID] = Field(default=None, description='The collection this view belongs to')
    z_min: Optional[int] = Field(alias='zMin', default=None, description='The minimum z coordinate of the view')
    z_max: Optional[int] = Field(alias='zMax', default=None, description='The maximum z coordinate of the view')
    x_min: Optional[int] = Field(alias='xMin', default=None, description='The minimum x coordinate of the view')
    x_max: Optional[int] = Field(alias='xMax', default=None, description='The maximum x coordinate of the view')
    y_min: Optional[int] = Field(alias='yMin', default=None, description='The minimum y coordinate of the view')
    y_max: Optional[int] = Field(alias='yMax', default=None, description='The maximum y coordinate of the view')
    t_min: Optional[int] = Field(alias='tMin', default=None, description='The minimum t coordinate of the view')
    t_max: Optional[int] = Field(alias='tMax', default=None, description='The maximum t coordinate of the view')
    c_min: Optional[int] = Field(alias='cMin', default=None, description='The minimum c (channel) coordinate of the view')
    c_max: Optional[int] = Field(alias='cMax', default=None, description='The maximum c (channel) coordinate of the view')
    parent: Optional[ID] = Field(default=None, description='The ID of the parent view this scale view is derived from')
    scale_x: Optional[float] = Field(alias='scaleX', default=None, description='The scale in x direction')
    scale_y: Optional[float] = Field(alias='scaleY', default=None, description='The scale in y direction')
    scale_z: Optional[float] = Field(alias='scaleZ', default=None, description='The scale in z direction')
    scale_t: Optional[float] = Field(alias='scaleT', default=None, description='The scale in t direction')
    scale_c: Optional[float] = Field(alias='scaleC', default=None, description='The scale in c direction')
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class PartialTimepointViewInput(BaseModel):
    """Input for creating a timepoint view (placing the region in time relative to an era) as part of creating an image; the image is taken from the surrounding input"""
    collection: Optional[ID] = Field(default=None, description='The collection this view belongs to')
    z_min: Optional[int] = Field(alias='zMin', default=None, description='The minimum z coordinate of the view')
    z_max: Optional[int] = Field(alias='zMax', default=None, description='The maximum z coordinate of the view')
    x_min: Optional[int] = Field(alias='xMin', default=None, description='The minimum x coordinate of the view')
    x_max: Optional[int] = Field(alias='xMax', default=None, description='The maximum x coordinate of the view')
    y_min: Optional[int] = Field(alias='yMin', default=None, description='The minimum y coordinate of the view')
    y_max: Optional[int] = Field(alias='yMax', default=None, description='The maximum y coordinate of the view')
    t_min: Optional[int] = Field(alias='tMin', default=None, description='The minimum t coordinate of the view')
    t_max: Optional[int] = Field(alias='tMax', default=None, description='The maximum t coordinate of the view')
    c_min: Optional[int] = Field(alias='cMin', default=None, description='The minimum c (channel) coordinate of the view')
    c_max: Optional[int] = Field(alias='cMax', default=None, description='The maximum c (channel) coordinate of the view')
    era: Optional[ID] = Field(default=None, description='The ID of the era this timepoint belongs to')
    time_since_start: Optional[Duration] = Field(alias='timeSinceStart', default=None, description="The time since the start of the era (e.g. '100 ms')")
    index_since_start: Optional[int] = Field(alias='indexSinceStart', default=None, description='The index of the timepoint since the start of the era')
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class PhasorCalibrationInput(BaseModel):
    """Input type for an instrument-response correction: the phase offset and modulation factor taking a raw phasor to a calibrated one"""
    axis: str = Field(description='The axis the correction applies to')
    harmonic: Optional[int] = Field(default=None, description='The harmonic the correction applies at')
    phase_offset: Optional[float] = Field(alias='phaseOffset', default=None, description='The phase correction in radians')
    modulation_factor: Optional[float] = Field(alias='modulationFactor', default=None, description='The modulation correction')
    reference: Optional[str] = Field(default=None, description='What the correction was measured against')
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class PhasorCursorInput(BaseModel):
    """A region of phasor space, and the color the pixels falling inside it are painted. A color rule on the image, not a plot widget"""
    kind: Optional[PhasorCursorKind] = None
    g: Optional[float] = None
    s: Optional[float] = None
    radius: Optional[float] = None
    points: Optional[Tuple[Tuple[float, ...], ...]] = None
    color: Optional[Tuple[int, ...]] = None
    label: Optional[str] = None
    visible: Optional[bool] = None
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class PhasorHistogramInput(BaseModel):
    """Input type for a phasor distribution: the 2D (g, s) density of a phasor taken over one axis at one harmonic, plus the summed profile it came from. Persisted so a client can pick a value range for a phasor overlay without reading the cube"""
    axis: str = Field(description='The axis the phasor was taken over')
    counts: Tuple[float, ...] = Field(description='The flattened bins x bins density')
    harmonic: Optional[int] = Field(default=None, description='The harmonic the phasor was taken at')
    bins: Optional[int] = Field(default=None, description='The resolution of the square (g, s) density grid')
    g_min: Optional[float] = Field(alias='gMin', default=None)
    g_max: Optional[float] = Field(alias='gMax', default=None)
    s_min: Optional[float] = Field(alias='sMin', default=None)
    s_max: Optional[float] = Field(alias='sMax', default=None)
    total: Optional[int] = None
    calibrated: Optional[bool] = None
    profile: Optional[Tuple[float, ...]] = None
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class PhasorTransferInput(BaseModel):
    """How a phasor becomes the pixel's color: the transfer function of a phasor source"""
    mode: Optional[PhasorColorMode] = None
    min: Optional[GenericQuantity] = None
    max: Optional[GenericQuantity] = None
    colormap: Optional[ColorMap] = None
    weight_by_intensity: Optional[bool] = Field(alias='weightByIntensity', default=None)
    intensity: Optional['TransferFunctionInput'] = None
    cursors: Optional[Tuple[PhasorCursorInput, ...]] = None
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class PhysicalAxisInput(BaseModel):
    """Input type for one axis of a unit-carrying coordinate system: its name, its semantic kind and its physical unit"""
    name: str
    type: AxisType
    unit: Unit
    long_name: Optional[str] = Field(alias='longName', default=None)
    description: Optional[str] = None
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class PinSceneSnapshotInput(BaseModel):
    """Input for pinning or unpinning a lens snapshot for quick access"""
    id: ID = Field(description='The ID of the snapshot to pin or unpin')
    pin: bool = Field(description='True to pin, false to unpin')
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class Pose3DInput(BaseModel):
    """A 3D pose consisting of position and orientation."""
    position: Optional['Vec3Input'] = None
    orientation: Optional[EulerInput] = None
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class RGBViewInput(BaseModel):
    """Input for creating an RGB render view on an existing image, referenced by ID"""
    collection: Optional[ID] = Field(default=None, description='The collection this view belongs to')
    z_min: Optional[int] = Field(alias='zMin', default=None, description='The minimum z coordinate of the view')
    z_max: Optional[int] = Field(alias='zMax', default=None, description='The maximum z coordinate of the view')
    x_min: Optional[int] = Field(alias='xMin', default=None, description='The minimum x coordinate of the view')
    x_max: Optional[int] = Field(alias='xMax', default=None, description='The maximum x coordinate of the view')
    y_min: Optional[int] = Field(alias='yMin', default=None, description='The minimum y coordinate of the view')
    y_max: Optional[int] = Field(alias='yMax', default=None, description='The maximum y coordinate of the view')
    t_min: Optional[int] = Field(alias='tMin', default=None, description='The minimum t coordinate of the view')
    t_max: Optional[int] = Field(alias='tMax', default=None, description='The maximum t coordinate of the view')
    c_min: Optional[int] = Field(alias='cMin', default=None, description='The minimum c (channel) coordinate of the view')
    c_max: Optional[int] = Field(alias='cMax', default=None, description='The maximum c (channel) coordinate of the view')
    context: ID = Field(description='The ID of the RGB render context this view belongs to')
    gamma: Optional[float] = Field(default=None, description='The gamma correction applied to the channel')
    contrast_limit_min: Optional[float] = Field(alias='contrastLimitMin', default=None, description='The minimum contrast limit of the channel')
    contrast_limit_max: Optional[float] = Field(alias='contrastLimitMax', default=None, description='The maximum contrast limit of the channel')
    rescale: Optional[bool] = Field(default=None, description='Whether to rescale the channel data to the contrast limits')
    scale: Optional[float] = Field(default=None, description='The scale factor applied to the channel when rendering')
    active: Optional[bool] = Field(default=None, description='Whether the view is active')
    color_map: Optional[ColorMap] = Field(alias='colorMap', default=None, description='The color map applied to the channel')
    base_color: Optional[Tuple[float, ...]] = Field(alias='baseColor', default=None, description='The base color of the channel as RGBA values (if using a mapped scaler)')
    image: ID = Field(description='The ID of the image this view is for')
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class ReferenceViewInput(BaseModel):
    """Input for creating a reference view on an existing image, referenced by ID"""
    collection: Optional[ID] = Field(default=None, description='The collection this view belongs to')
    z_min: Optional[int] = Field(alias='zMin', default=None, description='The minimum z coordinate of the view')
    z_max: Optional[int] = Field(alias='zMax', default=None, description='The maximum z coordinate of the view')
    x_min: Optional[int] = Field(alias='xMin', default=None, description='The minimum x coordinate of the view')
    x_max: Optional[int] = Field(alias='xMax', default=None, description='The maximum x coordinate of the view')
    y_min: Optional[int] = Field(alias='yMin', default=None, description='The minimum y coordinate of the view')
    y_max: Optional[int] = Field(alias='yMax', default=None, description='The maximum y coordinate of the view')
    t_min: Optional[int] = Field(alias='tMin', default=None, description='The minimum t coordinate of the view')
    t_max: Optional[int] = Field(alias='tMax', default=None, description='The maximum t coordinate of the view')
    c_min: Optional[int] = Field(alias='cMin', default=None, description='The minimum c (channel) coordinate of the view')
    c_max: Optional[int] = Field(alias='cMax', default=None, description='The maximum c (channel) coordinate of the view')
    image: ID = Field(description='The ID of the image this view is for')
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class RegistrationPathInput(BaseModel):
    """A source (dataset, table dataset, mesh collection, or coordinate system) to register into a shared space, plus the edge that places it. The edge points from the source's own coordinate system to the shared space; the transform is validated exactly as createTransformation validates one"""
    dataset: Optional[ID] = None
    table_dataset: Optional[ID] = Field(alias='tableDataset', default=None)
    mesh_collection: Optional[ID] = Field(alias='meshCollection', default=None)
    annotation_collection: Optional[ID] = Field(alias='annotationCollection', default=None)
    coordinate_system: Optional[ID] = Field(alias='coordinateSystem', default=None)
    transform: Optional['TransformInput'] = None
    name: Optional[str] = None
    validity: Optional[PlacementValidity] = None
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
    id: ID = Field(description='The ID of the dataset to revert')
    history_id: ID = Field(alias='historyId', description='The ID of the provenance history entry to revert the dataset to')
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class RoiInput(BaseModel):
    """Input for creating a region of interest (ROI) on an image"""
    image: ID = Field(description='The image this ROI belongs to')
    vectors: Tuple[FiveDVector, ...] = Field(description='The vector coordinates defining the ROI')
    kind: RoiKind = Field(description='The type/kind of ROI')
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class ScaleInput(BaseModel):
    """Input type for one pyramid level: the array backing it. Its scale is derived from its actual shape, never supplied"""
    scale_method: Optional[str] = Field(alias='scaleMethod', default=None, description="The method used to create the scale, e.g. 'nearest', 'bilinear', 'bicubic'. Recorded as provenance on the level's transformation")
    level: int
    array: ArrayLike = Field(description='The array-like object to create the image from')
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class ScenePolicyInput(BaseModel):
    """The policy createSceneFromCoordinateSystem follows: at most `nchildren` layers, materialized from the sources living in or registered into the space, filtered by source kind and drawn by the recipe in `kind`"""
    nchildren: Annotated[Optional[int], GraphQLDefault('8')] = None
    'Default: 8'
    transform_tables: Annotated[Optional[bool], GraphQLDefault('False')] = Field(alias='transformTables', default=None)
    'Default: False'
    include_meshes: Annotated[Optional[bool], GraphQLDefault('True')] = Field(alias='includeMeshes', default=None)
    'Default: True'
    kind: Optional[BootstrapLayerKind] = None
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class SceneSnapshotFilter(BaseModel):
    """No documentation"""
    ids: Optional[Tuple[ID, ...]] = Field(default=None, description='Filter by list of IDs')
    search: Optional[str] = Field(default=None, description='Search by name (case-insensitive substring)')
    created_before: Optional[datetime] = Field(alias='createdBefore', default=None, description='Filter for items created before this datetime')
    created_after: Optional[datetime] = Field(alias='createdAfter', default=None, description='Filter for items created after this datetime')
    owner: Optional[ID] = Field(default=None, description="Filter by the creator's subject ID")
    pinned: Optional[bool] = Field(default=None, description='Filter by whether the current user has pinned the item')
    created_through_task: Optional[str] = Field(alias='createdThroughTask', default=None, description='Filter by the rekuest task id the item was created through')
    created_through: Optional[ID] = Field(alias='createdThrough', default=None, description='Filter by the database ID of the task the item was created through (the `createdThrough { id }` field)')
    assigned_by: Optional[ID] = Field(alias='assignedBy', default=None, description='Filter by the sub of the user that assigned the creating task')
    created_through_by: Optional[ID] = Field(alias='createdThroughBy', default=None, description='Filter by the database ID of the user that assigned the creating task (the `createdThroughBy { id }` field)')
    id: Optional[ID] = None
    name: Optional['StrFilterLookup'] = None
    and_: Optional['SceneSnapshotFilter'] = Field(alias='AND', default=None)
    or_: Optional['SceneSnapshotFilter'] = Field(alias='OR', default=None)
    not_: Optional['SceneSnapshotFilter'] = Field(alias='NOT', default=None)
    distinct: Optional[bool] = Field(alias='DISTINCT', default=None)
    scene: Optional[ID] = Field(default=None, description='Filter by the scene this snapshot is a picture of')
    scenes: Optional[Tuple[ID, ...]] = Field(default=None, description='Filter by a list of scenes (fetch the tiles for a set of scenes in one query, the way a picker does)')
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class SceneSnapshotInput(BaseModel):
    """Input for creating a snapshot (a pre-rendered picture) of a scene from an already-uploaded media file"""
    file: ImageFileLike = Field(description='The uploaded media file store containing the rendered image')
    scene: ID = Field(description='The ID of the scene this is a picture of')
    name: Optional[str] = Field(default=None, description='The name of the snapshot')
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class SettingInput(BaseModel):
    """One named device setting with exactly one value slot filled: a quantity when the setting carries a unit, else a number, text or flag. A setting holding two values is two settings"""
    name: str
    quantity: Optional[GenericQuantity] = None
    number: Optional[float] = None
    text: Optional[str] = None
    flag: Optional[bool] = None
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class SliceInput(BaseModel):
    """Input type for a slice along one axis of a dataset"""
    axis: str
    start: Optional[int] = None
    stop: Optional[int] = None
    step: Optional[int] = None
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class SnapshotInput(BaseModel):
    """Input for creating a snapshot (pre-rendered thumbnail) of an image from an uploaded media file"""
    file: ImageFileLike = Field(description='The uploaded media file store containing the rendered snapshot')
    image: ID = Field(description='The ID of the image this snapshot belongs to')
    name: Optional[str] = Field(default=None, description='The name of the snapshot')
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class SpectrumInput(BaseModel):
    """Spectral window for wavelength-dependent components."""
    min: Length
    max: Length
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class StageFilter(BaseModel):
    """No documentation"""
    ids: Optional[Tuple[ID, ...]] = Field(default=None, description='Filter by list of IDs')
    search: Optional[str] = Field(default=None, description='Search by name (case-insensitive substring)')
    created_before: Optional[datetime] = Field(alias='createdBefore', default=None, description='Filter for items created before this datetime')
    created_after: Optional[datetime] = Field(alias='createdAfter', default=None, description='Filter for items created after this datetime')
    owner: Optional[ID] = Field(default=None, description="Filter by the creator's subject ID")
    pinned: Optional[bool] = Field(default=None, description='Filter by whether the current user has pinned the item')
    created_through_task: Optional[str] = Field(alias='createdThroughTask', default=None, description='Filter by the rekuest task id the item was created through')
    created_through: Optional[ID] = Field(alias='createdThrough', default=None, description='Filter by the database ID of the task the item was created through (the `createdThrough { id }` field)')
    assigned_by: Optional[ID] = Field(alias='assignedBy', default=None, description='Filter by the sub of the user that assigned the creating task')
    created_through_by: Optional[ID] = Field(alias='createdThroughBy', default=None, description='Filter by the database ID of the user that assigned the creating task (the `createdThroughBy { id }` field)')
    id: Optional[ID] = None
    kind: Optional[str] = None
    name: Optional['StrFilterLookup'] = None
    and_: Optional['StageFilter'] = Field(alias='AND', default=None)
    or_: Optional['StageFilter'] = Field(alias='OR', default=None)
    not_: Optional['StageFilter'] = Field(alias='NOT', default=None)
    distinct: Optional[bool] = Field(alias='DISTINCT', default=None)
    instrument: Optional[ID] = Field(default=None, description='Filter by the instrument this stage belongs to')
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class StageInput(BaseModel):
    """Input for creating a stage, a physical coordinate system for positioning images"""
    name: str = Field(description='The name of the stage')
    instrument: Optional[ID] = Field(default=None, description='The ID of the instrument this stage belongs to')
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class StageStateInput(BaseModel):
    """Where the stage was, per axis, as physical lengths (e.g. '100.5 um')"""
    x: Optional[Length] = None
    y: Optional[Length] = None
    z: Optional[Length] = None
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

class TableColumnInput(BaseModel):
    """One declared column of a table dataset: its name, dtype, and role. A COORDINATE column also carries an axis type and optional unit and becomes an axis of the table's space"""
    name: str
    dtype: str
    role: Annotated[Optional[TableColumnRole], GraphQLDefault('ATTRIBUTE')] = None
    'Default: ATTRIBUTE'
    axis_type: Optional[AxisType] = Field(alias='axisType', default=None)
    unit: Optional[str] = None
    long_name: Optional[str] = Field(alias='longName', default=None)
    description: Optional[str] = None
    references: Optional[ID] = None
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class TableDatasetFilter(BaseModel):
    """No documentation"""
    ids: Optional[Tuple[ID, ...]] = Field(default=None, description='Filter by list of IDs')
    search: Optional[str] = Field(default=None, description='Search by name (case-insensitive substring)')
    created_before: Optional[datetime] = Field(alias='createdBefore', default=None, description='Filter for items created before this datetime')
    created_after: Optional[datetime] = Field(alias='createdAfter', default=None, description='Filter for items created after this datetime')
    owner: Optional[ID] = Field(default=None, description="Filter by the creator's subject ID")
    created_through_task: Optional[str] = Field(alias='createdThroughTask', default=None, description='Filter by the rekuest task id the item was created through')
    created_through: Optional[ID] = Field(alias='createdThrough', default=None, description='Filter by the database ID of the task the item was created through (the `createdThrough { id }` field)')
    assigned_by: Optional[ID] = Field(alias='assignedBy', default=None, description='Filter by the sub of the user that assigned the creating task')
    created_through_by: Optional[ID] = Field(alias='createdThroughBy', default=None, description='Filter by the database ID of the user that assigned the creating task (the `createdThroughBy { id }` field)')
    id: Optional[ID] = None
    name: Optional[StrFilterLookup] = None
    description: Optional[StrFilterLookup] = None
    and_: Optional['TableDatasetFilter'] = Field(alias='AND', default=None)
    or_: Optional['TableDatasetFilter'] = Field(alias='OR', default=None)
    not_: Optional['TableDatasetFilter'] = Field(alias='NOT', default=None)
    distinct: Optional[bool] = Field(alias='DISTINCT', default=None)
    dataset: Optional[ID] = Field(default=None, description='Filter by the dataset the table was computed from, following its derivation edge')
    has_column_role: Optional[TableColumnRole] = Field(alias='hasColumnRole', default=None, description='Filter to tables that declare a column of this role, e.g. TRACK_ID')
    placeable_in: Optional[ID] = Field(alias='placeableIn', default=None, description='Filter to table datasets placeable into this coordinate system: those whose own coordinate system has a traversable path into it, walking the transformation edges. Takes a *space*, not a scene -- pass `scene.worldCoordinateSystem.id` to ask it of a scene')
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class TimepointViewFilter(BaseModel):
    """No documentation"""
    ids: Optional[Tuple[ID, ...]] = Field(default=None, description='Filter by list of IDs')
    is_global: Optional[bool] = Field(alias='isGlobal', default=None)
    image: Optional[ID] = Field(default=None, description='Filter by the image this view belongs to')
    images: Optional[Tuple[ID, ...]] = Field(default=None, description='Filter by a list of images this view belongs to')
    search: Optional[str] = Field(default=None, description='Search by the name of the image this view belongs to')
    id: Optional[ID] = None
    era: Optional[EraFilter] = None
    time_since_start: Optional[int] = Field(alias='timeSinceStart', default=None)
    index_since_start: Optional[int] = Field(alias='indexSinceStart', default=None)
    and_: Optional['TimepointViewFilter'] = Field(alias='AND', default=None)
    or_: Optional['TimepointViewFilter'] = Field(alias='OR', default=None)
    not_: Optional['TimepointViewFilter'] = Field(alias='NOT', default=None)
    distinct: Optional[bool] = Field(alias='DISTINCT', default=None)
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class TransferFunctionInput(BaseModel):
    """Transfer-function settings for a channel source in a layer render graph"""
    clim_min: Optional[float] = Field(alias='climMin', default=None)
    clim_max: Optional[float] = Field(alias='climMax', default=None)
    colormap: Optional[ColorMap] = None
    color: Optional[Tuple[int, ...]] = None
    gamma: Optional[float] = None
    opacity: Optional[float] = None
    invert: Optional[bool] = None
    categorical: Optional[bool] = None
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)
TransformInput = Annotated[Union[AffineTransformInput, ByDimensionTransformInput, FieldTransformInput, MapAxisTransformInput, RotationTransformInput, ScaleTransformInput, TranslationTransformInput, UnmappableTransformInput], Field(discriminator='kind')]

class TransformationFilter(BaseModel):
    """No documentation"""
    ids: Optional[Tuple[ID, ...]] = Field(default=None, description='Filter by list of IDs')
    created_before: Optional[datetime] = Field(alias='createdBefore', default=None, description='Filter for items created before this datetime')
    created_after: Optional[datetime] = Field(alias='createdAfter', default=None, description='Filter for items created after this datetime')
    owner: Optional[ID] = Field(default=None, description="Filter by the creator's subject ID")
    id: Optional[ID] = None
    kind: Optional[TransformKindChoices] = None
    and_: Optional['TransformationFilter'] = Field(alias='AND', default=None)
    or_: Optional['TransformationFilter'] = Field(alias='OR', default=None)
    not_: Optional['TransformationFilter'] = Field(alias='NOT', default=None)
    distinct: Optional[bool] = Field(alias='DISTINCT', default=None)
    validity: Optional[PlacementValidity] = Field(default=None, description="Filter by how much the edge's map is actually known, e.g. UNKNOWN to list every placement that is still an assumption")
    input: Optional[ID] = Field(default=None, description='Filter by the coordinate system this transformation maps from')
    output: Optional[ID] = Field(default=None, description='Filter by the coordinate system this transformation maps to')
    roots_only: Optional[bool] = Field(alias='rootsOnly', default=None, description='Show only top-level edges, excluding the children of SEQUENCE / BY_DIMENSION wrappers')
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class TreeInput(BaseModel):
    """No documentation"""
    id: Annotated[Optional[str], GraphQLDefault('root')] = None
    'Default: root'
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

class UpdateAnimationInput(BaseModel):
    """Input for re-authoring a camera tour. Passing `waypoints` replaces every stop -- which is also how a tour is reordered, since a stop's position in the tour is its position in this list"""
    id: ID = Field(description='The ID of the tour to update')
    name: Optional[str] = Field(default=None, description='The name of the tour')
    description: Optional[str] = Field(default=None, description='What the tour shows')
    waypoints: Optional[Tuple[AnimationWaypointInput, ...]] = Field(default=None, description="The poses, in tour order. Replaces the tour's stops entirely")
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class UpdateAnnotationInput(BaseModel):
    """Input for editing an annotation. Only the supplied fields change; new vectors re-derive the bounding box against the current transform chain"""
    kind: Optional[RoiKind] = None
    vectors: Optional[Tuple[ThreeDVector, ...]] = None
    stroke_color: Optional[Tuple[int, ...]] = Field(alias='strokeColor', default=None)
    fill_color: Optional[Tuple[int, ...]] = Field(alias='fillColor', default=None)
    id: ID
    name: Optional[str] = None
    description: Optional[str] = None
    coordinates: Optional[Tuple[CoordinateInput, ...]] = None
    stroke_width: Optional[float] = Field(alias='strokeWidth', default=None)
    filled: Optional[bool] = None
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class UpdateCoordinateSystemInput(BaseModel):
    """Input for renaming a shared coordinate system or anchoring its clock. Shared spaces only: every other system is named by the container that owns it"""
    id: ID
    name: Optional[str] = None
    epoch: Optional[datetime] = None
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class UpdateImageInput(BaseModel):
    """Input for updating an image's name or tags"""
    id: ID = Field(description='The ID of the image to update')
    tags: Optional[Tuple[str, ...]] = Field(default=None, description='Tags to add to the image')
    name: Optional[str] = Field(default=None, description='The new name of the image')
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class UpdateRGBContextInput(BaseModel):
    """Input for updating an existing RGB render context"""
    id: ID = Field(description='The ID of the RGB context to update')
    name: Optional[str] = Field(default=None, description='The new name of the RGB context')
    thumbnail: Optional[ID] = Field(default=None, description='The ID of an uploaded media store to use as the thumbnail snapshot')
    views: Optional[Tuple[PartialRGBViewInput, ...]] = Field(default=None, description="The RGB views (channel rendering settings) to replace the context's views with")
    z: Optional[int] = Field(default=None, description='The z plane the context renders')
    t: Optional[int] = Field(default=None, description='The timepoint the context renders')
    c: Optional[int] = Field(default=None, description='The channel the context renders')
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class UpdateRGBViewInput(BaseModel):
    """Input for updating an existing RGB view, referenced by ID"""
    collection: Optional[ID] = Field(default=None, description='The collection this view belongs to')
    z_min: Optional[int] = Field(alias='zMin', default=None, description='The minimum z coordinate of the view')
    z_max: Optional[int] = Field(alias='zMax', default=None, description='The maximum z coordinate of the view')
    x_min: Optional[int] = Field(alias='xMin', default=None, description='The minimum x coordinate of the view')
    x_max: Optional[int] = Field(alias='xMax', default=None, description='The maximum x coordinate of the view')
    y_min: Optional[int] = Field(alias='yMin', default=None, description='The minimum y coordinate of the view')
    y_max: Optional[int] = Field(alias='yMax', default=None, description='The maximum y coordinate of the view')
    t_min: Optional[int] = Field(alias='tMin', default=None, description='The minimum t coordinate of the view')
    t_max: Optional[int] = Field(alias='tMax', default=None, description='The maximum t coordinate of the view')
    c_min: Optional[int] = Field(alias='cMin', default=None, description='The minimum c (channel) coordinate of the view')
    c_max: Optional[int] = Field(alias='cMax', default=None, description='The maximum c (channel) coordinate of the view')
    context: Optional[ID] = Field(default=None, description='The ID of the RGB render context this view belongs to')
    gamma: Optional[float] = Field(default=None, description='The gamma correction applied to the channel')
    contrast_limit_min: Optional[float] = Field(alias='contrastLimitMin', default=None, description='The minimum contrast limit of the channel')
    contrast_limit_max: Optional[float] = Field(alias='contrastLimitMax', default=None, description='The maximum contrast limit of the channel')
    rescale: Optional[bool] = Field(default=None, description='Whether to rescale the channel data to the contrast limits')
    scale: Optional[float] = Field(default=None, description='The scale factor applied to the channel when rendering')
    active: Optional[bool] = Field(default=None, description='Whether the view is active')
    color_map: Optional[ColorMap] = Field(alias='colorMap', default=None, description='The color map applied to the channel')
    base_color: Optional[Tuple[float, ...]] = Field(alias='baseColor', default=None, description='The base color of the channel as RGBA values (if using a mapped scaler)')
    id: ID = Field(description='The ID of the RGB view to update')
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class UpdateRoiInput(BaseModel):
    """Input for updating an existing region of interest (ROI)"""
    roi: ID = Field(description='The ID of the ROI to update')
    vectors: Optional[Tuple[FiveDVector, ...]] = Field(default=None, description='The new vector coordinates defining the ROI')
    kind: Optional[RoiKind] = Field(default=None, description='The new type/kind of ROI')
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class UpdateSceneInput(BaseModel):
    """Input for setting a scene's viewer preferences. Every field is optional and an omitted one is left alone, so a client may set one preference without restating the others"""
    id: ID = Field(description='The ID of the scene to update')
    preferred_view: Optional[PreferredView] = Field(alias='preferredView', default=None)
    background_color: Optional[Tuple[float, ...]] = Field(alias='backgroundColor', default=None)
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class UpdateTableDatasetInput(BaseModel):
    """Input for renaming or redescribing a table dataset. These two fields are the whole of what is editable: the store, the declared columns and the coordinate system derived from them are fixed at creation, and a recomputation is a new table"""
    id: ID
    name: Optional[str] = None
    description: Optional[str] = None
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class UpdateTransformationInput(BaseModel):
    """Input for refining an edge's parameters. Bumps its version, which is what tells an ROI its chain has moved"""
    id: ID
    name: Optional[str] = None
    scale: Optional[Tuple[float, ...]] = None
    translation: Optional[Tuple[float, ...]] = None
    affine: Optional[Tuple[Tuple[float, ...], ...]] = None
    validity: Optional[PlacementValidity] = None
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class ValueHistogramInput(ValueHistogramInputTrait, BaseModel):
    """Input type for a value histogram, which specifies the histogram of pixel values along certain dimensions to provide additional context about the distribution of pixel values in an image"""
    histogram: Tuple[float, ...] = Field(description='The histogram of the pixel values (y values)')
    bins: Tuple[float, ...] = Field(description='The bin indices of the histogram (x values)')
    min: Optional[float] = Field(default=None, description='The minimum pixel value of the histogram')
    max: Optional[float] = Field(default=None, description='The maximum pixel value of the histogram')
    p1: Optional[float] = Field(default=None, description='The 1st percentile pixel value of the histogram')
    p99: Optional[float] = Field(default=None, description='The 99th percentile pixel value of the histogram')
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class Vec3Input(BaseModel):
    """A 3D vector representing a point or offset in space."""
    x: Optional[float] = None
    y: Optional[float] = None
    z: Optional[float] = None
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class ViewCollectionInput(BaseModel):
    """Input for creating a view collection to group views"""
    name: str = Field(description='The name of the view collection')
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class ViewFilter(BaseModel):
    """No documentation"""
    ids: Optional[Tuple[ID, ...]] = Field(default=None, description='Filter by list of IDs')
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
    """A view anchoring an image region in real time: it places the region within an era (a named time epoch on the microscope) at a time offset or frame index since its start."""
    typename: Literal['TimepointView'] = Field(alias='__typename', default='TimepointView', exclude=True)

class ViewWellPositionView(ViewBase, BaseModel):
    """A view mapping an image region to a well (row/column) of a multi well plate, so plate-based acquisitions can be traced back to their well."""
    typename: Literal['WellPositionView'] = Field(alias='__typename', default='WellPositionView', exclude=True)

class CameraState(MikroFetchable, BaseModel):
    """Where a viewer's camera is in a scene, and how it is looking at it. Carries a flat cross-section view and a volumetric projection view of one position, so a single pose serves both and `Scene.preferredView` picks which is used. Every number is read against the scene's world coordinate system, whose axes carry the units"""
    typename: Literal['CameraState'] = Field(alias='__typename', default='CameraState', exclude=True)
    position: Any
    "Where the camera is centred, keyed by the world's axis names. Keyed rather than a positional list because the world's axes are named and a tour through a timelapse moves in t as much as in z -- a list would silently depend on axis order. Axes the pose does not name are left wherever the viewer already had them."
    cross_section_orientation: Optional[Tuple[float, ...]] = Field(default=None, alias='crossSectionOrientation')
    "The flat view's orientation, as a quaternion. Null to leave it to the viewer."
    cross_section_scale: Optional[float] = Field(default=None, alias='crossSectionScale')
    "The flat view's zoom, in world units per screen pixel. Null to leave it to the viewer."
    projection_orientation: Optional[Tuple[float, ...]] = Field(default=None, alias='projectionOrientation')
    "The volumetric view's orientation, as a quaternion. Null to leave it to the viewer."
    projection_scale: Optional[float] = Field(default=None, alias='projectionScale')
    "The volumetric view's zoom, in world units per screen pixel. Null to leave it to the viewer."
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for CameraState"""
        document = 'fragment CameraState on CameraState {\n  position\n  crossSectionOrientation\n  crossSectionScale\n  projectionOrientation\n  projectionScale\n  __typename\n}'
        name = 'CameraState'
        type = 'CameraState'

class Camera(MikroFetchable, BaseModel):
    """A camera (detector) on a microscope, described by its sensor dimensions, pixel sizes and bit depth. Clients use it through optics views to record which detector acquired an image."""
    typename: Literal['Camera'] = Field(alias='__typename', default='Camera', exclude=True)
    sensor_size_x: Optional[int] = Field(default=None, alias='sensorSizeX')
    sensor_size_y: Optional[int] = Field(default=None, alias='sensorSizeY')
    pixel_size_x: Optional[Length] = Field(default=None, alias='pixelSizeX')
    pixel_size_y: Optional[Length] = Field(default=None, alias='pixelSizeY')
    name: str
    serial_number: str = Field(alias='serialNumber')
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for Camera"""
        document = 'fragment Camera on Camera {\n  sensorSizeX\n  sensorSizeY\n  pixelSizeX\n  pixelSizeY\n  name\n  serialNumber\n  __typename\n}'
        name = 'Camera'
        type = 'Camera'

class Axis(MikroFetchable, BaseModel):
    """One named, typed dimension of a coordinate system. Its `order` is its index into the array shape"""
    typename: Literal['Axis'] = Field(alias='__typename', default='Axis', exclude=True)
    id: ID
    order: int
    name: str
    type: AxisType
    unit: Optional[Unit] = Field(default=None)
    long_name: Optional[str] = Field(default=None, alias='longName')
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for Axis"""
        document = 'fragment Axis on Axis {\n  id\n  order\n  name\n  type\n  unit\n  longName\n  __typename\n}'
        name = 'Axis'
        type = 'Axis'

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

class LayerScene(SceneTrait, BaseModel):
    """A composition of layers over a shared world coordinate system. The scene carries no units of its own -- they are per-axis, on the axes of its world system"""
    typename: Literal['Scene'] = Field(alias='__typename', default='Scene', exclude=True)
    id: ID
    name: str
    model_config = ConfigDict(frozen=True)

class LayerLens(Lensable, BaseModel):
    """A Lens is a way of looking at a dataset: a dimensional selection (slices) over a dataset that defines a view of its data"""
    typename: Literal['Lens'] = Field(alias='__typename', default='Lens', exclude=True)
    id: ID
    model_config = ConfigDict(frozen=True)

class LayerBase(BaseModel):
    """A layer placed in a scene and alpha-blended over the layers below it. It carries view state only: a spatial fact is a coordinate system or a transformation edge, never a field here, and every spatial question a layer answers -- `pathToWorld`, `placement`, `placementValidity`, `placementInvariance` -- is derived from the graph on read and stored nowhere, so refining one edge updates every layer that looks through it. Which columns hold a point layer's coordinates is likewise the table dataset's declaration, not a per-layer copy. The concrete kind (ImageLayer, AnnotationLayer, PointLayer, TrackLayer, MeshLayer) carries its own data source and render settings."""
    id: ID
    scene: LayerScene

class LayerCatch(LayerBase):
    """Catch all class for LayerBase"""
    typename: str = Field(alias='__typename', exclude=True)
    "A layer placed in a scene and alpha-blended over the layers below it. It carries view state only: a spatial fact is a coordinate system or a transformation edge, never a field here, and every spatial question a layer answers -- `pathToWorld`, `placement`, `placementValidity`, `placementInvariance` -- is derived from the graph on read and stored nowhere, so refining one edge updates every layer that looks through it. Which columns hold a point layer's coordinates is likewise the table dataset's declaration, not a per-layer copy. The concrete kind (ImageLayer, AnnotationLayer, PointLayer, TrackLayer, MeshLayer) carries its own data source and render settings."
    id: ID
    scene: LayerScene

class LayerAnnotationLayer(LayerBase, BaseModel):
    """A layer that renders an annotation collection's drawn shapes (polygons, boxes, ellipses, lines, paths) in a scene. One layer per collection: per-shape styling lives on the annotations themselves."""
    typename: Literal['AnnotationLayer'] = Field(alias='__typename', default='AnnotationLayer', exclude=True)

class LayerImageLayer(LayerBase, BaseModel):
    """A layer that renders array (lens) data as an alpha-blended image. Its rendering is described entirely by the composable render graph; its placement, entirely by the coordinate graph."""
    typename: Literal['ImageLayer'] = Field(alias='__typename', default='ImageLayer', exclude=True)
    lens: LayerLens

class LayerMeshLayer(LayerBase, BaseModel):
    """A layer that renders a 3D mesh (surface reconstruction / isosurface) placed and styled in a scene."""
    typename: Literal['MeshLayer'] = Field(alias='__typename', default='MeshLayer', exclude=True)

class LayerPointLayer(LayerBase, BaseModel):
    """A layer that renders a point cloud (e.g. SMLM localisations, centroids) from a table dataset."""
    typename: Literal['PointLayer'] = Field(alias='__typename', default='PointLayer', exclude=True)

class LayerTrackLayer(LayerBase, BaseModel):
    """A layer that renders trajectories (e.g. particle/cell tracks) from a table dataset, grouped by its TRACK_ID column."""
    typename: Literal['TrackLayer'] = Field(alias='__typename', default='TrackLayer', exclude=True)

class Slice(MikroFetchable, BaseModel):
    """A slice along a named axis, with optional start, stop and step"""
    typename: Literal['Slice'] = Field(alias='__typename', default='Slice', exclude=True)
    axis: str
    "The name of the axis the slice acts on, e.g. 'x', 'y', 'z', 'c', or 't'"
    start: Optional[int] = Field(default=None)
    'The starting index of the slice, or None to start from the beginning'
    stop: Optional[int] = Field(default=None)
    'The stopping index of the slice, or None to go to the end'
    step: Optional[int] = Field(default=None)
    'The step size of the slice, or None to use the default step'
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for Slice"""
        document = 'fragment Slice on Slice {\n  axis\n  start\n  stop\n  step\n  __typename\n}'
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

class PhasorCalibration(MikroFetchable, BaseModel):
    """The instrument-response correction taking a raw phasor to a calibrated one, pinned to a coordinate anchor. An acquisition fact, not a display choice: two layers over one dataset cannot coherently disagree about it. Its absence means the phasor is uncalibrated, which still renders"""
    typename: Literal['PhasorCalibration'] = Field(alias='__typename', default='PhasorCalibration', exclude=True)
    id: ID
    axis: str
    harmonic: int
    phase_offset: Optional[float] = Field(default=None, alias='phaseOffset')
    modulation_factor: Optional[float] = Field(default=None, alias='modulationFactor')
    reference: Optional[str] = Field(default=None)
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for PhasorCalibration"""
        document = 'fragment PhasorCalibration on PhasorCalibration {\n  id\n  axis\n  harmonic\n  phaseOffset\n  modulationFactor\n  reference\n  __typename\n}'
        name = 'PhasorCalibration'
        type = 'PhasorCalibration'

class PhasorHistogram(MikroFetchable, BaseModel):
    """The distribution of a phasor pinned to a coordinate anchor: a 2D (g, s) density plus the summed profile it was computed from. What ValueHistogram is to an intensity channel -- it lets a client pick a sane value range for a phasor overlay without reading the cube"""
    typename: Literal['PhasorHistogram'] = Field(alias='__typename', default='PhasorHistogram', exclude=True)
    id: ID
    axis: str
    harmonic: int
    bins: int
    g_min: float = Field(alias='gMin')
    g_max: float = Field(alias='gMax')
    s_min: float = Field(alias='sMin')
    s_max: float = Field(alias='sMax')
    total: Optional[int] = Field(default=None)
    calibrated: bool
    counts: Tuple[float, ...]
    'The flattened bins x bins (g, s) density, row-major with s outermost'
    profile: Tuple[float, ...]
    'The summed profile along the phasor axis (a decay for a MICROTIME axis, a spectrum for a SPECTRUM one), one value per bin'
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for PhasorHistogram"""
        document = 'fragment PhasorHistogram on PhasorHistogram {\n  id\n  axis\n  harmonic\n  bins\n  gMin\n  gMax\n  sMin\n  sMax\n  total\n  calibrated\n  counts\n  profile\n  __typename\n}'
        name = 'PhasorHistogram'
        type = 'PhasorHistogram'

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

class TransformationChildBase(BaseModel):
    """A directed edge of the coordinate graph, mapping `input` to `output`. Direction is always forward. The concrete kind (Scale, Translation, Affine, Sequence, ...) carries the parameters"""
    id: ID
    kind: TransformKind
    input_axes: Tuple[str, ...] = Field(alias='inputAxes')
    "The names of the input axes this edge's parameters are ordered by. `scale`, `translation` and the columns of `affine` follow this order -- which is the input system's axis order, NOT the reading layer's axis names, and the two differ often enough that indexing the arrays against them silently misplaces them. A BY_DIMENSION edge names only the subset of axes it acts on; the axes it does not name are the ones it leaves untouched"
    output_axes: Tuple[str, ...] = Field(alias='outputAxes')
    "The names of the output axes this edge produces. For a rank-changing BY_DIMENSION edge (placing a (c,y,x) dataset into a (t,z,y,x) world) this is the subset it maps onto; the world's other axes are untouched"

class TransformationChildCatch(TransformationChildBase):
    """Catch all class for TransformationChildBase"""
    typename: str = Field(alias='__typename', exclude=True)
    'A directed edge of the coordinate graph, mapping `input` to `output`. Direction is always forward. The concrete kind (Scale, Translation, Affine, Sequence, ...) carries the parameters'
    id: ID
    kind: TransformKind
    input_axes: Tuple[str, ...] = Field(alias='inputAxes')
    "The names of the input axes this edge's parameters are ordered by. `scale`, `translation` and the columns of `affine` follow this order -- which is the input system's axis order, NOT the reading layer's axis names, and the two differ often enough that indexing the arrays against them silently misplaces them. A BY_DIMENSION edge names only the subset of axes it acts on; the axes it does not name are the ones it leaves untouched"
    output_axes: Tuple[str, ...] = Field(alias='outputAxes')
    "The names of the output axes this edge produces. For a rank-changing BY_DIMENSION edge (placing a (c,y,x) dataset into a (t,z,y,x) world) this is the subset it maps onto; the world's other axes are untouched"

class TransformationChildAffineTransformation(TransformationChildBase, TransformationTrait, BaseModel):
    """A general affine map, given as an M x (N+1) matrix with rows outermost"""
    typename: Literal['AffineTransformation'] = Field(alias='__typename', default='AffineTransformation', exclude=True)
    affine: Tuple[Tuple[float, ...], ...]
    'The affine matrix, M x (N+1), rows outermost. The last column is the translation'

class TransformationChildBijectionTransformation(TransformationChildBase, TransformationTrait, BaseModel):
    """A pair of child transformations giving an explicit forward and inverse map"""
    typename: Literal['BijectionTransformation'] = Field(alias='__typename', default='BijectionTransformation', exclude=True)

class TransformationChildByDimensionTransformation(TransformationChildBase, TransformationTrait, BaseModel):
    """A composition of child transformations, each acting on a named subset of the axes"""
    typename: Literal['ByDimensionTransformation'] = Field(alias='__typename', default='ByDimensionTransformation', exclude=True)

class TransformationChildFieldTransformation(TransformationChildBase, TransformationTrait, BaseModel):
    """A non-affine map given by the values of an array rather than by a formula. The array is a `field`: a node of this graph, not a payload on this edge, so it keeps its own lineage and its axes say what its numbers mean. It has no closed-form inverse, so a placement path never walks it backwards"""
    typename: Literal['FieldTransformation'] = Field(alias='__typename', default='FieldTransformation', exclude=True)

class TransformationChildIdentityTransformation(TransformationChildBase, TransformationTrait, BaseModel):
    """The identity map: input and output coordinates are the same"""
    typename: Literal['IdentityTransformation'] = Field(alias='__typename', default='IdentityTransformation', exclude=True)

class TransformationChildMapAxisTransformation(TransformationChildBase, TransformationTrait, BaseModel):
    """A permutation of axes, mapping each input axis to an output axis by name"""
    typename: Literal['MapAxisTransformation'] = Field(alias='__typename', default='MapAxisTransformation', exclude=True)

class TransformationChildRotationTransformation(TransformationChildBase, TransformationTrait, BaseModel):
    """A rotation, given as an orthonormal matrix"""
    typename: Literal['RotationTransformation'] = Field(alias='__typename', default='RotationTransformation', exclude=True)
    affine: Tuple[Tuple[float, ...], ...]
    'The rotation matrix'

class TransformationChildScaleTransformation(TransformationChildBase, TransformationTrait, BaseModel):
    """A per-axis multiplication, with one entry per input axis"""
    typename: Literal['ScaleTransformation'] = Field(alias='__typename', default='ScaleTransformation', exclude=True)
    scale: Tuple[float, ...]
    "The per-axis scale factors, in the axis order of the input system, expressed in the units of the output system's axes (dimensionless between pixel systems, e.g. within a pyramid). Absolute, not relative to another level"

class TransformationChildSequenceTransformation(TransformationChildBase, TransformationTrait, BaseModel):
    """An ordered composition of child transformations, applied first to last"""
    typename: Literal['SequenceTransformation'] = Field(alias='__typename', default='SequenceTransformation', exclude=True)

class TransformationChildTranslationTransformation(TransformationChildBase, TransformationTrait, BaseModel):
    """A per-axis offset, with one entry per input axis"""
    typename: Literal['TranslationTransformation'] = Field(alias='__typename', default='TranslationTransformation', exclude=True)
    translation: Tuple[float, ...]
    'The per-axis offsets, in the axis order of the input system'

class TransformationChildUnmappableTransformation(TransformationChildBase, TransformationTrait, BaseModel):
    """A declared NON-correspondence: the two systems are related -- one was computed from the other -- and no point of either maps to a point of the other. It has no parameters, no rank and no matrix, and no placement search will walk it, in either direction. This is what a per-object measurement table's relation to the image it was measured from looks like"""
    typename: Literal['UnmappableTransformation'] = Field(alias='__typename', default='UnmappableTransformation', exclude=True)

class ChannelView(ViewChannelView, MikroFetchable, BaseModel):
    """A channel view describes an acquisition channel of an image, carrying its name and optical properties such as emission and excitation wavelengths."""
    typename: Literal['ChannelView'] = Field(alias='__typename', default='ChannelView', exclude=True)
    id: ID
    emission_wavelength: Optional[Length] = Field(default=None, alias='emissionWavelength')
    'The emission wavelength of the channel'
    excitation_wavelength: Optional[Length] = Field(default=None, alias='excitationWavelength')
    'The excitation wavelength of the channel'
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

class AnimationWaypoint(MikroFetchable, BaseModel):
    """One camera pose in a tour, and how the viewer travels to it"""
    typename: Literal['AnimationWaypoint'] = Field(alias='__typename', default='AnimationWaypoint', exclude=True)
    id: ID
    order: int
    "The pose's index in the tour. Written by enumeration when the tour is authored, so it always runs 0, 1, 2 ... with no gaps"
    name: str
    "What this stop shows, e.g. 'the nucleus'"
    duration_ms: int = Field(alias='durationMs')
    'How long the viewer takes to travel TO this pose, in milliseconds. Ignored for the first pose, which is where the tour starts'
    easing: Easing
    'How the viewer eases the camera along that travel'
    camera: CameraState
    "Where the camera is: a position keyed by the world's axis names, plus the flat and volumetric views of it"
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for AnimationWaypoint"""
        document = 'fragment CameraState on CameraState {\n  position\n  crossSectionOrientation\n  crossSectionScale\n  projectionOrientation\n  projectionScale\n  __typename\n}\n\nfragment AnimationWaypoint on AnimationWaypoint {\n  id\n  order\n  name\n  durationMs\n  easing\n  camera {\n    ...CameraState\n    __typename\n  }\n  __typename\n}'
        name = 'AnimationWaypoint'
        type = 'AnimationWaypoint'

class CoordinateSystem(CoordinateSystemTrait, MikroFetchable, BaseModel):
    """A named coordinate space: a node in the transformation graph. Its axes are ordered, and that order is the order of the array's dimensions"""
    typename: Literal['CoordinateSystem'] = Field(alias='__typename', default='CoordinateSystem', exclude=True)
    id: ID
    name: str
    epoch: Optional[datetime] = Field(default=None)
    "The wall-clock instant this system's time axis has its origin at: `wall_clock = epoch + t * unit`. A property of the space, not of any composition over it. Meaningful only for a unit-carrying system with a TIME axis (a shared world space); null when the clock is unanchored -- the time axis is still a perfectly composable relative coordinate"
    axes: Tuple[Axis, ...]
    "The system's axes, in array order (slowest-varying first). RFC-5 requires them ordered by type: time, then channel and custom types, then space"
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for CoordinateSystem"""
        document = 'fragment Axis on Axis {\n  id\n  order\n  name\n  type\n  unit\n  longName\n  __typename\n}\n\nfragment CoordinateSystem on CoordinateSystem {\n  id\n  name\n  epoch\n  axes {\n    ...Axis\n    __typename\n  }\n  __typename\n}'
        name = 'CoordinateSystem'
        type = 'CoordinateSystem'

class TimepointView(ViewTimepointView, MikroFetchable, BaseModel):
    """A view anchoring an image region in real time: it places the region within an era (a named time epoch on the microscope) at a time offset or frame index since its start."""
    typename: Literal['TimepointView'] = Field(alias='__typename', default='TimepointView', exclude=True)
    id: ID
    time_since_start: Optional[Duration] = Field(default=None, alias='timeSinceStart')
    index_since_start: Optional[int] = Field(default=None, alias='indexSinceStart')
    era: Era
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for TimepointView"""
        document = 'fragment Era on Era {\n  id\n  begin\n  name\n  __typename\n}\n\nfragment View on View {\n  xMin\n  xMax\n  yMin\n  yMax\n  tMin\n  tMax\n  cMin\n  cMax\n  zMin\n  zMax\n  __typename\n}\n\nfragment TimepointView on TimepointView {\n  ...View\n  id\n  timeSinceStart\n  indexSinceStart\n  era {\n    ...Era\n    __typename\n  }\n  __typename\n}'
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

class ADatasetDataarrays(DataArrayTrait, BaseModel):
    """One level of a dataset's resolution pyramid: a zarr-backed array, with its own voxel-index coordinate system and a stored edge into the dataset's intrinsic space"""
    typename: Literal['DataArray'] = Field(alias='__typename', default='DataArray', exclude=True)
    id: ID
    level: int
    shape: Tuple[int, ...]
    chunk_shape: Tuple[int, ...] = Field(alias='chunkShape')
    store: ZarrStore
    model_config = ConfigDict(frozen=True)

class ADataset(DatasetTrait, MikroFetchable, BaseModel):
    """A multi-dimensional array dataset. Its dimensions and their types live on the axes of its INTRINSIC (pixel grid) coordinate system; physical units live on the physical spaces it has edges into; its pyramid levels are DataArrays, each mapping into its grid"""
    typename: Literal['ADataset'] = Field(alias='__typename', default='ADataset', exclude=True)
    id: ID
    name: str
    axis_names: Tuple[str, ...] = Field(alias='axisNames')
    "The dataset's axis names, in array order. Derived from the axes of its intrinsic coordinate system"
    shape: Tuple[int, ...]
    "The dataset's shape: that of its level-0 array"
    multiscale: bool
    'Whether this dataset carries a resolution pyramid. Derived: true when it has more than one level'
    intrinsic_system: Optional[CoordinateSystem] = Field(default=None, alias='intrinsicSystem')
    "The dataset's INTRINSIC coordinate system: its level-0 pixel grid, the space every pyramid level and lens maps into and the space ROIs resolve against. Structural and unit-independent"
    data_arrays: Tuple[ADatasetDataarrays, ...] = Field(alias='dataArrays')
    'The multiscale data arrays belonging to this dataset'
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for ADataset"""
        document = 'fragment Axis on Axis {\n  id\n  order\n  name\n  type\n  unit\n  longName\n  __typename\n}\n\nfragment CoordinateSystem on CoordinateSystem {\n  id\n  name\n  epoch\n  axes {\n    ...Axis\n    __typename\n  }\n  __typename\n}\n\nfragment ZarrStore on ZarrStore {\n  id\n  key\n  bucket\n  path\n  __typename\n}\n\nfragment ADataset on ADataset {\n  id\n  name\n  axisNames\n  shape\n  multiscale\n  intrinsicSystem {\n    ...CoordinateSystem\n    __typename\n  }\n  dataArrays {\n    id\n    level\n    shape\n    chunkShape\n    store {\n      ...ZarrStore\n      __typename\n    }\n    __typename\n  }\n  __typename\n}'
        name = 'ADataset'
        type = 'ADataset'

class AnnotationCoordinates(BaseModel):
    """A discrete coordinate an annotation is pinned to, e.g. a timepoint or a channel"""
    typename: Literal['Coordinate'] = Field(alias='__typename', default='Coordinate', exclude=True)
    name: str
    "The name of the coordinate, e.g. 't' or 'c'"
    value: int
    'The value along that coordinate'
    model_config = ConfigDict(frozen=True)

class AnnotationIntrinsicbbox(BaseModel):
    """An axis-aligned bounding box, as a min and a max corner"""
    typename: Literal['BoundingBox'] = Field(alias='__typename', default='BoundingBox', exclude=True)
    min: Tuple[float, ...]
    'The lower corner, in the coordinate order of the coordinate system'
    max: Tuple[float, ...]
    'The upper corner, in the coordinate order of the coordinate system'
    model_config = ConfigDict(frozen=True)

class Annotation(MikroFetchable, BaseModel):
    """A human-drawn shape in an annotation collection's coordinate system. It belongs to the collection, not to a scene: delete the scene and the annotation survives"""
    typename: Literal['Annotation'] = Field(alias='__typename', default='Annotation', exclude=True)
    id: str
    name: str
    kind: RoiKind
    vectors: Tuple[Tuple[float, ...], ...]
    coordinates: Tuple[AnnotationCoordinates, ...]
    'The discrete coordinates this annotation is pinned to. A coordinate the annotation does not pin is one it spans'
    coordinate_system: Optional[CoordinateSystem] = Field(default=None, alias='coordinateSystem')
    "The coordinate system this annotation's vectors are expressed in: its collection's own system"
    intrinsic_bbox: Optional[AnnotationIntrinsicbbox] = Field(default=None, alias='intrinsicBbox')
    "The annotation's bounding box in the nearest intrinsic space, derived from every corner of its geometry (an affine-transformed box is not a box: min/max alone gives a strictly too-small answer under rotation or shear). Intrinsic, not world: world is scene-owned, and one collection can sit in two scenes under two registrations"
    stroke_color: Optional[Tuple[int, ...]] = Field(default=None, alias='strokeColor')
    'The stroke (outline) color of the geometry, as RGBA'
    fill_color: Optional[Tuple[int, ...]] = Field(default=None, alias='fillColor')
    'The fill color of the geometry, as RGBA, or null for no fill'
    stroke_width: float = Field(alias='strokeWidth')
    "The stroke width of the geometry, in the drawing space's units. One number for every direction, so it is a well-defined length only where that space's axes share a scale"
    filled: bool
    'Whether the geometry is filled with fill_color'
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for Annotation"""
        document = 'fragment Axis on Axis {\n  id\n  order\n  name\n  type\n  unit\n  longName\n  __typename\n}\n\nfragment CoordinateSystem on CoordinateSystem {\n  id\n  name\n  epoch\n  axes {\n    ...Axis\n    __typename\n  }\n  __typename\n}\n\nfragment Annotation on Annotation {\n  id\n  name\n  kind\n  vectors\n  coordinates {\n    name\n    value\n    __typename\n  }\n  coordinateSystem {\n    ...CoordinateSystem\n    __typename\n  }\n  intrinsicBbox {\n    min\n    max\n    __typename\n  }\n  strokeColor\n  fillColor\n  strokeWidth\n  filled\n  __typename\n}'
        name = 'Annotation'
        type = 'Annotation'

class LensDatasetDataarrays(DataArrayTrait, BaseModel):
    """One level of a dataset's resolution pyramid: a zarr-backed array, with its own voxel-index coordinate system and a stored edge into the dataset's intrinsic space"""
    typename: Literal['DataArray'] = Field(alias='__typename', default='DataArray', exclude=True)
    id: ID
    level: int
    store: ZarrStore
    model_config = ConfigDict(frozen=True)

class LensDataset(DatasetTrait, BaseModel):
    """A multi-dimensional array dataset. Its dimensions and their types live on the axes of its INTRINSIC (pixel grid) coordinate system; physical units live on the physical spaces it has edges into; its pyramid levels are DataArrays, each mapping into its grid"""
    typename: Literal['ADataset'] = Field(alias='__typename', default='ADataset', exclude=True)
    id: ID
    axis_names: Tuple[str, ...] = Field(alias='axisNames')
    "The dataset's axis names, in array order. Derived from the axes of its intrinsic coordinate system"
    data_arrays: Tuple[LensDatasetDataarrays, ...] = Field(alias='dataArrays')
    'The multiscale data arrays belonging to this dataset'
    model_config = ConfigDict(frozen=True)

class LensRenderaxes(BaseModel):
    """Which axis of a data source maps to screen x, y, z, time and intensity. Derived from the axis types, never stored"""
    typename: Literal['RenderAxes'] = Field(alias='__typename', default='RenderAxes', exclude=True)
    x: str
    'The axis mapped to screen x: the last (fastest-varying) spatial axis'
    y: str
    'The axis mapped to screen y: the second-to-last spatial axis'
    z: Optional[str] = Field(default=None)
    'The axis mapped to screen z: the third-to-last spatial axis, if the data is volumetric'
    t: Optional[str] = Field(default=None)
    'The time axis, if the data has one'
    intensity: Optional[str] = Field(default=None)
    'The channel axis, if the data has one'
    model_config = ConfigDict(frozen=True)

class Lens(Lensable, MikroFetchable, BaseModel):
    """A Lens is a way of looking at a dataset: a dimensional selection (slices) over a dataset that defines a view of its data"""
    typename: Literal['Lens'] = Field(alias='__typename', default='Lens', exclude=True)
    id: ID
    dataset: LensDataset
    shape: Tuple[int, ...]
    "The shape this lens' slices cut out of its dataset"
    axis_names: Tuple[str, ...] = Field(alias='axisNames')
    "The lens' axis names, in array order. A selection never drops or reorders an axis"
    coordinate_system: Optional[CoordinateSystem] = Field(default=None, alias='coordinateSystem')
    "The coordinate system the lens' selection is expressed in. A sliced lens owns one (the space its slices cut out, with the derived edge recording the shift); an unsliced lens selects everything, so this resolves to the dataset's INTRINSIC system"
    render_axes: LensRenderaxes = Field(alias='renderAxes')
    'Which axis of the data source maps to screen x, y, z, time and intensity. Derived from the axis types: spatial axes are in array order, so the last is x'
    slices: Tuple[Slice, ...]
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for Lens"""
        document = 'fragment Axis on Axis {\n  id\n  order\n  name\n  type\n  unit\n  longName\n  __typename\n}\n\nfragment CoordinateSystem on CoordinateSystem {\n  id\n  name\n  epoch\n  axes {\n    ...Axis\n    __typename\n  }\n  __typename\n}\n\nfragment Slice on Slice {\n  axis\n  start\n  stop\n  step\n  __typename\n}\n\nfragment ZarrStore on ZarrStore {\n  id\n  key\n  bucket\n  path\n  __typename\n}\n\nfragment Lens on Lens {\n  id\n  dataset {\n    id\n    axisNames\n    dataArrays {\n      id\n      level\n      store {\n        ...ZarrStore\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  shape\n  axisNames\n  coordinateSystem {\n    ...CoordinateSystem\n    __typename\n  }\n  renderAxes {\n    x\n    y\n    z\n    t\n    intensity\n    __typename\n  }\n  slices {\n    ...Slice\n    __typename\n  }\n  __typename\n}'
        name = 'Lens'
        type = 'Lens'

class Scene(SceneTrait, MikroFetchable, BaseModel):
    """A composition of layers over a shared world coordinate system. The scene carries no units of its own -- they are per-axis, on the axes of its world system"""
    typename: Literal['Scene'] = Field(alias='__typename', default='Scene', exclude=True)
    name: str
    id: ID
    preferred_view: PreferredView = Field(alias='preferredView')
    'How a viewer should open this scene: flat, volumetric, or its own choice. A preference, not a constraint -- nothing server-side reads it, and a viewer that cannot render volumes is not wrong to show the slice view'
    background_color: Optional[Tuple[float, ...]] = Field(default=None, alias='backgroundColor')
    'The viewer background, as RGBA. Null lets the viewer use its own'
    world_coordinate_system: CoordinateSystem = Field(alias='worldCoordinateSystem')
    'The shared space this scene composes its layers over. Never owned by the scene: many scenes can share it, it outlives each of them, and deleting a scene never deletes it'
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for Scene"""
        document = 'fragment Axis on Axis {\n  id\n  order\n  name\n  type\n  unit\n  longName\n  __typename\n}\n\nfragment CoordinateSystem on CoordinateSystem {\n  id\n  name\n  epoch\n  axes {\n    ...Axis\n    __typename\n  }\n  __typename\n}\n\nfragment Scene on Scene {\n  name\n  id\n  preferredView\n  backgroundColor\n  worldCoordinateSystem {\n    ...CoordinateSystem\n    __typename\n  }\n  __typename\n}'
        name = 'Scene'
        type = 'Scene'

class TransformationSequencechildrenBase(BaseModel):
    """A directed edge of the coordinate graph, mapping `input` to `output`. Direction is always forward. The concrete kind (Scale, Translation, Affine, Sequence, ...) carries the parameters"""
    model_config = ConfigDict(frozen=True)

class TransformationSequencechildrenBaseAffineTransformation(TransformationChildAffineTransformation, TransformationSequencechildrenBase, TransformationTrait, BaseModel):
    """A general affine map, given as an M x (N+1) matrix with rows outermost"""
    typename: Literal['AffineTransformation'] = Field(alias='__typename', default='AffineTransformation', exclude=True)

class TransformationSequencechildrenBaseBijectionTransformation(TransformationChildBijectionTransformation, TransformationSequencechildrenBase, TransformationTrait, BaseModel):
    """A pair of child transformations giving an explicit forward and inverse map"""
    typename: Literal['BijectionTransformation'] = Field(alias='__typename', default='BijectionTransformation', exclude=True)

class TransformationSequencechildrenBaseByDimensionTransformation(TransformationChildByDimensionTransformation, TransformationSequencechildrenBase, TransformationTrait, BaseModel):
    """A composition of child transformations, each acting on a named subset of the axes"""
    typename: Literal['ByDimensionTransformation'] = Field(alias='__typename', default='ByDimensionTransformation', exclude=True)

class TransformationSequencechildrenBaseFieldTransformation(TransformationChildFieldTransformation, TransformationSequencechildrenBase, TransformationTrait, BaseModel):
    """A non-affine map given by the values of an array rather than by a formula. The array is a `field`: a node of this graph, not a payload on this edge, so it keeps its own lineage and its axes say what its numbers mean. It has no closed-form inverse, so a placement path never walks it backwards"""
    typename: Literal['FieldTransformation'] = Field(alias='__typename', default='FieldTransformation', exclude=True)

class TransformationSequencechildrenBaseIdentityTransformation(TransformationChildIdentityTransformation, TransformationSequencechildrenBase, TransformationTrait, BaseModel):
    """The identity map: input and output coordinates are the same"""
    typename: Literal['IdentityTransformation'] = Field(alias='__typename', default='IdentityTransformation', exclude=True)

class TransformationSequencechildrenBaseMapAxisTransformation(TransformationChildMapAxisTransformation, TransformationSequencechildrenBase, TransformationTrait, BaseModel):
    """A permutation of axes, mapping each input axis to an output axis by name"""
    typename: Literal['MapAxisTransformation'] = Field(alias='__typename', default='MapAxisTransformation', exclude=True)

class TransformationSequencechildrenBaseRotationTransformation(TransformationChildRotationTransformation, TransformationSequencechildrenBase, TransformationTrait, BaseModel):
    """A rotation, given as an orthonormal matrix"""
    typename: Literal['RotationTransformation'] = Field(alias='__typename', default='RotationTransformation', exclude=True)

class TransformationSequencechildrenBaseScaleTransformation(TransformationChildScaleTransformation, TransformationSequencechildrenBase, TransformationTrait, BaseModel):
    """A per-axis multiplication, with one entry per input axis"""
    typename: Literal['ScaleTransformation'] = Field(alias='__typename', default='ScaleTransformation', exclude=True)

class TransformationSequencechildrenBaseSequenceTransformation(TransformationChildSequenceTransformation, TransformationSequencechildrenBase, TransformationTrait, BaseModel):
    """An ordered composition of child transformations, applied first to last"""
    typename: Literal['SequenceTransformation'] = Field(alias='__typename', default='SequenceTransformation', exclude=True)

class TransformationSequencechildrenBaseTranslationTransformation(TransformationChildTranslationTransformation, TransformationSequencechildrenBase, TransformationTrait, BaseModel):
    """A per-axis offset, with one entry per input axis"""
    typename: Literal['TranslationTransformation'] = Field(alias='__typename', default='TranslationTransformation', exclude=True)

class TransformationSequencechildrenBaseUnmappableTransformation(TransformationChildUnmappableTransformation, TransformationSequencechildrenBase, TransformationTrait, BaseModel):
    """A declared NON-correspondence: the two systems are related -- one was computed from the other -- and no point of either maps to a point of the other. It has no parameters, no rank and no matrix, and no placement search will walk it, in either direction. This is what a per-object measurement table's relation to the image it was measured from looks like"""
    typename: Literal['UnmappableTransformation'] = Field(alias='__typename', default='UnmappableTransformation', exclude=True)

class TransformationSequencechildrenBaseCatchAll(TransformationSequencechildrenBase, BaseModel):
    """Catch all class for TransformationSequencechildrenBase"""
    typename: str = Field(alias='__typename', exclude=True)

class TransformationBydimensionchildrenBase(BaseModel):
    """A directed edge of the coordinate graph, mapping `input` to `output`. Direction is always forward. The concrete kind (Scale, Translation, Affine, Sequence, ...) carries the parameters"""
    model_config = ConfigDict(frozen=True)

class TransformationBydimensionchildrenBaseAffineTransformation(TransformationChildAffineTransformation, TransformationBydimensionchildrenBase, TransformationTrait, BaseModel):
    """A general affine map, given as an M x (N+1) matrix with rows outermost"""
    typename: Literal['AffineTransformation'] = Field(alias='__typename', default='AffineTransformation', exclude=True)

class TransformationBydimensionchildrenBaseBijectionTransformation(TransformationChildBijectionTransformation, TransformationBydimensionchildrenBase, TransformationTrait, BaseModel):
    """A pair of child transformations giving an explicit forward and inverse map"""
    typename: Literal['BijectionTransformation'] = Field(alias='__typename', default='BijectionTransformation', exclude=True)

class TransformationBydimensionchildrenBaseByDimensionTransformation(TransformationChildByDimensionTransformation, TransformationBydimensionchildrenBase, TransformationTrait, BaseModel):
    """A composition of child transformations, each acting on a named subset of the axes"""
    typename: Literal['ByDimensionTransformation'] = Field(alias='__typename', default='ByDimensionTransformation', exclude=True)

class TransformationBydimensionchildrenBaseFieldTransformation(TransformationChildFieldTransformation, TransformationBydimensionchildrenBase, TransformationTrait, BaseModel):
    """A non-affine map given by the values of an array rather than by a formula. The array is a `field`: a node of this graph, not a payload on this edge, so it keeps its own lineage and its axes say what its numbers mean. It has no closed-form inverse, so a placement path never walks it backwards"""
    typename: Literal['FieldTransformation'] = Field(alias='__typename', default='FieldTransformation', exclude=True)

class TransformationBydimensionchildrenBaseIdentityTransformation(TransformationChildIdentityTransformation, TransformationBydimensionchildrenBase, TransformationTrait, BaseModel):
    """The identity map: input and output coordinates are the same"""
    typename: Literal['IdentityTransformation'] = Field(alias='__typename', default='IdentityTransformation', exclude=True)

class TransformationBydimensionchildrenBaseMapAxisTransformation(TransformationChildMapAxisTransformation, TransformationBydimensionchildrenBase, TransformationTrait, BaseModel):
    """A permutation of axes, mapping each input axis to an output axis by name"""
    typename: Literal['MapAxisTransformation'] = Field(alias='__typename', default='MapAxisTransformation', exclude=True)

class TransformationBydimensionchildrenBaseRotationTransformation(TransformationChildRotationTransformation, TransformationBydimensionchildrenBase, TransformationTrait, BaseModel):
    """A rotation, given as an orthonormal matrix"""
    typename: Literal['RotationTransformation'] = Field(alias='__typename', default='RotationTransformation', exclude=True)

class TransformationBydimensionchildrenBaseScaleTransformation(TransformationChildScaleTransformation, TransformationBydimensionchildrenBase, TransformationTrait, BaseModel):
    """A per-axis multiplication, with one entry per input axis"""
    typename: Literal['ScaleTransformation'] = Field(alias='__typename', default='ScaleTransformation', exclude=True)

class TransformationBydimensionchildrenBaseSequenceTransformation(TransformationChildSequenceTransformation, TransformationBydimensionchildrenBase, TransformationTrait, BaseModel):
    """An ordered composition of child transformations, applied first to last"""
    typename: Literal['SequenceTransformation'] = Field(alias='__typename', default='SequenceTransformation', exclude=True)

class TransformationBydimensionchildrenBaseTranslationTransformation(TransformationChildTranslationTransformation, TransformationBydimensionchildrenBase, TransformationTrait, BaseModel):
    """A per-axis offset, with one entry per input axis"""
    typename: Literal['TranslationTransformation'] = Field(alias='__typename', default='TranslationTransformation', exclude=True)

class TransformationBydimensionchildrenBaseUnmappableTransformation(TransformationChildUnmappableTransformation, TransformationBydimensionchildrenBase, TransformationTrait, BaseModel):
    """A declared NON-correspondence: the two systems are related -- one was computed from the other -- and no point of either maps to a point of the other. It has no parameters, no rank and no matrix, and no placement search will walk it, in either direction. This is what a per-object measurement table's relation to the image it was measured from looks like"""
    typename: Literal['UnmappableTransformation'] = Field(alias='__typename', default='UnmappableTransformation', exclude=True)

class TransformationBydimensionchildrenBaseCatchAll(TransformationBydimensionchildrenBase, BaseModel):
    """Catch all class for TransformationBydimensionchildrenBase"""
    typename: str = Field(alias='__typename', exclude=True)

class TransformationBijectionchildrenBase(BaseModel):
    """A directed edge of the coordinate graph, mapping `input` to `output`. Direction is always forward. The concrete kind (Scale, Translation, Affine, Sequence, ...) carries the parameters"""
    model_config = ConfigDict(frozen=True)

class TransformationBijectionchildrenBaseAffineTransformation(TransformationChildAffineTransformation, TransformationBijectionchildrenBase, TransformationTrait, BaseModel):
    """A general affine map, given as an M x (N+1) matrix with rows outermost"""
    typename: Literal['AffineTransformation'] = Field(alias='__typename', default='AffineTransformation', exclude=True)

class TransformationBijectionchildrenBaseBijectionTransformation(TransformationChildBijectionTransformation, TransformationBijectionchildrenBase, TransformationTrait, BaseModel):
    """A pair of child transformations giving an explicit forward and inverse map"""
    typename: Literal['BijectionTransformation'] = Field(alias='__typename', default='BijectionTransformation', exclude=True)

class TransformationBijectionchildrenBaseByDimensionTransformation(TransformationChildByDimensionTransformation, TransformationBijectionchildrenBase, TransformationTrait, BaseModel):
    """A composition of child transformations, each acting on a named subset of the axes"""
    typename: Literal['ByDimensionTransformation'] = Field(alias='__typename', default='ByDimensionTransformation', exclude=True)

class TransformationBijectionchildrenBaseFieldTransformation(TransformationChildFieldTransformation, TransformationBijectionchildrenBase, TransformationTrait, BaseModel):
    """A non-affine map given by the values of an array rather than by a formula. The array is a `field`: a node of this graph, not a payload on this edge, so it keeps its own lineage and its axes say what its numbers mean. It has no closed-form inverse, so a placement path never walks it backwards"""
    typename: Literal['FieldTransformation'] = Field(alias='__typename', default='FieldTransformation', exclude=True)

class TransformationBijectionchildrenBaseIdentityTransformation(TransformationChildIdentityTransformation, TransformationBijectionchildrenBase, TransformationTrait, BaseModel):
    """The identity map: input and output coordinates are the same"""
    typename: Literal['IdentityTransformation'] = Field(alias='__typename', default='IdentityTransformation', exclude=True)

class TransformationBijectionchildrenBaseMapAxisTransformation(TransformationChildMapAxisTransformation, TransformationBijectionchildrenBase, TransformationTrait, BaseModel):
    """A permutation of axes, mapping each input axis to an output axis by name"""
    typename: Literal['MapAxisTransformation'] = Field(alias='__typename', default='MapAxisTransformation', exclude=True)

class TransformationBijectionchildrenBaseRotationTransformation(TransformationChildRotationTransformation, TransformationBijectionchildrenBase, TransformationTrait, BaseModel):
    """A rotation, given as an orthonormal matrix"""
    typename: Literal['RotationTransformation'] = Field(alias='__typename', default='RotationTransformation', exclude=True)

class TransformationBijectionchildrenBaseScaleTransformation(TransformationChildScaleTransformation, TransformationBijectionchildrenBase, TransformationTrait, BaseModel):
    """A per-axis multiplication, with one entry per input axis"""
    typename: Literal['ScaleTransformation'] = Field(alias='__typename', default='ScaleTransformation', exclude=True)

class TransformationBijectionchildrenBaseSequenceTransformation(TransformationChildSequenceTransformation, TransformationBijectionchildrenBase, TransformationTrait, BaseModel):
    """An ordered composition of child transformations, applied first to last"""
    typename: Literal['SequenceTransformation'] = Field(alias='__typename', default='SequenceTransformation', exclude=True)

class TransformationBijectionchildrenBaseTranslationTransformation(TransformationChildTranslationTransformation, TransformationBijectionchildrenBase, TransformationTrait, BaseModel):
    """A per-axis offset, with one entry per input axis"""
    typename: Literal['TranslationTransformation'] = Field(alias='__typename', default='TranslationTransformation', exclude=True)

class TransformationBijectionchildrenBaseUnmappableTransformation(TransformationChildUnmappableTransformation, TransformationBijectionchildrenBase, TransformationTrait, BaseModel):
    """A declared NON-correspondence: the two systems are related -- one was computed from the other -- and no point of either maps to a point of the other. It has no parameters, no rank and no matrix, and no placement search will walk it, in either direction. This is what a per-object measurement table's relation to the image it was measured from looks like"""
    typename: Literal['UnmappableTransformation'] = Field(alias='__typename', default='UnmappableTransformation', exclude=True)

class TransformationBijectionchildrenBaseCatchAll(TransformationBijectionchildrenBase, BaseModel):
    """Catch all class for TransformationBijectionchildrenBase"""
    typename: str = Field(alias='__typename', exclude=True)

class TransformationBase(BaseModel):
    """A directed edge of the coordinate graph, mapping `input` to `output`. Direction is always forward. The concrete kind (Scale, Translation, Affine, Sequence, ...) carries the parameters"""
    id: ID
    kind: TransformKind
    name: Optional[str] = Field(default=None)
    version: int
    input: Optional[CoordinateSystem] = Field(default=None)
    output: Optional[CoordinateSystem] = Field(default=None)

class TransformationCatch(TransformationBase):
    """Catch all class for TransformationBase"""
    typename: str = Field(alias='__typename', exclude=True)
    'A directed edge of the coordinate graph, mapping `input` to `output`. Direction is always forward. The concrete kind (Scale, Translation, Affine, Sequence, ...) carries the parameters'
    id: ID
    kind: TransformKind
    name: Optional[str] = Field(default=None)
    version: int
    input: Optional[CoordinateSystem] = Field(default=None)
    output: Optional[CoordinateSystem] = Field(default=None)

class TransformationAffineTransformation(TransformationBase, TransformationTrait, BaseModel):
    """A general affine map, given as an M x (N+1) matrix with rows outermost"""
    typename: Literal['AffineTransformation'] = Field(alias='__typename', default='AffineTransformation', exclude=True)
    affine: Tuple[Tuple[float, ...], ...]
    'The affine matrix, M x (N+1), rows outermost. The last column is the translation'

class TransformationBijectionTransformation(TransformationBase, TransformationTrait, BaseModel):
    """A pair of child transformations giving an explicit forward and inverse map"""
    typename: Literal['BijectionTransformation'] = Field(alias='__typename', default='BijectionTransformation', exclude=True)
    bijection_children: Tuple[Union[Annotated[Union[TransformationBijectionchildrenBaseAffineTransformation, TransformationBijectionchildrenBaseBijectionTransformation, TransformationBijectionchildrenBaseByDimensionTransformation, TransformationBijectionchildrenBaseFieldTransformation, TransformationBijectionchildrenBaseIdentityTransformation, TransformationBijectionchildrenBaseMapAxisTransformation, TransformationBijectionchildrenBaseRotationTransformation, TransformationBijectionchildrenBaseScaleTransformation, TransformationBijectionchildrenBaseSequenceTransformation, TransformationBijectionchildrenBaseTranslationTransformation, TransformationBijectionchildrenBaseUnmappableTransformation], Field(discriminator='typename')], TransformationBijectionchildrenBaseCatchAll], ...] = Field(alias='bijectionChildren')
    'The forward transformation (order 0) and its inverse (order 1)'

class TransformationByDimensionTransformation(TransformationBase, TransformationTrait, BaseModel):
    """A composition of child transformations, each acting on a named subset of the axes"""
    typename: Literal['ByDimensionTransformation'] = Field(alias='__typename', default='ByDimensionTransformation', exclude=True)
    input_axes: Tuple[str, ...] = Field(alias='inputAxes')
    "The names of the input axes this edge's parameters are ordered by. `scale`, `translation` and the columns of `affine` follow this order -- which is the input system's axis order, NOT the reading layer's axis names, and the two differ often enough that indexing the arrays against them silently misplaces them. A BY_DIMENSION edge names only the subset of axes it acts on; the axes it does not name are the ones it leaves untouched"
    output_axes: Tuple[str, ...] = Field(alias='outputAxes')
    "The names of the output axes this edge produces. For a rank-changing BY_DIMENSION edge (placing a (c,y,x) dataset into a (t,z,y,x) world) this is the subset it maps onto; the world's other axes are untouched"
    by_dimension_children: Tuple[Union[Annotated[Union[TransformationBydimensionchildrenBaseAffineTransformation, TransformationBydimensionchildrenBaseBijectionTransformation, TransformationBydimensionchildrenBaseByDimensionTransformation, TransformationBydimensionchildrenBaseFieldTransformation, TransformationBydimensionchildrenBaseIdentityTransformation, TransformationBydimensionchildrenBaseMapAxisTransformation, TransformationBydimensionchildrenBaseRotationTransformation, TransformationBydimensionchildrenBaseScaleTransformation, TransformationBydimensionchildrenBaseSequenceTransformation, TransformationBydimensionchildrenBaseTranslationTransformation, TransformationBydimensionchildrenBaseUnmappableTransformation], Field(discriminator='typename')], TransformationBydimensionchildrenBaseCatchAll], ...] = Field(alias='byDimensionChildren')
    'The child transformations. Each carries the `inputAxes` and `outputAxes` it acts on'

class TransformationFieldTransformation(TransformationBase, TransformationTrait, BaseModel):
    """A non-affine map given by the values of an array rather than by a formula. The array is a `field`: a node of this graph, not a payload on this edge, so it keeps its own lineage and its axes say what its numbers mean. It has no closed-form inverse, so a placement path never walks it backwards"""
    typename: Literal['FieldTransformation'] = Field(alias='__typename', default='FieldTransformation', exclude=True)
    field: Optional[CoordinateSystem] = Field(default=None)
    "The coordinate system of the array whose values are this map. Its value axis says what they mean: COORDINATE for absolute positions, DISPLACEMENT for offsets, none at all for a scalar array whose single value is a position. Equal to `input` when the array's own pixels are the map, as for a label mask keying a table of objects"

class TransformationIdentityTransformation(TransformationBase, TransformationTrait, BaseModel):
    """The identity map: input and output coordinates are the same"""
    typename: Literal['IdentityTransformation'] = Field(alias='__typename', default='IdentityTransformation', exclude=True)

class TransformationMapAxisTransformation(TransformationBase, TransformationTrait, BaseModel):
    """A permutation of axes, mapping each input axis to an output axis by name"""
    typename: Literal['MapAxisTransformation'] = Field(alias='__typename', default='MapAxisTransformation', exclude=True)
    input_axes: Tuple[str, ...] = Field(alias='inputAxes')
    'The names of the input axes, positionally matched to `outputAxes`'
    output_axes: Tuple[str, ...] = Field(alias='outputAxes')
    'The names of the output axes, positionally matched to `inputAxes`'

class TransformationRotationTransformation(TransformationBase, TransformationTrait, BaseModel):
    """A rotation, given as an orthonormal matrix"""
    typename: Literal['RotationTransformation'] = Field(alias='__typename', default='RotationTransformation', exclude=True)
    affine: Tuple[Tuple[float, ...], ...]
    'The rotation matrix'

class TransformationScaleTransformation(TransformationBase, TransformationTrait, BaseModel):
    """A per-axis multiplication, with one entry per input axis"""
    typename: Literal['ScaleTransformation'] = Field(alias='__typename', default='ScaleTransformation', exclude=True)
    scale: Tuple[float, ...]
    "The per-axis scale factors, in the axis order of the input system, expressed in the units of the output system's axes (dimensionless between pixel systems, e.g. within a pyramid). Absolute, not relative to another level"

class TransformationSequenceTransformation(TransformationBase, TransformationTrait, BaseModel):
    """An ordered composition of child transformations, applied first to last"""
    typename: Literal['SequenceTransformation'] = Field(alias='__typename', default='SequenceTransformation', exclude=True)
    sequence_children: Tuple[Union[Annotated[Union[TransformationSequencechildrenBaseAffineTransformation, TransformationSequencechildrenBaseBijectionTransformation, TransformationSequencechildrenBaseByDimensionTransformation, TransformationSequencechildrenBaseFieldTransformation, TransformationSequencechildrenBaseIdentityTransformation, TransformationSequencechildrenBaseMapAxisTransformation, TransformationSequencechildrenBaseRotationTransformation, TransformationSequencechildrenBaseScaleTransformation, TransformationSequencechildrenBaseSequenceTransformation, TransformationSequencechildrenBaseTranslationTransformation, TransformationSequencechildrenBaseUnmappableTransformation], Field(discriminator='typename')], TransformationSequencechildrenBaseCatchAll], ...] = Field(alias='sequenceChildren')
    'The child transformations, applied first to last. They omit their own input and output: the sequence supplies them'

class TransformationTranslationTransformation(TransformationBase, TransformationTrait, BaseModel):
    """A per-axis offset, with one entry per input axis"""
    typename: Literal['TranslationTransformation'] = Field(alias='__typename', default='TranslationTransformation', exclude=True)
    translation: Tuple[float, ...]
    'The per-axis offsets, in the axis order of the input system'

class TransformationUnmappableTransformation(TransformationBase, TransformationTrait, BaseModel):
    """A declared NON-correspondence: the two systems are related -- one was computed from the other -- and no point of either maps to a point of the other. It has no parameters, no rank and no matrix, and no placement search will walk it, in either direction. This is what a per-object measurement table's relation to the image it was measured from looks like"""
    typename: Literal['UnmappableTransformation'] = Field(alias='__typename', default='UnmappableTransformation', exclude=True)

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
    """A view anchoring an image region in real time: it places the region within an era (a named time epoch on the microscope) at a time offset or frame index since its start."""
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
        document = 'fragment Era on Era {\n  id\n  begin\n  name\n  __typename\n}\n\nfragment ReferenceView on ReferenceView {\n  ...View\n  id\n  __typename\n}\n\nfragment View on View {\n  xMin\n  xMax\n  yMin\n  yMax\n  tMin\n  tMax\n  cMin\n  cMax\n  zMin\n  zMax\n  __typename\n}\n\nfragment AcquisitionView on AcquisitionView {\n  ...View\n  id\n  description\n  acquiredAt\n  operator {\n    sub\n    __typename\n  }\n  __typename\n}\n\nfragment AffineTransformationView on AffineTransformationView {\n  ...View\n  id\n  affineMatrix\n  stage {\n    id\n    name\n    __typename\n  }\n  __typename\n}\n\nfragment ChannelView on ChannelView {\n  ...View\n  id\n  emissionWavelength\n  excitationWavelength\n  __typename\n}\n\nfragment ContinousScanView on ContinousScanView {\n  ...View\n  id\n  direction\n  __typename\n}\n\nfragment DerivedView on DerivedView {\n  ...View\n  id\n  originImage {\n    id\n    name\n    __typename\n  }\n  __typename\n}\n\nfragment FileView on FileView {\n  ...View\n  id\n  seriesIdentifier\n  file {\n    id\n    name\n    __typename\n  }\n  __typename\n}\n\nfragment InstanceMaskView on InstanceMaskView {\n  ...View\n  id\n  referenceView {\n    ...ReferenceView\n    __typename\n  }\n  __typename\n}\n\nfragment MaskView on MaskView {\n  ...View\n  id\n  referenceView {\n    ...ReferenceView\n    __typename\n  }\n  __typename\n}\n\nfragment OpticsView on OpticsView {\n  ...View\n  id\n  objective {\n    id\n    name\n    serialNumber\n    __typename\n  }\n  camera {\n    id\n    name\n    serialNumber\n    __typename\n  }\n  instrument {\n    id\n    name\n    serialNumber\n    __typename\n  }\n  __typename\n}\n\nfragment RGBView on RGBView {\n  ...View\n  id\n  contexts {\n    id\n    name\n    __typename\n  }\n  name\n  image {\n    id\n    store {\n      ...ZarrStore\n      __typename\n    }\n    derivedScaleViews {\n      id\n      image {\n        id\n        store {\n          ...ZarrStore\n          __typename\n        }\n        __typename\n      }\n      scaleX\n      scaleY\n      scaleZ\n      scaleT\n      scaleC\n      __typename\n    }\n    __typename\n  }\n  colorMap\n  contrastLimitMin\n  contrastLimitMax\n  gamma\n  active\n  fullColour\n  baseColor\n  __typename\n}\n\nfragment ROIView on ROIView {\n  ...View\n  id\n  roi {\n    id\n    name\n    __typename\n  }\n  __typename\n}\n\nfragment TimepointView on TimepointView {\n  ...View\n  id\n  timeSinceStart\n  indexSinceStart\n  era {\n    ...Era\n    __typename\n  }\n  __typename\n}\n\nfragment WellPositionView on WellPositionView {\n  ...View\n  id\n  column\n  row\n  well {\n    id\n    rows\n    columns\n    name\n    __typename\n  }\n  __typename\n}\n\nfragment ZarrStore on ZarrStore {\n  id\n  key\n  bucket\n  path\n  __typename\n}\n\nfragment Image on Image {\n  id\n  name\n  store {\n    ...ZarrStore\n    __typename\n  }\n  views {\n    ...ChannelView\n    ...AffineTransformationView\n    ...TimepointView\n    ...OpticsView\n    ...AcquisitionView\n    ...RGBView\n    ...WellPositionView\n    ...DerivedView\n    ...ROIView\n    ...FileView\n    ...ContinousScanView\n    __typename\n  }\n  maskViews {\n    ...MaskView\n    __typename\n  }\n  instanceMaskViews {\n    ...InstanceMaskView\n    __typename\n  }\n  rgbContexts {\n    id\n    name\n    views {\n      ...RGBView\n      __typename\n    }\n    __typename\n  }\n  __typename\n}'
        name = 'Image'
        type = 'Image'

class AnnotationCollection(MikroFetchable, BaseModel):
    """A named set of human-drawn annotations, owning the coordinate system they are drawn in. The CRUD counterpart of a table dataset's machine-produced rows: shapes a person draws and edits, sharing one drawing space and one registration story"""
    typename: Literal['AnnotationCollection'] = Field(alias='__typename', default='AnnotationCollection', exclude=True)
    id: ID
    name: str
    description: Optional[str] = Field(default=None)
    coordinate_system: CoordinateSystem = Field(alias='coordinateSystem')
    "The coordinate system the annotations' vectors are expressed in. The collection owns it; `derivedFrom` relates it to whatever the shapes are drawn over"
    annotations: Tuple[Annotation, ...]
    'The annotations in this collection'
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for AnnotationCollection"""
        document = 'fragment Axis on Axis {\n  id\n  order\n  name\n  type\n  unit\n  longName\n  __typename\n}\n\nfragment Annotation on Annotation {\n  id\n  name\n  kind\n  vectors\n  coordinates {\n    name\n    value\n    __typename\n  }\n  coordinateSystem {\n    ...CoordinateSystem\n    __typename\n  }\n  intrinsicBbox {\n    min\n    max\n    __typename\n  }\n  strokeColor\n  fillColor\n  strokeWidth\n  filled\n  __typename\n}\n\nfragment CoordinateSystem on CoordinateSystem {\n  id\n  name\n  epoch\n  axes {\n    ...Axis\n    __typename\n  }\n  __typename\n}\n\nfragment AnnotationCollection on AnnotationCollection {\n  id\n  name\n  description\n  coordinateSystem {\n    ...CoordinateSystem\n    __typename\n  }\n  annotations {\n    ...Annotation\n    __typename\n  }\n  __typename\n}'
        name = 'AnnotationCollection'
        type = 'AnnotationCollection'

class Animation(MikroFetchable, BaseModel):
    """A named camera tour of a scene: the poses a viewer pans through, in order. A view artifact -- it cascades with the scene, no placement walk crosses it, and refining a registration moves the data but never the camera"""
    typename: Literal['Animation'] = Field(alias='__typename', default='Animation', exclude=True)
    id: ID
    name: str
    description: Optional[str] = Field(default=None)
    scene: Scene
    'The scene this tour flies through'
    waypoints: Tuple[AnimationWaypoint, ...]
    'The poses the viewer pans through, in tour order'
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for Animation"""
        document = 'fragment Axis on Axis {\n  id\n  order\n  name\n  type\n  unit\n  longName\n  __typename\n}\n\nfragment CameraState on CameraState {\n  position\n  crossSectionOrientation\n  crossSectionScale\n  projectionOrientation\n  projectionScale\n  __typename\n}\n\nfragment CoordinateSystem on CoordinateSystem {\n  id\n  name\n  epoch\n  axes {\n    ...Axis\n    __typename\n  }\n  __typename\n}\n\nfragment AnimationWaypoint on AnimationWaypoint {\n  id\n  order\n  name\n  durationMs\n  easing\n  camera {\n    ...CameraState\n    __typename\n  }\n  __typename\n}\n\nfragment Scene on Scene {\n  name\n  id\n  preferredView\n  backgroundColor\n  worldCoordinateSystem {\n    ...CoordinateSystem\n    __typename\n  }\n  __typename\n}\n\nfragment Animation on Animation {\n  id\n  name\n  description\n  scene {\n    ...Scene\n    __typename\n  }\n  waypoints {\n    ...AnimationWaypoint\n    __typename\n  }\n  __typename\n}'
        name = 'Animation'
        type = 'Animation'

class SceneSnapshot(MikroFetchable, BaseModel):
    """A pre-rendered picture of a composition: every layer of the scene, blended. Clients use snapshots to preview without compositing the layers themselves. A picture of the scene, not of any one dataset in it -- though `ADataset.latestSnapshot` will offer one of these where the scene's only anchored dataset is that dataset, since then the picture shows it and nothing else"""
    typename: Literal['SceneSnapshot'] = Field(alias='__typename', default='SceneSnapshot', exclude=True)
    id: ID
    name: str
    major_color: Optional[Tuple[float, ...]] = Field(default=None, alias='majorColor')
    'The dominant color of the image, for tinting a placeholder while it loads'
    scene: Scene
    'The composition this is a picture of'
    store: MediaStore
    'The media store holding the rendered image. Ask it for a presignedUrl or an accessGrant to actually fetch the bytes'
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for SceneSnapshot"""
        document = 'fragment Axis on Axis {\n  id\n  order\n  name\n  type\n  unit\n  longName\n  __typename\n}\n\nfragment CoordinateSystem on CoordinateSystem {\n  id\n  name\n  epoch\n  axes {\n    ...Axis\n    __typename\n  }\n  __typename\n}\n\nfragment MediaStore on MediaStore {\n  id\n  key\n  bucket\n  path\n  __typename\n}\n\nfragment Scene on Scene {\n  name\n  id\n  preferredView\n  backgroundColor\n  worldCoordinateSystem {\n    ...CoordinateSystem\n    __typename\n  }\n  __typename\n}\n\nfragment SceneSnapshot on SceneSnapshot {\n  id\n  name\n  majorColor\n  scene {\n    ...Scene\n    __typename\n  }\n  store {\n    ...MediaStore\n    __typename\n  }\n  __typename\n}'
        name = 'SceneSnapshot'
        type = 'SceneSnapshot'

class MeshCollectionDerivedfromBase(BaseModel):
    """A directed edge of the coordinate graph, mapping `input` to `output`. Direction is always forward. The concrete kind (Scale, Translation, Affine, Sequence, ...) carries the parameters"""
    model_config = ConfigDict(frozen=True)

class MeshCollectionDerivedfromBaseAffineTransformation(TransformationAffineTransformation, MeshCollectionDerivedfromBase, TransformationTrait, BaseModel):
    """A general affine map, given as an M x (N+1) matrix with rows outermost"""
    typename: Literal['AffineTransformation'] = Field(alias='__typename', default='AffineTransformation', exclude=True)

class MeshCollectionDerivedfromBaseBijectionTransformation(TransformationBijectionTransformation, MeshCollectionDerivedfromBase, TransformationTrait, BaseModel):
    """A pair of child transformations giving an explicit forward and inverse map"""
    typename: Literal['BijectionTransformation'] = Field(alias='__typename', default='BijectionTransformation', exclude=True)

class MeshCollectionDerivedfromBaseByDimensionTransformation(TransformationByDimensionTransformation, MeshCollectionDerivedfromBase, TransformationTrait, BaseModel):
    """A composition of child transformations, each acting on a named subset of the axes"""
    typename: Literal['ByDimensionTransformation'] = Field(alias='__typename', default='ByDimensionTransformation', exclude=True)

class MeshCollectionDerivedfromBaseFieldTransformation(TransformationFieldTransformation, MeshCollectionDerivedfromBase, TransformationTrait, BaseModel):
    """A non-affine map given by the values of an array rather than by a formula. The array is a `field`: a node of this graph, not a payload on this edge, so it keeps its own lineage and its axes say what its numbers mean. It has no closed-form inverse, so a placement path never walks it backwards"""
    typename: Literal['FieldTransformation'] = Field(alias='__typename', default='FieldTransformation', exclude=True)

class MeshCollectionDerivedfromBaseIdentityTransformation(TransformationIdentityTransformation, MeshCollectionDerivedfromBase, TransformationTrait, BaseModel):
    """The identity map: input and output coordinates are the same"""
    typename: Literal['IdentityTransformation'] = Field(alias='__typename', default='IdentityTransformation', exclude=True)

class MeshCollectionDerivedfromBaseMapAxisTransformation(TransformationMapAxisTransformation, MeshCollectionDerivedfromBase, TransformationTrait, BaseModel):
    """A permutation of axes, mapping each input axis to an output axis by name"""
    typename: Literal['MapAxisTransformation'] = Field(alias='__typename', default='MapAxisTransformation', exclude=True)

class MeshCollectionDerivedfromBaseRotationTransformation(TransformationRotationTransformation, MeshCollectionDerivedfromBase, TransformationTrait, BaseModel):
    """A rotation, given as an orthonormal matrix"""
    typename: Literal['RotationTransformation'] = Field(alias='__typename', default='RotationTransformation', exclude=True)

class MeshCollectionDerivedfromBaseScaleTransformation(TransformationScaleTransformation, MeshCollectionDerivedfromBase, TransformationTrait, BaseModel):
    """A per-axis multiplication, with one entry per input axis"""
    typename: Literal['ScaleTransformation'] = Field(alias='__typename', default='ScaleTransformation', exclude=True)

class MeshCollectionDerivedfromBaseSequenceTransformation(TransformationSequenceTransformation, MeshCollectionDerivedfromBase, TransformationTrait, BaseModel):
    """An ordered composition of child transformations, applied first to last"""
    typename: Literal['SequenceTransformation'] = Field(alias='__typename', default='SequenceTransformation', exclude=True)

class MeshCollectionDerivedfromBaseTranslationTransformation(TransformationTranslationTransformation, MeshCollectionDerivedfromBase, TransformationTrait, BaseModel):
    """A per-axis offset, with one entry per input axis"""
    typename: Literal['TranslationTransformation'] = Field(alias='__typename', default='TranslationTransformation', exclude=True)

class MeshCollectionDerivedfromBaseUnmappableTransformation(TransformationUnmappableTransformation, MeshCollectionDerivedfromBase, TransformationTrait, BaseModel):
    """A declared NON-correspondence: the two systems are related -- one was computed from the other -- and no point of either maps to a point of the other. It has no parameters, no rank and no matrix, and no placement search will walk it, in either direction. This is what a per-object measurement table's relation to the image it was measured from looks like"""
    typename: Literal['UnmappableTransformation'] = Field(alias='__typename', default='UnmappableTransformation', exclude=True)

class MeshCollectionDerivedfromBaseCatchAll(MeshCollectionDerivedfromBase, BaseModel):
    """Catch all class for MeshCollectionDerivedfromBase"""
    typename: str = Field(alias='__typename', exclude=True)

class MeshCollection(MikroFetchable, BaseModel):
    """An immutable, versioned collection of meshes, backed by Parquet stores. Ask the catalog store for an access grant and query the Parquet directly (e.g. with DuckDB) rather than paginating meshes through GraphQL"""
    typename: Literal['MeshCollection'] = Field(alias='__typename', default='MeshCollection', exclude=True)
    id: ID
    version: str
    spec_version: str = Field(alias='specVersion')
    grid: Any
    'The octree grid. Its `cellSize` is in voxels of the coordinate system, so the octree aligns to the label grid the meshes were extracted from'
    encoding: Any
    'The geometry encoding: how positions, normals and indices are quantized and compressed'
    coordinate_system: CoordinateSystem = Field(alias='coordinateSystem')
    "The coordinate system the collection's vertices are expressed in. The collection owns it; `derivedFrom` relates it to the data the meshes were extracted from"
    catalog: ParquetStore
    'The Parquet store holding the catalog. Request an access grant from it and read the Parquet directly'
    geometry: Tuple[ParquetStore, ...]
    'The Parquet stores holding the geometry shards'
    derived_from: Tuple[Union[Annotated[Union[MeshCollectionDerivedfromBaseAffineTransformation, MeshCollectionDerivedfromBaseBijectionTransformation, MeshCollectionDerivedfromBaseByDimensionTransformation, MeshCollectionDerivedfromBaseFieldTransformation, MeshCollectionDerivedfromBaseIdentityTransformation, MeshCollectionDerivedfromBaseMapAxisTransformation, MeshCollectionDerivedfromBaseRotationTransformation, MeshCollectionDerivedfromBaseScaleTransformation, MeshCollectionDerivedfromBaseSequenceTransformation, MeshCollectionDerivedfromBaseTranslationTransformation, MeshCollectionDerivedfromBaseUnmappableTransformation], Field(discriminator='typename')], MeshCollectionDerivedfromBaseCatchAll], ...] = Field(alias='derivedFrom')
    "Every edge from this collection's space back into data the meshes were extracted from, in declared order -- the first is the primary parent, the one that places it. An identity when the meshes are in that grid as-is, a scale when they came off a downsampled one, UNMAPPABLE where the lineage is recorded but no geometry is claimed. Empty for a mesh derived from no data at all. The same relation a derived dataset's `derivedFrom` records"
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for MeshCollection"""
        document = 'fragment Axis on Axis {\n  id\n  order\n  name\n  type\n  unit\n  longName\n  __typename\n}\n\nfragment TransformationChild on Transformation {\n  __typename\n  id\n  kind\n  inputAxes\n  outputAxes\n  ... on ScaleTransformation {\n    scale\n  }\n  ... on TranslationTransformation {\n    translation\n  }\n  ... on AffineTransformation {\n    affine\n  }\n  ... on RotationTransformation {\n    affine\n  }\n}\n\nfragment CoordinateSystem on CoordinateSystem {\n  id\n  name\n  epoch\n  axes {\n    ...Axis\n    __typename\n  }\n  __typename\n}\n\nfragment ParquetStore on ParquetStore {\n  id\n  key\n  bucket\n  path\n  __typename\n}\n\nfragment Transformation on Transformation {\n  id\n  kind\n  name\n  version\n  input {\n    ...CoordinateSystem\n    __typename\n  }\n  output {\n    ...CoordinateSystem\n    __typename\n  }\n  ... on ScaleTransformation {\n    scale\n  }\n  ... on TranslationTransformation {\n    translation\n  }\n  ... on AffineTransformation {\n    affine\n  }\n  ... on RotationTransformation {\n    affine\n  }\n  ... on MapAxisTransformation {\n    inputAxes\n    outputAxes\n  }\n  ... on FieldTransformation {\n    field {\n      ...CoordinateSystem\n    }\n  }\n  ... on SequenceTransformation {\n    sequenceChildren: transformations {\n      ...TransformationChild\n    }\n  }\n  ... on ByDimensionTransformation {\n    inputAxes\n    outputAxes\n    byDimensionChildren: transformations {\n      ...TransformationChild\n    }\n  }\n  ... on BijectionTransformation {\n    bijectionChildren: transformations {\n      ...TransformationChild\n    }\n  }\n  __typename\n}\n\nfragment MeshCollection on MeshCollection {\n  id\n  version\n  specVersion\n  grid\n  encoding\n  coordinateSystem {\n    ...CoordinateSystem\n    __typename\n  }\n  catalog {\n    ...ParquetStore\n    __typename\n  }\n  geometry {\n    ...ParquetStore\n    __typename\n  }\n  derivedFrom {\n    ...Transformation\n    __typename\n  }\n  __typename\n}'
        name = 'MeshCollection'
        type = 'MeshCollection'

class TableDatasetColumns(BaseModel):
    """One declared column of a table dataset: its name, dtype and role. A COORDINATE column is also an axis of the table's space"""
    typename: Literal['TableDatasetColumn'] = Field(alias='__typename', default='TableDatasetColumn', exclude=True)
    id: ID
    order: int
    name: str
    dtype: str
    role: TableColumnRole
    axis_type: Optional[AxisType] = Field(default=None, alias='axisType')
    unit: Optional[str] = Field(default=None)
    long_name: Optional[str] = Field(default=None, alias='longName')
    model_config = ConfigDict(frozen=True)

class TableDatasetDerivedfromBase(BaseModel):
    """A directed edge of the coordinate graph, mapping `input` to `output`. Direction is always forward. The concrete kind (Scale, Translation, Affine, Sequence, ...) carries the parameters"""
    model_config = ConfigDict(frozen=True)

class TableDatasetDerivedfromBaseAffineTransformation(TransformationAffineTransformation, TableDatasetDerivedfromBase, TransformationTrait, BaseModel):
    """A general affine map, given as an M x (N+1) matrix with rows outermost"""
    typename: Literal['AffineTransformation'] = Field(alias='__typename', default='AffineTransformation', exclude=True)

class TableDatasetDerivedfromBaseBijectionTransformation(TransformationBijectionTransformation, TableDatasetDerivedfromBase, TransformationTrait, BaseModel):
    """A pair of child transformations giving an explicit forward and inverse map"""
    typename: Literal['BijectionTransformation'] = Field(alias='__typename', default='BijectionTransformation', exclude=True)

class TableDatasetDerivedfromBaseByDimensionTransformation(TransformationByDimensionTransformation, TableDatasetDerivedfromBase, TransformationTrait, BaseModel):
    """A composition of child transformations, each acting on a named subset of the axes"""
    typename: Literal['ByDimensionTransformation'] = Field(alias='__typename', default='ByDimensionTransformation', exclude=True)

class TableDatasetDerivedfromBaseFieldTransformation(TransformationFieldTransformation, TableDatasetDerivedfromBase, TransformationTrait, BaseModel):
    """A non-affine map given by the values of an array rather than by a formula. The array is a `field`: a node of this graph, not a payload on this edge, so it keeps its own lineage and its axes say what its numbers mean. It has no closed-form inverse, so a placement path never walks it backwards"""
    typename: Literal['FieldTransformation'] = Field(alias='__typename', default='FieldTransformation', exclude=True)

class TableDatasetDerivedfromBaseIdentityTransformation(TransformationIdentityTransformation, TableDatasetDerivedfromBase, TransformationTrait, BaseModel):
    """The identity map: input and output coordinates are the same"""
    typename: Literal['IdentityTransformation'] = Field(alias='__typename', default='IdentityTransformation', exclude=True)

class TableDatasetDerivedfromBaseMapAxisTransformation(TransformationMapAxisTransformation, TableDatasetDerivedfromBase, TransformationTrait, BaseModel):
    """A permutation of axes, mapping each input axis to an output axis by name"""
    typename: Literal['MapAxisTransformation'] = Field(alias='__typename', default='MapAxisTransformation', exclude=True)

class TableDatasetDerivedfromBaseRotationTransformation(TransformationRotationTransformation, TableDatasetDerivedfromBase, TransformationTrait, BaseModel):
    """A rotation, given as an orthonormal matrix"""
    typename: Literal['RotationTransformation'] = Field(alias='__typename', default='RotationTransformation', exclude=True)

class TableDatasetDerivedfromBaseScaleTransformation(TransformationScaleTransformation, TableDatasetDerivedfromBase, TransformationTrait, BaseModel):
    """A per-axis multiplication, with one entry per input axis"""
    typename: Literal['ScaleTransformation'] = Field(alias='__typename', default='ScaleTransformation', exclude=True)

class TableDatasetDerivedfromBaseSequenceTransformation(TransformationSequenceTransformation, TableDatasetDerivedfromBase, TransformationTrait, BaseModel):
    """An ordered composition of child transformations, applied first to last"""
    typename: Literal['SequenceTransformation'] = Field(alias='__typename', default='SequenceTransformation', exclude=True)

class TableDatasetDerivedfromBaseTranslationTransformation(TransformationTranslationTransformation, TableDatasetDerivedfromBase, TransformationTrait, BaseModel):
    """A per-axis offset, with one entry per input axis"""
    typename: Literal['TranslationTransformation'] = Field(alias='__typename', default='TranslationTransformation', exclude=True)

class TableDatasetDerivedfromBaseUnmappableTransformation(TransformationUnmappableTransformation, TableDatasetDerivedfromBase, TransformationTrait, BaseModel):
    """A declared NON-correspondence: the two systems are related -- one was computed from the other -- and no point of either maps to a point of the other. It has no parameters, no rank and no matrix, and no placement search will walk it, in either direction. This is what a per-object measurement table's relation to the image it was measured from looks like"""
    typename: Literal['UnmappableTransformation'] = Field(alias='__typename', default='UnmappableTransformation', exclude=True)

class TableDatasetDerivedfromBaseCatchAll(TableDatasetDerivedfromBase, BaseModel):
    """Catch all class for TableDatasetDerivedfromBase"""
    typename: str = Field(alias='__typename', exclude=True)

class TableDataset(MikroFetchable, BaseModel):
    """A parquet-backed table whose rows are scientific records (segmented objects, localizations, cells). It owns a coordinate system whose axes are its coordinate columns, which is what makes a localization table placeable; a table with no coordinate columns enumerates its rows and its lineage edge is UNMAPPABLE. Its store, its columns and that coordinate system are fixed at creation -- only `name` and `description` can be updated, and a recomputation is a new table rather than an edit of this one. Read the rows directly from the Parquet store with a datalayer access grant rather than paginating through GraphQL"""
    typename: Literal['TableDataset'] = Field(alias='__typename', default='TableDataset', exclude=True)
    id: ID
    name: str
    description: Optional[str] = Field(default=None)
    store: ParquetStore
    'The Parquet store holding the rows. Request an access grant from it and read the Parquet directly'
    columns: Tuple[TableDatasetColumns, ...]
    "The declared column schema, in order. The COORDINATE columns are the axes of this table's coordinate system"
    coordinate_system: CoordinateSystem = Field(alias='coordinateSystem')
    "The coordinate system this table owns. Its axes are the table's coordinate columns (or a single INDEX axis for a pure measurement table)"
    derived_from: Tuple[Union[Annotated[Union[TableDatasetDerivedfromBaseAffineTransformation, TableDatasetDerivedfromBaseBijectionTransformation, TableDatasetDerivedfromBaseByDimensionTransformation, TableDatasetDerivedfromBaseFieldTransformation, TableDatasetDerivedfromBaseIdentityTransformation, TableDatasetDerivedfromBaseMapAxisTransformation, TableDatasetDerivedfromBaseRotationTransformation, TableDatasetDerivedfromBaseScaleTransformation, TableDatasetDerivedfromBaseSequenceTransformation, TableDatasetDerivedfromBaseTranslationTransformation, TableDatasetDerivedfromBaseUnmappableTransformation], Field(discriminator='typename')], TableDatasetDerivedfromBaseCatchAll], ...] = Field(alias='derivedFrom')
    "Every edge from this table's space back into data it was computed from, in declared order -- the first is the primary parent, the one that places it. UNMAPPABLE where the lineage is recorded but no geometry is claimed; empty for a freestanding table. The same relation a derived dataset's `derivedFrom` records"
    axis_names: Tuple[str, ...] = Field(alias='axisNames')
    "The table's axis names, in order. Derived from the coordinate columns"
    provenance_metadata: Any = Field(alias='provenanceMetadata')
    'How this table was produced: the run, its parameters and its inputs'
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for TableDataset"""
        document = 'fragment Axis on Axis {\n  id\n  order\n  name\n  type\n  unit\n  longName\n  __typename\n}\n\nfragment TransformationChild on Transformation {\n  __typename\n  id\n  kind\n  inputAxes\n  outputAxes\n  ... on ScaleTransformation {\n    scale\n  }\n  ... on TranslationTransformation {\n    translation\n  }\n  ... on AffineTransformation {\n    affine\n  }\n  ... on RotationTransformation {\n    affine\n  }\n}\n\nfragment CoordinateSystem on CoordinateSystem {\n  id\n  name\n  epoch\n  axes {\n    ...Axis\n    __typename\n  }\n  __typename\n}\n\nfragment ParquetStore on ParquetStore {\n  id\n  key\n  bucket\n  path\n  __typename\n}\n\nfragment Transformation on Transformation {\n  id\n  kind\n  name\n  version\n  input {\n    ...CoordinateSystem\n    __typename\n  }\n  output {\n    ...CoordinateSystem\n    __typename\n  }\n  ... on ScaleTransformation {\n    scale\n  }\n  ... on TranslationTransformation {\n    translation\n  }\n  ... on AffineTransformation {\n    affine\n  }\n  ... on RotationTransformation {\n    affine\n  }\n  ... on MapAxisTransformation {\n    inputAxes\n    outputAxes\n  }\n  ... on FieldTransformation {\n    field {\n      ...CoordinateSystem\n    }\n  }\n  ... on SequenceTransformation {\n    sequenceChildren: transformations {\n      ...TransformationChild\n    }\n  }\n  ... on ByDimensionTransformation {\n    inputAxes\n    outputAxes\n    byDimensionChildren: transformations {\n      ...TransformationChild\n    }\n  }\n  ... on BijectionTransformation {\n    bijectionChildren: transformations {\n      ...TransformationChild\n    }\n  }\n  __typename\n}\n\nfragment TableDataset on TableDataset {\n  id\n  name\n  description\n  store {\n    ...ParquetStore\n    __typename\n  }\n  columns {\n    id\n    order\n    name\n    dtype\n    role\n    axisType\n    unit\n    longName\n    __typename\n  }\n  coordinateSystem {\n    ...CoordinateSystem\n    __typename\n  }\n  derivedFrom {\n    ...Transformation\n    __typename\n  }\n  axisNames\n  provenanceMetadata\n  __typename\n}'
        name = 'TableDataset'
        type = 'TableDataset'

class CreateADatasetMutation(BaseModel):
    """No documentation found for this operation."""
    create_a_dataset: ADataset = Field(alias='createADataset')
    'Create a new dataset from array-like data with optional coordinate anchors and OME metadata'

    class Arguments(BaseModel):
        """Arguments for CreateADataset """
        input: CreateADatasetInput
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for CreateADataset """
        document = 'fragment Axis on Axis {\n  id\n  order\n  name\n  type\n  unit\n  longName\n  __typename\n}\n\nfragment CoordinateSystem on CoordinateSystem {\n  id\n  name\n  epoch\n  axes {\n    ...Axis\n    __typename\n  }\n  __typename\n}\n\nfragment ZarrStore on ZarrStore {\n  id\n  key\n  bucket\n  path\n  __typename\n}\n\nfragment ADataset on ADataset {\n  id\n  name\n  axisNames\n  shape\n  multiscale\n  intrinsicSystem {\n    ...CoordinateSystem\n    __typename\n  }\n  dataArrays {\n    id\n    level\n    shape\n    chunkShape\n    store {\n      ...ZarrStore\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nmutation CreateADataset($input: CreateADatasetInput!) {\n  createADataset(input: $input) {\n    ...ADataset\n    __typename\n  }\n}'

class CreateAnimationMutation(BaseModel):
    """No documentation found for this operation."""
    create_animation: Animation = Field(alias='createAnimation')
    'Author a named camera tour of a scene'

    class Arguments(BaseModel):
        """Arguments for CreateAnimation """
        input: CreateAnimationInput
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for CreateAnimation """
        document = 'fragment Axis on Axis {\n  id\n  order\n  name\n  type\n  unit\n  longName\n  __typename\n}\n\nfragment CameraState on CameraState {\n  position\n  crossSectionOrientation\n  crossSectionScale\n  projectionOrientation\n  projectionScale\n  __typename\n}\n\nfragment CoordinateSystem on CoordinateSystem {\n  id\n  name\n  epoch\n  axes {\n    ...Axis\n    __typename\n  }\n  __typename\n}\n\nfragment AnimationWaypoint on AnimationWaypoint {\n  id\n  order\n  name\n  durationMs\n  easing\n  camera {\n    ...CameraState\n    __typename\n  }\n  __typename\n}\n\nfragment Scene on Scene {\n  name\n  id\n  preferredView\n  backgroundColor\n  worldCoordinateSystem {\n    ...CoordinateSystem\n    __typename\n  }\n  __typename\n}\n\nfragment Animation on Animation {\n  id\n  name\n  description\n  scene {\n    ...Scene\n    __typename\n  }\n  waypoints {\n    ...AnimationWaypoint\n    __typename\n  }\n  __typename\n}\n\nmutation CreateAnimation($input: CreateAnimationInput!) {\n  createAnimation(input: $input) {\n    ...Animation\n    __typename\n  }\n}'

class UpdateAnimationMutation(BaseModel):
    """No documentation found for this operation."""
    update_animation: Animation = Field(alias='updateAnimation')
    'Re-author a camera tour: rename it, or replace its stops'

    class Arguments(BaseModel):
        """Arguments for UpdateAnimation """
        input: UpdateAnimationInput
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for UpdateAnimation """
        document = 'fragment Axis on Axis {\n  id\n  order\n  name\n  type\n  unit\n  longName\n  __typename\n}\n\nfragment CameraState on CameraState {\n  position\n  crossSectionOrientation\n  crossSectionScale\n  projectionOrientation\n  projectionScale\n  __typename\n}\n\nfragment CoordinateSystem on CoordinateSystem {\n  id\n  name\n  epoch\n  axes {\n    ...Axis\n    __typename\n  }\n  __typename\n}\n\nfragment AnimationWaypoint on AnimationWaypoint {\n  id\n  order\n  name\n  durationMs\n  easing\n  camera {\n    ...CameraState\n    __typename\n  }\n  __typename\n}\n\nfragment Scene on Scene {\n  name\n  id\n  preferredView\n  backgroundColor\n  worldCoordinateSystem {\n    ...CoordinateSystem\n    __typename\n  }\n  __typename\n}\n\nfragment Animation on Animation {\n  id\n  name\n  description\n  scene {\n    ...Scene\n    __typename\n  }\n  waypoints {\n    ...AnimationWaypoint\n    __typename\n  }\n  __typename\n}\n\nmutation UpdateAnimation($input: UpdateAnimationInput!) {\n  updateAnimation(input: $input) {\n    ...Animation\n    __typename\n  }\n}'

class DeleteAnimationMutation(BaseModel):
    """No documentation found for this operation."""
    delete_animation: ID = Field(alias='deleteAnimation')
    'Delete an existing camera tour'

    class Arguments(BaseModel):
        """Arguments for DeleteAnimation """
        input: DeleteAnimationInput
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for DeleteAnimation """
        document = 'mutation DeleteAnimation($input: DeleteAnimationInput!) {\n  deleteAnimation(input: $input)\n}'

class CreateAnnotationMutation(BaseModel):
    """No documentation found for this operation."""
    create_annotation: Annotation = Field(alias='createAnnotation')
    "Draw an annotation into a collection, or onto a scene (exactly one of the two). Drawing on a scene finds its annotation collection or mints it on first use: a coordinate system copying the world's axes, an identity registration into the world, and one annotation layer"

    class Arguments(BaseModel):
        """Arguments for CreateAnnotation """
        input: CreateAnnotationInput
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for CreateAnnotation """
        document = 'fragment Axis on Axis {\n  id\n  order\n  name\n  type\n  unit\n  longName\n  __typename\n}\n\nfragment CoordinateSystem on CoordinateSystem {\n  id\n  name\n  epoch\n  axes {\n    ...Axis\n    __typename\n  }\n  __typename\n}\n\nfragment Annotation on Annotation {\n  id\n  name\n  kind\n  vectors\n  coordinates {\n    name\n    value\n    __typename\n  }\n  coordinateSystem {\n    ...CoordinateSystem\n    __typename\n  }\n  intrinsicBbox {\n    min\n    max\n    __typename\n  }\n  strokeColor\n  fillColor\n  strokeWidth\n  filled\n  __typename\n}\n\nmutation CreateAnnotation($input: CreateAnnotationInput!) {\n  createAnnotation(input: $input) {\n    ...Annotation\n    __typename\n  }\n}'

class CreateAnnotationsMutation(BaseModel):
    """No documentation found for this operation."""
    create_annotations: Tuple[Annotation, ...] = Field(alias='createAnnotations')
    'Draw many annotations in one call, into a collection or onto a scene (exactly one of the two, same semantics as createAnnotation). The transform chain and version resolve once for the whole batch, and the rows insert in bulk'

    class Arguments(BaseModel):
        """Arguments for CreateAnnotations """
        input: CreateAnnotationsInput
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for CreateAnnotations """
        document = 'fragment Axis on Axis {\n  id\n  order\n  name\n  type\n  unit\n  longName\n  __typename\n}\n\nfragment CoordinateSystem on CoordinateSystem {\n  id\n  name\n  epoch\n  axes {\n    ...Axis\n    __typename\n  }\n  __typename\n}\n\nfragment Annotation on Annotation {\n  id\n  name\n  kind\n  vectors\n  coordinates {\n    name\n    value\n    __typename\n  }\n  coordinateSystem {\n    ...CoordinateSystem\n    __typename\n  }\n  intrinsicBbox {\n    min\n    max\n    __typename\n  }\n  strokeColor\n  fillColor\n  strokeWidth\n  filled\n  __typename\n}\n\nmutation CreateAnnotations($input: CreateAnnotationsInput!) {\n  createAnnotations(input: $input) {\n    ...Annotation\n    __typename\n  }\n}'

class UpdateAnnotationMutation(BaseModel):
    """No documentation found for this operation."""
    update_annotation: Annotation = Field(alias='updateAnnotation')
    'Edit an annotation: name, kind, vectors, pins or styling. New vectors re-derive the bounding box against the current transform chain'

    class Arguments(BaseModel):
        """Arguments for UpdateAnnotation """
        input: UpdateAnnotationInput
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for UpdateAnnotation """
        document = 'fragment Axis on Axis {\n  id\n  order\n  name\n  type\n  unit\n  longName\n  __typename\n}\n\nfragment CoordinateSystem on CoordinateSystem {\n  id\n  name\n  epoch\n  axes {\n    ...Axis\n    __typename\n  }\n  __typename\n}\n\nfragment Annotation on Annotation {\n  id\n  name\n  kind\n  vectors\n  coordinates {\n    name\n    value\n    __typename\n  }\n  coordinateSystem {\n    ...CoordinateSystem\n    __typename\n  }\n  intrinsicBbox {\n    min\n    max\n    __typename\n  }\n  strokeColor\n  fillColor\n  strokeWidth\n  filled\n  __typename\n}\n\nmutation UpdateAnnotation($input: UpdateAnnotationInput!) {\n  updateAnnotation(input: $input) {\n    ...Annotation\n    __typename\n  }\n}'

class DeleteAnnotationMutation(BaseModel):
    """No documentation found for this operation."""
    delete_annotation: ID = Field(alias='deleteAnnotation')
    'Delete an existing annotation'

    class Arguments(BaseModel):
        """Arguments for DeleteAnnotation """
        input: DeleteAnnotationInput
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for DeleteAnnotation """
        document = 'mutation DeleteAnnotation($input: DeleteAnnotationInput!) {\n  deleteAnnotation(input: $input)\n}'

class CreateAnnotationCollectionMutation(BaseModel):
    """No documentation found for this operation."""
    create_annotation_collection: AnnotationCollection = Field(alias='createAnnotationCollection')
    "Create an annotation collection explicitly, in a coordinate system of its own, optionally derived from the system the shapes are drawn over. The common path -- drawing on a scene -- goes through createAnnotation instead, which mints the scene's collection on first use"

    class Arguments(BaseModel):
        """Arguments for CreateAnnotationCollection """
        input: CreateAnnotationCollectionInput
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for CreateAnnotationCollection """
        document = 'fragment Axis on Axis {\n  id\n  order\n  name\n  type\n  unit\n  longName\n  __typename\n}\n\nfragment Annotation on Annotation {\n  id\n  name\n  kind\n  vectors\n  coordinates {\n    name\n    value\n    __typename\n  }\n  coordinateSystem {\n    ...CoordinateSystem\n    __typename\n  }\n  intrinsicBbox {\n    min\n    max\n    __typename\n  }\n  strokeColor\n  fillColor\n  strokeWidth\n  filled\n  __typename\n}\n\nfragment CoordinateSystem on CoordinateSystem {\n  id\n  name\n  epoch\n  axes {\n    ...Axis\n    __typename\n  }\n  __typename\n}\n\nfragment AnnotationCollection on AnnotationCollection {\n  id\n  name\n  description\n  coordinateSystem {\n    ...CoordinateSystem\n    __typename\n  }\n  annotations {\n    ...Annotation\n    __typename\n  }\n  __typename\n}\n\nmutation CreateAnnotationCollection($input: CreateAnnotationCollectionInput!) {\n  createAnnotationCollection(input: $input) {\n    ...AnnotationCollection\n    __typename\n  }\n}'

class DeleteAnnotationCollectionMutation(BaseModel):
    """No documentation found for this operation."""
    delete_annotation_collection: ID = Field(alias='deleteAnnotationCollection')
    'Delete an annotation collection. Its coordinate system, its annotations and its layers cascade with it'

    class Arguments(BaseModel):
        """Arguments for DeleteAnnotationCollection """
        input: DeleteAnnotationCollectionInput
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for DeleteAnnotationCollection """
        document = 'mutation DeleteAnnotationCollection($input: DeleteAnnotationCollectionInput!) {\n  deleteAnnotationCollection(input: $input)\n}'

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

class CreateCoordinateSystemMutation(BaseModel):
    """No documentation found for this operation."""
    create_coordinate_system: CoordinateSystem = Field(alias='createCoordinateSystem')
    'Create a SHARED coordinate system (an ownerless space) and, in one call, author the edges registering any number of sources (datasets, table datasets, mesh collections, coordinate systems) into it'

    class Arguments(BaseModel):
        """Arguments for CreateCoordinateSystem """
        input: CreateCoordinateSystemInput
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for CreateCoordinateSystem """
        document = 'fragment Axis on Axis {\n  id\n  order\n  name\n  type\n  unit\n  longName\n  __typename\n}\n\nfragment CoordinateSystem on CoordinateSystem {\n  id\n  name\n  epoch\n  axes {\n    ...Axis\n    __typename\n  }\n  __typename\n}\n\nmutation CreateCoordinateSystem($input: CreateCoordinateSystemInput!) {\n  createCoordinateSystem(input: $input) {\n    ...CoordinateSystem\n    __typename\n  }\n}'

class UpdateCoordinateSystemMutation(BaseModel):
    """No documentation found for this operation."""
    update_coordinate_system: CoordinateSystem = Field(alias='updateCoordinateSystem')
    "Rename a shared coordinate system or anchor its clock. Shared spaces only -- an owned system's name is its container's business, and where data sits is an edge (updateTransformation), not a property of the space"

    class Arguments(BaseModel):
        """Arguments for UpdateCoordinateSystem """
        input: UpdateCoordinateSystemInput
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for UpdateCoordinateSystem """
        document = 'fragment Axis on Axis {\n  id\n  order\n  name\n  type\n  unit\n  longName\n  __typename\n}\n\nfragment CoordinateSystem on CoordinateSystem {\n  id\n  name\n  epoch\n  axes {\n    ...Axis\n    __typename\n  }\n  __typename\n}\n\nmutation UpdateCoordinateSystem($input: UpdateCoordinateSystemInput!) {\n  updateCoordinateSystem(input: $input) {\n    ...CoordinateSystem\n    __typename\n  }\n}'

class DeleteCoordinateSystemMutation(BaseModel):
    """No documentation found for this operation."""
    delete_coordinate_system: ID = Field(alias='deleteCoordinateSystem')
    'Delete an unused shared coordinate system. Refused while any scene is rooted in it or any transformation edge touches it. This is the only door a shared space leaves through -- deleting a scene never deletes one. Other system kinds cascade with their owner and cannot be deleted directly'

    class Arguments(BaseModel):
        """Arguments for DeleteCoordinateSystem """
        input: DeleteCoordinateSystemInput
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for DeleteCoordinateSystem """
        document = 'mutation DeleteCoordinateSystem($input: DeleteCoordinateSystemInput!) {\n  deleteCoordinateSystem(input: $input)\n}'

class ClearCoordinateSystemMutation(BaseModel):
    """No documentation found for this operation."""
    clear_coordinate_system: Tuple[ID, ...] = Field(alias='clearCoordinateSystem')
    "Delete every registration INTO a shared space in one call, returning the deleted edge ids. The space, the scenes over it (their layers drop to UNREGISTERED) and the space's own claims into wider spaces all survive. Guarded by the space's creator: clearing a space is the space-owner's act"

    class Arguments(BaseModel):
        """Arguments for ClearCoordinateSystem """
        input: ClearCoordinateSystemInput
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for ClearCoordinateSystem """
        document = 'mutation ClearCoordinateSystem($input: ClearCoordinateSystemInput!) {\n  clearCoordinateSystem(input: $input)\n}'

class DeleteRegistrationMutation(BaseModel):
    """No documentation found for this operation."""
    delete_registration: Tuple[ID, ...] = Field(alias='deleteRegistration')
    "Un-register a source from a space by naming the source and the space rather than the edge. Deletes every edge from the source's space into that one -- rivals are allowed, so there is no single edge to mean -- and returns their ids. An UNMAPPABLE declaration is not a placement and is never matched"

    class Arguments(BaseModel):
        """Arguments for DeleteRegistration """
        input: DeleteRegistrationInput
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for DeleteRegistration """
        document = 'mutation DeleteRegistration($input: DeleteRegistrationInput!) {\n  deleteRegistration(input: $input)\n}'

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
        document = 'fragment Era on Era {\n  id\n  begin\n  name\n  __typename\n}\n\nfragment ReferenceView on ReferenceView {\n  ...View\n  id\n  __typename\n}\n\nfragment View on View {\n  xMin\n  xMax\n  yMin\n  yMax\n  tMin\n  tMax\n  cMin\n  cMax\n  zMin\n  zMax\n  __typename\n}\n\nfragment AcquisitionView on AcquisitionView {\n  ...View\n  id\n  description\n  acquiredAt\n  operator {\n    sub\n    __typename\n  }\n  __typename\n}\n\nfragment AffineTransformationView on AffineTransformationView {\n  ...View\n  id\n  affineMatrix\n  stage {\n    id\n    name\n    __typename\n  }\n  __typename\n}\n\nfragment ChannelView on ChannelView {\n  ...View\n  id\n  emissionWavelength\n  excitationWavelength\n  __typename\n}\n\nfragment ContinousScanView on ContinousScanView {\n  ...View\n  id\n  direction\n  __typename\n}\n\nfragment DerivedView on DerivedView {\n  ...View\n  id\n  originImage {\n    id\n    name\n    __typename\n  }\n  __typename\n}\n\nfragment FileView on FileView {\n  ...View\n  id\n  seriesIdentifier\n  file {\n    id\n    name\n    __typename\n  }\n  __typename\n}\n\nfragment InstanceMaskView on InstanceMaskView {\n  ...View\n  id\n  referenceView {\n    ...ReferenceView\n    __typename\n  }\n  __typename\n}\n\nfragment MaskView on MaskView {\n  ...View\n  id\n  referenceView {\n    ...ReferenceView\n    __typename\n  }\n  __typename\n}\n\nfragment OpticsView on OpticsView {\n  ...View\n  id\n  objective {\n    id\n    name\n    serialNumber\n    __typename\n  }\n  camera {\n    id\n    name\n    serialNumber\n    __typename\n  }\n  instrument {\n    id\n    name\n    serialNumber\n    __typename\n  }\n  __typename\n}\n\nfragment RGBView on RGBView {\n  ...View\n  id\n  contexts {\n    id\n    name\n    __typename\n  }\n  name\n  image {\n    id\n    store {\n      ...ZarrStore\n      __typename\n    }\n    derivedScaleViews {\n      id\n      image {\n        id\n        store {\n          ...ZarrStore\n          __typename\n        }\n        __typename\n      }\n      scaleX\n      scaleY\n      scaleZ\n      scaleT\n      scaleC\n      __typename\n    }\n    __typename\n  }\n  colorMap\n  contrastLimitMin\n  contrastLimitMax\n  gamma\n  active\n  fullColour\n  baseColor\n  __typename\n}\n\nfragment ROIView on ROIView {\n  ...View\n  id\n  roi {\n    id\n    name\n    __typename\n  }\n  __typename\n}\n\nfragment TimepointView on TimepointView {\n  ...View\n  id\n  timeSinceStart\n  indexSinceStart\n  era {\n    ...Era\n    __typename\n  }\n  __typename\n}\n\nfragment WellPositionView on WellPositionView {\n  ...View\n  id\n  column\n  row\n  well {\n    id\n    rows\n    columns\n    name\n    __typename\n  }\n  __typename\n}\n\nfragment ZarrStore on ZarrStore {\n  id\n  key\n  bucket\n  path\n  __typename\n}\n\nfragment Image on Image {\n  id\n  name\n  store {\n    ...ZarrStore\n    __typename\n  }\n  views {\n    ...ChannelView\n    ...AffineTransformationView\n    ...TimepointView\n    ...OpticsView\n    ...AcquisitionView\n    ...RGBView\n    ...WellPositionView\n    ...DerivedView\n    ...ROIView\n    ...FileView\n    ...ContinousScanView\n    __typename\n  }\n  maskViews {\n    ...MaskView\n    __typename\n  }\n  instanceMaskViews {\n    ...InstanceMaskView\n    __typename\n  }\n  rgbContexts {\n    id\n    name\n    views {\n      ...RGBView\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nmutation from_array_like($input: FromArrayLikeInput!) {\n  fromArrayLike(input: $input) {\n    ...Image\n    __typename\n  }\n}'

class UpdateImageMutation(BaseModel):
    """No documentation found for this operation."""
    update_image: Image = Field(alias='updateImage')
    "Update an existing image's metadata"

    class Arguments(BaseModel):
        """Arguments for UpdateImage """
        input: UpdateImageInput
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for UpdateImage """
        document = 'fragment Era on Era {\n  id\n  begin\n  name\n  __typename\n}\n\nfragment ReferenceView on ReferenceView {\n  ...View\n  id\n  __typename\n}\n\nfragment View on View {\n  xMin\n  xMax\n  yMin\n  yMax\n  tMin\n  tMax\n  cMin\n  cMax\n  zMin\n  zMax\n  __typename\n}\n\nfragment AcquisitionView on AcquisitionView {\n  ...View\n  id\n  description\n  acquiredAt\n  operator {\n    sub\n    __typename\n  }\n  __typename\n}\n\nfragment AffineTransformationView on AffineTransformationView {\n  ...View\n  id\n  affineMatrix\n  stage {\n    id\n    name\n    __typename\n  }\n  __typename\n}\n\nfragment ChannelView on ChannelView {\n  ...View\n  id\n  emissionWavelength\n  excitationWavelength\n  __typename\n}\n\nfragment ContinousScanView on ContinousScanView {\n  ...View\n  id\n  direction\n  __typename\n}\n\nfragment DerivedView on DerivedView {\n  ...View\n  id\n  originImage {\n    id\n    name\n    __typename\n  }\n  __typename\n}\n\nfragment FileView on FileView {\n  ...View\n  id\n  seriesIdentifier\n  file {\n    id\n    name\n    __typename\n  }\n  __typename\n}\n\nfragment InstanceMaskView on InstanceMaskView {\n  ...View\n  id\n  referenceView {\n    ...ReferenceView\n    __typename\n  }\n  __typename\n}\n\nfragment MaskView on MaskView {\n  ...View\n  id\n  referenceView {\n    ...ReferenceView\n    __typename\n  }\n  __typename\n}\n\nfragment OpticsView on OpticsView {\n  ...View\n  id\n  objective {\n    id\n    name\n    serialNumber\n    __typename\n  }\n  camera {\n    id\n    name\n    serialNumber\n    __typename\n  }\n  instrument {\n    id\n    name\n    serialNumber\n    __typename\n  }\n  __typename\n}\n\nfragment RGBView on RGBView {\n  ...View\n  id\n  contexts {\n    id\n    name\n    __typename\n  }\n  name\n  image {\n    id\n    store {\n      ...ZarrStore\n      __typename\n    }\n    derivedScaleViews {\n      id\n      image {\n        id\n        store {\n          ...ZarrStore\n          __typename\n        }\n        __typename\n      }\n      scaleX\n      scaleY\n      scaleZ\n      scaleT\n      scaleC\n      __typename\n    }\n    __typename\n  }\n  colorMap\n  contrastLimitMin\n  contrastLimitMax\n  gamma\n  active\n  fullColour\n  baseColor\n  __typename\n}\n\nfragment ROIView on ROIView {\n  ...View\n  id\n  roi {\n    id\n    name\n    __typename\n  }\n  __typename\n}\n\nfragment TimepointView on TimepointView {\n  ...View\n  id\n  timeSinceStart\n  indexSinceStart\n  era {\n    ...Era\n    __typename\n  }\n  __typename\n}\n\nfragment WellPositionView on WellPositionView {\n  ...View\n  id\n  column\n  row\n  well {\n    id\n    rows\n    columns\n    name\n    __typename\n  }\n  __typename\n}\n\nfragment ZarrStore on ZarrStore {\n  id\n  key\n  bucket\n  path\n  __typename\n}\n\nfragment Image on Image {\n  id\n  name\n  store {\n    ...ZarrStore\n    __typename\n  }\n  views {\n    ...ChannelView\n    ...AffineTransformationView\n    ...TimepointView\n    ...OpticsView\n    ...AcquisitionView\n    ...RGBView\n    ...WellPositionView\n    ...DerivedView\n    ...ROIView\n    ...FileView\n    ...ContinousScanView\n    __typename\n  }\n  maskViews {\n    ...MaskView\n    __typename\n  }\n  instanceMaskViews {\n    ...InstanceMaskView\n    __typename\n  }\n  rgbContexts {\n    id\n    name\n    views {\n      ...RGBView\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nmutation UpdateImage($input: UpdateImageInput!) {\n  updateImage(input: $input) {\n    ...Image\n    __typename\n  }\n}'

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
    create_layer: LayerImageLayer = Field(alias='createLayer')
    'Create a new layer from an existing lens with optional affine transformation and colormap settings'

    class Arguments(BaseModel):
        """Arguments for CreateLayer """
        input: CreateLayerInput
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for CreateLayer """
        document = 'fragment Layer on Layer {\n  id\n  scene {\n    id\n    name\n    __typename\n  }\n  ... on ImageLayer {\n    lens {\n      id\n    }\n  }\n  __typename\n}\n\nmutation CreateLayer($input: CreateLayerInput!) {\n  createLayer(input: $input) {\n    ...Layer\n    __typename\n  }\n}'

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
        document = 'fragment Axis on Axis {\n  id\n  order\n  name\n  type\n  unit\n  longName\n  __typename\n}\n\nfragment CoordinateSystem on CoordinateSystem {\n  id\n  name\n  epoch\n  axes {\n    ...Axis\n    __typename\n  }\n  __typename\n}\n\nfragment Slice on Slice {\n  axis\n  start\n  stop\n  step\n  __typename\n}\n\nfragment ZarrStore on ZarrStore {\n  id\n  key\n  bucket\n  path\n  __typename\n}\n\nfragment Lens on Lens {\n  id\n  dataset {\n    id\n    axisNames\n    dataArrays {\n      id\n      level\n      store {\n        ...ZarrStore\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  shape\n  axisNames\n  coordinateSystem {\n    ...CoordinateSystem\n    __typename\n  }\n  renderAxes {\n    x\n    y\n    z\n    t\n    intensity\n    __typename\n  }\n  slices {\n    ...Slice\n    __typename\n  }\n  __typename\n}\n\nmutation CreateLens($input: CreateLensInput!) {\n  createLens(input: $input) {\n    ...Lens\n    __typename\n  }\n}'

class CreateMeshCollectionMutation(BaseModel):
    """No documentation found for this operation."""
    create_mesh_collection: MeshCollection = Field(alias='createMeshCollection')
    'Register an immutable, versioned mesh collection against a coordinate system'

    class Arguments(BaseModel):
        """Arguments for CreateMeshCollection """
        input: CreateMeshCollectionInput
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for CreateMeshCollection """
        document = 'fragment Axis on Axis {\n  id\n  order\n  name\n  type\n  unit\n  longName\n  __typename\n}\n\nfragment TransformationChild on Transformation {\n  __typename\n  id\n  kind\n  inputAxes\n  outputAxes\n  ... on ScaleTransformation {\n    scale\n  }\n  ... on TranslationTransformation {\n    translation\n  }\n  ... on AffineTransformation {\n    affine\n  }\n  ... on RotationTransformation {\n    affine\n  }\n}\n\nfragment CoordinateSystem on CoordinateSystem {\n  id\n  name\n  epoch\n  axes {\n    ...Axis\n    __typename\n  }\n  __typename\n}\n\nfragment ParquetStore on ParquetStore {\n  id\n  key\n  bucket\n  path\n  __typename\n}\n\nfragment Transformation on Transformation {\n  id\n  kind\n  name\n  version\n  input {\n    ...CoordinateSystem\n    __typename\n  }\n  output {\n    ...CoordinateSystem\n    __typename\n  }\n  ... on ScaleTransformation {\n    scale\n  }\n  ... on TranslationTransformation {\n    translation\n  }\n  ... on AffineTransformation {\n    affine\n  }\n  ... on RotationTransformation {\n    affine\n  }\n  ... on MapAxisTransformation {\n    inputAxes\n    outputAxes\n  }\n  ... on FieldTransformation {\n    field {\n      ...CoordinateSystem\n    }\n  }\n  ... on SequenceTransformation {\n    sequenceChildren: transformations {\n      ...TransformationChild\n    }\n  }\n  ... on ByDimensionTransformation {\n    inputAxes\n    outputAxes\n    byDimensionChildren: transformations {\n      ...TransformationChild\n    }\n  }\n  ... on BijectionTransformation {\n    bijectionChildren: transformations {\n      ...TransformationChild\n    }\n  }\n  __typename\n}\n\nfragment MeshCollection on MeshCollection {\n  id\n  version\n  specVersion\n  grid\n  encoding\n  coordinateSystem {\n    ...CoordinateSystem\n    __typename\n  }\n  catalog {\n    ...ParquetStore\n    __typename\n  }\n  geometry {\n    ...ParquetStore\n    __typename\n  }\n  derivedFrom {\n    ...Transformation\n    __typename\n  }\n  __typename\n}\n\nmutation CreateMeshCollection($input: CreateMeshCollectionInput!) {\n  createMeshCollection(input: $input) {\n    ...MeshCollection\n    __typename\n  }\n}'

class DeleteMeshCollectionMutation(BaseModel):
    """No documentation found for this operation."""
    delete_mesh_collection: ID = Field(alias='deleteMeshCollection')
    'Delete an existing mesh collection'

    class Arguments(BaseModel):
        """Arguments for DeleteMeshCollection """
        input: DeleteMeshCollectionInput
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for DeleteMeshCollection """
        document = 'mutation DeleteMeshCollection($input: DeleteMeshCollectionInput!) {\n  deleteMeshCollection(input: $input)\n}'

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

class CreatePhasorLayerMutation(BaseModel):
    """No documentation found for this operation."""
    create_phasor_layer: LayerImageLayer = Field(alias='createPhasorLayer')
    'Create a layer that reduces one axis of a lens to a phasor and colors each pixel by it: a lifetime overlay over a FLIM (microtime) cube, or a spectral one over a hyperspectral cube'

    class Arguments(BaseModel):
        """Arguments for CreatePhasorLayer """
        input: CreatePhasorLayerInput
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for CreatePhasorLayer """
        document = 'fragment Layer on Layer {\n  id\n  scene {\n    id\n    name\n    __typename\n  }\n  ... on ImageLayer {\n    lens {\n      id\n    }\n  }\n  __typename\n}\n\nmutation CreatePhasorLayer($input: CreatePhasorLayerInput!) {\n  createPhasorLayer(input: $input) {\n    ...Layer\n    __typename\n  }\n}'

class CreatePhasorHistogramMutation(BaseModel):
    """No documentation found for this operation."""
    create_phasor_histogram: PhasorHistogram = Field(alias='createPhasorHistogram')
    'Attach a phasor distribution (the 2D g/s density at one axis and harmonic) to a dataset, so a client can range a phasor overlay without reading the cube'

    class Arguments(BaseModel):
        """Arguments for CreatePhasorHistogram """
        input: CreatePhasorHistogramInput
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for CreatePhasorHistogram """
        document = 'fragment PhasorHistogram on PhasorHistogram {\n  id\n  axis\n  harmonic\n  bins\n  gMin\n  gMax\n  sMin\n  sMax\n  total\n  calibrated\n  counts\n  profile\n  __typename\n}\n\nmutation CreatePhasorHistogram($input: CreatePhasorHistogramInput!) {\n  createPhasorHistogram(input: $input) {\n    ...PhasorHistogram\n    __typename\n  }\n}'

class CreatePhasorCalibrationMutation(BaseModel):
    """No documentation found for this operation."""
    create_phasor_calibration: PhasorCalibration = Field(alias='createPhasorCalibration')
    'Attach an instrument-response correction to a dataset, taking a raw phasor to a calibrated one'

    class Arguments(BaseModel):
        """Arguments for CreatePhasorCalibration """
        input: CreatePhasorCalibrationInput
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for CreatePhasorCalibration """
        document = 'fragment PhasorCalibration on PhasorCalibration {\n  id\n  axis\n  harmonic\n  phaseOffset\n  modulationFactor\n  reference\n  __typename\n}\n\nmutation CreatePhasorCalibration($input: CreatePhasorCalibrationInput!) {\n  createPhasorCalibration(input: $input) {\n    ...PhasorCalibration\n    __typename\n  }\n}'

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
    'Create a new scene over a world coordinate system: an adopted existing system, or an ordinary SHARED one created for it (never owned by the scene -- it outlives it)'

    class Arguments(BaseModel):
        """Arguments for CreateScene """
        input: CreateSceneInput
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for CreateScene """
        document = 'fragment Axis on Axis {\n  id\n  order\n  name\n  type\n  unit\n  longName\n  __typename\n}\n\nfragment CoordinateSystem on CoordinateSystem {\n  id\n  name\n  epoch\n  axes {\n    ...Axis\n    __typename\n  }\n  __typename\n}\n\nfragment Scene on Scene {\n  name\n  id\n  preferredView\n  backgroundColor\n  worldCoordinateSystem {\n    ...CoordinateSystem\n    __typename\n  }\n  __typename\n}\n\nmutation CreateScene($input: CreateSceneInput!) {\n  createScene(input: $input) {\n    ...Scene\n    __typename\n  }\n}'

class CreateSceneFromCoordinateSystemMutation(BaseModel):
    """No documentation found for this operation."""
    create_scene_from_coordinate_system: Scene = Field(alias='createSceneFromCoordinateSystem')
    "Bootstrap a renderable scene over an existing coordinate system: a shared space (its registered sources become layers, up to the policy's nchildren) or an owned system such as a dataset's intrinsic grid or a physical space (the container's own data becomes the layer). The scene adopts the system as its world; no edges are authored. This is how a dataset is staged -- pass `intrinsicSystem` to render in pixels, or a physical space it is registered into to render at physical scale"

    class Arguments(BaseModel):
        """Arguments for CreateSceneFromCoordinateSystem """
        input: CreateSceneFromCoordinateSystemInput
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for CreateSceneFromCoordinateSystem """
        document = 'fragment Axis on Axis {\n  id\n  order\n  name\n  type\n  unit\n  longName\n  __typename\n}\n\nfragment CoordinateSystem on CoordinateSystem {\n  id\n  name\n  epoch\n  axes {\n    ...Axis\n    __typename\n  }\n  __typename\n}\n\nfragment Scene on Scene {\n  name\n  id\n  preferredView\n  backgroundColor\n  worldCoordinateSystem {\n    ...CoordinateSystem\n    __typename\n  }\n  __typename\n}\n\nmutation CreateSceneFromCoordinateSystem($input: CreateSceneFromCoordinateSystemInput!) {\n  createSceneFromCoordinateSystem(input: $input) {\n    ...Scene\n    __typename\n  }\n}'

class UpdateSceneMutation(BaseModel):
    """No documentation found for this operation."""
    update_scene: Scene = Field(alias='updateScene')
    "Set a scene's viewer preferences: how a client should open it"

    class Arguments(BaseModel):
        """Arguments for UpdateScene """
        input: UpdateSceneInput
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for UpdateScene """
        document = 'fragment Axis on Axis {\n  id\n  order\n  name\n  type\n  unit\n  longName\n  __typename\n}\n\nfragment CoordinateSystem on CoordinateSystem {\n  id\n  name\n  epoch\n  axes {\n    ...Axis\n    __typename\n  }\n  __typename\n}\n\nfragment Scene on Scene {\n  name\n  id\n  preferredView\n  backgroundColor\n  worldCoordinateSystem {\n    ...CoordinateSystem\n    __typename\n  }\n  __typename\n}\n\nmutation UpdateScene($input: UpdateSceneInput!) {\n  updateScene(input: $input) {\n    ...Scene\n    __typename\n  }\n}'

class ClearSceneMutation(BaseModel):
    """No documentation found for this operation."""
    clear_scene: Scene = Field(alias='clearScene')
    'Delete every layer of a scene, keeping the scene itself. A pure view-state reset: no coordinate system, registration or dataset is touched, and other scenes over the same space never notice'

    class Arguments(BaseModel):
        """Arguments for ClearScene """
        input: ClearSceneInput
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for ClearScene """
        document = 'fragment Axis on Axis {\n  id\n  order\n  name\n  type\n  unit\n  longName\n  __typename\n}\n\nfragment CoordinateSystem on CoordinateSystem {\n  id\n  name\n  epoch\n  axes {\n    ...Axis\n    __typename\n  }\n  __typename\n}\n\nfragment Scene on Scene {\n  name\n  id\n  preferredView\n  backgroundColor\n  worldCoordinateSystem {\n    ...CoordinateSystem\n    __typename\n  }\n  __typename\n}\n\nmutation ClearScene($input: ClearSceneInput!) {\n  clearScene(input: $input) {\n    ...Scene\n    __typename\n  }\n}'

class DeleteSceneMutation(BaseModel):
    """No documentation found for this operation."""
    delete_scene: ID = Field(alias='deleteScene')
    'Delete an existing scene'

    class Arguments(BaseModel):
        """Arguments for DeleteScene """
        input: DeleteSceneInput
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for DeleteScene """
        document = 'mutation DeleteScene($input: DeleteSceneInput!) {\n  deleteScene(input: $input)\n}'

class CreateSceneSnapshotMutation(BaseModel):
    """No documentation found for this operation."""
    create_scene_snapshot: SceneSnapshot = Field(alias='createSceneSnapshot')
    'Adopt an uploaded media file as a pre-rendered picture of a scene'

    class Arguments(BaseModel):
        """Arguments for CreateSceneSnapshot """
        input: SceneSnapshotInput
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for CreateSceneSnapshot """
        document = 'fragment Axis on Axis {\n  id\n  order\n  name\n  type\n  unit\n  longName\n  __typename\n}\n\nfragment CoordinateSystem on CoordinateSystem {\n  id\n  name\n  epoch\n  axes {\n    ...Axis\n    __typename\n  }\n  __typename\n}\n\nfragment MediaStore on MediaStore {\n  id\n  key\n  bucket\n  path\n  __typename\n}\n\nfragment Scene on Scene {\n  name\n  id\n  preferredView\n  backgroundColor\n  worldCoordinateSystem {\n    ...CoordinateSystem\n    __typename\n  }\n  __typename\n}\n\nfragment SceneSnapshot on SceneSnapshot {\n  id\n  name\n  majorColor\n  scene {\n    ...Scene\n    __typename\n  }\n  store {\n    ...MediaStore\n    __typename\n  }\n  __typename\n}\n\nmutation CreateSceneSnapshot($input: SceneSnapshotInput!) {\n  createSceneSnapshot(input: $input) {\n    ...SceneSnapshot\n    __typename\n  }\n}'

class DeleteSceneSnapshotMutation(BaseModel):
    """No documentation found for this operation."""
    delete_scene_snapshot: ID = Field(alias='deleteSceneSnapshot')
    'Delete an existing scene snapshot'

    class Arguments(BaseModel):
        """Arguments for DeleteSceneSnapshot """
        input: DeleteSceneSnapshotInput
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for DeleteSceneSnapshot """
        document = 'mutation DeleteSceneSnapshot($input: DeleteSceneSnapshotInput!) {\n  deleteSceneSnapshot(input: $input)\n}'

class PinSceneSnapshotMutation(BaseModel):
    """No documentation found for this operation."""
    pin_scene_snapshot: SceneSnapshot = Field(alias='pinSceneSnapshot')
    'Pin a scene snapshot for quick access'

    class Arguments(BaseModel):
        """Arguments for PinSceneSnapshot """
        input: PinSceneSnapshotInput
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for PinSceneSnapshot """
        document = 'fragment Axis on Axis {\n  id\n  order\n  name\n  type\n  unit\n  longName\n  __typename\n}\n\nfragment CoordinateSystem on CoordinateSystem {\n  id\n  name\n  epoch\n  axes {\n    ...Axis\n    __typename\n  }\n  __typename\n}\n\nfragment MediaStore on MediaStore {\n  id\n  key\n  bucket\n  path\n  __typename\n}\n\nfragment Scene on Scene {\n  name\n  id\n  preferredView\n  backgroundColor\n  worldCoordinateSystem {\n    ...CoordinateSystem\n    __typename\n  }\n  __typename\n}\n\nfragment SceneSnapshot on SceneSnapshot {\n  id\n  name\n  majorColor\n  scene {\n    ...Scene\n    __typename\n  }\n  store {\n    ...MediaStore\n    __typename\n  }\n  __typename\n}\n\nmutation PinSceneSnapshot($input: PinSceneSnapshotInput!) {\n  pinSceneSnapshot(input: $input) {\n    ...SceneSnapshot\n    __typename\n  }\n}'

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

class CreateTableDatasetMutation(BaseModel):
    """No documentation found for this operation."""
    create_table_dataset: TableDataset = Field(alias='createTableDataset')
    'Create a table dataset from a Parquet store. Its declared coordinate columns become the axes of a coordinate system it owns, which lets a localization table be placed in a scene; a table with no coordinate columns is a measurement table whose rows enumerate objects and whose lineage edge is UNMAPPABLE'

    class Arguments(BaseModel):
        """Arguments for CreateTableDataset """
        input: CreateTableDatasetInput
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for CreateTableDataset """
        document = 'fragment Axis on Axis {\n  id\n  order\n  name\n  type\n  unit\n  longName\n  __typename\n}\n\nfragment TransformationChild on Transformation {\n  __typename\n  id\n  kind\n  inputAxes\n  outputAxes\n  ... on ScaleTransformation {\n    scale\n  }\n  ... on TranslationTransformation {\n    translation\n  }\n  ... on AffineTransformation {\n    affine\n  }\n  ... on RotationTransformation {\n    affine\n  }\n}\n\nfragment CoordinateSystem on CoordinateSystem {\n  id\n  name\n  epoch\n  axes {\n    ...Axis\n    __typename\n  }\n  __typename\n}\n\nfragment ParquetStore on ParquetStore {\n  id\n  key\n  bucket\n  path\n  __typename\n}\n\nfragment Transformation on Transformation {\n  id\n  kind\n  name\n  version\n  input {\n    ...CoordinateSystem\n    __typename\n  }\n  output {\n    ...CoordinateSystem\n    __typename\n  }\n  ... on ScaleTransformation {\n    scale\n  }\n  ... on TranslationTransformation {\n    translation\n  }\n  ... on AffineTransformation {\n    affine\n  }\n  ... on RotationTransformation {\n    affine\n  }\n  ... on MapAxisTransformation {\n    inputAxes\n    outputAxes\n  }\n  ... on FieldTransformation {\n    field {\n      ...CoordinateSystem\n    }\n  }\n  ... on SequenceTransformation {\n    sequenceChildren: transformations {\n      ...TransformationChild\n    }\n  }\n  ... on ByDimensionTransformation {\n    inputAxes\n    outputAxes\n    byDimensionChildren: transformations {\n      ...TransformationChild\n    }\n  }\n  ... on BijectionTransformation {\n    bijectionChildren: transformations {\n      ...TransformationChild\n    }\n  }\n  __typename\n}\n\nfragment TableDataset on TableDataset {\n  id\n  name\n  description\n  store {\n    ...ParquetStore\n    __typename\n  }\n  columns {\n    id\n    order\n    name\n    dtype\n    role\n    axisType\n    unit\n    longName\n    __typename\n  }\n  coordinateSystem {\n    ...CoordinateSystem\n    __typename\n  }\n  derivedFrom {\n    ...Transformation\n    __typename\n  }\n  axisNames\n  provenanceMetadata\n  __typename\n}\n\nmutation CreateTableDataset($input: CreateTableDatasetInput!) {\n  createTableDataset(input: $input) {\n    ...TableDataset\n    __typename\n  }\n}'

class UpdateTableDatasetMutation(BaseModel):
    """No documentation found for this operation."""
    update_table_dataset: TableDataset = Field(alias='updateTableDataset')
    'Rename a table dataset or redescribe it -- the whole of what is editable. Its store, columns and coordinate system are fixed at creation; a recomputation is a new table'

    class Arguments(BaseModel):
        """Arguments for UpdateTableDataset """
        input: UpdateTableDatasetInput
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for UpdateTableDataset """
        document = 'fragment Axis on Axis {\n  id\n  order\n  name\n  type\n  unit\n  longName\n  __typename\n}\n\nfragment TransformationChild on Transformation {\n  __typename\n  id\n  kind\n  inputAxes\n  outputAxes\n  ... on ScaleTransformation {\n    scale\n  }\n  ... on TranslationTransformation {\n    translation\n  }\n  ... on AffineTransformation {\n    affine\n  }\n  ... on RotationTransformation {\n    affine\n  }\n}\n\nfragment CoordinateSystem on CoordinateSystem {\n  id\n  name\n  epoch\n  axes {\n    ...Axis\n    __typename\n  }\n  __typename\n}\n\nfragment ParquetStore on ParquetStore {\n  id\n  key\n  bucket\n  path\n  __typename\n}\n\nfragment Transformation on Transformation {\n  id\n  kind\n  name\n  version\n  input {\n    ...CoordinateSystem\n    __typename\n  }\n  output {\n    ...CoordinateSystem\n    __typename\n  }\n  ... on ScaleTransformation {\n    scale\n  }\n  ... on TranslationTransformation {\n    translation\n  }\n  ... on AffineTransformation {\n    affine\n  }\n  ... on RotationTransformation {\n    affine\n  }\n  ... on MapAxisTransformation {\n    inputAxes\n    outputAxes\n  }\n  ... on FieldTransformation {\n    field {\n      ...CoordinateSystem\n    }\n  }\n  ... on SequenceTransformation {\n    sequenceChildren: transformations {\n      ...TransformationChild\n    }\n  }\n  ... on ByDimensionTransformation {\n    inputAxes\n    outputAxes\n    byDimensionChildren: transformations {\n      ...TransformationChild\n    }\n  }\n  ... on BijectionTransformation {\n    bijectionChildren: transformations {\n      ...TransformationChild\n    }\n  }\n  __typename\n}\n\nfragment TableDataset on TableDataset {\n  id\n  name\n  description\n  store {\n    ...ParquetStore\n    __typename\n  }\n  columns {\n    id\n    order\n    name\n    dtype\n    role\n    axisType\n    unit\n    longName\n    __typename\n  }\n  coordinateSystem {\n    ...CoordinateSystem\n    __typename\n  }\n  derivedFrom {\n    ...Transformation\n    __typename\n  }\n  axisNames\n  provenanceMetadata\n  __typename\n}\n\nmutation UpdateTableDataset($input: UpdateTableDatasetInput!) {\n  updateTableDataset(input: $input) {\n    ...TableDataset\n    __typename\n  }\n}'

class DeleteTableDatasetMutation(BaseModel):
    """No documentation found for this operation."""
    delete_table_dataset: ID = Field(alias='deleteTableDataset')
    'Delete an existing table dataset'

    class Arguments(BaseModel):
        """Arguments for DeleteTableDataset """
        input: DeleteTableDatasetInput
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for DeleteTableDataset """
        document = 'mutation DeleteTableDataset($input: DeleteTableDatasetInput!) {\n  deleteTableDataset(input: $input)\n}'

class CreateTransformationMutationCreatetransformationBase(BaseModel):
    """A directed edge of the coordinate graph, mapping `input` to `output`. Direction is always forward. The concrete kind (Scale, Translation, Affine, Sequence, ...) carries the parameters"""
    model_config = ConfigDict(frozen=True)

class CreateTransformationMutationCreatetransformationBaseAffineTransformation(TransformationAffineTransformation, CreateTransformationMutationCreatetransformationBase, TransformationTrait, BaseModel):
    """A general affine map, given as an M x (N+1) matrix with rows outermost"""
    typename: Literal['AffineTransformation'] = Field(alias='__typename', default='AffineTransformation', exclude=True)

class CreateTransformationMutationCreatetransformationBaseBijectionTransformation(TransformationBijectionTransformation, CreateTransformationMutationCreatetransformationBase, TransformationTrait, BaseModel):
    """A pair of child transformations giving an explicit forward and inverse map"""
    typename: Literal['BijectionTransformation'] = Field(alias='__typename', default='BijectionTransformation', exclude=True)

class CreateTransformationMutationCreatetransformationBaseByDimensionTransformation(TransformationByDimensionTransformation, CreateTransformationMutationCreatetransformationBase, TransformationTrait, BaseModel):
    """A composition of child transformations, each acting on a named subset of the axes"""
    typename: Literal['ByDimensionTransformation'] = Field(alias='__typename', default='ByDimensionTransformation', exclude=True)

class CreateTransformationMutationCreatetransformationBaseFieldTransformation(TransformationFieldTransformation, CreateTransformationMutationCreatetransformationBase, TransformationTrait, BaseModel):
    """A non-affine map given by the values of an array rather than by a formula. The array is a `field`: a node of this graph, not a payload on this edge, so it keeps its own lineage and its axes say what its numbers mean. It has no closed-form inverse, so a placement path never walks it backwards"""
    typename: Literal['FieldTransformation'] = Field(alias='__typename', default='FieldTransformation', exclude=True)

class CreateTransformationMutationCreatetransformationBaseIdentityTransformation(TransformationIdentityTransformation, CreateTransformationMutationCreatetransformationBase, TransformationTrait, BaseModel):
    """The identity map: input and output coordinates are the same"""
    typename: Literal['IdentityTransformation'] = Field(alias='__typename', default='IdentityTransformation', exclude=True)

class CreateTransformationMutationCreatetransformationBaseMapAxisTransformation(TransformationMapAxisTransformation, CreateTransformationMutationCreatetransformationBase, TransformationTrait, BaseModel):
    """A permutation of axes, mapping each input axis to an output axis by name"""
    typename: Literal['MapAxisTransformation'] = Field(alias='__typename', default='MapAxisTransformation', exclude=True)

class CreateTransformationMutationCreatetransformationBaseRotationTransformation(TransformationRotationTransformation, CreateTransformationMutationCreatetransformationBase, TransformationTrait, BaseModel):
    """A rotation, given as an orthonormal matrix"""
    typename: Literal['RotationTransformation'] = Field(alias='__typename', default='RotationTransformation', exclude=True)

class CreateTransformationMutationCreatetransformationBaseScaleTransformation(TransformationScaleTransformation, CreateTransformationMutationCreatetransformationBase, TransformationTrait, BaseModel):
    """A per-axis multiplication, with one entry per input axis"""
    typename: Literal['ScaleTransformation'] = Field(alias='__typename', default='ScaleTransformation', exclude=True)

class CreateTransformationMutationCreatetransformationBaseSequenceTransformation(TransformationSequenceTransformation, CreateTransformationMutationCreatetransformationBase, TransformationTrait, BaseModel):
    """An ordered composition of child transformations, applied first to last"""
    typename: Literal['SequenceTransformation'] = Field(alias='__typename', default='SequenceTransformation', exclude=True)

class CreateTransformationMutationCreatetransformationBaseTranslationTransformation(TransformationTranslationTransformation, CreateTransformationMutationCreatetransformationBase, TransformationTrait, BaseModel):
    """A per-axis offset, with one entry per input axis"""
    typename: Literal['TranslationTransformation'] = Field(alias='__typename', default='TranslationTransformation', exclude=True)

class CreateTransformationMutationCreatetransformationBaseUnmappableTransformation(TransformationUnmappableTransformation, CreateTransformationMutationCreatetransformationBase, TransformationTrait, BaseModel):
    """A declared NON-correspondence: the two systems are related -- one was computed from the other -- and no point of either maps to a point of the other. It has no parameters, no rank and no matrix, and no placement search will walk it, in either direction. This is what a per-object measurement table's relation to the image it was measured from looks like"""
    typename: Literal['UnmappableTransformation'] = Field(alias='__typename', default='UnmappableTransformation', exclude=True)

class CreateTransformationMutationCreatetransformationBaseCatchAll(CreateTransformationMutationCreatetransformationBase, BaseModel):
    """Catch all class for CreateTransformationMutationCreatetransformationBase"""
    typename: str = Field(alias='__typename', exclude=True)

class CreateTransformationMutation(BaseModel):
    """No documentation found for this operation."""
    create_transformation: Union[Annotated[Union[CreateTransformationMutationCreatetransformationBaseAffineTransformation, CreateTransformationMutationCreatetransformationBaseBijectionTransformation, CreateTransformationMutationCreatetransformationBaseByDimensionTransformation, CreateTransformationMutationCreatetransformationBaseFieldTransformation, CreateTransformationMutationCreatetransformationBaseIdentityTransformation, CreateTransformationMutationCreatetransformationBaseMapAxisTransformation, CreateTransformationMutationCreatetransformationBaseRotationTransformation, CreateTransformationMutationCreatetransformationBaseScaleTransformation, CreateTransformationMutationCreatetransformationBaseSequenceTransformation, CreateTransformationMutationCreatetransformationBaseTranslationTransformation, CreateTransformationMutationCreatetransformationBaseUnmappableTransformation], Field(discriminator='typename')], CreateTransformationMutationCreatetransformationBaseCatchAll] = Field(alias='createTransformation')
    'Create one edge of the coordinate graph, mapping an input coordinate system to an output one. This is where registration lives'

    class Arguments(BaseModel):
        """Arguments for CreateTransformation """
        input: CreateTransformationInput
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for CreateTransformation """
        document = 'fragment Axis on Axis {\n  id\n  order\n  name\n  type\n  unit\n  longName\n  __typename\n}\n\nfragment CoordinateSystem on CoordinateSystem {\n  id\n  name\n  epoch\n  axes {\n    ...Axis\n    __typename\n  }\n  __typename\n}\n\nfragment TransformationChild on Transformation {\n  __typename\n  id\n  kind\n  inputAxes\n  outputAxes\n  ... on ScaleTransformation {\n    scale\n  }\n  ... on TranslationTransformation {\n    translation\n  }\n  ... on AffineTransformation {\n    affine\n  }\n  ... on RotationTransformation {\n    affine\n  }\n}\n\nfragment Transformation on Transformation {\n  id\n  kind\n  name\n  version\n  input {\n    ...CoordinateSystem\n    __typename\n  }\n  output {\n    ...CoordinateSystem\n    __typename\n  }\n  ... on ScaleTransformation {\n    scale\n  }\n  ... on TranslationTransformation {\n    translation\n  }\n  ... on AffineTransformation {\n    affine\n  }\n  ... on RotationTransformation {\n    affine\n  }\n  ... on MapAxisTransformation {\n    inputAxes\n    outputAxes\n  }\n  ... on FieldTransformation {\n    field {\n      ...CoordinateSystem\n    }\n  }\n  ... on SequenceTransformation {\n    sequenceChildren: transformations {\n      ...TransformationChild\n    }\n  }\n  ... on ByDimensionTransformation {\n    inputAxes\n    outputAxes\n    byDimensionChildren: transformations {\n      ...TransformationChild\n    }\n  }\n  ... on BijectionTransformation {\n    bijectionChildren: transformations {\n      ...TransformationChild\n    }\n  }\n  __typename\n}\n\nmutation CreateTransformation($input: CreateTransformationInput!) {\n  createTransformation(input: $input) {\n    ...Transformation\n    __typename\n  }\n}'

class UpdateTransformationMutationUpdatetransformationBase(BaseModel):
    """A directed edge of the coordinate graph, mapping `input` to `output`. Direction is always forward. The concrete kind (Scale, Translation, Affine, Sequence, ...) carries the parameters"""
    model_config = ConfigDict(frozen=True)

class UpdateTransformationMutationUpdatetransformationBaseAffineTransformation(TransformationAffineTransformation, UpdateTransformationMutationUpdatetransformationBase, TransformationTrait, BaseModel):
    """A general affine map, given as an M x (N+1) matrix with rows outermost"""
    typename: Literal['AffineTransformation'] = Field(alias='__typename', default='AffineTransformation', exclude=True)

class UpdateTransformationMutationUpdatetransformationBaseBijectionTransformation(TransformationBijectionTransformation, UpdateTransformationMutationUpdatetransformationBase, TransformationTrait, BaseModel):
    """A pair of child transformations giving an explicit forward and inverse map"""
    typename: Literal['BijectionTransformation'] = Field(alias='__typename', default='BijectionTransformation', exclude=True)

class UpdateTransformationMutationUpdatetransformationBaseByDimensionTransformation(TransformationByDimensionTransformation, UpdateTransformationMutationUpdatetransformationBase, TransformationTrait, BaseModel):
    """A composition of child transformations, each acting on a named subset of the axes"""
    typename: Literal['ByDimensionTransformation'] = Field(alias='__typename', default='ByDimensionTransformation', exclude=True)

class UpdateTransformationMutationUpdatetransformationBaseFieldTransformation(TransformationFieldTransformation, UpdateTransformationMutationUpdatetransformationBase, TransformationTrait, BaseModel):
    """A non-affine map given by the values of an array rather than by a formula. The array is a `field`: a node of this graph, not a payload on this edge, so it keeps its own lineage and its axes say what its numbers mean. It has no closed-form inverse, so a placement path never walks it backwards"""
    typename: Literal['FieldTransformation'] = Field(alias='__typename', default='FieldTransformation', exclude=True)

class UpdateTransformationMutationUpdatetransformationBaseIdentityTransformation(TransformationIdentityTransformation, UpdateTransformationMutationUpdatetransformationBase, TransformationTrait, BaseModel):
    """The identity map: input and output coordinates are the same"""
    typename: Literal['IdentityTransformation'] = Field(alias='__typename', default='IdentityTransformation', exclude=True)

class UpdateTransformationMutationUpdatetransformationBaseMapAxisTransformation(TransformationMapAxisTransformation, UpdateTransformationMutationUpdatetransformationBase, TransformationTrait, BaseModel):
    """A permutation of axes, mapping each input axis to an output axis by name"""
    typename: Literal['MapAxisTransformation'] = Field(alias='__typename', default='MapAxisTransformation', exclude=True)

class UpdateTransformationMutationUpdatetransformationBaseRotationTransformation(TransformationRotationTransformation, UpdateTransformationMutationUpdatetransformationBase, TransformationTrait, BaseModel):
    """A rotation, given as an orthonormal matrix"""
    typename: Literal['RotationTransformation'] = Field(alias='__typename', default='RotationTransformation', exclude=True)

class UpdateTransformationMutationUpdatetransformationBaseScaleTransformation(TransformationScaleTransformation, UpdateTransformationMutationUpdatetransformationBase, TransformationTrait, BaseModel):
    """A per-axis multiplication, with one entry per input axis"""
    typename: Literal['ScaleTransformation'] = Field(alias='__typename', default='ScaleTransformation', exclude=True)

class UpdateTransformationMutationUpdatetransformationBaseSequenceTransformation(TransformationSequenceTransformation, UpdateTransformationMutationUpdatetransformationBase, TransformationTrait, BaseModel):
    """An ordered composition of child transformations, applied first to last"""
    typename: Literal['SequenceTransformation'] = Field(alias='__typename', default='SequenceTransformation', exclude=True)

class UpdateTransformationMutationUpdatetransformationBaseTranslationTransformation(TransformationTranslationTransformation, UpdateTransformationMutationUpdatetransformationBase, TransformationTrait, BaseModel):
    """A per-axis offset, with one entry per input axis"""
    typename: Literal['TranslationTransformation'] = Field(alias='__typename', default='TranslationTransformation', exclude=True)

class UpdateTransformationMutationUpdatetransformationBaseUnmappableTransformation(TransformationUnmappableTransformation, UpdateTransformationMutationUpdatetransformationBase, TransformationTrait, BaseModel):
    """A declared NON-correspondence: the two systems are related -- one was computed from the other -- and no point of either maps to a point of the other. It has no parameters, no rank and no matrix, and no placement search will walk it, in either direction. This is what a per-object measurement table's relation to the image it was measured from looks like"""
    typename: Literal['UnmappableTransformation'] = Field(alias='__typename', default='UnmappableTransformation', exclude=True)

class UpdateTransformationMutationUpdatetransformationBaseCatchAll(UpdateTransformationMutationUpdatetransformationBase, BaseModel):
    """Catch all class for UpdateTransformationMutationUpdatetransformationBase"""
    typename: str = Field(alias='__typename', exclude=True)

class UpdateTransformationMutation(BaseModel):
    """No documentation found for this operation."""
    update_transformation: Union[Annotated[Union[UpdateTransformationMutationUpdatetransformationBaseAffineTransformation, UpdateTransformationMutationUpdatetransformationBaseBijectionTransformation, UpdateTransformationMutationUpdatetransformationBaseByDimensionTransformation, UpdateTransformationMutationUpdatetransformationBaseFieldTransformation, UpdateTransformationMutationUpdatetransformationBaseIdentityTransformation, UpdateTransformationMutationUpdatetransformationBaseMapAxisTransformation, UpdateTransformationMutationUpdatetransformationBaseRotationTransformation, UpdateTransformationMutationUpdatetransformationBaseScaleTransformation, UpdateTransformationMutationUpdatetransformationBaseSequenceTransformation, UpdateTransformationMutationUpdatetransformationBaseTranslationTransformation, UpdateTransformationMutationUpdatetransformationBaseUnmappableTransformation], Field(discriminator='typename')], UpdateTransformationMutationUpdatetransformationBaseCatchAll] = Field(alias='updateTransformation')
    "Refine a transformation's parameters, bumping its version"

    class Arguments(BaseModel):
        """Arguments for UpdateTransformation """
        input: UpdateTransformationInput
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for UpdateTransformation """
        document = 'fragment Axis on Axis {\n  id\n  order\n  name\n  type\n  unit\n  longName\n  __typename\n}\n\nfragment CoordinateSystem on CoordinateSystem {\n  id\n  name\n  epoch\n  axes {\n    ...Axis\n    __typename\n  }\n  __typename\n}\n\nfragment TransformationChild on Transformation {\n  __typename\n  id\n  kind\n  inputAxes\n  outputAxes\n  ... on ScaleTransformation {\n    scale\n  }\n  ... on TranslationTransformation {\n    translation\n  }\n  ... on AffineTransformation {\n    affine\n  }\n  ... on RotationTransformation {\n    affine\n  }\n}\n\nfragment Transformation on Transformation {\n  id\n  kind\n  name\n  version\n  input {\n    ...CoordinateSystem\n    __typename\n  }\n  output {\n    ...CoordinateSystem\n    __typename\n  }\n  ... on ScaleTransformation {\n    scale\n  }\n  ... on TranslationTransformation {\n    translation\n  }\n  ... on AffineTransformation {\n    affine\n  }\n  ... on RotationTransformation {\n    affine\n  }\n  ... on MapAxisTransformation {\n    inputAxes\n    outputAxes\n  }\n  ... on FieldTransformation {\n    field {\n      ...CoordinateSystem\n    }\n  }\n  ... on SequenceTransformation {\n    sequenceChildren: transformations {\n      ...TransformationChild\n    }\n  }\n  ... on ByDimensionTransformation {\n    inputAxes\n    outputAxes\n    byDimensionChildren: transformations {\n      ...TransformationChild\n    }\n  }\n  ... on BijectionTransformation {\n    bijectionChildren: transformations {\n      ...TransformationChild\n    }\n  }\n  __typename\n}\n\nmutation UpdateTransformation($input: UpdateTransformationInput!) {\n  updateTransformation(input: $input) {\n    ...Transformation\n    __typename\n  }\n}'

class DeleteTransformationMutation(BaseModel):
    """No documentation found for this operation."""
    delete_transformation: ID = Field(alias='deleteTransformation')
    'Delete an existing transformation'

    class Arguments(BaseModel):
        """Arguments for DeleteTransformation """
        input: DeleteTransformationInput
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for DeleteTransformation """
        document = 'mutation DeleteTransformation($input: DeleteTransformationInput!) {\n  deleteTransformation(input: $input)\n}'

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

class GetADatasetQuery(BaseModel):
    """No documentation found for this operation."""
    adataset: ADataset
    'Get a single array dataset by ID'

    class Arguments(BaseModel):
        """Arguments for GetADataset """
        id: ID
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for GetADataset """
        document = 'fragment Axis on Axis {\n  id\n  order\n  name\n  type\n  unit\n  longName\n  __typename\n}\n\nfragment CoordinateSystem on CoordinateSystem {\n  id\n  name\n  epoch\n  axes {\n    ...Axis\n    __typename\n  }\n  __typename\n}\n\nfragment ZarrStore on ZarrStore {\n  id\n  key\n  bucket\n  path\n  __typename\n}\n\nfragment ADataset on ADataset {\n  id\n  name\n  axisNames\n  shape\n  multiscale\n  intrinsicSystem {\n    ...CoordinateSystem\n    __typename\n  }\n  dataArrays {\n    id\n    level\n    shape\n    chunkShape\n    store {\n      ...ZarrStore\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nquery GetADataset($id: ID!) {\n  adataset(id: $id) {\n    ...ADataset\n    __typename\n  }\n}'

class GetADatasetsQuery(BaseModel):
    """No documentation found for this operation."""
    adatasets: Tuple[ADataset, ...]
    'List array datasets (N-dimensional arrays with named dimensions and anchored metadata)'

    class Arguments(BaseModel):
        """Arguments for GetADatasets """
        filters: Optional[ADatasetFilter] = Field(default=None)
        pagination: Optional[OffsetPaginationInput] = Field(default=None)
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for GetADatasets """
        document = 'fragment Axis on Axis {\n  id\n  order\n  name\n  type\n  unit\n  longName\n  __typename\n}\n\nfragment CoordinateSystem on CoordinateSystem {\n  id\n  name\n  epoch\n  axes {\n    ...Axis\n    __typename\n  }\n  __typename\n}\n\nfragment ZarrStore on ZarrStore {\n  id\n  key\n  bucket\n  path\n  __typename\n}\n\nfragment ADataset on ADataset {\n  id\n  name\n  axisNames\n  shape\n  multiscale\n  intrinsicSystem {\n    ...CoordinateSystem\n    __typename\n  }\n  dataArrays {\n    id\n    level\n    shape\n    chunkShape\n    store {\n      ...ZarrStore\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nquery GetADatasets($filters: ADatasetFilter, $pagination: OffsetPaginationInput) {\n  adatasets(filters: $filters, pagination: $pagination) {\n    ...ADataset\n    __typename\n  }\n}'

class SearchADatasetsQueryOptions(DatasetTrait, BaseModel):
    """A multi-dimensional array dataset. Its dimensions and their types live on the axes of its INTRINSIC (pixel grid) coordinate system; physical units live on the physical spaces it has edges into; its pyramid levels are DataArrays, each mapping into its grid"""
    typename: Literal['ADataset'] = Field(alias='__typename', default='ADataset', exclude=True)
    value: ID
    label: str
    model_config = ConfigDict(frozen=True)

class SearchADatasetsQuery(BaseModel):
    """No documentation found for this operation."""
    options: Tuple[SearchADatasetsQueryOptions, ...]
    'List array datasets (N-dimensional arrays with named dimensions and anchored metadata)'

    class Arguments(BaseModel):
        """Arguments for SearchADatasets """
        search: Optional[str] = Field(default=None)
        values: Optional[List[ID]] = Field(default=None)
        limit: Optional[int] = Field(default=None)
        offset: Annotated[Optional[int], GraphQLDefault('0')] = Field(default=None)
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for SearchADatasets """
        document = 'query SearchADatasets($search: String, $values: [ID!], $limit: Int, $offset: Int = 0) {\n  options: adatasets(\n    filters: {search: $search, ids: $values}\n    pagination: {limit: $limit, offset: $offset}\n  ) {\n    value: id\n    label: name\n    __typename\n  }\n}'

class GetAnimationQuery(BaseModel):
    """No documentation found for this operation."""
    animation: Animation
    'Get a single animation by ID'

    class Arguments(BaseModel):
        """Arguments for GetAnimation """
        id: ID
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for GetAnimation """
        document = 'fragment Axis on Axis {\n  id\n  order\n  name\n  type\n  unit\n  longName\n  __typename\n}\n\nfragment CameraState on CameraState {\n  position\n  crossSectionOrientation\n  crossSectionScale\n  projectionOrientation\n  projectionScale\n  __typename\n}\n\nfragment CoordinateSystem on CoordinateSystem {\n  id\n  name\n  epoch\n  axes {\n    ...Axis\n    __typename\n  }\n  __typename\n}\n\nfragment AnimationWaypoint on AnimationWaypoint {\n  id\n  order\n  name\n  durationMs\n  easing\n  camera {\n    ...CameraState\n    __typename\n  }\n  __typename\n}\n\nfragment Scene on Scene {\n  name\n  id\n  preferredView\n  backgroundColor\n  worldCoordinateSystem {\n    ...CoordinateSystem\n    __typename\n  }\n  __typename\n}\n\nfragment Animation on Animation {\n  id\n  name\n  description\n  scene {\n    ...Scene\n    __typename\n  }\n  waypoints {\n    ...AnimationWaypoint\n    __typename\n  }\n  __typename\n}\n\nquery GetAnimation($id: ID!) {\n  animation(id: $id) {\n    ...Animation\n    __typename\n  }\n}'

class GetAnimationsQuery(BaseModel):
    """No documentation found for this operation."""
    animations: Tuple[Animation, ...]
    'List animations (named camera tours through a scene)'

    class Arguments(BaseModel):
        """Arguments for GetAnimations """
        filters: Optional[AnimationFilter] = Field(default=None)
        pagination: Optional[OffsetPaginationInput] = Field(default=None)
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for GetAnimations """
        document = 'fragment Axis on Axis {\n  id\n  order\n  name\n  type\n  unit\n  longName\n  __typename\n}\n\nfragment CameraState on CameraState {\n  position\n  crossSectionOrientation\n  crossSectionScale\n  projectionOrientation\n  projectionScale\n  __typename\n}\n\nfragment CoordinateSystem on CoordinateSystem {\n  id\n  name\n  epoch\n  axes {\n    ...Axis\n    __typename\n  }\n  __typename\n}\n\nfragment AnimationWaypoint on AnimationWaypoint {\n  id\n  order\n  name\n  durationMs\n  easing\n  camera {\n    ...CameraState\n    __typename\n  }\n  __typename\n}\n\nfragment Scene on Scene {\n  name\n  id\n  preferredView\n  backgroundColor\n  worldCoordinateSystem {\n    ...CoordinateSystem\n    __typename\n  }\n  __typename\n}\n\nfragment Animation on Animation {\n  id\n  name\n  description\n  scene {\n    ...Scene\n    __typename\n  }\n  waypoints {\n    ...AnimationWaypoint\n    __typename\n  }\n  __typename\n}\n\nquery GetAnimations($filters: AnimationFilter, $pagination: OffsetPaginationInput) {\n  animations(filters: $filters, pagination: $pagination) {\n    ...Animation\n    __typename\n  }\n}'

class SearchAnimationsQueryOptions(BaseModel):
    """A named camera tour of a scene: the poses a viewer pans through, in order. A view artifact -- it cascades with the scene, no placement walk crosses it, and refining a registration moves the data but never the camera"""
    typename: Literal['Animation'] = Field(alias='__typename', default='Animation', exclude=True)
    value: ID
    label: str
    model_config = ConfigDict(frozen=True)

class SearchAnimationsQuery(BaseModel):
    """No documentation found for this operation."""
    options: Tuple[SearchAnimationsQueryOptions, ...]
    'List animations (named camera tours through a scene)'

    class Arguments(BaseModel):
        """Arguments for SearchAnimations """
        search: Optional[str] = Field(default=None)
        values: Optional[List[ID]] = Field(default=None)
        limit: Optional[int] = Field(default=None)
        offset: Annotated[Optional[int], GraphQLDefault('0')] = Field(default=None)
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for SearchAnimations """
        document = 'query SearchAnimations($search: String, $values: [ID!], $limit: Int, $offset: Int = 0) {\n  options: animations(\n    filters: {search: $search, ids: $values}\n    pagination: {limit: $limit, offset: $offset}\n  ) {\n    value: id\n    label: name\n    __typename\n  }\n}'

class GetAnnotationQuery(BaseModel):
    """No documentation found for this operation."""
    annotation: Annotation
    'Get a single annotation by ID'

    class Arguments(BaseModel):
        """Arguments for GetAnnotation """
        id: ID
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for GetAnnotation """
        document = 'fragment Axis on Axis {\n  id\n  order\n  name\n  type\n  unit\n  longName\n  __typename\n}\n\nfragment CoordinateSystem on CoordinateSystem {\n  id\n  name\n  epoch\n  axes {\n    ...Axis\n    __typename\n  }\n  __typename\n}\n\nfragment Annotation on Annotation {\n  id\n  name\n  kind\n  vectors\n  coordinates {\n    name\n    value\n    __typename\n  }\n  coordinateSystem {\n    ...CoordinateSystem\n    __typename\n  }\n  intrinsicBbox {\n    min\n    max\n    __typename\n  }\n  strokeColor\n  fillColor\n  strokeWidth\n  filled\n  __typename\n}\n\nquery GetAnnotation($id: ID!) {\n  annotation(id: $id) {\n    ...Annotation\n    __typename\n  }\n}'

class GetAnnotationsQuery(BaseModel):
    """No documentation found for this operation."""
    annotations: Tuple[Annotation, ...]
    "List annotations (human-drawn shapes, each in its collection's coordinate system)"

    class Arguments(BaseModel):
        """Arguments for GetAnnotations """
        filters: Optional[AnnotationFilter] = Field(default=None)
        pagination: Optional[OffsetPaginationInput] = Field(default=None)
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for GetAnnotations """
        document = 'fragment Axis on Axis {\n  id\n  order\n  name\n  type\n  unit\n  longName\n  __typename\n}\n\nfragment CoordinateSystem on CoordinateSystem {\n  id\n  name\n  epoch\n  axes {\n    ...Axis\n    __typename\n  }\n  __typename\n}\n\nfragment Annotation on Annotation {\n  id\n  name\n  kind\n  vectors\n  coordinates {\n    name\n    value\n    __typename\n  }\n  coordinateSystem {\n    ...CoordinateSystem\n    __typename\n  }\n  intrinsicBbox {\n    min\n    max\n    __typename\n  }\n  strokeColor\n  fillColor\n  strokeWidth\n  filled\n  __typename\n}\n\nquery GetAnnotations($filters: AnnotationFilter, $pagination: OffsetPaginationInput) {\n  annotations(filters: $filters, pagination: $pagination) {\n    ...Annotation\n    __typename\n  }\n}'

class GetAnnotationCollectionQuery(BaseModel):
    """No documentation found for this operation."""
    annotation_collection: AnnotationCollection = Field(alias='annotationCollection')
    'Get a single annotation collection by ID'

    class Arguments(BaseModel):
        """Arguments for GetAnnotationCollection """
        id: ID
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for GetAnnotationCollection """
        document = 'fragment Axis on Axis {\n  id\n  order\n  name\n  type\n  unit\n  longName\n  __typename\n}\n\nfragment Annotation on Annotation {\n  id\n  name\n  kind\n  vectors\n  coordinates {\n    name\n    value\n    __typename\n  }\n  coordinateSystem {\n    ...CoordinateSystem\n    __typename\n  }\n  intrinsicBbox {\n    min\n    max\n    __typename\n  }\n  strokeColor\n  fillColor\n  strokeWidth\n  filled\n  __typename\n}\n\nfragment CoordinateSystem on CoordinateSystem {\n  id\n  name\n  epoch\n  axes {\n    ...Axis\n    __typename\n  }\n  __typename\n}\n\nfragment AnnotationCollection on AnnotationCollection {\n  id\n  name\n  description\n  coordinateSystem {\n    ...CoordinateSystem\n    __typename\n  }\n  annotations {\n    ...Annotation\n    __typename\n  }\n  __typename\n}\n\nquery GetAnnotationCollection($id: ID!) {\n  annotationCollection(id: $id) {\n    ...AnnotationCollection\n    __typename\n  }\n}'

class GetAnnotationCollectionsQuery(BaseModel):
    """No documentation found for this operation."""
    annotation_collections: Tuple[AnnotationCollection, ...] = Field(alias='annotationCollections')
    'List annotation collections (named sets of human-drawn shapes, each owning the coordinate system they are drawn in)'

    class Arguments(BaseModel):
        """Arguments for GetAnnotationCollections """
        filters: Optional[AnnotationCollectionFilter] = Field(default=None)
        pagination: Optional[OffsetPaginationInput] = Field(default=None)
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for GetAnnotationCollections """
        document = 'fragment Axis on Axis {\n  id\n  order\n  name\n  type\n  unit\n  longName\n  __typename\n}\n\nfragment Annotation on Annotation {\n  id\n  name\n  kind\n  vectors\n  coordinates {\n    name\n    value\n    __typename\n  }\n  coordinateSystem {\n    ...CoordinateSystem\n    __typename\n  }\n  intrinsicBbox {\n    min\n    max\n    __typename\n  }\n  strokeColor\n  fillColor\n  strokeWidth\n  filled\n  __typename\n}\n\nfragment CoordinateSystem on CoordinateSystem {\n  id\n  name\n  epoch\n  axes {\n    ...Axis\n    __typename\n  }\n  __typename\n}\n\nfragment AnnotationCollection on AnnotationCollection {\n  id\n  name\n  description\n  coordinateSystem {\n    ...CoordinateSystem\n    __typename\n  }\n  annotations {\n    ...Annotation\n    __typename\n  }\n  __typename\n}\n\nquery GetAnnotationCollections($filters: AnnotationCollectionFilter, $pagination: OffsetPaginationInput) {\n  annotationCollections(filters: $filters, pagination: $pagination) {\n    ...AnnotationCollection\n    __typename\n  }\n}'

class SearchAnnotationCollectionsQueryOptions(BaseModel):
    """A named set of human-drawn annotations, owning the coordinate system they are drawn in. The CRUD counterpart of a table dataset's machine-produced rows: shapes a person draws and edits, sharing one drawing space and one registration story"""
    typename: Literal['AnnotationCollection'] = Field(alias='__typename', default='AnnotationCollection', exclude=True)
    value: ID
    label: str
    model_config = ConfigDict(frozen=True)

class SearchAnnotationCollectionsQuery(BaseModel):
    """No documentation found for this operation."""
    options: Tuple[SearchAnnotationCollectionsQueryOptions, ...]
    'List annotation collections (named sets of human-drawn shapes, each owning the coordinate system they are drawn in)'

    class Arguments(BaseModel):
        """Arguments for SearchAnnotationCollections """
        search: Optional[str] = Field(default=None)
        values: Optional[List[ID]] = Field(default=None)
        limit: Optional[int] = Field(default=None)
        offset: Annotated[Optional[int], GraphQLDefault('0')] = Field(default=None)
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for SearchAnnotationCollections """
        document = 'query SearchAnnotationCollections($search: String, $values: [ID!], $limit: Int, $offset: Int = 0) {\n  options: annotationCollections(\n    filters: {search: $search, ids: $values}\n    pagination: {limit: $limit, offset: $offset}\n  ) {\n    value: id\n    label: name\n    __typename\n  }\n}'

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

class GetCoordinateGraphQueryCoordinategraphTransformationsBase(BaseModel):
    """A directed edge of the coordinate graph, mapping `input` to `output`. Direction is always forward. The concrete kind (Scale, Translation, Affine, Sequence, ...) carries the parameters"""
    model_config = ConfigDict(frozen=True)

class GetCoordinateGraphQueryCoordinategraphTransformationsBaseAffineTransformation(TransformationAffineTransformation, GetCoordinateGraphQueryCoordinategraphTransformationsBase, TransformationTrait, BaseModel):
    """A general affine map, given as an M x (N+1) matrix with rows outermost"""
    typename: Literal['AffineTransformation'] = Field(alias='__typename', default='AffineTransformation', exclude=True)

class GetCoordinateGraphQueryCoordinategraphTransformationsBaseBijectionTransformation(TransformationBijectionTransformation, GetCoordinateGraphQueryCoordinategraphTransformationsBase, TransformationTrait, BaseModel):
    """A pair of child transformations giving an explicit forward and inverse map"""
    typename: Literal['BijectionTransformation'] = Field(alias='__typename', default='BijectionTransformation', exclude=True)

class GetCoordinateGraphQueryCoordinategraphTransformationsBaseByDimensionTransformation(TransformationByDimensionTransformation, GetCoordinateGraphQueryCoordinategraphTransformationsBase, TransformationTrait, BaseModel):
    """A composition of child transformations, each acting on a named subset of the axes"""
    typename: Literal['ByDimensionTransformation'] = Field(alias='__typename', default='ByDimensionTransformation', exclude=True)

class GetCoordinateGraphQueryCoordinategraphTransformationsBaseFieldTransformation(TransformationFieldTransformation, GetCoordinateGraphQueryCoordinategraphTransformationsBase, TransformationTrait, BaseModel):
    """A non-affine map given by the values of an array rather than by a formula. The array is a `field`: a node of this graph, not a payload on this edge, so it keeps its own lineage and its axes say what its numbers mean. It has no closed-form inverse, so a placement path never walks it backwards"""
    typename: Literal['FieldTransformation'] = Field(alias='__typename', default='FieldTransformation', exclude=True)

class GetCoordinateGraphQueryCoordinategraphTransformationsBaseIdentityTransformation(TransformationIdentityTransformation, GetCoordinateGraphQueryCoordinategraphTransformationsBase, TransformationTrait, BaseModel):
    """The identity map: input and output coordinates are the same"""
    typename: Literal['IdentityTransformation'] = Field(alias='__typename', default='IdentityTransformation', exclude=True)

class GetCoordinateGraphQueryCoordinategraphTransformationsBaseMapAxisTransformation(TransformationMapAxisTransformation, GetCoordinateGraphQueryCoordinategraphTransformationsBase, TransformationTrait, BaseModel):
    """A permutation of axes, mapping each input axis to an output axis by name"""
    typename: Literal['MapAxisTransformation'] = Field(alias='__typename', default='MapAxisTransformation', exclude=True)

class GetCoordinateGraphQueryCoordinategraphTransformationsBaseRotationTransformation(TransformationRotationTransformation, GetCoordinateGraphQueryCoordinategraphTransformationsBase, TransformationTrait, BaseModel):
    """A rotation, given as an orthonormal matrix"""
    typename: Literal['RotationTransformation'] = Field(alias='__typename', default='RotationTransformation', exclude=True)

class GetCoordinateGraphQueryCoordinategraphTransformationsBaseScaleTransformation(TransformationScaleTransformation, GetCoordinateGraphQueryCoordinategraphTransformationsBase, TransformationTrait, BaseModel):
    """A per-axis multiplication, with one entry per input axis"""
    typename: Literal['ScaleTransformation'] = Field(alias='__typename', default='ScaleTransformation', exclude=True)

class GetCoordinateGraphQueryCoordinategraphTransformationsBaseSequenceTransformation(TransformationSequenceTransformation, GetCoordinateGraphQueryCoordinategraphTransformationsBase, TransformationTrait, BaseModel):
    """An ordered composition of child transformations, applied first to last"""
    typename: Literal['SequenceTransformation'] = Field(alias='__typename', default='SequenceTransformation', exclude=True)

class GetCoordinateGraphQueryCoordinategraphTransformationsBaseTranslationTransformation(TransformationTranslationTransformation, GetCoordinateGraphQueryCoordinategraphTransformationsBase, TransformationTrait, BaseModel):
    """A per-axis offset, with one entry per input axis"""
    typename: Literal['TranslationTransformation'] = Field(alias='__typename', default='TranslationTransformation', exclude=True)

class GetCoordinateGraphQueryCoordinategraphTransformationsBaseUnmappableTransformation(TransformationUnmappableTransformation, GetCoordinateGraphQueryCoordinategraphTransformationsBase, TransformationTrait, BaseModel):
    """A declared NON-correspondence: the two systems are related -- one was computed from the other -- and no point of either maps to a point of the other. It has no parameters, no rank and no matrix, and no placement search will walk it, in either direction. This is what a per-object measurement table's relation to the image it was measured from looks like"""
    typename: Literal['UnmappableTransformation'] = Field(alias='__typename', default='UnmappableTransformation', exclude=True)

class GetCoordinateGraphQueryCoordinategraphTransformationsBaseCatchAll(GetCoordinateGraphQueryCoordinategraphTransformationsBase, BaseModel):
    """Catch all class for GetCoordinateGraphQueryCoordinategraphTransformationsBase"""
    typename: str = Field(alias='__typename', exclude=True)

class GetCoordinateGraphQueryCoordinategraph(BaseModel):
    """The connected component of the coordinate graph around one system: every coordinate system it relates to, and every top-level edge between them. Reachability is undirected -- an edge pointing *into* the system you started from (the edge into a physical space, say) relates to it just as much as one pointing out -- but every edge is returned in its true stored direction, so composing a path is still the client's job and still needs the inversions flagged"""
    typename: Literal['CoordinateGraph'] = Field(alias='__typename', default='CoordinateGraph', exclude=True)
    root: CoordinateSystem
    'The coordinate system the walk started from'
    systems: Tuple[CoordinateSystem, ...]
    'Every coordinate system reachable from the root, the root included, ordered by ID'
    transformations: Tuple[Union[Annotated[Union[GetCoordinateGraphQueryCoordinategraphTransformationsBaseAffineTransformation, GetCoordinateGraphQueryCoordinategraphTransformationsBaseBijectionTransformation, GetCoordinateGraphQueryCoordinategraphTransformationsBaseByDimensionTransformation, GetCoordinateGraphQueryCoordinategraphTransformationsBaseFieldTransformation, GetCoordinateGraphQueryCoordinategraphTransformationsBaseIdentityTransformation, GetCoordinateGraphQueryCoordinategraphTransformationsBaseMapAxisTransformation, GetCoordinateGraphQueryCoordinategraphTransformationsBaseRotationTransformation, GetCoordinateGraphQueryCoordinategraphTransformationsBaseScaleTransformation, GetCoordinateGraphQueryCoordinategraphTransformationsBaseSequenceTransformation, GetCoordinateGraphQueryCoordinategraphTransformationsBaseTranslationTransformation, GetCoordinateGraphQueryCoordinategraphTransformationsBaseUnmappableTransformation], Field(discriminator='typename')], GetCoordinateGraphQueryCoordinategraphTransformationsBaseCatchAll], ...]
    'Every top-level edge with both endpoints in `systems`, ordered by ID. The children of a SEQUENCE / BY_DIMENSION / BIJECTION wrapper are not listed here; they hang off their wrapper'
    model_config = ConfigDict(frozen=True)

class GetCoordinateGraphQuery(BaseModel):
    """No documentation found for this operation."""
    coordinate_graph: GetCoordinateGraphQueryCoordinategraph = Field(alias='coordinateGraph')
    "Walk the coordinate graph out from one system: every coordinate system it reaches and every top-level edge between them. Reachability is undirected (an edge pointing into the system relates to it as much as one pointing out), the edges keep their true direction, and nothing is composed -- what the list queries cannot answer is 'which edges relate to *this* one', because relatedness is transitive and a filter is not"

    class Arguments(BaseModel):
        """Arguments for GetCoordinateGraph """
        coordinate_system: ID = Field(alias='coordinateSystem')
        max_depth: Optional[int] = Field(alias='maxDepth', default=None)
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for GetCoordinateGraph """
        document = 'fragment Axis on Axis {\n  id\n  order\n  name\n  type\n  unit\n  longName\n  __typename\n}\n\nfragment TransformationChild on Transformation {\n  __typename\n  id\n  kind\n  inputAxes\n  outputAxes\n  ... on ScaleTransformation {\n    scale\n  }\n  ... on TranslationTransformation {\n    translation\n  }\n  ... on AffineTransformation {\n    affine\n  }\n  ... on RotationTransformation {\n    affine\n  }\n}\n\nfragment CoordinateSystem on CoordinateSystem {\n  id\n  name\n  epoch\n  axes {\n    ...Axis\n    __typename\n  }\n  __typename\n}\n\nfragment Transformation on Transformation {\n  id\n  kind\n  name\n  version\n  input {\n    ...CoordinateSystem\n    __typename\n  }\n  output {\n    ...CoordinateSystem\n    __typename\n  }\n  ... on ScaleTransformation {\n    scale\n  }\n  ... on TranslationTransformation {\n    translation\n  }\n  ... on AffineTransformation {\n    affine\n  }\n  ... on RotationTransformation {\n    affine\n  }\n  ... on MapAxisTransformation {\n    inputAxes\n    outputAxes\n  }\n  ... on FieldTransformation {\n    field {\n      ...CoordinateSystem\n    }\n  }\n  ... on SequenceTransformation {\n    sequenceChildren: transformations {\n      ...TransformationChild\n    }\n  }\n  ... on ByDimensionTransformation {\n    inputAxes\n    outputAxes\n    byDimensionChildren: transformations {\n      ...TransformationChild\n    }\n  }\n  ... on BijectionTransformation {\n    bijectionChildren: transformations {\n      ...TransformationChild\n    }\n  }\n  __typename\n}\n\nquery GetCoordinateGraph($coordinateSystem: ID!, $maxDepth: Int) {\n  coordinateGraph(coordinateSystem: $coordinateSystem, maxDepth: $maxDepth) {\n    root {\n      ...CoordinateSystem\n      __typename\n    }\n    systems {\n      ...CoordinateSystem\n      __typename\n    }\n    transformations {\n      ...Transformation\n      __typename\n    }\n    __typename\n  }\n}'

class GetCoordinateSystemQuery(BaseModel):
    """No documentation found for this operation."""
    coordinate_system: CoordinateSystem = Field(alias='coordinateSystem')
    'Get a single coordinate system by ID'

    class Arguments(BaseModel):
        """Arguments for GetCoordinateSystem """
        id: ID
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for GetCoordinateSystem """
        document = 'fragment Axis on Axis {\n  id\n  order\n  name\n  type\n  unit\n  longName\n  __typename\n}\n\nfragment CoordinateSystem on CoordinateSystem {\n  id\n  name\n  epoch\n  axes {\n    ...Axis\n    __typename\n  }\n  __typename\n}\n\nquery GetCoordinateSystem($id: ID!) {\n  coordinateSystem(id: $id) {\n    ...CoordinateSystem\n    __typename\n  }\n}'

class GetCoordinateSystemsQuery(BaseModel):
    """No documentation found for this operation."""
    coordinate_systems: Tuple[CoordinateSystem, ...] = Field(alias='coordinateSystems')
    'List coordinate systems (the nodes of the RFC-5 coordinate graph)'

    class Arguments(BaseModel):
        """Arguments for GetCoordinateSystems """
        filters: Optional[CoordinateSystemFilter] = Field(default=None)
        pagination: Optional[OffsetPaginationInput] = Field(default=None)
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for GetCoordinateSystems """
        document = 'fragment Axis on Axis {\n  id\n  order\n  name\n  type\n  unit\n  longName\n  __typename\n}\n\nfragment CoordinateSystem on CoordinateSystem {\n  id\n  name\n  epoch\n  axes {\n    ...Axis\n    __typename\n  }\n  __typename\n}\n\nquery GetCoordinateSystems($filters: CoordinateSystemFilter, $pagination: OffsetPaginationInput) {\n  coordinateSystems(filters: $filters, pagination: $pagination) {\n    ...CoordinateSystem\n    __typename\n  }\n}'

class SearchCoordinateSystemsQueryOptions(CoordinateSystemTrait, BaseModel):
    """A named coordinate space: a node in the transformation graph. Its axes are ordered, and that order is the order of the array's dimensions"""
    typename: Literal['CoordinateSystem'] = Field(alias='__typename', default='CoordinateSystem', exclude=True)
    value: ID
    label: str
    model_config = ConfigDict(frozen=True)

class SearchCoordinateSystemsQuery(BaseModel):
    """No documentation found for this operation."""
    options: Tuple[SearchCoordinateSystemsQueryOptions, ...]
    'List coordinate systems (the nodes of the RFC-5 coordinate graph)'

    class Arguments(BaseModel):
        """Arguments for SearchCoordinateSystems """
        search: Optional[str] = Field(default=None)
        values: Optional[List[ID]] = Field(default=None)
        limit: Optional[int] = Field(default=None)
        offset: Annotated[Optional[int], GraphQLDefault('0')] = Field(default=None)
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for SearchCoordinateSystems """
        document = 'query SearchCoordinateSystems($search: String, $values: [ID!], $limit: Int, $offset: Int = 0) {\n  options: coordinateSystems(\n    filters: {search: $search, ids: $values}\n    pagination: {limit: $limit, offset: $offset}\n  ) {\n    value: id\n    label: name\n    __typename\n  }\n}'

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
        offset: Annotated[Optional[int], GraphQLDefault('0')] = Field(default=None)
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
        offset: Annotated[Optional[int], GraphQLDefault('0')] = Field(default=None)
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
        document = 'fragment Era on Era {\n  id\n  begin\n  name\n  __typename\n}\n\nfragment ReferenceView on ReferenceView {\n  ...View\n  id\n  __typename\n}\n\nfragment View on View {\n  xMin\n  xMax\n  yMin\n  yMax\n  tMin\n  tMax\n  cMin\n  cMax\n  zMin\n  zMax\n  __typename\n}\n\nfragment AcquisitionView on AcquisitionView {\n  ...View\n  id\n  description\n  acquiredAt\n  operator {\n    sub\n    __typename\n  }\n  __typename\n}\n\nfragment AffineTransformationView on AffineTransformationView {\n  ...View\n  id\n  affineMatrix\n  stage {\n    id\n    name\n    __typename\n  }\n  __typename\n}\n\nfragment ChannelView on ChannelView {\n  ...View\n  id\n  emissionWavelength\n  excitationWavelength\n  __typename\n}\n\nfragment ContinousScanView on ContinousScanView {\n  ...View\n  id\n  direction\n  __typename\n}\n\nfragment DerivedView on DerivedView {\n  ...View\n  id\n  originImage {\n    id\n    name\n    __typename\n  }\n  __typename\n}\n\nfragment FileView on FileView {\n  ...View\n  id\n  seriesIdentifier\n  file {\n    id\n    name\n    __typename\n  }\n  __typename\n}\n\nfragment InstanceMaskView on InstanceMaskView {\n  ...View\n  id\n  referenceView {\n    ...ReferenceView\n    __typename\n  }\n  __typename\n}\n\nfragment MaskView on MaskView {\n  ...View\n  id\n  referenceView {\n    ...ReferenceView\n    __typename\n  }\n  __typename\n}\n\nfragment OpticsView on OpticsView {\n  ...View\n  id\n  objective {\n    id\n    name\n    serialNumber\n    __typename\n  }\n  camera {\n    id\n    name\n    serialNumber\n    __typename\n  }\n  instrument {\n    id\n    name\n    serialNumber\n    __typename\n  }\n  __typename\n}\n\nfragment RGBView on RGBView {\n  ...View\n  id\n  contexts {\n    id\n    name\n    __typename\n  }\n  name\n  image {\n    id\n    store {\n      ...ZarrStore\n      __typename\n    }\n    derivedScaleViews {\n      id\n      image {\n        id\n        store {\n          ...ZarrStore\n          __typename\n        }\n        __typename\n      }\n      scaleX\n      scaleY\n      scaleZ\n      scaleT\n      scaleC\n      __typename\n    }\n    __typename\n  }\n  colorMap\n  contrastLimitMin\n  contrastLimitMax\n  gamma\n  active\n  fullColour\n  baseColor\n  __typename\n}\n\nfragment ROIView on ROIView {\n  ...View\n  id\n  roi {\n    id\n    name\n    __typename\n  }\n  __typename\n}\n\nfragment TimepointView on TimepointView {\n  ...View\n  id\n  timeSinceStart\n  indexSinceStart\n  era {\n    ...Era\n    __typename\n  }\n  __typename\n}\n\nfragment WellPositionView on WellPositionView {\n  ...View\n  id\n  column\n  row\n  well {\n    id\n    rows\n    columns\n    name\n    __typename\n  }\n  __typename\n}\n\nfragment ZarrStore on ZarrStore {\n  id\n  key\n  bucket\n  path\n  __typename\n}\n\nfragment Image on Image {\n  id\n  name\n  store {\n    ...ZarrStore\n    __typename\n  }\n  views {\n    ...ChannelView\n    ...AffineTransformationView\n    ...TimepointView\n    ...OpticsView\n    ...AcquisitionView\n    ...RGBView\n    ...WellPositionView\n    ...DerivedView\n    ...ROIView\n    ...FileView\n    ...ContinousScanView\n    __typename\n  }\n  maskViews {\n    ...MaskView\n    __typename\n  }\n  instanceMaskViews {\n    ...InstanceMaskView\n    __typename\n  }\n  rgbContexts {\n    id\n    name\n    views {\n      ...RGBView\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nquery GetImage($id: ID!) {\n  image(id: $id) {\n    ...Image\n    __typename\n  }\n}'

class GetRandomImageQuery(BaseModel):
    """No documentation found for this operation."""
    random_image: Image = Field(alias='randomImage')
    'Get a random image of the current organization'

    class Arguments(BaseModel):
        """Arguments for GetRandomImage """
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for GetRandomImage """
        document = 'fragment Era on Era {\n  id\n  begin\n  name\n  __typename\n}\n\nfragment ReferenceView on ReferenceView {\n  ...View\n  id\n  __typename\n}\n\nfragment View on View {\n  xMin\n  xMax\n  yMin\n  yMax\n  tMin\n  tMax\n  cMin\n  cMax\n  zMin\n  zMax\n  __typename\n}\n\nfragment AcquisitionView on AcquisitionView {\n  ...View\n  id\n  description\n  acquiredAt\n  operator {\n    sub\n    __typename\n  }\n  __typename\n}\n\nfragment AffineTransformationView on AffineTransformationView {\n  ...View\n  id\n  affineMatrix\n  stage {\n    id\n    name\n    __typename\n  }\n  __typename\n}\n\nfragment ChannelView on ChannelView {\n  ...View\n  id\n  emissionWavelength\n  excitationWavelength\n  __typename\n}\n\nfragment ContinousScanView on ContinousScanView {\n  ...View\n  id\n  direction\n  __typename\n}\n\nfragment DerivedView on DerivedView {\n  ...View\n  id\n  originImage {\n    id\n    name\n    __typename\n  }\n  __typename\n}\n\nfragment FileView on FileView {\n  ...View\n  id\n  seriesIdentifier\n  file {\n    id\n    name\n    __typename\n  }\n  __typename\n}\n\nfragment InstanceMaskView on InstanceMaskView {\n  ...View\n  id\n  referenceView {\n    ...ReferenceView\n    __typename\n  }\n  __typename\n}\n\nfragment MaskView on MaskView {\n  ...View\n  id\n  referenceView {\n    ...ReferenceView\n    __typename\n  }\n  __typename\n}\n\nfragment OpticsView on OpticsView {\n  ...View\n  id\n  objective {\n    id\n    name\n    serialNumber\n    __typename\n  }\n  camera {\n    id\n    name\n    serialNumber\n    __typename\n  }\n  instrument {\n    id\n    name\n    serialNumber\n    __typename\n  }\n  __typename\n}\n\nfragment RGBView on RGBView {\n  ...View\n  id\n  contexts {\n    id\n    name\n    __typename\n  }\n  name\n  image {\n    id\n    store {\n      ...ZarrStore\n      __typename\n    }\n    derivedScaleViews {\n      id\n      image {\n        id\n        store {\n          ...ZarrStore\n          __typename\n        }\n        __typename\n      }\n      scaleX\n      scaleY\n      scaleZ\n      scaleT\n      scaleC\n      __typename\n    }\n    __typename\n  }\n  colorMap\n  contrastLimitMin\n  contrastLimitMax\n  gamma\n  active\n  fullColour\n  baseColor\n  __typename\n}\n\nfragment ROIView on ROIView {\n  ...View\n  id\n  roi {\n    id\n    name\n    __typename\n  }\n  __typename\n}\n\nfragment TimepointView on TimepointView {\n  ...View\n  id\n  timeSinceStart\n  indexSinceStart\n  era {\n    ...Era\n    __typename\n  }\n  __typename\n}\n\nfragment WellPositionView on WellPositionView {\n  ...View\n  id\n  column\n  row\n  well {\n    id\n    rows\n    columns\n    name\n    __typename\n  }\n  __typename\n}\n\nfragment ZarrStore on ZarrStore {\n  id\n  key\n  bucket\n  path\n  __typename\n}\n\nfragment Image on Image {\n  id\n  name\n  store {\n    ...ZarrStore\n    __typename\n  }\n  views {\n    ...ChannelView\n    ...AffineTransformationView\n    ...TimepointView\n    ...OpticsView\n    ...AcquisitionView\n    ...RGBView\n    ...WellPositionView\n    ...DerivedView\n    ...ROIView\n    ...FileView\n    ...ContinousScanView\n    __typename\n  }\n  maskViews {\n    ...MaskView\n    __typename\n  }\n  instanceMaskViews {\n    ...InstanceMaskView\n    __typename\n  }\n  rgbContexts {\n    id\n    name\n    views {\n      ...RGBView\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nquery GetRandomImage {\n  randomImage {\n    ...Image\n    __typename\n  }\n}'

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
        offset: Annotated[Optional[int], GraphQLDefault('0')] = Field(default=None)
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
        document = 'fragment Era on Era {\n  id\n  begin\n  name\n  __typename\n}\n\nfragment ReferenceView on ReferenceView {\n  ...View\n  id\n  __typename\n}\n\nfragment View on View {\n  xMin\n  xMax\n  yMin\n  yMax\n  tMin\n  tMax\n  cMin\n  cMax\n  zMin\n  zMax\n  __typename\n}\n\nfragment AcquisitionView on AcquisitionView {\n  ...View\n  id\n  description\n  acquiredAt\n  operator {\n    sub\n    __typename\n  }\n  __typename\n}\n\nfragment AffineTransformationView on AffineTransformationView {\n  ...View\n  id\n  affineMatrix\n  stage {\n    id\n    name\n    __typename\n  }\n  __typename\n}\n\nfragment ChannelView on ChannelView {\n  ...View\n  id\n  emissionWavelength\n  excitationWavelength\n  __typename\n}\n\nfragment ContinousScanView on ContinousScanView {\n  ...View\n  id\n  direction\n  __typename\n}\n\nfragment DerivedView on DerivedView {\n  ...View\n  id\n  originImage {\n    id\n    name\n    __typename\n  }\n  __typename\n}\n\nfragment FileView on FileView {\n  ...View\n  id\n  seriesIdentifier\n  file {\n    id\n    name\n    __typename\n  }\n  __typename\n}\n\nfragment InstanceMaskView on InstanceMaskView {\n  ...View\n  id\n  referenceView {\n    ...ReferenceView\n    __typename\n  }\n  __typename\n}\n\nfragment MaskView on MaskView {\n  ...View\n  id\n  referenceView {\n    ...ReferenceView\n    __typename\n  }\n  __typename\n}\n\nfragment OpticsView on OpticsView {\n  ...View\n  id\n  objective {\n    id\n    name\n    serialNumber\n    __typename\n  }\n  camera {\n    id\n    name\n    serialNumber\n    __typename\n  }\n  instrument {\n    id\n    name\n    serialNumber\n    __typename\n  }\n  __typename\n}\n\nfragment RGBView on RGBView {\n  ...View\n  id\n  contexts {\n    id\n    name\n    __typename\n  }\n  name\n  image {\n    id\n    store {\n      ...ZarrStore\n      __typename\n    }\n    derivedScaleViews {\n      id\n      image {\n        id\n        store {\n          ...ZarrStore\n          __typename\n        }\n        __typename\n      }\n      scaleX\n      scaleY\n      scaleZ\n      scaleT\n      scaleC\n      __typename\n    }\n    __typename\n  }\n  colorMap\n  contrastLimitMin\n  contrastLimitMax\n  gamma\n  active\n  fullColour\n  baseColor\n  __typename\n}\n\nfragment ROIView on ROIView {\n  ...View\n  id\n  roi {\n    id\n    name\n    __typename\n  }\n  __typename\n}\n\nfragment TimepointView on TimepointView {\n  ...View\n  id\n  timeSinceStart\n  indexSinceStart\n  era {\n    ...Era\n    __typename\n  }\n  __typename\n}\n\nfragment WellPositionView on WellPositionView {\n  ...View\n  id\n  column\n  row\n  well {\n    id\n    rows\n    columns\n    name\n    __typename\n  }\n  __typename\n}\n\nfragment ZarrStore on ZarrStore {\n  id\n  key\n  bucket\n  path\n  __typename\n}\n\nfragment Image on Image {\n  id\n  name\n  store {\n    ...ZarrStore\n    __typename\n  }\n  views {\n    ...ChannelView\n    ...AffineTransformationView\n    ...TimepointView\n    ...OpticsView\n    ...AcquisitionView\n    ...RGBView\n    ...WellPositionView\n    ...DerivedView\n    ...ROIView\n    ...FileView\n    ...ContinousScanView\n    __typename\n  }\n  maskViews {\n    ...MaskView\n    __typename\n  }\n  instanceMaskViews {\n    ...InstanceMaskView\n    __typename\n  }\n  rgbContexts {\n    id\n    name\n    views {\n      ...RGBView\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nquery Images($filter: ImageFilter, $pagination: OffsetPaginationInput) {\n  images(filters: $filter, pagination: $pagination) {\n    ...Image\n    __typename\n  }\n}'

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
    """A view anchoring an image region in real time: it places the region within an era (a named time epoch on the microscope) at a time offset or frame index since its start."""
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
        document = 'fragment Axis on Axis {\n  id\n  order\n  name\n  type\n  unit\n  longName\n  __typename\n}\n\nfragment CoordinateSystem on CoordinateSystem {\n  id\n  name\n  epoch\n  axes {\n    ...Axis\n    __typename\n  }\n  __typename\n}\n\nfragment Slice on Slice {\n  axis\n  start\n  stop\n  step\n  __typename\n}\n\nfragment ZarrStore on ZarrStore {\n  id\n  key\n  bucket\n  path\n  __typename\n}\n\nfragment Lens on Lens {\n  id\n  dataset {\n    id\n    axisNames\n    dataArrays {\n      id\n      level\n      store {\n        ...ZarrStore\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  shape\n  axisNames\n  coordinateSystem {\n    ...CoordinateSystem\n    __typename\n  }\n  renderAxes {\n    x\n    y\n    z\n    t\n    intensity\n    __typename\n  }\n  slices {\n    ...Slice\n    __typename\n  }\n  __typename\n}\n\nquery GetLens($id: ID!) {\n  lens(id: $id) {\n    ...Lens\n    __typename\n  }\n}'

class GetMeshCollectionQuery(BaseModel):
    """No documentation found for this operation."""
    mesh_collection: MeshCollection = Field(alias='meshCollection')
    'Get a single mesh collection by ID'

    class Arguments(BaseModel):
        """Arguments for GetMeshCollection """
        id: ID
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for GetMeshCollection """
        document = 'fragment Axis on Axis {\n  id\n  order\n  name\n  type\n  unit\n  longName\n  __typename\n}\n\nfragment TransformationChild on Transformation {\n  __typename\n  id\n  kind\n  inputAxes\n  outputAxes\n  ... on ScaleTransformation {\n    scale\n  }\n  ... on TranslationTransformation {\n    translation\n  }\n  ... on AffineTransformation {\n    affine\n  }\n  ... on RotationTransformation {\n    affine\n  }\n}\n\nfragment CoordinateSystem on CoordinateSystem {\n  id\n  name\n  epoch\n  axes {\n    ...Axis\n    __typename\n  }\n  __typename\n}\n\nfragment ParquetStore on ParquetStore {\n  id\n  key\n  bucket\n  path\n  __typename\n}\n\nfragment Transformation on Transformation {\n  id\n  kind\n  name\n  version\n  input {\n    ...CoordinateSystem\n    __typename\n  }\n  output {\n    ...CoordinateSystem\n    __typename\n  }\n  ... on ScaleTransformation {\n    scale\n  }\n  ... on TranslationTransformation {\n    translation\n  }\n  ... on AffineTransformation {\n    affine\n  }\n  ... on RotationTransformation {\n    affine\n  }\n  ... on MapAxisTransformation {\n    inputAxes\n    outputAxes\n  }\n  ... on FieldTransformation {\n    field {\n      ...CoordinateSystem\n    }\n  }\n  ... on SequenceTransformation {\n    sequenceChildren: transformations {\n      ...TransformationChild\n    }\n  }\n  ... on ByDimensionTransformation {\n    inputAxes\n    outputAxes\n    byDimensionChildren: transformations {\n      ...TransformationChild\n    }\n  }\n  ... on BijectionTransformation {\n    bijectionChildren: transformations {\n      ...TransformationChild\n    }\n  }\n  __typename\n}\n\nfragment MeshCollection on MeshCollection {\n  id\n  version\n  specVersion\n  grid\n  encoding\n  coordinateSystem {\n    ...CoordinateSystem\n    __typename\n  }\n  catalog {\n    ...ParquetStore\n    __typename\n  }\n  geometry {\n    ...ParquetStore\n    __typename\n  }\n  derivedFrom {\n    ...Transformation\n    __typename\n  }\n  __typename\n}\n\nquery GetMeshCollection($id: ID!) {\n  meshCollection(id: $id) {\n    ...MeshCollection\n    __typename\n  }\n}'

class GetMeshCollectionsQuery(BaseModel):
    """No documentation found for this operation."""
    mesh_collections: Tuple[MeshCollection, ...] = Field(alias='meshCollections')
    'List mesh collections (immutable, versioned Parquet-backed mesh sets, each in a coordinate system of its own)'

    class Arguments(BaseModel):
        """Arguments for GetMeshCollections """
        filters: Optional[MeshCollectionFilter] = Field(default=None)
        pagination: Optional[OffsetPaginationInput] = Field(default=None)
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for GetMeshCollections """
        document = 'fragment Axis on Axis {\n  id\n  order\n  name\n  type\n  unit\n  longName\n  __typename\n}\n\nfragment TransformationChild on Transformation {\n  __typename\n  id\n  kind\n  inputAxes\n  outputAxes\n  ... on ScaleTransformation {\n    scale\n  }\n  ... on TranslationTransformation {\n    translation\n  }\n  ... on AffineTransformation {\n    affine\n  }\n  ... on RotationTransformation {\n    affine\n  }\n}\n\nfragment CoordinateSystem on CoordinateSystem {\n  id\n  name\n  epoch\n  axes {\n    ...Axis\n    __typename\n  }\n  __typename\n}\n\nfragment ParquetStore on ParquetStore {\n  id\n  key\n  bucket\n  path\n  __typename\n}\n\nfragment Transformation on Transformation {\n  id\n  kind\n  name\n  version\n  input {\n    ...CoordinateSystem\n    __typename\n  }\n  output {\n    ...CoordinateSystem\n    __typename\n  }\n  ... on ScaleTransformation {\n    scale\n  }\n  ... on TranslationTransformation {\n    translation\n  }\n  ... on AffineTransformation {\n    affine\n  }\n  ... on RotationTransformation {\n    affine\n  }\n  ... on MapAxisTransformation {\n    inputAxes\n    outputAxes\n  }\n  ... on FieldTransformation {\n    field {\n      ...CoordinateSystem\n    }\n  }\n  ... on SequenceTransformation {\n    sequenceChildren: transformations {\n      ...TransformationChild\n    }\n  }\n  ... on ByDimensionTransformation {\n    inputAxes\n    outputAxes\n    byDimensionChildren: transformations {\n      ...TransformationChild\n    }\n  }\n  ... on BijectionTransformation {\n    bijectionChildren: transformations {\n      ...TransformationChild\n    }\n  }\n  __typename\n}\n\nfragment MeshCollection on MeshCollection {\n  id\n  version\n  specVersion\n  grid\n  encoding\n  coordinateSystem {\n    ...CoordinateSystem\n    __typename\n  }\n  catalog {\n    ...ParquetStore\n    __typename\n  }\n  geometry {\n    ...ParquetStore\n    __typename\n  }\n  derivedFrom {\n    ...Transformation\n    __typename\n  }\n  __typename\n}\n\nquery GetMeshCollections($filters: MeshCollectionFilter, $pagination: OffsetPaginationInput) {\n  meshCollections(filters: $filters, pagination: $pagination) {\n    ...MeshCollection\n    __typename\n  }\n}'

class SearchMeshCollectionsQueryOptions(BaseModel):
    """An immutable, versioned collection of meshes, backed by Parquet stores. Ask the catalog store for an access grant and query the Parquet directly (e.g. with DuckDB) rather than paginating meshes through GraphQL"""
    typename: Literal['MeshCollection'] = Field(alias='__typename', default='MeshCollection', exclude=True)
    value: ID
    label: str
    model_config = ConfigDict(frozen=True)

class SearchMeshCollectionsQuery(BaseModel):
    """No documentation found for this operation."""
    options: Tuple[SearchMeshCollectionsQueryOptions, ...]
    'List mesh collections (immutable, versioned Parquet-backed mesh sets, each in a coordinate system of its own)'

    class Arguments(BaseModel):
        """Arguments for SearchMeshCollections """
        search: Optional[str] = Field(default=None)
        values: Optional[List[ID]] = Field(default=None)
        limit: Optional[int] = Field(default=None)
        offset: Annotated[Optional[int], GraphQLDefault('0')] = Field(default=None)
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for SearchMeshCollections """
        document = 'query SearchMeshCollections($search: String, $values: [ID!], $limit: Int, $offset: Int = 0) {\n  options: meshCollections(\n    filters: {version: {iContains: $search}, ids: $values}\n    pagination: {limit: $limit, offset: $offset}\n  ) {\n    value: id\n    label: version\n    __typename\n  }\n}'

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
        offset: Annotated[Optional[int], GraphQLDefault('0')] = Field(default=None)
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
        document = 'fragment Axis on Axis {\n  id\n  order\n  name\n  type\n  unit\n  longName\n  __typename\n}\n\nfragment CoordinateSystem on CoordinateSystem {\n  id\n  name\n  epoch\n  axes {\n    ...Axis\n    __typename\n  }\n  __typename\n}\n\nfragment Scene on Scene {\n  name\n  id\n  preferredView\n  backgroundColor\n  worldCoordinateSystem {\n    ...CoordinateSystem\n    __typename\n  }\n  __typename\n}\n\nquery GetScene($id: ID!) {\n  scene(id: $id) {\n    ...Scene\n    __typename\n  }\n}'

class SearchScenesQueryOptions(SceneTrait, BaseModel):
    """A composition of layers over a shared world coordinate system. The scene carries no units of its own -- they are per-axis, on the axes of its world system"""
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
        offset: Annotated[Optional[int], GraphQLDefault('0')] = Field(default=None)
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for SearchScenes """
        document = 'query SearchScenes($search: String, $values: [ID!], $limit: Int, $offset: Int = 0) {\n  options: scenes(\n    filters: {search: $search, ids: $values}\n    pagination: {limit: $limit, offset: $offset}\n  ) {\n    value: id\n    label: name\n    __typename\n  }\n}'

class GetSceneSnapshotQuery(BaseModel):
    """No documentation found for this operation."""
    scene_snapshot: SceneSnapshot = Field(alias='sceneSnapshot')
    'Get a single scene snapshot by ID'

    class Arguments(BaseModel):
        """Arguments for GetSceneSnapshot """
        id: ID
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for GetSceneSnapshot """
        document = 'fragment Axis on Axis {\n  id\n  order\n  name\n  type\n  unit\n  longName\n  __typename\n}\n\nfragment CoordinateSystem on CoordinateSystem {\n  id\n  name\n  epoch\n  axes {\n    ...Axis\n    __typename\n  }\n  __typename\n}\n\nfragment MediaStore on MediaStore {\n  id\n  key\n  bucket\n  path\n  __typename\n}\n\nfragment Scene on Scene {\n  name\n  id\n  preferredView\n  backgroundColor\n  worldCoordinateSystem {\n    ...CoordinateSystem\n    __typename\n  }\n  __typename\n}\n\nfragment SceneSnapshot on SceneSnapshot {\n  id\n  name\n  majorColor\n  scene {\n    ...Scene\n    __typename\n  }\n  store {\n    ...MediaStore\n    __typename\n  }\n  __typename\n}\n\nquery GetSceneSnapshot($id: ID!) {\n  sceneSnapshot(id: $id) {\n    ...SceneSnapshot\n    __typename\n  }\n}'

class GetSceneSnapshotsQuery(BaseModel):
    """No documentation found for this operation."""
    scene_snapshots: Tuple[SceneSnapshot, ...] = Field(alias='sceneSnapshots')
    'List scene snapshots (pre-rendered pictures of a composition, for previewing it without compositing the layers)'

    class Arguments(BaseModel):
        """Arguments for GetSceneSnapshots """
        filters: Optional[SceneSnapshotFilter] = Field(default=None)
        pagination: Optional[OffsetPaginationInput] = Field(default=None)
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for GetSceneSnapshots """
        document = 'fragment Axis on Axis {\n  id\n  order\n  name\n  type\n  unit\n  longName\n  __typename\n}\n\nfragment CoordinateSystem on CoordinateSystem {\n  id\n  name\n  epoch\n  axes {\n    ...Axis\n    __typename\n  }\n  __typename\n}\n\nfragment MediaStore on MediaStore {\n  id\n  key\n  bucket\n  path\n  __typename\n}\n\nfragment Scene on Scene {\n  name\n  id\n  preferredView\n  backgroundColor\n  worldCoordinateSystem {\n    ...CoordinateSystem\n    __typename\n  }\n  __typename\n}\n\nfragment SceneSnapshot on SceneSnapshot {\n  id\n  name\n  majorColor\n  scene {\n    ...Scene\n    __typename\n  }\n  store {\n    ...MediaStore\n    __typename\n  }\n  __typename\n}\n\nquery GetSceneSnapshots($filters: SceneSnapshotFilter, $pagination: OffsetPaginationInput) {\n  sceneSnapshots(filters: $filters, pagination: $pagination) {\n    ...SceneSnapshot\n    __typename\n  }\n}'

class SearchSceneSnapshotsQueryOptions(BaseModel):
    """A pre-rendered picture of a composition: every layer of the scene, blended. Clients use snapshots to preview without compositing the layers themselves. A picture of the scene, not of any one dataset in it -- though `ADataset.latestSnapshot` will offer one of these where the scene's only anchored dataset is that dataset, since then the picture shows it and nothing else"""
    typename: Literal['SceneSnapshot'] = Field(alias='__typename', default='SceneSnapshot', exclude=True)
    value: ID
    label: str
    model_config = ConfigDict(frozen=True)

class SearchSceneSnapshotsQuery(BaseModel):
    """No documentation found for this operation."""
    options: Tuple[SearchSceneSnapshotsQueryOptions, ...]
    'List scene snapshots (pre-rendered pictures of a composition, for previewing it without compositing the layers)'

    class Arguments(BaseModel):
        """Arguments for SearchSceneSnapshots """
        search: Optional[str] = Field(default=None)
        values: Optional[List[ID]] = Field(default=None)
        limit: Optional[int] = Field(default=None)
        offset: Annotated[Optional[int], GraphQLDefault('0')] = Field(default=None)
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for SearchSceneSnapshots """
        document = 'query SearchSceneSnapshots($search: String, $values: [ID!], $limit: Int, $offset: Int = 0) {\n  options: sceneSnapshots(\n    filters: {search: $search, ids: $values}\n    pagination: {limit: $limit, offset: $offset}\n  ) {\n    value: id\n    label: name\n    __typename\n  }\n}'

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
        offset: Annotated[Optional[int], GraphQLDefault('0')] = Field(default=None)
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
        offset: Annotated[Optional[int], GraphQLDefault('0')] = Field(default=None)
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
        offset: Annotated[Optional[int], GraphQLDefault('0')] = Field(default=None)
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
        offset: Annotated[Optional[int], GraphQLDefault('0')] = Field(default=None)
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for SearchTableCells """
        document = 'query SearchTableCells($search: String, $values: [ID!], $table: ID!, $limit: Int, $offset: Int = 0) {\n  options: tableCells(\n    table: $table\n    filters: {search: $search, ids: $values}\n    pagination: {limit: $limit, offset: $offset}\n  ) {\n    value: id\n    label: name\n    __typename\n  }\n}'

class GetTableDatasetQuery(BaseModel):
    """No documentation found for this operation."""
    table_dataset: TableDataset = Field(alias='tableDataset')
    'Get a single table dataset by ID'

    class Arguments(BaseModel):
        """Arguments for GetTableDataset """
        id: ID
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for GetTableDataset """
        document = 'fragment Axis on Axis {\n  id\n  order\n  name\n  type\n  unit\n  longName\n  __typename\n}\n\nfragment TransformationChild on Transformation {\n  __typename\n  id\n  kind\n  inputAxes\n  outputAxes\n  ... on ScaleTransformation {\n    scale\n  }\n  ... on TranslationTransformation {\n    translation\n  }\n  ... on AffineTransformation {\n    affine\n  }\n  ... on RotationTransformation {\n    affine\n  }\n}\n\nfragment CoordinateSystem on CoordinateSystem {\n  id\n  name\n  epoch\n  axes {\n    ...Axis\n    __typename\n  }\n  __typename\n}\n\nfragment ParquetStore on ParquetStore {\n  id\n  key\n  bucket\n  path\n  __typename\n}\n\nfragment Transformation on Transformation {\n  id\n  kind\n  name\n  version\n  input {\n    ...CoordinateSystem\n    __typename\n  }\n  output {\n    ...CoordinateSystem\n    __typename\n  }\n  ... on ScaleTransformation {\n    scale\n  }\n  ... on TranslationTransformation {\n    translation\n  }\n  ... on AffineTransformation {\n    affine\n  }\n  ... on RotationTransformation {\n    affine\n  }\n  ... on MapAxisTransformation {\n    inputAxes\n    outputAxes\n  }\n  ... on FieldTransformation {\n    field {\n      ...CoordinateSystem\n    }\n  }\n  ... on SequenceTransformation {\n    sequenceChildren: transformations {\n      ...TransformationChild\n    }\n  }\n  ... on ByDimensionTransformation {\n    inputAxes\n    outputAxes\n    byDimensionChildren: transformations {\n      ...TransformationChild\n    }\n  }\n  ... on BijectionTransformation {\n    bijectionChildren: transformations {\n      ...TransformationChild\n    }\n  }\n  __typename\n}\n\nfragment TableDataset on TableDataset {\n  id\n  name\n  description\n  store {\n    ...ParquetStore\n    __typename\n  }\n  columns {\n    id\n    order\n    name\n    dtype\n    role\n    axisType\n    unit\n    longName\n    __typename\n  }\n  coordinateSystem {\n    ...CoordinateSystem\n    __typename\n  }\n  derivedFrom {\n    ...Transformation\n    __typename\n  }\n  axisNames\n  provenanceMetadata\n  __typename\n}\n\nquery GetTableDataset($id: ID!) {\n  tableDataset(id: $id) {\n    ...TableDataset\n    __typename\n  }\n}'

class GetTableDatasetsQuery(BaseModel):
    """No documentation found for this operation."""
    table_datasets: Tuple[TableDataset, ...] = Field(alias='tableDatasets')
    'List table datasets (Parquet-backed tables of scientific records: measurements, localizations, expression levels)'

    class Arguments(BaseModel):
        """Arguments for GetTableDatasets """
        filters: Optional[TableDatasetFilter] = Field(default=None)
        pagination: Optional[OffsetPaginationInput] = Field(default=None)
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for GetTableDatasets """
        document = 'fragment Axis on Axis {\n  id\n  order\n  name\n  type\n  unit\n  longName\n  __typename\n}\n\nfragment TransformationChild on Transformation {\n  __typename\n  id\n  kind\n  inputAxes\n  outputAxes\n  ... on ScaleTransformation {\n    scale\n  }\n  ... on TranslationTransformation {\n    translation\n  }\n  ... on AffineTransformation {\n    affine\n  }\n  ... on RotationTransformation {\n    affine\n  }\n}\n\nfragment CoordinateSystem on CoordinateSystem {\n  id\n  name\n  epoch\n  axes {\n    ...Axis\n    __typename\n  }\n  __typename\n}\n\nfragment ParquetStore on ParquetStore {\n  id\n  key\n  bucket\n  path\n  __typename\n}\n\nfragment Transformation on Transformation {\n  id\n  kind\n  name\n  version\n  input {\n    ...CoordinateSystem\n    __typename\n  }\n  output {\n    ...CoordinateSystem\n    __typename\n  }\n  ... on ScaleTransformation {\n    scale\n  }\n  ... on TranslationTransformation {\n    translation\n  }\n  ... on AffineTransformation {\n    affine\n  }\n  ... on RotationTransformation {\n    affine\n  }\n  ... on MapAxisTransformation {\n    inputAxes\n    outputAxes\n  }\n  ... on FieldTransformation {\n    field {\n      ...CoordinateSystem\n    }\n  }\n  ... on SequenceTransformation {\n    sequenceChildren: transformations {\n      ...TransformationChild\n    }\n  }\n  ... on ByDimensionTransformation {\n    inputAxes\n    outputAxes\n    byDimensionChildren: transformations {\n      ...TransformationChild\n    }\n  }\n  ... on BijectionTransformation {\n    bijectionChildren: transformations {\n      ...TransformationChild\n    }\n  }\n  __typename\n}\n\nfragment TableDataset on TableDataset {\n  id\n  name\n  description\n  store {\n    ...ParquetStore\n    __typename\n  }\n  columns {\n    id\n    order\n    name\n    dtype\n    role\n    axisType\n    unit\n    longName\n    __typename\n  }\n  coordinateSystem {\n    ...CoordinateSystem\n    __typename\n  }\n  derivedFrom {\n    ...Transformation\n    __typename\n  }\n  axisNames\n  provenanceMetadata\n  __typename\n}\n\nquery GetTableDatasets($filters: TableDatasetFilter, $pagination: OffsetPaginationInput) {\n  tableDatasets(filters: $filters, pagination: $pagination) {\n    ...TableDataset\n    __typename\n  }\n}'

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
        offset: Annotated[Optional[int], GraphQLDefault('0')] = Field(default=None)
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for SearchTableRows """
        document = 'query SearchTableRows($search: String, $values: [ID!], $table: ID!, $limit: Int, $offset: Int = 0) {\n  options: tableRows(\n    table: $table\n    filters: {search: $search, ids: $values}\n    pagination: {limit: $limit, offset: $offset}\n  ) {\n    value: id\n    label: name\n    __typename\n  }\n}'

class GetTransformationQueryTransformationBase(BaseModel):
    """A directed edge of the coordinate graph, mapping `input` to `output`. Direction is always forward. The concrete kind (Scale, Translation, Affine, Sequence, ...) carries the parameters"""
    model_config = ConfigDict(frozen=True)

class GetTransformationQueryTransformationBaseAffineTransformation(TransformationAffineTransformation, GetTransformationQueryTransformationBase, TransformationTrait, BaseModel):
    """A general affine map, given as an M x (N+1) matrix with rows outermost"""
    typename: Literal['AffineTransformation'] = Field(alias='__typename', default='AffineTransformation', exclude=True)

class GetTransformationQueryTransformationBaseBijectionTransformation(TransformationBijectionTransformation, GetTransformationQueryTransformationBase, TransformationTrait, BaseModel):
    """A pair of child transformations giving an explicit forward and inverse map"""
    typename: Literal['BijectionTransformation'] = Field(alias='__typename', default='BijectionTransformation', exclude=True)

class GetTransformationQueryTransformationBaseByDimensionTransformation(TransformationByDimensionTransformation, GetTransformationQueryTransformationBase, TransformationTrait, BaseModel):
    """A composition of child transformations, each acting on a named subset of the axes"""
    typename: Literal['ByDimensionTransformation'] = Field(alias='__typename', default='ByDimensionTransformation', exclude=True)

class GetTransformationQueryTransformationBaseFieldTransformation(TransformationFieldTransformation, GetTransformationQueryTransformationBase, TransformationTrait, BaseModel):
    """A non-affine map given by the values of an array rather than by a formula. The array is a `field`: a node of this graph, not a payload on this edge, so it keeps its own lineage and its axes say what its numbers mean. It has no closed-form inverse, so a placement path never walks it backwards"""
    typename: Literal['FieldTransformation'] = Field(alias='__typename', default='FieldTransformation', exclude=True)

class GetTransformationQueryTransformationBaseIdentityTransformation(TransformationIdentityTransformation, GetTransformationQueryTransformationBase, TransformationTrait, BaseModel):
    """The identity map: input and output coordinates are the same"""
    typename: Literal['IdentityTransformation'] = Field(alias='__typename', default='IdentityTransformation', exclude=True)

class GetTransformationQueryTransformationBaseMapAxisTransformation(TransformationMapAxisTransformation, GetTransformationQueryTransformationBase, TransformationTrait, BaseModel):
    """A permutation of axes, mapping each input axis to an output axis by name"""
    typename: Literal['MapAxisTransformation'] = Field(alias='__typename', default='MapAxisTransformation', exclude=True)

class GetTransformationQueryTransformationBaseRotationTransformation(TransformationRotationTransformation, GetTransformationQueryTransformationBase, TransformationTrait, BaseModel):
    """A rotation, given as an orthonormal matrix"""
    typename: Literal['RotationTransformation'] = Field(alias='__typename', default='RotationTransformation', exclude=True)

class GetTransformationQueryTransformationBaseScaleTransformation(TransformationScaleTransformation, GetTransformationQueryTransformationBase, TransformationTrait, BaseModel):
    """A per-axis multiplication, with one entry per input axis"""
    typename: Literal['ScaleTransformation'] = Field(alias='__typename', default='ScaleTransformation', exclude=True)

class GetTransformationQueryTransformationBaseSequenceTransformation(TransformationSequenceTransformation, GetTransformationQueryTransformationBase, TransformationTrait, BaseModel):
    """An ordered composition of child transformations, applied first to last"""
    typename: Literal['SequenceTransformation'] = Field(alias='__typename', default='SequenceTransformation', exclude=True)

class GetTransformationQueryTransformationBaseTranslationTransformation(TransformationTranslationTransformation, GetTransformationQueryTransformationBase, TransformationTrait, BaseModel):
    """A per-axis offset, with one entry per input axis"""
    typename: Literal['TranslationTransformation'] = Field(alias='__typename', default='TranslationTransformation', exclude=True)

class GetTransformationQueryTransformationBaseUnmappableTransformation(TransformationUnmappableTransformation, GetTransformationQueryTransformationBase, TransformationTrait, BaseModel):
    """A declared NON-correspondence: the two systems are related -- one was computed from the other -- and no point of either maps to a point of the other. It has no parameters, no rank and no matrix, and no placement search will walk it, in either direction. This is what a per-object measurement table's relation to the image it was measured from looks like"""
    typename: Literal['UnmappableTransformation'] = Field(alias='__typename', default='UnmappableTransformation', exclude=True)

class GetTransformationQueryTransformationBaseCatchAll(GetTransformationQueryTransformationBase, BaseModel):
    """Catch all class for GetTransformationQueryTransformationBase"""
    typename: str = Field(alias='__typename', exclude=True)

class GetTransformationQuery(BaseModel):
    """No documentation found for this operation."""
    transformation: Union[Annotated[Union[GetTransformationQueryTransformationBaseAffineTransformation, GetTransformationQueryTransformationBaseBijectionTransformation, GetTransformationQueryTransformationBaseByDimensionTransformation, GetTransformationQueryTransformationBaseFieldTransformation, GetTransformationQueryTransformationBaseIdentityTransformation, GetTransformationQueryTransformationBaseMapAxisTransformation, GetTransformationQueryTransformationBaseRotationTransformation, GetTransformationQueryTransformationBaseScaleTransformation, GetTransformationQueryTransformationBaseSequenceTransformation, GetTransformationQueryTransformationBaseTranslationTransformation, GetTransformationQueryTransformationBaseUnmappableTransformation], Field(discriminator='typename')], GetTransformationQueryTransformationBaseCatchAll]
    'Get a single transformation by ID'

    class Arguments(BaseModel):
        """Arguments for GetTransformation """
        id: ID
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for GetTransformation """
        document = 'fragment Axis on Axis {\n  id\n  order\n  name\n  type\n  unit\n  longName\n  __typename\n}\n\nfragment CoordinateSystem on CoordinateSystem {\n  id\n  name\n  epoch\n  axes {\n    ...Axis\n    __typename\n  }\n  __typename\n}\n\nfragment TransformationChild on Transformation {\n  __typename\n  id\n  kind\n  inputAxes\n  outputAxes\n  ... on ScaleTransformation {\n    scale\n  }\n  ... on TranslationTransformation {\n    translation\n  }\n  ... on AffineTransformation {\n    affine\n  }\n  ... on RotationTransformation {\n    affine\n  }\n}\n\nfragment Transformation on Transformation {\n  id\n  kind\n  name\n  version\n  input {\n    ...CoordinateSystem\n    __typename\n  }\n  output {\n    ...CoordinateSystem\n    __typename\n  }\n  ... on ScaleTransformation {\n    scale\n  }\n  ... on TranslationTransformation {\n    translation\n  }\n  ... on AffineTransformation {\n    affine\n  }\n  ... on RotationTransformation {\n    affine\n  }\n  ... on MapAxisTransformation {\n    inputAxes\n    outputAxes\n  }\n  ... on FieldTransformation {\n    field {\n      ...CoordinateSystem\n    }\n  }\n  ... on SequenceTransformation {\n    sequenceChildren: transformations {\n      ...TransformationChild\n    }\n  }\n  ... on ByDimensionTransformation {\n    inputAxes\n    outputAxes\n    byDimensionChildren: transformations {\n      ...TransformationChild\n    }\n  }\n  ... on BijectionTransformation {\n    bijectionChildren: transformations {\n      ...TransformationChild\n    }\n  }\n  __typename\n}\n\nquery GetTransformation($id: ID!) {\n  transformation(id: $id) {\n    ...Transformation\n    __typename\n  }\n}'

class GetTransformationsQueryTransformationsBase(BaseModel):
    """A directed edge of the coordinate graph, mapping `input` to `output`. Direction is always forward. The concrete kind (Scale, Translation, Affine, Sequence, ...) carries the parameters"""
    model_config = ConfigDict(frozen=True)

class GetTransformationsQueryTransformationsBaseAffineTransformation(TransformationAffineTransformation, GetTransformationsQueryTransformationsBase, TransformationTrait, BaseModel):
    """A general affine map, given as an M x (N+1) matrix with rows outermost"""
    typename: Literal['AffineTransformation'] = Field(alias='__typename', default='AffineTransformation', exclude=True)

class GetTransformationsQueryTransformationsBaseBijectionTransformation(TransformationBijectionTransformation, GetTransformationsQueryTransformationsBase, TransformationTrait, BaseModel):
    """A pair of child transformations giving an explicit forward and inverse map"""
    typename: Literal['BijectionTransformation'] = Field(alias='__typename', default='BijectionTransformation', exclude=True)

class GetTransformationsQueryTransformationsBaseByDimensionTransformation(TransformationByDimensionTransformation, GetTransformationsQueryTransformationsBase, TransformationTrait, BaseModel):
    """A composition of child transformations, each acting on a named subset of the axes"""
    typename: Literal['ByDimensionTransformation'] = Field(alias='__typename', default='ByDimensionTransformation', exclude=True)

class GetTransformationsQueryTransformationsBaseFieldTransformation(TransformationFieldTransformation, GetTransformationsQueryTransformationsBase, TransformationTrait, BaseModel):
    """A non-affine map given by the values of an array rather than by a formula. The array is a `field`: a node of this graph, not a payload on this edge, so it keeps its own lineage and its axes say what its numbers mean. It has no closed-form inverse, so a placement path never walks it backwards"""
    typename: Literal['FieldTransformation'] = Field(alias='__typename', default='FieldTransformation', exclude=True)

class GetTransformationsQueryTransformationsBaseIdentityTransformation(TransformationIdentityTransformation, GetTransformationsQueryTransformationsBase, TransformationTrait, BaseModel):
    """The identity map: input and output coordinates are the same"""
    typename: Literal['IdentityTransformation'] = Field(alias='__typename', default='IdentityTransformation', exclude=True)

class GetTransformationsQueryTransformationsBaseMapAxisTransformation(TransformationMapAxisTransformation, GetTransformationsQueryTransformationsBase, TransformationTrait, BaseModel):
    """A permutation of axes, mapping each input axis to an output axis by name"""
    typename: Literal['MapAxisTransformation'] = Field(alias='__typename', default='MapAxisTransformation', exclude=True)

class GetTransformationsQueryTransformationsBaseRotationTransformation(TransformationRotationTransformation, GetTransformationsQueryTransformationsBase, TransformationTrait, BaseModel):
    """A rotation, given as an orthonormal matrix"""
    typename: Literal['RotationTransformation'] = Field(alias='__typename', default='RotationTransformation', exclude=True)

class GetTransformationsQueryTransformationsBaseScaleTransformation(TransformationScaleTransformation, GetTransformationsQueryTransformationsBase, TransformationTrait, BaseModel):
    """A per-axis multiplication, with one entry per input axis"""
    typename: Literal['ScaleTransformation'] = Field(alias='__typename', default='ScaleTransformation', exclude=True)

class GetTransformationsQueryTransformationsBaseSequenceTransformation(TransformationSequenceTransformation, GetTransformationsQueryTransformationsBase, TransformationTrait, BaseModel):
    """An ordered composition of child transformations, applied first to last"""
    typename: Literal['SequenceTransformation'] = Field(alias='__typename', default='SequenceTransformation', exclude=True)

class GetTransformationsQueryTransformationsBaseTranslationTransformation(TransformationTranslationTransformation, GetTransformationsQueryTransformationsBase, TransformationTrait, BaseModel):
    """A per-axis offset, with one entry per input axis"""
    typename: Literal['TranslationTransformation'] = Field(alias='__typename', default='TranslationTransformation', exclude=True)

class GetTransformationsQueryTransformationsBaseUnmappableTransformation(TransformationUnmappableTransformation, GetTransformationsQueryTransformationsBase, TransformationTrait, BaseModel):
    """A declared NON-correspondence: the two systems are related -- one was computed from the other -- and no point of either maps to a point of the other. It has no parameters, no rank and no matrix, and no placement search will walk it, in either direction. This is what a per-object measurement table's relation to the image it was measured from looks like"""
    typename: Literal['UnmappableTransformation'] = Field(alias='__typename', default='UnmappableTransformation', exclude=True)

class GetTransformationsQueryTransformationsBaseCatchAll(GetTransformationsQueryTransformationsBase, BaseModel):
    """Catch all class for GetTransformationsQueryTransformationsBase"""
    typename: str = Field(alias='__typename', exclude=True)

class GetTransformationsQuery(BaseModel):
    """No documentation found for this operation."""
    transformations: Tuple[Union[Annotated[Union[GetTransformationsQueryTransformationsBaseAffineTransformation, GetTransformationsQueryTransformationsBaseBijectionTransformation, GetTransformationsQueryTransformationsBaseByDimensionTransformation, GetTransformationsQueryTransformationsBaseFieldTransformation, GetTransformationsQueryTransformationsBaseIdentityTransformation, GetTransformationsQueryTransformationsBaseMapAxisTransformation, GetTransformationsQueryTransformationsBaseRotationTransformation, GetTransformationsQueryTransformationsBaseScaleTransformation, GetTransformationsQueryTransformationsBaseSequenceTransformation, GetTransformationsQueryTransformationsBaseTranslationTransformation, GetTransformationsQueryTransformationsBaseUnmappableTransformation], Field(discriminator='typename')], GetTransformationsQueryTransformationsBaseCatchAll], ...]
    'List transformations (the directed edges of the coordinate graph). Compose them client-side; the server never resolves a path to world, because the same dataset can sit in two scenes under two registrations'

    class Arguments(BaseModel):
        """Arguments for GetTransformations """
        filters: Optional[TransformationFilter] = Field(default=None)
        pagination: Optional[OffsetPaginationInput] = Field(default=None)
        model_config = ConfigDict(populate_by_name=True)

    class Meta:
        """Meta class for GetTransformations """
        document = 'fragment Axis on Axis {\n  id\n  order\n  name\n  type\n  unit\n  longName\n  __typename\n}\n\nfragment CoordinateSystem on CoordinateSystem {\n  id\n  name\n  epoch\n  axes {\n    ...Axis\n    __typename\n  }\n  __typename\n}\n\nfragment TransformationChild on Transformation {\n  __typename\n  id\n  kind\n  inputAxes\n  outputAxes\n  ... on ScaleTransformation {\n    scale\n  }\n  ... on TranslationTransformation {\n    translation\n  }\n  ... on AffineTransformation {\n    affine\n  }\n  ... on RotationTransformation {\n    affine\n  }\n}\n\nfragment Transformation on Transformation {\n  id\n  kind\n  name\n  version\n  input {\n    ...CoordinateSystem\n    __typename\n  }\n  output {\n    ...CoordinateSystem\n    __typename\n  }\n  ... on ScaleTransformation {\n    scale\n  }\n  ... on TranslationTransformation {\n    translation\n  }\n  ... on AffineTransformation {\n    affine\n  }\n  ... on RotationTransformation {\n    affine\n  }\n  ... on MapAxisTransformation {\n    inputAxes\n    outputAxes\n  }\n  ... on FieldTransformation {\n    field {\n      ...CoordinateSystem\n    }\n  }\n  ... on SequenceTransformation {\n    sequenceChildren: transformations {\n      ...TransformationChild\n    }\n  }\n  ... on ByDimensionTransformation {\n    inputAxes\n    outputAxes\n    byDimensionChildren: transformations {\n      ...TransformationChild\n    }\n  }\n  ... on BijectionTransformation {\n    bijectionChildren: transformations {\n      ...TransformationChild\n    }\n  }\n  __typename\n}\n\nquery GetTransformations($filters: TransformationFilter, $pagination: OffsetPaginationInput) {\n  transformations(filters: $filters, pagination: $pagination) {\n    ...Transformation\n    __typename\n  }\n}'

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
        offset: Annotated[Optional[int], GraphQLDefault('0')] = Field(default=None)
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
        document = 'fragment Era on Era {\n  id\n  begin\n  name\n  __typename\n}\n\nfragment ReferenceView on ReferenceView {\n  ...View\n  id\n  __typename\n}\n\nfragment View on View {\n  xMin\n  xMax\n  yMin\n  yMax\n  tMin\n  tMax\n  cMin\n  cMax\n  zMin\n  zMax\n  __typename\n}\n\nfragment AcquisitionView on AcquisitionView {\n  ...View\n  id\n  description\n  acquiredAt\n  operator {\n    sub\n    __typename\n  }\n  __typename\n}\n\nfragment AffineTransformationView on AffineTransformationView {\n  ...View\n  id\n  affineMatrix\n  stage {\n    id\n    name\n    __typename\n  }\n  __typename\n}\n\nfragment ChannelView on ChannelView {\n  ...View\n  id\n  emissionWavelength\n  excitationWavelength\n  __typename\n}\n\nfragment ContinousScanView on ContinousScanView {\n  ...View\n  id\n  direction\n  __typename\n}\n\nfragment DerivedView on DerivedView {\n  ...View\n  id\n  originImage {\n    id\n    name\n    __typename\n  }\n  __typename\n}\n\nfragment FileView on FileView {\n  ...View\n  id\n  seriesIdentifier\n  file {\n    id\n    name\n    __typename\n  }\n  __typename\n}\n\nfragment InstanceMaskView on InstanceMaskView {\n  ...View\n  id\n  referenceView {\n    ...ReferenceView\n    __typename\n  }\n  __typename\n}\n\nfragment MaskView on MaskView {\n  ...View\n  id\n  referenceView {\n    ...ReferenceView\n    __typename\n  }\n  __typename\n}\n\nfragment OpticsView on OpticsView {\n  ...View\n  id\n  objective {\n    id\n    name\n    serialNumber\n    __typename\n  }\n  camera {\n    id\n    name\n    serialNumber\n    __typename\n  }\n  instrument {\n    id\n    name\n    serialNumber\n    __typename\n  }\n  __typename\n}\n\nfragment RGBView on RGBView {\n  ...View\n  id\n  contexts {\n    id\n    name\n    __typename\n  }\n  name\n  image {\n    id\n    store {\n      ...ZarrStore\n      __typename\n    }\n    derivedScaleViews {\n      id\n      image {\n        id\n        store {\n          ...ZarrStore\n          __typename\n        }\n        __typename\n      }\n      scaleX\n      scaleY\n      scaleZ\n      scaleT\n      scaleC\n      __typename\n    }\n    __typename\n  }\n  colorMap\n  contrastLimitMin\n  contrastLimitMax\n  gamma\n  active\n  fullColour\n  baseColor\n  __typename\n}\n\nfragment ROIView on ROIView {\n  ...View\n  id\n  roi {\n    id\n    name\n    __typename\n  }\n  __typename\n}\n\nfragment TimepointView on TimepointView {\n  ...View\n  id\n  timeSinceStart\n  indexSinceStart\n  era {\n    ...Era\n    __typename\n  }\n  __typename\n}\n\nfragment WellPositionView on WellPositionView {\n  ...View\n  id\n  column\n  row\n  well {\n    id\n    rows\n    columns\n    name\n    __typename\n  }\n  __typename\n}\n\nfragment ZarrStore on ZarrStore {\n  id\n  key\n  bucket\n  path\n  __typename\n}\n\nfragment Image on Image {\n  id\n  name\n  store {\n    ...ZarrStore\n    __typename\n  }\n  views {\n    ...ChannelView\n    ...AffineTransformationView\n    ...TimepointView\n    ...OpticsView\n    ...AcquisitionView\n    ...RGBView\n    ...WellPositionView\n    ...DerivedView\n    ...ROIView\n    ...FileView\n    ...ContinousScanView\n    __typename\n  }\n  maskViews {\n    ...MaskView\n    __typename\n  }\n  instanceMaskViews {\n    ...InstanceMaskView\n    __typename\n  }\n  rgbContexts {\n    id\n    name\n    views {\n      ...RGBView\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nsubscription WatchImages($dataset: ID) {\n  images(dataset: $dataset) {\n    create {\n      ...Image\n      __typename\n    }\n    delete\n    update {\n      ...Image\n      __typename\n    }\n    __typename\n  }\n}'

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

async def acreate_a_dataset(data: ArrayCoercible, scales: Iterable[ScaleInput], name: str, axes: Iterable[Union[AxisInput, str]], anchors: Union[Optional[Iterable[CoordinateAnchorInput]], UnsetType]=UNSET, derived_from: Union[Optional[Iterable[DerivedFromInput]], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> ADataset:
    """CreateADataset 

Create a new dataset from array-like data with optional coordinate anchors and OME metadata

Args:
    data: The `ArrayLike` scalar type represents a reference to a store previously created by the user n a datalayer (required)
    scales: Input type for one pyramid level: the array backing it. Its scale is derived from its actual shape, never supplied (required) (list) (required)
    name: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text. (required)
    axes: Input type for one structural axis of a dataset's pixel grid: its name and its semantic kind. Units and spacings do not belong here -- they belong to a physical space, a separate coordinate system plus one edge (required) (list) (required)
    anchors: Input type for a coordinate anchor, which specifies a list of dimension anchors to anchor to (required) (list)
    derived_from: Where this data came from, as a discriminated union: `kind` selects which sort of source is being named, and only that member's id field is read -- any other is rejected. The member inputs annotated `@unionElementOf(union: "DerivedFromInput")` say which field each kind reads. Direction is always this data -> its source (required) (list)
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    ADataset
"""
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    _input['data'] = data
    _input['scales'] = scales
    _input['name'] = name
    _input['axes'] = axes
    if anchors is not UNSET:
        _input['anchors'] = anchors
    if derived_from is not UNSET:
        _input['derivedFrom'] = derived_from
    variables['input'] = _input
    return (await aexecute(CreateADatasetMutation, variables, rath=rath)).create_a_dataset

def create_a_dataset(data: ArrayCoercible, scales: Iterable[ScaleInput], name: str, axes: Iterable[Union[AxisInput, str]], anchors: Union[Optional[Iterable[CoordinateAnchorInput]], UnsetType]=UNSET, derived_from: Union[Optional[Iterable[DerivedFromInput]], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> ADataset:
    """CreateADataset 

Create a new dataset from array-like data with optional coordinate anchors and OME metadata

Args:
    data: The `ArrayLike` scalar type represents a reference to a store previously created by the user n a datalayer (required)
    scales: Input type for one pyramid level: the array backing it. Its scale is derived from its actual shape, never supplied (required) (list) (required)
    name: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text. (required)
    axes: Input type for one structural axis of a dataset's pixel grid: its name and its semantic kind. Units and spacings do not belong here -- they belong to a physical space, a separate coordinate system plus one edge (required) (list) (required)
    anchors: Input type for a coordinate anchor, which specifies a list of dimension anchors to anchor to (required) (list)
    derived_from: Where this data came from, as a discriminated union: `kind` selects which sort of source is being named, and only that member's id field is read -- any other is rejected. The member inputs annotated `@unionElementOf(union: "DerivedFromInput")` say which field each kind reads. Direction is always this data -> its source (required) (list)
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    ADataset
"""
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    _input['data'] = data
    _input['scales'] = scales
    _input['name'] = name
    _input['axes'] = axes
    if anchors is not UNSET:
        _input['anchors'] = anchors
    if derived_from is not UNSET:
        _input['derivedFrom'] = derived_from
    variables['input'] = _input
    return execute(CreateADatasetMutation, variables, rath=rath).create_a_dataset

async def acreate_animation(scene: IDCoercible, name: str, waypoints: Iterable[AnimationWaypointInput], description: Union[Optional[str], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> Animation:
    """CreateAnimation 

Author a named camera tour of a scene

Args:
    scene: The ID of the scene this tour flies through
    name: The name of the tour
    description: What the tour shows
    waypoints: The poses the viewer pans through, in tour order
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    Animation
"""
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    _input['scene'] = scene
    _input['name'] = name
    if description is not UNSET:
        _input['description'] = description
    _input['waypoints'] = waypoints
    variables['input'] = _input
    return (await aexecute(CreateAnimationMutation, variables, rath=rath)).create_animation

def create_animation(scene: IDCoercible, name: str, waypoints: Iterable[AnimationWaypointInput], description: Union[Optional[str], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> Animation:
    """CreateAnimation 

Author a named camera tour of a scene

Args:
    scene: The ID of the scene this tour flies through
    name: The name of the tour
    description: What the tour shows
    waypoints: The poses the viewer pans through, in tour order
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    Animation
"""
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    _input['scene'] = scene
    _input['name'] = name
    if description is not UNSET:
        _input['description'] = description
    _input['waypoints'] = waypoints
    variables['input'] = _input
    return execute(CreateAnimationMutation, variables, rath=rath).create_animation

async def aupdate_animation(id: IDCoercible, name: Union[Optional[str], UnsetType]=UNSET, description: Union[Optional[str], UnsetType]=UNSET, waypoints: Union[Optional[Iterable[AnimationWaypointInput]], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> Animation:
    """UpdateAnimation 

Re-author a camera tour: rename it, or replace its stops

Args:
    id: The ID of the tour to update
    name: The name of the tour
    description: What the tour shows
    waypoints: The poses, in tour order. Replaces the tour's stops entirely
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    Animation
"""
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    _input['id'] = id
    if name is not UNSET:
        _input['name'] = name
    if description is not UNSET:
        _input['description'] = description
    if waypoints is not UNSET:
        _input['waypoints'] = waypoints
    variables['input'] = _input
    return (await aexecute(UpdateAnimationMutation, variables, rath=rath)).update_animation

def update_animation(id: IDCoercible, name: Union[Optional[str], UnsetType]=UNSET, description: Union[Optional[str], UnsetType]=UNSET, waypoints: Union[Optional[Iterable[AnimationWaypointInput]], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> Animation:
    """UpdateAnimation 

Re-author a camera tour: rename it, or replace its stops

Args:
    id: The ID of the tour to update
    name: The name of the tour
    description: What the tour shows
    waypoints: The poses, in tour order. Replaces the tour's stops entirely
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    Animation
"""
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    _input['id'] = id
    if name is not UNSET:
        _input['name'] = name
    if description is not UNSET:
        _input['description'] = description
    if waypoints is not UNSET:
        _input['waypoints'] = waypoints
    variables['input'] = _input
    return execute(UpdateAnimationMutation, variables, rath=rath).update_animation

async def adelete_animation(id: IDCoercible, rath: Optional[MikroNextRath]=None) -> ID:
    """DeleteAnimation 

Delete an existing camera tour

Args:
    id: The ID of the tour to delete
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    ID
"""
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    _input['id'] = id
    variables['input'] = _input
    return (await aexecute(DeleteAnimationMutation, variables, rath=rath)).delete_animation

def delete_animation(id: IDCoercible, rath: Optional[MikroNextRath]=None) -> ID:
    """DeleteAnimation 

Delete an existing camera tour

Args:
    id: The ID of the tour to delete
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    ID
"""
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    _input['id'] = id
    variables['input'] = _input
    return execute(DeleteAnimationMutation, variables, rath=rath).delete_animation

async def acreate_annotation(kind: RoiKind, vectors: Iterable[ThreeDVector], stroke_color: Union[Optional[Iterable[int]], UnsetType]=UNSET, fill_color: Union[Optional[Iterable[int]], UnsetType]=UNSET, collection: Union[Optional[IDCoercible], UnsetType]=UNSET, scene: Union[Optional[IDCoercible], UnsetType]=UNSET, name: Union[Optional[str], UnsetType]=UNSET, description: Union[Optional[str], UnsetType]=UNSET, coordinates: Union[Optional[Iterable[CoordinateInput]], UnsetType]=UNSET, stroke_width: Union[Optional[float], UnsetType]=UNSET, filled: Union[Optional[bool], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> Annotation:
    """CreateAnnotation 

Draw an annotation into a collection, or onto a scene (exactly one of the two). Drawing on a scene finds its annotation collection or mints it on first use: a coordinate system copying the world's axes, an identity registration into the world, and one annotation layer

Args:
    kind: RoiKind (required)
    vectors: The `Vector` scalar type represents a matrix values as specified by (required) (list) (required)
    stroke_color: The `Int` scalar type represents non-fractional signed whole numeric values. Int can represent values between -(2^31) and 2^31 - 1. (required) (list)
    fill_color: The `Int` scalar type represents non-fractional signed whole numeric values. Int can represent values between -(2^31) and 2^31 - 1. (required) (list)
    collection: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID.
    scene: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID.
    name: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.
    description: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.
    coordinates: A discrete coordinate an annotation is pinned to, e.g. a timepoint or a channel (required) (list)
    stroke_width: The `Float` scalar type represents signed double-precision fractional values as specified by [IEEE 754](https://en.wikipedia.org/wiki/IEEE_floating_point).
    filled: The `Boolean` scalar type represents `true` or `false`.
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    Annotation
"""
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    _input['kind'] = kind
    _input['vectors'] = vectors
    if stroke_color is not UNSET:
        _input['strokeColor'] = stroke_color
    if fill_color is not UNSET:
        _input['fillColor'] = fill_color
    if collection is not UNSET:
        _input['collection'] = collection
    if scene is not UNSET:
        _input['scene'] = scene
    if name is not UNSET:
        _input['name'] = name
    if description is not UNSET:
        _input['description'] = description
    if coordinates is not UNSET:
        _input['coordinates'] = coordinates
    if stroke_width is not UNSET:
        _input['strokeWidth'] = stroke_width
    if filled is not UNSET:
        _input['filled'] = filled
    variables['input'] = _input
    return (await aexecute(CreateAnnotationMutation, variables, rath=rath)).create_annotation

def create_annotation(kind: RoiKind, vectors: Iterable[ThreeDVector], stroke_color: Union[Optional[Iterable[int]], UnsetType]=UNSET, fill_color: Union[Optional[Iterable[int]], UnsetType]=UNSET, collection: Union[Optional[IDCoercible], UnsetType]=UNSET, scene: Union[Optional[IDCoercible], UnsetType]=UNSET, name: Union[Optional[str], UnsetType]=UNSET, description: Union[Optional[str], UnsetType]=UNSET, coordinates: Union[Optional[Iterable[CoordinateInput]], UnsetType]=UNSET, stroke_width: Union[Optional[float], UnsetType]=UNSET, filled: Union[Optional[bool], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> Annotation:
    """CreateAnnotation 

Draw an annotation into a collection, or onto a scene (exactly one of the two). Drawing on a scene finds its annotation collection or mints it on first use: a coordinate system copying the world's axes, an identity registration into the world, and one annotation layer

Args:
    kind: RoiKind (required)
    vectors: The `Vector` scalar type represents a matrix values as specified by (required) (list) (required)
    stroke_color: The `Int` scalar type represents non-fractional signed whole numeric values. Int can represent values between -(2^31) and 2^31 - 1. (required) (list)
    fill_color: The `Int` scalar type represents non-fractional signed whole numeric values. Int can represent values between -(2^31) and 2^31 - 1. (required) (list)
    collection: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID.
    scene: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID.
    name: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.
    description: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.
    coordinates: A discrete coordinate an annotation is pinned to, e.g. a timepoint or a channel (required) (list)
    stroke_width: The `Float` scalar type represents signed double-precision fractional values as specified by [IEEE 754](https://en.wikipedia.org/wiki/IEEE_floating_point).
    filled: The `Boolean` scalar type represents `true` or `false`.
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    Annotation
"""
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    _input['kind'] = kind
    _input['vectors'] = vectors
    if stroke_color is not UNSET:
        _input['strokeColor'] = stroke_color
    if fill_color is not UNSET:
        _input['fillColor'] = fill_color
    if collection is not UNSET:
        _input['collection'] = collection
    if scene is not UNSET:
        _input['scene'] = scene
    if name is not UNSET:
        _input['name'] = name
    if description is not UNSET:
        _input['description'] = description
    if coordinates is not UNSET:
        _input['coordinates'] = coordinates
    if stroke_width is not UNSET:
        _input['strokeWidth'] = stroke_width
    if filled is not UNSET:
        _input['filled'] = filled
    variables['input'] = _input
    return execute(CreateAnnotationMutation, variables, rath=rath).create_annotation

async def acreate_annotations(annotations: Iterable[AnnotationSpecInput], collection: Union[Optional[IDCoercible], UnsetType]=UNSET, scene: Union[Optional[IDCoercible], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> Tuple[Annotation, ...]:
    """CreateAnnotations 

Draw many annotations in one call, into a collection or onto a scene (exactly one of the two, same semantics as createAnnotation). The transform chain and version resolve once for the whole batch, and the rows insert in bulk

Args:
    collection: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID.
    scene: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID.
    annotations: One shape of a bulk draw: the per-annotation subset of CreateAnnotationInput, without the collection/scene target (required) (list) (required)
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    List[Annotation]
"""
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    if collection is not UNSET:
        _input['collection'] = collection
    if scene is not UNSET:
        _input['scene'] = scene
    _input['annotations'] = annotations
    variables['input'] = _input
    return (await aexecute(CreateAnnotationsMutation, variables, rath=rath)).create_annotations

def create_annotations(annotations: Iterable[AnnotationSpecInput], collection: Union[Optional[IDCoercible], UnsetType]=UNSET, scene: Union[Optional[IDCoercible], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> Tuple[Annotation, ...]:
    """CreateAnnotations 

Draw many annotations in one call, into a collection or onto a scene (exactly one of the two, same semantics as createAnnotation). The transform chain and version resolve once for the whole batch, and the rows insert in bulk

Args:
    collection: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID.
    scene: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID.
    annotations: One shape of a bulk draw: the per-annotation subset of CreateAnnotationInput, without the collection/scene target (required) (list) (required)
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    List[Annotation]
"""
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    if collection is not UNSET:
        _input['collection'] = collection
    if scene is not UNSET:
        _input['scene'] = scene
    _input['annotations'] = annotations
    variables['input'] = _input
    return execute(CreateAnnotationsMutation, variables, rath=rath).create_annotations

async def aupdate_annotation(id: IDCoercible, kind: Union[Optional[RoiKind], UnsetType]=UNSET, vectors: Union[Optional[Iterable[ThreeDVector]], UnsetType]=UNSET, stroke_color: Union[Optional[Iterable[int]], UnsetType]=UNSET, fill_color: Union[Optional[Iterable[int]], UnsetType]=UNSET, name: Union[Optional[str], UnsetType]=UNSET, description: Union[Optional[str], UnsetType]=UNSET, coordinates: Union[Optional[Iterable[CoordinateInput]], UnsetType]=UNSET, stroke_width: Union[Optional[float], UnsetType]=UNSET, filled: Union[Optional[bool], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> Annotation:
    """UpdateAnnotation 

Edit an annotation: name, kind, vectors, pins or styling. New vectors re-derive the bounding box against the current transform chain

Args:
    kind: RoiKind
    vectors: The `Vector` scalar type represents a matrix values as specified by (required) (list)
    stroke_color: The `Int` scalar type represents non-fractional signed whole numeric values. Int can represent values between -(2^31) and 2^31 - 1. (required) (list)
    fill_color: The `Int` scalar type represents non-fractional signed whole numeric values. Int can represent values between -(2^31) and 2^31 - 1. (required) (list)
    id: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID. (required)
    name: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.
    description: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.
    coordinates: A discrete coordinate an annotation is pinned to, e.g. a timepoint or a channel (required) (list)
    stroke_width: The `Float` scalar type represents signed double-precision fractional values as specified by [IEEE 754](https://en.wikipedia.org/wiki/IEEE_floating_point).
    filled: The `Boolean` scalar type represents `true` or `false`.
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    Annotation
"""
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    if kind is not UNSET:
        _input['kind'] = kind
    if vectors is not UNSET:
        _input['vectors'] = vectors
    if stroke_color is not UNSET:
        _input['strokeColor'] = stroke_color
    if fill_color is not UNSET:
        _input['fillColor'] = fill_color
    _input['id'] = id
    if name is not UNSET:
        _input['name'] = name
    if description is not UNSET:
        _input['description'] = description
    if coordinates is not UNSET:
        _input['coordinates'] = coordinates
    if stroke_width is not UNSET:
        _input['strokeWidth'] = stroke_width
    if filled is not UNSET:
        _input['filled'] = filled
    variables['input'] = _input
    return (await aexecute(UpdateAnnotationMutation, variables, rath=rath)).update_annotation

def update_annotation(id: IDCoercible, kind: Union[Optional[RoiKind], UnsetType]=UNSET, vectors: Union[Optional[Iterable[ThreeDVector]], UnsetType]=UNSET, stroke_color: Union[Optional[Iterable[int]], UnsetType]=UNSET, fill_color: Union[Optional[Iterable[int]], UnsetType]=UNSET, name: Union[Optional[str], UnsetType]=UNSET, description: Union[Optional[str], UnsetType]=UNSET, coordinates: Union[Optional[Iterable[CoordinateInput]], UnsetType]=UNSET, stroke_width: Union[Optional[float], UnsetType]=UNSET, filled: Union[Optional[bool], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> Annotation:
    """UpdateAnnotation 

Edit an annotation: name, kind, vectors, pins or styling. New vectors re-derive the bounding box against the current transform chain

Args:
    kind: RoiKind
    vectors: The `Vector` scalar type represents a matrix values as specified by (required) (list)
    stroke_color: The `Int` scalar type represents non-fractional signed whole numeric values. Int can represent values between -(2^31) and 2^31 - 1. (required) (list)
    fill_color: The `Int` scalar type represents non-fractional signed whole numeric values. Int can represent values between -(2^31) and 2^31 - 1. (required) (list)
    id: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID. (required)
    name: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.
    description: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.
    coordinates: A discrete coordinate an annotation is pinned to, e.g. a timepoint or a channel (required) (list)
    stroke_width: The `Float` scalar type represents signed double-precision fractional values as specified by [IEEE 754](https://en.wikipedia.org/wiki/IEEE_floating_point).
    filled: The `Boolean` scalar type represents `true` or `false`.
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    Annotation
"""
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    if kind is not UNSET:
        _input['kind'] = kind
    if vectors is not UNSET:
        _input['vectors'] = vectors
    if stroke_color is not UNSET:
        _input['strokeColor'] = stroke_color
    if fill_color is not UNSET:
        _input['fillColor'] = fill_color
    _input['id'] = id
    if name is not UNSET:
        _input['name'] = name
    if description is not UNSET:
        _input['description'] = description
    if coordinates is not UNSET:
        _input['coordinates'] = coordinates
    if stroke_width is not UNSET:
        _input['strokeWidth'] = stroke_width
    if filled is not UNSET:
        _input['filled'] = filled
    variables['input'] = _input
    return execute(UpdateAnnotationMutation, variables, rath=rath).update_annotation

async def adelete_annotation(id: IDCoercible, rath: Optional[MikroNextRath]=None) -> ID:
    """DeleteAnnotation 

Delete an existing annotation

Args:
    id: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID. (required)
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    ID
"""
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    _input['id'] = id
    variables['input'] = _input
    return (await aexecute(DeleteAnnotationMutation, variables, rath=rath)).delete_annotation

def delete_annotation(id: IDCoercible, rath: Optional[MikroNextRath]=None) -> ID:
    """DeleteAnnotation 

Delete an existing annotation

Args:
    id: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID. (required)
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    ID
"""
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    _input['id'] = id
    variables['input'] = _input
    return execute(DeleteAnnotationMutation, variables, rath=rath).delete_annotation

async def acreate_annotation_collection(name: str, axes: Iterable[Union[AxisInput, str]], description: Union[Optional[str], UnsetType]=UNSET, derived_from: Union[Optional[Iterable[DerivedFromInput]], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> AnnotationCollection:
    """CreateAnnotationCollection 

Create an annotation collection explicitly, in a coordinate system of its own, optionally derived from the system the shapes are drawn over. The common path -- drawing on a scene -- goes through createAnnotation instead, which mints the scene's collection on first use

Args:
    name: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text. (required)
    description: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.
    axes: Input type for one structural axis of a dataset's pixel grid: its name and its semantic kind. Units and spacings do not belong here -- they belong to a physical space, a separate coordinate system plus one edge (required) (list) (required)
    derived_from: Where this data came from, as a discriminated union: `kind` selects which sort of source is being named, and only that member's id field is read -- any other is rejected. The member inputs annotated `@unionElementOf(union: "DerivedFromInput")` say which field each kind reads. Direction is always this data -> its source (required) (list)
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    AnnotationCollection
"""
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    _input['name'] = name
    if description is not UNSET:
        _input['description'] = description
    _input['axes'] = axes
    if derived_from is not UNSET:
        _input['derivedFrom'] = derived_from
    variables['input'] = _input
    return (await aexecute(CreateAnnotationCollectionMutation, variables, rath=rath)).create_annotation_collection

def create_annotation_collection(name: str, axes: Iterable[Union[AxisInput, str]], description: Union[Optional[str], UnsetType]=UNSET, derived_from: Union[Optional[Iterable[DerivedFromInput]], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> AnnotationCollection:
    """CreateAnnotationCollection 

Create an annotation collection explicitly, in a coordinate system of its own, optionally derived from the system the shapes are drawn over. The common path -- drawing on a scene -- goes through createAnnotation instead, which mints the scene's collection on first use

Args:
    name: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text. (required)
    description: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.
    axes: Input type for one structural axis of a dataset's pixel grid: its name and its semantic kind. Units and spacings do not belong here -- they belong to a physical space, a separate coordinate system plus one edge (required) (list) (required)
    derived_from: Where this data came from, as a discriminated union: `kind` selects which sort of source is being named, and only that member's id field is read -- any other is rejected. The member inputs annotated `@unionElementOf(union: "DerivedFromInput")` say which field each kind reads. Direction is always this data -> its source (required) (list)
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    AnnotationCollection
"""
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    _input['name'] = name
    if description is not UNSET:
        _input['description'] = description
    _input['axes'] = axes
    if derived_from is not UNSET:
        _input['derivedFrom'] = derived_from
    variables['input'] = _input
    return execute(CreateAnnotationCollectionMutation, variables, rath=rath).create_annotation_collection

async def adelete_annotation_collection(id: IDCoercible, rath: Optional[MikroNextRath]=None) -> ID:
    """DeleteAnnotationCollection 

Delete an annotation collection. Its coordinate system, its annotations and its layers cascade with it

Args:
    id: The ID of the annotation collection to delete
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    ID
"""
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    _input['id'] = id
    variables['input'] = _input
    return (await aexecute(DeleteAnnotationCollectionMutation, variables, rath=rath)).delete_annotation_collection

def delete_annotation_collection(id: IDCoercible, rath: Optional[MikroNextRath]=None) -> ID:
    """DeleteAnnotationCollection 

Delete an annotation collection. Its coordinate system, its annotations and its layers cascade with it

Args:
    id: The ID of the annotation collection to delete
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    ID
"""
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    _input['id'] = id
    variables['input'] = _input
    return execute(DeleteAnnotationCollectionMutation, variables, rath=rath).delete_annotation_collection

async def acreate_camera(serial_number: str, name: Union[Optional[str], UnsetType]=UNSET, model: Union[Optional[str], UnsetType]=UNSET, bit_depth: Union[Optional[int], UnsetType]=UNSET, sensor_size_x: Union[Optional[int], UnsetType]=UNSET, sensor_size_y: Union[Optional[int], UnsetType]=UNSET, pixel_size_x: Union[Optional[Length], UnsetType]=UNSET, pixel_size_y: Union[Optional[Length], UnsetType]=UNSET, manufacturer: Union[Optional[str], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> CreateCameraMutationCreatecamera:
    """CreateCamera 

Create a new camera configuration

Args:
    serial_number: The unique serial number of the camera
    name: The name of the camera
    model: The model of the camera
    bit_depth: The bit depth of the camera sensor
    sensor_size_x: The sensor size in x direction (pixels)
    sensor_size_y: The sensor size in y direction (pixels)
    pixel_size_x: The physical pixel size in x direction (e.g. '6.5 µm')
    pixel_size_y: The physical pixel size in y direction (e.g. '6.5 µm')
    manufacturer: The manufacturer of the camera
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    CreateCameraMutationCreatecamera
"""
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    _input['serialNumber'] = serial_number
    if name is not UNSET:
        _input['name'] = name
    if model is not UNSET:
        _input['model'] = model
    if bit_depth is not UNSET:
        _input['bitDepth'] = bit_depth
    if sensor_size_x is not UNSET:
        _input['sensorSizeX'] = sensor_size_x
    if sensor_size_y is not UNSET:
        _input['sensorSizeY'] = sensor_size_y
    if pixel_size_x is not UNSET:
        _input['pixelSizeX'] = pixel_size_x
    if pixel_size_y is not UNSET:
        _input['pixelSizeY'] = pixel_size_y
    if manufacturer is not UNSET:
        _input['manufacturer'] = manufacturer
    variables['input'] = _input
    return (await aexecute(CreateCameraMutation, variables, rath=rath)).create_camera

def create_camera(serial_number: str, name: Union[Optional[str], UnsetType]=UNSET, model: Union[Optional[str], UnsetType]=UNSET, bit_depth: Union[Optional[int], UnsetType]=UNSET, sensor_size_x: Union[Optional[int], UnsetType]=UNSET, sensor_size_y: Union[Optional[int], UnsetType]=UNSET, pixel_size_x: Union[Optional[Length], UnsetType]=UNSET, pixel_size_y: Union[Optional[Length], UnsetType]=UNSET, manufacturer: Union[Optional[str], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> CreateCameraMutationCreatecamera:
    """CreateCamera 

Create a new camera configuration

Args:
    serial_number: The unique serial number of the camera
    name: The name of the camera
    model: The model of the camera
    bit_depth: The bit depth of the camera sensor
    sensor_size_x: The sensor size in x direction (pixels)
    sensor_size_y: The sensor size in y direction (pixels)
    pixel_size_x: The physical pixel size in x direction (e.g. '6.5 µm')
    pixel_size_y: The physical pixel size in y direction (e.g. '6.5 µm')
    manufacturer: The manufacturer of the camera
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    CreateCameraMutationCreatecamera
"""
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    _input['serialNumber'] = serial_number
    if name is not UNSET:
        _input['name'] = name
    if model is not UNSET:
        _input['model'] = model
    if bit_depth is not UNSET:
        _input['bitDepth'] = bit_depth
    if sensor_size_x is not UNSET:
        _input['sensorSizeX'] = sensor_size_x
    if sensor_size_y is not UNSET:
        _input['sensorSizeY'] = sensor_size_y
    if pixel_size_x is not UNSET:
        _input['pixelSizeX'] = pixel_size_x
    if pixel_size_y is not UNSET:
        _input['pixelSizeY'] = pixel_size_y
    if manufacturer is not UNSET:
        _input['manufacturer'] = manufacturer
    variables['input'] = _input
    return execute(CreateCameraMutation, variables, rath=rath).create_camera

async def aensure_camera(serial_number: str, name: Union[Optional[str], UnsetType]=UNSET, model: Union[Optional[str], UnsetType]=UNSET, bit_depth: Union[Optional[int], UnsetType]=UNSET, sensor_size_x: Union[Optional[int], UnsetType]=UNSET, sensor_size_y: Union[Optional[int], UnsetType]=UNSET, pixel_size_x: Union[Optional[Length], UnsetType]=UNSET, pixel_size_y: Union[Optional[Length], UnsetType]=UNSET, manufacturer: Union[Optional[str], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> EnsureCameraMutationEnsurecamera:
    """EnsureCamera 

Ensure a camera exists, creating if needed

Args:
    serial_number: The unique serial number of the camera
    name: The name of the camera
    model: The model of the camera
    bit_depth: The bit depth of the camera sensor
    sensor_size_x: The sensor size in x direction (pixels)
    sensor_size_y: The sensor size in y direction (pixels)
    pixel_size_x: The physical pixel size in x direction (e.g. '6.5 µm')
    pixel_size_y: The physical pixel size in y direction (e.g. '6.5 µm')
    manufacturer: The manufacturer of the camera
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    EnsureCameraMutationEnsurecamera
"""
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    _input['serialNumber'] = serial_number
    if name is not UNSET:
        _input['name'] = name
    if model is not UNSET:
        _input['model'] = model
    if bit_depth is not UNSET:
        _input['bitDepth'] = bit_depth
    if sensor_size_x is not UNSET:
        _input['sensorSizeX'] = sensor_size_x
    if sensor_size_y is not UNSET:
        _input['sensorSizeY'] = sensor_size_y
    if pixel_size_x is not UNSET:
        _input['pixelSizeX'] = pixel_size_x
    if pixel_size_y is not UNSET:
        _input['pixelSizeY'] = pixel_size_y
    if manufacturer is not UNSET:
        _input['manufacturer'] = manufacturer
    variables['input'] = _input
    return (await aexecute(EnsureCameraMutation, variables, rath=rath)).ensure_camera

def ensure_camera(serial_number: str, name: Union[Optional[str], UnsetType]=UNSET, model: Union[Optional[str], UnsetType]=UNSET, bit_depth: Union[Optional[int], UnsetType]=UNSET, sensor_size_x: Union[Optional[int], UnsetType]=UNSET, sensor_size_y: Union[Optional[int], UnsetType]=UNSET, pixel_size_x: Union[Optional[Length], UnsetType]=UNSET, pixel_size_y: Union[Optional[Length], UnsetType]=UNSET, manufacturer: Union[Optional[str], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> EnsureCameraMutationEnsurecamera:
    """EnsureCamera 

Ensure a camera exists, creating if needed

Args:
    serial_number: The unique serial number of the camera
    name: The name of the camera
    model: The model of the camera
    bit_depth: The bit depth of the camera sensor
    sensor_size_x: The sensor size in x direction (pixels)
    sensor_size_y: The sensor size in y direction (pixels)
    pixel_size_x: The physical pixel size in x direction (e.g. '6.5 µm')
    pixel_size_y: The physical pixel size in y direction (e.g. '6.5 µm')
    manufacturer: The manufacturer of the camera
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    EnsureCameraMutationEnsurecamera
"""
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    _input['serialNumber'] = serial_number
    if name is not UNSET:
        _input['name'] = name
    if model is not UNSET:
        _input['model'] = model
    if bit_depth is not UNSET:
        _input['bitDepth'] = bit_depth
    if sensor_size_x is not UNSET:
        _input['sensorSizeX'] = sensor_size_x
    if sensor_size_y is not UNSET:
        _input['sensorSizeY'] = sensor_size_y
    if pixel_size_x is not UNSET:
        _input['pixelSizeX'] = pixel_size_x
    if pixel_size_y is not UNSET:
        _input['pixelSizeY'] = pixel_size_y
    if manufacturer is not UNSET:
        _input['manufacturer'] = manufacturer
    variables['input'] = _input
    return execute(EnsureCameraMutation, variables, rath=rath).ensure_camera

async def acreate_coordinate_system(name: str, axes: Iterable[PhysicalAxisInput], registrations: Iterable[RegistrationPathInput], epoch: Union[Optional[datetime], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> CoordinateSystem:
    """CreateCoordinateSystem 

Create a SHARED coordinate system (an ownerless space) and, in one call, author the edges registering any number of sources (datasets, table datasets, mesh collections, coordinate systems) into it

Args:
    name: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text. (required)
    axes: Input type for one axis of a unit-carrying coordinate system: its name, its semantic kind and its physical unit (required) (list) (required)
    epoch: Date with time (isoformat)
    registrations: A source (dataset, table dataset, mesh collection, or coordinate system) to register into a shared space, plus the edge that places it. The edge points from the source's own coordinate system to the shared space; the transform is validated exactly as createTransformation validates one (required) (list) (required)
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    CoordinateSystem
"""
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    _input['name'] = name
    _input['axes'] = axes
    if epoch is not UNSET:
        _input['epoch'] = epoch
    _input['registrations'] = registrations
    variables['input'] = _input
    return (await aexecute(CreateCoordinateSystemMutation, variables, rath=rath)).create_coordinate_system

def create_coordinate_system(name: str, axes: Iterable[PhysicalAxisInput], registrations: Iterable[RegistrationPathInput], epoch: Union[Optional[datetime], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> CoordinateSystem:
    """CreateCoordinateSystem 

Create a SHARED coordinate system (an ownerless space) and, in one call, author the edges registering any number of sources (datasets, table datasets, mesh collections, coordinate systems) into it

Args:
    name: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text. (required)
    axes: Input type for one axis of a unit-carrying coordinate system: its name, its semantic kind and its physical unit (required) (list) (required)
    epoch: Date with time (isoformat)
    registrations: A source (dataset, table dataset, mesh collection, or coordinate system) to register into a shared space, plus the edge that places it. The edge points from the source's own coordinate system to the shared space; the transform is validated exactly as createTransformation validates one (required) (list) (required)
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    CoordinateSystem
"""
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    _input['name'] = name
    _input['axes'] = axes
    if epoch is not UNSET:
        _input['epoch'] = epoch
    _input['registrations'] = registrations
    variables['input'] = _input
    return execute(CreateCoordinateSystemMutation, variables, rath=rath).create_coordinate_system

async def aupdate_coordinate_system(id: IDCoercible, name: Union[Optional[str], UnsetType]=UNSET, epoch: Union[Optional[datetime], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> CoordinateSystem:
    """UpdateCoordinateSystem 

Rename a shared coordinate system or anchor its clock. Shared spaces only -- an owned system's name is its container's business, and where data sits is an edge (updateTransformation), not a property of the space

Args:
    id: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID. (required)
    name: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.
    epoch: Date with time (isoformat)
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    CoordinateSystem
"""
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    _input['id'] = id
    if name is not UNSET:
        _input['name'] = name
    if epoch is not UNSET:
        _input['epoch'] = epoch
    variables['input'] = _input
    return (await aexecute(UpdateCoordinateSystemMutation, variables, rath=rath)).update_coordinate_system

def update_coordinate_system(id: IDCoercible, name: Union[Optional[str], UnsetType]=UNSET, epoch: Union[Optional[datetime], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> CoordinateSystem:
    """UpdateCoordinateSystem 

Rename a shared coordinate system or anchor its clock. Shared spaces only -- an owned system's name is its container's business, and where data sits is an edge (updateTransformation), not a property of the space

Args:
    id: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID. (required)
    name: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.
    epoch: Date with time (isoformat)
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    CoordinateSystem
"""
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    _input['id'] = id
    if name is not UNSET:
        _input['name'] = name
    if epoch is not UNSET:
        _input['epoch'] = epoch
    variables['input'] = _input
    return execute(UpdateCoordinateSystemMutation, variables, rath=rath).update_coordinate_system

async def adelete_coordinate_system(id: IDCoercible, rath: Optional[MikroNextRath]=None) -> ID:
    """DeleteCoordinateSystem 

Delete an unused shared coordinate system. Refused while any scene is rooted in it or any transformation edge touches it. This is the only door a shared space leaves through -- deleting a scene never deletes one. Other system kinds cascade with their owner and cannot be deleted directly

Args:
    id: The ID of the shared coordinate system to delete
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    ID
"""
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    _input['id'] = id
    variables['input'] = _input
    return (await aexecute(DeleteCoordinateSystemMutation, variables, rath=rath)).delete_coordinate_system

def delete_coordinate_system(id: IDCoercible, rath: Optional[MikroNextRath]=None) -> ID:
    """DeleteCoordinateSystem 

Delete an unused shared coordinate system. Refused while any scene is rooted in it or any transformation edge touches it. This is the only door a shared space leaves through -- deleting a scene never deletes one. Other system kinds cascade with their owner and cannot be deleted directly

Args:
    id: The ID of the shared coordinate system to delete
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    ID
"""
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    _input['id'] = id
    variables['input'] = _input
    return execute(DeleteCoordinateSystemMutation, variables, rath=rath).delete_coordinate_system

async def aclear_coordinate_system(id: IDCoercible, rath: Optional[MikroNextRath]=None) -> Tuple[ID, ...]:
    """ClearCoordinateSystem 

Delete every registration INTO a shared space in one call, returning the deleted edge ids. The space, the scenes over it (their layers drop to UNREGISTERED) and the space's own claims into wider spaces all survive. Guarded by the space's creator: clearing a space is the space-owner's act

Args:
    id: The ID of the shared coordinate system to clear
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    List[ID]
"""
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    _input['id'] = id
    variables['input'] = _input
    return (await aexecute(ClearCoordinateSystemMutation, variables, rath=rath)).clear_coordinate_system

def clear_coordinate_system(id: IDCoercible, rath: Optional[MikroNextRath]=None) -> Tuple[ID, ...]:
    """ClearCoordinateSystem 

Delete every registration INTO a shared space in one call, returning the deleted edge ids. The space, the scenes over it (their layers drop to UNREGISTERED) and the space's own claims into wider spaces all survive. Guarded by the space's creator: clearing a space is the space-owner's act

Args:
    id: The ID of the shared coordinate system to clear
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    List[ID]
"""
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    _input['id'] = id
    variables['input'] = _input
    return execute(ClearCoordinateSystemMutation, variables, rath=rath).clear_coordinate_system

async def adelete_registration(world: IDCoercible, dataset: Union[Optional[IDCoercible], UnsetType]=UNSET, table_dataset: Union[Optional[IDCoercible], UnsetType]=UNSET, mesh_collection: Union[Optional[IDCoercible], UnsetType]=UNSET, annotation_collection: Union[Optional[IDCoercible], UnsetType]=UNSET, coordinate_system: Union[Optional[IDCoercible], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> Tuple[ID, ...]:
    """DeleteRegistration 

Un-register a source from a space by naming the source and the space rather than the edge. Deletes every edge from the source's space into that one -- rivals are allowed, so there is no single edge to mean -- and returns their ids. An UNMAPPABLE declaration is not a placement and is never matched

Args:
    dataset: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID.
    table_dataset: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID.
    mesh_collection: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID.
    annotation_collection: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID.
    coordinate_system: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID.
    world: The shared space the registration goes into
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    List[ID]
"""
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    if dataset is not UNSET:
        _input['dataset'] = dataset
    if table_dataset is not UNSET:
        _input['tableDataset'] = table_dataset
    if mesh_collection is not UNSET:
        _input['meshCollection'] = mesh_collection
    if annotation_collection is not UNSET:
        _input['annotationCollection'] = annotation_collection
    if coordinate_system is not UNSET:
        _input['coordinateSystem'] = coordinate_system
    _input['world'] = world
    variables['input'] = _input
    return (await aexecute(DeleteRegistrationMutation, variables, rath=rath)).delete_registration

def delete_registration(world: IDCoercible, dataset: Union[Optional[IDCoercible], UnsetType]=UNSET, table_dataset: Union[Optional[IDCoercible], UnsetType]=UNSET, mesh_collection: Union[Optional[IDCoercible], UnsetType]=UNSET, annotation_collection: Union[Optional[IDCoercible], UnsetType]=UNSET, coordinate_system: Union[Optional[IDCoercible], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> Tuple[ID, ...]:
    """DeleteRegistration 

Un-register a source from a space by naming the source and the space rather than the edge. Deletes every edge from the source's space into that one -- rivals are allowed, so there is no single edge to mean -- and returns their ids. An UNMAPPABLE declaration is not a placement and is never matched

Args:
    dataset: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID.
    table_dataset: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID.
    mesh_collection: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID.
    annotation_collection: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID.
    coordinate_system: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID.
    world: The shared space the registration goes into
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    List[ID]
"""
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    if dataset is not UNSET:
        _input['dataset'] = dataset
    if table_dataset is not UNSET:
        _input['tableDataset'] = table_dataset
    if mesh_collection is not UNSET:
        _input['meshCollection'] = mesh_collection
    if annotation_collection is not UNSET:
        _input['annotationCollection'] = annotation_collection
    if coordinate_system is not UNSET:
        _input['coordinateSystem'] = coordinate_system
    _input['world'] = world
    variables['input'] = _input
    return execute(DeleteRegistrationMutation, variables, rath=rath).delete_registration

async def arequest_bigfile_upload(original_file_name: str, file_size: Union[Optional[int], UnsetType]=UNSET, content_type: Union[Optional[str], UnsetType]=UNSET, host: Union[Optional[str], UnsetType]=UNSET, port: Union[Optional[int], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> BigFileUploadGrant:
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
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    _input['originalFileName'] = original_file_name
    if file_size is not UNSET:
        _input['fileSize'] = file_size
    if content_type is not UNSET:
        _input['contentType'] = content_type
    if host is not UNSET:
        _input['host'] = host
    if port is not UNSET:
        _input['port'] = port
    variables['input'] = _input
    return (await aexecute(RequestBigfileUploadMutation, variables, rath=rath)).request_bigfile_upload

def request_bigfile_upload(original_file_name: str, file_size: Union[Optional[int], UnsetType]=UNSET, content_type: Union[Optional[str], UnsetType]=UNSET, host: Union[Optional[str], UnsetType]=UNSET, port: Union[Optional[int], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> BigFileUploadGrant:
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
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    _input['originalFileName'] = original_file_name
    if file_size is not UNSET:
        _input['fileSize'] = file_size
    if content_type is not UNSET:
        _input['contentType'] = content_type
    if host is not UNSET:
        _input['host'] = host
    if port is not UNSET:
        _input['port'] = port
    variables['input'] = _input
    return execute(RequestBigfileUploadMutation, variables, rath=rath).request_bigfile_upload

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
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    _input['storeId'] = store_id
    _input['valid'] = valid
    variables['input'] = _input
    return (await aexecute(FinishBigfileUploadMutation, variables, rath=rath)).finish_bigfile_upload

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
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    _input['storeId'] = store_id
    _input['valid'] = valid
    variables['input'] = _input
    return execute(FinishBigfileUploadMutation, variables, rath=rath).finish_bigfile_upload

async def arequest_bigfile_access(store_id: str, rath: Optional[MikroNextRath]=None) -> BigFileAccessGrant:
    """RequestBigfileAccess 

Request temporary S3 read credentials for a big file

Args:
    store_id: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text. (required)
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    BigFileAccessGrant
"""
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    _input['storeId'] = store_id
    variables['input'] = _input
    return (await aexecute(RequestBigfileAccessMutation, variables, rath=rath)).request_bigfile_access

def request_bigfile_access(store_id: str, rath: Optional[MikroNextRath]=None) -> BigFileAccessGrant:
    """RequestBigfileAccess 

Request temporary S3 read credentials for a big file

Args:
    store_id: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text. (required)
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    BigFileAccessGrant
"""
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    _input['storeId'] = store_id
    variables['input'] = _input
    return execute(RequestBigfileAccessMutation, variables, rath=rath).request_bigfile_access

async def arequest_media_upload(original_file_name: str, file_size: Union[Optional[int], UnsetType]=UNSET, content_type: Union[Optional[str], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> MediaUploadGrant:
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
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    _input['originalFileName'] = original_file_name
    if file_size is not UNSET:
        _input['fileSize'] = file_size
    if content_type is not UNSET:
        _input['contentType'] = content_type
    variables['input'] = _input
    return (await aexecute(RequestMediaUploadMutation, variables, rath=rath)).request_media_upload

def request_media_upload(original_file_name: str, file_size: Union[Optional[int], UnsetType]=UNSET, content_type: Union[Optional[str], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> MediaUploadGrant:
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
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    _input['originalFileName'] = original_file_name
    if file_size is not UNSET:
        _input['fileSize'] = file_size
    if content_type is not UNSET:
        _input['contentType'] = content_type
    variables['input'] = _input
    return execute(RequestMediaUploadMutation, variables, rath=rath).request_media_upload

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
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    _input['storeId'] = store_id
    _input['valid'] = valid
    variables['input'] = _input
    return (await aexecute(FinishMediaUploadMutation, variables, rath=rath)).finish_media_upload

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
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    _input['storeId'] = store_id
    _input['valid'] = valid
    variables['input'] = _input
    return execute(FinishMediaUploadMutation, variables, rath=rath).finish_media_upload

async def arequest_media_access(store_id: str, rath: Optional[MikroNextRath]=None) -> MediaAccessGrant:
    """RequestMediaAccess 

Request temporary S3 read credentials for a media file

Args:
    store_id: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text. (required)
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    MediaAccessGrant
"""
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    _input['storeId'] = store_id
    variables['input'] = _input
    return (await aexecute(RequestMediaAccessMutation, variables, rath=rath)).request_media_access

def request_media_access(store_id: str, rath: Optional[MikroNextRath]=None) -> MediaAccessGrant:
    """RequestMediaAccess 

Request temporary S3 read credentials for a media file

Args:
    store_id: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text. (required)
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    MediaAccessGrant
"""
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    _input['storeId'] = store_id
    variables['input'] = _input
    return execute(RequestMediaAccessMutation, variables, rath=rath).request_media_access

async def arequest_parquet_upload(content_type: Union[Optional[str], UnsetType]=UNSET, host: Union[Optional[str], UnsetType]=UNSET, port: Union[Optional[int], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> ParquetUploadGrant:
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
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    if content_type is not UNSET:
        _input['contentType'] = content_type
    if host is not UNSET:
        _input['host'] = host
    if port is not UNSET:
        _input['port'] = port
    variables['input'] = _input
    return (await aexecute(RequestParquetUploadMutation, variables, rath=rath)).request_parquet_upload

def request_parquet_upload(content_type: Union[Optional[str], UnsetType]=UNSET, host: Union[Optional[str], UnsetType]=UNSET, port: Union[Optional[int], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> ParquetUploadGrant:
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
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    if content_type is not UNSET:
        _input['contentType'] = content_type
    if host is not UNSET:
        _input['host'] = host
    if port is not UNSET:
        _input['port'] = port
    variables['input'] = _input
    return execute(RequestParquetUploadMutation, variables, rath=rath).request_parquet_upload

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
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    _input['storeId'] = store_id
    _input['valid'] = valid
    variables['input'] = _input
    return (await aexecute(FinishParquetUploadMutation, variables, rath=rath)).finish_parquet_upload

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
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    _input['storeId'] = store_id
    _input['valid'] = valid
    variables['input'] = _input
    return execute(FinishParquetUploadMutation, variables, rath=rath).finish_parquet_upload

async def arequest_parquet_access(store_id: str, rath: Optional[MikroNextRath]=None) -> ParquetAccessGrant:
    """RequestParquetAccess 

Request temporary S3 read credentials for a Parquet file

Args:
    store_id: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text. (required)
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    ParquetAccessGrant
"""
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    _input['storeId'] = store_id
    variables['input'] = _input
    return (await aexecute(RequestParquetAccessMutation, variables, rath=rath)).request_parquet_access

def request_parquet_access(store_id: str, rath: Optional[MikroNextRath]=None) -> ParquetAccessGrant:
    """RequestParquetAccess 

Request temporary S3 read credentials for a Parquet file

Args:
    store_id: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text. (required)
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    ParquetAccessGrant
"""
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    _input['storeId'] = store_id
    variables['input'] = _input
    return execute(RequestParquetAccessMutation, variables, rath=rath).request_parquet_access

async def arequest_zarr_upload(shape: Union[Optional[Iterable[int]], UnsetType]=UNSET, chunks: Union[Optional[Iterable[int]], UnsetType]=UNSET, version: Union[Optional[str], UnsetType]=UNSET, host: Union[Optional[str], UnsetType]=UNSET, port: Union[Optional[int], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> ZarrUploadGrant:
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
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    if shape is not UNSET:
        _input['shape'] = shape
    if chunks is not UNSET:
        _input['chunks'] = chunks
    if version is not UNSET:
        _input['version'] = version
    if host is not UNSET:
        _input['host'] = host
    if port is not UNSET:
        _input['port'] = port
    variables['input'] = _input
    return (await aexecute(RequestZarrUploadMutation, variables, rath=rath)).request_zarr_upload

def request_zarr_upload(shape: Union[Optional[Iterable[int]], UnsetType]=UNSET, chunks: Union[Optional[Iterable[int]], UnsetType]=UNSET, version: Union[Optional[str], UnsetType]=UNSET, host: Union[Optional[str], UnsetType]=UNSET, port: Union[Optional[int], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> ZarrUploadGrant:
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
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    if shape is not UNSET:
        _input['shape'] = shape
    if chunks is not UNSET:
        _input['chunks'] = chunks
    if version is not UNSET:
        _input['version'] = version
    if host is not UNSET:
        _input['host'] = host
    if port is not UNSET:
        _input['port'] = port
    variables['input'] = _input
    return execute(RequestZarrUploadMutation, variables, rath=rath).request_zarr_upload

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
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    _input['storeId'] = store_id
    _input['valid'] = valid
    variables['input'] = _input
    return (await aexecute(FinishZarrUploadMutation, variables, rath=rath)).finish_zarr_upload

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
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    _input['storeId'] = store_id
    _input['valid'] = valid
    variables['input'] = _input
    return execute(FinishZarrUploadMutation, variables, rath=rath).finish_zarr_upload

async def arequest_zarr_access(store_id: str, rath: Optional[MikroNextRath]=None) -> ZarrAccessGrant:
    """RequestZarrAccess 

Request temporary S3 read credentials for a Zarr store

Args:
    store_id: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text. (required)
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    ZarrAccessGrant
"""
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    _input['storeId'] = store_id
    variables['input'] = _input
    return (await aexecute(RequestZarrAccessMutation, variables, rath=rath)).request_zarr_access

def request_zarr_access(store_id: str, rath: Optional[MikroNextRath]=None) -> ZarrAccessGrant:
    """RequestZarrAccess 

Request temporary S3 read credentials for a Zarr store

Args:
    store_id: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text. (required)
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    ZarrAccessGrant
"""
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    _input['storeId'] = store_id
    variables['input'] = _input
    return execute(RequestZarrAccessMutation, variables, rath=rath).request_zarr_access

async def acreate_dataset(name: str, parent: Union[Optional[IDCoercible], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> Dataset:
    """CreateDataset 

Create a new dataset to organize data

Args:
    name: The name of the dataset
    parent: The ID of the parent dataset to nest this dataset under
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    Dataset
"""
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    _input['name'] = name
    if parent is not UNSET:
        _input['parent'] = parent
    variables['input'] = _input
    return (await aexecute(CreateDatasetMutation, variables, rath=rath)).create_dataset

def create_dataset(name: str, parent: Union[Optional[IDCoercible], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> Dataset:
    """CreateDataset 

Create a new dataset to organize data

Args:
    name: The name of the dataset
    parent: The ID of the parent dataset to nest this dataset under
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    Dataset
"""
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    _input['name'] = name
    if parent is not UNSET:
        _input['parent'] = parent
    variables['input'] = _input
    return execute(CreateDatasetMutation, variables, rath=rath).create_dataset

async def aensure_dataset(name: str, parent: Union[Optional[IDCoercible], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> Dataset:
    """EnsureDataset 

Create a new dataset to organize data

Args:
    name: The name of the dataset
    parent: The ID of the parent dataset to nest this dataset under
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    Dataset
"""
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    _input['name'] = name
    if parent is not UNSET:
        _input['parent'] = parent
    variables['input'] = _input
    return (await aexecute(EnsureDatasetMutation, variables, rath=rath)).ensure_dataset

def ensure_dataset(name: str, parent: Union[Optional[IDCoercible], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> Dataset:
    """EnsureDataset 

Create a new dataset to organize data

Args:
    name: The name of the dataset
    parent: The ID of the parent dataset to nest this dataset under
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    Dataset
"""
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    _input['name'] = name
    if parent is not UNSET:
        _input['parent'] = parent
    variables['input'] = _input
    return execute(EnsureDatasetMutation, variables, rath=rath).ensure_dataset

async def aupdate_dataset(name: str, id: IDCoercible, parent: Union[Optional[IDCoercible], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> Dataset:
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
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    _input['name'] = name
    if parent is not UNSET:
        _input['parent'] = parent
    _input['id'] = id
    variables['input'] = _input
    return (await aexecute(UpdateDatasetMutation, variables, rath=rath)).update_dataset

def update_dataset(name: str, id: IDCoercible, parent: Union[Optional[IDCoercible], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> Dataset:
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
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    _input['name'] = name
    if parent is not UNSET:
        _input['parent'] = parent
    _input['id'] = id
    variables['input'] = _input
    return execute(UpdateDatasetMutation, variables, rath=rath).update_dataset

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
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    _input['id'] = id
    _input['historyId'] = history_id
    variables['input'] = _input
    return (await aexecute(RevertDatasetMutation, variables, rath=rath)).revert_dataset

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
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    _input['id'] = id
    _input['historyId'] = history_id
    variables['input'] = _input
    return execute(RevertDatasetMutation, variables, rath=rath).revert_dataset

async def acreate_era(name: str, begin: Union[Optional[datetime], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> CreateEraMutationCreateera:
    """CreateEra 

Create a new era for temporal organization

Args:
    name: The name of the era
    begin: The datetime at which the era begins
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    CreateEraMutationCreateera
"""
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    _input['name'] = name
    if begin is not UNSET:
        _input['begin'] = begin
    variables['input'] = _input
    return (await aexecute(CreateEraMutation, variables, rath=rath)).create_era

def create_era(name: str, begin: Union[Optional[datetime], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> CreateEraMutationCreateera:
    """CreateEra 

Create a new era for temporal organization

Args:
    name: The name of the era
    begin: The datetime at which the era begins
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    CreateEraMutationCreateera
"""
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    _input['name'] = name
    if begin is not UNSET:
        _input['begin'] = begin
    variables['input'] = _input
    return execute(CreateEraMutation, variables, rath=rath).create_era

async def afrom_file_like(file: ImageFileCoercible, file_name: str, dataset: Union[Optional[IDCoercible], UnsetType]=UNSET, origins: Union[Optional[Iterable[IDCoercible]], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> File:
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
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    _input['file'] = file
    _input['fileName'] = file_name
    if dataset is not UNSET:
        _input['dataset'] = dataset
    if origins is not UNSET:
        _input['origins'] = origins
    variables['input'] = _input
    return (await aexecute(FromFileLikeMutation, variables, rath=rath)).from_file_like

def from_file_like(file: ImageFileCoercible, file_name: str, dataset: Union[Optional[IDCoercible], UnsetType]=UNSET, origins: Union[Optional[Iterable[IDCoercible]], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> File:
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
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    _input['file'] = file
    _input['fileName'] = file_name
    if dataset is not UNSET:
        _input['dataset'] = dataset
    if origins is not UNSET:
        _input['origins'] = origins
    variables['input'] = _input
    return execute(FromFileLikeMutation, variables, rath=rath).from_file_like

async def afrom_array_like(array: ImageCoercible, name: str, dataset: Union[Optional[IDCoercible], UnsetType]=UNSET, channel_views: Union[Optional[Iterable[PartialChannelViewInput]], UnsetType]=UNSET, transformation_views: Union[Optional[Iterable[PartialAffineTransformationViewInput]], UnsetType]=UNSET, acquisition_views: Union[Optional[Iterable[PartialAcquisitionViewInput]], UnsetType]=UNSET, mask_views: Union[Optional[Iterable[PartialMaskViewInput]], UnsetType]=UNSET, reference_views: Union[Optional[Iterable[PartialReferenceViewInput]], UnsetType]=UNSET, instance_mask_views: Union[Optional[Iterable[PartialInstanceMaskViewInput]], UnsetType]=UNSET, rgb_views: Union[Optional[Iterable[PartialRGBViewInput]], UnsetType]=UNSET, timepoint_views: Union[Optional[Iterable[PartialTimepointViewInput]], UnsetType]=UNSET, optics_views: Union[Optional[Iterable[PartialOpticsViewInput]], UnsetType]=UNSET, scale_views: Union[Optional[Iterable[PartialScaleViewInput]], UnsetType]=UNSET, tags: Union[Optional[Iterable[str]], UnsetType]=UNSET, roi_views: Union[Optional[Iterable[PartialROIViewInput]], UnsetType]=UNSET, file_views: Union[Optional[Iterable[PartialFileViewInput]], UnsetType]=UNSET, derived_views: Union[Optional[Iterable[PartialDerivedViewInput]], UnsetType]=UNSET, lightpath_views: Union[Optional[Iterable[PartialLightpathViewInput]], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> Image:
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
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    _input['array'] = array
    _input['name'] = name
    if dataset is not UNSET:
        _input['dataset'] = dataset
    if channel_views is not UNSET:
        _input['channelViews'] = channel_views
    if transformation_views is not UNSET:
        _input['transformationViews'] = transformation_views
    if acquisition_views is not UNSET:
        _input['acquisitionViews'] = acquisition_views
    if mask_views is not UNSET:
        _input['maskViews'] = mask_views
    if reference_views is not UNSET:
        _input['referenceViews'] = reference_views
    if instance_mask_views is not UNSET:
        _input['instanceMaskViews'] = instance_mask_views
    if rgb_views is not UNSET:
        _input['rgbViews'] = rgb_views
    if timepoint_views is not UNSET:
        _input['timepointViews'] = timepoint_views
    if optics_views is not UNSET:
        _input['opticsViews'] = optics_views
    if scale_views is not UNSET:
        _input['scaleViews'] = scale_views
    if tags is not UNSET:
        _input['tags'] = tags
    if roi_views is not UNSET:
        _input['roiViews'] = roi_views
    if file_views is not UNSET:
        _input['fileViews'] = file_views
    if derived_views is not UNSET:
        _input['derivedViews'] = derived_views
    if lightpath_views is not UNSET:
        _input['lightpathViews'] = lightpath_views
    variables['input'] = _input
    return (await aexecute(From_array_likeMutation, variables, rath=rath)).from_array_like

def from_array_like(array: ImageCoercible, name: str, dataset: Union[Optional[IDCoercible], UnsetType]=UNSET, channel_views: Union[Optional[Iterable[PartialChannelViewInput]], UnsetType]=UNSET, transformation_views: Union[Optional[Iterable[PartialAffineTransformationViewInput]], UnsetType]=UNSET, acquisition_views: Union[Optional[Iterable[PartialAcquisitionViewInput]], UnsetType]=UNSET, mask_views: Union[Optional[Iterable[PartialMaskViewInput]], UnsetType]=UNSET, reference_views: Union[Optional[Iterable[PartialReferenceViewInput]], UnsetType]=UNSET, instance_mask_views: Union[Optional[Iterable[PartialInstanceMaskViewInput]], UnsetType]=UNSET, rgb_views: Union[Optional[Iterable[PartialRGBViewInput]], UnsetType]=UNSET, timepoint_views: Union[Optional[Iterable[PartialTimepointViewInput]], UnsetType]=UNSET, optics_views: Union[Optional[Iterable[PartialOpticsViewInput]], UnsetType]=UNSET, scale_views: Union[Optional[Iterable[PartialScaleViewInput]], UnsetType]=UNSET, tags: Union[Optional[Iterable[str]], UnsetType]=UNSET, roi_views: Union[Optional[Iterable[PartialROIViewInput]], UnsetType]=UNSET, file_views: Union[Optional[Iterable[PartialFileViewInput]], UnsetType]=UNSET, derived_views: Union[Optional[Iterable[PartialDerivedViewInput]], UnsetType]=UNSET, lightpath_views: Union[Optional[Iterable[PartialLightpathViewInput]], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> Image:
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
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    _input['array'] = array
    _input['name'] = name
    if dataset is not UNSET:
        _input['dataset'] = dataset
    if channel_views is not UNSET:
        _input['channelViews'] = channel_views
    if transformation_views is not UNSET:
        _input['transformationViews'] = transformation_views
    if acquisition_views is not UNSET:
        _input['acquisitionViews'] = acquisition_views
    if mask_views is not UNSET:
        _input['maskViews'] = mask_views
    if reference_views is not UNSET:
        _input['referenceViews'] = reference_views
    if instance_mask_views is not UNSET:
        _input['instanceMaskViews'] = instance_mask_views
    if rgb_views is not UNSET:
        _input['rgbViews'] = rgb_views
    if timepoint_views is not UNSET:
        _input['timepointViews'] = timepoint_views
    if optics_views is not UNSET:
        _input['opticsViews'] = optics_views
    if scale_views is not UNSET:
        _input['scaleViews'] = scale_views
    if tags is not UNSET:
        _input['tags'] = tags
    if roi_views is not UNSET:
        _input['roiViews'] = roi_views
    if file_views is not UNSET:
        _input['fileViews'] = file_views
    if derived_views is not UNSET:
        _input['derivedViews'] = derived_views
    if lightpath_views is not UNSET:
        _input['lightpathViews'] = lightpath_views
    variables['input'] = _input
    return execute(From_array_likeMutation, variables, rath=rath).from_array_like

async def aupdate_image(id: IDCoercible, tags: Union[Optional[Iterable[str]], UnsetType]=UNSET, name: Union[Optional[str], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> Image:
    """UpdateImage 

Update an existing image's metadata

Args:
    id: The ID of the image to update
    tags: Tags to add to the image
    name: The new name of the image
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    Image
"""
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    _input['id'] = id
    if tags is not UNSET:
        _input['tags'] = tags
    if name is not UNSET:
        _input['name'] = name
    variables['input'] = _input
    return (await aexecute(UpdateImageMutation, variables, rath=rath)).update_image

def update_image(id: IDCoercible, tags: Union[Optional[Iterable[str]], UnsetType]=UNSET, name: Union[Optional[str], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> Image:
    """UpdateImage 

Update an existing image's metadata

Args:
    id: The ID of the image to update
    tags: Tags to add to the image
    name: The new name of the image
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    Image
"""
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    _input['id'] = id
    if tags is not UNSET:
        _input['tags'] = tags
    if name is not UNSET:
        _input['name'] = name
    variables['input'] = _input
    return execute(UpdateImageMutation, variables, rath=rath).update_image

async def acreate_instrument(serial_number: str, manufacturer: Union[Optional[str], UnsetType]=UNSET, name: Union[Optional[str], UnsetType]=UNSET, model: Union[Optional[str], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> CreateInstrumentMutationCreateinstrument:
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
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    _input['serialNumber'] = serial_number
    if manufacturer is not UNSET:
        _input['manufacturer'] = manufacturer
    if name is not UNSET:
        _input['name'] = name
    if model is not UNSET:
        _input['model'] = model
    variables['input'] = _input
    return (await aexecute(CreateInstrumentMutation, variables, rath=rath)).create_instrument

def create_instrument(serial_number: str, manufacturer: Union[Optional[str], UnsetType]=UNSET, name: Union[Optional[str], UnsetType]=UNSET, model: Union[Optional[str], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> CreateInstrumentMutationCreateinstrument:
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
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    _input['serialNumber'] = serial_number
    if manufacturer is not UNSET:
        _input['manufacturer'] = manufacturer
    if name is not UNSET:
        _input['name'] = name
    if model is not UNSET:
        _input['model'] = model
    variables['input'] = _input
    return execute(CreateInstrumentMutation, variables, rath=rath).create_instrument

async def aensure_instrument(serial_number: str, manufacturer: Union[Optional[str], UnsetType]=UNSET, name: Union[Optional[str], UnsetType]=UNSET, model: Union[Optional[str], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> EnsureInstrumentMutationEnsureinstrument:
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
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    _input['serialNumber'] = serial_number
    if manufacturer is not UNSET:
        _input['manufacturer'] = manufacturer
    if name is not UNSET:
        _input['name'] = name
    if model is not UNSET:
        _input['model'] = model
    variables['input'] = _input
    return (await aexecute(EnsureInstrumentMutation, variables, rath=rath)).ensure_instrument

def ensure_instrument(serial_number: str, manufacturer: Union[Optional[str], UnsetType]=UNSET, name: Union[Optional[str], UnsetType]=UNSET, model: Union[Optional[str], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> EnsureInstrumentMutationEnsureinstrument:
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
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    _input['serialNumber'] = serial_number
    if manufacturer is not UNSET:
        _input['manufacturer'] = manufacturer
    if name is not UNSET:
        _input['name'] = name
    if model is not UNSET:
        _input['model'] = model
    variables['input'] = _input
    return execute(EnsureInstrumentMutation, variables, rath=rath).ensure_instrument

async def acreate_layer(lens: IDCoercible, scene: IDCoercible, render_graph: LayerRenderGraphInput, blending: Union[Optional[Blending], UnsetType]=UNSET, opacity: Union[Optional[float], UnsetType]=UNSET, visible: Union[Optional[bool], UnsetType]=UNSET, order: Union[Optional[int], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> LayerImageLayer:
    """CreateLayer 

Create a new layer from an existing lens with optional affine transformation and colormap settings

Args:
    lens: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID. (required)
    scene: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID. (required)
    blending: Blending
    opacity: The `Float` scalar type represents signed double-precision fractional values as specified by [IEEE 754](https://en.wikipedia.org/wiki/IEEE_floating_point).
    visible: The `Boolean` scalar type represents `true` or `false`.
    order: The `Int` scalar type represents non-fractional signed whole numeric values. Int can represent values between -(2^31) and 2^31 - 1.
    render_graph: The composable render recipe inside a single layer, rooted at a blend node (required)
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    LayerImageLayer
"""
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    _input['lens'] = lens
    _input['scene'] = scene
    if blending is not UNSET:
        _input['blending'] = blending
    if opacity is not UNSET:
        _input['opacity'] = opacity
    if visible is not UNSET:
        _input['visible'] = visible
    if order is not UNSET:
        _input['order'] = order
    _input['renderGraph'] = render_graph
    variables['input'] = _input
    return (await aexecute(CreateLayerMutation, variables, rath=rath)).create_layer

def create_layer(lens: IDCoercible, scene: IDCoercible, render_graph: LayerRenderGraphInput, blending: Union[Optional[Blending], UnsetType]=UNSET, opacity: Union[Optional[float], UnsetType]=UNSET, visible: Union[Optional[bool], UnsetType]=UNSET, order: Union[Optional[int], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> LayerImageLayer:
    """CreateLayer 

Create a new layer from an existing lens with optional affine transformation and colormap settings

Args:
    lens: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID. (required)
    scene: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID. (required)
    blending: Blending
    opacity: The `Float` scalar type represents signed double-precision fractional values as specified by [IEEE 754](https://en.wikipedia.org/wiki/IEEE_floating_point).
    visible: The `Boolean` scalar type represents `true` or `false`.
    order: The `Int` scalar type represents non-fractional signed whole numeric values. Int can represent values between -(2^31) and 2^31 - 1.
    render_graph: The composable render recipe inside a single layer, rooted at a blend node (required)
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    LayerImageLayer
"""
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    _input['lens'] = lens
    _input['scene'] = scene
    if blending is not UNSET:
        _input['blending'] = blending
    if opacity is not UNSET:
        _input['opacity'] = opacity
    if visible is not UNSET:
        _input['visible'] = visible
    if order is not UNSET:
        _input['order'] = order
    _input['renderGraph'] = render_graph
    variables['input'] = _input
    return execute(CreateLayerMutation, variables, rath=rath).create_layer

async def acreate_lens(dataset: IDCoercible, slices: Iterable[SliceInput], rath: Optional[MikroNextRath]=None) -> Lens:
    """CreateLens 

Create a new lens from an existing dataset and slicing constraints

Args:
    dataset: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID. (required)
    slices: Input type for a slice along one axis of a dataset (required) (list) (required)
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    Lens
"""
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    _input['dataset'] = dataset
    _input['slices'] = slices
    variables['input'] = _input
    return (await aexecute(CreateLensMutation, variables, rath=rath)).create_lens

def create_lens(dataset: IDCoercible, slices: Iterable[SliceInput], rath: Optional[MikroNextRath]=None) -> Lens:
    """CreateLens 

Create a new lens from an existing dataset and slicing constraints

Args:
    dataset: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID. (required)
    slices: Input type for a slice along one axis of a dataset (required) (list) (required)
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    Lens
"""
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    _input['dataset'] = dataset
    _input['slices'] = slices
    variables['input'] = _input
    return execute(CreateLensMutation, variables, rath=rath).create_lens

async def acreate_mesh_collection(version: str, spec_version: str, catalog: ParquetCoercible, axes: Iterable[Union[AxisInput, str]], geometry: Union[Optional[Iterable[ParquetCoercible]], UnsetType]=UNSET, derived_from: Union[Optional[Iterable[DerivedFromInput]], UnsetType]=UNSET, grid: Union[Optional[Any], UnsetType]=UNSET, encoding: Union[Optional[Any], UnsetType]=UNSET, provenance_metadata: Union[Optional[Any], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> MeshCollection:
    """CreateMeshCollection 

Register an immutable, versioned mesh collection against a coordinate system

Args:
    version: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text. (required)
    spec_version: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text. (required)
    catalog: The `ParquetLike` scalar type represents a reference to a parquet objected stored previously created by the user on a datalayer (required)
    geometry: The `ParquetLike` scalar type represents a reference to a parquet objected stored previously created by the user on a datalayer (required) (list)
    axes: Input type for one structural axis of a dataset's pixel grid: its name and its semantic kind. Units and spacings do not belong here -- they belong to a physical space, a separate coordinate system plus one edge (required) (list) (required)
    derived_from: Where this data came from, as a discriminated union: `kind` selects which sort of source is being named, and only that member's id field is read -- any other is rejected. The member inputs annotated `@unionElementOf(union: "DerivedFromInput")` say which field each kind reads. Direction is always this data -> its source (required) (list)
    grid: The `Any` scalar any type
    encoding: The `Any` scalar any type
    provenance_metadata: The `Any` scalar any type
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    MeshCollection
"""
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    _input['version'] = version
    _input['specVersion'] = spec_version
    _input['catalog'] = catalog
    if geometry is not UNSET:
        _input['geometry'] = geometry
    _input['axes'] = axes
    if derived_from is not UNSET:
        _input['derivedFrom'] = derived_from
    if grid is not UNSET:
        _input['grid'] = grid
    if encoding is not UNSET:
        _input['encoding'] = encoding
    if provenance_metadata is not UNSET:
        _input['provenanceMetadata'] = provenance_metadata
    variables['input'] = _input
    return (await aexecute(CreateMeshCollectionMutation, variables, rath=rath)).create_mesh_collection

def create_mesh_collection(version: str, spec_version: str, catalog: ParquetCoercible, axes: Iterable[Union[AxisInput, str]], geometry: Union[Optional[Iterable[ParquetCoercible]], UnsetType]=UNSET, derived_from: Union[Optional[Iterable[DerivedFromInput]], UnsetType]=UNSET, grid: Union[Optional[Any], UnsetType]=UNSET, encoding: Union[Optional[Any], UnsetType]=UNSET, provenance_metadata: Union[Optional[Any], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> MeshCollection:
    """CreateMeshCollection 

Register an immutable, versioned mesh collection against a coordinate system

Args:
    version: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text. (required)
    spec_version: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text. (required)
    catalog: The `ParquetLike` scalar type represents a reference to a parquet objected stored previously created by the user on a datalayer (required)
    geometry: The `ParquetLike` scalar type represents a reference to a parquet objected stored previously created by the user on a datalayer (required) (list)
    axes: Input type for one structural axis of a dataset's pixel grid: its name and its semantic kind. Units and spacings do not belong here -- they belong to a physical space, a separate coordinate system plus one edge (required) (list) (required)
    derived_from: Where this data came from, as a discriminated union: `kind` selects which sort of source is being named, and only that member's id field is read -- any other is rejected. The member inputs annotated `@unionElementOf(union: "DerivedFromInput")` say which field each kind reads. Direction is always this data -> its source (required) (list)
    grid: The `Any` scalar any type
    encoding: The `Any` scalar any type
    provenance_metadata: The `Any` scalar any type
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    MeshCollection
"""
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    _input['version'] = version
    _input['specVersion'] = spec_version
    _input['catalog'] = catalog
    if geometry is not UNSET:
        _input['geometry'] = geometry
    _input['axes'] = axes
    if derived_from is not UNSET:
        _input['derivedFrom'] = derived_from
    if grid is not UNSET:
        _input['grid'] = grid
    if encoding is not UNSET:
        _input['encoding'] = encoding
    if provenance_metadata is not UNSET:
        _input['provenanceMetadata'] = provenance_metadata
    variables['input'] = _input
    return execute(CreateMeshCollectionMutation, variables, rath=rath).create_mesh_collection

async def adelete_mesh_collection(id: IDCoercible, rath: Optional[MikroNextRath]=None) -> ID:
    """DeleteMeshCollection 

Delete an existing mesh collection

Args:
    id: The ID of the mesh collection to delete
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    ID
"""
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    _input['id'] = id
    variables['input'] = _input
    return (await aexecute(DeleteMeshCollectionMutation, variables, rath=rath)).delete_mesh_collection

def delete_mesh_collection(id: IDCoercible, rath: Optional[MikroNextRath]=None) -> ID:
    """DeleteMeshCollection 

Delete an existing mesh collection

Args:
    id: The ID of the mesh collection to delete
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    ID
"""
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    _input['id'] = id
    variables['input'] = _input
    return execute(DeleteMeshCollectionMutation, variables, rath=rath).delete_mesh_collection

async def acreate_objective(serial_number: str, name: Union[Optional[str], UnsetType]=UNSET, na: Union[Optional[float], UnsetType]=UNSET, magnification: Union[Optional[float], UnsetType]=UNSET, immersion: Union[Optional[str], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> CreateObjectiveMutationCreateobjective:
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
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    _input['serialNumber'] = serial_number
    if name is not UNSET:
        _input['name'] = name
    if na is not UNSET:
        _input['na'] = na
    if magnification is not UNSET:
        _input['magnification'] = magnification
    if immersion is not UNSET:
        _input['immersion'] = immersion
    variables['input'] = _input
    return (await aexecute(CreateObjectiveMutation, variables, rath=rath)).create_objective

def create_objective(serial_number: str, name: Union[Optional[str], UnsetType]=UNSET, na: Union[Optional[float], UnsetType]=UNSET, magnification: Union[Optional[float], UnsetType]=UNSET, immersion: Union[Optional[str], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> CreateObjectiveMutationCreateobjective:
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
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    _input['serialNumber'] = serial_number
    if name is not UNSET:
        _input['name'] = name
    if na is not UNSET:
        _input['na'] = na
    if magnification is not UNSET:
        _input['magnification'] = magnification
    if immersion is not UNSET:
        _input['immersion'] = immersion
    variables['input'] = _input
    return execute(CreateObjectiveMutation, variables, rath=rath).create_objective

async def aensure_objective(serial_number: str, name: Union[Optional[str], UnsetType]=UNSET, na: Union[Optional[float], UnsetType]=UNSET, magnification: Union[Optional[float], UnsetType]=UNSET, immersion: Union[Optional[str], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> EnsureObjectiveMutationEnsureobjective:
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
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    _input['serialNumber'] = serial_number
    if name is not UNSET:
        _input['name'] = name
    if na is not UNSET:
        _input['na'] = na
    if magnification is not UNSET:
        _input['magnification'] = magnification
    if immersion is not UNSET:
        _input['immersion'] = immersion
    variables['input'] = _input
    return (await aexecute(EnsureObjectiveMutation, variables, rath=rath)).ensure_objective

def ensure_objective(serial_number: str, name: Union[Optional[str], UnsetType]=UNSET, na: Union[Optional[float], UnsetType]=UNSET, magnification: Union[Optional[float], UnsetType]=UNSET, immersion: Union[Optional[str], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> EnsureObjectiveMutationEnsureobjective:
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
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    _input['serialNumber'] = serial_number
    if name is not UNSET:
        _input['name'] = name
    if na is not UNSET:
        _input['na'] = na
    if magnification is not UNSET:
        _input['magnification'] = magnification
    if immersion is not UNSET:
        _input['immersion'] = immersion
    variables['input'] = _input
    return execute(EnsureObjectiveMutation, variables, rath=rath).ensure_objective

async def acreate_phasor_layer(lens: IDCoercible, scene: IDCoercible, phasor_axis: Union[Optional[str], UnsetType]=UNSET, intensity_axis: Union[Optional[str], UnsetType]=UNSET, intensity_index: Union[Optional[int], UnsetType]=UNSET, harmonic: Union[Optional[int], UnsetType]=UNSET, transfer: Union[Optional[PhasorTransferInput], UnsetType]=UNSET, blending: Union[Optional[Blending], UnsetType]=UNSET, opacity: Union[Optional[float], UnsetType]=UNSET, visible: Union[Optional[bool], UnsetType]=UNSET, order: Union[Optional[int], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> LayerImageLayer:
    """CreatePhasorLayer 

Create a layer that reduces one axis of a lens to a phasor and colors each pixel by it: a lifetime overlay over a FLIM (microtime) cube, or a spectral one over a hyperspectral cube

Args:
    lens: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID. (required)
    scene: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID. (required)
    phasor_axis: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.
    intensity_axis: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.
    intensity_index: The `Int` scalar type represents non-fractional signed whole numeric values. Int can represent values between -(2^31) and 2^31 - 1.
    harmonic: The `Int` scalar type represents non-fractional signed whole numeric values. Int can represent values between -(2^31) and 2^31 - 1.
    transfer: How a phasor becomes the pixel's color: the transfer function of a phasor source
    blending: Blending
    opacity: The `Float` scalar type represents signed double-precision fractional values as specified by [IEEE 754](https://en.wikipedia.org/wiki/IEEE_floating_point).
    visible: The `Boolean` scalar type represents `true` or `false`.
    order: The `Int` scalar type represents non-fractional signed whole numeric values. Int can represent values between -(2^31) and 2^31 - 1.
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    LayerImageLayer
"""
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    _input['lens'] = lens
    _input['scene'] = scene
    if phasor_axis is not UNSET:
        _input['phasorAxis'] = phasor_axis
    if intensity_axis is not UNSET:
        _input['intensityAxis'] = intensity_axis
    if intensity_index is not UNSET:
        _input['intensityIndex'] = intensity_index
    if harmonic is not UNSET:
        _input['harmonic'] = harmonic
    if transfer is not UNSET:
        _input['transfer'] = transfer
    if blending is not UNSET:
        _input['blending'] = blending
    if opacity is not UNSET:
        _input['opacity'] = opacity
    if visible is not UNSET:
        _input['visible'] = visible
    if order is not UNSET:
        _input['order'] = order
    variables['input'] = _input
    return (await aexecute(CreatePhasorLayerMutation, variables, rath=rath)).create_phasor_layer

def create_phasor_layer(lens: IDCoercible, scene: IDCoercible, phasor_axis: Union[Optional[str], UnsetType]=UNSET, intensity_axis: Union[Optional[str], UnsetType]=UNSET, intensity_index: Union[Optional[int], UnsetType]=UNSET, harmonic: Union[Optional[int], UnsetType]=UNSET, transfer: Union[Optional[PhasorTransferInput], UnsetType]=UNSET, blending: Union[Optional[Blending], UnsetType]=UNSET, opacity: Union[Optional[float], UnsetType]=UNSET, visible: Union[Optional[bool], UnsetType]=UNSET, order: Union[Optional[int], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> LayerImageLayer:
    """CreatePhasorLayer 

Create a layer that reduces one axis of a lens to a phasor and colors each pixel by it: a lifetime overlay over a FLIM (microtime) cube, or a spectral one over a hyperspectral cube

Args:
    lens: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID. (required)
    scene: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID. (required)
    phasor_axis: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.
    intensity_axis: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.
    intensity_index: The `Int` scalar type represents non-fractional signed whole numeric values. Int can represent values between -(2^31) and 2^31 - 1.
    harmonic: The `Int` scalar type represents non-fractional signed whole numeric values. Int can represent values between -(2^31) and 2^31 - 1.
    transfer: How a phasor becomes the pixel's color: the transfer function of a phasor source
    blending: Blending
    opacity: The `Float` scalar type represents signed double-precision fractional values as specified by [IEEE 754](https://en.wikipedia.org/wiki/IEEE_floating_point).
    visible: The `Boolean` scalar type represents `true` or `false`.
    order: The `Int` scalar type represents non-fractional signed whole numeric values. Int can represent values between -(2^31) and 2^31 - 1.
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    LayerImageLayer
"""
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    _input['lens'] = lens
    _input['scene'] = scene
    if phasor_axis is not UNSET:
        _input['phasorAxis'] = phasor_axis
    if intensity_axis is not UNSET:
        _input['intensityAxis'] = intensity_axis
    if intensity_index is not UNSET:
        _input['intensityIndex'] = intensity_index
    if harmonic is not UNSET:
        _input['harmonic'] = harmonic
    if transfer is not UNSET:
        _input['transfer'] = transfer
    if blending is not UNSET:
        _input['blending'] = blending
    if opacity is not UNSET:
        _input['opacity'] = opacity
    if visible is not UNSET:
        _input['visible'] = visible
    if order is not UNSET:
        _input['order'] = order
    variables['input'] = _input
    return execute(CreatePhasorLayerMutation, variables, rath=rath).create_phasor_layer

async def acreate_phasor_histogram(axis: str, counts: Iterable[float], dataset: IDCoercible, harmonic: Union[Optional[int], UnsetType]=UNSET, bins: Union[Optional[int], UnsetType]=UNSET, g_min: Union[Optional[float], UnsetType]=UNSET, g_max: Union[Optional[float], UnsetType]=UNSET, s_min: Union[Optional[float], UnsetType]=UNSET, s_max: Union[Optional[float], UnsetType]=UNSET, total: Union[Optional[int], UnsetType]=UNSET, calibrated: Union[Optional[bool], UnsetType]=UNSET, profile: Union[Optional[Iterable[float]], UnsetType]=UNSET, axis_anchors: Union[Optional[Iterable[AxisAnchorInput]], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> PhasorHistogram:
    """CreatePhasorHistogram 

Attach a phasor distribution (the 2D g/s density at one axis and harmonic) to a dataset, so a client can range a phasor overlay without reading the cube

Args:
    axis: The axis the phasor was taken over
    counts: The flattened bins x bins density
    harmonic: The harmonic the phasor was taken at
    bins: The resolution of the square (g, s) density grid
    g_min: The `Float` scalar type represents signed double-precision fractional values as specified by [IEEE 754](https://en.wikipedia.org/wiki/IEEE_floating_point).
    g_max: The `Float` scalar type represents signed double-precision fractional values as specified by [IEEE 754](https://en.wikipedia.org/wiki/IEEE_floating_point).
    s_min: The `Float` scalar type represents signed double-precision fractional values as specified by [IEEE 754](https://en.wikipedia.org/wiki/IEEE_floating_point).
    s_max: The `Float` scalar type represents signed double-precision fractional values as specified by [IEEE 754](https://en.wikipedia.org/wiki/IEEE_floating_point).
    total: The `Int` scalar type represents non-fractional signed whole numeric values. Int can represent values between -(2^31) and 2^31 - 1.
    calibrated: The `Boolean` scalar type represents `true` or `false`.
    profile: The `Float` scalar type represents signed double-precision fractional values as specified by [IEEE 754](https://en.wikipedia.org/wiki/IEEE_floating_point). (required) (list)
    dataset: The ID of the dataset the phasor was computed from
    axis_anchors: The coordinates the distribution is pinned to
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    PhasorHistogram
"""
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    _input['axis'] = axis
    _input['counts'] = counts
    if harmonic is not UNSET:
        _input['harmonic'] = harmonic
    if bins is not UNSET:
        _input['bins'] = bins
    if g_min is not UNSET:
        _input['gMin'] = g_min
    if g_max is not UNSET:
        _input['gMax'] = g_max
    if s_min is not UNSET:
        _input['sMin'] = s_min
    if s_max is not UNSET:
        _input['sMax'] = s_max
    if total is not UNSET:
        _input['total'] = total
    if calibrated is not UNSET:
        _input['calibrated'] = calibrated
    if profile is not UNSET:
        _input['profile'] = profile
    _input['dataset'] = dataset
    if axis_anchors is not UNSET:
        _input['axisAnchors'] = axis_anchors
    variables['input'] = _input
    return (await aexecute(CreatePhasorHistogramMutation, variables, rath=rath)).create_phasor_histogram

def create_phasor_histogram(axis: str, counts: Iterable[float], dataset: IDCoercible, harmonic: Union[Optional[int], UnsetType]=UNSET, bins: Union[Optional[int], UnsetType]=UNSET, g_min: Union[Optional[float], UnsetType]=UNSET, g_max: Union[Optional[float], UnsetType]=UNSET, s_min: Union[Optional[float], UnsetType]=UNSET, s_max: Union[Optional[float], UnsetType]=UNSET, total: Union[Optional[int], UnsetType]=UNSET, calibrated: Union[Optional[bool], UnsetType]=UNSET, profile: Union[Optional[Iterable[float]], UnsetType]=UNSET, axis_anchors: Union[Optional[Iterable[AxisAnchorInput]], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> PhasorHistogram:
    """CreatePhasorHistogram 

Attach a phasor distribution (the 2D g/s density at one axis and harmonic) to a dataset, so a client can range a phasor overlay without reading the cube

Args:
    axis: The axis the phasor was taken over
    counts: The flattened bins x bins density
    harmonic: The harmonic the phasor was taken at
    bins: The resolution of the square (g, s) density grid
    g_min: The `Float` scalar type represents signed double-precision fractional values as specified by [IEEE 754](https://en.wikipedia.org/wiki/IEEE_floating_point).
    g_max: The `Float` scalar type represents signed double-precision fractional values as specified by [IEEE 754](https://en.wikipedia.org/wiki/IEEE_floating_point).
    s_min: The `Float` scalar type represents signed double-precision fractional values as specified by [IEEE 754](https://en.wikipedia.org/wiki/IEEE_floating_point).
    s_max: The `Float` scalar type represents signed double-precision fractional values as specified by [IEEE 754](https://en.wikipedia.org/wiki/IEEE_floating_point).
    total: The `Int` scalar type represents non-fractional signed whole numeric values. Int can represent values between -(2^31) and 2^31 - 1.
    calibrated: The `Boolean` scalar type represents `true` or `false`.
    profile: The `Float` scalar type represents signed double-precision fractional values as specified by [IEEE 754](https://en.wikipedia.org/wiki/IEEE_floating_point). (required) (list)
    dataset: The ID of the dataset the phasor was computed from
    axis_anchors: The coordinates the distribution is pinned to
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    PhasorHistogram
"""
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    _input['axis'] = axis
    _input['counts'] = counts
    if harmonic is not UNSET:
        _input['harmonic'] = harmonic
    if bins is not UNSET:
        _input['bins'] = bins
    if g_min is not UNSET:
        _input['gMin'] = g_min
    if g_max is not UNSET:
        _input['gMax'] = g_max
    if s_min is not UNSET:
        _input['sMin'] = s_min
    if s_max is not UNSET:
        _input['sMax'] = s_max
    if total is not UNSET:
        _input['total'] = total
    if calibrated is not UNSET:
        _input['calibrated'] = calibrated
    if profile is not UNSET:
        _input['profile'] = profile
    _input['dataset'] = dataset
    if axis_anchors is not UNSET:
        _input['axisAnchors'] = axis_anchors
    variables['input'] = _input
    return execute(CreatePhasorHistogramMutation, variables, rath=rath).create_phasor_histogram

async def acreate_phasor_calibration(axis: str, dataset: IDCoercible, harmonic: Union[Optional[int], UnsetType]=UNSET, phase_offset: Union[Optional[float], UnsetType]=UNSET, modulation_factor: Union[Optional[float], UnsetType]=UNSET, reference: Union[Optional[str], UnsetType]=UNSET, axis_anchors: Union[Optional[Iterable[AxisAnchorInput]], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> PhasorCalibration:
    """CreatePhasorCalibration 

Attach an instrument-response correction to a dataset, taking a raw phasor to a calibrated one

Args:
    axis: The axis the correction applies to
    harmonic: The harmonic the correction applies at
    phase_offset: The phase correction in radians
    modulation_factor: The modulation correction
    reference: What the correction was measured against
    dataset: The ID of the dataset the correction applies to
    axis_anchors: The coordinates the correction is pinned to
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    PhasorCalibration
"""
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    _input['axis'] = axis
    if harmonic is not UNSET:
        _input['harmonic'] = harmonic
    if phase_offset is not UNSET:
        _input['phaseOffset'] = phase_offset
    if modulation_factor is not UNSET:
        _input['modulationFactor'] = modulation_factor
    if reference is not UNSET:
        _input['reference'] = reference
    _input['dataset'] = dataset
    if axis_anchors is not UNSET:
        _input['axisAnchors'] = axis_anchors
    variables['input'] = _input
    return (await aexecute(CreatePhasorCalibrationMutation, variables, rath=rath)).create_phasor_calibration

def create_phasor_calibration(axis: str, dataset: IDCoercible, harmonic: Union[Optional[int], UnsetType]=UNSET, phase_offset: Union[Optional[float], UnsetType]=UNSET, modulation_factor: Union[Optional[float], UnsetType]=UNSET, reference: Union[Optional[str], UnsetType]=UNSET, axis_anchors: Union[Optional[Iterable[AxisAnchorInput]], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> PhasorCalibration:
    """CreatePhasorCalibration 

Attach an instrument-response correction to a dataset, taking a raw phasor to a calibrated one

Args:
    axis: The axis the correction applies to
    harmonic: The harmonic the correction applies at
    phase_offset: The phase correction in radians
    modulation_factor: The modulation correction
    reference: What the correction was measured against
    dataset: The ID of the dataset the correction applies to
    axis_anchors: The coordinates the correction is pinned to
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    PhasorCalibration
"""
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    _input['axis'] = axis
    if harmonic is not UNSET:
        _input['harmonic'] = harmonic
    if phase_offset is not UNSET:
        _input['phaseOffset'] = phase_offset
    if modulation_factor is not UNSET:
        _input['modulationFactor'] = modulation_factor
    if reference is not UNSET:
        _input['reference'] = reference
    _input['dataset'] = dataset
    if axis_anchors is not UNSET:
        _input['axisAnchors'] = axis_anchors
    variables['input'] = _input
    return execute(CreatePhasorCalibrationMutation, variables, rath=rath).create_phasor_calibration

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
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    _input['tree'] = tree
    _input['name'] = name
    variables['input'] = _input
    return (await aexecute(CreateRenderTreeMutation, variables, rath=rath)).create_render_tree

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
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    _input['tree'] = tree
    _input['name'] = name
    variables['input'] = _input
    return execute(CreateRenderTreeMutation, variables, rath=rath).create_render_tree

async def acreate_rgb_context(image: IDCoercible, name: Union[Optional[str], UnsetType]=UNSET, thumbnail: Union[Optional[IDCoercible], UnsetType]=UNSET, views: Union[Optional[Iterable[PartialRGBViewInput]], UnsetType]=UNSET, z: Union[Optional[int], UnsetType]=UNSET, t: Union[Optional[int], UnsetType]=UNSET, c: Union[Optional[int], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> RGBContext:
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
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    if name is not UNSET:
        _input['name'] = name
    if thumbnail is not UNSET:
        _input['thumbnail'] = thumbnail
    _input['image'] = image
    if views is not UNSET:
        _input['views'] = views
    if z is not UNSET:
        _input['z'] = z
    if t is not UNSET:
        _input['t'] = t
    if c is not UNSET:
        _input['c'] = c
    variables['input'] = _input
    return (await aexecute(CreateRGBContextMutation, variables, rath=rath)).create_rgb_context

def create_rgb_context(image: IDCoercible, name: Union[Optional[str], UnsetType]=UNSET, thumbnail: Union[Optional[IDCoercible], UnsetType]=UNSET, views: Union[Optional[Iterable[PartialRGBViewInput]], UnsetType]=UNSET, z: Union[Optional[int], UnsetType]=UNSET, t: Union[Optional[int], UnsetType]=UNSET, c: Union[Optional[int], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> RGBContext:
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
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    if name is not UNSET:
        _input['name'] = name
    if thumbnail is not UNSET:
        _input['thumbnail'] = thumbnail
    _input['image'] = image
    if views is not UNSET:
        _input['views'] = views
    if z is not UNSET:
        _input['z'] = z
    if t is not UNSET:
        _input['t'] = t
    if c is not UNSET:
        _input['c'] = c
    variables['input'] = _input
    return execute(CreateRGBContextMutation, variables, rath=rath).create_rgb_context

async def aupdate_rgb_context(id: IDCoercible, name: Union[Optional[str], UnsetType]=UNSET, thumbnail: Union[Optional[IDCoercible], UnsetType]=UNSET, views: Union[Optional[Iterable[PartialRGBViewInput]], UnsetType]=UNSET, z: Union[Optional[int], UnsetType]=UNSET, t: Union[Optional[int], UnsetType]=UNSET, c: Union[Optional[int], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> RGBContext:
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
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    _input['id'] = id
    if name is not UNSET:
        _input['name'] = name
    if thumbnail is not UNSET:
        _input['thumbnail'] = thumbnail
    if views is not UNSET:
        _input['views'] = views
    if z is not UNSET:
        _input['z'] = z
    if t is not UNSET:
        _input['t'] = t
    if c is not UNSET:
        _input['c'] = c
    variables['input'] = _input
    return (await aexecute(UpdateRGBContextMutation, variables, rath=rath)).update_rgb_context

def update_rgb_context(id: IDCoercible, name: Union[Optional[str], UnsetType]=UNSET, thumbnail: Union[Optional[IDCoercible], UnsetType]=UNSET, views: Union[Optional[Iterable[PartialRGBViewInput]], UnsetType]=UNSET, z: Union[Optional[int], UnsetType]=UNSET, t: Union[Optional[int], UnsetType]=UNSET, c: Union[Optional[int], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> RGBContext:
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
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    _input['id'] = id
    if name is not UNSET:
        _input['name'] = name
    if thumbnail is not UNSET:
        _input['thumbnail'] = thumbnail
    if views is not UNSET:
        _input['views'] = views
    if z is not UNSET:
        _input['z'] = z
    if t is not UNSET:
        _input['t'] = t
    if c is not UNSET:
        _input['c'] = c
    variables['input'] = _input
    return execute(UpdateRGBContextMutation, variables, rath=rath).update_rgb_context

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
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    _input['image'] = image
    _input['vectors'] = vectors
    _input['kind'] = kind
    variables['input'] = _input
    return (await aexecute(CreateRoiMutation, variables, rath=rath)).create_roi

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
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    _input['image'] = image
    _input['vectors'] = vectors
    _input['kind'] = kind
    variables['input'] = _input
    return execute(CreateRoiMutation, variables, rath=rath).create_roi

async def adelete_roi(id: IDCoercible, rath: Optional[MikroNextRath]=None) -> ID:
    """DeleteRoi 

Delete an existing region of interest

Args:
    id: The ID of the ROI to delete
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    ID
"""
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    _input['id'] = id
    variables['input'] = _input
    return (await aexecute(DeleteRoiMutation, variables, rath=rath)).delete_roi

def delete_roi(id: IDCoercible, rath: Optional[MikroNextRath]=None) -> ID:
    """DeleteRoi 

Delete an existing region of interest

Args:
    id: The ID of the ROI to delete
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    ID
"""
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    _input['id'] = id
    variables['input'] = _input
    return execute(DeleteRoiMutation, variables, rath=rath).delete_roi

async def aupdate_roi(roi: IDCoercible, vectors: Union[Optional[Iterable[FiveDVector]], UnsetType]=UNSET, kind: Union[Optional[RoiKind], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> ROI:
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
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    _input['roi'] = roi
    if vectors is not UNSET:
        _input['vectors'] = vectors
    if kind is not UNSET:
        _input['kind'] = kind
    variables['input'] = _input
    return (await aexecute(UpdateRoiMutation, variables, rath=rath)).update_roi

def update_roi(roi: IDCoercible, vectors: Union[Optional[Iterable[FiveDVector]], UnsetType]=UNSET, kind: Union[Optional[RoiKind], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> ROI:
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
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    _input['roi'] = roi
    if vectors is not UNSET:
        _input['vectors'] = vectors
    if kind is not UNSET:
        _input['kind'] = kind
    variables['input'] = _input
    return execute(UpdateRoiMutation, variables, rath=rath).update_roi

async def acreate_scene(name: str, blending: Union[Optional[Blending], UnsetType]=UNSET, preferred_view: Union[Optional[PreferredView], UnsetType]=UNSET, background_color: Union[Optional[Iterable[float]], UnsetType]=UNSET, axes: Union[Optional[Iterable[PhysicalAxisInput]], UnsetType]=UNSET, epoch: Union[Optional[datetime], UnsetType]=UNSET, coordinate_system: Union[Optional[IDCoercible], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> Scene:
    """CreateScene 

Create a new scene over a world coordinate system: an adopted existing system, or an ordinary SHARED one created for it (never owned by the scene -- it outlives it)

Args:
    name: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text. (required)
    blending: Blending
    preferred_view: PreferredView
    background_color: The `Float` scalar type represents signed double-precision fractional values as specified by [IEEE 754](https://en.wikipedia.org/wiki/IEEE_floating_point). (required) (list)
    axes: Input type for one axis of a unit-carrying coordinate system: its name, its semantic kind and its physical unit (required) (list)
    epoch: Date with time (isoformat)
    coordinate_system: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID.
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    Scene
"""
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    _input['name'] = name
    if blending is not UNSET:
        _input['blending'] = blending
    if preferred_view is not UNSET:
        _input['preferredView'] = preferred_view
    if background_color is not UNSET:
        _input['backgroundColor'] = background_color
    if axes is not UNSET:
        _input['axes'] = axes
    if epoch is not UNSET:
        _input['epoch'] = epoch
    if coordinate_system is not UNSET:
        _input['coordinateSystem'] = coordinate_system
    variables['input'] = _input
    return (await aexecute(CreateSceneMutation, variables, rath=rath)).create_scene

def create_scene(name: str, blending: Union[Optional[Blending], UnsetType]=UNSET, preferred_view: Union[Optional[PreferredView], UnsetType]=UNSET, background_color: Union[Optional[Iterable[float]], UnsetType]=UNSET, axes: Union[Optional[Iterable[PhysicalAxisInput]], UnsetType]=UNSET, epoch: Union[Optional[datetime], UnsetType]=UNSET, coordinate_system: Union[Optional[IDCoercible], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> Scene:
    """CreateScene 

Create a new scene over a world coordinate system: an adopted existing system, or an ordinary SHARED one created for it (never owned by the scene -- it outlives it)

Args:
    name: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text. (required)
    blending: Blending
    preferred_view: PreferredView
    background_color: The `Float` scalar type represents signed double-precision fractional values as specified by [IEEE 754](https://en.wikipedia.org/wiki/IEEE_floating_point). (required) (list)
    axes: Input type for one axis of a unit-carrying coordinate system: its name, its semantic kind and its physical unit (required) (list)
    epoch: Date with time (isoformat)
    coordinate_system: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID.
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    Scene
"""
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    _input['name'] = name
    if blending is not UNSET:
        _input['blending'] = blending
    if preferred_view is not UNSET:
        _input['preferredView'] = preferred_view
    if background_color is not UNSET:
        _input['backgroundColor'] = background_color
    if axes is not UNSET:
        _input['axes'] = axes
    if epoch is not UNSET:
        _input['epoch'] = epoch
    if coordinate_system is not UNSET:
        _input['coordinateSystem'] = coordinate_system
    variables['input'] = _input
    return execute(CreateSceneMutation, variables, rath=rath).create_scene

async def acreate_scene_from_coordinate_system(coordinate_system: IDCoercible, policy: ScenePolicyInput, name: Union[Optional[str], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> Scene:
    """CreateSceneFromCoordinateSystem 

Bootstrap a renderable scene over an existing coordinate system: a shared space (its registered sources become layers, up to the policy's nchildren) or an owned system such as a dataset's intrinsic grid or a physical space (the container's own data becomes the layer). The scene adopts the system as its world; no edges are authored. This is how a dataset is staged -- pass `intrinsicSystem` to render in pixels, or a physical space it is registered into to render at physical scale

Args:
    coordinate_system: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID. (required)
    name: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.
    policy: The policy createSceneFromCoordinateSystem follows: at most `nchildren` layers, materialized from the sources living in or registered into the space, filtered by source kind and drawn by the recipe in `kind` (required)
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    Scene
"""
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    _input['coordinateSystem'] = coordinate_system
    if name is not UNSET:
        _input['name'] = name
    _input['policy'] = policy
    variables['input'] = _input
    return (await aexecute(CreateSceneFromCoordinateSystemMutation, variables, rath=rath)).create_scene_from_coordinate_system

def create_scene_from_coordinate_system(coordinate_system: IDCoercible, policy: ScenePolicyInput, name: Union[Optional[str], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> Scene:
    """CreateSceneFromCoordinateSystem 

Bootstrap a renderable scene over an existing coordinate system: a shared space (its registered sources become layers, up to the policy's nchildren) or an owned system such as a dataset's intrinsic grid or a physical space (the container's own data becomes the layer). The scene adopts the system as its world; no edges are authored. This is how a dataset is staged -- pass `intrinsicSystem` to render in pixels, or a physical space it is registered into to render at physical scale

Args:
    coordinate_system: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID. (required)
    name: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.
    policy: The policy createSceneFromCoordinateSystem follows: at most `nchildren` layers, materialized from the sources living in or registered into the space, filtered by source kind and drawn by the recipe in `kind` (required)
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    Scene
"""
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    _input['coordinateSystem'] = coordinate_system
    if name is not UNSET:
        _input['name'] = name
    _input['policy'] = policy
    variables['input'] = _input
    return execute(CreateSceneFromCoordinateSystemMutation, variables, rath=rath).create_scene_from_coordinate_system

async def aupdate_scene(id: IDCoercible, preferred_view: Union[Optional[PreferredView], UnsetType]=UNSET, background_color: Union[Optional[Iterable[float]], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> Scene:
    """UpdateScene 

Set a scene's viewer preferences: how a client should open it

Args:
    id: The ID of the scene to update
    preferred_view: PreferredView
    background_color: The `Float` scalar type represents signed double-precision fractional values as specified by [IEEE 754](https://en.wikipedia.org/wiki/IEEE_floating_point). (required) (list)
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    Scene
"""
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    _input['id'] = id
    if preferred_view is not UNSET:
        _input['preferredView'] = preferred_view
    if background_color is not UNSET:
        _input['backgroundColor'] = background_color
    variables['input'] = _input
    return (await aexecute(UpdateSceneMutation, variables, rath=rath)).update_scene

def update_scene(id: IDCoercible, preferred_view: Union[Optional[PreferredView], UnsetType]=UNSET, background_color: Union[Optional[Iterable[float]], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> Scene:
    """UpdateScene 

Set a scene's viewer preferences: how a client should open it

Args:
    id: The ID of the scene to update
    preferred_view: PreferredView
    background_color: The `Float` scalar type represents signed double-precision fractional values as specified by [IEEE 754](https://en.wikipedia.org/wiki/IEEE_floating_point). (required) (list)
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    Scene
"""
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    _input['id'] = id
    if preferred_view is not UNSET:
        _input['preferredView'] = preferred_view
    if background_color is not UNSET:
        _input['backgroundColor'] = background_color
    variables['input'] = _input
    return execute(UpdateSceneMutation, variables, rath=rath).update_scene

async def aclear_scene(id: IDCoercible, rath: Optional[MikroNextRath]=None) -> Scene:
    """ClearScene 

Delete every layer of a scene, keeping the scene itself. A pure view-state reset: no coordinate system, registration or dataset is touched, and other scenes over the same space never notice

Args:
    id: The ID of the scene to clear
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    Scene
"""
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    _input['id'] = id
    variables['input'] = _input
    return (await aexecute(ClearSceneMutation, variables, rath=rath)).clear_scene

def clear_scene(id: IDCoercible, rath: Optional[MikroNextRath]=None) -> Scene:
    """ClearScene 

Delete every layer of a scene, keeping the scene itself. A pure view-state reset: no coordinate system, registration or dataset is touched, and other scenes over the same space never notice

Args:
    id: The ID of the scene to clear
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    Scene
"""
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    _input['id'] = id
    variables['input'] = _input
    return execute(ClearSceneMutation, variables, rath=rath).clear_scene

async def adelete_scene(id: IDCoercible, rath: Optional[MikroNextRath]=None) -> ID:
    """DeleteScene 

Delete an existing scene

Args:
    id: The ID of the scene to delete
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    ID
"""
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    _input['id'] = id
    variables['input'] = _input
    return (await aexecute(DeleteSceneMutation, variables, rath=rath)).delete_scene

def delete_scene(id: IDCoercible, rath: Optional[MikroNextRath]=None) -> ID:
    """DeleteScene 

Delete an existing scene

Args:
    id: The ID of the scene to delete
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    ID
"""
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    _input['id'] = id
    variables['input'] = _input
    return execute(DeleteSceneMutation, variables, rath=rath).delete_scene

async def acreate_scene_snapshot(file: ImageFileCoercible, scene: IDCoercible, name: Union[Optional[str], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> SceneSnapshot:
    """CreateSceneSnapshot 

Adopt an uploaded media file as a pre-rendered picture of a scene

Args:
    file: The uploaded media file store containing the rendered image
    scene: The ID of the scene this is a picture of
    name: The name of the snapshot
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    SceneSnapshot
"""
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    _input['file'] = file
    _input['scene'] = scene
    if name is not UNSET:
        _input['name'] = name
    variables['input'] = _input
    return (await aexecute(CreateSceneSnapshotMutation, variables, rath=rath)).create_scene_snapshot

def create_scene_snapshot(file: ImageFileCoercible, scene: IDCoercible, name: Union[Optional[str], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> SceneSnapshot:
    """CreateSceneSnapshot 

Adopt an uploaded media file as a pre-rendered picture of a scene

Args:
    file: The uploaded media file store containing the rendered image
    scene: The ID of the scene this is a picture of
    name: The name of the snapshot
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    SceneSnapshot
"""
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    _input['file'] = file
    _input['scene'] = scene
    if name is not UNSET:
        _input['name'] = name
    variables['input'] = _input
    return execute(CreateSceneSnapshotMutation, variables, rath=rath).create_scene_snapshot

async def adelete_scene_snapshot(id: IDCoercible, rath: Optional[MikroNextRath]=None) -> ID:
    """DeleteSceneSnapshot 

Delete an existing scene snapshot

Args:
    id: The ID of the snapshot to delete
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    ID
"""
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    _input['id'] = id
    variables['input'] = _input
    return (await aexecute(DeleteSceneSnapshotMutation, variables, rath=rath)).delete_scene_snapshot

def delete_scene_snapshot(id: IDCoercible, rath: Optional[MikroNextRath]=None) -> ID:
    """DeleteSceneSnapshot 

Delete an existing scene snapshot

Args:
    id: The ID of the snapshot to delete
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    ID
"""
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    _input['id'] = id
    variables['input'] = _input
    return execute(DeleteSceneSnapshotMutation, variables, rath=rath).delete_scene_snapshot

async def apin_scene_snapshot(id: IDCoercible, pin: bool, rath: Optional[MikroNextRath]=None) -> SceneSnapshot:
    """PinSceneSnapshot 

Pin a scene snapshot for quick access

Args:
    id: The ID of the snapshot to pin or unpin
    pin: True to pin, false to unpin
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    SceneSnapshot
"""
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    _input['id'] = id
    _input['pin'] = pin
    variables['input'] = _input
    return (await aexecute(PinSceneSnapshotMutation, variables, rath=rath)).pin_scene_snapshot

def pin_scene_snapshot(id: IDCoercible, pin: bool, rath: Optional[MikroNextRath]=None) -> SceneSnapshot:
    """PinSceneSnapshot 

Pin a scene snapshot for quick access

Args:
    id: The ID of the snapshot to pin or unpin
    pin: True to pin, false to unpin
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    SceneSnapshot
"""
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    _input['id'] = id
    _input['pin'] = pin
    variables['input'] = _input
    return execute(PinSceneSnapshotMutation, variables, rath=rath).pin_scene_snapshot

async def acreate_snapshot(file: ImageFileCoercible, image: IDCoercible, name: Union[Optional[str], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> Snapshot:
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
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    _input['file'] = file
    _input['image'] = image
    if name is not UNSET:
        _input['name'] = name
    variables['input'] = _input
    return (await aexecute(CreateSnapshotMutation, variables, rath=rath)).create_snapshot

def create_snapshot(file: ImageFileCoercible, image: IDCoercible, name: Union[Optional[str], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> Snapshot:
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
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    _input['file'] = file
    _input['image'] = image
    if name is not UNSET:
        _input['name'] = name
    variables['input'] = _input
    return execute(CreateSnapshotMutation, variables, rath=rath).create_snapshot

async def acreate_stage(name: str, instrument: Union[Optional[IDCoercible], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> Stage:
    """CreateStage 

Create a new stage for organizing data

Args:
    name: The name of the stage
    instrument: The ID of the instrument this stage belongs to
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    Stage
"""
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    _input['name'] = name
    if instrument is not UNSET:
        _input['instrument'] = instrument
    variables['input'] = _input
    return (await aexecute(CreateStageMutation, variables, rath=rath)).create_stage

def create_stage(name: str, instrument: Union[Optional[IDCoercible], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> Stage:
    """CreateStage 

Create a new stage for organizing data

Args:
    name: The name of the stage
    instrument: The ID of the instrument this stage belongs to
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    Stage
"""
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    _input['name'] = name
    if instrument is not UNSET:
        _input['instrument'] = instrument
    variables['input'] = _input
    return execute(CreateStageMutation, variables, rath=rath).create_stage

async def afrom_parquet_like(dataframe: ParquetCoercible, name: str, origins: Union[Optional[Iterable[IDCoercible]], UnsetType]=UNSET, dataset: Union[Optional[IDCoercible], UnsetType]=UNSET, label_accessors: Union[Optional[Iterable[PartialLabelAccessorInput]], UnsetType]=UNSET, image_accessors: Union[Optional[Iterable[PartialImageAccessorInput]], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> Table:
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
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    _input['dataframe'] = dataframe
    _input['name'] = name
    if origins is not UNSET:
        _input['origins'] = origins
    if dataset is not UNSET:
        _input['dataset'] = dataset
    if label_accessors is not UNSET:
        _input['labelAccessors'] = label_accessors
    if image_accessors is not UNSET:
        _input['imageAccessors'] = image_accessors
    variables['input'] = _input
    return (await aexecute(From_parquet_likeMutation, variables, rath=rath)).from_parquet_like

def from_parquet_like(dataframe: ParquetCoercible, name: str, origins: Union[Optional[Iterable[IDCoercible]], UnsetType]=UNSET, dataset: Union[Optional[IDCoercible], UnsetType]=UNSET, label_accessors: Union[Optional[Iterable[PartialLabelAccessorInput]], UnsetType]=UNSET, image_accessors: Union[Optional[Iterable[PartialImageAccessorInput]], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> Table:
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
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    _input['dataframe'] = dataframe
    _input['name'] = name
    if origins is not UNSET:
        _input['origins'] = origins
    if dataset is not UNSET:
        _input['dataset'] = dataset
    if label_accessors is not UNSET:
        _input['labelAccessors'] = label_accessors
    if image_accessors is not UNSET:
        _input['imageAccessors'] = image_accessors
    variables['input'] = _input
    return execute(From_parquet_likeMutation, variables, rath=rath).from_parquet_like

async def acreate_table_dataset(name: str, data: ParquetCoercible, columns: Iterable[TableColumnInput], validate_schema: bool, description: Union[Optional[str], UnsetType]=UNSET, derived_from: Union[Optional[Iterable[DerivedFromInput]], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> TableDataset:
    """CreateTableDataset 

Create a table dataset from a Parquet store. Its declared coordinate columns become the axes of a coordinate system it owns, which lets a localization table be placed in a scene; a table with no coordinate columns is a measurement table whose rows enumerate objects and whose lineage edge is UNMAPPABLE

Args:
    name: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text. (required)
    data: The `ParquetLike` scalar type represents a reference to a parquet objected stored previously created by the user on a datalayer (required)
    columns: One declared column of a table dataset: its name, dtype, and role. A COORDINATE column also carries an axis type and optional unit and becomes an axis of the table's space (required) (list) (required)
    description: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.
    derived_from: Where this data came from, as a discriminated union: `kind` selects which sort of source is being named, and only that member's id field is read -- any other is rejected. The member inputs annotated `@unionElementOf(union: "DerivedFromInput")` say which field each kind reads. Direction is always this data -> its source (required) (list)
    validate_schema: The `Boolean` scalar type represents `true` or `false`. (required)
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    TableDataset
"""
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    _input['name'] = name
    _input['data'] = data
    _input['columns'] = columns
    if description is not UNSET:
        _input['description'] = description
    if derived_from is not UNSET:
        _input['derivedFrom'] = derived_from
    _input['validateSchema'] = validate_schema
    variables['input'] = _input
    return (await aexecute(CreateTableDatasetMutation, variables, rath=rath)).create_table_dataset

def create_table_dataset(name: str, data: ParquetCoercible, columns: Iterable[TableColumnInput], validate_schema: bool, description: Union[Optional[str], UnsetType]=UNSET, derived_from: Union[Optional[Iterable[DerivedFromInput]], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> TableDataset:
    """CreateTableDataset 

Create a table dataset from a Parquet store. Its declared coordinate columns become the axes of a coordinate system it owns, which lets a localization table be placed in a scene; a table with no coordinate columns is a measurement table whose rows enumerate objects and whose lineage edge is UNMAPPABLE

Args:
    name: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text. (required)
    data: The `ParquetLike` scalar type represents a reference to a parquet objected stored previously created by the user on a datalayer (required)
    columns: One declared column of a table dataset: its name, dtype, and role. A COORDINATE column also carries an axis type and optional unit and becomes an axis of the table's space (required) (list) (required)
    description: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.
    derived_from: Where this data came from, as a discriminated union: `kind` selects which sort of source is being named, and only that member's id field is read -- any other is rejected. The member inputs annotated `@unionElementOf(union: "DerivedFromInput")` say which field each kind reads. Direction is always this data -> its source (required) (list)
    validate_schema: The `Boolean` scalar type represents `true` or `false`. (required)
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    TableDataset
"""
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    _input['name'] = name
    _input['data'] = data
    _input['columns'] = columns
    if description is not UNSET:
        _input['description'] = description
    if derived_from is not UNSET:
        _input['derivedFrom'] = derived_from
    _input['validateSchema'] = validate_schema
    variables['input'] = _input
    return execute(CreateTableDatasetMutation, variables, rath=rath).create_table_dataset

async def aupdate_table_dataset(id: IDCoercible, name: Union[Optional[str], UnsetType]=UNSET, description: Union[Optional[str], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> TableDataset:
    """UpdateTableDataset 

Rename a table dataset or redescribe it -- the whole of what is editable. Its store, columns and coordinate system are fixed at creation; a recomputation is a new table

Args:
    id: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID. (required)
    name: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.
    description: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    TableDataset
"""
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    _input['id'] = id
    if name is not UNSET:
        _input['name'] = name
    if description is not UNSET:
        _input['description'] = description
    variables['input'] = _input
    return (await aexecute(UpdateTableDatasetMutation, variables, rath=rath)).update_table_dataset

def update_table_dataset(id: IDCoercible, name: Union[Optional[str], UnsetType]=UNSET, description: Union[Optional[str], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> TableDataset:
    """UpdateTableDataset 

Rename a table dataset or redescribe it -- the whole of what is editable. Its store, columns and coordinate system are fixed at creation; a recomputation is a new table

Args:
    id: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID. (required)
    name: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.
    description: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    TableDataset
"""
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    _input['id'] = id
    if name is not UNSET:
        _input['name'] = name
    if description is not UNSET:
        _input['description'] = description
    variables['input'] = _input
    return execute(UpdateTableDatasetMutation, variables, rath=rath).update_table_dataset

async def adelete_table_dataset(id: IDCoercible, rath: Optional[MikroNextRath]=None) -> ID:
    """DeleteTableDataset 

Delete an existing table dataset

Args:
    id: The ID of the table dataset to delete
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    ID
"""
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    _input['id'] = id
    variables['input'] = _input
    return (await aexecute(DeleteTableDatasetMutation, variables, rath=rath)).delete_table_dataset

def delete_table_dataset(id: IDCoercible, rath: Optional[MikroNextRath]=None) -> ID:
    """DeleteTableDataset 

Delete an existing table dataset

Args:
    id: The ID of the table dataset to delete
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    ID
"""
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    _input['id'] = id
    variables['input'] = _input
    return execute(DeleteTableDatasetMutation, variables, rath=rath).delete_table_dataset

async def acreate_transformation(input: IDCoercible, output: IDCoercible, transform: TransformInput, name: Union[Optional[str], UnsetType]=UNSET, validity: Union[Optional[PlacementValidity], UnsetType]=UNSET, value_relation: Union[Optional[ValueRelation], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> Union[Annotated[Union[CreateTransformationMutationCreatetransformationBaseAffineTransformation, CreateTransformationMutationCreatetransformationBaseBijectionTransformation, CreateTransformationMutationCreatetransformationBaseByDimensionTransformation, CreateTransformationMutationCreatetransformationBaseFieldTransformation, CreateTransformationMutationCreatetransformationBaseIdentityTransformation, CreateTransformationMutationCreatetransformationBaseMapAxisTransformation, CreateTransformationMutationCreatetransformationBaseRotationTransformation, CreateTransformationMutationCreatetransformationBaseScaleTransformation, CreateTransformationMutationCreatetransformationBaseSequenceTransformation, CreateTransformationMutationCreatetransformationBaseTranslationTransformation, CreateTransformationMutationCreatetransformationBaseUnmappableTransformation], Field(discriminator='typename')], CreateTransformationMutationCreatetransformationBaseCatchAll]:
    """CreateTransformation 

Create one edge of the coordinate graph, mapping an input coordinate system to an output one. This is where registration lives

Args:
    input: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID. (required)
    output: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID. (required)
    transform: One edge of the coordinate graph, as a discriminated union: `kind` selects a member, and only that member's fields are read -- any other supplied field is rejected, never dropped. The member inputs annotated `@unionElementOf(union: "TransformInput")` say which fields each kind reads. Direction is always forward, input -> output (required)
    name: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.
    validity: PlacementValidity
    value_relation: ValueRelation
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    Transformation
"""
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    _input['input'] = input
    _input['output'] = output
    _input['transform'] = transform
    if name is not UNSET:
        _input['name'] = name
    if validity is not UNSET:
        _input['validity'] = validity
    if value_relation is not UNSET:
        _input['valueRelation'] = value_relation
    variables['input'] = _input
    return (await aexecute(CreateTransformationMutation, variables, rath=rath)).create_transformation

def create_transformation(input: IDCoercible, output: IDCoercible, transform: TransformInput, name: Union[Optional[str], UnsetType]=UNSET, validity: Union[Optional[PlacementValidity], UnsetType]=UNSET, value_relation: Union[Optional[ValueRelation], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> Union[Annotated[Union[CreateTransformationMutationCreatetransformationBaseAffineTransformation, CreateTransformationMutationCreatetransformationBaseBijectionTransformation, CreateTransformationMutationCreatetransformationBaseByDimensionTransformation, CreateTransformationMutationCreatetransformationBaseFieldTransformation, CreateTransformationMutationCreatetransformationBaseIdentityTransformation, CreateTransformationMutationCreatetransformationBaseMapAxisTransformation, CreateTransformationMutationCreatetransformationBaseRotationTransformation, CreateTransformationMutationCreatetransformationBaseScaleTransformation, CreateTransformationMutationCreatetransformationBaseSequenceTransformation, CreateTransformationMutationCreatetransformationBaseTranslationTransformation, CreateTransformationMutationCreatetransformationBaseUnmappableTransformation], Field(discriminator='typename')], CreateTransformationMutationCreatetransformationBaseCatchAll]:
    """CreateTransformation 

Create one edge of the coordinate graph, mapping an input coordinate system to an output one. This is where registration lives

Args:
    input: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID. (required)
    output: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID. (required)
    transform: One edge of the coordinate graph, as a discriminated union: `kind` selects a member, and only that member's fields are read -- any other supplied field is rejected, never dropped. The member inputs annotated `@unionElementOf(union: "TransformInput")` say which fields each kind reads. Direction is always forward, input -> output (required)
    name: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.
    validity: PlacementValidity
    value_relation: ValueRelation
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    Transformation
"""
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    _input['input'] = input
    _input['output'] = output
    _input['transform'] = transform
    if name is not UNSET:
        _input['name'] = name
    if validity is not UNSET:
        _input['validity'] = validity
    if value_relation is not UNSET:
        _input['valueRelation'] = value_relation
    variables['input'] = _input
    return execute(CreateTransformationMutation, variables, rath=rath).create_transformation

async def aupdate_transformation(id: IDCoercible, name: Union[Optional[str], UnsetType]=UNSET, scale: Union[Optional[Iterable[float]], UnsetType]=UNSET, translation: Union[Optional[Iterable[float]], UnsetType]=UNSET, affine: Union[Optional[Iterable[Iterable[float]]], UnsetType]=UNSET, validity: Union[Optional[PlacementValidity], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> Union[Annotated[Union[UpdateTransformationMutationUpdatetransformationBaseAffineTransformation, UpdateTransformationMutationUpdatetransformationBaseBijectionTransformation, UpdateTransformationMutationUpdatetransformationBaseByDimensionTransformation, UpdateTransformationMutationUpdatetransformationBaseFieldTransformation, UpdateTransformationMutationUpdatetransformationBaseIdentityTransformation, UpdateTransformationMutationUpdatetransformationBaseMapAxisTransformation, UpdateTransformationMutationUpdatetransformationBaseRotationTransformation, UpdateTransformationMutationUpdatetransformationBaseScaleTransformation, UpdateTransformationMutationUpdatetransformationBaseSequenceTransformation, UpdateTransformationMutationUpdatetransformationBaseTranslationTransformation, UpdateTransformationMutationUpdatetransformationBaseUnmappableTransformation], Field(discriminator='typename')], UpdateTransformationMutationUpdatetransformationBaseCatchAll]:
    """UpdateTransformation 

Refine a transformation's parameters, bumping its version

Args:
    id: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID. (required)
    name: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.
    scale: The `Float` scalar type represents signed double-precision fractional values as specified by [IEEE 754](https://en.wikipedia.org/wiki/IEEE_floating_point). (required) (list)
    translation: The `Float` scalar type represents signed double-precision fractional values as specified by [IEEE 754](https://en.wikipedia.org/wiki/IEEE_floating_point). (required) (list)
    affine: The `Float` scalar type represents signed double-precision fractional values as specified by [IEEE 754](https://en.wikipedia.org/wiki/IEEE_floating_point). (required) (list) (required) (list)
    validity: PlacementValidity
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    Transformation
"""
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    _input['id'] = id
    if name is not UNSET:
        _input['name'] = name
    if scale is not UNSET:
        _input['scale'] = scale
    if translation is not UNSET:
        _input['translation'] = translation
    if affine is not UNSET:
        _input['affine'] = affine
    if validity is not UNSET:
        _input['validity'] = validity
    variables['input'] = _input
    return (await aexecute(UpdateTransformationMutation, variables, rath=rath)).update_transformation

def update_transformation(id: IDCoercible, name: Union[Optional[str], UnsetType]=UNSET, scale: Union[Optional[Iterable[float]], UnsetType]=UNSET, translation: Union[Optional[Iterable[float]], UnsetType]=UNSET, affine: Union[Optional[Iterable[Iterable[float]]], UnsetType]=UNSET, validity: Union[Optional[PlacementValidity], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> Union[Annotated[Union[UpdateTransformationMutationUpdatetransformationBaseAffineTransformation, UpdateTransformationMutationUpdatetransformationBaseBijectionTransformation, UpdateTransformationMutationUpdatetransformationBaseByDimensionTransformation, UpdateTransformationMutationUpdatetransformationBaseFieldTransformation, UpdateTransformationMutationUpdatetransformationBaseIdentityTransformation, UpdateTransformationMutationUpdatetransformationBaseMapAxisTransformation, UpdateTransformationMutationUpdatetransformationBaseRotationTransformation, UpdateTransformationMutationUpdatetransformationBaseScaleTransformation, UpdateTransformationMutationUpdatetransformationBaseSequenceTransformation, UpdateTransformationMutationUpdatetransformationBaseTranslationTransformation, UpdateTransformationMutationUpdatetransformationBaseUnmappableTransformation], Field(discriminator='typename')], UpdateTransformationMutationUpdatetransformationBaseCatchAll]:
    """UpdateTransformation 

Refine a transformation's parameters, bumping its version

Args:
    id: The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID. (required)
    name: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.
    scale: The `Float` scalar type represents signed double-precision fractional values as specified by [IEEE 754](https://en.wikipedia.org/wiki/IEEE_floating_point). (required) (list)
    translation: The `Float` scalar type represents signed double-precision fractional values as specified by [IEEE 754](https://en.wikipedia.org/wiki/IEEE_floating_point). (required) (list)
    affine: The `Float` scalar type represents signed double-precision fractional values as specified by [IEEE 754](https://en.wikipedia.org/wiki/IEEE_floating_point). (required) (list) (required) (list)
    validity: PlacementValidity
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    Transformation
"""
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    _input['id'] = id
    if name is not UNSET:
        _input['name'] = name
    if scale is not UNSET:
        _input['scale'] = scale
    if translation is not UNSET:
        _input['translation'] = translation
    if affine is not UNSET:
        _input['affine'] = affine
    if validity is not UNSET:
        _input['validity'] = validity
    variables['input'] = _input
    return execute(UpdateTransformationMutation, variables, rath=rath).update_transformation

async def adelete_transformation(id: IDCoercible, rath: Optional[MikroNextRath]=None) -> ID:
    """DeleteTransformation 

Delete an existing transformation

Args:
    id: The ID of the transformation to delete
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    ID
"""
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    _input['id'] = id
    variables['input'] = _input
    return (await aexecute(DeleteTransformationMutation, variables, rath=rath)).delete_transformation

def delete_transformation(id: IDCoercible, rath: Optional[MikroNextRath]=None) -> ID:
    """DeleteTransformation 

Delete an existing transformation

Args:
    id: The ID of the transformation to delete
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    ID
"""
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    _input['id'] = id
    variables['input'] = _input
    return execute(DeleteTransformationMutation, variables, rath=rath).delete_transformation

async def acreate_rgb_view(context: IDCoercible, image: IDCoercible, collection: Union[Optional[IDCoercible], UnsetType]=UNSET, z_min: Union[Optional[int], UnsetType]=UNSET, z_max: Union[Optional[int], UnsetType]=UNSET, x_min: Union[Optional[int], UnsetType]=UNSET, x_max: Union[Optional[int], UnsetType]=UNSET, y_min: Union[Optional[int], UnsetType]=UNSET, y_max: Union[Optional[int], UnsetType]=UNSET, t_min: Union[Optional[int], UnsetType]=UNSET, t_max: Union[Optional[int], UnsetType]=UNSET, c_min: Union[Optional[int], UnsetType]=UNSET, c_max: Union[Optional[int], UnsetType]=UNSET, gamma: Union[Optional[float], UnsetType]=UNSET, contrast_limit_min: Union[Optional[float], UnsetType]=UNSET, contrast_limit_max: Union[Optional[float], UnsetType]=UNSET, rescale: Union[Optional[bool], UnsetType]=UNSET, scale: Union[Optional[float], UnsetType]=UNSET, active: Union[Optional[bool], UnsetType]=UNSET, color_map: Union[Optional[ColorMap], UnsetType]=UNSET, base_color: Union[Optional[Iterable[float]], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> CreateRgbViewMutationCreatergbview:
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
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    if collection is not UNSET:
        _input['collection'] = collection
    if z_min is not UNSET:
        _input['zMin'] = z_min
    if z_max is not UNSET:
        _input['zMax'] = z_max
    if x_min is not UNSET:
        _input['xMin'] = x_min
    if x_max is not UNSET:
        _input['xMax'] = x_max
    if y_min is not UNSET:
        _input['yMin'] = y_min
    if y_max is not UNSET:
        _input['yMax'] = y_max
    if t_min is not UNSET:
        _input['tMin'] = t_min
    if t_max is not UNSET:
        _input['tMax'] = t_max
    if c_min is not UNSET:
        _input['cMin'] = c_min
    if c_max is not UNSET:
        _input['cMax'] = c_max
    _input['context'] = context
    if gamma is not UNSET:
        _input['gamma'] = gamma
    if contrast_limit_min is not UNSET:
        _input['contrastLimitMin'] = contrast_limit_min
    if contrast_limit_max is not UNSET:
        _input['contrastLimitMax'] = contrast_limit_max
    if rescale is not UNSET:
        _input['rescale'] = rescale
    if scale is not UNSET:
        _input['scale'] = scale
    if active is not UNSET:
        _input['active'] = active
    if color_map is not UNSET:
        _input['colorMap'] = color_map
    if base_color is not UNSET:
        _input['baseColor'] = base_color
    _input['image'] = image
    variables['input'] = _input
    return (await aexecute(CreateRgbViewMutation, variables, rath=rath)).create_rgb_view

def create_rgb_view(context: IDCoercible, image: IDCoercible, collection: Union[Optional[IDCoercible], UnsetType]=UNSET, z_min: Union[Optional[int], UnsetType]=UNSET, z_max: Union[Optional[int], UnsetType]=UNSET, x_min: Union[Optional[int], UnsetType]=UNSET, x_max: Union[Optional[int], UnsetType]=UNSET, y_min: Union[Optional[int], UnsetType]=UNSET, y_max: Union[Optional[int], UnsetType]=UNSET, t_min: Union[Optional[int], UnsetType]=UNSET, t_max: Union[Optional[int], UnsetType]=UNSET, c_min: Union[Optional[int], UnsetType]=UNSET, c_max: Union[Optional[int], UnsetType]=UNSET, gamma: Union[Optional[float], UnsetType]=UNSET, contrast_limit_min: Union[Optional[float], UnsetType]=UNSET, contrast_limit_max: Union[Optional[float], UnsetType]=UNSET, rescale: Union[Optional[bool], UnsetType]=UNSET, scale: Union[Optional[float], UnsetType]=UNSET, active: Union[Optional[bool], UnsetType]=UNSET, color_map: Union[Optional[ColorMap], UnsetType]=UNSET, base_color: Union[Optional[Iterable[float]], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> CreateRgbViewMutationCreatergbview:
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
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    if collection is not UNSET:
        _input['collection'] = collection
    if z_min is not UNSET:
        _input['zMin'] = z_min
    if z_max is not UNSET:
        _input['zMax'] = z_max
    if x_min is not UNSET:
        _input['xMin'] = x_min
    if x_max is not UNSET:
        _input['xMax'] = x_max
    if y_min is not UNSET:
        _input['yMin'] = y_min
    if y_max is not UNSET:
        _input['yMax'] = y_max
    if t_min is not UNSET:
        _input['tMin'] = t_min
    if t_max is not UNSET:
        _input['tMax'] = t_max
    if c_min is not UNSET:
        _input['cMin'] = c_min
    if c_max is not UNSET:
        _input['cMax'] = c_max
    _input['context'] = context
    if gamma is not UNSET:
        _input['gamma'] = gamma
    if contrast_limit_min is not UNSET:
        _input['contrastLimitMin'] = contrast_limit_min
    if contrast_limit_max is not UNSET:
        _input['contrastLimitMax'] = contrast_limit_max
    if rescale is not UNSET:
        _input['rescale'] = rescale
    if scale is not UNSET:
        _input['scale'] = scale
    if active is not UNSET:
        _input['active'] = active
    if color_map is not UNSET:
        _input['colorMap'] = color_map
    if base_color is not UNSET:
        _input['baseColor'] = base_color
    _input['image'] = image
    variables['input'] = _input
    return execute(CreateRgbViewMutation, variables, rath=rath).create_rgb_view

async def aupdate_rgb_view(id: IDCoercible, collection: Union[Optional[IDCoercible], UnsetType]=UNSET, z_min: Union[Optional[int], UnsetType]=UNSET, z_max: Union[Optional[int], UnsetType]=UNSET, x_min: Union[Optional[int], UnsetType]=UNSET, x_max: Union[Optional[int], UnsetType]=UNSET, y_min: Union[Optional[int], UnsetType]=UNSET, y_max: Union[Optional[int], UnsetType]=UNSET, t_min: Union[Optional[int], UnsetType]=UNSET, t_max: Union[Optional[int], UnsetType]=UNSET, c_min: Union[Optional[int], UnsetType]=UNSET, c_max: Union[Optional[int], UnsetType]=UNSET, context: Union[Optional[IDCoercible], UnsetType]=UNSET, gamma: Union[Optional[float], UnsetType]=UNSET, contrast_limit_min: Union[Optional[float], UnsetType]=UNSET, contrast_limit_max: Union[Optional[float], UnsetType]=UNSET, rescale: Union[Optional[bool], UnsetType]=UNSET, scale: Union[Optional[float], UnsetType]=UNSET, active: Union[Optional[bool], UnsetType]=UNSET, color_map: Union[Optional[ColorMap], UnsetType]=UNSET, base_color: Union[Optional[Iterable[float]], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> UpdateRgbViewMutationUpdatergbview:
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
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    if collection is not UNSET:
        _input['collection'] = collection
    if z_min is not UNSET:
        _input['zMin'] = z_min
    if z_max is not UNSET:
        _input['zMax'] = z_max
    if x_min is not UNSET:
        _input['xMin'] = x_min
    if x_max is not UNSET:
        _input['xMax'] = x_max
    if y_min is not UNSET:
        _input['yMin'] = y_min
    if y_max is not UNSET:
        _input['yMax'] = y_max
    if t_min is not UNSET:
        _input['tMin'] = t_min
    if t_max is not UNSET:
        _input['tMax'] = t_max
    if c_min is not UNSET:
        _input['cMin'] = c_min
    if c_max is not UNSET:
        _input['cMax'] = c_max
    if context is not UNSET:
        _input['context'] = context
    if gamma is not UNSET:
        _input['gamma'] = gamma
    if contrast_limit_min is not UNSET:
        _input['contrastLimitMin'] = contrast_limit_min
    if contrast_limit_max is not UNSET:
        _input['contrastLimitMax'] = contrast_limit_max
    if rescale is not UNSET:
        _input['rescale'] = rescale
    if scale is not UNSET:
        _input['scale'] = scale
    if active is not UNSET:
        _input['active'] = active
    if color_map is not UNSET:
        _input['colorMap'] = color_map
    if base_color is not UNSET:
        _input['baseColor'] = base_color
    _input['id'] = id
    variables['input'] = _input
    return (await aexecute(UpdateRgbViewMutation, variables, rath=rath)).update_rgb_view

def update_rgb_view(id: IDCoercible, collection: Union[Optional[IDCoercible], UnsetType]=UNSET, z_min: Union[Optional[int], UnsetType]=UNSET, z_max: Union[Optional[int], UnsetType]=UNSET, x_min: Union[Optional[int], UnsetType]=UNSET, x_max: Union[Optional[int], UnsetType]=UNSET, y_min: Union[Optional[int], UnsetType]=UNSET, y_max: Union[Optional[int], UnsetType]=UNSET, t_min: Union[Optional[int], UnsetType]=UNSET, t_max: Union[Optional[int], UnsetType]=UNSET, c_min: Union[Optional[int], UnsetType]=UNSET, c_max: Union[Optional[int], UnsetType]=UNSET, context: Union[Optional[IDCoercible], UnsetType]=UNSET, gamma: Union[Optional[float], UnsetType]=UNSET, contrast_limit_min: Union[Optional[float], UnsetType]=UNSET, contrast_limit_max: Union[Optional[float], UnsetType]=UNSET, rescale: Union[Optional[bool], UnsetType]=UNSET, scale: Union[Optional[float], UnsetType]=UNSET, active: Union[Optional[bool], UnsetType]=UNSET, color_map: Union[Optional[ColorMap], UnsetType]=UNSET, base_color: Union[Optional[Iterable[float]], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> UpdateRgbViewMutationUpdatergbview:
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
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    if collection is not UNSET:
        _input['collection'] = collection
    if z_min is not UNSET:
        _input['zMin'] = z_min
    if z_max is not UNSET:
        _input['zMax'] = z_max
    if x_min is not UNSET:
        _input['xMin'] = x_min
    if x_max is not UNSET:
        _input['xMax'] = x_max
    if y_min is not UNSET:
        _input['yMin'] = y_min
    if y_max is not UNSET:
        _input['yMax'] = y_max
    if t_min is not UNSET:
        _input['tMin'] = t_min
    if t_max is not UNSET:
        _input['tMax'] = t_max
    if c_min is not UNSET:
        _input['cMin'] = c_min
    if c_max is not UNSET:
        _input['cMax'] = c_max
    if context is not UNSET:
        _input['context'] = context
    if gamma is not UNSET:
        _input['gamma'] = gamma
    if contrast_limit_min is not UNSET:
        _input['contrastLimitMin'] = contrast_limit_min
    if contrast_limit_max is not UNSET:
        _input['contrastLimitMax'] = contrast_limit_max
    if rescale is not UNSET:
        _input['rescale'] = rescale
    if scale is not UNSET:
        _input['scale'] = scale
    if active is not UNSET:
        _input['active'] = active
    if color_map is not UNSET:
        _input['colorMap'] = color_map
    if base_color is not UNSET:
        _input['baseColor'] = base_color
    _input['id'] = id
    variables['input'] = _input
    return execute(UpdateRgbViewMutation, variables, rath=rath).update_rgb_view

async def acreate_histogram_view(histogram: Iterable[float], bins: Iterable[float], min: float, max: float, image: IDCoercible, collection: Union[Optional[IDCoercible], UnsetType]=UNSET, z_min: Union[Optional[int], UnsetType]=UNSET, z_max: Union[Optional[int], UnsetType]=UNSET, x_min: Union[Optional[int], UnsetType]=UNSET, x_max: Union[Optional[int], UnsetType]=UNSET, y_min: Union[Optional[int], UnsetType]=UNSET, y_max: Union[Optional[int], UnsetType]=UNSET, t_min: Union[Optional[int], UnsetType]=UNSET, t_max: Union[Optional[int], UnsetType]=UNSET, c_min: Union[Optional[int], UnsetType]=UNSET, c_max: Union[Optional[int], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> HistogramView:
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
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    if collection is not UNSET:
        _input['collection'] = collection
    if z_min is not UNSET:
        _input['zMin'] = z_min
    if z_max is not UNSET:
        _input['zMax'] = z_max
    if x_min is not UNSET:
        _input['xMin'] = x_min
    if x_max is not UNSET:
        _input['xMax'] = x_max
    if y_min is not UNSET:
        _input['yMin'] = y_min
    if y_max is not UNSET:
        _input['yMax'] = y_max
    if t_min is not UNSET:
        _input['tMin'] = t_min
    if t_max is not UNSET:
        _input['tMax'] = t_max
    if c_min is not UNSET:
        _input['cMin'] = c_min
    if c_max is not UNSET:
        _input['cMax'] = c_max
    _input['histogram'] = histogram
    _input['bins'] = bins
    _input['min'] = min
    _input['max'] = max
    _input['image'] = image
    variables['input'] = _input
    return (await aexecute(CreateHistogramViewMutation, variables, rath=rath)).create_histogram_view

def create_histogram_view(histogram: Iterable[float], bins: Iterable[float], min: float, max: float, image: IDCoercible, collection: Union[Optional[IDCoercible], UnsetType]=UNSET, z_min: Union[Optional[int], UnsetType]=UNSET, z_max: Union[Optional[int], UnsetType]=UNSET, x_min: Union[Optional[int], UnsetType]=UNSET, x_max: Union[Optional[int], UnsetType]=UNSET, y_min: Union[Optional[int], UnsetType]=UNSET, y_max: Union[Optional[int], UnsetType]=UNSET, t_min: Union[Optional[int], UnsetType]=UNSET, t_max: Union[Optional[int], UnsetType]=UNSET, c_min: Union[Optional[int], UnsetType]=UNSET, c_max: Union[Optional[int], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> HistogramView:
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
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    if collection is not UNSET:
        _input['collection'] = collection
    if z_min is not UNSET:
        _input['zMin'] = z_min
    if z_max is not UNSET:
        _input['zMax'] = z_max
    if x_min is not UNSET:
        _input['xMin'] = x_min
    if x_max is not UNSET:
        _input['xMax'] = x_max
    if y_min is not UNSET:
        _input['yMin'] = y_min
    if y_max is not UNSET:
        _input['yMax'] = y_max
    if t_min is not UNSET:
        _input['tMin'] = t_min
    if t_max is not UNSET:
        _input['tMax'] = t_max
    if c_min is not UNSET:
        _input['cMin'] = c_min
    if c_max is not UNSET:
        _input['cMax'] = c_max
    _input['histogram'] = histogram
    _input['bins'] = bins
    _input['min'] = min
    _input['max'] = max
    _input['image'] = image
    variables['input'] = _input
    return execute(CreateHistogramViewMutation, variables, rath=rath).create_histogram_view

async def acreate_mask_view(image: IDCoercible, collection: Union[Optional[IDCoercible], UnsetType]=UNSET, z_min: Union[Optional[int], UnsetType]=UNSET, z_max: Union[Optional[int], UnsetType]=UNSET, x_min: Union[Optional[int], UnsetType]=UNSET, x_max: Union[Optional[int], UnsetType]=UNSET, y_min: Union[Optional[int], UnsetType]=UNSET, y_max: Union[Optional[int], UnsetType]=UNSET, t_min: Union[Optional[int], UnsetType]=UNSET, t_max: Union[Optional[int], UnsetType]=UNSET, c_min: Union[Optional[int], UnsetType]=UNSET, c_max: Union[Optional[int], UnsetType]=UNSET, reference_view: Union[Optional[IDCoercible], UnsetType]=UNSET, labels: Union[Optional[LabelsLike], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> MaskView:
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
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    if collection is not UNSET:
        _input['collection'] = collection
    if z_min is not UNSET:
        _input['zMin'] = z_min
    if z_max is not UNSET:
        _input['zMax'] = z_max
    if x_min is not UNSET:
        _input['xMin'] = x_min
    if x_max is not UNSET:
        _input['xMax'] = x_max
    if y_min is not UNSET:
        _input['yMin'] = y_min
    if y_max is not UNSET:
        _input['yMax'] = y_max
    if t_min is not UNSET:
        _input['tMin'] = t_min
    if t_max is not UNSET:
        _input['tMax'] = t_max
    if c_min is not UNSET:
        _input['cMin'] = c_min
    if c_max is not UNSET:
        _input['cMax'] = c_max
    if reference_view is not UNSET:
        _input['referenceView'] = reference_view
    if labels is not UNSET:
        _input['labels'] = labels
    _input['image'] = image
    variables['input'] = _input
    return (await aexecute(CreateMaskViewMutation, variables, rath=rath)).create_mask_view

def create_mask_view(image: IDCoercible, collection: Union[Optional[IDCoercible], UnsetType]=UNSET, z_min: Union[Optional[int], UnsetType]=UNSET, z_max: Union[Optional[int], UnsetType]=UNSET, x_min: Union[Optional[int], UnsetType]=UNSET, x_max: Union[Optional[int], UnsetType]=UNSET, y_min: Union[Optional[int], UnsetType]=UNSET, y_max: Union[Optional[int], UnsetType]=UNSET, t_min: Union[Optional[int], UnsetType]=UNSET, t_max: Union[Optional[int], UnsetType]=UNSET, c_min: Union[Optional[int], UnsetType]=UNSET, c_max: Union[Optional[int], UnsetType]=UNSET, reference_view: Union[Optional[IDCoercible], UnsetType]=UNSET, labels: Union[Optional[LabelsLike], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> MaskView:
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
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    if collection is not UNSET:
        _input['collection'] = collection
    if z_min is not UNSET:
        _input['zMin'] = z_min
    if z_max is not UNSET:
        _input['zMax'] = z_max
    if x_min is not UNSET:
        _input['xMin'] = x_min
    if x_max is not UNSET:
        _input['xMax'] = x_max
    if y_min is not UNSET:
        _input['yMin'] = y_min
    if y_max is not UNSET:
        _input['yMax'] = y_max
    if t_min is not UNSET:
        _input['tMin'] = t_min
    if t_max is not UNSET:
        _input['tMax'] = t_max
    if c_min is not UNSET:
        _input['cMin'] = c_min
    if c_max is not UNSET:
        _input['cMax'] = c_max
    if reference_view is not UNSET:
        _input['referenceView'] = reference_view
    if labels is not UNSET:
        _input['labels'] = labels
    _input['image'] = image
    variables['input'] = _input
    return execute(CreateMaskViewMutation, variables, rath=rath).create_mask_view

async def acreate_instance_mask_view(image: IDCoercible, collection: Union[Optional[IDCoercible], UnsetType]=UNSET, z_min: Union[Optional[int], UnsetType]=UNSET, z_max: Union[Optional[int], UnsetType]=UNSET, x_min: Union[Optional[int], UnsetType]=UNSET, x_max: Union[Optional[int], UnsetType]=UNSET, y_min: Union[Optional[int], UnsetType]=UNSET, y_max: Union[Optional[int], UnsetType]=UNSET, t_min: Union[Optional[int], UnsetType]=UNSET, t_max: Union[Optional[int], UnsetType]=UNSET, c_min: Union[Optional[int], UnsetType]=UNSET, c_max: Union[Optional[int], UnsetType]=UNSET, reference_view: Union[Optional[IDCoercible], UnsetType]=UNSET, labels: Union[Optional[LabelsLike], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> InstanceMaskView:
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
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    if collection is not UNSET:
        _input['collection'] = collection
    if z_min is not UNSET:
        _input['zMin'] = z_min
    if z_max is not UNSET:
        _input['zMax'] = z_max
    if x_min is not UNSET:
        _input['xMin'] = x_min
    if x_max is not UNSET:
        _input['xMax'] = x_max
    if y_min is not UNSET:
        _input['yMin'] = y_min
    if y_max is not UNSET:
        _input['yMax'] = y_max
    if t_min is not UNSET:
        _input['tMin'] = t_min
    if t_max is not UNSET:
        _input['tMax'] = t_max
    if c_min is not UNSET:
        _input['cMin'] = c_min
    if c_max is not UNSET:
        _input['cMax'] = c_max
    if reference_view is not UNSET:
        _input['referenceView'] = reference_view
    if labels is not UNSET:
        _input['labels'] = labels
    _input['image'] = image
    variables['input'] = _input
    return (await aexecute(CreateInstanceMaskViewMutation, variables, rath=rath)).create_instance_mask_view

def create_instance_mask_view(image: IDCoercible, collection: Union[Optional[IDCoercible], UnsetType]=UNSET, z_min: Union[Optional[int], UnsetType]=UNSET, z_max: Union[Optional[int], UnsetType]=UNSET, x_min: Union[Optional[int], UnsetType]=UNSET, x_max: Union[Optional[int], UnsetType]=UNSET, y_min: Union[Optional[int], UnsetType]=UNSET, y_max: Union[Optional[int], UnsetType]=UNSET, t_min: Union[Optional[int], UnsetType]=UNSET, t_max: Union[Optional[int], UnsetType]=UNSET, c_min: Union[Optional[int], UnsetType]=UNSET, c_max: Union[Optional[int], UnsetType]=UNSET, reference_view: Union[Optional[IDCoercible], UnsetType]=UNSET, labels: Union[Optional[LabelsLike], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> InstanceMaskView:
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
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    if collection is not UNSET:
        _input['collection'] = collection
    if z_min is not UNSET:
        _input['zMin'] = z_min
    if z_max is not UNSET:
        _input['zMax'] = z_max
    if x_min is not UNSET:
        _input['xMin'] = x_min
    if x_max is not UNSET:
        _input['xMax'] = x_max
    if y_min is not UNSET:
        _input['yMin'] = y_min
    if y_max is not UNSET:
        _input['yMax'] = y_max
    if t_min is not UNSET:
        _input['tMin'] = t_min
    if t_max is not UNSET:
        _input['tMax'] = t_max
    if c_min is not UNSET:
        _input['cMin'] = c_min
    if c_max is not UNSET:
        _input['cMax'] = c_max
    if reference_view is not UNSET:
        _input['referenceView'] = reference_view
    if labels is not UNSET:
        _input['labels'] = labels
    _input['image'] = image
    variables['input'] = _input
    return execute(CreateInstanceMaskViewMutation, variables, rath=rath).create_instance_mask_view

async def acreate_reference_view(image: IDCoercible, collection: Union[Optional[IDCoercible], UnsetType]=UNSET, z_min: Union[Optional[int], UnsetType]=UNSET, z_max: Union[Optional[int], UnsetType]=UNSET, x_min: Union[Optional[int], UnsetType]=UNSET, x_max: Union[Optional[int], UnsetType]=UNSET, y_min: Union[Optional[int], UnsetType]=UNSET, y_max: Union[Optional[int], UnsetType]=UNSET, t_min: Union[Optional[int], UnsetType]=UNSET, t_max: Union[Optional[int], UnsetType]=UNSET, c_min: Union[Optional[int], UnsetType]=UNSET, c_max: Union[Optional[int], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> ReferenceView:
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
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    if collection is not UNSET:
        _input['collection'] = collection
    if z_min is not UNSET:
        _input['zMin'] = z_min
    if z_max is not UNSET:
        _input['zMax'] = z_max
    if x_min is not UNSET:
        _input['xMin'] = x_min
    if x_max is not UNSET:
        _input['xMax'] = x_max
    if y_min is not UNSET:
        _input['yMin'] = y_min
    if y_max is not UNSET:
        _input['yMax'] = y_max
    if t_min is not UNSET:
        _input['tMin'] = t_min
    if t_max is not UNSET:
        _input['tMax'] = t_max
    if c_min is not UNSET:
        _input['cMin'] = c_min
    if c_max is not UNSET:
        _input['cMax'] = c_max
    _input['image'] = image
    variables['input'] = _input
    return (await aexecute(CreateReferenceViewMutation, variables, rath=rath)).create_reference_view

def create_reference_view(image: IDCoercible, collection: Union[Optional[IDCoercible], UnsetType]=UNSET, z_min: Union[Optional[int], UnsetType]=UNSET, z_max: Union[Optional[int], UnsetType]=UNSET, x_min: Union[Optional[int], UnsetType]=UNSET, x_max: Union[Optional[int], UnsetType]=UNSET, y_min: Union[Optional[int], UnsetType]=UNSET, y_max: Union[Optional[int], UnsetType]=UNSET, t_min: Union[Optional[int], UnsetType]=UNSET, t_max: Union[Optional[int], UnsetType]=UNSET, c_min: Union[Optional[int], UnsetType]=UNSET, c_max: Union[Optional[int], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> ReferenceView:
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
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    if collection is not UNSET:
        _input['collection'] = collection
    if z_min is not UNSET:
        _input['zMin'] = z_min
    if z_max is not UNSET:
        _input['zMax'] = z_max
    if x_min is not UNSET:
        _input['xMin'] = x_min
    if x_max is not UNSET:
        _input['xMax'] = x_max
    if y_min is not UNSET:
        _input['yMin'] = y_min
    if y_max is not UNSET:
        _input['yMax'] = y_max
    if t_min is not UNSET:
        _input['tMin'] = t_min
    if t_max is not UNSET:
        _input['tMax'] = t_max
    if c_min is not UNSET:
        _input['cMin'] = c_min
    if c_max is not UNSET:
        _input['cMax'] = c_max
    _input['image'] = image
    variables['input'] = _input
    return execute(CreateReferenceViewMutation, variables, rath=rath).create_reference_view

async def acreate_view_collection(name: str, rath: Optional[MikroNextRath]=None) -> CreateViewCollectionMutationCreateviewcollection:
    """CreateViewCollection 

Create a new collection of views to organize related views

Args:
    name: The name of the view collection
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    CreateViewCollectionMutationCreateviewcollection
"""
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    _input['name'] = name
    variables['input'] = _input
    return (await aexecute(CreateViewCollectionMutation, variables, rath=rath)).create_view_collection

def create_view_collection(name: str, rath: Optional[MikroNextRath]=None) -> CreateViewCollectionMutationCreateviewcollection:
    """CreateViewCollection 

Create a new collection of views to organize related views

Args:
    name: The name of the view collection
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    CreateViewCollectionMutationCreateviewcollection
"""
    variables: Dict[str, Any] = {}
    _input: Dict[str, Any] = {}
    _input['name'] = name
    variables['input'] = _input
    return execute(CreateViewCollectionMutation, variables, rath=rath).create_view_collection

async def aget_a_dataset(id: IDCoercible, rath: Optional[MikroNextRath]=None) -> ADataset:
    """GetADataset 

Get a single array dataset by ID

Args:
    id (ID): No description
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    ADataset
"""
    variables: Dict[str, Any] = {}
    variables['id'] = id
    return (await aexecute(GetADatasetQuery, variables, rath=rath)).adataset

def get_a_dataset(id: IDCoercible, rath: Optional[MikroNextRath]=None) -> ADataset:
    """GetADataset 

Get a single array dataset by ID

Args:
    id (ID): No description
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    ADataset
"""
    variables: Dict[str, Any] = {}
    variables['id'] = id
    return execute(GetADatasetQuery, variables, rath=rath).adataset

async def aget_a_datasets(filters: Union[Optional[ADatasetFilter], UnsetType]=UNSET, pagination: Union[Optional[OffsetPaginationInput], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> Tuple[ADataset, ...]:
    """GetADatasets 

List array datasets (N-dimensional arrays with named dimensions and anchored metadata)

Args:
    filters (Optional[ADatasetFilter], optional): No description. 
    pagination (Optional[OffsetPaginationInput], optional): No description. 
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    List[ADataset]
"""
    variables: Dict[str, Any] = {}
    if filters is not UNSET:
        variables['filters'] = filters
    if pagination is not UNSET:
        variables['pagination'] = pagination
    return (await aexecute(GetADatasetsQuery, variables, rath=rath)).adatasets

def get_a_datasets(filters: Union[Optional[ADatasetFilter], UnsetType]=UNSET, pagination: Union[Optional[OffsetPaginationInput], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> Tuple[ADataset, ...]:
    """GetADatasets 

List array datasets (N-dimensional arrays with named dimensions and anchored metadata)

Args:
    filters (Optional[ADatasetFilter], optional): No description. 
    pagination (Optional[OffsetPaginationInput], optional): No description. 
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    List[ADataset]
"""
    variables: Dict[str, Any] = {}
    if filters is not UNSET:
        variables['filters'] = filters
    if pagination is not UNSET:
        variables['pagination'] = pagination
    return execute(GetADatasetsQuery, variables, rath=rath).adatasets

async def asearch_a_datasets(search: Union[Optional[str], UnsetType]=UNSET, values: Union[Optional[List[IDCoercible]], UnsetType]=UNSET, limit: Union[Optional[int], UnsetType]=UNSET, offset: Union[Optional[int], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> Tuple[SearchADatasetsQueryOptions, ...]:
    """SearchADatasets 

List array datasets (N-dimensional arrays with named dimensions and anchored metadata)

Args:
    search (Optional[str], optional): No description. 
    values (Optional[List[ID]], optional): No description. 
    limit (Optional[int], optional): No description. 
    offset (Optional[int], optional): No description. Defaults to 0
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    List[SearchADatasetsQueryAdatasets]
"""
    variables: Dict[str, Any] = {}
    if search is not UNSET:
        variables['search'] = search
    if values is not UNSET:
        variables['values'] = values
    if limit is not UNSET:
        variables['limit'] = limit
    if offset is not UNSET:
        variables['offset'] = offset
    return (await aexecute(SearchADatasetsQuery, variables, rath=rath)).options

def search_a_datasets(search: Union[Optional[str], UnsetType]=UNSET, values: Union[Optional[List[IDCoercible]], UnsetType]=UNSET, limit: Union[Optional[int], UnsetType]=UNSET, offset: Union[Optional[int], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> Tuple[SearchADatasetsQueryOptions, ...]:
    """SearchADatasets 

List array datasets (N-dimensional arrays with named dimensions and anchored metadata)

Args:
    search (Optional[str], optional): No description. 
    values (Optional[List[ID]], optional): No description. 
    limit (Optional[int], optional): No description. 
    offset (Optional[int], optional): No description. Defaults to 0
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    List[SearchADatasetsQueryAdatasets]
"""
    variables: Dict[str, Any] = {}
    if search is not UNSET:
        variables['search'] = search
    if values is not UNSET:
        variables['values'] = values
    if limit is not UNSET:
        variables['limit'] = limit
    if offset is not UNSET:
        variables['offset'] = offset
    return execute(SearchADatasetsQuery, variables, rath=rath).options

async def aget_animation(id: IDCoercible, rath: Optional[MikroNextRath]=None) -> Animation:
    """GetAnimation 

Get a single animation by ID

Args:
    id (ID): The unique identifier of an object
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    Animation
"""
    variables: Dict[str, Any] = {}
    variables['id'] = id
    return (await aexecute(GetAnimationQuery, variables, rath=rath)).animation

def get_animation(id: IDCoercible, rath: Optional[MikroNextRath]=None) -> Animation:
    """GetAnimation 

Get a single animation by ID

Args:
    id (ID): The unique identifier of an object
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    Animation
"""
    variables: Dict[str, Any] = {}
    variables['id'] = id
    return execute(GetAnimationQuery, variables, rath=rath).animation

async def aget_animations(filters: Union[Optional[AnimationFilter], UnsetType]=UNSET, pagination: Union[Optional[OffsetPaginationInput], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> Tuple[Animation, ...]:
    """GetAnimations 

List animations (named camera tours through a scene)

Args:
    filters (Optional[AnimationFilter], optional): No description. 
    pagination (Optional[OffsetPaginationInput], optional): No description. 
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    List[Animation]
"""
    variables: Dict[str, Any] = {}
    if filters is not UNSET:
        variables['filters'] = filters
    if pagination is not UNSET:
        variables['pagination'] = pagination
    return (await aexecute(GetAnimationsQuery, variables, rath=rath)).animations

def get_animations(filters: Union[Optional[AnimationFilter], UnsetType]=UNSET, pagination: Union[Optional[OffsetPaginationInput], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> Tuple[Animation, ...]:
    """GetAnimations 

List animations (named camera tours through a scene)

Args:
    filters (Optional[AnimationFilter], optional): No description. 
    pagination (Optional[OffsetPaginationInput], optional): No description. 
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    List[Animation]
"""
    variables: Dict[str, Any] = {}
    if filters is not UNSET:
        variables['filters'] = filters
    if pagination is not UNSET:
        variables['pagination'] = pagination
    return execute(GetAnimationsQuery, variables, rath=rath).animations

async def asearch_animations(search: Union[Optional[str], UnsetType]=UNSET, values: Union[Optional[List[IDCoercible]], UnsetType]=UNSET, limit: Union[Optional[int], UnsetType]=UNSET, offset: Union[Optional[int], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> Tuple[SearchAnimationsQueryOptions, ...]:
    """SearchAnimations 

List animations (named camera tours through a scene)

Args:
    search (Optional[str], optional): No description. 
    values (Optional[List[ID]], optional): No description. 
    limit (Optional[int], optional): No description. 
    offset (Optional[int], optional): No description. Defaults to 0
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    List[SearchAnimationsQueryAnimations]
"""
    variables: Dict[str, Any] = {}
    if search is not UNSET:
        variables['search'] = search
    if values is not UNSET:
        variables['values'] = values
    if limit is not UNSET:
        variables['limit'] = limit
    if offset is not UNSET:
        variables['offset'] = offset
    return (await aexecute(SearchAnimationsQuery, variables, rath=rath)).options

def search_animations(search: Union[Optional[str], UnsetType]=UNSET, values: Union[Optional[List[IDCoercible]], UnsetType]=UNSET, limit: Union[Optional[int], UnsetType]=UNSET, offset: Union[Optional[int], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> Tuple[SearchAnimationsQueryOptions, ...]:
    """SearchAnimations 

List animations (named camera tours through a scene)

Args:
    search (Optional[str], optional): No description. 
    values (Optional[List[ID]], optional): No description. 
    limit (Optional[int], optional): No description. 
    offset (Optional[int], optional): No description. Defaults to 0
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    List[SearchAnimationsQueryAnimations]
"""
    variables: Dict[str, Any] = {}
    if search is not UNSET:
        variables['search'] = search
    if values is not UNSET:
        variables['values'] = values
    if limit is not UNSET:
        variables['limit'] = limit
    if offset is not UNSET:
        variables['offset'] = offset
    return execute(SearchAnimationsQuery, variables, rath=rath).options

async def aget_annotation(id: IDCoercible, rath: Optional[MikroNextRath]=None) -> Annotation:
    """GetAnnotation 

Get a single annotation by ID

Args:
    id (ID): No description
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    Annotation
"""
    variables: Dict[str, Any] = {}
    variables['id'] = id
    return (await aexecute(GetAnnotationQuery, variables, rath=rath)).annotation

def get_annotation(id: IDCoercible, rath: Optional[MikroNextRath]=None) -> Annotation:
    """GetAnnotation 

Get a single annotation by ID

Args:
    id (ID): No description
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    Annotation
"""
    variables: Dict[str, Any] = {}
    variables['id'] = id
    return execute(GetAnnotationQuery, variables, rath=rath).annotation

async def aget_annotations(filters: Union[Optional[AnnotationFilter], UnsetType]=UNSET, pagination: Union[Optional[OffsetPaginationInput], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> Tuple[Annotation, ...]:
    """GetAnnotations 

List annotations (human-drawn shapes, each in its collection's coordinate system)

Args:
    filters (Optional[AnnotationFilter], optional): No description. 
    pagination (Optional[OffsetPaginationInput], optional): No description. 
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    List[Annotation]
"""
    variables: Dict[str, Any] = {}
    if filters is not UNSET:
        variables['filters'] = filters
    if pagination is not UNSET:
        variables['pagination'] = pagination
    return (await aexecute(GetAnnotationsQuery, variables, rath=rath)).annotations

def get_annotations(filters: Union[Optional[AnnotationFilter], UnsetType]=UNSET, pagination: Union[Optional[OffsetPaginationInput], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> Tuple[Annotation, ...]:
    """GetAnnotations 

List annotations (human-drawn shapes, each in its collection's coordinate system)

Args:
    filters (Optional[AnnotationFilter], optional): No description. 
    pagination (Optional[OffsetPaginationInput], optional): No description. 
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    List[Annotation]
"""
    variables: Dict[str, Any] = {}
    if filters is not UNSET:
        variables['filters'] = filters
    if pagination is not UNSET:
        variables['pagination'] = pagination
    return execute(GetAnnotationsQuery, variables, rath=rath).annotations

async def aget_annotation_collection(id: IDCoercible, rath: Optional[MikroNextRath]=None) -> AnnotationCollection:
    """GetAnnotationCollection 

Get a single annotation collection by ID

Args:
    id (ID): No description
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    AnnotationCollection
"""
    variables: Dict[str, Any] = {}
    variables['id'] = id
    return (await aexecute(GetAnnotationCollectionQuery, variables, rath=rath)).annotation_collection

def get_annotation_collection(id: IDCoercible, rath: Optional[MikroNextRath]=None) -> AnnotationCollection:
    """GetAnnotationCollection 

Get a single annotation collection by ID

Args:
    id (ID): No description
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    AnnotationCollection
"""
    variables: Dict[str, Any] = {}
    variables['id'] = id
    return execute(GetAnnotationCollectionQuery, variables, rath=rath).annotation_collection

async def aget_annotation_collections(filters: Union[Optional[AnnotationCollectionFilter], UnsetType]=UNSET, pagination: Union[Optional[OffsetPaginationInput], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> Tuple[AnnotationCollection, ...]:
    """GetAnnotationCollections 

List annotation collections (named sets of human-drawn shapes, each owning the coordinate system they are drawn in)

Args:
    filters (Optional[AnnotationCollectionFilter], optional): No description. 
    pagination (Optional[OffsetPaginationInput], optional): No description. 
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    List[AnnotationCollection]
"""
    variables: Dict[str, Any] = {}
    if filters is not UNSET:
        variables['filters'] = filters
    if pagination is not UNSET:
        variables['pagination'] = pagination
    return (await aexecute(GetAnnotationCollectionsQuery, variables, rath=rath)).annotation_collections

def get_annotation_collections(filters: Union[Optional[AnnotationCollectionFilter], UnsetType]=UNSET, pagination: Union[Optional[OffsetPaginationInput], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> Tuple[AnnotationCollection, ...]:
    """GetAnnotationCollections 

List annotation collections (named sets of human-drawn shapes, each owning the coordinate system they are drawn in)

Args:
    filters (Optional[AnnotationCollectionFilter], optional): No description. 
    pagination (Optional[OffsetPaginationInput], optional): No description. 
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    List[AnnotationCollection]
"""
    variables: Dict[str, Any] = {}
    if filters is not UNSET:
        variables['filters'] = filters
    if pagination is not UNSET:
        variables['pagination'] = pagination
    return execute(GetAnnotationCollectionsQuery, variables, rath=rath).annotation_collections

async def asearch_annotation_collections(search: Union[Optional[str], UnsetType]=UNSET, values: Union[Optional[List[IDCoercible]], UnsetType]=UNSET, limit: Union[Optional[int], UnsetType]=UNSET, offset: Union[Optional[int], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> Tuple[SearchAnnotationCollectionsQueryOptions, ...]:
    """SearchAnnotationCollections 

List annotation collections (named sets of human-drawn shapes, each owning the coordinate system they are drawn in)

Args:
    search (Optional[str], optional): No description. 
    values (Optional[List[ID]], optional): No description. 
    limit (Optional[int], optional): No description. 
    offset (Optional[int], optional): No description. Defaults to 0
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    List[SearchAnnotationCollectionsQueryAnnotationcollections]
"""
    variables: Dict[str, Any] = {}
    if search is not UNSET:
        variables['search'] = search
    if values is not UNSET:
        variables['values'] = values
    if limit is not UNSET:
        variables['limit'] = limit
    if offset is not UNSET:
        variables['offset'] = offset
    return (await aexecute(SearchAnnotationCollectionsQuery, variables, rath=rath)).options

def search_annotation_collections(search: Union[Optional[str], UnsetType]=UNSET, values: Union[Optional[List[IDCoercible]], UnsetType]=UNSET, limit: Union[Optional[int], UnsetType]=UNSET, offset: Union[Optional[int], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> Tuple[SearchAnnotationCollectionsQueryOptions, ...]:
    """SearchAnnotationCollections 

List annotation collections (named sets of human-drawn shapes, each owning the coordinate system they are drawn in)

Args:
    search (Optional[str], optional): No description. 
    values (Optional[List[ID]], optional): No description. 
    limit (Optional[int], optional): No description. 
    offset (Optional[int], optional): No description. Defaults to 0
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    List[SearchAnnotationCollectionsQueryAnnotationcollections]
"""
    variables: Dict[str, Any] = {}
    if search is not UNSET:
        variables['search'] = search
    if values is not UNSET:
        variables['values'] = values
    if limit is not UNSET:
        variables['limit'] = limit
    if offset is not UNSET:
        variables['offset'] = offset
    return execute(SearchAnnotationCollectionsQuery, variables, rath=rath).options

async def aget_camera(id: IDCoercible, rath: Optional[MikroNextRath]=None) -> Camera:
    """GetCamera 

Get a single camera by ID

Args:
    id (ID): The unique identifier of an object
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    Camera
"""
    variables: Dict[str, Any] = {}
    variables['id'] = id
    return (await aexecute(GetCameraQuery, variables, rath=rath)).camera

def get_camera(id: IDCoercible, rath: Optional[MikroNextRath]=None) -> Camera:
    """GetCamera 

Get a single camera by ID

Args:
    id (ID): The unique identifier of an object
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    Camera
"""
    variables: Dict[str, Any] = {}
    variables['id'] = id
    return execute(GetCameraQuery, variables, rath=rath).camera

async def aget_coordinate_graph(coordinate_system: IDCoercible, max_depth: Union[Optional[int], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> GetCoordinateGraphQueryCoordinategraph:
    """GetCoordinateGraph 

Walk the coordinate graph out from one system: every coordinate system it reaches and every top-level edge between them. Reachability is undirected (an edge pointing into the system relates to it as much as one pointing out), the edges keep their true direction, and nothing is composed -- what the list queries cannot answer is 'which edges relate to *this* one', because relatedness is transitive and a filter is not

Args:
    coordinate_system (ID): No description
    max_depth (Optional[int], optional): No description. 
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    GetCoordinateGraphQueryCoordinategraph
"""
    variables: Dict[str, Any] = {}
    variables['coordinateSystem'] = coordinate_system
    if max_depth is not UNSET:
        variables['maxDepth'] = max_depth
    return (await aexecute(GetCoordinateGraphQuery, variables, rath=rath)).coordinate_graph

def get_coordinate_graph(coordinate_system: IDCoercible, max_depth: Union[Optional[int], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> GetCoordinateGraphQueryCoordinategraph:
    """GetCoordinateGraph 

Walk the coordinate graph out from one system: every coordinate system it reaches and every top-level edge between them. Reachability is undirected (an edge pointing into the system relates to it as much as one pointing out), the edges keep their true direction, and nothing is composed -- what the list queries cannot answer is 'which edges relate to *this* one', because relatedness is transitive and a filter is not

Args:
    coordinate_system (ID): No description
    max_depth (Optional[int], optional): No description. 
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    GetCoordinateGraphQueryCoordinategraph
"""
    variables: Dict[str, Any] = {}
    variables['coordinateSystem'] = coordinate_system
    if max_depth is not UNSET:
        variables['maxDepth'] = max_depth
    return execute(GetCoordinateGraphQuery, variables, rath=rath).coordinate_graph

async def aget_coordinate_system(id: IDCoercible, rath: Optional[MikroNextRath]=None) -> CoordinateSystem:
    """GetCoordinateSystem 

Get a single coordinate system by ID

Args:
    id (ID): No description
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    CoordinateSystem
"""
    variables: Dict[str, Any] = {}
    variables['id'] = id
    return (await aexecute(GetCoordinateSystemQuery, variables, rath=rath)).coordinate_system

def get_coordinate_system(id: IDCoercible, rath: Optional[MikroNextRath]=None) -> CoordinateSystem:
    """GetCoordinateSystem 

Get a single coordinate system by ID

Args:
    id (ID): No description
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    CoordinateSystem
"""
    variables: Dict[str, Any] = {}
    variables['id'] = id
    return execute(GetCoordinateSystemQuery, variables, rath=rath).coordinate_system

async def aget_coordinate_systems(filters: Union[Optional[CoordinateSystemFilter], UnsetType]=UNSET, pagination: Union[Optional[OffsetPaginationInput], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> Tuple[CoordinateSystem, ...]:
    """GetCoordinateSystems 

List coordinate systems (the nodes of the RFC-5 coordinate graph)

Args:
    filters (Optional[CoordinateSystemFilter], optional): No description. 
    pagination (Optional[OffsetPaginationInput], optional): No description. 
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    List[CoordinateSystem]
"""
    variables: Dict[str, Any] = {}
    if filters is not UNSET:
        variables['filters'] = filters
    if pagination is not UNSET:
        variables['pagination'] = pagination
    return (await aexecute(GetCoordinateSystemsQuery, variables, rath=rath)).coordinate_systems

def get_coordinate_systems(filters: Union[Optional[CoordinateSystemFilter], UnsetType]=UNSET, pagination: Union[Optional[OffsetPaginationInput], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> Tuple[CoordinateSystem, ...]:
    """GetCoordinateSystems 

List coordinate systems (the nodes of the RFC-5 coordinate graph)

Args:
    filters (Optional[CoordinateSystemFilter], optional): No description. 
    pagination (Optional[OffsetPaginationInput], optional): No description. 
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    List[CoordinateSystem]
"""
    variables: Dict[str, Any] = {}
    if filters is not UNSET:
        variables['filters'] = filters
    if pagination is not UNSET:
        variables['pagination'] = pagination
    return execute(GetCoordinateSystemsQuery, variables, rath=rath).coordinate_systems

async def asearch_coordinate_systems(search: Union[Optional[str], UnsetType]=UNSET, values: Union[Optional[List[IDCoercible]], UnsetType]=UNSET, limit: Union[Optional[int], UnsetType]=UNSET, offset: Union[Optional[int], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> Tuple[SearchCoordinateSystemsQueryOptions, ...]:
    """SearchCoordinateSystems 

List coordinate systems (the nodes of the RFC-5 coordinate graph)

Args:
    search (Optional[str], optional): No description. 
    values (Optional[List[ID]], optional): No description. 
    limit (Optional[int], optional): No description. 
    offset (Optional[int], optional): No description. Defaults to 0
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    List[SearchCoordinateSystemsQueryCoordinatesystems]
"""
    variables: Dict[str, Any] = {}
    if search is not UNSET:
        variables['search'] = search
    if values is not UNSET:
        variables['values'] = values
    if limit is not UNSET:
        variables['limit'] = limit
    if offset is not UNSET:
        variables['offset'] = offset
    return (await aexecute(SearchCoordinateSystemsQuery, variables, rath=rath)).options

def search_coordinate_systems(search: Union[Optional[str], UnsetType]=UNSET, values: Union[Optional[List[IDCoercible]], UnsetType]=UNSET, limit: Union[Optional[int], UnsetType]=UNSET, offset: Union[Optional[int], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> Tuple[SearchCoordinateSystemsQueryOptions, ...]:
    """SearchCoordinateSystems 

List coordinate systems (the nodes of the RFC-5 coordinate graph)

Args:
    search (Optional[str], optional): No description. 
    values (Optional[List[ID]], optional): No description. 
    limit (Optional[int], optional): No description. 
    offset (Optional[int], optional): No description. Defaults to 0
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    List[SearchCoordinateSystemsQueryCoordinatesystems]
"""
    variables: Dict[str, Any] = {}
    if search is not UNSET:
        variables['search'] = search
    if values is not UNSET:
        variables['values'] = values
    if limit is not UNSET:
        variables['limit'] = limit
    if offset is not UNSET:
        variables['offset'] = offset
    return execute(SearchCoordinateSystemsQuery, variables, rath=rath).options

async def aget_dataset(id: IDCoercible, rath: Optional[MikroNextRath]=None) -> Dataset:
    """GetDataset 

Get a single dataset by ID

Args:
    id (ID): The unique identifier of an object
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    Dataset
"""
    variables: Dict[str, Any] = {}
    variables['id'] = id
    return (await aexecute(GetDatasetQuery, variables, rath=rath)).dataset

def get_dataset(id: IDCoercible, rath: Optional[MikroNextRath]=None) -> Dataset:
    """GetDataset 

Get a single dataset by ID

Args:
    id (ID): The unique identifier of an object
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    Dataset
"""
    variables: Dict[str, Any] = {}
    variables['id'] = id
    return execute(GetDatasetQuery, variables, rath=rath).dataset

async def asearch_datasets(search: Union[Optional[str], UnsetType]=UNSET, values: Union[Optional[List[IDCoercible]], UnsetType]=UNSET, limit: Union[Optional[int], UnsetType]=UNSET, offset: Union[Optional[int], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> Tuple[SearchDatasetsQueryOptions, ...]:
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
    variables: Dict[str, Any] = {}
    if search is not UNSET:
        variables['search'] = search
    if values is not UNSET:
        variables['values'] = values
    if limit is not UNSET:
        variables['limit'] = limit
    if offset is not UNSET:
        variables['offset'] = offset
    return (await aexecute(SearchDatasetsQuery, variables, rath=rath)).options

def search_datasets(search: Union[Optional[str], UnsetType]=UNSET, values: Union[Optional[List[IDCoercible]], UnsetType]=UNSET, limit: Union[Optional[int], UnsetType]=UNSET, offset: Union[Optional[int], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> Tuple[SearchDatasetsQueryOptions, ...]:
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
    variables: Dict[str, Any] = {}
    if search is not UNSET:
        variables['search'] = search
    if values is not UNSET:
        variables['values'] = values
    if limit is not UNSET:
        variables['limit'] = limit
    if offset is not UNSET:
        variables['offset'] = offset
    return execute(SearchDatasetsQuery, variables, rath=rath).options

async def aget_file(id: IDCoercible, rath: Optional[MikroNextRath]=None) -> File:
    """GetFile 

Get a single file by ID

Args:
    id (ID): The unique identifier of an object
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    File
"""
    variables: Dict[str, Any] = {}
    variables['id'] = id
    return (await aexecute(GetFileQuery, variables, rath=rath)).file

def get_file(id: IDCoercible, rath: Optional[MikroNextRath]=None) -> File:
    """GetFile 

Get a single file by ID

Args:
    id (ID): The unique identifier of an object
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    File
"""
    variables: Dict[str, Any] = {}
    variables['id'] = id
    return execute(GetFileQuery, variables, rath=rath).file

async def asearch_files(search: Union[Optional[str], UnsetType]=UNSET, values: Union[Optional[List[IDCoercible]], UnsetType]=UNSET, limit: Union[Optional[int], UnsetType]=UNSET, offset: Union[Optional[int], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> Tuple[SearchFilesQueryOptions, ...]:
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
    variables: Dict[str, Any] = {}
    if search is not UNSET:
        variables['search'] = search
    if values is not UNSET:
        variables['values'] = values
    if limit is not UNSET:
        variables['limit'] = limit
    if offset is not UNSET:
        variables['offset'] = offset
    return (await aexecute(SearchFilesQuery, variables, rath=rath)).options

def search_files(search: Union[Optional[str], UnsetType]=UNSET, values: Union[Optional[List[IDCoercible]], UnsetType]=UNSET, limit: Union[Optional[int], UnsetType]=UNSET, offset: Union[Optional[int], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> Tuple[SearchFilesQueryOptions, ...]:
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
    variables: Dict[str, Any] = {}
    if search is not UNSET:
        variables['search'] = search
    if values is not UNSET:
        variables['values'] = values
    if limit is not UNSET:
        variables['limit'] = limit
    if offset is not UNSET:
        variables['offset'] = offset
    return execute(SearchFilesQuery, variables, rath=rath).options

async def aget_image(id: IDCoercible, rath: Optional[MikroNextRath]=None) -> Image:
    """GetImage 

Returns a single image by ID

Args:
    id (ID): The unique identifier of an object
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    Image
"""
    variables: Dict[str, Any] = {}
    variables['id'] = id
    return (await aexecute(GetImageQuery, variables, rath=rath)).image

def get_image(id: IDCoercible, rath: Optional[MikroNextRath]=None) -> Image:
    """GetImage 

Returns a single image by ID

Args:
    id (ID): The unique identifier of an object
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    Image
"""
    variables: Dict[str, Any] = {}
    variables['id'] = id
    return execute(GetImageQuery, variables, rath=rath).image

async def aget_random_image(rath: Optional[MikroNextRath]=None) -> Image:
    """GetRandomImage 

Get a random image of the current organization

Args:
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    Image
"""
    variables: Dict[str, Any] = {}
    return (await aexecute(GetRandomImageQuery, variables, rath=rath)).random_image

def get_random_image(rath: Optional[MikroNextRath]=None) -> Image:
    """GetRandomImage 

Get a random image of the current organization

Args:
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    Image
"""
    variables: Dict[str, Any] = {}
    return execute(GetRandomImageQuery, variables, rath=rath).random_image

async def asearch_images(search: Union[Optional[str], UnsetType]=UNSET, values: Union[Optional[List[IDCoercible]], UnsetType]=UNSET, limit: Union[Optional[int], UnsetType]=UNSET, offset: Union[Optional[int], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> Tuple[SearchImagesQueryOptions, ...]:
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
    variables: Dict[str, Any] = {}
    if search is not UNSET:
        variables['search'] = search
    if values is not UNSET:
        variables['values'] = values
    if limit is not UNSET:
        variables['limit'] = limit
    if offset is not UNSET:
        variables['offset'] = offset
    return (await aexecute(SearchImagesQuery, variables, rath=rath)).options

def search_images(search: Union[Optional[str], UnsetType]=UNSET, values: Union[Optional[List[IDCoercible]], UnsetType]=UNSET, limit: Union[Optional[int], UnsetType]=UNSET, offset: Union[Optional[int], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> Tuple[SearchImagesQueryOptions, ...]:
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
    variables: Dict[str, Any] = {}
    if search is not UNSET:
        variables['search'] = search
    if values is not UNSET:
        variables['values'] = values
    if limit is not UNSET:
        variables['limit'] = limit
    if offset is not UNSET:
        variables['offset'] = offset
    return execute(SearchImagesQuery, variables, rath=rath).options

async def aimages(filter: Union[Optional[ImageFilter], UnsetType]=UNSET, pagination: Union[Optional[OffsetPaginationInput], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> Tuple[Image, ...]:
    """Images 

List images in the current organization, filterable and orderable

Args:
    filter (Optional[ImageFilter], optional): No description. 
    pagination (Optional[OffsetPaginationInput], optional): No description. 
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    List[Image]
"""
    variables: Dict[str, Any] = {}
    if filter is not UNSET:
        variables['filter'] = filter
    if pagination is not UNSET:
        variables['pagination'] = pagination
    return (await aexecute(ImagesQuery, variables, rath=rath)).images

def images(filter: Union[Optional[ImageFilter], UnsetType]=UNSET, pagination: Union[Optional[OffsetPaginationInput], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> Tuple[Image, ...]:
    """Images 

List images in the current organization, filterable and orderable

Args:
    filter (Optional[ImageFilter], optional): No description. 
    pagination (Optional[OffsetPaginationInput], optional): No description. 
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    List[Image]
"""
    variables: Dict[str, Any] = {}
    if filter is not UNSET:
        variables['filter'] = filter
    if pagination is not UNSET:
        variables['pagination'] = pagination
    return execute(ImagesQuery, variables, rath=rath).images

async def aview_image(id: IDCoercible, filtersggg: Union[Optional[ViewFilter], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> ViewImageQueryImage:
    """ViewImage 

Returns a single image by ID

Args:
    id (ID): The unique identifier of an object
    filtersggg (Optional[ViewFilter], optional): No description. 
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    ViewImageQueryImage
"""
    variables: Dict[str, Any] = {}
    variables['id'] = id
    if filtersggg is not UNSET:
        variables['filtersggg'] = filtersggg
    return (await aexecute(ViewImageQuery, variables, rath=rath)).image

def view_image(id: IDCoercible, filtersggg: Union[Optional[ViewFilter], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> ViewImageQueryImage:
    """ViewImage 

Returns a single image by ID

Args:
    id (ID): The unique identifier of an object
    filtersggg (Optional[ViewFilter], optional): No description. 
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    ViewImageQueryImage
"""
    variables: Dict[str, Any] = {}
    variables['id'] = id
    if filtersggg is not UNSET:
        variables['filtersggg'] = filtersggg
    return execute(ViewImageQuery, variables, rath=rath).image

async def aartemiy_images(rath: Optional[MikroNextRath]=None) -> Tuple[ArtemiyImagesQueryImages, ...]:
    """ArtemiyImages 

List images in the current organization, filterable and orderable

Args:
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    List[ArtemiyImagesQueryImages]
"""
    variables: Dict[str, Any] = {}
    return (await aexecute(ArtemiyImagesQuery, variables, rath=rath)).images

def artemiy_images(rath: Optional[MikroNextRath]=None) -> Tuple[ArtemiyImagesQueryImages, ...]:
    """ArtemiyImages 

List images in the current organization, filterable and orderable

Args:
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    List[ArtemiyImagesQueryImages]
"""
    variables: Dict[str, Any] = {}
    return execute(ArtemiyImagesQuery, variables, rath=rath).images

async def aget_instrument(id: IDCoercible, rath: Optional[MikroNextRath]=None) -> Instrument:
    """GetInstrument 

Get a single instrument by ID

Args:
    id (ID): The unique identifier of an object
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    Instrument
"""
    variables: Dict[str, Any] = {}
    variables['id'] = id
    return (await aexecute(GetInstrumentQuery, variables, rath=rath)).instrument

def get_instrument(id: IDCoercible, rath: Optional[MikroNextRath]=None) -> Instrument:
    """GetInstrument 

Get a single instrument by ID

Args:
    id (ID): The unique identifier of an object
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    Instrument
"""
    variables: Dict[str, Any] = {}
    variables['id'] = id
    return execute(GetInstrumentQuery, variables, rath=rath).instrument

async def aget_lens(id: IDCoercible, rath: Optional[MikroNextRath]=None) -> Lens:
    """GetLens 

Get a single lens by ID

Args:
    id (ID): No description
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    Lens
"""
    variables: Dict[str, Any] = {}
    variables['id'] = id
    return (await aexecute(GetLensQuery, variables, rath=rath)).lens

def get_lens(id: IDCoercible, rath: Optional[MikroNextRath]=None) -> Lens:
    """GetLens 

Get a single lens by ID

Args:
    id (ID): No description
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    Lens
"""
    variables: Dict[str, Any] = {}
    variables['id'] = id
    return execute(GetLensQuery, variables, rath=rath).lens

async def aget_mesh_collection(id: IDCoercible, rath: Optional[MikroNextRath]=None) -> MeshCollection:
    """GetMeshCollection 

Get a single mesh collection by ID

Args:
    id (ID): No description
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    MeshCollection
"""
    variables: Dict[str, Any] = {}
    variables['id'] = id
    return (await aexecute(GetMeshCollectionQuery, variables, rath=rath)).mesh_collection

def get_mesh_collection(id: IDCoercible, rath: Optional[MikroNextRath]=None) -> MeshCollection:
    """GetMeshCollection 

Get a single mesh collection by ID

Args:
    id (ID): No description
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    MeshCollection
"""
    variables: Dict[str, Any] = {}
    variables['id'] = id
    return execute(GetMeshCollectionQuery, variables, rath=rath).mesh_collection

async def aget_mesh_collections(filters: Union[Optional[MeshCollectionFilter], UnsetType]=UNSET, pagination: Union[Optional[OffsetPaginationInput], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> Tuple[MeshCollection, ...]:
    """GetMeshCollections 

List mesh collections (immutable, versioned Parquet-backed mesh sets, each in a coordinate system of its own)

Args:
    filters (Optional[MeshCollectionFilter], optional): No description. 
    pagination (Optional[OffsetPaginationInput], optional): No description. 
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    List[MeshCollection]
"""
    variables: Dict[str, Any] = {}
    if filters is not UNSET:
        variables['filters'] = filters
    if pagination is not UNSET:
        variables['pagination'] = pagination
    return (await aexecute(GetMeshCollectionsQuery, variables, rath=rath)).mesh_collections

def get_mesh_collections(filters: Union[Optional[MeshCollectionFilter], UnsetType]=UNSET, pagination: Union[Optional[OffsetPaginationInput], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> Tuple[MeshCollection, ...]:
    """GetMeshCollections 

List mesh collections (immutable, versioned Parquet-backed mesh sets, each in a coordinate system of its own)

Args:
    filters (Optional[MeshCollectionFilter], optional): No description. 
    pagination (Optional[OffsetPaginationInput], optional): No description. 
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    List[MeshCollection]
"""
    variables: Dict[str, Any] = {}
    if filters is not UNSET:
        variables['filters'] = filters
    if pagination is not UNSET:
        variables['pagination'] = pagination
    return execute(GetMeshCollectionsQuery, variables, rath=rath).mesh_collections

async def asearch_mesh_collections(search: Union[Optional[str], UnsetType]=UNSET, values: Union[Optional[List[IDCoercible]], UnsetType]=UNSET, limit: Union[Optional[int], UnsetType]=UNSET, offset: Union[Optional[int], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> Tuple[SearchMeshCollectionsQueryOptions, ...]:
    """SearchMeshCollections 

List mesh collections (immutable, versioned Parquet-backed mesh sets, each in a coordinate system of its own)

Args:
    search (Optional[str], optional): No description. 
    values (Optional[List[ID]], optional): No description. 
    limit (Optional[int], optional): No description. 
    offset (Optional[int], optional): No description. Defaults to 0
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    List[SearchMeshCollectionsQueryMeshcollections]
"""
    variables: Dict[str, Any] = {}
    if search is not UNSET:
        variables['search'] = search
    if values is not UNSET:
        variables['values'] = values
    if limit is not UNSET:
        variables['limit'] = limit
    if offset is not UNSET:
        variables['offset'] = offset
    return (await aexecute(SearchMeshCollectionsQuery, variables, rath=rath)).options

def search_mesh_collections(search: Union[Optional[str], UnsetType]=UNSET, values: Union[Optional[List[IDCoercible]], UnsetType]=UNSET, limit: Union[Optional[int], UnsetType]=UNSET, offset: Union[Optional[int], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> Tuple[SearchMeshCollectionsQueryOptions, ...]:
    """SearchMeshCollections 

List mesh collections (immutable, versioned Parquet-backed mesh sets, each in a coordinate system of its own)

Args:
    search (Optional[str], optional): No description. 
    values (Optional[List[ID]], optional): No description. 
    limit (Optional[int], optional): No description. 
    offset (Optional[int], optional): No description. Defaults to 0
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    List[SearchMeshCollectionsQueryMeshcollections]
"""
    variables: Dict[str, Any] = {}
    if search is not UNSET:
        variables['search'] = search
    if values is not UNSET:
        variables['values'] = values
    if limit is not UNSET:
        variables['limit'] = limit
    if offset is not UNSET:
        variables['offset'] = offset
    return execute(SearchMeshCollectionsQuery, variables, rath=rath).options

async def aget_objective(id: IDCoercible, rath: Optional[MikroNextRath]=None) -> Objective:
    """GetObjective 

Get a single objective by ID

Args:
    id (ID): The unique identifier of an object
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    Objective
"""
    variables: Dict[str, Any] = {}
    variables['id'] = id
    return (await aexecute(GetObjectiveQuery, variables, rath=rath)).objective

def get_objective(id: IDCoercible, rath: Optional[MikroNextRath]=None) -> Objective:
    """GetObjective 

Get a single objective by ID

Args:
    id (ID): The unique identifier of an object
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    Objective
"""
    variables: Dict[str, Any] = {}
    variables['id'] = id
    return execute(GetObjectiveQuery, variables, rath=rath).objective

async def aget_rgb_context(id: IDCoercible, rath: Optional[MikroNextRath]=None) -> RGBContext:
    """GetRGBContext 

Get a single RGB render context by ID

Args:
    id (ID): The unique identifier of an object
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    RGBContext
"""
    variables: Dict[str, Any] = {}
    variables['id'] = id
    return (await aexecute(GetRGBContextQuery, variables, rath=rath)).rgbcontext

def get_rgb_context(id: IDCoercible, rath: Optional[MikroNextRath]=None) -> RGBContext:
    """GetRGBContext 

Get a single RGB render context by ID

Args:
    id (ID): The unique identifier of an object
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    RGBContext
"""
    variables: Dict[str, Any] = {}
    variables['id'] = id
    return execute(GetRGBContextQuery, variables, rath=rath).rgbcontext

async def aget_rois(image: IDCoercible, rath: Optional[MikroNextRath]=None) -> Tuple[ROI, ...]:
    """GetRois 

List regions of interest drawn on images

Args:
    image (ID): No description
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    List[ROI]
"""
    variables: Dict[str, Any] = {}
    variables['image'] = image
    return (await aexecute(GetRoisQuery, variables, rath=rath)).rois

def get_rois(image: IDCoercible, rath: Optional[MikroNextRath]=None) -> Tuple[ROI, ...]:
    """GetRois 

List regions of interest drawn on images

Args:
    image (ID): No description
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    List[ROI]
"""
    variables: Dict[str, Any] = {}
    variables['image'] = image
    return execute(GetRoisQuery, variables, rath=rath).rois

async def aget_roi(id: IDCoercible, rath: Optional[MikroNextRath]=None) -> ROI:
    """GetRoi 

Get a single region of interest by ID

Args:
    id (ID): The unique identifier of an object
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    ROI
"""
    variables: Dict[str, Any] = {}
    variables['id'] = id
    return (await aexecute(GetRoiQuery, variables, rath=rath)).roi

def get_roi(id: IDCoercible, rath: Optional[MikroNextRath]=None) -> ROI:
    """GetRoi 

Get a single region of interest by ID

Args:
    id (ID): The unique identifier of an object
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    ROI
"""
    variables: Dict[str, Any] = {}
    variables['id'] = id
    return execute(GetRoiQuery, variables, rath=rath).roi

async def asearch_rois(search: Union[Optional[str], UnsetType]=UNSET, values: Union[Optional[List[IDCoercible]], UnsetType]=UNSET, limit: Union[Optional[int], UnsetType]=UNSET, offset: Union[Optional[int], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> Tuple[SearchRoisQueryOptions, ...]:
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
    variables: Dict[str, Any] = {}
    if search is not UNSET:
        variables['search'] = search
    if values is not UNSET:
        variables['values'] = values
    if limit is not UNSET:
        variables['limit'] = limit
    if offset is not UNSET:
        variables['offset'] = offset
    return (await aexecute(SearchRoisQuery, variables, rath=rath)).options

def search_rois(search: Union[Optional[str], UnsetType]=UNSET, values: Union[Optional[List[IDCoercible]], UnsetType]=UNSET, limit: Union[Optional[int], UnsetType]=UNSET, offset: Union[Optional[int], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> Tuple[SearchRoisQueryOptions, ...]:
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
    variables: Dict[str, Any] = {}
    if search is not UNSET:
        variables['search'] = search
    if values is not UNSET:
        variables['values'] = values
    if limit is not UNSET:
        variables['limit'] = limit
    if offset is not UNSET:
        variables['offset'] = offset
    return execute(SearchRoisQuery, variables, rath=rath).options

async def aget_scene(id: IDCoercible, rath: Optional[MikroNextRath]=None) -> Scene:
    """GetScene 

Get a single scene by ID

Args:
    id (ID): No description
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    Scene
"""
    variables: Dict[str, Any] = {}
    variables['id'] = id
    return (await aexecute(GetSceneQuery, variables, rath=rath)).scene

def get_scene(id: IDCoercible, rath: Optional[MikroNextRath]=None) -> Scene:
    """GetScene 

Get a single scene by ID

Args:
    id (ID): No description
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    Scene
"""
    variables: Dict[str, Any] = {}
    variables['id'] = id
    return execute(GetSceneQuery, variables, rath=rath).scene

async def asearch_scenes(search: Union[Optional[str], UnsetType]=UNSET, values: Union[Optional[List[IDCoercible]], UnsetType]=UNSET, limit: Union[Optional[int], UnsetType]=UNSET, offset: Union[Optional[int], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> Tuple[SearchScenesQueryOptions, ...]:
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
    variables: Dict[str, Any] = {}
    if search is not UNSET:
        variables['search'] = search
    if values is not UNSET:
        variables['values'] = values
    if limit is not UNSET:
        variables['limit'] = limit
    if offset is not UNSET:
        variables['offset'] = offset
    return (await aexecute(SearchScenesQuery, variables, rath=rath)).options

def search_scenes(search: Union[Optional[str], UnsetType]=UNSET, values: Union[Optional[List[IDCoercible]], UnsetType]=UNSET, limit: Union[Optional[int], UnsetType]=UNSET, offset: Union[Optional[int], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> Tuple[SearchScenesQueryOptions, ...]:
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
    variables: Dict[str, Any] = {}
    if search is not UNSET:
        variables['search'] = search
    if values is not UNSET:
        variables['values'] = values
    if limit is not UNSET:
        variables['limit'] = limit
    if offset is not UNSET:
        variables['offset'] = offset
    return execute(SearchScenesQuery, variables, rath=rath).options

async def aget_scene_snapshot(id: IDCoercible, rath: Optional[MikroNextRath]=None) -> SceneSnapshot:
    """GetSceneSnapshot 

Get a single scene snapshot by ID

Args:
    id (ID): The unique identifier of an object
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    SceneSnapshot
"""
    variables: Dict[str, Any] = {}
    variables['id'] = id
    return (await aexecute(GetSceneSnapshotQuery, variables, rath=rath)).scene_snapshot

def get_scene_snapshot(id: IDCoercible, rath: Optional[MikroNextRath]=None) -> SceneSnapshot:
    """GetSceneSnapshot 

Get a single scene snapshot by ID

Args:
    id (ID): The unique identifier of an object
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    SceneSnapshot
"""
    variables: Dict[str, Any] = {}
    variables['id'] = id
    return execute(GetSceneSnapshotQuery, variables, rath=rath).scene_snapshot

async def aget_scene_snapshots(filters: Union[Optional[SceneSnapshotFilter], UnsetType]=UNSET, pagination: Union[Optional[OffsetPaginationInput], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> Tuple[SceneSnapshot, ...]:
    """GetSceneSnapshots 

List scene snapshots (pre-rendered pictures of a composition, for previewing it without compositing the layers)

Args:
    filters (Optional[SceneSnapshotFilter], optional): No description. 
    pagination (Optional[OffsetPaginationInput], optional): No description. 
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    List[SceneSnapshot]
"""
    variables: Dict[str, Any] = {}
    if filters is not UNSET:
        variables['filters'] = filters
    if pagination is not UNSET:
        variables['pagination'] = pagination
    return (await aexecute(GetSceneSnapshotsQuery, variables, rath=rath)).scene_snapshots

def get_scene_snapshots(filters: Union[Optional[SceneSnapshotFilter], UnsetType]=UNSET, pagination: Union[Optional[OffsetPaginationInput], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> Tuple[SceneSnapshot, ...]:
    """GetSceneSnapshots 

List scene snapshots (pre-rendered pictures of a composition, for previewing it without compositing the layers)

Args:
    filters (Optional[SceneSnapshotFilter], optional): No description. 
    pagination (Optional[OffsetPaginationInput], optional): No description. 
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    List[SceneSnapshot]
"""
    variables: Dict[str, Any] = {}
    if filters is not UNSET:
        variables['filters'] = filters
    if pagination is not UNSET:
        variables['pagination'] = pagination
    return execute(GetSceneSnapshotsQuery, variables, rath=rath).scene_snapshots

async def asearch_scene_snapshots(search: Union[Optional[str], UnsetType]=UNSET, values: Union[Optional[List[IDCoercible]], UnsetType]=UNSET, limit: Union[Optional[int], UnsetType]=UNSET, offset: Union[Optional[int], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> Tuple[SearchSceneSnapshotsQueryOptions, ...]:
    """SearchSceneSnapshots 

List scene snapshots (pre-rendered pictures of a composition, for previewing it without compositing the layers)

Args:
    search (Optional[str], optional): No description. 
    values (Optional[List[ID]], optional): No description. 
    limit (Optional[int], optional): No description. 
    offset (Optional[int], optional): No description. Defaults to 0
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    List[SearchSceneSnapshotsQueryScenesnapshots]
"""
    variables: Dict[str, Any] = {}
    if search is not UNSET:
        variables['search'] = search
    if values is not UNSET:
        variables['values'] = values
    if limit is not UNSET:
        variables['limit'] = limit
    if offset is not UNSET:
        variables['offset'] = offset
    return (await aexecute(SearchSceneSnapshotsQuery, variables, rath=rath)).options

def search_scene_snapshots(search: Union[Optional[str], UnsetType]=UNSET, values: Union[Optional[List[IDCoercible]], UnsetType]=UNSET, limit: Union[Optional[int], UnsetType]=UNSET, offset: Union[Optional[int], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> Tuple[SearchSceneSnapshotsQueryOptions, ...]:
    """SearchSceneSnapshots 

List scene snapshots (pre-rendered pictures of a composition, for previewing it without compositing the layers)

Args:
    search (Optional[str], optional): No description. 
    values (Optional[List[ID]], optional): No description. 
    limit (Optional[int], optional): No description. 
    offset (Optional[int], optional): No description. Defaults to 0
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    List[SearchSceneSnapshotsQueryScenesnapshots]
"""
    variables: Dict[str, Any] = {}
    if search is not UNSET:
        variables['search'] = search
    if values is not UNSET:
        variables['values'] = values
    if limit is not UNSET:
        variables['limit'] = limit
    if offset is not UNSET:
        variables['offset'] = offset
    return execute(SearchSceneSnapshotsQuery, variables, rath=rath).options

async def aget_snapshot(id: IDCoercible, rath: Optional[MikroNextRath]=None) -> Snapshot:
    """GetSnapshot 

Get a single snapshot by ID

Args:
    id (ID): The unique identifier of an object
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    Snapshot
"""
    variables: Dict[str, Any] = {}
    variables['id'] = id
    return (await aexecute(GetSnapshotQuery, variables, rath=rath)).snapshot

def get_snapshot(id: IDCoercible, rath: Optional[MikroNextRath]=None) -> Snapshot:
    """GetSnapshot 

Get a single snapshot by ID

Args:
    id (ID): The unique identifier of an object
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    Snapshot
"""
    variables: Dict[str, Any] = {}
    variables['id'] = id
    return execute(GetSnapshotQuery, variables, rath=rath).snapshot

async def asearch_snapshots(search: Union[Optional[str], UnsetType]=UNSET, values: Union[Optional[List[IDCoercible]], UnsetType]=UNSET, limit: Union[Optional[int], UnsetType]=UNSET, offset: Union[Optional[int], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> Tuple[SearchSnapshotsQueryOptions, ...]:
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
    variables: Dict[str, Any] = {}
    if search is not UNSET:
        variables['search'] = search
    if values is not UNSET:
        variables['values'] = values
    if limit is not UNSET:
        variables['limit'] = limit
    if offset is not UNSET:
        variables['offset'] = offset
    return (await aexecute(SearchSnapshotsQuery, variables, rath=rath)).options

def search_snapshots(search: Union[Optional[str], UnsetType]=UNSET, values: Union[Optional[List[IDCoercible]], UnsetType]=UNSET, limit: Union[Optional[int], UnsetType]=UNSET, offset: Union[Optional[int], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> Tuple[SearchSnapshotsQueryOptions, ...]:
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
    variables: Dict[str, Any] = {}
    if search is not UNSET:
        variables['search'] = search
    if values is not UNSET:
        variables['values'] = values
    if limit is not UNSET:
        variables['limit'] = limit
    if offset is not UNSET:
        variables['offset'] = offset
    return execute(SearchSnapshotsQuery, variables, rath=rath).options

async def aget_stage(id: IDCoercible, rath: Optional[MikroNextRath]=None) -> Stage:
    """GetStage 

Get a single stage by ID

Args:
    id (ID): The unique identifier of an object
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    Stage
"""
    variables: Dict[str, Any] = {}
    variables['id'] = id
    return (await aexecute(GetStageQuery, variables, rath=rath)).stage

def get_stage(id: IDCoercible, rath: Optional[MikroNextRath]=None) -> Stage:
    """GetStage 

Get a single stage by ID

Args:
    id (ID): The unique identifier of an object
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    Stage
"""
    variables: Dict[str, Any] = {}
    variables['id'] = id
    return execute(GetStageQuery, variables, rath=rath).stage

async def asearch_stages(search: Union[Optional[str], UnsetType]=UNSET, values: Union[Optional[List[IDCoercible]], UnsetType]=UNSET, limit: Union[Optional[int], UnsetType]=UNSET, offset: Union[Optional[int], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> Tuple[SearchStagesQueryOptions, ...]:
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
    variables: Dict[str, Any] = {}
    if search is not UNSET:
        variables['search'] = search
    if values is not UNSET:
        variables['values'] = values
    if limit is not UNSET:
        variables['limit'] = limit
    if offset is not UNSET:
        variables['offset'] = offset
    return (await aexecute(SearchStagesQuery, variables, rath=rath)).options

def search_stages(search: Union[Optional[str], UnsetType]=UNSET, values: Union[Optional[List[IDCoercible]], UnsetType]=UNSET, limit: Union[Optional[int], UnsetType]=UNSET, offset: Union[Optional[int], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> Tuple[SearchStagesQueryOptions, ...]:
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
    variables: Dict[str, Any] = {}
    if search is not UNSET:
        variables['search'] = search
    if values is not UNSET:
        variables['values'] = values
    if limit is not UNSET:
        variables['limit'] = limit
    if offset is not UNSET:
        variables['offset'] = offset
    return execute(SearchStagesQuery, variables, rath=rath).options

async def aget_table(id: IDCoercible, rath: Optional[MikroNextRath]=None) -> Table:
    """GetTable 

Get a single table by ID

Args:
    id (ID): The unique identifier of an object
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    Table
"""
    variables: Dict[str, Any] = {}
    variables['id'] = id
    return (await aexecute(GetTableQuery, variables, rath=rath)).table

def get_table(id: IDCoercible, rath: Optional[MikroNextRath]=None) -> Table:
    """GetTable 

Get a single table by ID

Args:
    id (ID): The unique identifier of an object
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    Table
"""
    variables: Dict[str, Any] = {}
    variables['id'] = id
    return execute(GetTableQuery, variables, rath=rath).table

async def asearch_tables(search: Union[Optional[str], UnsetType]=UNSET, values: Union[Optional[List[IDCoercible]], UnsetType]=UNSET, limit: Union[Optional[int], UnsetType]=UNSET, offset: Union[Optional[int], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> Tuple[SearchTablesQueryOptions, ...]:
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
    variables: Dict[str, Any] = {}
    if search is not UNSET:
        variables['search'] = search
    if values is not UNSET:
        variables['values'] = values
    if limit is not UNSET:
        variables['limit'] = limit
    if offset is not UNSET:
        variables['offset'] = offset
    return (await aexecute(SearchTablesQuery, variables, rath=rath)).options

def search_tables(search: Union[Optional[str], UnsetType]=UNSET, values: Union[Optional[List[IDCoercible]], UnsetType]=UNSET, limit: Union[Optional[int], UnsetType]=UNSET, offset: Union[Optional[int], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> Tuple[SearchTablesQueryOptions, ...]:
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
    variables: Dict[str, Any] = {}
    if search is not UNSET:
        variables['search'] = search
    if values is not UNSET:
        variables['values'] = values
    if limit is not UNSET:
        variables['limit'] = limit
    if offset is not UNSET:
        variables['offset'] = offset
    return execute(SearchTablesQuery, variables, rath=rath).options

async def aget_table_cell(id: IDCoercible, rath: Optional[MikroNextRath]=None) -> TableCell:
    """GetTableCell 

Get a single table cell by its compound ID (tableId-rowId-columnId)

Args:
    id (ID): The unique identifier of an object
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    TableCell
"""
    variables: Dict[str, Any] = {}
    variables['id'] = id
    return (await aexecute(GetTableCellQuery, variables, rath=rath)).table_cell

def get_table_cell(id: IDCoercible, rath: Optional[MikroNextRath]=None) -> TableCell:
    """GetTableCell 

Get a single table cell by its compound ID (tableId-rowId-columnId)

Args:
    id (ID): The unique identifier of an object
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    TableCell
"""
    variables: Dict[str, Any] = {}
    variables['id'] = id
    return execute(GetTableCellQuery, variables, rath=rath).table_cell

async def asearch_table_cells(table: IDCoercible, search: Union[Optional[str], UnsetType]=UNSET, values: Union[Optional[List[IDCoercible]], UnsetType]=UNSET, limit: Union[Optional[int], UnsetType]=UNSET, offset: Union[Optional[int], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> Tuple[SearchTableCellsQueryOptions, ...]:
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
    variables: Dict[str, Any] = {}
    if search is not UNSET:
        variables['search'] = search
    if values is not UNSET:
        variables['values'] = values
    variables['table'] = table
    if limit is not UNSET:
        variables['limit'] = limit
    if offset is not UNSET:
        variables['offset'] = offset
    return (await aexecute(SearchTableCellsQuery, variables, rath=rath)).options

def search_table_cells(table: IDCoercible, search: Union[Optional[str], UnsetType]=UNSET, values: Union[Optional[List[IDCoercible]], UnsetType]=UNSET, limit: Union[Optional[int], UnsetType]=UNSET, offset: Union[Optional[int], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> Tuple[SearchTableCellsQueryOptions, ...]:
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
    variables: Dict[str, Any] = {}
    if search is not UNSET:
        variables['search'] = search
    if values is not UNSET:
        variables['values'] = values
    variables['table'] = table
    if limit is not UNSET:
        variables['limit'] = limit
    if offset is not UNSET:
        variables['offset'] = offset
    return execute(SearchTableCellsQuery, variables, rath=rath).options

async def aget_table_dataset(id: IDCoercible, rath: Optional[MikroNextRath]=None) -> TableDataset:
    """GetTableDataset 

Get a single table dataset by ID

Args:
    id (ID): No description
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    TableDataset
"""
    variables: Dict[str, Any] = {}
    variables['id'] = id
    return (await aexecute(GetTableDatasetQuery, variables, rath=rath)).table_dataset

def get_table_dataset(id: IDCoercible, rath: Optional[MikroNextRath]=None) -> TableDataset:
    """GetTableDataset 

Get a single table dataset by ID

Args:
    id (ID): No description
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    TableDataset
"""
    variables: Dict[str, Any] = {}
    variables['id'] = id
    return execute(GetTableDatasetQuery, variables, rath=rath).table_dataset

async def aget_table_datasets(filters: Union[Optional[TableDatasetFilter], UnsetType]=UNSET, pagination: Union[Optional[OffsetPaginationInput], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> Tuple[TableDataset, ...]:
    """GetTableDatasets 

List table datasets (Parquet-backed tables of scientific records: measurements, localizations, expression levels)

Args:
    filters (Optional[TableDatasetFilter], optional): No description. 
    pagination (Optional[OffsetPaginationInput], optional): No description. 
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    List[TableDataset]
"""
    variables: Dict[str, Any] = {}
    if filters is not UNSET:
        variables['filters'] = filters
    if pagination is not UNSET:
        variables['pagination'] = pagination
    return (await aexecute(GetTableDatasetsQuery, variables, rath=rath)).table_datasets

def get_table_datasets(filters: Union[Optional[TableDatasetFilter], UnsetType]=UNSET, pagination: Union[Optional[OffsetPaginationInput], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> Tuple[TableDataset, ...]:
    """GetTableDatasets 

List table datasets (Parquet-backed tables of scientific records: measurements, localizations, expression levels)

Args:
    filters (Optional[TableDatasetFilter], optional): No description. 
    pagination (Optional[OffsetPaginationInput], optional): No description. 
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    List[TableDataset]
"""
    variables: Dict[str, Any] = {}
    if filters is not UNSET:
        variables['filters'] = filters
    if pagination is not UNSET:
        variables['pagination'] = pagination
    return execute(GetTableDatasetsQuery, variables, rath=rath).table_datasets

async def aget_table_row(id: IDCoercible, rath: Optional[MikroNextRath]=None) -> TableRow:
    """GetTableRow 

Get a single table row by its compound ID (tableId-rowId)

Args:
    id (ID): The unique identifier of an object
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    TableRow
"""
    variables: Dict[str, Any] = {}
    variables['id'] = id
    return (await aexecute(GetTableRowQuery, variables, rath=rath)).table_row

def get_table_row(id: IDCoercible, rath: Optional[MikroNextRath]=None) -> TableRow:
    """GetTableRow 

Get a single table row by its compound ID (tableId-rowId)

Args:
    id (ID): The unique identifier of an object
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    TableRow
"""
    variables: Dict[str, Any] = {}
    variables['id'] = id
    return execute(GetTableRowQuery, variables, rath=rath).table_row

async def asearch_table_rows(table: IDCoercible, search: Union[Optional[str], UnsetType]=UNSET, values: Union[Optional[List[IDCoercible]], UnsetType]=UNSET, limit: Union[Optional[int], UnsetType]=UNSET, offset: Union[Optional[int], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> Tuple[SearchTableRowsQueryOptions, ...]:
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
    variables: Dict[str, Any] = {}
    if search is not UNSET:
        variables['search'] = search
    if values is not UNSET:
        variables['values'] = values
    variables['table'] = table
    if limit is not UNSET:
        variables['limit'] = limit
    if offset is not UNSET:
        variables['offset'] = offset
    return (await aexecute(SearchTableRowsQuery, variables, rath=rath)).options

def search_table_rows(table: IDCoercible, search: Union[Optional[str], UnsetType]=UNSET, values: Union[Optional[List[IDCoercible]], UnsetType]=UNSET, limit: Union[Optional[int], UnsetType]=UNSET, offset: Union[Optional[int], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> Tuple[SearchTableRowsQueryOptions, ...]:
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
    variables: Dict[str, Any] = {}
    if search is not UNSET:
        variables['search'] = search
    if values is not UNSET:
        variables['values'] = values
    variables['table'] = table
    if limit is not UNSET:
        variables['limit'] = limit
    if offset is not UNSET:
        variables['offset'] = offset
    return execute(SearchTableRowsQuery, variables, rath=rath).options

async def aget_transformation(id: IDCoercible, rath: Optional[MikroNextRath]=None) -> Union[Annotated[Union[GetTransformationQueryTransformationBaseAffineTransformation, GetTransformationQueryTransformationBaseBijectionTransformation, GetTransformationQueryTransformationBaseByDimensionTransformation, GetTransformationQueryTransformationBaseFieldTransformation, GetTransformationQueryTransformationBaseIdentityTransformation, GetTransformationQueryTransformationBaseMapAxisTransformation, GetTransformationQueryTransformationBaseRotationTransformation, GetTransformationQueryTransformationBaseScaleTransformation, GetTransformationQueryTransformationBaseSequenceTransformation, GetTransformationQueryTransformationBaseTranslationTransformation, GetTransformationQueryTransformationBaseUnmappableTransformation], Field(discriminator='typename')], GetTransformationQueryTransformationBaseCatchAll]:
    """GetTransformation 

Get a single transformation by ID

Args:
    id (ID): No description
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    Transformation
"""
    variables: Dict[str, Any] = {}
    variables['id'] = id
    return (await aexecute(GetTransformationQuery, variables, rath=rath)).transformation

def get_transformation(id: IDCoercible, rath: Optional[MikroNextRath]=None) -> Union[Annotated[Union[GetTransformationQueryTransformationBaseAffineTransformation, GetTransformationQueryTransformationBaseBijectionTransformation, GetTransformationQueryTransformationBaseByDimensionTransformation, GetTransformationQueryTransformationBaseFieldTransformation, GetTransformationQueryTransformationBaseIdentityTransformation, GetTransformationQueryTransformationBaseMapAxisTransformation, GetTransformationQueryTransformationBaseRotationTransformation, GetTransformationQueryTransformationBaseScaleTransformation, GetTransformationQueryTransformationBaseSequenceTransformation, GetTransformationQueryTransformationBaseTranslationTransformation, GetTransformationQueryTransformationBaseUnmappableTransformation], Field(discriminator='typename')], GetTransformationQueryTransformationBaseCatchAll]:
    """GetTransformation 

Get a single transformation by ID

Args:
    id (ID): No description
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    Transformation
"""
    variables: Dict[str, Any] = {}
    variables['id'] = id
    return execute(GetTransformationQuery, variables, rath=rath).transformation

async def aget_transformations(filters: Union[Optional[TransformationFilter], UnsetType]=UNSET, pagination: Union[Optional[OffsetPaginationInput], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> Tuple[Union[Annotated[Union[GetTransformationsQueryTransformationsBaseAffineTransformation, GetTransformationsQueryTransformationsBaseBijectionTransformation, GetTransformationsQueryTransformationsBaseByDimensionTransformation, GetTransformationsQueryTransformationsBaseFieldTransformation, GetTransformationsQueryTransformationsBaseIdentityTransformation, GetTransformationsQueryTransformationsBaseMapAxisTransformation, GetTransformationsQueryTransformationsBaseRotationTransformation, GetTransformationsQueryTransformationsBaseScaleTransformation, GetTransformationsQueryTransformationsBaseSequenceTransformation, GetTransformationsQueryTransformationsBaseTranslationTransformation, GetTransformationsQueryTransformationsBaseUnmappableTransformation], Field(discriminator='typename')], GetTransformationsQueryTransformationsBaseCatchAll], ...]:
    """GetTransformations 

List transformations (the directed edges of the coordinate graph). Compose them client-side; the server never resolves a path to world, because the same dataset can sit in two scenes under two registrations

Args:
    filters (Optional[TransformationFilter], optional): No description. 
    pagination (Optional[OffsetPaginationInput], optional): No description. 
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    List[Transformation]
"""
    variables: Dict[str, Any] = {}
    if filters is not UNSET:
        variables['filters'] = filters
    if pagination is not UNSET:
        variables['pagination'] = pagination
    return (await aexecute(GetTransformationsQuery, variables, rath=rath)).transformations

def get_transformations(filters: Union[Optional[TransformationFilter], UnsetType]=UNSET, pagination: Union[Optional[OffsetPaginationInput], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> Tuple[Union[Annotated[Union[GetTransformationsQueryTransformationsBaseAffineTransformation, GetTransformationsQueryTransformationsBaseBijectionTransformation, GetTransformationsQueryTransformationsBaseByDimensionTransformation, GetTransformationsQueryTransformationsBaseFieldTransformation, GetTransformationsQueryTransformationsBaseIdentityTransformation, GetTransformationsQueryTransformationsBaseMapAxisTransformation, GetTransformationsQueryTransformationsBaseRotationTransformation, GetTransformationsQueryTransformationsBaseScaleTransformation, GetTransformationsQueryTransformationsBaseSequenceTransformation, GetTransformationsQueryTransformationsBaseTranslationTransformation, GetTransformationsQueryTransformationsBaseUnmappableTransformation], Field(discriminator='typename')], GetTransformationsQueryTransformationsBaseCatchAll], ...]:
    """GetTransformations 

List transformations (the directed edges of the coordinate graph). Compose them client-side; the server never resolves a path to world, because the same dataset can sit in two scenes under two registrations

Args:
    filters (Optional[TransformationFilter], optional): No description. 
    pagination (Optional[OffsetPaginationInput], optional): No description. 
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    List[Transformation]
"""
    variables: Dict[str, Any] = {}
    if filters is not UNSET:
        variables['filters'] = filters
    if pagination is not UNSET:
        variables['pagination'] = pagination
    return execute(GetTransformationsQuery, variables, rath=rath).transformations

async def aget_rgb_view(id: IDCoercible, rath: Optional[MikroNextRath]=None) -> RGBView:
    """GetRGBView 

Get a single RGB render view by ID

Args:
    id (ID): The unique identifier of an object
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    RGBView
"""
    variables: Dict[str, Any] = {}
    variables['id'] = id
    return (await aexecute(GetRGBViewQuery, variables, rath=rath)).rgb_view

def get_rgb_view(id: IDCoercible, rath: Optional[MikroNextRath]=None) -> RGBView:
    """GetRGBView 

Get a single RGB render view by ID

Args:
    id (ID): The unique identifier of an object
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    RGBView
"""
    variables: Dict[str, Any] = {}
    variables['id'] = id
    return execute(GetRGBViewQuery, variables, rath=rath).rgb_view

async def asearch_rgb_views(search: Union[Optional[str], UnsetType]=UNSET, values: Union[Optional[List[IDCoercible]], UnsetType]=UNSET, limit: Union[Optional[int], UnsetType]=UNSET, offset: Union[Optional[int], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> Tuple[SearchRGBViewsQueryOptions, ...]:
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
    variables: Dict[str, Any] = {}
    if search is not UNSET:
        variables['search'] = search
    if values is not UNSET:
        variables['values'] = values
    if limit is not UNSET:
        variables['limit'] = limit
    if offset is not UNSET:
        variables['offset'] = offset
    return (await aexecute(SearchRGBViewsQuery, variables, rath=rath)).options

def search_rgb_views(search: Union[Optional[str], UnsetType]=UNSET, values: Union[Optional[List[IDCoercible]], UnsetType]=UNSET, limit: Union[Optional[int], UnsetType]=UNSET, offset: Union[Optional[int], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> Tuple[SearchRGBViewsQueryOptions, ...]:
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
    variables: Dict[str, Any] = {}
    if search is not UNSET:
        variables['search'] = search
    if values is not UNSET:
        variables['values'] = values
    if limit is not UNSET:
        variables['limit'] = limit
    if offset is not UNSET:
        variables['offset'] = offset
    return execute(SearchRGBViewsQuery, variables, rath=rath).options

async def awatch_files(dataset: Union[Optional[IDCoercible], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> AsyncIterator[WatchFilesSubscriptionFiles]:
    """WatchFiles 

Subscribe to real-time file updates

Args:
    dataset (Optional[ID], optional): No description. 
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    WatchFilesSubscriptionFiles
"""
    variables: Dict[str, Any] = {}
    if dataset is not UNSET:
        variables['dataset'] = dataset
    async for event in asubscribe(WatchFilesSubscription, variables, rath=rath):
        yield event.files

def watch_files(dataset: Union[Optional[IDCoercible], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> Iterator[WatchFilesSubscriptionFiles]:
    """WatchFiles 

Subscribe to real-time file updates

Args:
    dataset (Optional[ID], optional): No description. 
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    WatchFilesSubscriptionFiles
"""
    variables: Dict[str, Any] = {}
    if dataset is not UNSET:
        variables['dataset'] = dataset
    for event in subscribe(WatchFilesSubscription, variables, rath=rath):
        yield event.files

async def awatch_images(dataset: Union[Optional[IDCoercible], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> AsyncIterator[WatchImagesSubscriptionImages]:
    """WatchImages 

Subscribe to real-time image updates

Args:
    dataset (Optional[ID], optional): No description. 
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    WatchImagesSubscriptionImages
"""
    variables: Dict[str, Any] = {}
    if dataset is not UNSET:
        variables['dataset'] = dataset
    async for event in asubscribe(WatchImagesSubscription, variables, rath=rath):
        yield event.images

def watch_images(dataset: Union[Optional[IDCoercible], UnsetType]=UNSET, rath: Optional[MikroNextRath]=None) -> Iterator[WatchImagesSubscriptionImages]:
    """WatchImages 

Subscribe to real-time image updates

Args:
    dataset (Optional[ID], optional): No description. 
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    WatchImagesSubscriptionImages
"""
    variables: Dict[str, Any] = {}
    if dataset is not UNSET:
        variables['dataset'] = dataset
    for event in subscribe(WatchImagesSubscription, variables, rath=rath):
        yield event.images

async def awatch_rois(image: IDCoercible, rath: Optional[MikroNextRath]=None) -> AsyncIterator[WatchRoisSubscriptionRois]:
    """WatchRois 

Subscribe to real-time ROI updates

Args:
    image (ID): No description
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    WatchRoisSubscriptionRois
"""
    variables: Dict[str, Any] = {}
    variables['image'] = image
    async for event in asubscribe(WatchRoisSubscription, variables, rath=rath):
        yield event.rois

def watch_rois(image: IDCoercible, rath: Optional[MikroNextRath]=None) -> Iterator[WatchRoisSubscriptionRois]:
    """WatchRois 

Subscribe to real-time ROI updates

Args:
    image (ID): No description
    rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

Returns:
    WatchRoisSubscriptionRois
"""
    variables: Dict[str, Any] = {}
    variables['image'] = image
    for event in subscribe(WatchRoisSubscription, variables, rath=rath):
        yield event.rois
ADatasetFilter.model_rebuild()
AffineTransformationViewFilter.model_rebuild()
AnimationFilter.model_rebuild()
AnimationWaypointInput.model_rebuild()
AnnotationCollectionDerivedFromInput.model_rebuild()
AnnotationCollectionFilter.model_rebuild()
AnnotationFilter.model_rebuild()
AnnotationSpecInput.model_rebuild()
ApertureElementInput.model_rebuild()
BeamSplitterElementInput.model_rebuild()
CCDElementInput.model_rebuild()
CoordinateAnchorInput.model_rebuild()
CoordinateSystemDerivedFromInput.model_rebuild()
CoordinateSystemFilter.model_rebuild()
CreateADatasetInput.model_rebuild()
CreateAnnotationCollectionInput.model_rebuild()
CreateCoordinateSystemInput.model_rebuild()
CreateLayerInput.model_rebuild()
CreateLensInput.model_rebuild()
CreateMeshCollectionInput.model_rebuild()
CreatePhasorLayerInput.model_rebuild()
CreateRGBContextInput.model_rebuild()
CreateSceneFromCoordinateSystemInput.model_rebuild()
CreateSceneInput.model_rebuild()
CreateTableDatasetInput.model_rebuild()
CreateTransformationInput.model_rebuild()
DatasetDerivedFromInput.model_rebuild()
DatasetFilter.model_rebuild()
DetectorElementInput.model_rebuild()
DeviceStateInput.model_rebuild()
EraFilter.model_rebuild()
FilterElementInput.model_rebuild()
FromArrayLikeInput.model_rebuild()
FromParquetLike.model_rebuild()
ImageFilter.model_rebuild()
LampElementInput.model_rebuild()
LaserElementInput.model_rebuild()
LayerNodeInput.model_rebuild()
LensDerivedFromInput.model_rebuild()
LensElementInput.model_rebuild()
LightPortInput.model_rebuild()
LightpathGraphInput.model_rebuild()
MeshCollectionDerivedFromInput.model_rebuild()
MeshCollectionFilter.model_rebuild()
MirrorElementInput.model_rebuild()
ObjectiveElementInput.model_rebuild()
OptikitStateInput.model_rebuild()
OtherElementInput.model_rebuild()
OtherSourceElementInput.model_rebuild()
PhasorTransferInput.model_rebuild()
PinholeElementInput.model_rebuild()
PolarizerElementInput.model_rebuild()
Pose3DInput.model_rebuild()
RegistrationPathInput.model_rebuild()
RenderTreeInput.model_rebuild()
SampleElementInput.model_rebuild()
SceneSnapshotFilter.model_rebuild()
ShutterElementInput.model_rebuild()
StageFilter.model_rebuild()
TableDatasetDerivedFromInput.model_rebuild()
TableDatasetFilter.model_rebuild()
TimepointViewFilter.model_rebuild()
TransformationFilter.model_rebuild()
TreeInput.model_rebuild()
TreeNodeInput.model_rebuild()
ViewFilter.model_rebuild()
WaveplateElementInput.model_rebuild()
ZarrStoreFilter.model_rebuild()