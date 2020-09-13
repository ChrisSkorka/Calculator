import re
import compiler.token_matcher

newline_token = [t for t in compiler.tokens.seperators if t['function'] == 'newline'][0]

class Tokenizer:

    def __init__(self, continuing=False):
        self.tokens = []
        self.source = []
        self.indent = None
        self.continuing = continuing

    def tokenizeBlock(self, string):
        lines = string.splitlines()
        for line in lines:
            self.tokenizeLine(line)

    def tokenizeLine(self, string):

        re_indent = re.search(r'\S', string)
        code_start_i = re_indent.start() if re_indent else 0
        indent_str = string[:code_start_i].replace('\t', '    ')
        code_str =  string[code_start_i:]
        
        self.source.append(indent_str + code_str)

        if len(code_str) == 0:
            return

        if self.indent == None and len(indent_str) > 0:
            self.indent = indent_str
            indent = indent_str.count(self.indent)
        else:
            indent = 0


        i = 0
        w = len(indent_str)
        l = len(self.source)-1

        self.tokens.append({**newline_token, 'indent': indent, 'ln': l, 'c': i})

        while i < len(code_str):
            
            if code_str[i] in ' \t':
                i += 1
                continue
            
            last_type = self.tokens[-1]['syntax_type']

            token_type_candidates_keys = []

            if len(self.tokens) <= 1 and self.continuing:
                token_type_candidates_keys += [
                    compiler.tokens.CONTINUING_INFIX,
                    compiler.tokens.CONTINUING_POSTFIX,
                ]

            if last_type in [
                    compiler.tokens.SEPERATORS,
                ]:
                token_type_candidates_keys += [
                    compiler.tokens.KEYWORD,
                    compiler.tokens.VALUE,
                    compiler.tokens.PREFIX,
                    compiler.tokens.SEPERATORS,
                    compiler.tokens.GROUP_OPEN,
                    compiler.tokens.GROUP_CLOSE,
                ]
            elif last_type in [
                    compiler.tokens.KEYWORD,
                ]:
                token_type_candidates_keys += [
                    compiler.tokens.KEYWORD,
                    compiler.tokens.VALUE,
                    compiler.tokens.PREFIX,
                    compiler.tokens.SEPERATORS,
                    compiler.tokens.GROUP_OPEN,
                    compiler.tokens.GROUP_CLOSE,
                ]
            elif last_type in [
                    compiler.tokens.VALUE,
                ]:
                token_type_candidates_keys += [
                    compiler.tokens.KEYWORD,
                    compiler.tokens.VALUE,
                    compiler.tokens.INFIX,
                    compiler.tokens.POSTFIX,
                    compiler.tokens.SEPERATORS,
                    compiler.tokens.GROUP_OPEN,
                    compiler.tokens.GROUP_CLOSE,
                ]
            elif last_type in [
                    compiler.tokens.GROUP_OPEN,
                ]:
                token_type_candidates_keys += [
                    compiler.tokens.KEYWORD,
                    compiler.tokens.VALUE,
                    compiler.tokens.PREFIX,
                    compiler.tokens.SEPERATORS,
                    compiler.tokens.GROUP_OPEN,
                    compiler.tokens.GROUP_CLOSE,
                ]
            elif last_type in [
                    compiler.tokens.GROUP_CLOSE,
                ]:
                token_type_candidates_keys += [
                    compiler.tokens.KEYWORD,
                    compiler.tokens.VALUE,
                    compiler.tokens.INFIX,
                    compiler.tokens.POSTFIX,
                    compiler.tokens.SEPERATORS,
                    compiler.tokens.GROUP_OPEN,
                    compiler.tokens.GROUP_CLOSE,
                ]
            elif last_type in [
                    compiler.tokens.INFIX,
                ]:
                token_type_candidates_keys += [
                    compiler.tokens.KEYWORD,
                    compiler.tokens.VALUE,
                    compiler.tokens.PREFIX,
                    compiler.tokens.GROUP_OPEN,
                ]
            elif last_type in [
                    compiler.tokens.PREFIX,
                ]:
                token_type_candidates_keys += [
                    compiler.tokens.KEYWORD,
                    compiler.tokens.VALUE,
                    compiler.tokens.PREFIX,
                    compiler.tokens.GROUP_OPEN,
                ]
            elif last_type in [
                    compiler.tokens.POSTFIX,
                ]:
                token_type_candidates_keys += [
                    compiler.tokens.KEYWORD,
                    compiler.tokens.VALUE,
                    compiler.tokens.INFIX,
                    compiler.tokens.POSTFIX,
                    compiler.tokens.SEPERATORS,
                    compiler.tokens.GROUP_OPEN,
                    compiler.tokens.GROUP_CLOSE,
                ]


            token_type_candidates = [compiler.token_matcher.token_matchers[k] for k in token_type_candidates_keys]
            token_matcher = compiler.token_matcher.FirstMatcher(token_type_candidates)
            token = token_matcher.match(code_str[i:])

            if token:
                if not token.get('non_code', False):
                    self.tokens.append({**token, 'ln': l, 'c': i})
                i += len(token['symbol'])
            else:
                raise Exception(f'Token not allowed Tokenizer.tokenizeLine() at ln={l}, c={i}\n{code_str[i:i+10]}')
            