from mikro_next.api.schema import EntityRelation


def register_structures(structure_reg):
    from rekuest_next.structures.default import (
        PortScope,
        id_shrink,
    )
    from rekuest_next.widgets import SearchWidget
    from mikro_next.api.schema import (
        Image,
        aget_image,
        SearchImagesQuery,
        Dataset,
        Stage,
        aget_stage,
        File,
        aget_file,
        SearchStagesQuery,
        SearchFilesQuery,
        ProtocolStep,
        aget_protocol_step,
        SearchProtocolStepsQuery,
        aget_rgb_context,
        RGBContext,
        aget_dataset,
    )
    from mikro_next.api.schema import (
        Snapshot,
        aget_snapshot,
        SearchSnapshotsQuery,
        Ontology,
        aget_ontology,
        Entity,
        EntityRelationKind,
        aget_entity,
        SearchOntologiesQuery,
        SearchEntitiesQuery,
        EntityKind,
        aget_entity_kind,
        aget_rendered_plot,
        aget_entity_relation_kind,
        SearchEntityRelationKindsQuery,
        RenderedPlot,
        Protocol,
        aget_protocol,
        Specimen,
        aget_specimen,
        SearchSpecimensQuery,
        SearchProtocolsQuery,
        SearchRenderedPlotsQuery,
        SearchEntityKindQuery,
    )

    structure_reg.register_as_structure(
        Image,
        identifier="@mikro/image",
        aexpand=aget_image,
        ashrink=id_shrink,
        scope=PortScope.GLOBAL,
        default_widget=SearchWidget(
            query=SearchImagesQuery.Meta.document, ward="mikro"
        ),
    )
    structure_reg.register_as_structure(
        Snapshot,
        identifier="@mikro/snapshot",
        aexpand=aget_snapshot,
        ashrink=id_shrink,
        scope=PortScope.GLOBAL,
        default_widget=SearchWidget(
            query=SearchSnapshotsQuery.Meta.document, ward="mikro"
        ),
    )
    structure_reg.register_as_structure(
        Specimen,
        identifier="@mikro/specimen",
        aexpand=aget_specimen,
        ashrink=id_shrink,
        scope=PortScope.GLOBAL,
        default_widget=SearchWidget(
            query=SearchSpecimensQuery.Meta.document, ward="mikro"
        ),
    )
    structure_reg.register_as_structure(
        Stage,
        identifier="@mikro/stage",
        aexpand=aget_stage,
        ashrink=id_shrink,
        scope=PortScope.GLOBAL,
        default_widget=SearchWidget(
            query=SearchStagesQuery.Meta.document, ward="mikro"
        ),
    )
    structure_reg.register_as_structure(
        Dataset,
        identifier="@mikro/dataset",
        aexpand=aget_dataset,
        ashrink=id_shrink,
        scope=PortScope.GLOBAL,
        default_widget=SearchWidget(
            query=SearchImagesQuery.Meta.document, ward="mikro"
        ),
    )
    structure_reg.register_as_structure(
        File,
        identifier="@mikro/file",
        aexpand=aget_file,
        ashrink=id_shrink,
        scope=PortScope.GLOBAL,
        default_widget=SearchWidget(query=SearchFilesQuery.Meta.document, ward="mikro"),
    )
    structure_reg.register_as_structure(
        RGBContext,
        identifier="@mikro/rbgcontext",
        aexpand=aget_rgb_context,
        ashrink=id_shrink,
        scope=PortScope.GLOBAL,
    )

    structure_reg.register_as_structure(
        Ontology,
        identifier="@mikro/ontology",
        aexpand=aget_ontology,
        ashrink=id_shrink,
        scope=PortScope.GLOBAL,
        default_widget=SearchWidget(
            query=SearchOntologiesQuery.Meta.document, ward="mikro"
        ),
    )
    structure_reg.register_as_structure(
        RenderedPlot,
        identifier="@mikro/renderedplot",
        aexpand=aget_rendered_plot,
        ashrink=id_shrink,
        scope=PortScope.GLOBAL,
        default_widget=SearchWidget(
            query=SearchRenderedPlotsQuery.Meta.document, ward="mikro"
        ),
    )

    structure_reg.register_as_structure(
        Entity,
        identifier="@mikro/entity",
        aexpand=aget_entity,
        ashrink=id_shrink,
        scope=PortScope.GLOBAL,
        default_widget=SearchWidget(
            query=SearchEntitiesQuery.Meta.document, ward="mikro"
        ),
    )

    structure_reg.register_as_structure(
        EntityKind,
        identifier="@mikro/entity_kind",
        aexpand=aget_entity_kind,
        ashrink=id_shrink,
        scope=PortScope.GLOBAL,
        default_widget=SearchWidget(
            query=SearchEntityKindQuery.Meta.document, ward="mikro"
        ),
    )

    structure_reg.register_as_structure(
        EntityRelationKind,
        identifier="@mikro/entity_relation_kind",
        aexpand=aget_entity_relation_kind,
        ashrink=id_shrink,
        scope=PortScope.GLOBAL,
        default_widget=SearchWidget(
            query=SearchEntityRelationKindsQuery.Meta.document, ward="mikro"
        ),
    )

    structure_reg.register_as_structure(
        EntityRelation,
        identifier="@mikro/entity_relation",
        aexpand=aget_entity_kind,
        ashrink=id_shrink,
        scope=PortScope.GLOBAL,
        default_widget=SearchWidget(
            query=SearchEntityKindQuery.Meta.document, ward="mikro"
        ),
    )

    structure_reg.register_as_structure(
        Protocol,
        identifier="@mikro/protocol",
        aexpand=aget_protocol,
        ashrink=id_shrink,
        scope=PortScope.GLOBAL,
        default_widget=SearchWidget(
            query=SearchProtocolsQuery.Meta.document, ward="mikro"
        ),
    )

    structure_reg.register_as_structure(
        ProtocolStep,
        identifier="@mikro/protocolstep",
        aexpand=aget_protocol_step,
        ashrink=id_shrink,
        scope=PortScope.GLOBAL,
        default_widget=SearchWidget(
            query=SearchProtocolStepsQuery.Meta.document, ward="mikro"
        ),
    )


