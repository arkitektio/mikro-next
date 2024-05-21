dfrom typing import Tuple, List, Optional, Union, Literal
from mikro_next.scalars import (
    ParquetLike,
    FileLike,
    ArrayLike,
    FourByFourMatrix,
    Upload,
    Micrometers,
    Milliseconds,
)
from pydantic import Field, BaseModel
from mikro_next.traits import (
    Stage,
    ParquetStore,
    ZarrStore,
    MediaStore,
    Table,
    Image,
    Objective,
    BigFileStore,
    File,
)
from datetime import datetime
from mikro_next.funcs import aexecute, execute
from rath.scalars import ID
from mikro_next.rath import MikroNextRath
from enum import Enum


class PartialChannelViewInput(BaseModel):
    collection: Optional[ID]
    z_min: Optional[int] = Field(alias="zMin")
    z_max: Optional[int] = Field(alias="zMax")
    x_min: Optional[int] = Field(alias="xMin")
    x_max: Optional[int] = Field(alias="xMax")
    y_min: Optional[int] = Field(alias="yMin")
    y_max: Optional[int] = Field(alias="yMax")
    t_min: Optional[int] = Field(alias="tMin")
    t_max: Optional[int] = Field(alias="tMax")
    c_min: Optional[int] = Field(alias="cMin")
    c_max: Optional[int] = Field(alias="cMax")
    channel: ID

    class Config:
        """A config class"""

        frozen = True
        extra = "forbid"
        allow_population_by_field_name = True
        use_enum_values = True


class PartialAffineTransformationViewInput(BaseModel):
    collection: Optional[ID]
    z_min: Optional[int] = Field(alias="zMin")
    z_max: Optional[int] = Field(alias="zMax")
    x_min: Optional[int] = Field(alias="xMin")
    x_max: Optional[int] = Field(alias="xMax")
    y_min: Optional[int] = Field(alias="yMin")
    y_max: Optional[int] = Field(alias="yMax")
    t_min: Optional[int] = Field(alias="tMin")
    t_max: Optional[int] = Field(alias="tMax")
    c_min: Optional[int] = Field(alias="cMin")
    c_max: Optional[int] = Field(alias="cMax")
    stage: Optional[ID]
    affine_matrix: FourByFourMatrix = Field(alias="affineMatrix")

    class Config:
        """A config class"""

        frozen = True
        extra = "forbid"
        allow_population_by_field_name = True
        use_enum_values = True


class PartialAcquisitionViewInput(BaseModel):
    collection: Optional[ID]
    z_min: Optional[int] = Field(alias="zMin")
    z_max: Optional[int] = Field(alias="zMax")
    x_min: Optional[int] = Field(alias="xMin")
    x_max: Optional[int] = Field(alias="xMax")
    y_min: Optional[int] = Field(alias="yMin")
    y_max: Optional[int] = Field(alias="yMax")
    t_min: Optional[int] = Field(alias="tMin")
    t_max: Optional[int] = Field(alias="tMax")
    c_min: Optional[int] = Field(alias="cMin")
    c_max: Optional[int] = Field(alias="cMax")
    description: Optional[str]
    acquired_at: Optional[datetime] = Field(alias="acquiredAt")
    operator: Optional[ID]

    class Config:
        """A config class"""

        frozen = True
        extra = "forbid"
        allow_population_by_field_name = True
        use_enum_values = True


class PartialLabelViewInput(BaseModel):
    collection: Optional[ID]
    z_min: Optional[int] = Field(alias="zMin")
    z_max: Optional[int] = Field(alias="zMax")
    x_min: Optional[int] = Field(alias="xMin")
    x_max: Optional[int] = Field(alias="xMax")
    y_min: Optional[int] = Field(alias="yMin")
    y_max: Optional[int] = Field(alias="yMax")
    t_min: Optional[int] = Field(alias="tMin")
    t_max: Optional[int] = Field(alias="tMax")
    c_min: Optional[int] = Field(alias="cMin")
    c_max: Optional[int] = Field(alias="cMax")
    fluorophore: Optional[ID]
    primary_antibody: Optional[ID] = Field(alias="primaryAntibody")
    secondary_antibody: Optional[ID] = Field(alias="secondaryAntibody")

    class Config:
        """A config class"""

        frozen = True
        extra = "forbid"
        allow_population_by_field_name = True
        use_enum_values = True


class PartialRGBViewInput(BaseModel):
    collection: Optional[ID]
    z_min: Optional[int] = Field(alias="zMin")
    z_max: Optional[int] = Field(alias="zMax")
    x_min: Optional[int] = Field(alias="xMin")
    x_max: Optional[int] = Field(alias="xMax")
    y_min: Optional[int] = Field(alias="yMin")
    y_max: Optional[int] = Field(alias="yMax")
    t_min: Optional[int] = Field(alias="tMin")
    t_max: Optional[int] = Field(alias="tMax")
    c_min: Optional[int] = Field(alias="cMin")
    c_max: Optional[int] = Field(alias="cMax")
    context: Optional[ID]
    r_scale: float = Field(alias="rScale")
    g_scale: float = Field(alias="gScale")
    b_scale: float = Field(alias="bScale")

    class Config:
        """A config class"""

        frozen = True
        extra = "forbid"
        allow_population_by_field_name = True
        use_enum_values = True


class PartialTimepointViewInput(BaseModel):
    collection: Optional[ID]
    z_min: Optional[int] = Field(alias="zMin")
    z_max: Optional[int] = Field(alias="zMax")
    x_min: Optional[int] = Field(alias="xMin")
    x_max: Optional[int] = Field(alias="xMax")
    y_min: Optional[int] = Field(alias="yMin")
    y_max: Optional[int] = Field(alias="yMax")
    t_min: Optional[int] = Field(alias="tMin")
    t_max: Optional[int] = Field(alias="tMax")
    c_min: Optional[int] = Field(alias="cMin")
    c_max: Optional[int] = Field(alias="cMax")
    era: Optional[ID]
    ms_since_start: Optional[Milliseconds] = Field(alias="msSinceStart")
    index_since_start: Optional[int] = Field(alias="indexSinceStart")

    class Config:
        """A config class"""

        frozen = True
        extra = "forbid"
        allow_population_by_field_name = True
        use_enum_values = True


class PartialOpticsViewInput(BaseModel):
    collection: Optional[ID]
    z_min: Optional[int] = Field(alias="zMin")
    z_max: Optional[int] = Field(alias="zMax")
    x_min: Optional[int] = Field(alias="xMin")
    x_max: Optional[int] = Field(alias="xMax")
    y_min: Optional[int] = Field(alias="yMin")
    y_max: Optional[int] = Field(alias="yMax")
    t_min: Optional[int] = Field(alias="tMin")
    t_max: Optional[int] = Field(alias="tMax")
    c_min: Optional[int] = Field(alias="cMin")
    c_max: Optional[int] = Field(alias="cMax")
    instrument: Optional[ID]
    objective: Optional[ID]
    camera: Optional[ID]

    class Config:
        """A config class"""

        frozen = True
        extra = "forbid"
        allow_population_by_field_name = True
        use_enum_values = True


class TableFragmentOrigins(Image, BaseModel):
    typename: Optional[Literal["Image"]] = Field(alias="__typename", exclude=True)
    id: ID

    class Config:
        """A config class"""

        frozen = True


class TableFragment(Table, BaseModel):
    typename: Optional[Literal["Table"]] = Field(alias="__typename", exclude=True)
    origins: Tuple[TableFragmentOrigins, ...]
    id: ID
    name: str
    store: "ParquetStoreFragment"

    class Config:
        """A config class"""

        frozen = True


class CredentialsFragment(BaseModel):
    typename: Optional[Literal["Credentials"]] = Field(alias="__typename", exclude=True)
    access_key: str = Field(alias="accessKey")
    status: str
    secret_key: str = Field(alias="secretKey")
    bucket: str
    key: str
    session_token: str = Field(alias="sessionToken")
    store: str

    class Config:
        """A config class"""

        frozen = True


class AccessCredentialsFragment(BaseModel):
    typename: Optional[Literal["AccessCredentials"]] = Field(
        alias="__typename", exclude=True
    )
    access_key: str = Field(alias="accessKey")
    secret_key: str = Field(alias="secretKey")
    bucket: str
    key: str
    session_token: str = Field(alias="sessionToken")
    path: str

    class Config:
        """A config class"""

        frozen = True


class ViewFragmentBase(BaseModel):
    z_min: Optional[int] = Field(alias="zMin")
    z_max: Optional[int] = Field(alias="zMax")


class ChannelViewFragment(ViewFragmentBase, BaseModel):
    typename: Optional[Literal["ChannelView"]] = Field(alias="__typename", exclude=True)
    id: ID
    channel: "ChannelFragment"

    class Config:
        """A config class"""

        frozen = True


class AffineTransformationViewFragmentStage(Stage, BaseModel):
    typename: Optional[Literal["Stage"]] = Field(alias="__typename", exclude=True)
    id: ID

    class Config:
        """A config class"""

        frozen = True


class AffineTransformationViewFragment(ViewFragmentBase, BaseModel):
    typename: Optional[Literal["AffineTransformationView"]] = Field(
        alias="__typename", exclude=True
    )
    id: ID
    affine_matrix: FourByFourMatrix = Field(alias="affineMatrix")
    stage: AffineTransformationViewFragmentStage

    class Config:
        """A config class"""

        frozen = True


class TimepointViewFragment(ViewFragmentBase, BaseModel):
    typename: Optional[Literal["TimepointView"]] = Field(
        alias="__typename", exclude=True
    )
    id: ID
    ms_since_start: Optional[Milliseconds] = Field(alias="msSinceStart")
    index_since_start: Optional[int] = Field(alias="indexSinceStart")
    era: "EraFragment"

    class Config:
        """A config class"""

        frozen = True


class OpticsViewFragmentObjective(Objective, BaseModel):
    typename: Optional[Literal["Objective"]] = Field(alias="__typename", exclude=True)
    id: ID
    name: str
    serial_number: str = Field(alias="serialNumber")

    class Config:
        """A config class"""

        frozen = True


class OpticsViewFragmentCamera(BaseModel):
    typename: Optional[Literal["Camera"]] = Field(alias="__typename", exclude=True)
    id: ID
    name: str
    serial_number: str = Field(alias="serialNumber")

    class Config:
        """A config class"""

        frozen = True


class OpticsViewFragmentInstrument(BaseModel):
    typename: Optional[Literal["Instrument"]] = Field(alias="__typename", exclude=True)
    id: ID
    name: str
    serial_number: str = Field(alias="serialNumber")

    class Config:
        """A config class"""

        frozen = True


class OpticsViewFragment(ViewFragmentBase, BaseModel):
    typename: Optional[Literal["OpticsView"]] = Field(alias="__typename", exclude=True)
    objective: Optional[OpticsViewFragmentObjective]
    camera: Optional[OpticsViewFragmentCamera]
    instrument: Optional[OpticsViewFragmentInstrument]

    class Config:
        """A config class"""

        frozen = True


class LabelViewFragment(ViewFragmentBase, BaseModel):
    typename: Optional[Literal["LabelView"]] = Field(alias="__typename", exclude=True)
    id: ID
    fluorophore: Optional["FluorophoreFragment"]
    primary_antibody: Optional["AntibodyFragment"] = Field(alias="primaryAntibody")
    secondary_antibody: Optional["AntibodyFragment"] = Field(alias="secondaryAntibody")

    class Config:
        """A config class"""

        frozen = True


class ChannelFragment(BaseModel):
    typename: Optional[Literal["Channel"]] = Field(alias="__typename", exclude=True)
    id: ID
    name: str
    excitation_wavelength: Optional[float] = Field(alias="excitationWavelength")

    class Config:
        """A config class"""

        frozen = True


class EraFragment(BaseModel):
    typename: Optional[Literal["Era"]] = Field(alias="__typename", exclude=True)
    id: ID
    begin: Optional[datetime]
    name: str

    class Config:
        """A config class"""

        frozen = True


class FileFragmentOrigins(Image, BaseModel):
    typename: Optional[Literal["Image"]] = Field(alias="__typename", exclude=True)
    id: ID

    class Config:
        """A config class"""

        frozen = True


