# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import voting_pb2 as voting__pb2


class eVotingStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.RegisterVoter = channel.unary_unary(
                '/voting.eVoting/RegisterVoter',
                request_serializer=voting__pb2.Voter.SerializeToString,
                response_deserializer=voting__pb2.Status.FromString,
                )
        self.UnregisterVoter = channel.unary_unary(
                '/voting.eVoting/UnregisterVoter',
                request_serializer=voting__pb2.VoterName.SerializeToString,
                response_deserializer=voting__pb2.Status.FromString,
                )
        self.PreAuth = channel.unary_unary(
                '/voting.eVoting/PreAuth',
                request_serializer=voting__pb2.VoterName.SerializeToString,
                response_deserializer=voting__pb2.Challenge.FromString,
                )
        self.Auth = channel.unary_unary(
                '/voting.eVoting/Auth',
                request_serializer=voting__pb2.AuthRequest.SerializeToString,
                response_deserializer=voting__pb2.AuthToken.FromString,
                )
        self.CreateElection = channel.unary_unary(
                '/voting.eVoting/CreateElection',
                request_serializer=voting__pb2.Election.SerializeToString,
                response_deserializer=voting__pb2.Status.FromString,
                )
        self.CastVote = channel.unary_unary(
                '/voting.eVoting/CastVote',
                request_serializer=voting__pb2.Vote.SerializeToString,
                response_deserializer=voting__pb2.Status.FromString,
                )
        self.GetResult = channel.unary_unary(
                '/voting.eVoting/GetResult',
                request_serializer=voting__pb2.ElectionName.SerializeToString,
                response_deserializer=voting__pb2.ElectionResult.FromString,
                )


class eVotingServicer(object):
    """Missing associated documentation comment in .proto file."""

    def RegisterVoter(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UnregisterVoter(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def PreAuth(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Auth(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CreateElection(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CastVote(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetResult(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_eVotingServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'RegisterVoter': grpc.unary_unary_rpc_method_handler(
                    servicer.RegisterVoter,
                    request_deserializer=voting__pb2.Voter.FromString,
                    response_serializer=voting__pb2.Status.SerializeToString,
            ),
            'UnregisterVoter': grpc.unary_unary_rpc_method_handler(
                    servicer.UnregisterVoter,
                    request_deserializer=voting__pb2.VoterName.FromString,
                    response_serializer=voting__pb2.Status.SerializeToString,
            ),
            'PreAuth': grpc.unary_unary_rpc_method_handler(
                    servicer.PreAuth,
                    request_deserializer=voting__pb2.VoterName.FromString,
                    response_serializer=voting__pb2.Challenge.SerializeToString,
            ),
            'Auth': grpc.unary_unary_rpc_method_handler(
                    servicer.Auth,
                    request_deserializer=voting__pb2.AuthRequest.FromString,
                    response_serializer=voting__pb2.AuthToken.SerializeToString,
            ),
            'CreateElection': grpc.unary_unary_rpc_method_handler(
                    servicer.CreateElection,
                    request_deserializer=voting__pb2.Election.FromString,
                    response_serializer=voting__pb2.Status.SerializeToString,
            ),
            'CastVote': grpc.unary_unary_rpc_method_handler(
                    servicer.CastVote,
                    request_deserializer=voting__pb2.Vote.FromString,
                    response_serializer=voting__pb2.Status.SerializeToString,
            ),
            'GetResult': grpc.unary_unary_rpc_method_handler(
                    servicer.GetResult,
                    request_deserializer=voting__pb2.ElectionName.FromString,
                    response_serializer=voting__pb2.ElectionResult.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'voting.eVoting', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class eVoting(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def RegisterVoter(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/voting.eVoting/RegisterVoter',
            voting__pb2.Voter.SerializeToString,
            voting__pb2.Status.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def UnregisterVoter(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/voting.eVoting/UnregisterVoter',
            voting__pb2.VoterName.SerializeToString,
            voting__pb2.Status.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def PreAuth(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/voting.eVoting/PreAuth',
            voting__pb2.VoterName.SerializeToString,
            voting__pb2.Challenge.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Auth(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/voting.eVoting/Auth',
            voting__pb2.AuthRequest.SerializeToString,
            voting__pb2.AuthToken.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def CreateElection(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/voting.eVoting/CreateElection',
            voting__pb2.Election.SerializeToString,
            voting__pb2.Status.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def CastVote(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/voting.eVoting/CastVote',
            voting__pb2.Vote.SerializeToString,
            voting__pb2.Status.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetResult(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/voting.eVoting/GetResult',
            voting__pb2.ElectionName.SerializeToString,
            voting__pb2.ElectionResult.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
