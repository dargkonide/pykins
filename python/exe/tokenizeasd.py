import tokenize
from io import BytesIO
from collections import deque
code_string = """
# A comment.
with foo(a, b):
  return a + b

class Bar(object):
  def __init__(self):

    self.my_list = [
        'a',
        'b',
    ]

  def test(self): pass
  def abc(self):
    '''multi-
    line token'''

def baz():
  return [
1,
  ]

class Baz(object):
  def hello(self, x):
    a = \
1
    return self.hello(
x - 1)

def my_type_annotated_function(
  my_long_argument_name: SomeLongArgumentTypeName
) -> SomeLongReturnTypeName:
  pass
  # unmatched parenthesis: (
""".strip()
file = BytesIO(code_string.encode())
tokens = deque(tokenize.tokenize(file.readline))
lines = []
while tokens:
    token = tokens.popleft()
    if token.type == tokenize.NAME and token.string == 'def':
        start_line, _ = token.start
        last_token = token
        while tokens:
            token = tokens.popleft()
            if token.type == tokenize.NEWLINE:
                break
            last_token = token
        if last_token.type == tokenize.OP and last_token.string == ':':
            indents = 0
            while tokens:
                token = tokens.popleft()
                if token.type == tokenize.NL:
                    continue
                if token.type == tokenize.INDENT:
                    indents += 1
                elif token.type == tokenize.DEDENT:
                    indents -= 1
                    if not indents:
                        break
                else:
                    last_token = token
        lines.append((start_line, last_token.end[0]))

x=code_string.split('\n')
for n in lines:
  print(x[n[0]:n[1]])