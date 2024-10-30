from google.protobuf.descriptor import Descriptor, FileDescriptor
from google.protobuf.descriptor_pool import DescriptorPool

class MessageIndexFinder:

    def getAll(self, schema_descriptor: FileDescriptor) -> dict[Descriptor, int]:
        all_descriptor: list[Descriptor] = []

        parent_level_types = schema_descriptor.message_types_by_name.values()
        descriptor_queue: list[Descriptor] = list(parent_level_types)

        while len(descriptor_queue) != 0:
            descriptor = descriptor_queue.pop()
            all_descriptor.append(descriptor)

            nested_descriptor: list[Descriptor] = descriptor.nested_types
            descriptor_queue.extend(nested_descriptor)

        # Sort descriptor names by lexicographical order and assign an index.
        all_descriptor.sort(key=lambda x: x.name)

        message_indices: dict[Descriptor, int] = {}
        for i in range(len(all_descriptor)):
            message_indices[all_descriptor[i]] = i

        return message_indices
