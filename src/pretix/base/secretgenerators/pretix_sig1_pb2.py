# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: pretix_sig1.proto
"""Generated protocol buffer code."""

from google.protobuf import (
    descriptor as _descriptor,
    descriptor_pool as _descriptor_pool,
    symbol_database as _symbol_database,
)
from google.protobuf.internal import builder as _builder

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\x11pretix_sig1.proto"I\n\x06Ticket\x12\x0c\n\x04seed\x18\x01 \x01(\t\x12\x0c\n\x04item\x18\x02 \x01(\x03\x12\x11\n\tvariation\x18\x03 \x01(\x03\x12\x10\n\x08subevent\x18\x04 \x01(\x03\x42\x33\n#eu.pretix.libpretixsync.crypto.sig1B\x0cTicketProtosb\x06proto3'
)

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'pretix_sig1_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'\n#eu.pretix.libpretixsync.crypto.sig1B\014TicketProtos'
    _globals['_TICKET']._serialized_start = 21
    _globals['_TICKET']._serialized_end = 94
# @@protoc_insertion_point(module_scope)
