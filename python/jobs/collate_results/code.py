import os

os.environ['ID']=str(test_id)
shell('''
    cd D:/auto/diff/collate/
    python D:/auto/diff/collate/core.py
''')