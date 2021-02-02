from importlib import util
from uuid import uuid4


module_name=str(uuid4())
with open(f'{module_name}.py','w') as f:
    f.write("""
def node1(a):
    print(a)""")

spec=util.spec_from_file_location(module_name,f"{module_name}.py")
module=util.module_from_spec(spec)
spec.loader.exec_module(module)
print(module.node1)
