import os
import tempfile
import argparse
import json


parser = argparse.ArgumentParser()
parser.add_argument('--val')
parser.add_argument('--key')
args = parser.parse_args()
storage_path = os.path.join(tempfile.gettempdir(), 'storage.data')
try:
    with open(storage_path, 'r') as f:
        json_read = f.read()
        json_file = json.loads(json_read)
except:
    json_file = {}

if args.val:
    new_val = []
    if args.key in json_file:
        new_val.extend(json_file[args.key])
        new_val.append(args.val)
        json_file[args.key] = new_val
    else:
        new_val.append(args.val)
        json_file[args.key] = new_val
    with open(storage_path, 'w') as f:
        f.write(json.dumps(json_file))
else:
    if args.key in json_file:
        print(', '.join(json_file[args.key]))
    else:
        print('')

