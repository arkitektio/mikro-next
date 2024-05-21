"""Strucutre Registration

This module is autoimported by arkitekt. It registers the default structure types with the arkitekt
structure-registry so that they can be used in the arkitekt app without having to import them.

You can of course overwrite this in your app if you need to expand to a more complex query.

"""

import logging

logger = logging.getLogger(__name__)


rekuest = None

try:
    import rekuest_next
except ImportError:
    pass
    rekuest = rekuest_next
    structure_reg = None

# Check if rekuest is installed
# If it is, register the structures with the default structure registry
if True:
    from rekuest_next.structures.default import (
        get_default_structure_registry,
        PortScope,
        id_shrink,
    )
    from rekuest_next.widgets import SearchWidget
    from mikro_next.api.schema import (
        ImageFragment,
        aget_image,
        SearchImagesQuery,
        DatasetFragment,
        aget_dataset,
    )
    from mikro_next.api.schema import (
        SnapshotFragment,
        aget_snapshot,
        SearchSnapshotsQuery,
    )

    structure_reg = get_default_structure_registry()
    structure_reg.register_as_structure(
        ImageFragment,
        identifier="@mikro/image",
        aexpand=aget_image,
        ashrink=id_shrink,
        scope=PortScope.GLOBAL,
        default_widget=SearchWidget(
            query=SearchImagesQuery.Meta.document, ward="mikro"
        ),
    )
    structure_reg.register_as_structure(
        SnapshotFragment,
        identifier="@mikro/snapshot",
        aexpand=aget_snapshot,
        ashrink=id_shrink,
        scope=PortScope.GLOBAL,
        default_widget=SearchWidget(
            query=SearchSnapshotsQuery.Meta.document, ward="mikro"
        ),
    )
    structure_reg.register_as_structure(
        DatasetFragment,
        identifier="@mikro/dataset",
        aexpand=aget_dataset,
        ashrink=id_shrink,
        scope=PortScope.GLOBAL,
        default_widget=SearchWidget(
            query=SearchImagesQuery.Meta.document, ward="mikro"
        ),
    )
