# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: voting.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0cvoting.proto\x12\x06voting\x1a\x1fgoogle/protobuf/timestamp.proto\"8\n\x05Voter\x12\x0c\n\x04name\x18\x01 \x02(\t\x12\r\n\x05group\x18\x02 \x02(\t\x12\x12\n\npublic_key\x18\x03 \x02(\x0c\"\x19\n\tVoterName\x12\x0c\n\x04name\x18\x01 \x02(\t\"\x16\n\x06Status\x12\x0c\n\x04\x63ode\x18\x01 \x02(\x05\"\x1a\n\tChallenge\x12\r\n\x05value\x18\x01 \x02(\x0c\"\x19\n\x08Response\x12\r\n\x05value\x18\x01 \x02(\x0c\"R\n\x0b\x41uthRequest\x12\x1f\n\x04name\x18\x01 \x02(\x0b\x32\x11.voting.VoterName\x12\"\n\x08response\x18\x02 \x02(\x0b\x32\x10.voting.Response\"\x1a\n\tAuthToken\x12\r\n\x05value\x18\x01 \x02(\x0c\"\x89\x01\n\x08\x45lection\x12\x0c\n\x04name\x18\x01 \x02(\t\x12\x0e\n\x06groups\x18\x02 \x03(\t\x12\x0f\n\x07\x63hoices\x18\x03 \x03(\t\x12,\n\x08\x65nd_date\x18\x04 \x02(\x0b\x32\x1a.google.protobuf.Timestamp\x12 \n\x05token\x18\x05 \x02(\x0b\x32\x11.voting.AuthToken\"T\n\x04Vote\x12\x15\n\relection_name\x18\x01 \x02(\t\x12\x13\n\x0b\x63hoice_name\x18\x02 \x02(\t\x12 \n\x05token\x18\x03 \x02(\x0b\x32\x11.voting.AuthToken\"\x1c\n\x0c\x45lectionName\x12\x0c\n\x04name\x18\x01 \x02(\t\"/\n\tVoteCount\x12\x13\n\x0b\x63hoice_name\x18\x01 \x02(\t\x12\r\n\x05\x63ount\x18\x02 \x02(\x05\"C\n\x0e\x45lectionResult\x12\x0e\n\x06status\x18\x01 \x02(\x05\x12!\n\x06\x63ounts\x18\x02 \x03(\x0b\x32\x11.voting.VoteCount2\xe9\x02\n\x07\x65Voting\x12.\n\rRegisterVoter\x12\r.voting.Voter\x1a\x0e.voting.Status\x12\x34\n\x0fUnregisterVoter\x12\x11.voting.VoterName\x1a\x0e.voting.Status\x12/\n\x07PreAuth\x12\x11.voting.VoterName\x1a\x11.voting.Challenge\x12.\n\x04\x41uth\x12\x13.voting.AuthRequest\x1a\x11.voting.AuthToken\x12\x32\n\x0e\x43reateElection\x12\x10.voting.Election\x1a\x0e.voting.Status\x12(\n\x08\x43\x61stVote\x12\x0c.voting.Vote\x1a\x0e.voting.Status\x12\x39\n\tGetResult\x12\x14.voting.ElectionName\x1a\x16.voting.ElectionResult')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'voting_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _VOTER._serialized_start=57
  _VOTER._serialized_end=113
  _VOTERNAME._serialized_start=115
  _VOTERNAME._serialized_end=140
  _STATUS._serialized_start=142
  _STATUS._serialized_end=164
  _CHALLENGE._serialized_start=166
  _CHALLENGE._serialized_end=192
  _RESPONSE._serialized_start=194
  _RESPONSE._serialized_end=219
  _AUTHREQUEST._serialized_start=221
  _AUTHREQUEST._serialized_end=303
  _AUTHTOKEN._serialized_start=305
  _AUTHTOKEN._serialized_end=331
  _ELECTION._serialized_start=334
  _ELECTION._serialized_end=471
  _VOTE._serialized_start=473
  _VOTE._serialized_end=557
  _ELECTIONNAME._serialized_start=559
  _ELECTIONNAME._serialized_end=587
  _VOTECOUNT._serialized_start=589
  _VOTECOUNT._serialized_end=636
  _ELECTIONRESULT._serialized_start=638
  _ELECTIONRESULT._serialized_end=705
  _EVOTING._serialized_start=708
  _EVOTING._serialized_end=1069
# @@protoc_insertion_point(module_scope)