class FileFragment(File, BaseModel):
    typename: Optional[Literal["File"]] = Field(alias="__typename", exclude=True)
    origins: Tuple[FileFragmentOrigins, ...]
    id: ID
    name: str
    store: "BigFileStoreFragment"

    class Config:
        """A config class"""

        frozen = True


class InstrumentFragment(BaseModel):
    typename: Optional[Literal["Instrument"]] = Field(alias="__typename", exclude=True)
    id: ID
    model: Optional[str]
    name: str
    serial_number: str = Field(alias="serialNumber")

    class Config:
        """A config class"""

        frozen = True


class AntibodyFragment(BaseModel):
    typename: Optional[Literal["Antibody"]] = Field(alias="__typename", exclude=True)
    name: str
    epitope: Optional[str]

    class Config:
        """A config class"""

        frozen = True


class ZarrStoreFragment(ZarrStore, BaseModel):
    typename: Optional[Literal["ZarrStore"]] = Field(alias="__typename", exclude=True)
    id: ID
    key: str
    "The key where the data is stored."
    bucket: str
    "The bucket where the data is stored."
    path: Optional[str]
    "The path to the data. Relative to the bucket."

    class Config:
        """A config class"""

        frozen = True


class ParquetStoreFragment(ParquetStore, BaseModel):
    typename: Optional[Literal["ParquetStore"]] = Field(
        alias="__typename", exclude=True
    )
    id: ID
    key: str
    bucket: str
    path: str

    class Config:
        """A config class"""

        frozen = True


class BigFileStoreFragment(BigFileStore, BaseModel):
    typename: Optional[Literal["BigFileStore"]] = Field(
        alias="__typename", exclude=True
    )
    id: ID
    key: str
    bucket: str
    path: str

    class Config:
        """A config class"""

        frozen = True


class SnapshotFragmentStore(MediaStore, BaseModel):
    typename: Optional[Literal["MediaStore"]] = Field(alias="__typename", exclude=True)
    key: str
    presigned_url: str = Field(alias="presignedUrl")

    class Config:
        """A config class"""

        frozen = True


class SnapshotFragment(BaseModel):
    typename: Optional[Literal["Snapshot"]] = Field(alias="__typename", exclude=True)
    id: ID
    store: SnapshotFragmentStore
    name: str

    class Config:
        """A config class"""

        frozen = True


class HistoryStuffFragmentApp(BaseModel):
    typename: Optional[Literal["App"]] = Field(alias="__typename", exclude=True)
    id: ID

    class Config:
        """A config class"""

        frozen = True


class HistoryStuffFragment(BaseModel):
    typename: Optional[Literal["History"]] = Field(alias="__typename", exclude=True)
    id: ID
    app: Optional[HistoryStuffFragmentApp]

    class Config:
        """A config class"""

        frozen = True


class DatasetFragment(BaseModel):
    typename: Optional[Literal["Dataset"]] = Field(alias="__typename", exclude=True)
    name: str
    description: Optional[str]
    history: Tuple[HistoryStuffFragment, ...]

    class Config:
        """A config class"""

        frozen = True


class FluorophoreFragment(BaseModel):
    typename: Optional[Literal["Fluorophore"]] = Field(alias="__typename", exclude=True)
    id: ID
    name: str
    emission_wavelength: Optional[Micrometers] = Field(alias="emissionWavelength")
    excitation_wavelength: Optional[Micrometers] = Field(alias="excitationWavelength")

    class Config:
        """A config class"""

        frozen = True


class ImageFragmentOrigins(Image, BaseModel):
    typename: Optional[Literal["Image"]] = Field(alias="__typename", exclude=True)
    id: ID

    class Config:
        """A config class"""

        frozen = True


class ImageFragmentViewsBase(BaseModel):
    pass

    class Config:
        """A config class"""

        frozen = True


class ImageFragmentViewsChannelView(ImageFragmentViewsBase, ChannelViewFragment):
    pass

    class Config:
        """A config class"""

        frozen = True


class ImageFragmentViewsAffineTransformationView(
    ImageFragmentViewsBase, AffineTransformationViewFragment
):
    pass

    class Config:
        """A config class"""

        frozen = True


class ImageFragmentViewsLabelView(ImageFragmentViewsBase, LabelViewFragment):
    pass

    class Config:
        """A config class"""

        frozen = True


class ImageFragmentViewsTimepointView(ImageFragmentViewsBase, TimepointViewFragment):
    pass

    class Config:
        """A config class"""

        frozen = True


class ImageFragmentViewsOpticsView(ImageFragmentViewsBase, OpticsViewFragment):
    pass

    class Config:
        """A config class"""

        frozen = True


class ImageFragment(Image, BaseModel):
    typename: Optional[Literal["Image"]] = Field(alias="__typename", exclude=True)
    origins: Tuple[ImageFragmentOrigins, ...]
    id: ID
    name: str
    store: ZarrStoreFragment
    "The store where the image data is stored."
    views: Tuple[
        Union[
            ImageFragmentViewsChannelView,
            ImageFragmentViewsAffineTransformationView,
            ImageFragmentViewsLabelView,
            ImageFragmentViewsTimepointView,
            ImageFragmentViewsOpticsView,
        ],
        ...,
    ]

    class Config:
        """A config class"""

        frozen = True


class ObjectiveFragment(Objective, BaseModel):
    typename: Optional[Literal["Objective"]] = Field(alias="__typename", exclude=True)
    id: ID
    na: Optional[float]
    name: str
    serial_number: str = Field(alias="serialNumber")

    class Config:
        """A config class"""

        frozen = True


class CameraFragment(BaseModel):
    typename: Optional[Literal["Camera"]] = Field(alias="__typename", exclude=True)
    sensor_size_x: Optional[int] = Field(alias="sensorSizeX")
    sensor_size_y: Optional[int] = Field(alias="sensorSizeY")
    pixel_size_x: Optional[Micrometers] = Field(alias="pixelSizeX")
    pixel_size_y: Optional[Micrometers] = Field(alias="pixelSizeY")
    name: str
    serial_number: str = Field(alias="serialNumber")

    class Config:
        """A config class"""

        frozen = True


class From_parquet_likeMutation(BaseModel):
    from_parquet_like: TableFragment = Field(alias="fromParquetLike")

    class Arguments(BaseModel):
        dataframe: ParquetLike
        name: str
        origins: Optional[List[ID]] = Field(default=None)
        dataset: Optional[ID] = Field(default=None)

    class Meta:
        document = "fragment ParquetStore on ParquetStore {\n  id\n  key\n  bucket\n  path\n}\n\nfragment Table on Table {\n  origins {\n    id\n  }\n  id\n  name\n  store {\n    ...ParquetStore\n  }\n}\n\nmutation from_parquet_like($dataframe: ParquetLike!, $name: String!, $origins: [ID!], $dataset: ID) {\n  fromParquetLike(\n    input: {dataframe: $dataframe, name: $name, origins: $origins, dataset: $dataset}\n  ) {\n    ...Table\n  }\n}"


class RequestTableUploadMutation(BaseModel):
    request_table_upload: CredentialsFragment = Field(alias="requestTableUpload")

    class Arguments(BaseModel):
        key: str
        datalayer: str

    class Meta:
        document = "fragment Credentials on Credentials {\n  accessKey\n  status\n  secretKey\n  bucket\n  key\n  sessionToken\n  store\n}\n\nmutation RequestTableUpload($key: String!, $datalayer: String!) {\n  requestTableUpload(input: {key: $key, datalayer: $datalayer}) {\n    ...Credentials\n  }\n}"


class RequestTableAccessMutation(BaseModel):
    request_table_access: AccessCredentialsFragment = Field(alias="requestTableAccess")

    class Arguments(BaseModel):
        store: ID
        duration: Optional[int] = Field(default=None)

    class Meta:
        document = "fragment AccessCredentials on AccessCredentials {\n  accessKey\n  secretKey\n  bucket\n  key\n  sessionToken\n  path\n}\n\nmutation RequestTableAccess($store: ID!, $duration: Int) {\n  requestTableAccess(input: {store: $store, duration: $duration}) {\n    ...AccessCredentials\n  }\n}"


class CreateStageMutationCreatestage(Stage, BaseModel):
    typename: Optional[Literal["Stage"]] = Field(alias="__typename", exclude=True)
    id: ID
    name: str

    class Config:
        """A config class"""

        frozen = True


class CreateStageMutation(BaseModel):
    create_stage: CreateStageMutationCreatestage = Field(alias="createStage")

    class Arguments(BaseModel):
        name: str

    class Meta:
        document = "mutation CreateStage($name: String!) {\n  createStage(input: {name: $name}) {\n    id\n    name\n  }\n}"


class CreateChannelMutationCreatechannel(BaseModel):
    typename: Optional[Literal["Channel"]] = Field(alias="__typename", exclude=True)
    id: ID
    name: str

    class Config:
        """A config class"""

        frozen = True


class CreateChannelMutation(BaseModel):
    create_channel: CreateChannelMutationCreatechannel = Field(alias="createChannel")

    class Arguments(BaseModel):
        name: str

    class Meta:
        document = "mutation CreateChannel($name: String!) {\n  createChannel(input: {name: $name}) {\n    id\n    name\n  }\n}"


class EnsureChannelMutationEnsurechannel(BaseModel):
    typename: Optional[Literal["Channel"]] = Field(alias="__typename", exclude=True)
    id: ID
    name: str

    class Config:
        """A config class"""

        frozen = True


class EnsureChannelMutation(BaseModel):
    ensure_channel: EnsureChannelMutationEnsurechannel = Field(alias="ensureChannel")

    class Arguments(BaseModel):
        name: str

    class Meta:
        document = "mutation EnsureChannel($name: String!) {\n  ensureChannel(input: {name: $name}) {\n    id\n    name\n  }\n}"


class CreateEraMutationCreateera(BaseModel):
    typename: Optional[Literal["Era"]] = Field(alias="__typename", exclude=True)
    id: ID
    begin: Optional[datetime]

    class Config:
        """A config class"""

        frozen = True


class CreateEraMutation(BaseModel):
    create_era: CreateEraMutationCreateera = Field(alias="createEra")

    class Arguments(BaseModel):
        name: str
        begin: Optional[datetime] = Field(default=None)

    class Meta:
        document = "mutation CreateEra($name: String!, $begin: DateTime) {\n  createEra(input: {name: $name, begin: $begin}) {\n    id\n    begin\n  }\n}"


class CreateRgbViewMutationCreatergbview(BaseModel):
    typename: Optional[Literal["RGBView"]] = Field(alias="__typename", exclude=True)
    id: ID

    class Config:
        """A config class"""

        frozen = True


class CreateRgbViewMutation(BaseModel):
    create_rgb_view: CreateRgbViewMutationCreatergbview = Field(alias="createRgbView")

    class Arguments(BaseModel):
        image: ID
        r_scale: float = Field(alias="rScale")
        b_scale: float = Field(alias="bScale")
        g_scale: float = Field(alias="gScale")
        context: Optional[ID] = Field(default=None)

    class Meta:
        document = "mutation CreateRgbView($image: ID!, $rScale: Float!, $bScale: Float!, $gScale: Float!, $context: ID) {\n  createRgbView(\n    input: {rScale: $rScale, bScale: $bScale, gScale: $gScale, context: $context, image: $image}\n  ) {\n    id\n  }\n}"


class From_file_likeMutation(BaseModel):
    from_file_like: FileFragment = Field(alias="fromFileLike")

    class Arguments(BaseModel):
        file: FileLike
        name: str
        origins: Optional[List[ID]] = Field(default=None)
        dataset: Optional[ID] = Field(default=None)

    class Meta:
        document = "fragment BigFileStore on BigFileStore {\n  id\n  key\n  bucket\n  path\n}\n\nfragment File on File {\n  origins {\n    id\n  }\n  id\n  name\n  store {\n    ...BigFileStore\n  }\n}\n\nmutation from_file_like($file: FileLike!, $name: String!, $origins: [ID!], $dataset: ID) {\n  fromFileLike(\n    input: {file: $file, name: $name, origins: $origins, dataset: $dataset}\n  ) {\n    ...File\n  }\n}"


class RequestFileUploadMutation(BaseModel):
    request_file_upload: CredentialsFragment = Field(alias="requestFileUpload")

    class Arguments(BaseModel):
        key: str
        datalayer: str

    class Meta:
        document = "fragment Credentials on Credentials {\n  accessKey\n  status\n  secretKey\n  bucket\n  key\n  sessionToken\n  store\n}\n\nmutation RequestFileUpload($key: String!, $datalayer: String!) {\n  requestFileUpload(input: {key: $key, datalayer: $datalayer}) {\n    ...Credentials\n  }\n}"


