from io import BytesIO

from aws_schema_registry.proto_message_index_finder import MessageIndexFinder
from aws_schema_registry.schema import DataFormat, Schema, ValidationError
from google.protobuf.descriptor import Descriptor, FileDescriptor
from google.protobuf.message import Message
from google.protobuf.proto import serialize


class ProtobufSchema(Schema):
    def __init__(self, definition: str):
        self.descriptor = None
        self._definition = definition
        # self.schema_name = schema_name
        self.message_index_finder = MessageIndexFinder()

    @property
    def file_descriptor(self) -> Descriptor:
        return self.descriptor

    @file_descriptor.setter
    def file_descriptor(self, descriptor: Descriptor) -> None:
        self.descriptor = descriptor

    @property
    def data_format(self) -> DataFormat:
        return 'PROTOBUF'

    def write(self, data) -> bytes:
        b = BytesIO()

        schema_file_descriptor: FileDescriptor = data.DESCRIPTOR.file

        message_index = self.message_index_finder.get_by_descriptor(self.descriptor.file, self.descriptor)

        b.write(message_index.to_bytes(4, byteorder='big'))
        b.write(data.SerializeToString())

        value = b.getvalue()
        b.close()
        return value

    def read(self, bytes_: bytes):
        b = BytesIO(bytes_)

        # schema_proto_file_name = get_proto_file_name(self.schema_name)

        # fake file descriptor, the real file descriptor should be generated from the schema def and class name
        file_descriptor: FileDescriptor = self.message_index_finder.g




    def validate(self, data):
        pass
