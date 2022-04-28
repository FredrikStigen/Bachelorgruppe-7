# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: proto.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0bproto.proto\"o\n\rclientRequest\x12\x10\n\x08methodID\x18\x01 \x01(\x05\x12\x10\n\x08velocity\x18\x03 \x01(\x05\x12\x14\n\x0c\x61\x63\x63\x65leration\x18\x04 \x01(\x05\x12\x11\n\tvariable1\x18\x05 \x01(\x05\x12\x11\n\tvariable2\x18\x06 \x01(\x05\"2\n\x0eserverResponse\x12\x0c\n\x04resp\x18\x01 \x01(\t\x12\x12\n\nstartCount\x18\x02 \x01(\x05\"\x1f\n\x0c\x63lientStream\x12\x0f\n\x07\x63ounter\x18\x01 \x01(\x05\"0\n\x0cserverStream\x12\x0f\n\x07\x63ounter\x18\x01 \x01(\x05\x12\x0f\n\x07\x65ncoder\x18\x02 \x01(\x05\x32V\n\x06stream\x12%\n\x02SM\x12\x0e.clientRequest\x1a\x0f.serverResponse\x12%\n\x03SSM\x12\r.clientStream\x1a\r.serverStream(\x01\x62\x06proto3')



_CLIENTREQUEST = DESCRIPTOR.message_types_by_name['clientRequest']
_SERVERRESPONSE = DESCRIPTOR.message_types_by_name['serverResponse']
_CLIENTSTREAM = DESCRIPTOR.message_types_by_name['clientStream']
_SERVERSTREAM = DESCRIPTOR.message_types_by_name['serverStream']
clientRequest = _reflection.GeneratedProtocolMessageType('clientRequest', (_message.Message,), {
  'DESCRIPTOR' : _CLIENTREQUEST,
  '__module__' : 'proto_pb2'
  # @@protoc_insertion_point(class_scope:clientRequest)
  })
_sym_db.RegisterMessage(clientRequest)

serverResponse = _reflection.GeneratedProtocolMessageType('serverResponse', (_message.Message,), {
  'DESCRIPTOR' : _SERVERRESPONSE,
  '__module__' : 'proto_pb2'
  # @@protoc_insertion_point(class_scope:serverResponse)
  })
_sym_db.RegisterMessage(serverResponse)

clientStream = _reflection.GeneratedProtocolMessageType('clientStream', (_message.Message,), {
  'DESCRIPTOR' : _CLIENTSTREAM,
  '__module__' : 'proto_pb2'
  # @@protoc_insertion_point(class_scope:clientStream)
  })
_sym_db.RegisterMessage(clientStream)

serverStream = _reflection.GeneratedProtocolMessageType('serverStream', (_message.Message,), {
  'DESCRIPTOR' : _SERVERSTREAM,
  '__module__' : 'proto_pb2'
  # @@protoc_insertion_point(class_scope:serverStream)
  })
_sym_db.RegisterMessage(serverStream)

_STREAM = DESCRIPTOR.services_by_name['stream']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _CLIENTREQUEST._serialized_start=15
  _CLIENTREQUEST._serialized_end=126
  _SERVERRESPONSE._serialized_start=128
  _SERVERRESPONSE._serialized_end=178
  _CLIENTSTREAM._serialized_start=180
  _CLIENTSTREAM._serialized_end=211
  _SERVERSTREAM._serialized_start=213
  _SERVERSTREAM._serialized_end=261
  _STREAM._serialized_start=263
  _STREAM._serialized_end=349
# @@protoc_insertion_point(module_scope)