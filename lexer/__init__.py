from .tokenclass import Token
import re

KEYWORDS = {
  'func': 'FUNCTION',
  'fun': 'FUNCTION',
  'if': 'IF',
  'else': 'ELSE',
  'true': 'BOOLEAN',
  'false': 'BOOLEAN',
  'while': 'WHILE',
  'for': 'FOR',
  'times': 'TIMES',
  'import': 'IMPORT'
}

def run(string):
    i = 0
    tokens = []
    tokens.append(Token('{', '{'))
    while i < len(string):
        char = string[i]
        if char == ' ' or char == '\t' or char == '\n':
            if char == '\n':
                tokens.append(Token('\n', '\n'))
            while i < len(string) and (string[i] == ' ' or string[i] == '\t' or string[i] == '\n'):
                i += 1
            continue

        if re.match(r'[0-9]', char):
            a = ''
            while i < len(string) and (re.match(r'[0-9]', string[i])):
                a += string[i]
                i += 1
            if i < len(string) and (string[i] == '.'):
                a += string[i]
                i += 1
                while re.match(r'[0-9]', string[i]):
                    a += string[i]
                    i += 1
                tokens.append(Token('NUMBER', float(a)))
            else:
                tokens.append(Token('NUMBER', int(a)))

            continue
        
        if char in ['\'', '"']:
            i += 1
            a = ''
            while i < len(string) and ((not (string[i] in ['\'', '"'] and string[i - 1] != '\\')) or string[i - 1] == '\n'):
                a += string[i]
                i += 1
            i += 1
            
            if a.endswith('\n'):
                raise SyntaxError('Error: Didn\'t close string.')

            a = a.replace('\\\'', '\'')
            a = a.replace('\\"', '"')
            a = a.replace('\\n', '\n')
            tokens.append(Token('STRING', a))
            continue

        if re.match(r'[a-zA-Z]', char):
            a = ''
            while i < len(string) and (re.match(r'[a-zA-Z]', string[i]) or re.match(r'[0-9]', string[i]) or string[i] == '_'):
                a += string[i]
                i += 1

            if (a in KEYWORDS):
                tokens.append(Token(KEYWORDS[a], a))
            else:
                tokens.append(Token('ID', a))
            continue

        if char == '/' and string[i + 1] == '/':
            while string[i] != '\n':
                i += 1
            continue

        if char == '/' and string[i + 1] == '*':
            while string[i - 2] != '*' or string[i - 1] != '/':
                i += 1
            continue

        if char == ':' and string[i + 1] == '=':
            i += 2
            tokens.append(Token(':=', ':='))
            continue

        if char == '=' and string[i + 1] == '=':
            i += 2
            tokens.append(Token('==', '=='))
            continue

        if char == '>' and string[i + 1] == '=':
            i += 2
            tokens.append(Token('>=', '>='))
            continue

        if char == '<' and string[i + 1] == '=':
            i += 2
            tokens.append(Token('<=', '<='))
            continue

        if char == '!' and string[i + 1] == '=':
            i += 2
            tokens.append(Token('!=', '!='))
            continue

        if char == '|' and string[i + 1] == '|':
            i += 2
            tokens.append(Token('||', '||'))
            continue

        if char == '&' and string[i + 1] == '&':
            i += 2
            tokens.append(Token('&&', '&&'))
            continue

        if char == '=':
            i += 1
            tokens.append(Token('=', '='))
            continue

        if char == '>':
            i += 1
            tokens.append(Token('>', '>'))
            continue

        if char == '<':
            i += 1
            tokens.append(Token('<', '<'))
            continue

        if char == '+':
            i += 1
            tokens.append(Token('+', '+'))
            continue

        if char == '-':
            i += 1
            tokens.append(Token('-', '-'))
            continue

        if char == '*':
            i += 1
            tokens.append(Token('*', '*'))
            continue

        if char == '/':
            i += 1
            tokens.append(Token('/', '/'))
            continue

        if char == '(':
            i += 1
            tokens.append(Token('(', '('))
            continue

        if char == ')':
            i += 1
            tokens.append(Token(')', ')'))
            continue

        if char == '[':
            i += 1
            tokens.append(Token('[', '['))
            continue

        if char == ']':
            i += 1
            tokens.append(Token(']', ']'))
            continue

        if char == '{':
            i += 1
            tokens.append(Token('{', '{'))
            continue

        if char == '}':
            i += 1
            tokens.append(Token('}', '}'))
            continue

        if char == '.':
            i += 1
            tokens.append(Token('.', '.'))
            continue

        if char == ',':
            i += 1
            tokens.append(Token(',', ','))
            continue

        if char == ':':
            i += 1
            tokens.append(Token(':', ':'))
            continue

        if char == ';':
            i += 1
            tokens.append(Token(';', ';'))
            continue
    tokens.append(Token('}', '}'))
    tokens.append(Token('None', None))
    return tokens
