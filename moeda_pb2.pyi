from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ConverterRequest(_message.Message):
    __slots__ = ("moedaOrigem", "valorOrigem", "moedaDestino")
    MOEDAORIGEM_FIELD_NUMBER: _ClassVar[int]
    VALORORIGEM_FIELD_NUMBER: _ClassVar[int]
    MOEDADESTINO_FIELD_NUMBER: _ClassVar[int]
    moedaOrigem: str
    valorOrigem: float
    moedaDestino: str
    def __init__(self, moedaOrigem: _Optional[str] = ..., valorOrigem: _Optional[float] = ..., moedaDestino: _Optional[str] = ...) -> None: ...

class ConverterReply(_message.Message):
    __slots__ = ("valorOrigem", "valorDestino")
    VALORORIGEM_FIELD_NUMBER: _ClassVar[int]
    VALORDESTINO_FIELD_NUMBER: _ClassVar[int]
    valorOrigem: float
    valorDestino: float
    def __init__(self, valorOrigem: _Optional[float] = ..., valorDestino: _Optional[float] = ...) -> None: ...
