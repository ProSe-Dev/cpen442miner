import argparse
import hashlib

parser = argparse.ArgumentParser(description='Get the public version of the ID')
parser.add_argument("privatePassword", help="The private password")

args = parser.parse_args()

m = hashlib.sha256()
m.update(args.privatePassword.encode())
print(m.hexdigest())

with open("public_id", "w") as f:
    f.write(m.hexdigest())
