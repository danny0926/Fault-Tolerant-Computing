import voting_pb2_grpc
import voting_pb2
import grpc
import time
import enum
import argparse
from datetime import datetime, timedelta
import nacl.signing
import ed25519
import numpy as np
from concurrent import futures
from google.protobuf.timestamp_pb2 import Timestamp
from google.protobuf import timestamp_pb2
import os
import re
import socket
import chardet
import base64

### class User
class User():
    def __init__(self, name, group, public_key):
        self.name = name
        self.group = group
        self.public_key = public_key
        
        self.challenge = base64.b64encode(np.random.bytes(64))#.decode('utf8')
        self.auth_token = base64.b64encode(np.random.bytes(64))#.decode('utf8')
        self.auth_token_expire_time = 0
        self.token_expire = False
        self.vote_done = False
        
    def set_challenge(self, challenge):
        self.challenge = challenge
        
    def set_authToken(self, token):
        self.auth_token = token
        
        # Create a new Timestamp object instance
        ts = timestamp_pb2.Timestamp()
        # Call the GetCurrentTime() method on the Timestamp object
        ts.GetCurrentTime()
        ts_plus_one_hour = ts.ToDatetime() + timedelta(hours=1)

        ts.FromDatetime(dt=ts_plus_one_hour)
        self.auth_token_expire_time = ts
        
    def check_token_alive(self,):
        ts = timestamp_pb2.Timestamp()
        ts.GetCurrentTime()
        if ts.seconds > self.auth_token_expire_time.seconds:
            print(f'Token expired, setting the new token...')
            new_token = np.random.bytes(64)
            new_token = bytes(1) if new_token == bytes(0) else new_token
            
            self.set_authToken(new_token)
        else:
            print(f'Token is valid, keep doing')

def find_idx(List, target, using='name'):
    ### only can find the user in User List
    for i in range(len(List)):
        if using == 'name':
            if List[i].name == target:
                return i
        if using == 'token':
            if List[i].auth_token == target:
                return i
            
    return -1


### class candidate
class Candidate():
    def __init__(self, name):
        self.name = name
        self.ballot = 0
        
    def get_vote(self,):
        self.ballot += 1

