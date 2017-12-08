from yaml import load

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

with open('/run/secrets/common_secrets', 'r') as fp:
    secrets = load(fp, Loader=Loader)
