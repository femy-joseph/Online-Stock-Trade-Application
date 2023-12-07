from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class LookupRequest(_message.Message):
    __slots__ = ["name"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class TradeReply(_message.Message):
    __slots__ = ["message"]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: int
    def __init__(self, message: _Optional[int] = ...) -> None: ...

class TradeRequest(_message.Message):
    __slots__ = ["add_remove", "name", "type"]
    ADD_REMOVE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    add_remove: int
    name: str
    type: str
    def __init__(self, name: _Optional[str] = ..., add_remove: _Optional[int] = ..., type: _Optional[str] = ...) -> None: ...

class UpdateReply(_message.Message):
    __slots__ = ["message"]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: int
    def __init__(self, message: _Optional[int] = ...) -> None: ...

class UpdateRequest(_message.Message):
    __slots__ = ["name", "price"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    PRICE_FIELD_NUMBER: _ClassVar[int]
    name: str
    price: int
    def __init__(self, name: _Optional[str] = ..., price: _Optional[int] = ...) -> None: ...

class lookupReply(_message.Message):
    __slots__ = ["price", "volume"]
    PRICE_FIELD_NUMBER: _ClassVar[int]
    VOLUME_FIELD_NUMBER: _ClassVar[int]
    price: float
    volume: int
    def __init__(self, price: _Optional[float] = ..., volume: _Optional[int] = ...) -> None: ...