class RequestFileAccessMutation(BaseModel):
    request_file_access: AccessCredentialsFragment = Field(alias="requestFileAccess")

    class Arguments(BaseModel):
        store: ID
        duration: Optional[int] = Field(default=None)

    class Meta:
        document = "fragment AccessCredentials on AccessCredentials {\n  accessKey\n  secretKey\n  bucket\n  key\n  sessionToken\n  path\n}\n\nmutation RequestFileAccess($store: ID!, $duration: Int) {\n  requestFileAccess(input: {store: $store, duration: $duration}) {\n    ...AccessCredentials\n  }\n}"


class CreateRGBContextMutationCreatergbcontext(BaseModel):
    typename: Optional[Literal["RGBContext"]] = Field(alias="__typename", exclude=True)
    id: ID

    class Config:
        """A config class"""

        frozen = True


class CreateRGBContextMutation(BaseModel):
    create_rgb_context: CreateRGBContextMutationCreatergbcontext = Field(
        alias="createRgbContext"
    )

    class Arguments(BaseModel):
        name: str

    class Meta:
        document = "mutation CreateRGBContext($name: String!) {\n  createRgbContext(input: {name: $name}) {\n    id\n  }\n}"


class CreateInstrumentMutationCreateinstrument(BaseModel):
    typename: Optional[Literal["Instrument"]] = Field(alias="__typename", exclude=True)
    id: ID
    name: str

    class Config:
        """A config class"""

        frozen = True


class CreateInstrumentMutation(BaseModel):
    create_instrument: CreateInstrumentMutationCreateinstrument = Field(
        alias="createInstrument"
    )

    class Arguments(BaseModel):
        serial_number: str = Field(alias="serialNumber")
        name: Optional[str] = Field(default=None)
        model: Optional[str] = Field(default=None)

    class Meta:
        document = "mutation CreateInstrument($serialNumber: String!, $name: String, $model: String) {\n  createInstrument(\n    input: {name: $name, model: $model, serialNumber: $serialNumber}\n  ) {\n    id\n    name\n  }\n}"


class EnsureInstrumentMutationEnsureinstrument(BaseModel):
    typename: Optional[Literal["Instrument"]] = Field(alias="__typename", exclude=True)
    id: ID
    name: str

    class Config:
        """A config class"""

        frozen = True


class EnsureInstrumentMutation(BaseModel):
    ensure_instrument: EnsureInstrumentMutationEnsureinstrument = Field(
        alias="ensureInstrument"
    )

    class Arguments(BaseModel):
        serial_number: str = Field(alias="serialNumber")
        name: Optional[str] = Field(default=None)
        model: Optional[str] = Field(default=None)

    class Meta:
        document = "mutation EnsureInstrument($serialNumber: String!, $name: String, $model: String) {\n  ensureInstrument(\n    input: {name: $name, model: $model, serialNumber: $serialNumber}\n  ) {\n    id\n    name\n  }\n}"


class CreateViewCollectionMutationCreateviewcollection(BaseModel):
    typename: Optional[Literal["ViewCollection"]] = Field(
        alias="__typename", exclude=True
    )
    id: ID
    name: str

    class Config:
        """A config class"""

        frozen = True


class CreateViewCollectionMutation(BaseModel):
    create_view_collection: CreateViewCollectionMutationCreateviewcollection = Field(
        alias="createViewCollection"
    )

    class Arguments(BaseModel):
        name: str

    class Meta:
        document = "mutation CreateViewCollection($name: String!) {\n  createViewCollection(input: {name: $name}) {\n    id\n    name\n  }\n}"


class CreateAntibodyMutationCreateantibody(BaseModel):
    typename: Optional[Literal["Antibody"]] = Field(alias="__typename", exclude=True)
    id: ID
    name: str

    class Config:
        """A config class"""

        frozen = True


class CreateAntibodyMutation(BaseModel):
    create_antibody: CreateAntibodyMutationCreateantibody = Field(
        alias="createAntibody"
    )

    class Arguments(BaseModel):
        name: str
        epitope: Optional[str] = Field(default=None)

    class Meta:
        document = "mutation CreateAntibody($name: String!, $epitope: String) {\n  createAntibody(input: {name: $name, epitope: $epitope}) {\n    id\n    name\n  }\n}"


class EnsureAntibodyMutationEnsureantibody(BaseModel):
    typename: Optional[Literal["Antibody"]] = Field(alias="__typename", exclude=True)
    id: ID
    name: str

    class Config:
        """A config class"""

        frozen = True


class EnsureAntibodyMutation(BaseModel):
    ensure_antibody: EnsureAntibodyMutationEnsureantibody = Field(
        alias="ensureAntibody"
    )

    class Arguments(BaseModel):
        name: str
        epitope: Optional[str] = Field(default=None)

    class Meta:
        document = "mutation EnsureAntibody($name: String!, $epitope: String) {\n  ensureAntibody(input: {name: $name, epitope: $epitope}) {\n    id\n    name\n  }\n}"


class CreateSnapshotMutation(BaseModel):
    create_snapshot: SnapshotFragment = Field(alias="createSnapshot")

    class Arguments(BaseModel):
        image: ID
        file: Upload

    class Meta:
        document = "fragment Snapshot on Snapshot {\n  id\n  store {\n    key\n    presignedUrl\n  }\n  name\n}\n\nmutation CreateSnapshot($image: ID!, $file: Upload!) {\n  createSnapshot(input: {file: $file, image: $image}) {\n    ...Snapshot\n  }\n}"


class CreateDatasetMutationCreatedataset(BaseModel):
    typename: Optional[Literal["Dataset"]] = Field(alias="__typename", exclude=True)
    id: ID
    name: str

    class Config:
        """A config class"""

        frozen = True


class CreateDatasetMutation(BaseModel):
    create_dataset: CreateDatasetMutationCreatedataset = Field(alias="createDataset")

    class Arguments(BaseModel):
        name: str

    class Meta:
        document = "mutation CreateDataset($name: String!) {\n  createDataset(input: {name: $name}) {\n    id\n    name\n  }\n}"


class UpdateDatasetMutationUpdatedataset(BaseModel):
    typename: Optional[Literal["Dataset"]] = Field(alias="__typename", exclude=True)
    id: ID
    name: str

    class Config:
        """A config class"""

        frozen = True


class UpdateDatasetMutation(BaseModel):
    update_dataset: UpdateDatasetMutationUpdatedataset = Field(alias="updateDataset")

    class Arguments(BaseModel):
        id: ID
        name: str

    class Meta:
        document = "mutation UpdateDataset($id: ID!, $name: String!) {\n  updateDataset(input: {id: $id, name: $name}) {\n    id\n    name\n  }\n}"


class RevertDatasetMutationRevertdataset(BaseModel):
    typename: Optional[Literal["Dataset"]] = Field(alias="__typename", exclude=True)
    id: ID
    name: str
    description: Optional[str]

    class Config:
        """A config class"""

        frozen = True


class RevertDatasetMutation(BaseModel):
    revert_dataset: RevertDatasetMutationRevertdataset = Field(alias="revertDataset")

    class Arguments(BaseModel):
        dataset: ID
        history: ID

    class Meta:
        document = "mutation RevertDataset($dataset: ID!, $history: ID!) {\n  revertDataset(input: {id: $dataset, historyId: $history}) {\n    id\n    name\n    description\n  }\n}"


class CreateFluorophoreMutationCreatefluorophore(BaseModel):
    typename: Optional[Literal["Fluorophore"]] = Field(alias="__typename", exclude=True)
    id: ID
    name: str

    class Config:
        """A config class"""

        frozen = True


class CreateFluorophoreMutation(BaseModel):
    create_fluorophore: CreateFluorophoreMutationCreatefluorophore = Field(
        alias="createFluorophore"
    )

    class Arguments(BaseModel):
        name: str
        excitation_wavelength: Optional[Micrometers] = Field(
            alias="excitationWavelength", default=None
        )
        emission_wavelength: Optional[Micrometers] = Field(
            alias="emissionWavelength", default=None
        )

    class Meta:
        document = "mutation CreateFluorophore($name: String!, $excitationWavelength: Micrometers, $emissionWavelength: Micrometers) {\n  createFluorophore(\n    input: {name: $name, excitationWavelength: $excitationWavelength, emissionWavelength: $emissionWavelength}\n  ) {\n    id\n    name\n  }\n}"


class EnsureFluorophoreMutationEnsurefluorophore(BaseModel):
    typename: Optional[Literal["Fluorophore"]] = Field(alias="__typename", exclude=True)
    id: ID
    name: str

    class Config:
        """A config class"""

        frozen = True


class EnsureFluorophoreMutation(BaseModel):
    ensure_fluorophore: EnsureFluorophoreMutationEnsurefluorophore = Field(
        alias="ensureFluorophore"
    )

    class Arguments(BaseModel):
        name: str
        excitation_wavelength: Optional[Micrometers] = Field(
            alias="excitationWavelength", default=None
        )
        emission_wavelength: Optional[Micrometers] = Field(
            alias="emissionWavelength", default=None
        )

    class Meta:
        document = "mutation EnsureFluorophore($name: String!, $excitationWavelength: Micrometers, $emissionWavelength: Micrometers) {\n  ensureFluorophore(\n    input: {name: $name, excitationWavelength: $excitationWavelength, emissionWavelength: $emissionWavelength}\n  ) {\n    id\n    name\n  }\n}"


class From_array_likeMutation(BaseModel):
    from_array_like: ImageFragment = Field(alias="fromArrayLike")

    class Arguments(BaseModel):
        array: ArrayLike
        name: str
        origins: Optional[List[ID]] = Field(default=None)
        channel_views: Optional[List[PartialChannelViewInput]] = Field(
            alias="channelViews", default=None
        )
        transformation_views: Optional[
            List[PartialAffineTransformationViewInput]
        ] = Field(alias="transformationViews", default=None)
        label_views: Optional[List[PartialLabelViewInput]] = Field(
            alias="labelViews", default=None
        )
        rgb_views: Optional[List[PartialRGBViewInput]] = Field(
            alias="rgbViews", default=None
        )
        acquisition_views: Optional[List[PartialAcquisitionViewInput]] = Field(
            alias="acquisitionViews", default=None
        )
        timepoint_views: Optional[List[PartialTimepointViewInput]] = Field(
            alias="timepointViews", default=None
        )
        optics_views: Optional[List[PartialOpticsViewInput]] = Field(
            alias="opticsViews", default=None
        )
        tags: Optional[List[str]] = Field(default=None)

    class Meta:
        document = "fragment View on View {\n  zMin\n  zMax\n}\n\nfragment Antibody on Antibody {\n  name\n  epitope\n}\n\nfragment Era on Era {\n  id\n  begin\n  name\n}\n\nfragment Channel on Channel {\n  id\n  name\n  excitationWavelength\n}\n\nfragment Fluorophore on Fluorophore {\n  id\n  name\n  emissionWavelength\n  excitationWavelength\n}\n\nfragment TimepointView on TimepointView {\n  ...View\n  id\n  msSinceStart\n  indexSinceStart\n  era {\n    ...Era\n  }\n}\n\nfragment ZarrStore on ZarrStore {\n  id\n  key\n  bucket\n  path\n}\n\nfragment OpticsView on OpticsView {\n  ...View\n  objective {\n    id\n    name\n    serialNumber\n  }\n  camera {\n    id\n    name\n    serialNumber\n  }\n  instrument {\n    id\n    name\n    serialNumber\n  }\n}\n\nfragment LabelView on LabelView {\n  ...View\n  id\n  fluorophore {\n    ...Fluorophore\n  }\n  primaryAntibody {\n    ...Antibody\n  }\n  secondaryAntibody {\n    ...Antibody\n  }\n}\n\nfragment ChannelView on ChannelView {\n  ...View\n  id\n  channel {\n    ...Channel\n  }\n}\n\nfragment AffineTransformationView on AffineTransformationView {\n  ...View\n  id\n  affineMatrix\n  stage {\n    id\n  }\n}\n\nfragment Image on Image {\n  origins {\n    id\n  }\n  id\n  name\n  store {\n    ...ZarrStore\n  }\n  views {\n    ...ChannelView\n    ...AffineTransformationView\n    ...LabelView\n    ...TimepointView\n    ...OpticsView\n  }\n}\n\nmutation from_array_like($array: ArrayLike!, $name: String!, $origins: [ID!], $channelViews: [PartialChannelViewInput!], $transformationViews: [PartialAffineTransformationViewInput!], $labelViews: [PartialLabelViewInput!], $rgbViews: [PartialRGBViewInput!], $acquisitionViews: [PartialAcquisitionViewInput!], $timepointViews: [PartialTimepointViewInput!], $opticsViews: [PartialOpticsViewInput!], $tags: [String!]) {\n  fromArrayLike(\n    input: {array: $array, name: $name, origins: $origins, channelViews: $channelViews, transformationViews: $transformationViews, acquisitionViews: $acquisitionViews, labelViews: $labelViews, timepointViews: $timepointViews, opticsViews: $opticsViews, rgbViews: $rgbViews, tags: $tags}\n  ) {\n    ...Image\n  }\n}"


