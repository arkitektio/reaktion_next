from typing import Awaitable, Callable, Dict
from rekuest.messages import Assignation
from fluss_next.api.schema import (
    RekuestFilterNodeFragment,
    RekuestMapNodeFragment,
    GraphNodeFragmentBaseRekuestFilterNode,
    GraphNodeFragmentBaseRekuestMapNode,
    ReactiveNodeFragment,
    BaseGraphNodeFragmentBase,
    MapStrategy,
    ReactiveImplementation,
    NodeKind,
)
import asyncio
from reaktion_next.atoms.arkitekt import (
    ArkitektMapAtom,
    ArkitektMergeMapAtom,
    ArkitektAsCompletedAtom,
    ArkitektOrderedAtom,
)
from reaktion_next.atoms.arkitekt_filter import ArkitektFilterAtom
from reaktion_next.atoms.transformation.chunk import ChunkAtom
from reaktion_next.atoms.transformation.buffer_complete import BufferCompleteAtom
from reaktion_next.atoms.transformation.split import SplitAtom
from reaktion_next.atoms.combination.zip import ZipAtom
from reaktion_next.atoms.transformation.filter import FilterAtom
from reaktion_next.atoms.combination.withlatest import WithLatestAtom
from reaktion_next.atoms.combination.gate import GateAtom
from reaktion_next.atoms.filter.all import AllAtom
from rekuest.postmans.utils import RPCContract
from .base import Atom
from .transport import AtomTransport
from rekuest.actors.types import Assignment
from typing import Any, Optional
from reaktion_next.atoms.operations.math import MathAtom, operation_map


def atomify(
    node: BaseGraphNodeFragmentBase,
    transport: AtomTransport,
    contract: Optional[RPCContract],
    globals: Dict[str, Any],
    assignment: Assignment,
    alog: Callable[[Assignation, str, str], Awaitable[None]] = None,
) -> Atom:
    if isinstance(node, RekuestMapNodeFragment):
        if node.node_kind == NodeKind.FUNCTION:
            if node.map_strategy == MapStrategy.MAP:
                return ArkitektMapAtom(
                    node=node,
                    contract=contract,
                    transport=transport,
                    assignment=assignment,
                    globals=globals,
                    alog=alog,
                )
            if node.map_strategy == MapStrategy.AS_COMPLETED:
                return ArkitektAsCompletedAtom(
                    node=node,
                    contract=contract,
                    transport=transport,
                    assignment=assignment,
                    globals=globals,
                    alog=alog,
                )
            if node.map_strategy == MapStrategy.ORDERED:
                return ArkitektAsCompletedAtom(
                    node=node,
                    contract=contract,
                    transport=transport,
                    assignment=assignment,
                    globals=globals,
                    alog=alog,
                )

            raise NotImplementedError(
                f"Map strategy {node.map_strategy} is not implemented"
            )
        if node.node_kind == NodeKind.GENERATOR:
            return ArkitektMergeMapAtom(
                node=node,
                contract=contract,
                transport=transport,
                assignment=assignment,
                globals=globals,
                alog=alog,
            )

        raise NotImplementedError(f"Node kind {node.kind} is not implemented")
    if isinstance(node, RekuestFilterNodeFragment):
        if node.node_kind == NodeKind.FUNCTION:
            if node.map_strategy == MapStrategy.MAP:
                return ArkitektFilterAtom(
                    node=node,
                    contract=contract,
                    transport=transport,
                    assignment=assignment,
                    globals=globals,
                    alog=alog,
                )
        if node.node_kind == NodeKind.GENERATOR:
            raise NotImplementedError("Generator cannot be used as a filter")

    if isinstance(node, ReactiveNodeFragment):
        if node.implementation == ReactiveImplementation.ZIP:
            return ZipAtom(
                node=node,
                transport=transport,
                assignment=assignment,
                globals=globals,
                alog=alog,
            )
        if node.implementation == ReactiveImplementation.FILTER:
            return FilterAtom(
                node=node,
                transport=transport,
                assignment=assignment,
                globals=globals,
                alog=alog,
            )
        if node.implementation == ReactiveImplementation.CHUNK:
            return ChunkAtom(
                node=node,
                transport=transport,
                assignment=assignment,
                globals=globals,
                alog=alog,
            )
        if node.implementation == ReactiveImplementation.GATE:
            return GateAtom(
                node=node,
                transport=transport,
                assignment=assignment,
                globals=globals,
                alog=alog,
            )
        if node.implementation == ReactiveImplementation.BUFFER_COMPLETE:
            return BufferCompleteAtom(
                node=node,
                transport=transport,
                assignment=assignment,
                globals=globals,
                alog=alog,
            )
        if node.implementation == ReactiveImplementation.WITHLATEST:
            return WithLatestAtom(
                node=node,
                transport=transport,
                assignment=assignment,
                globals=globals,
                alog=alog,
            )
        if node.implementation == ReactiveImplementation.COMBINELATEST:
            return WithLatestAtom(
                node=node,
                transport=transport,
                assignment=assignment,
                globals=globals,
                alog=alog,
            )
        if node.implementation == ReactiveImplementation.SPLIT:
            return SplitAtom(
                node=node,
                transport=transport,
                assignment=assignment,
                globals=globals,
                alog=alog,
            )
        if node.implementation == ReactiveImplementation.ALL:
            return AllAtom(
                node=node,
                transport=transport,
                assignment=assignment,
                globals=globals,
                alog=alog,
            )
        if node.implementation in operation_map:
            return MathAtom(
                node=node,
                transport=transport,
                assignment=assignment,
                globals=globals,
                alog=alog,
            )

    raise NotImplementedError(f"Atom for {node} {type(node)} is not implemented")
