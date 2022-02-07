from sslib import shamir
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
import sys


def keys_to_file(public_key, private_key_shares: list):
    '''This function writes the public key and the private key
    broken into shards in the respective files'''

    with open("Public.txt", mode='w') as file:
        file.write(public_key.export_key().decode())

    for i in range(len(private_key_shares)):
        with open(f"Shard{i+1}.txt", mode='w') as file:
            file.write(private_key_shares[i])

    return 0


def keys_from_files(required_shares: int, index: list):
    '''This function reads the public key and the shares of private keys from the files
    and reconstructs the private key using minimum shares required'''

    with open("Public.txt", mode='r') as file:
        public_key = RSA.import_key(file.read())

    shards = []
    for i in index:
        with open(f"Shard{i}.txt", mode='r') as file:
            shards.append(file.read())

    private_key = regenerate_private_key(required_shares, shards)

    return private_key, public_key


def shards(n: int, k: int, private_key):
    '''This function splits the RSA private key into n shards such that
    it would require at least k shards to reconstruct it'''

    raw_data = shamir.split_secret(secret_bytes=private_key.export_key().decode().encode('utf-16'),
                                   required_shares=k,
                                   distributed_shares=n)

    data_base64 = shamir.to_base64(raw_data)
    with open('PrimeMod.txt', mode='w') as file:
        file.write(data_base64.get("prime_mod"))

    return data_base64["shares"], data_base64["required_shares"]


def regenerate_private_key(required_shares: int, shares: list):
    '''This function reconstructs the private key using minimum shares required'''

    dic_ = dict()
    dic_["required_shares"] = required_shares
    dic_["shares"] = shares
    with open("PrimeMod.txt", 'r') as file:
        prime_mod = file.read()
    dic_["prime_mod"] = prime_mod

    private_key = shamir.recover_secret(shamir.from_base64(dic_)).decode('utf-16')
    return RSA.import_key(private_key)


def generate_key_pair():
    '''Generates RSA public and private key pair'''

    private_key = RSA.generate(1024)
    public_key = private_key.public_key()

    return private_key, public_key


def encrypt_message(message: str, public_key):
    '''Encrypts a message using RSA public key'''

    cipher = PKCS1_OAEP.new(public_key)
    return cipher.encrypt(message.encode('utf-16'))


def decrypt_message(cipher, private_key):
    '''Decrypts the encoded message'''

    decrypt = PKCS1_OAEP.new(private_key)
    return decrypt.decrypt(cipher).decode('utf-16')


if __name__ == "__main__":
    print("Welcome to RSA and Shamir algorithm testing")
    private_key, public_key = generate_key_pair()
    
    if len(sys.argv) < 2:
        n = int(input("Enter the number of shares you want for the private key: "))
        k = int(input("Enter the least amount of shares needed to reconstruct the private key: "))
        msg = input("Enter the message you would like to encrypt: ")
    else:
        if len(sys.argv) == 2:
            n = int(sys.argv[1])
            k = int(input("Enter the least amount of shares needed to reconstruct the private key: "))
            msg = input("Enter the message you would like to encrypt: ")
        elif len(sys.argv) == 3:
            n = int(sys.argv[1])
            k = int(sys.argv[2])
            msg = input("Enter the message you would like to encrypt: ")
        else:
            n = int(sys.argv[1])
            k = int(sys.argv[2])
            msg = str(sys.argv[3])

    shares, k = shards(n, k, private_key)

    keys_to_file(public_key, shares)

    index = input("Enter the index of shards that you want to use "
                  "to reconstruct the key (separate the values by ','): ").split(',')
    index = set(index)
    
    if len(index) < k:
        sys.exit(f"You need at least {k} shares.")
    if len(index) > n:
        sys.exit("Index Overflow")

    shares_indices = [int(i) for i in index]

    re_private_key, re_public_key = keys_from_files(k, shares_indices)

    cipher = encrypt_message(msg, public_key)
    text = decrypt_message(cipher, re_private_key)

    if msg == text:
        print(f"\nMessage successfully decrypted.\nDecrypted message: {text}")
    else:
        print("There's something fishy with the algorithm implementation.")
