from typing import Iterable, Optional, Text

from google.protobuf.descriptor_pb2 import FileDescriptorProto
from google.protobuf.internal.containers import RepeatedCompositeFieldContainer, RepeatedScalarFieldContainer
from google.protobuf.internal.enum_type_wrapper import EnumTypeWrapper
from google.protobuf.message import Message

class Version(Message):
    major: int
    minor: int
    patch: int
    suffix: Text
    def __init__(
        self, major: Optional[int] = ..., minor: Optional[int] = ..., patch: Optional[int] = ..., suffix: Optional[Text] = ...
    ) -> None: ...

class CodeGeneratorRequest(Message):
    file_to_generate: RepeatedScalarFieldContainer[Text]
    parameter: Text
    @property
    def proto_file(self) -> RepeatedCompositeFieldContainer[FileDescriptorProto]: ...
    @property
    def compiler_version(self) -> Version: ...
    def __init__(
        self,
        file_to_generate: Optional[Iterable[Text]] = ...,
        parameter: Optional[Text] = ...,
        proto_file: Optional[Iterable[FileDescriptorProto]] = ...,
        compiler_version: Optional[Version] = ...,
    ) -> None: ...

class CodeGeneratorResponse(Message):
    class File(Message):
        name: Text
        insertion_point: Text
        content: Text
        def __init__(
            self, name: Optional[Text] = ..., insertion_point: Optional[Text] = ..., content: Optional[Text] = ...
        ) -> None: ...
    class _Feature(EnumTypeWrapper):
        FEATURE_NONE: int
        FEATURE_PROTO_3_OPTIONAL: int
    Feature: CodeGeneratorResponse._Feature
    FEATURE_NONE: int
    FEATURE_PROTO_3_OPTIONAL: int
    supported_features: int
    error: Text
    @property
    def file(self) -> RepeatedCompositeFieldContainer[CodeGeneratorResponse.File]: ...
    def __init__(self, error: Optional[Text] = ..., file: Optional[Iterable[CodeGeneratorResponse.File]] = ...) -> None: ...
