import grpc
import argparse
import voting_pb2_grpc
import voting_pb2
import nacl.signing
from google.protobuf.timestamp_pb2 import Timestamp
from datetime import datetime, timedelta
from google.protobuf import timestamp_pb2
### user login
def try_login(stub, UserName, private_key):
    VoterName = voting_pb2.VoterName(name=UserName)
    ### get a challenge need to response
    
    Challenge = stub.PreAuth(VoterName)
    ### package the response and the user name into the Request
    request = voting_pb2.AuthRequest()
    request.name.name = VoterName.name
    request.response.value = bytes(private_key.sign(Challenge.value, encoder=nacl.encoding.RawEncoder))
    
    ### get the response
    auth_token = stub.Auth(request)
    
    return auth_token


def parse_arguments():
    parser = argparse.ArgumentParser(description='Client')
    parser.add_argument('--host', default='localhost', type=str)
    parser.add_argument('--port', default='50051', type=str)
    parser.add_argument('--identity', default='voter', help='identity={voter, vote_creator}', type=str)
    parser.add_argument('--user_name', default='unknown', type=str)
    parser.add_argument('--my_group', help='you may reference the groups list', type=str)
    parser.add_argument('--election_name', default='Student president election', type=str)
    
    
    ### if the identity is vote_creator, use the below arguments
    parser.add_argument('--groups', nargs='+', help="e.g. g undergraduate_student graduate_student means g=['undergraduate_student', 'graduate_student']", default=['undergraduate_student', 'graduate_student'], type=str)
    parser.add_argument('--choices', nargs='+', help="e.g. c Apple Orange means =['Apple, Orange']", default=['Apple', 'Orange'], type=str)
    
    ### dafault end time
    # timestamp = Timestamp()
    #current_time = timestamp.GetCurrentTime()
    # print(current_time)
    parser.add_argument('--during_time', default=1, help='This term means the during time (hours) of the voting system. Default the voting will end an hour later.', type=int)
    
    
    ### if the identity is voter, use the below arguments
    
    parser.add_argument('--choice_name', help='please choose the valid candidate, you may reference the candidate list, if you are the vote creator, set to NIL', type=str)
    
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_arguments()
    host = args.host
    port = args.port
    identity = args.identity
    user_name = args.user_name
    my_group = args.my_group
    election_name = args.election_name
    groups = args.groups
    choices = args.choices
    during_time = args.during_time
    choice_name = args.choice_name
    
    # Create a new Timestamp object instance
    ts = timestamp_pb2.Timestamp()

    # Call the GetCurrentTime() method on the Timestamp object
    ts.GetCurrentTime()
    ts_plus_one_hour = ts.ToDatetime() + timedelta(seconds=during_time)
    # Print the Timestamp object to check if it was updated successfully
    # print(ts)

    ts.FromDatetime(dt=ts_plus_one_hour)
    end_date = ts
    
    
    if my_group not in groups:
        print(f'The groups: {groups}')
        raise(f'invalid groups')
        
    
    ### connect to the localhost:50051
    channel = grpc.insecure_channel(host + ':' + port)

    ### make a stub
    stub = voting_pb2_grpc.eVotingStub(channel)
    
    ### create the user info
    signing_key = nacl.signing.SigningKey.generate()
    verify_key = signing_key.verify_key

    ### try to login and get the response from the server (AuthToken)
    
    voter = voting_pb2.Voter(name=user_name, group=my_group, public_key=verify_key.encode(encoder=nacl.encoding.RawEncoder))
    status = stub.RegisterVoter(voter).code
    
    if status == 0:
        print(f'Successful registerion')
    elif status == 1:
        print(f'Voter with the same name already exists, update its public_key')
    elif status == 2:
        print(f'Undefined error')
    
    auth_token = try_login(stub, user_name, private_key=signing_key)
    
    
    if identity == 'vote_creator':
        timestamp = Timestamp()
        
        election = voting_pb2.Election(name=election_name, groups=groups, choices=choices, end_date=end_date, token=auth_token)
        status = stub.CreateElection(election).code
        
        if status != 0:
            if status == 1:
                raise(f'invalid authentication token')
            elif status == 2:
                raise(f'Missing groups or choices specification (at least one group and one choice should be listed for the election)')
            elif status == 3:
                raise(f'Unknown error')
        print('Waiting for the result...')
        ts = timestamp_pb2.Timestamp()
        ts.GetCurrentTime()  
        while ts.seconds <= end_date.seconds:
            ts.GetCurrentTime()
            # print(f'{ts.second} : {end_date.seconds})
            continue
            
        election_name = voting_pb2.ElectionName(name=election_name)
        status = stub.GetResult(election_name)
        if status != 0:
            if status == 1:
                raise(f'None-existent election')
            elif status == 2:
                raise(f'The election is still ongoing. Election result is not available yet')
        
        print(status.counts)
        print(f'Election is over')
        
        
    elif identity == 'voter':
        vote = voting_pb2.Vote(election_name=election_name, choice_name=choice_name, token=auth_token)
        
        status = stub.CastVote(vote).code
        
        if status != 0:
            if status == 1:
                raise(f'Invalid authentication token')
            elif status == 2:
                raise(f'Invalid election name')
            elif status == 3:
                raise(f"The voter's group is not allowed in the election")
            elif status == 4:
                raise(f'A previous vote has been cast')
            
        print(f'Successful vote')
        # new_name = voting_pb2.VoterName(name='Dann')
        # status = stub.UnregisterVoter(new_name).code
        # if status != 0:
        #     if status == 1:
        #         raise(f'No voter with the name exists on the server')
        
    else:
        raise(f'invalid identity')
    