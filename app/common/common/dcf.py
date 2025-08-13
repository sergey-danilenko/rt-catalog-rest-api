from __future__ import annotations as _annotations

import sys
import typing
from dataclasses import fields, dataclass, MISSING, is_dataclass
from enum import Enum, EnumType
from types import UnionType, GetSetDescriptorType, NoneType
from typing import Any, Type, Dict, Union

from typing_extensions import NewType


def _is_dataclass_instance(obj) -> bool:
    try:
        return is_dataclass(obj)
    except AttributeError:
        return False


def _is_enum_subclass(obj) -> bool:
    return issubclass(obj, Enum)


def _process_union_field(actual_types, value):
    for possible_type in actual_types:
        if possible_type is not None:
            try:
                return _get_value(possible_type, value)
            except AttributeError:
                return _value_from_type(possible_type, value)


def add_module_globals(obj: Any, globalns: dict[str, Any] | None = None) -> \
dict[str, Any]:
    module_name = getattr(obj, '__module__', None)
    if module_name:
        try:
            module_globalns = sys.modules[module_name].__dict__
        except KeyError:
            pass
        else:
            if globalns:
                return {**module_globalns, **globalns}
            else:
                return module_globalns.copy()

    return globalns or {}


def get_cls_types_namespace(
    cls: type[Any], parent_namespace: dict[str, Any] | None = None
) -> dict[str, Any]:
    ns = add_module_globals(cls, parent_namespace)
    ns[cls.__name__] = cls
    return ns


def _make_forward_ref(
    arg: Any,
    is_argument: bool = True,
    *,
    is_class: bool = False,
) -> typing.ForwardRef:
    return typing.ForwardRef(arg, is_argument)


def eval_type_lenient(value: Any, globalns: dict[str, Any] | None,
                      localns: dict[str, Any] | None) -> Any:
    if value is None:
        value = NoneType
    elif isinstance(value, str):
        value = _make_forward_ref(value, is_argument=False, is_class=True)
    try:
        return typing._eval_type(value, globalns, localns)  # type: ignore
    except NameError:
        return value


def get_cls_type_hints_lenient(obj: Any,
                               globalns: dict[str, Any] | None = None) -> dict[
    str, Any]:
    hints = {}
    for base in reversed(obj.__mro__):
        ann = base.__dict__.get('__annotations__')
        localns = dict(vars(base))
        if ann is not None and ann is not GetSetDescriptorType:
            for name, value in ann.items():
                val = eval_type_lenient(value, globalns, localns)
                hints[name] = val
    return hints


def is_forward_ref(ann_type: type[Any]) -> bool:
    if ann_type.__class__ == typing.ForwardRef:
        return True
    return False


def _value_from_type(obj, value):
    if _is_dataclass_instance(obj) and isinstance(value, dict):
        value = _make_dataclass(obj, value)
    else:
        value = obj(value)
    return value


def _get_enum_value(enum_type: EnumType, value) -> Enum:
    if isinstance(value, dict):
        value = tuple(value.values())[0]
    base, *args = enum_type.__bases__
    if not isinstance(base, EnumType) and base != type(value):
        try:
            value = base(value)
        except ValueError:
            pass
    try:
        return enum_type[value]
    except KeyError:
        try:
            return enum_type(value)
        except ValueError:
            return value


def _get_value(field_type, value):
    if value is not None:
        if _type := typing.get_origin(field_type):
            if _type in (UnionType, Union):
                value = _process_union_field(typing.get_args(field_type), value)
            elif issubclass(_type, list):
                if isinstance(value, type) and issubclass(value, list):
                    value = value()
                else:
                    value = _from_dict(field_type, value)
        elif isinstance(field_type, NewType):
            value = value
        elif is_forward_ref(field_type):
            value = value
        elif _is_enum_subclass(field_type) and value is not None:
            value = _get_enum_value(enum_type=field_type, value=value)
        else:
            value = _value_from_type(field_type, value)
    return value


def _make_dataclass(cls: Type[dataclass], data: Dict[str, Any]) -> dataclass:
    instance = cls.__new__(cls)

    types_namespace = get_cls_types_namespace(cls)
    type_hints = get_cls_type_hints_lenient(cls, types_namespace)

    try:
        for attr in fields(cls):
            value = data.get(attr.name, None)
            field_type = type_hints[attr.name]
            if value is None:
                if attr.default != MISSING:
                    value = attr.default
                elif attr.default_factory != MISSING:
                    value = attr.default_factory
            value = _get_value(field_type, value)

            setattr(instance, attr.name, value)

        post_init_method = getattr(instance, "__post_init__", None)
        if callable(post_init_method):
            post_init_method()
        return instance
    except TypeError as e:
        raise ValueError(f"Could not convert dictionary to dataclass") from e


def _from_dict(
    cls: Type[dataclass] | list | list[Type[dataclass]] | Enum | bool,
    data: Any,
) -> Union[dataclass, list[dataclass]]:
    if _is_dataclass_instance(cls):
        return _make_dataclass(cls, data)
    elif _is_enum_subclass(cls):
        return _get_enum_value(enum_type=cls, value=data)
    else:
        obj = cls()
        if isinstance(obj, list):
            if not isinstance(data, list):
                raise TypeError("value of data must be of type list")
            if typing.get_origin(cls):
                _obj = typing.get_args(cls)[0]
                if _is_dataclass_instance(_obj):
                    for obj_data in data:
                        new_obj = _make_dataclass(_obj, obj_data)
                        obj.append(new_obj)
                elif _is_enum_subclass(_obj):
                    for obj_data in data:
                        value = _get_enum_value(enum_type=_obj, value=obj_data)
                        obj.append(value)
                else:
                    if data is not None:
                        obj += data
            else:
                if data is not None:
                    obj += data
            return obj
        elif isinstance(obj, dict):
            _data = {}
            if typing.get_origin(cls):
                k_obj, v_obj = typing.get_args(cls)
                if isinstance(data, dict):
                    for k, v in data.items():
                        key = _from_dict(k_obj, k)
                        value = _from_dict(v_obj, v)
                        _data[key] = value
            else:
                if data is not None:
                    _data.update(**data)
            return _data
        elif isinstance(obj, bool):
            if data is not None:
                return data


def make_dataclass(
    cls: Type[dataclass] | list | list[Type[dataclass]] | Enum | bool,
    data: list | Dict[str, Any] | bool,
) -> Union[dataclass, list[dataclass]] | None:
    if data is None:
        return None
    return _from_dict(cls, data)


def _find_property_attr(obj: dataclass) -> list[str]:
    property_attrs = []
    cls = obj.__class__
    for attr_name in dir(cls):
        if attr_name.startswith("__"):
            continue
        attr = getattr(cls, attr_name)
        if isinstance(attr, property):
            property_attrs.append(attr_name)
    return property_attrs


def to_dict(obj: dataclass, with_property: bool = False) -> dict[str, Any]:
    result = {}
    for key, value in obj.__dict__.items():
        if _is_dataclass_instance(value):
            result[key] = to_dict(value, with_property)
        elif isinstance(value, list):
            lst = []
            for v in value:
                if not _is_dataclass_instance(v):
                    lst.append(v)
                else:
                    lst.append(to_dict(v, with_property))
            result[key] = lst
        else:
            result[key] = value
    if with_property:
        for key in _find_property_attr(obj):
            result[key] = getattr(obj, key)
    return result