### make the server, make sure it need to inherent from voting_pb2_grpc.eVotingServicer
class eVotingServicer(voting_pb2_grpc.eVotingServicer):
    ### implement functionality if the server
    def __init__(self, restart=False):
        self.Users = []
        self.end_date = 0
        self.voting_name = 'unknown'
        self.candidates = []
        self.groups = []
        self.election_done = False
        
        if restart == False and os.path.isfile('backup.txt'):
            os.remove('backup.txt')
        if restart == True:
            self.recover_data()
        
    
    def RegisterVoter(self, request, context):
        ### register the new user
        code = 2
        Status = voting_pb2.Status(code=code)
        
        user_idx = find_idx(self.Users, request.name, using='name')
        if user_idx != -1:
            ## already registered
            code = 1
            self.Users[user_idx].public_key = request.public_key
            Status = voting_pb2.Status(code=code)
        if user_idx == -1:
            ## register the new user
            self.Users.append(User(name=request.name, group=request.group, public_key=request.public_key))
            code = 0
            Status = voting_pb2.Status(code=code)
        
        if code == 0:
            print(f'USER {request.name} register successfully.')
            print(self.Users)
        if code == 1:
            print(f'USER {request.name} already registered, public_key is {self.Users[-1].public_key}')
        if code == 2:
            print(f'Undefined error.')
        
        self.backup_data()
           
        return Status
    
    def UnregisterVoter(self, request, context):
        name = request.name
        code = 2
        Status = voting_pb2.Status(code=code)
        
        user_idx = find_idx(self.Users, name)
        
        if user_idx != -1:
            ## delete the user
            self.Users.pop(user_idx)
            code = 0
            Status = voting_pb2.Status(code=code)
            
        if user_idx == 1:
            ## user already D.N.E.
            code = 1
            Status = voting_pb2.Status(code=code)
        
        if code == 0:
            print(f'USER {request.name} unregister successfully.')
        if code == 1:
            print(f'USER {request.name} register already delete.')
        if code == 2:
            print(f'Undefined error.')
        
        self.backup_data()
        
        return Status
    
    
    def PreAuth(self, request, context):
        name = request.name
        # VoterName request
        
        user_idx = find_idx(self.Users, name)
        
        ### generate 4 bits number randomly as the challenge (int)
        encoded = base64.b64encode(np.random.bytes(64))
        Challenge = voting_pb2.Challenge(value=encoded)
        
        print(f'Send challenge: {Challenge.value} to user: {name}')
        
        self.Users[user_idx].set_challenge(encoded)
        
        self.backup_data()
        
        return Challenge
    
    
    def Auth(self, request, context):
        # AuthRequest request
        name = request.name.name
        response = request.response.value
        idx = find_idx(self.Users, name)
        verify_key = nacl.signing.VerifyKey(self.Users[idx].public_key, encoder=nacl.encoding.RawEncoder)

        signature = self.Users[idx].challenge
        
        
        try:   
            message = nacl.encoding.RawEncoder.decode(response)
            verify_key.verify(message, encoder=nacl.encoding.RawEncoder)
            token = np.random.bytes(64)
            
            ### 0 is used for fail login
            print(f'Login successfully')
            token = bytes(1) if token == bytes(0) else token
            
        except nacl.exceptions.BadSignatureError:
            print(f'Fail to Login.')
            print(f'Excepted: {signature}\nbut get: {message}')
            
            token = bytes(0)
            
        token = base64.b64encode(token)
        AuthToken = voting_pb2.AuthToken(value=token)
        self.Users[idx].set_authToken(token)    
        
        self.backup_data()
        
        return AuthToken
    
    
    def CreateElection(self, request, context):
        code = 3
        # print(code)
        ### Election request
        name = request.name
        groups = request.groups
        choices = request.choices
        token = request.token.value
        end_date = request.end_date
        # print('sent data')
        self.end_date = end_date
        self.voting_name = name
        self.candidates = []
        self.groups = []
        self.groups = groups
        self.election_done = False
        
        for people in choices:
            self.candidates.append(Candidate(people))
        # print(self.candidates)
        ### so far the setting of the election is done
        code = 0
        ### judge the status
        if find_idx(self.Users, token, using='token') == -1:
            code = 1
            print(f'Trying created vote by invaild token')
        else:
            idx = find_idx(self.Users, token, using='token')
            self.Users[idx].check_token_alive() 
        
        if len(self.candidates) == 0 or len(self.groups) == 0:
            code = 2
            print(f'Invalid number of groups or choices')
            
        
        
        Status = voting_pb2.Status(code=code)
        
        self.backup_data()
        
        return Status
    
    
    def CastVote(self, request, context):
        ### Vote request
        
        election_name = request.election_name    ### assume there is only one election, so this term not used
        choice_name = request.choice_name
        using_token = request.token.value
        
        user_idx = find_idx(self.Users, using_token, using='token')
        if user_idx == -1:
            ### invalid token
            code = 1
            print(f'Invalid authentication token')
        else:
            self.Users[user_idx].check_token_alive()
            
            if election_name != self.voting_name:
                ### invalid voting name
                code = 2
                print(f'Invalid election name')
                print(f'except {self.voting_name} but get {election_name}')
            else:
                if find_idx(self.candidates, choice_name) == -1:
                    ### not allowed in the election
                    code = 3
                    print("The voter's group is not allowed in the election")
                else:
                    if self.Users[user_idx].vote_done is True:
                        ### have been done the vote
                        code = 4
                    else:
                        candidate_idx = find_idx(self.candidates, choice_name, using='name')
                        print("giving a vote")
                        self.candidates[candidate_idx].get_vote()
                        self.Users[user_idx].vote_done = True
                        code = 0
                        print(f'candidate {self.candidates[candidate_idx].name} got 1 vote')
        
        
        Status = voting_pb2.Status(code=code)
        print('do the backup operation')
        self.backup_data()
        
        return Status
        
        
    def GetResult(self, request, context):
        #### ElectionName request
        
        voting_name = request.name
        result = []

        if voting_name != self.voting_name:
            code = 1
            print(f'Non-sxistent election')
        else:    
            ts = timestamp_pb2.Timestamp()
            ts.GetCurrentTime()
            if ts.seconds <= self.end_date.seconds:
                code = 2
                print(f'The election is still ongoing. Election result is not available yet')
            else:
                code = 0
                for candidate in self.candidates:
                    result.append(voting_pb2.VoteCount(choice_name=candidate.name, count=candidate.ballot))
                    
        ElectionResult = voting_pb2.ElectionResult(status=code, counts=result)
        
        return ElectionResult
        
    
        
    def backup_data(self,):
        ### backup the data to a file, named backup.txt
        """
        need to store: self.Users,      (list)
                       |- self.name              (str)
                       |- self.group             (str)
                       |- self.public_key        (binary)
                       |- self.challenge         (binary)
                       |- self.auth_token        (binary)
                       |- self.auth_token_expire_time (int)
                       |- self.token_expire      (bool)
                       |- self.vote_done         (bool)
                       
                       self.end_date,
                       self.voting_name,
                       
                       self.candidates, (list)
                       |- self.name
                       |- self.ballot
                       
                       self.groups,     (list)
                       self.election_done
        """
        with open('backup.txt', mode='w', newline='') as f:
            ### clear contents in the file
            f.truncate()
            f.write(str(len(self.Users)) + '\n')
            for user in self.Users:
                f.write(str(user.name) + '\n')
                f.write(str(user.group) + '\n')
                #encoding = chardet.detect(user.public_key)['encoding']
                #print(encoding)
                """
                bytes = new.decode('windows-1251'))    ### bytes -> str
                string = new.decode('windows-1251').encode('windows-1251')  ### bytes -> str -> bytes
                
                Stored by utf8 encoding, used by windows-1251 encoding
                
                print(type(user.public_key))    ### bytes
                print(user.public_key)
                print()
                print(type(user.public_key.decode('windows-1251').encode('utf8')))    ### bytes
                print(user.public_key.decode('windows-1251').encode('utf8'))
                print()
                print(type(user.public_key.decode('windows-1251').encode('utf8').decode('utf8')))   ### str
                print(user.public_key.decode('windows-1251').encode('utf8').decode('utf8'))
                print()
                print(type(user.public_key.decode('windows-1251').encode('utf8').decode('utf8').encode('windows-1251')))    ### bytes
                print(user.public_key.decode('windows-1251').encode('utf8').decode('utf8').encode('windows-1251'))
                input()
                """
                #print(base64.b64encode(user.public_key))
                #print(type(base64.b64encode(user.public_key)))
                #print(base64.b64encode(user.public_key).decode('utf8'))
                #print(type(base64.b64encode(user.public_key).decode('utf8')))
                #input()
                #f.write(user.public_key.decode(encoding).encode('utf8').decode('utf8') + '\n')
                f.write(base64.b64encode(user.public_key).decode('utf8') + '\n')
                f.write(user.challenge.decode('utf8') + '\n')
                f.write(user.auth_token.decode('utf8') + '\n')
                f.write(str(user.auth_token_expire_time) + '\n')
                f.write(str(user.token_expire) + '\n')
                f.write(str(user.vote_done) + '\n')
                
            f.write(str(self.end_date) + '\n')
            f.write(self.voting_name + '\n')
            f.write(str(len(self.candidates)) + '\n')
            for candidate in self.candidates:
                candidate_info = str(candidate.name) + ',' + str(candidate.ballot) + '\n'
                f.write(candidate_info)
            f.write(str(len(self.groups)) + '\n')
            for group in self.groups:
                f.write(group + '\n')
            f.write(str(self.election_done) + '\n')
            
        print("Got an action on server, doing the backup operation.")
        
    def recover_data(self,):
        
        with open('backup.txt', 'r') as f:
            user_num = f.readline()
             
            ### reconver all users
            for i in range(int(user_num)):
                name = f.readline()[:-1]
                #print(name)
                #print('read name done')
                #input()
                group = f.readline()[:-1]
                public_key = (f.readline()[:-1]).encode('utf8')
                challenge = (f.readline()[:-1]).encode('utf8')
                auth_token = (f.readline()[:-1]).encode('utf8')
                seconds = f.readline()
                seconds = int(seconds[9:-2])
                nanos = f.readline()
                nanos = int(nanos[7:-1])
                #print(nanos)
                auth_token_expire_time  = Timestamp(seconds=seconds, nanos=nanos)
                dangling = f.readline()[:-1] ### the surplus \n
                str_token_expire = f.readline()
                token_expire = True if str_token_expire == True else False
                #print(type(token_expire))
                
                str_vote_done = f.readline()
                vote_done = True if str_vote_done == True else False
                #print(vote_done)
                
                self.Users.append(User(name=name,
                                       group=group,
                                       public_key=public_key))
                self.Users[i].challenge = challenge
                self.Users[i].auth_token = auth_token
                self.Users[i].auth_token_expire_time = auth_token_expire_time
                self.Users[i].vote_done = vote_done
            
            seconds = f.readline()
            seconds = int(seconds[9:-2])
            nanos = f.readline()
            nanos = int(nanos[7:-1])
            self.end_date = Timestamp(seconds=seconds, nanos=nanos)
            dangling = f.readline() ### the surplus \n
            self.voting_name = f.readline()[:-1]
            candidate_num = f.readline()  
            ### recover all candidates
            for i in range(int(candidate_num)):
                candidate_info = f.readline().split(',')
                name = candidate_info[0]
                ballot = candidate_info[1][:-1]
                self.candidates.append(Candidate(name))
                
                self.candidates[i].ballot = int(ballot)
                
            groups_num = f.readline()
            self.group = []
            for i in range(int(groups_num)):
                self.groups.append(f.readline()[:-1])
            
            self.election_done = f.readline()[:-1]
                
                 
 
