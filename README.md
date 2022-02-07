# RSA_Shamir_Algorithms

App:

    This app uses RSA Algorithm to create a key pair consisting of a public and private key, then by using the Shamir's 
    Secret Sharing Algorithm, it breaks the private key into n pieces with the dependancy that at least k shares of the 
    private key are required to reconstruct it. It writes the public key and the shares of the private key into their 
    respective files. Then it reads the public key and at least the required shares 'k' (as per the input of user) from 
    their respective files and reconstructs the private key. After that, it encrypts the message inputted by the user 
    using the public key which was read from its file and decrypts the message using the reconstructed private key. 
    Lastly, it prints out a messge depending on whether or not the original message the deciphered text are the same.

App Dependencies:

    I use the python 3.9 version, it can easily work on versions later than 3.6.
    
    cryptodome library => pip3 install pycryptodome
    sslib library => pip3 install sslib
    

How to run the app on CLI:

    Go to the directory where the file 'RSA_Shamir_algo.py' in your system is.
    The command which runs it on CLI is:
    
    python3 RSA_Shamir_algo.py n k msg
    Alternatively,
    python RSA_Shamir_algo.py n k msg
    
    where 'n' is the number of shares you want to break the private key in, 'k' is the number of required shares needed 
    to rebuild the private key and msg is the message that you want to try the encryption and decryption on.
    Now, it's not necessary for you to provide these arguments because if you don't, the app will ask you for them. 
    Also, any extra arguments provided will be overlooked.
    
    Even if you are not in the same directory as the file, you can still run it by giving a relative or an absolute 
    path to the file.
    Like,
    python3 /home/User/Downloads/RSA_Shamir_algo.py n k msg
    or,
    python3 ../../ABC/XYZ/RSA_Shamir_algo.py n k msg
    
    
How to run the unit test:

    The python library used in the unit test should be pre-installed with python.
    Similarly to running the CLI, go to the directory where the file 'unit_test.py' in your system is.
    he command which runs it on CLI is:
    
    python3 unit_test.py
    Alternatively,
    python unit_test.py
    
    Even if you are not in the same directory as the file, you can still run it by giving a relative or an absolute 
    path to the file.
    Like,
    python3 /home/User/Downloads/unit_test.py
    or,
    python3 ../../ABC/XYZ/unit_test.py
