from google.protobuf.descriptor import Descriptor, FileDescriptor
from google.protobuf.descriptor_pool import DescriptorPool

class MessageIndexFinder:

    def get_by_descriptor(self, schema_descriptor: FileDescriptor, descriptor_to_find: Descriptor) -> int:
        descriptor_to_index_map = self.get_all(schema_descriptor)
        if descriptor_to_find not in descriptor_to_index_map:
            raise KeyError(f"Provided descriptor is not present in the schema: {descriptor_to_find.name}")

        return descriptor_to_index_map.get(descriptor_to_find)

    def get_by_index(self, schema_descriptor: FileDescriptor, index_to_find: int) -> Descriptor:
        index_to_descriptor_dict = {}
        for descriptor, index in self.get_all(schema_descriptor):
            index_to_descriptor_dict[index] = descriptor

        if index_to_find not in index_to_descriptor_dict:
            raise KeyError(f"No corresponding descriptor found for the inded {index_to_find}")

        return index_to_descriptor_dict.get(index_to_find)

    def get_all(self, schema_descriptor: FileDescriptor) -> dict[Descriptor, int]:
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