def parse_arguments():
    parser = argparse.ArgumentParser(description='Server')
    parser.add_argument('--port', default='50051', type=str)
    parser.add_argument('--restart', default=False, type=bool)
    
    return parser.parse_args()
    
def serve(port, restart):
    voting_server = eVotingServicer(restart=restart)
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    voting_pb2_grpc.add_eVotingServicer_to_server(voting_server, server)
    
    if restart == True:
        server.add_insecure_port('[::]:' + port)
        print(f"Waiting for reconnect the primary server...")
    else:
        server.add_insecure_port('[::]:' + port)

    print(f'server is acting......')
    server.start()
    
    try:
        while True:
            time.sleep(86400)
            
    except KeyboardInterrupt:
        print(f'Primary server not available, wait for 5 seconds before start up the backup server')
        time.sleep(5)
        server.stop(0)
    
    except grpc.RpcError:
        print(f'Primary server not available, wait for 5 seconds before start up the backup server')
        time.sleep(5)
    
    backup_server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    voting_pb2_grpc.add_eVotingServicer_to_server(voting_server, backup_server)
    backup_server.add_insecure_port('[::]:' + port)
    print(f'Backup server initialized')
    backup_server.start()
    
    try:
        while True:
            time.sleep(86400)
            
    except KeyboardInterrupt:
        backup_server.stop(0)

      
      
if __name__ == '__main__':
    args = parse_arguments()
    port = args.port
    restart = args.restart
    serve(port=port, restart=restart)