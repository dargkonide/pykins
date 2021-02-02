import ast
import re
from uuid import uuid4

code_string = """
from time import time

t=time()


with node('tvsi-erib0054'):
    from time import time
    print(time()-t)
    with node('tvsi-erib0054'):
        from time import time
        print(time()-t)
        with node('tvsi-erib0054'):
            from time import time
            print(time()-t)
            with node('tvsi-erib0054'):
                from time import time
                print(time()-t)
                with node('tvsi-erib0054'):
                    from time import time
                    print(time()-t)
                    with node('tvsi-erib0054'):
                        from time import time
                        print(time()-t)
                        with node('tvsi-erib0054'):
                            from time import time
                            print(time()-t)
                            with node('tvsi-erib0054'):
                                from time import time
                                print(time()-t)
                                with node('tvsi-erib0054'):
                                    from time import time
                                    print(time()-t)
                                    print(1)

print(time()-t)
""".strip()

def get_var_name():
    x=str(uuid4())
    if x[0].isdigit():
        x='x'+x[1:]
    return x.replace('-','_')

code_split=code_string.split('\n')
code_ast = ast.parse(code_string)
with_nodes = [node for node in ast.walk(code_ast) if isinstance(node, ast.With)]

filtr=[]
nodes={}
for with_node in with_nodes:
    if re.match(r'.*with\s+node\s*\(',code_split[with_node.lineno-1]):
        for i,node in enumerate(ast.walk(with_node)):
            if i and isinstance(node, ast.With):
                filtr.append(node)
        start=with_node.lineno-1
        if hasattr(with_node,'end_lineno'):#in python3.8
            end=with_node.end_lineno
        else:
            end=max(n.lineno for n in ast.walk(with_node) if hasattr(n,'lineno'))

        print(end)
        nodes[with_node]=(start,end,code_split[start:end])
for n in filtr:
    if nodes.get(n):nodes.pop(n)

send_code_vars={}
mapping=[]
for k,v in nodes.items():
    start,end,code_list=v
    code='\n'.join(code_list)
    node=code.split(':')[0]
    index=node.index('with')
    if index>0:
        char=node[0]
        for i,n in enumerate(code_list):
            if n[:index]==char*index:
                code_list[i]=n[index:]
        code='\n'.join(code_list)
        node=code.split(':')[0]
    else:char=''

    send_code=[n for n in code.split(node)[1][1:].split('\n') if n.strip()]
    for i,n in enumerate(send_code):
        if not i:
            spaces=re.search(r'^\s*',n)[0]
        if spaces and n[:len(spaces)]==spaces:
            send_code[i]=n[len(spaces):]
        send_code[i]
    code_var=get_var_name()
    node_vars=re.findall(r"(node\s*\(.*)\)",node.replace('\n',''))[0]
    node=f'{index*char}{node_vars},{code_var})'
    mapping.append((start,end,node))
    send_code_vars[code_var]='\n'.join(send_code)

mapping.sort(key=lambda x:x[0])

i=0
new_code_split=[]
while i<len(code_split):
    continue_flag=False
    for start,end,node in mapping:
        if i in range(start,end):
            new_code_split.append(node)
            i=end
            continue_flag=True
            break
    if continue_flag:continue
    new_code_split.append(code_split[i])
    i+=1
for n in new_code_split:
    print(n)

for k,v in send_code_vars.items():
    print(k)
    print(v)
