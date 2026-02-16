from typing import get_origin, get_args, Union, Any, Annotated
from fastapi import Request, HTTPException
from pydantic import BaseModel, ValidationError, ConfigDict
import json, types


def _unwrap_annotation(annotation):
    origin = get_origin(annotation)
    if origin is Annotated:
        return _unwrap_annotation(get_args(annotation)[0])
    if origin is Union or origin is types.UnionType:
        args = [a for a in get_args(annotation) if a is not type(None)]
        return _unwrap_annotation(args[0]) if args else annotation
    return annotation


def _is_list_annotation(annotation) -> bool:
    unwrapped = _unwrap_annotation(annotation)
    return get_origin(unwrapped) is list


def _is_dict_annotation(annotation) -> bool:
    unwrapped = _unwrap_annotation(annotation)
    return get_origin(unwrapped) is dict


class BaseValidator(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    @classmethod
    async def validate(cls, request: Request) -> Any:
        try:
            data: dict[str, Any] = {}

            # ======================
            # Query parameters
            # ======================
            for key in request.query_params.keys():
                values = request.query_params.getlist(key)
                field = cls.model_fields.get(key)

                # LIST FIELD
                if field and _is_list_annotation(field.annotation):
                    data[key] = values
                    continue

                single_value = values if len(values) > 1 else values[0]

                # ✅ DICT FIELD (JSON in query param)
                if field and _is_dict_annotation(field.annotation):
                    if isinstance(single_value, str):
                        try:
                            single_value = json.loads(single_value)
                        except json.JSONDecodeError:
                            raise HTTPException(
                                status_code=422,
                                detail=f"Invalid JSON for field '{key}'"
                            )

                data[key] = single_value

            # ======================
            # Request body
            # ======================
            if request.method != "GET":
                content_type = request.headers.get("content-type", "")

                if content_type.startswith("application/json"):
                    body_data = await request.json()

                elif content_type.startswith(
                    ("application/x-www-form-urlencoded", "multipart/form-data")
                ):
                    form = await request.form()
                    body_data = {}

                    for key in form.keys():
                        values = form.getlist(key)
                        field = cls.model_fields.get(key)

                        if field and _is_list_annotation(field.annotation):
                            body_data[key] = values
                            continue

                        single_value = values if len(values) > 1 else values[0]

                        if field and _is_dict_annotation(field.annotation):
                            if isinstance(single_value, str):
                                try:
                                    single_value = json.loads(single_value)
                                except json.JSONDecodeError:
                                    raise HTTPException(
                                        status_code=422,
                                        detail=f"Invalid JSON for field '{key}'"
                                    )

                        body_data[key] = single_value

                else:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Unsupported content type: {content_type or 'no body found'}"
                    )

                data.update(body_data)

            # ======================
            # Final list normalization
            # ======================
            for name, field in cls.model_fields.items():
                if name in data and _is_list_annotation(field.annotation):
                    if not isinstance(data[name], list):
                        data[name] = [data[name]]

            # ======================
            # Create model
            # ======================
            return cls(**data)

        except ValidationError as error:
            raise HTTPException(
                status_code=422,
                detail=error.errors()
            ) from error