class RequestUploadMutation(BaseModel):
    request_upload: CredentialsFragment = Field(alias="requestUpload")

    class Arguments(BaseModel):
        key: str
        datalayer: str

    class Meta:
        document = "fragment Credentials on Credentials {\n  accessKey\n  status\n  secretKey\n  bucket\n  key\n  sessionToken\n  store\n}\n\nmutation RequestUpload($key: String!, $datalayer: String!) {\n  requestUpload(input: {key: $key, datalayer: $datalayer}) {\n    ...Credentials\n  }\n}"


class RequestAccessMutation(BaseModel):
    request_access: AccessCredentialsFragment = Field(alias="requestAccess")
    "Request upload credentials for a given key"

    class Arguments(BaseModel):
        store: ID
        duration: Optional[int] = Field(default=None)

    class Meta:
        document = "fragment AccessCredentials on AccessCredentials {\n  accessKey\n  secretKey\n  bucket\n  key\n  sessionToken\n  path\n}\n\nmutation RequestAccess($store: ID!, $duration: Int) {\n  requestAccess(input: {store: $store, duration: $duration}) {\n    ...AccessCredentials\n  }\n}"


class CreateObjectiveMutationCreateobjective(Objective, BaseModel):
    typename: Optional[Literal["Objective"]] = Field(alias="__typename", exclude=True)
    id: ID
    name: str

    class Config:
        """A config class"""

        frozen = True


class CreateObjectiveMutation(BaseModel):
    create_objective: CreateObjectiveMutationCreateobjective = Field(
        alias="createObjective"
    )

    class Arguments(BaseModel):
        serial_number: str = Field(alias="serialNumber")
        name: Optional[str] = Field(default=None)
        na: Optional[float] = Field(default=None)
        magnification: Optional[float] = Field(default=None)

    class Meta:
        document = "mutation CreateObjective($serialNumber: String!, $name: String, $na: Float, $magnification: Float) {\n  createObjective(\n    input: {name: $name, na: $na, serialNumber: $serialNumber, magnification: $magnification}\n  ) {\n    id\n    name\n  }\n}"


class EnsureObjectiveMutationEnsureobjective(Objective, BaseModel):
    typename: Optional[Literal["Objective"]] = Field(alias="__typename", exclude=True)
    id: ID
    name: str

    class Config:
        """A config class"""

        frozen = True


class EnsureObjectiveMutation(BaseModel):
    ensure_objective: EnsureObjectiveMutationEnsureobjective = Field(
        alias="ensureObjective"
    )

    class Arguments(BaseModel):
        serial_number: str = Field(alias="serialNumber")
        name: Optional[str] = Field(default=None)
        na: Optional[float] = Field(default=None)
        magnification: Optional[float] = Field(default=None)

    class Meta:
        document = "mutation EnsureObjective($serialNumber: String!, $name: String, $na: Float, $magnification: Float) {\n  ensureObjective(\n    input: {name: $name, na: $na, serialNumber: $serialNumber, magnification: $magnification}\n  ) {\n    id\n    name\n  }\n}"


class CreateCameraMutationCreatecamera(BaseModel):
    typename: Optional[Literal["Camera"]] = Field(alias="__typename", exclude=True)
    id: ID
    name: str

    class Config:
        """A config class"""

        frozen = True


class CreateCameraMutation(BaseModel):
    create_camera: CreateCameraMutationCreatecamera = Field(alias="createCamera")

    class Arguments(BaseModel):
        serial_number: str = Field(alias="serialNumber")
        name: Optional[str] = Field(default=None)
        pixel_size_x: Optional[Micrometers] = Field(alias="pixelSizeX", default=None)
        pixel_size_y: Optional[Micrometers] = Field(alias="pixelSizeY", default=None)
        sensor_size_x: Optional[int] = Field(alias="sensorSizeX", default=None)
        sensor_size_y: Optional[int] = Field(alias="sensorSizeY", default=None)

    class Meta:
        document = "mutation CreateCamera($serialNumber: String!, $name: String, $pixelSizeX: Micrometers, $pixelSizeY: Micrometers, $sensorSizeX: Int, $sensorSizeY: Int) {\n  createCamera(\n    input: {name: $name, pixelSizeX: $pixelSizeX, serialNumber: $serialNumber, pixelSizeY: $pixelSizeY, sensorSizeX: $sensorSizeX, sensorSizeY: $sensorSizeY}\n  ) {\n    id\n    name\n  }\n}"


class EnsureCameraMutationEnsurecamera(BaseModel):
    typename: Optional[Literal["Camera"]] = Field(alias="__typename", exclude=True)
    id: ID
    name: str

    class Config:
        """A config class"""

        frozen = True


class EnsureCameraMutation(BaseModel):
    ensure_camera: EnsureCameraMutationEnsurecamera = Field(alias="ensureCamera")

    class Arguments(BaseModel):
        serial_number: str = Field(alias="serialNumber")
        name: Optional[str] = Field(default=None)
        pixel_size_x: Optional[Micrometers] = Field(alias="pixelSizeX", default=None)
        pixel_size_y: Optional[Micrometers] = Field(alias="pixelSizeY", default=None)
        sensor_size_x: Optional[int] = Field(alias="sensorSizeX", default=None)
        sensor_size_y: Optional[int] = Field(alias="sensorSizeY", default=None)

    class Meta:
        document = "mutation EnsureCamera($serialNumber: String!, $name: String, $pixelSizeX: Micrometers, $pixelSizeY: Micrometers, $sensorSizeX: Int, $sensorSizeY: Int) {\n  ensureCamera(\n    input: {name: $name, pixelSizeX: $pixelSizeX, serialNumber: $serialNumber, pixelSizeY: $pixelSizeY, sensorSizeX: $sensorSizeX, sensorSizeY: $sensorSizeY}\n  ) {\n    id\n    name\n  }\n}"


class GetTableQuery(BaseModel):
    table: TableFragment

    class Arguments(BaseModel):
        id: ID

    class Meta:
        document = "fragment ParquetStore on ParquetStore {\n  id\n  key\n  bucket\n  path\n}\n\nfragment Table on Table {\n  origins {\n    id\n  }\n  id\n  name\n  store {\n    ...ParquetStore\n  }\n}\n\nquery GetTable($id: ID!) {\n  table(id: $id) {\n    ...Table\n  }\n}"


class GetFileQuery(BaseModel):
    file: FileFragment

    class Arguments(BaseModel):
        id: ID

    class Meta:
        document = "fragment BigFileStore on BigFileStore {\n  id\n  key\n  bucket\n  path\n}\n\nfragment File on File {\n  origins {\n    id\n  }\n  id\n  name\n  store {\n    ...BigFileStore\n  }\n}\n\nquery GetFile($id: ID!) {\n  file(id: $id) {\n    ...File\n  }\n}"


class GetInstrumentQuery(BaseModel):
    instrument: InstrumentFragment

    class Arguments(BaseModel):
        id: ID

    class Meta:
        document = "fragment Instrument on Instrument {\n  id\n  model\n  name\n  serialNumber\n}\n\nquery GetInstrument($id: ID!) {\n  instrument(id: $id) {\n    ...Instrument\n  }\n}"


class GetSnapshotQuery(BaseModel):
    snapshot: SnapshotFragment

    class Arguments(BaseModel):
        id: ID

    class Meta:
        document = "fragment Snapshot on Snapshot {\n  id\n  store {\n    key\n    presignedUrl\n  }\n  name\n}\n\nquery GetSnapshot($id: ID!) {\n  snapshot(id: $id) {\n    ...Snapshot\n  }\n}"


class SearchSnapshotsQueryOptions(BaseModel):
    typename: Optional[Literal["Snapshot"]] = Field(alias="__typename", exclude=True)
    value: ID
    label: str

    class Config:
        """A config class"""

        frozen = True


class SearchSnapshotsQuery(BaseModel):
    options: Tuple[SearchSnapshotsQueryOptions, ...]

    class Arguments(BaseModel):
        search: Optional[str] = Field(default=None)
        values: Optional[List[ID]] = Field(default=None)

    class Meta:
        document = "query SearchSnapshots($search: String, $values: [ID!]) {\n  options: snapshots(\n    filters: {name: {contains: $search}, ids: $values}\n    pagination: {limit: 10}\n  ) {\n    value: id\n    label: name\n  }\n}"


class GetDatasetQuery(BaseModel):
    dataset: DatasetFragment

    class Arguments(BaseModel):
        id: ID

    class Meta:
        document = "fragment HistoryStuff on History {\n  id\n  app {\n    id\n  }\n}\n\nfragment Dataset on Dataset {\n  name\n  description\n  history {\n    ...HistoryStuff\n  }\n}\n\nquery GetDataset($id: ID!) {\n  dataset(id: $id) {\n    ...Dataset\n  }\n}"


class ImagesQueryImages(Image, BaseModel):
    typename: Optional[Literal["Image"]] = Field(alias="__typename", exclude=True)
    id: ID

    class Config:
        """A config class"""

        frozen = True


class ImagesQuery(BaseModel):
    images: Tuple[ImagesQueryImages, ...]

    class Arguments(BaseModel):
        pass

    class Meta:
        document = "query Images {\n  images {\n    id\n  }\n}"


class GetImageQuery(BaseModel):
    image: ImageFragment

    class Arguments(BaseModel):
        id: ID

    class Meta:
        document = "fragment View on View {\n  zMin\n  zMax\n}\n\nfragment Antibody on Antibody {\n  name\n  epitope\n}\n\nfragment Era on Era {\n  id\n  begin\n  name\n}\n\nfragment Channel on Channel {\n  id\n  name\n  excitationWavelength\n}\n\nfragment Fluorophore on Fluorophore {\n  id\n  name\n  emissionWavelength\n  excitationWavelength\n}\n\nfragment TimepointView on TimepointView {\n  ...View\n  id\n  msSinceStart\n  indexSinceStart\n  era {\n    ...Era\n  }\n}\n\nfragment ZarrStore on ZarrStore {\n  id\n  key\n  bucket\n  path\n}\n\nfragment OpticsView on OpticsView {\n  ...View\n  objective {\n    id\n    name\n    serialNumber\n  }\n  camera {\n    id\n    name\n    serialNumber\n  }\n  instrument {\n    id\n    name\n    serialNumber\n  }\n}\n\nfragment LabelView on LabelView {\n  ...View\n  id\n  fluorophore {\n    ...Fluorophore\n  }\n  primaryAntibody {\n    ...Antibody\n  }\n  secondaryAntibody {\n    ...Antibody\n  }\n}\n\nfragment ChannelView on ChannelView {\n  ...View\n  id\n  channel {\n    ...Channel\n  }\n}\n\nfragment AffineTransformationView on AffineTransformationView {\n  ...View\n  id\n  affineMatrix\n  stage {\n    id\n  }\n}\n\nfragment Image on Image {\n  origins {\n    id\n  }\n  id\n  name\n  store {\n    ...ZarrStore\n  }\n  views {\n    ...ChannelView\n    ...AffineTransformationView\n    ...LabelView\n    ...TimepointView\n    ...OpticsView\n  }\n}\n\nquery GetImage($id: ID!) {\n  image(id: $id) {\n    ...Image\n  }\n}"


