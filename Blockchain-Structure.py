
"""
Created on Mon Jun 24 13:40:41 2019

@author: Subhasish Goswami
"""
import datetime #for the use of date and time when block is mined#
import hashlib #for SHA256#
from flask import Flask, jsonify
import json #for string object#
class Blockchain:
    def   __init__(self):
        self.chain= [] #creating chain in form of a list#
        self.create_block(proof= 1, prev_hash= '0') #first block of the chain, prev_hash is kept 0 for random. '' because sha256 requires string
    def create_block(self, proof, prev_hash): #function to create a block in the chain from mined proof(data)#
        block= {
                'index': len(self.chain)+1,   #position of each block in the chain 
                'time': str(datetime.datetime.now()),  #Date and time when the function is caled. str() because SHA256 takes string to create hash
                'proof': proof,                       #we will get the proof after mining a block
                'prev_hash': prev_hash
                }                 
        
        self.chain.append(block) #adding the created block in the chain
        return block
    def previous_block(self): #to get the previous block
        return self.chain[-1]
    def proof_of_work(self,previous_block_proof):   #to return particuar proof(like nonce) for a block
        new_proof=1        #will check the proof from 1 and will keep it increamenting until correct proof is found which satisfies the problem
        check_proof= False
        while check_proof is False:
            hash_output= hashlib.sha256(str(new_proof**2-previous_block_proof**2).encode()).hexdigest() #hash_output is not same as hash of the block
            if hash_output[:5]=='00000': #first 5 digits of th hash_output of the block are 00000. this is governing condition for proof(once) of a block
                check_proof = True
            else:
                new_proof = new_proof +1
        return new_proof
    def hash(self, block):                            #to produce hash of a block
        encoded_string_block= json.dumps(block, sort_keys= True).encode() #to covert dictionary block into proper encoded string for sha256 argument
        return hashlib.sha256(encoded_string_block).hexdigest() #will return sha256 hash for the block
    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index= 1
        while block_index<len(chain):
            block= chain[block_index]
            if block['prev_hash']!= self.hash_of_block(previous_block):
                return False
            hash_output= hashlib.sha256(str(block['proof']**2- previous_block['proof']**2).encode())
            if hash_output[:4] != '0000' :
                return False
            previous_block= block
            block_index += 1
        return True

app = Flask(__name__)
blockchain= Blockchain()
@app.route('/mine_block', methods = ['GET'])

def mine_block():
    previous_block = blockchain.previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof, previous_hash)
    response = {'message': 'Congratulations, you just mined a block!',
                'index': block['index'],
                'timestamp': block['time'],
                'proof': block['proof'],
                'prev_hash': block['prev_hash']}
    return jsonify(response), 200
 
@app.route('/get_chain', methods = ['GET'])
def get_chain():
    response = {'chain': blockchain.chain,
                'length': len(blockchain.chain)}
    return jsonify(response), 200


@app.route('/is_valid', methods = ['GET'])
def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_valid:
        response = {'message': 'All good. The Blockchain is valid.'}
    else:
        response = {'message': 'Houston, we have a problem. The Blockchain is not valid.'}
    return jsonify(response), 200
app.run(host= '0.0.0.0', port= 5000)

 