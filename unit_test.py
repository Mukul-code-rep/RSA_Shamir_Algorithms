import unittest
import RSA_Shamir_algo


class TestAlgo(unittest.TestCase):

    def testcase(self):
        #generating keys
        encrypted_priv_key, encrypted_public_key = RSA_Shamir_algo.generate_key_pair()

        #Breaking up private key into 5 shares with the condition that at least two shares are needed to
        # reconstruct the key
        shards, k = RSA_Shamir_algo.shards(5, 2, encrypted_priv_key)

        #Using key 2 and 5 to reconstruct the share
        re_priv_key = RSA_Shamir_algo.regenerate_private_key(k, [shards[1], shards[4]])

        #Message to encode
        msg = "Test Run"

        #Encrypting the message using public key
        cipher = RSA_Shamir_algo.encrypt_message(msg, encrypted_public_key)

        #Decrypting the message using reconstructed private key
        decrypted_msg = RSA_Shamir_algo.decrypt_message(cipher, re_priv_key)

        #Checking if the original message matches the decrypted one
        if msg == decrypted_msg:
            print("The test was successful.")
        else:
            print("The test failed.")


if __name__ == "__main__":
    unittest.main()