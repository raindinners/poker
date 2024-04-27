from __future__ import annotations

from typing import Any, Dict, List, Literal, Optional, Sequence, Union


def model_rebuild(__all__: Sequence[str], __globals__: Dict[str, Any]) -> None:
    for _entity_name in __all__:
        _entity = __globals__[_entity_name]
        if not hasattr(_entity, "model_rebuild"):
            continue

        _entity.model_rebuild(
            _types_namespace={
                "List": List,
                "Optional": Optional,
                "Union": Union,
                "Literal": Literal,
                **{k: v for k, v in __globals__.items() if k in __all__},
            }
        )