class GetRandomImageQuery(BaseModel):
    random_image: ImageFragment = Field(alias="randomImage")

    class Arguments(BaseModel):
        pass

    class Meta:
        document = "fragment View on View {\n  zMin\n  zMax\n}\n\nfragment Antibody on Antibody {\n  name\n  epitope\n}\n\nfragment Era on Era {\n  id\n  begin\n  name\n}\n\nfragment Channel on Channel {\n  id\n  name\n  excitationWavelength\n}\n\nfragment Fluorophore on Fluorophore {\n  id\n  name\n  emissionWavelength\n  excitationWavelength\n}\n\nfragment TimepointView on TimepointView {\n  ...View\n  id\n  msSinceStart\n  indexSinceStart\n  era {\n    ...Era\n  }\n}\n\nfragment ZarrStore on ZarrStore {\n  id\n  key\n  bucket\n  path\n}\n\nfragment OpticsView on OpticsView {\n  ...View\n  objective {\n    id\n    name\n    serialNumber\n  }\n  camera {\n    id\n    name\n    serialNumber\n  }\n  instrument {\n    id\n    name\n    serialNumber\n  }\n}\n\nfragment LabelView on LabelView {\n  ...View\n  id\n  fluorophore {\n    ...Fluorophore\n  }\n  primaryAntibody {\n    ...Antibody\n  }\n  secondaryAntibody {\n    ...Antibody\n  }\n}\n\nfragment ChannelView on ChannelView {\n  ...View\n  id\n  channel {\n    ...Channel\n  }\n}\n\nfragment AffineTransformationView on AffineTransformationView {\n  ...View\n  id\n  affineMatrix\n  stage {\n    id\n  }\n}\n\nfragment Image on Image {\n  origins {\n    id\n  }\n  id\n  name\n  store {\n    ...ZarrStore\n  }\n  views {\n    ...ChannelView\n    ...AffineTransformationView\n    ...LabelView\n    ...TimepointView\n    ...OpticsView\n  }\n}\n\nquery GetRandomImage {\n  randomImage {\n    ...Image\n  }\n}"


class SearchImagesQueryOptions(Image, BaseModel):
    typename: Optional[Literal["Image"]] = Field(alias="__typename", exclude=True)
    value: ID
    label: str

    class Config:
        """A config class"""

        frozen = True


class SearchImagesQuery(BaseModel):
    options: Tuple[SearchImagesQueryOptions, ...]

    class Arguments(BaseModel):
        search: Optional[str] = Field(default=None)
        values: Optional[List[ID]] = Field(default=None)

    class Meta:
        document = "query SearchImages($search: String, $values: [ID!]) {\n  options: images(\n    filters: {name: {contains: $search}, ids: $values}\n    pagination: {limit: 10}\n  ) {\n    value: id\n    label: name\n  }\n}"


class GetObjectiveQuery(BaseModel):
    objective: ObjectiveFragment

    class Arguments(BaseModel):
        id: ID

    class Meta:
        document = "fragment Objective on Objective {\n  id\n  na\n  name\n  serialNumber\n}\n\nquery GetObjective($id: ID!) {\n  objective(id: $id) {\n    ...Objective\n  }\n}"


class GetCameraQuery(BaseModel):
    camera: CameraFragment

    class Arguments(BaseModel):
        id: ID

    class Meta:
        document = "fragment Camera on Camera {\n  sensorSizeX\n  sensorSizeY\n  pixelSizeX\n  pixelSizeY\n  name\n  serialNumber\n}\n\nquery GetCamera($id: ID!) {\n  camera(id: $id) {\n    ...Camera\n  }\n}"


async def afrom_parquet_like(
    dataframe: ParquetLike,
    name: str,
    origins: Optional[List[ID]] = None,
    dataset: Optional[ID] = None,
    rath: Optional[MikroNextRath] = None,
) -> TableFragment:
    """from_parquet_like



    Arguments:
        dataframe (ParquetLike): dataframe
        name (str): name
        origins (Optional[List[ID]], optional): origins.
        dataset (Optional[ID], optional): dataset.
        rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

    Returns:
        TableFragment"""
    return (
        await aexecute(
            From_parquet_likeMutation,
            {
                "dataframe": dataframe,
                "name": name,
                "origins": origins,
                "dataset": dataset,
            },
            rath=rath,
        )
    ).from_parquet_like


def from_parquet_like(
    dataframe: ParquetLike,
    name: str,
    origins: Optional[List[ID]] = None,
    dataset: Optional[ID] = None,
    rath: Optional[MikroNextRath] = None,
) -> TableFragment:
    """from_parquet_like



    Arguments:
        dataframe (ParquetLike): dataframe
        name (str): name
        origins (Optional[List[ID]], optional): origins.
        dataset (Optional[ID], optional): dataset.
        rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

    Returns:
        TableFragment"""
    return execute(
        From_parquet_likeMutation,
        {"dataframe": dataframe, "name": name, "origins": origins, "dataset": dataset},
        rath=rath,
    ).from_parquet_like


async def arequest_table_upload(
    key: str, datalayer: str, rath: Optional[MikroNextRath] = None
) -> CredentialsFragment:
    """RequestTableUpload


     requestTableUpload: Temporary Credentials for a file upload that can be used by a Client (e.g. in a python datalayer)


    Arguments:
        key (str): key
        datalayer (str): datalayer
        rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

    Returns:
        CredentialsFragment"""
    return (
        await aexecute(
            RequestTableUploadMutation, {"key": key, "datalayer": datalayer}, rath=rath
        )
    ).request_table_upload


def request_table_upload(
    key: str, datalayer: str, rath: Optional[MikroNextRath] = None
) -> CredentialsFragment:
    """RequestTableUpload


     requestTableUpload: Temporary Credentials for a file upload that can be used by a Client (e.g. in a python datalayer)


    Arguments:
        key (str): key
        datalayer (str): datalayer
        rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

    Returns:
        CredentialsFragment"""
    return execute(
        RequestTableUploadMutation, {"key": key, "datalayer": datalayer}, rath=rath
    ).request_table_upload


async def arequest_table_access(
    store: ID, duration: Optional[int] = None, rath: Optional[MikroNextRath] = None
) -> AccessCredentialsFragment:
    """RequestTableAccess


     requestTableAccess: Temporary Credentials for a file download that can be used by a Client (e.g. in a python datalayer)


    Arguments:
        store (ID): store
        duration (Optional[int], optional): duration.
        rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

    Returns:
        AccessCredentialsFragment"""
    return (
        await aexecute(
            RequestTableAccessMutation,
            {"store": store, "duration": duration},
            rath=rath,
        )
    ).request_table_access


def request_table_access(
    store: ID, duration: Optional[int] = None, rath: Optional[MikroNextRath] = None
) -> AccessCredentialsFragment:
    """RequestTableAccess


     requestTableAccess: Temporary Credentials for a file download that can be used by a Client (e.g. in a python datalayer)


    Arguments:
        store (ID): store
        duration (Optional[int], optional): duration.
        rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

    Returns:
        AccessCredentialsFragment"""
    return execute(
        RequestTableAccessMutation, {"store": store, "duration": duration}, rath=rath
    ).request_table_access


async def acreate_stage(
    name: str, rath: Optional[MikroNextRath] = None
) -> CreateStageMutationCreatestage:
    """CreateStage



    Arguments:
        name (str): name
        rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

    Returns:
        CreateStageMutationCreatestage"""
    return (await aexecute(CreateStageMutation, {"name": name}, rath=rath)).create_stage


def create_stage(
    name: str, rath: Optional[MikroNextRath] = None
) -> CreateStageMutationCreatestage:
    """CreateStage



    Arguments:
        name (str): name
        rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

    Returns:
        CreateStageMutationCreatestage"""
    return execute(CreateStageMutation, {"name": name}, rath=rath).create_stage


async def acreate_channel(
    name: str, rath: Optional[MikroNextRath] = None
) -> CreateChannelMutationCreatechannel:
    """CreateChannel



    Arguments:
        name (str): name
        rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

    Returns:
        CreateChannelMutationCreatechannel"""
    return (
        await aexecute(CreateChannelMutation, {"name": name}, rath=rath)
    ).create_channel


def create_channel(
    name: str, rath: Optional[MikroNextRath] = None
) -> CreateChannelMutationCreatechannel:
    """CreateChannel



    Arguments:
        name (str): name
        rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

    Returns:
        CreateChannelMutationCreatechannel"""
    return execute(CreateChannelMutation, {"name": name}, rath=rath).create_channel


async def aensure_channel(
    name: str, rath: Optional[MikroNextRath] = None
) -> EnsureChannelMutationEnsurechannel:
    """EnsureChannel



    Arguments:
        name (str): name
        rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

    Returns:
        EnsureChannelMutationEnsurechannel"""
    return (
        await aexecute(EnsureChannelMutation, {"name": name}, rath=rath)
    ).ensure_channel


def ensure_channel(
    name: str, rath: Optional[MikroNextRath] = None
) -> EnsureChannelMutationEnsurechannel:
    """EnsureChannel



    Arguments:
        name (str): name
        rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

    Returns:
        EnsureChannelMutationEnsurechannel"""
    return execute(EnsureChannelMutation, {"name": name}, rath=rath).ensure_channel


async def acreate_era(
    name: str, begin: Optional[datetime] = None, rath: Optional[MikroNextRath] = None
) -> CreateEraMutationCreateera:
    """CreateEra



    Arguments:
        name (str): name
        begin (Optional[datetime], optional): begin.
        rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

    Returns:
        CreateEraMutationCreateera"""
    return (
        await aexecute(CreateEraMutation, {"name": name, "begin": begin}, rath=rath)
    ).create_era


def create_era(
    name: str, begin: Optional[datetime] = None, rath: Optional[MikroNextRath] = None
) -> CreateEraMutationCreateera:
    """CreateEra



    Arguments:
        name (str): name
        begin (Optional[datetime], optional): begin.
        rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

    Returns:
        CreateEraMutationCreateera"""
    return execute(
        CreateEraMutation, {"name": name, "begin": begin}, rath=rath
    ).create_era


async def acreate_rgb_view(
    image: ID,
    r_scale: float,
    b_scale: float,
    g_scale: float,
    context: Optional[ID] = None,
    rath: Optional[MikroNextRath] = None,
) -> CreateRgbViewMutationCreatergbview:
    """CreateRgbView



    Arguments:
        image (ID): image
        r_scale (float): rScale
        b_scale (float): bScale
        g_scale (float): gScale
        context (Optional[ID], optional): context.
        rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

    Returns:
        CreateRgbViewMutationCreatergbview"""
    return (
        await aexecute(
            CreateRgbViewMutation,
            {
                "image": image,
                "rScale": r_scale,
                "bScale": b_scale,
                "gScale": g_scale,
                "context": context,
            },
            rath=rath,
        )
    ).create_rgb_view


def create_rgb_view(
    image: ID,
    r_scale: float,
    b_scale: float,
    g_scale: float,
    context: Optional[ID] = None,
    rath: Optional[MikroNextRath] = None,
) -> CreateRgbViewMutationCreatergbview:
    """CreateRgbView



    Arguments:
        image (ID): image
        r_scale (float): rScale
        b_scale (float): bScale
        g_scale (float): gScale
        context (Optional[ID], optional): context.
        rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

    Returns:
        CreateRgbViewMutationCreatergbview"""
    return execute(
        CreateRgbViewMutation,
        {
            "image": image,
            "rScale": r_scale,
            "bScale": b_scale,
            "gScale": g_scale,
            "context": context,
        },
        rath=rath,
    ).create_rgb_view


async def afrom_file_like(
    file: FileLike,
    name: str,
    origins: Optional[List[ID]] = None,
    dataset: Optional[ID] = None,
    rath: Optional[MikroNextRath] = None,
) -> FileFragment:
    """from_file_like



    Arguments:
        file (FileLike): file
        name (str): name
        origins (Optional[List[ID]], optional): origins.
        dataset (Optional[ID], optional): dataset.
        rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

    Returns:
        FileFragment"""
    return (
        await aexecute(
            From_file_likeMutation,
            {"file": file, "name": name, "origins": origins, "dataset": dataset},
            rath=rath,
        )
    ).from_file_like


