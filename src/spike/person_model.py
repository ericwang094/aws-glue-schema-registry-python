import schema_pb2

person = schema_pb2.Person()
person.id = 1234
person.name = "John Doe"
person.email = "jdoe@example.com"
phone = person.phones.add()
phone.number = "555-4321"
phone.type = schema_pb2.Person.PHONE_TYPE_HOME

print(person.DESCRIPTOR.file)

message_index = 4

converted_byte = message_index.to_bytes(4, byteorder='big')
print(converted_byte)

revert_back = int.from_bytes(converted_byte, byteorder='big')
print(revert_back)
