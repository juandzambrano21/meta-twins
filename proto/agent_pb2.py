# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: agent.proto
# Protobuf Python Version: 5.26.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0b\x61gent.proto\x12\x05\x61gent\"6\n\x0bTaskRequest\x12\x13\n\x0b\x64\x65scription\x18\x01 \x01(\t\x12\x12\n\ninput_data\x18\x02 \x01(\t\"\x1e\n\x0cTaskResponse\x12\x0e\n\x06status\x18\x01 \x01(\t2F\n\x0c\x41gentService\x12\x36\n\x0b\x45xecuteTask\x12\x12.agent.TaskRequest\x1a\x13.agent.TaskResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'agent_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_TASKREQUEST']._serialized_start=22
  _globals['_TASKREQUEST']._serialized_end=76
  _globals['_TASKRESPONSE']._serialized_start=78
  _globals['_TASKRESPONSE']._serialized_end=108
  _globals['_AGENTSERVICE']._serialized_start=110
  _globals['_AGENTSERVICE']._serialized_end=180
# @@protoc_insertion_point(module_scope)