def from_file_like(
    file: FileLike,
    name: str,
    origins: Optional[List[ID]] = None,
    dataset: Optional[ID] = None,
    rath: Optional[MikroNextRath] = None,
) -> FileFragment:
    """from_file_like



    Arguments:
        file (FileLike): file
        name (str): name
        origins (Optional[List[ID]], optional): origins.
        dataset (Optional[ID], optional): dataset.
        rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

    Returns:
        FileFragment"""
    return execute(
        From_file_likeMutation,
        {"file": file, "name": name, "origins": origins, "dataset": dataset},
        rath=rath,
    ).from_file_like


async def arequest_file_upload(
    key: str, datalayer: str, rath: Optional[MikroNextRath] = None
) -> CredentialsFragment:
    """RequestFileUpload


     requestFileUpload: Temporary Credentials for a file upload that can be used by a Client (e.g. in a python datalayer)


    Arguments:
        key (str): key
        datalayer (str): datalayer
        rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

    Returns:
        CredentialsFragment"""
    return (
        await aexecute(
            RequestFileUploadMutation, {"key": key, "datalayer": datalayer}, rath=rath
        )
    ).request_file_upload


def request_file_upload(
    key: str, datalayer: str, rath: Optional[MikroNextRath] = None
) -> CredentialsFragment:
    """RequestFileUpload


     requestFileUpload: Temporary Credentials for a file upload that can be used by a Client (e.g. in a python datalayer)


    Arguments:
        key (str): key
        datalayer (str): datalayer
        rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

    Returns:
        CredentialsFragment"""
    return execute(
        RequestFileUploadMutation, {"key": key, "datalayer": datalayer}, rath=rath
    ).request_file_upload


async def arequest_file_access(
    store: ID, duration: Optional[int] = None, rath: Optional[MikroNextRath] = None
) -> AccessCredentialsFragment:
    """RequestFileAccess


     requestFileAccess: Temporary Credentials for a file download that can be used by a Client (e.g. in a python datalayer)


    Arguments:
        store (ID): store
        duration (Optional[int], optional): duration.
        rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

    Returns:
        AccessCredentialsFragment"""
    return (
        await aexecute(
            RequestFileAccessMutation, {"store": store, "duration": duration}, rath=rath
        )
    ).request_file_access


def request_file_access(
    store: ID, duration: Optional[int] = None, rath: Optional[MikroNextRath] = None
) -> AccessCredentialsFragment:
    """RequestFileAccess


     requestFileAccess: Temporary Credentials for a file download that can be used by a Client (e.g. in a python datalayer)


    Arguments:
        store (ID): store
        duration (Optional[int], optional): duration.
        rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

    Returns:
        AccessCredentialsFragment"""
    return execute(
        RequestFileAccessMutation, {"store": store, "duration": duration}, rath=rath
    ).request_file_access


async def acreate_rgb_context(
    name: str, rath: Optional[MikroNextRath] = None
) -> CreateRGBContextMutationCreatergbcontext:
    """CreateRGBContext



    Arguments:
        name (str): name
        rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

    Returns:
        CreateRGBContextMutationCreatergbcontext"""
    return (
        await aexecute(CreateRGBContextMutation, {"name": name}, rath=rath)
    ).create_rgb_context


def create_rgb_context(
    name: str, rath: Optional[MikroNextRath] = None
) -> CreateRGBContextMutationCreatergbcontext:
    """CreateRGBContext



    Arguments:
        name (str): name
        rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

    Returns:
        CreateRGBContextMutationCreatergbcontext"""
    return execute(
        CreateRGBContextMutation, {"name": name}, rath=rath
    ).create_rgb_context


async def acreate_instrument(
    serial_number: str,
    name: Optional[str] = None,
    model: Optional[str] = None,
    rath: Optional[MikroNextRath] = None,
) -> CreateInstrumentMutationCreateinstrument:
    """CreateInstrument



    Arguments:
        serial_number (str): serialNumber
        name (Optional[str], optional): name.
        model (Optional[str], optional): model.
        rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

    Returns:
        CreateInstrumentMutationCreateinstrument"""
    return (
        await aexecute(
            CreateInstrumentMutation,
            {"serialNumber": serial_number, "name": name, "model": model},
            rath=rath,
        )
    ).create_instrument


def create_instrument(
    serial_number: str,
    name: Optional[str] = None,
    model: Optional[str] = None,
    rath: Optional[MikroNextRath] = None,
) -> CreateInstrumentMutationCreateinstrument:
    """CreateInstrument



    Arguments:
        serial_number (str): serialNumber
        name (Optional[str], optional): name.
        model (Optional[str], optional): model.
        rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

    Returns:
        CreateInstrumentMutationCreateinstrument"""
    return execute(
        CreateInstrumentMutation,
        {"serialNumber": serial_number, "name": name, "model": model},
        rath=rath,
    ).create_instrument


async def aensure_instrument(
    serial_number: str,
    name: Optional[str] = None,
    model: Optional[str] = None,
    rath: Optional[MikroNextRath] = None,
) -> EnsureInstrumentMutationEnsureinstrument:
    """EnsureInstrument



    Arguments:
        serial_number (str): serialNumber
        name (Optional[str], optional): name.
        model (Optional[str], optional): model.
        rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

    Returns:
        EnsureInstrumentMutationEnsureinstrument"""
    return (
        await aexecute(
            EnsureInstrumentMutation,
            {"serialNumber": serial_number, "name": name, "model": model},
            rath=rath,
        )
    ).ensure_instrument


def ensure_instrument(
    serial_number: str,
    name: Optional[str] = None,
    model: Optional[str] = None,
    rath: Optional[MikroNextRath] = None,
) -> EnsureInstrumentMutationEnsureinstrument:
    """EnsureInstrument



    Arguments:
        serial_number (str): serialNumber
        name (Optional[str], optional): name.
        model (Optional[str], optional): model.
        rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

    Returns:
        EnsureInstrumentMutationEnsureinstrument"""
    return execute(
        EnsureInstrumentMutation,
        {"serialNumber": serial_number, "name": name, "model": model},
        rath=rath,
    ).ensure_instrument


async def acreate_view_collection(
    name: str, rath: Optional[MikroNextRath] = None
) -> CreateViewCollectionMutationCreateviewcollection:
    """CreateViewCollection



    Arguments:
        name (str): name
        rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

    Returns:
        CreateViewCollectionMutationCreateviewcollection"""
    return (
        await aexecute(CreateViewCollectionMutation, {"name": name}, rath=rath)
    ).create_view_collection


def create_view_collection(
    name: str, rath: Optional[MikroNextRath] = None
) -> CreateViewCollectionMutationCreateviewcollection:
    """CreateViewCollection



    Arguments:
        name (str): name
        rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

    Returns:
        CreateViewCollectionMutationCreateviewcollection"""
    return execute(
        CreateViewCollectionMutation, {"name": name}, rath=rath
    ).create_view_collection


async def acreate_antibody(
    name: str, epitope: Optional[str] = None, rath: Optional[MikroNextRath] = None
) -> CreateAntibodyMutationCreateantibody:
    """CreateAntibody



    Arguments:
        name (str): name
        epitope (Optional[str], optional): epitope.
        rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

    Returns:
        CreateAntibodyMutationCreateantibody"""
    return (
        await aexecute(
            CreateAntibodyMutation, {"name": name, "epitope": epitope}, rath=rath
        )
    ).create_antibody


def create_antibody(
    name: str, epitope: Optional[str] = None, rath: Optional[MikroNextRath] = None
) -> CreateAntibodyMutationCreateantibody:
    """CreateAntibody



    Arguments:
        name (str): name
        epitope (Optional[str], optional): epitope.
        rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

    Returns:
        CreateAntibodyMutationCreateantibody"""
    return execute(
        CreateAntibodyMutation, {"name": name, "epitope": epitope}, rath=rath
    ).create_antibody


async def aensure_antibody(
    name: str, epitope: Optional[str] = None, rath: Optional[MikroNextRath] = None
) -> EnsureAntibodyMutationEnsureantibody:
    """EnsureAntibody



    Arguments:
        name (str): name
        epitope (Optional[str], optional): epitope.
        rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

    Returns:
        EnsureAntibodyMutationEnsureantibody"""
    return (
        await aexecute(
            EnsureAntibodyMutation, {"name": name, "epitope": epitope}, rath=rath
        )
    ).ensure_antibody


def ensure_antibody(
    name: str, epitope: Optional[str] = None, rath: Optional[MikroNextRath] = None
) -> EnsureAntibodyMutationEnsureantibody:
    """EnsureAntibody



    Arguments:
        name (str): name
        epitope (Optional[str], optional): epitope.
        rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

    Returns:
        EnsureAntibodyMutationEnsureantibody"""
    return execute(
        EnsureAntibodyMutation, {"name": name, "epitope": epitope}, rath=rath
    ).ensure_antibody


async def acreate_snapshot(
    image: ID, file: Upload, rath: Optional[MikroNextRath] = None
) -> SnapshotFragment:
    """CreateSnapshot



    Arguments:
        image (ID): image
        file (Upload): file
        rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

    Returns:
        SnapshotFragment"""
    return (
        await aexecute(
            CreateSnapshotMutation, {"image": image, "file": file}, rath=rath
        )
    ).create_snapshot


def create_snapshot(
    image: ID, file: Upload, rath: Optional[MikroNextRath] = None
) -> SnapshotFragment:
    """CreateSnapshot



    Arguments:
        image (ID): image
        file (Upload): file
        rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

    Returns:
        SnapshotFragment"""
    return execute(
        CreateSnapshotMutation, {"image": image, "file": file}, rath=rath
    ).create_snapshot


async def acreate_dataset(
    name: str, rath: Optional[MikroNextRath] = None
) -> CreateDatasetMutationCreatedataset:
    """CreateDataset



    Arguments:
        name (str): name
        rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

    Returns:
        CreateDatasetMutationCreatedataset"""
    return (
        await aexecute(CreateDatasetMutation, {"name": name}, rath=rath)
    ).create_dataset


def create_dataset(
    name: str, rath: Optional[MikroNextRath] = None
) -> CreateDatasetMutationCreatedataset:
    """CreateDataset



    Arguments:
        name (str): name
        rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

    Returns:
        CreateDatasetMutationCreatedataset"""
    return execute(CreateDatasetMutation, {"name": name}, rath=rath).create_dataset


async def aupdate_dataset(
    id: ID, name: str, rath: Optional[MikroNextRath] = None
) -> UpdateDatasetMutationUpdatedataset:
    """UpdateDataset



    Arguments:
        id (ID): id
        name (str): name
        rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

    Returns:
        UpdateDatasetMutationUpdatedataset"""
    return (
        await aexecute(UpdateDatasetMutation, {"id": id, "name": name}, rath=rath)
    ).update_dataset


def update_dataset(
    id: ID, name: str, rath: Optional[MikroNextRath] = None
) -> UpdateDatasetMutationUpdatedataset:
    """UpdateDataset



    Arguments:
        id (ID): id
        name (str): name
        rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

    Returns:
        UpdateDatasetMutationUpdatedataset"""
    return execute(
        UpdateDatasetMutation, {"id": id, "name": name}, rath=rath
    ).update_dataset


async def arevert_dataset(
    dataset: ID, history: ID, rath: Optional[MikroNextRath] = None
) -> RevertDatasetMutationRevertdataset:
    """RevertDataset



    Arguments:
        dataset (ID): dataset
        history (ID): history
        rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

    Returns:
        RevertDatasetMutationRevertdataset"""
    return (
        await aexecute(
            RevertDatasetMutation, {"dataset": dataset, "history": history}, rath=rath
        )
    ).revert_dataset


def revert_dataset(
    dataset: ID, history: ID, rath: Optional[MikroNextRath] = None
) -> RevertDatasetMutationRevertdataset:
    """RevertDataset



    Arguments:
        dataset (ID): dataset
        history (ID): history
        rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

    Returns:
        RevertDatasetMutationRevertdataset"""
    return execute(
        RevertDatasetMutation, {"dataset": dataset, "history": history}, rath=rath
    ).revert_dataset


async def acreate_fluorophore(
    name: str,
    excitation_wavelength: Optional[Micrometers] = None,
    emission_wavelength: Optional[Micrometers] = None,
    rath: Optional[MikroNextRath] = None,
) -> CreateFluorophoreMutationCreatefluorophore:
    """CreateFluorophore



    Arguments:
        name (str): name
        excitation_wavelength (Optional[Micrometers], optional): excitationWavelength.
        emission_wavelength (Optional[Micrometers], optional): emissionWavelength.
        rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

    Returns:
        CreateFluorophoreMutationCreatefluorophore"""
    return (
        await aexecute(
            CreateFluorophoreMutation,
            {
                "name": name,
                "excitationWavelength": excitation_wavelength,
                "emissionWavelength": emission_wavelength,
            },
            rath=rath,
        )
    ).create_fluorophore


