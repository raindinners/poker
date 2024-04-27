from __future__ import annotations

from schemas import ApplicationSchema, Event


def update_event(event: Event, class_type: ApplicationSchema) -> Event:
    event.request = class_type.model_validate(event.request)

    return event
