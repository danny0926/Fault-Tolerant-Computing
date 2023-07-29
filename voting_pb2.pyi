from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AuthRequest(_message.Message):
    __slots__ = ["name", "response"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    name: VoterName
    response: Response
    def __init__(self, name: _Optional[_Union[VoterName, _Mapping]] = ..., response: _Optional[_Union[Response, _Mapping]] = ...) -> None: ...

class AuthToken(_message.Message):
    __slots__ = ["value"]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    value: bytes
    def __init__(self, value: _Optional[bytes] = ...) -> None: ...

class Challenge(_message.Message):
    __slots__ = ["value"]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    value: bytes
    def __init__(self, value: _Optional[bytes] = ...) -> None: ...

class Election(_message.Message):
    __slots__ = ["choices", "end_date", "groups", "name", "token"]
    CHOICES_FIELD_NUMBER: _ClassVar[int]
    END_DATE_FIELD_NUMBER: _ClassVar[int]
    GROUPS_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    choices: _containers.RepeatedScalarFieldContainer[str]
    end_date: _timestamp_pb2.Timestamp
    groups: _containers.RepeatedScalarFieldContainer[str]
    name: str
    token: AuthToken
    def __init__(self, name: _Optional[str] = ..., groups: _Optional[_Iterable[str]] = ..., choices: _Optional[_Iterable[str]] = ..., end_date: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., token: _Optional[_Union[AuthToken, _Mapping]] = ...) -> None: ...

class ElectionName(_message.Message):
    __slots__ = ["name"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class ElectionResult(_message.Message):
    __slots__ = ["counts", "status"]
    COUNTS_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    counts: _containers.RepeatedCompositeFieldContainer[VoteCount]
    status: int
    def __init__(self, status: _Optional[int] = ..., counts: _Optional[_Iterable[_Union[VoteCount, _Mapping]]] = ...) -> None: ...

class Response(_message.Message):
    __slots__ = ["value"]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    value: bytes
    def __init__(self, value: _Optional[bytes] = ...) -> None: ...

class Status(_message.Message):
    __slots__ = ["code"]
    CODE_FIELD_NUMBER: _ClassVar[int]
    code: int
    def __init__(self, code: _Optional[int] = ...) -> None: ...

class Vote(_message.Message):
    __slots__ = ["choice_name", "election_name", "token"]
    CHOICE_NAME_FIELD_NUMBER: _ClassVar[int]
    ELECTION_NAME_FIELD_NUMBER: _ClassVar[int]
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    choice_name: str
    election_name: str
    token: AuthToken
    def __init__(self, election_name: _Optional[str] = ..., choice_name: _Optional[str] = ..., token: _Optional[_Union[AuthToken, _Mapping]] = ...) -> None: ...

class VoteCount(_message.Message):
    __slots__ = ["choice_name", "count"]
    CHOICE_NAME_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    choice_name: str
    count: int
    def __init__(self, choice_name: _Optional[str] = ..., count: _Optional[int] = ...) -> None: ...

class Voter(_message.Message):
    __slots__ = ["group", "name", "public_key"]
    GROUP_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    PUBLIC_KEY_FIELD_NUMBER: _ClassVar[int]
    group: str
    name: str
    public_key: bytes
    def __init__(self, name: _Optional[str] = ..., group: _Optional[str] = ..., public_key: _Optional[bytes] = ...) -> None: ...

class VoterName(_message.Message):
    __slots__ = ["name"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...