def create_fluorophore(
    name: str,
    excitation_wavelength: Optional[Micrometers] = None,
    emission_wavelength: Optional[Micrometers] = None,
    rath: Optional[MikroNextRath] = None,
) -> CreateFluorophoreMutationCreatefluorophore:
    """CreateFluorophore



    Arguments:
        name (str): name
        excitation_wavelength (Optional[Micrometers], optional): excitationWavelength.
        emission_wavelength (Optional[Micrometers], optional): emissionWavelength.
        rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

    Returns:
        CreateFluorophoreMutationCreatefluorophore"""
    return execute(
        CreateFluorophoreMutation,
        {
            "name": name,
            "excitationWavelength": excitation_wavelength,
            "emissionWavelength": emission_wavelength,
        },
        rath=rath,
    ).create_fluorophore


async def aensure_fluorophore(
    name: str,
    excitation_wavelength: Optional[Micrometers] = None,
    emission_wavelength: Optional[Micrometers] = None,
    rath: Optional[MikroNextRath] = None,
) -> EnsureFluorophoreMutationEnsurefluorophore:
    """EnsureFluorophore



    Arguments:
        name (str): name
        excitation_wavelength (Optional[Micrometers], optional): excitationWavelength.
        emission_wavelength (Optional[Micrometers], optional): emissionWavelength.
        rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

    Returns:
        EnsureFluorophoreMutationEnsurefluorophore"""
    return (
        await aexecute(
            EnsureFluorophoreMutation,
            {
                "name": name,
                "excitationWavelength": excitation_wavelength,
                "emissionWavelength": emission_wavelength,
            },
            rath=rath,
        )
    ).ensure_fluorophore


def ensure_fluorophore(
    name: str,
    excitation_wavelength: Optional[Micrometers] = None,
    emission_wavelength: Optional[Micrometers] = None,
    rath: Optional[MikroNextRath] = None,
) -> EnsureFluorophoreMutationEnsurefluorophore:
    """EnsureFluorophore



    Arguments:
        name (str): name
        excitation_wavelength (Optional[Micrometers], optional): excitationWavelength.
        emission_wavelength (Optional[Micrometers], optional): emissionWavelength.
        rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

    Returns:
        EnsureFluorophoreMutationEnsurefluorophore"""
    return execute(
        EnsureFluorophoreMutation,
        {
            "name": name,
            "excitationWavelength": excitation_wavelength,
            "emissionWavelength": emission_wavelength,
        },
        rath=rath,
    ).ensure_fluorophore


async def afrom_array_like(
    array: ArrayLike,
    name: str,
    origins: Optional[List[ID]] = None,
    channel_views: Optional[List[PartialChannelViewInput]] = None,
    transformation_views: Optional[List[PartialAffineTransformationViewInput]] = None,
    label_views: Optional[List[PartialLabelViewInput]] = None,
    rgb_views: Optional[List[PartialRGBViewInput]] = None,
    acquisition_views: Optional[List[PartialAcquisitionViewInput]] = None,
    timepoint_views: Optional[List[PartialTimepointViewInput]] = None,
    optics_views: Optional[List[PartialOpticsViewInput]] = None,
    tags: Optional[List[str]] = None,
    rath: Optional[MikroNextRath] = None,
) -> ImageFragment:
    """from_array_like



    Arguments:
        array (ArrayLike): array
        name (str): name
        origins (Optional[List[ID]], optional): origins.
        channel_views (Optional[List[PartialChannelViewInput]], optional): channelViews.
        transformation_views (Optional[List[PartialAffineTransformationViewInput]], optional): transformationViews.
        label_views (Optional[List[PartialLabelViewInput]], optional): labelViews.
        rgb_views (Optional[List[PartialRGBViewInput]], optional): rgbViews.
        acquisition_views (Optional[List[PartialAcquisitionViewInput]], optional): acquisitionViews.
        timepoint_views (Optional[List[PartialTimepointViewInput]], optional): timepointViews.
        optics_views (Optional[List[PartialOpticsViewInput]], optional): opticsViews.
        tags (Optional[List[str]], optional): tags.
        rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

    Returns:
        ImageFragment"""
    return (
        await aexecute(
            From_array_likeMutation,
            {
                "array": array,
                "name": name,
                "origins": origins,
                "channelViews": channel_views,
                "transformationViews": transformation_views,
                "labelViews": label_views,
                "rgbViews": rgb_views,
                "acquisitionViews": acquisition_views,
                "timepointViews": timepoint_views,
                "opticsViews": optics_views,
                "tags": tags,
            },
            rath=rath,
        )
    ).from_array_like


def from_array_like(
    array: ArrayLike,
    name: str,
    origins: Optional[List[ID]] = None,
    channel_views: Optional[List[PartialChannelViewInput]] = None,
    transformation_views: Optional[List[PartialAffineTransformationViewInput]] = None,
    label_views: Optional[List[PartialLabelViewInput]] = None,
    rgb_views: Optional[List[PartialRGBViewInput]] = None,
    acquisition_views: Optional[List[PartialAcquisitionViewInput]] = None,
    timepoint_views: Optional[List[PartialTimepointViewInput]] = None,
    optics_views: Optional[List[PartialOpticsViewInput]] = None,
    tags: Optional[List[str]] = None,
    rath: Optional[MikroNextRath] = None,
) -> ImageFragment:
    """from_array_like



    Arguments:
        array (ArrayLike): array
        name (str): name
        origins (Optional[List[ID]], optional): origins.
        channel_views (Optional[List[PartialChannelViewInput]], optional): channelViews.
        transformation_views (Optional[List[PartialAffineTransformationViewInput]], optional): transformationViews.
        label_views (Optional[List[PartialLabelViewInput]], optional): labelViews.
        rgb_views (Optional[List[PartialRGBViewInput]], optional): rgbViews.
        acquisition_views (Optional[List[PartialAcquisitionViewInput]], optional): acquisitionViews.
        timepoint_views (Optional[List[PartialTimepointViewInput]], optional): timepointViews.
        optics_views (Optional[List[PartialOpticsViewInput]], optional): opticsViews.
        tags (Optional[List[str]], optional): tags.
        rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

    Returns:
        ImageFragment"""
    return execute(
        From_array_likeMutation,
        {
            "array": array,
            "name": name,
            "origins": origins,
            "channelViews": channel_views,
            "transformationViews": transformation_views,
            "labelViews": label_views,
            "rgbViews": rgb_views,
            "acquisitionViews": acquisition_views,
            "timepointViews": timepoint_views,
            "opticsViews": optics_views,
            "tags": tags,
        },
        rath=rath,
    ).from_array_like


async def arequest_upload(
    key: str, datalayer: str, rath: Optional[MikroNextRath] = None
) -> CredentialsFragment:
    """RequestUpload


     requestUpload: Temporary Credentials for a file upload that can be used by a Client (e.g. in a python datalayer)


    Arguments:
        key (str): key
        datalayer (str): datalayer
        rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

    Returns:
        CredentialsFragment"""
    return (
        await aexecute(
            RequestUploadMutation, {"key": key, "datalayer": datalayer}, rath=rath
        )
    ).request_upload


def request_upload(
    key: str, datalayer: str, rath: Optional[MikroNextRath] = None
) -> CredentialsFragment:
    """RequestUpload


     requestUpload: Temporary Credentials for a file upload that can be used by a Client (e.g. in a python datalayer)


    Arguments:
        key (str): key
        datalayer (str): datalayer
        rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

    Returns:
        CredentialsFragment"""
    return execute(
        RequestUploadMutation, {"key": key, "datalayer": datalayer}, rath=rath
    ).request_upload


async def arequest_access(
    store: ID, duration: Optional[int] = None, rath: Optional[MikroNextRath] = None
) -> AccessCredentialsFragment:
    """RequestAccess


     requestAccess: Temporary Credentials for a file download that can be used by a Client (e.g. in a python datalayer)


    Arguments:
        store (ID): store
        duration (Optional[int], optional): duration.
        rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

    Returns:
        AccessCredentialsFragment"""
    return (
        await aexecute(
            RequestAccessMutation, {"store": store, "duration": duration}, rath=rath
        )
    ).request_access


def request_access(
    store: ID, duration: Optional[int] = None, rath: Optional[MikroNextRath] = None
) -> AccessCredentialsFragment:
    """RequestAccess


     requestAccess: Temporary Credentials for a file download that can be used by a Client (e.g. in a python datalayer)


    Arguments:
        store (ID): store
        duration (Optional[int], optional): duration.
        rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

    Returns:
        AccessCredentialsFragment"""
    return execute(
        RequestAccessMutation, {"store": store, "duration": duration}, rath=rath
    ).request_access


async def acreate_objective(
    serial_number: str,
    name: Optional[str] = None,
    na: Optional[float] = None,
    magnification: Optional[float] = None,
    rath: Optional[MikroNextRath] = None,
) -> CreateObjectiveMutationCreateobjective:
    """CreateObjective



    Arguments:
        serial_number (str): serialNumber
        name (Optional[str], optional): name.
        na (Optional[float], optional): na.
        magnification (Optional[float], optional): magnification.
        rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

    Returns:
        CreateObjectiveMutationCreateobjective"""
    return (
        await aexecute(
            CreateObjectiveMutation,
            {
                "serialNumber": serial_number,
                "name": name,
                "na": na,
                "magnification": magnification,
            },
            rath=rath,
        )
    ).create_objective


def create_objective(
    serial_number: str,
    name: Optional[str] = None,
    na: Optional[float] = None,
    magnification: Optional[float] = None,
    rath: Optional[MikroNextRath] = None,
) -> CreateObjectiveMutationCreateobjective:
    """CreateObjective



    Arguments:
        serial_number (str): serialNumber
        name (Optional[str], optional): name.
        na (Optional[float], optional): na.
        magnification (Optional[float], optional): magnification.
        rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

    Returns:
        CreateObjectiveMutationCreateobjective"""
    return execute(
        CreateObjectiveMutation,
        {
            "serialNumber": serial_number,
            "name": name,
            "na": na,
            "magnification": magnification,
        },
        rath=rath,
    ).create_objective


async def aensure_objective(
    serial_number: str,
    name: Optional[str] = None,
    na: Optional[float] = None,
    magnification: Optional[float] = None,
    rath: Optional[MikroNextRath] = None,
) -> EnsureObjectiveMutationEnsureobjective:
    """EnsureObjective



    Arguments:
        serial_number (str): serialNumber
        name (Optional[str], optional): name.
        na (Optional[float], optional): na.
        magnification (Optional[float], optional): magnification.
        rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

    Returns:
        EnsureObjectiveMutationEnsureobjective"""
    return (
        await aexecute(
            EnsureObjectiveMutation,
            {
                "serialNumber": serial_number,
                "name": name,
                "na": na,
                "magnification": magnification,
            },
            rath=rath,
        )
    ).ensure_objective


def ensure_objective(
    serial_number: str,
    name: Optional[str] = None,
    na: Optional[float] = None,
    magnification: Optional[float] = None,
    rath: Optional[MikroNextRath] = None,
) -> EnsureObjectiveMutationEnsureobjective:
    """EnsureObjective



    Arguments:
        serial_number (str): serialNumber
        name (Optional[str], optional): name.
        na (Optional[float], optional): na.
        magnification (Optional[float], optional): magnification.
        rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

    Returns:
        EnsureObjectiveMutationEnsureobjective"""
    return execute(
        EnsureObjectiveMutation,
        {
            "serialNumber": serial_number,
            "name": name,
            "na": na,
            "magnification": magnification,
        },
        rath=rath,
    ).ensure_objective


