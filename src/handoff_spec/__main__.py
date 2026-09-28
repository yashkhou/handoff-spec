import json,sys
from .core import validate,digest
try:
 d=json.load(open(sys.argv[1])); validate(d); print(json.dumps({'valid':True,'sha256':digest(d)},indent=2))
except Exception as e: print(json.dumps({'valid':False,'error':str(e)},indent=2)); raise SystemExit(2)