async def acreate_camera(
    serial_number: str,
    name: Optional[str] = None,
    pixel_size_x: Optional[Micrometers] = None,
    pixel_size_y: Optional[Micrometers] = None,
    sensor_size_x: Optional[int] = None,
    sensor_size_y: Optional[int] = None,
    rath: Optional[MikroNextRath] = None,
) -> CreateCameraMutationCreatecamera:
    """CreateCamera



    Arguments:
        serial_number (str): serialNumber
        name (Optional[str], optional): name.
        pixel_size_x (Optional[Micrometers], optional): pixelSizeX.
        pixel_size_y (Optional[Micrometers], optional): pixelSizeY.
        sensor_size_x (Optional[int], optional): sensorSizeX.
        sensor_size_y (Optional[int], optional): sensorSizeY.
        rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

    Returns:
        CreateCameraMutationCreatecamera"""
    return (
        await aexecute(
            CreateCameraMutation,
            {
                "serialNumber": serial_number,
                "name": name,
                "pixelSizeX": pixel_size_x,
                "pixelSizeY": pixel_size_y,
                "sensorSizeX": sensor_size_x,
                "sensorSizeY": sensor_size_y,
            },
            rath=rath,
        )
    ).create_camera


def create_camera(
    serial_number: str,
    name: Optional[str] = None,
    pixel_size_x: Optional[Micrometers] = None,
    pixel_size_y: Optional[Micrometers] = None,
    sensor_size_x: Optional[int] = None,
    sensor_size_y: Optional[int] = None,
    rath: Optional[MikroNextRath] = None,
) -> CreateCameraMutationCreatecamera:
    """CreateCamera



    Arguments:
        serial_number (str): serialNumber
        name (Optional[str], optional): name.
        pixel_size_x (Optional[Micrometers], optional): pixelSizeX.
        pixel_size_y (Optional[Micrometers], optional): pixelSizeY.
        sensor_size_x (Optional[int], optional): sensorSizeX.
        sensor_size_y (Optional[int], optional): sensorSizeY.
        rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

    Returns:
        CreateCameraMutationCreatecamera"""
    return execute(
        CreateCameraMutation,
        {
            "serialNumber": serial_number,
            "name": name,
            "pixelSizeX": pixel_size_x,
            "pixelSizeY": pixel_size_y,
            "sensorSizeX": sensor_size_x,
            "sensorSizeY": sensor_size_y,
        },
        rath=rath,
    ).create_camera


async def aensure_camera(
    serial_number: str,
    name: Optional[str] = None,
    pixel_size_x: Optional[Micrometers] = None,
    pixel_size_y: Optional[Micrometers] = None,
    sensor_size_x: Optional[int] = None,
    sensor_size_y: Optional[int] = None,
    rath: Optional[MikroNextRath] = None,
) -> EnsureCameraMutationEnsurecamera:
    """EnsureCamera



    Arguments:
        serial_number (str): serialNumber
        name (Optional[str], optional): name.
        pixel_size_x (Optional[Micrometers], optional): pixelSizeX.
        pixel_size_y (Optional[Micrometers], optional): pixelSizeY.
        sensor_size_x (Optional[int], optional): sensorSizeX.
        sensor_size_y (Optional[int], optional): sensorSizeY.
        rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

    Returns:
        EnsureCameraMutationEnsurecamera"""
    return (
        await aexecute(
            EnsureCameraMutation,
            {
                "serialNumber": serial_number,
                "name": name,
                "pixelSizeX": pixel_size_x,
                "pixelSizeY": pixel_size_y,
                "sensorSizeX": sensor_size_x,
                "sensorSizeY": sensor_size_y,
            },
            rath=rath,
        )
    ).ensure_camera


def ensure_camera(
    serial_number: str,
    name: Optional[str] = None,
    pixel_size_x: Optional[Micrometers] = None,
    pixel_size_y: Optional[Micrometers] = None,
    sensor_size_x: Optional[int] = None,
    sensor_size_y: Optional[int] = None,
    rath: Optional[MikroNextRath] = None,
) -> EnsureCameraMutationEnsurecamera:
    """EnsureCamera



    Arguments:
        serial_number (str): serialNumber
        name (Optional[str], optional): name.
        pixel_size_x (Optional[Micrometers], optional): pixelSizeX.
        pixel_size_y (Optional[Micrometers], optional): pixelSizeY.
        sensor_size_x (Optional[int], optional): sensorSizeX.
        sensor_size_y (Optional[int], optional): sensorSizeY.
        rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

    Returns:
        EnsureCameraMutationEnsurecamera"""
    return execute(
        EnsureCameraMutation,
        {
            "serialNumber": serial_number,
            "name": name,
            "pixelSizeX": pixel_size_x,
            "pixelSizeY": pixel_size_y,
            "sensorSizeX": sensor_size_x,
            "sensorSizeY": sensor_size_y,
        },
        rath=rath,
    ).ensure_camera


async def aget_table(id: ID, rath: Optional[MikroNextRath] = None) -> TableFragment:
    """GetTable



    Arguments:
        id (ID): id
        rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

    Returns:
        TableFragment"""
    return (await aexecute(GetTableQuery, {"id": id}, rath=rath)).table


def get_table(id: ID, rath: Optional[MikroNextRath] = None) -> TableFragment:
    """GetTable



    Arguments:
        id (ID): id
        rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

    Returns:
        TableFragment"""
    return execute(GetTableQuery, {"id": id}, rath=rath).table


async def aget_file(id: ID, rath: Optional[MikroNextRath] = None) -> FileFragment:
    """GetFile



    Arguments:
        id (ID): id
        rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

    Returns:
        FileFragment"""
    return (await aexecute(GetFileQuery, {"id": id}, rath=rath)).file


def get_file(id: ID, rath: Optional[MikroNextRath] = None) -> FileFragment:
    """GetFile



    Arguments:
        id (ID): id
        rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

    Returns:
        FileFragment"""
    return execute(GetFileQuery, {"id": id}, rath=rath).file


async def aget_instrument(
    id: ID, rath: Optional[MikroNextRath] = None
) -> InstrumentFragment:
    """GetInstrument



    Arguments:
        id (ID): id
        rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

    Returns:
        InstrumentFragment"""
    return (await aexecute(GetInstrumentQuery, {"id": id}, rath=rath)).instrument


def get_instrument(id: ID, rath: Optional[MikroNextRath] = None) -> InstrumentFragment:
    """GetInstrument



    Arguments:
        id (ID): id
        rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

    Returns:
        InstrumentFragment"""
    return execute(GetInstrumentQuery, {"id": id}, rath=rath).instrument


async def aget_snapshot(
    id: ID, rath: Optional[MikroNextRath] = None
) -> SnapshotFragment:
    """GetSnapshot



    Arguments:
        id (ID): id
        rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

    Returns:
        SnapshotFragment"""
    return (await aexecute(GetSnapshotQuery, {"id": id}, rath=rath)).snapshot


def get_snapshot(id: ID, rath: Optional[MikroNextRath] = None) -> SnapshotFragment:
    """GetSnapshot



    Arguments:
        id (ID): id
        rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

    Returns:
        SnapshotFragment"""
    return execute(GetSnapshotQuery, {"id": id}, rath=rath).snapshot


async def asearch_snapshots(
    search: Optional[str] = None,
    values: Optional[List[ID]] = None,
    rath: Optional[MikroNextRath] = None,
) -> List[SearchSnapshotsQueryOptions]:
    """SearchSnapshots



    Arguments:
        search (Optional[str], optional): search.
        values (Optional[List[ID]], optional): values.
        rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

    Returns:
        List[SearchSnapshotsQuerySnapshots]"""
    return (
        await aexecute(
            SearchSnapshotsQuery, {"search": search, "values": values}, rath=rath
        )
    ).options


def search_snapshots(
    search: Optional[str] = None,
    values: Optional[List[ID]] = None,
    rath: Optional[MikroNextRath] = None,
) -> List[SearchSnapshotsQueryOptions]:
    """SearchSnapshots



    Arguments:
        search (Optional[str], optional): search.
        values (Optional[List[ID]], optional): values.
        rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

    Returns:
        List[SearchSnapshotsQuerySnapshots]"""
    return execute(
        SearchSnapshotsQuery, {"search": search, "values": values}, rath=rath
    ).options


async def aget_dataset(id: ID, rath: Optional[MikroNextRath] = None) -> DatasetFragment:
    """GetDataset



    Arguments:
        id (ID): id
        rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

    Returns:
        DatasetFragment"""
    return (await aexecute(GetDatasetQuery, {"id": id}, rath=rath)).dataset


def get_dataset(id: ID, rath: Optional[MikroNextRath] = None) -> DatasetFragment:
    """GetDataset



    Arguments:
        id (ID): id
        rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

    Returns:
        DatasetFragment"""
    return execute(GetDatasetQuery, {"id": id}, rath=rath).dataset


async def aimages(rath: Optional[MikroNextRath] = None) -> List[ImagesQueryImages]:
    """Images



    Arguments:
        rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

    Returns:
        List[ImagesQueryImages]"""
    return (await aexecute(ImagesQuery, {}, rath=rath)).images


def images(rath: Optional[MikroNextRath] = None) -> List[ImagesQueryImages]:
    """Images



    Arguments:
        rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

    Returns:
        List[ImagesQueryImages]"""
    return execute(ImagesQuery, {}, rath=rath).images


async def aget_image(id: ID, rath: Optional[MikroNextRath] = None) -> ImageFragment:
    """GetImage



    Arguments:
        id (ID): id
        rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

    Returns:
        ImageFragment"""
    return (await aexecute(GetImageQuery, {"id": id}, rath=rath)).image


def get_image(id: ID, rath: Optional[MikroNextRath] = None) -> ImageFragment:
    """GetImage



    Arguments:
        id (ID): id
        rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

    Returns:
        ImageFragment"""
    return execute(GetImageQuery, {"id": id}, rath=rath).image


async def aget_random_image(rath: Optional[MikroNextRath] = None) -> ImageFragment:
    """GetRandomImage



    Arguments:
        rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

    Returns:
        ImageFragment"""
    return (await aexecute(GetRandomImageQuery, {}, rath=rath)).random_image


def get_random_image(rath: Optional[MikroNextRath] = None) -> ImageFragment:
    """GetRandomImage



    Arguments:
        rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

    Returns:
        ImageFragment"""
    return execute(GetRandomImageQuery, {}, rath=rath).random_image


async def asearch_images(
    search: Optional[str] = None,
    values: Optional[List[ID]] = None,
    rath: Optional[MikroNextRath] = None,
) -> List[SearchImagesQueryOptions]:
    """SearchImages



    Arguments:
        search (Optional[str], optional): search.
        values (Optional[List[ID]], optional): values.
        rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

    Returns:
        List[SearchImagesQueryImages]"""
    return (
        await aexecute(
            SearchImagesQuery, {"search": search, "values": values}, rath=rath
        )
    ).options


def search_images(
    search: Optional[str] = None,
    values: Optional[List[ID]] = None,
    rath: Optional[MikroNextRath] = None,
) -> List[SearchImagesQueryOptions]:
    """SearchImages



    Arguments:
        search (Optional[str], optional): search.
        values (Optional[List[ID]], optional): values.
        rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

    Returns:
        List[SearchImagesQueryImages]"""
    return execute(
        SearchImagesQuery, {"search": search, "values": values}, rath=rath
    ).options


async def aget_objective(
    id: ID, rath: Optional[MikroNextRath] = None
) -> ObjectiveFragment:
    """GetObjective



    Arguments:
        id (ID): id
        rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

    Returns:
        ObjectiveFragment"""
    return (await aexecute(GetObjectiveQuery, {"id": id}, rath=rath)).objective


def get_objective(id: ID, rath: Optional[MikroNextRath] = None) -> ObjectiveFragment:
    """GetObjective



    Arguments:
        id (ID): id
        rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

    Returns:
        ObjectiveFragment"""
    return execute(GetObjectiveQuery, {"id": id}, rath=rath).objective


async def aget_camera(id: ID, rath: Optional[MikroNextRath] = None) -> CameraFragment:
    """GetCamera



    Arguments:
        id (ID): id
        rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

    Returns:
        CameraFragment"""
    return (await aexecute(GetCameraQuery, {"id": id}, rath=rath)).camera


def get_camera(id: ID, rath: Optional[MikroNextRath] = None) -> CameraFragment:
    """GetCamera



    Arguments:
        id (ID): id
        rath (mikro_next.rath.MikroNextRath, optional): The mikro rath client

    Returns:
        CameraFragment"""
    return execute(GetCameraQuery, {"id": id}, rath=rath).camera


ChannelViewFragment.update_forward_refs()
FileFragment.update_forward_refs()
LabelViewFragment.update_forward_refs()
TableFragment.update_forward_refs()
TimepointViewFragment.update_forward_refs()
