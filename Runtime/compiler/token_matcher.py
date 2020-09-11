import re
import compiler.tokens



class TokenMatcher:
    def __init__(self, token_definition):
        self.token_definition = token_definition

    def match(self, string):
        return None

class RegexMatcher(TokenMatcher):
    def __init__(self, token_definition):
        self.token_definition = token_definition
        self.re_pattern = token_definition['regex']

    def match(self, string):
        re_match = re.match(self.re_pattern, string)
        if re_match:
            return {**self.token_definition, 'symbol':re_match.group()}
        else:
            return None

class KeywordMatcher(TokenMatcher):
    def __init__(self, token_definition):
        self.token_definition = token_definition
        self.keyword = token_definition['symbol']
        self.length = len(self.keyword)
    
    def match(self, string):
        if string.startswith(self.keyword):
            return self.token_definition
        else:
            return None

class LongestMatcher(TokenMatcher):
    def __init__(self, matchers):
        self.matchers = matchers

    def match(self, string):
        max_match = None
        for matcher in self.matchers:
            candidate = matcher.match(string)
            if candidate:
                if not max_match or len(candidate['symbol']) > len(max_match['symbol']):
                    max_match = candidate

        return max_match

class FirstMatcher(TokenMatcher):
    def __init__(self, matchers):
        self.matchers = matchers
        
    def match(self, string):
        for matcher in self.matchers:
            candidate = matcher.match(string)
            if candidate:
                return candidate
        return None



value_matchers =                        FirstMatcher(  [  RegexMatcher(t) for t in compiler.tokens.values])
keyword_matchers =                      LongestMatcher([KeywordMatcher(t) for t in compiler.tokens.keywords])
infix_operator_matchers =               LongestMatcher([KeywordMatcher(t) for t in compiler.tokens.infix_operators])
continuing_infix_operator_matchers =    LongestMatcher([KeywordMatcher(t) for t in compiler.tokens.infix_operators if t.get('continuing', False)])
prefix_operator_matchers =              LongestMatcher([KeywordMatcher(t) for t in compiler.tokens.prefix_operators])
postfix_operator_matchers =             LongestMatcher([KeywordMatcher(t) for t in compiler.tokens.postfix_operators])
continuing_postfix_operator_matchers =  LongestMatcher([KeywordMatcher(t) for t in compiler.tokens.postfix_operators if t.get('continuing', False)])
sepperators_matchers =                  FirstMatcher(  [KeywordMatcher(t) for t in compiler.tokens.seperators])
group_open_matchers =                   FirstMatcher(  [KeywordMatcher(t) for t in compiler.tokens.group_open])
group_close_matchers =                  FirstMatcher(  [KeywordMatcher(t) for t in compiler.tokens.group_close])

token_matchers = {
    compiler.tokens.KEYWORD:            keyword_matchers, 
    compiler.tokens.VALUE:              value_matchers, 
    compiler.tokens.INFIX:              infix_operator_matchers, 
    compiler.tokens.CONTINUING_INFIX:   continuing_infix_operator_matchers, 
    compiler.tokens.PREFIX:             prefix_operator_matchers, 
    compiler.tokens.POSTFIX:            postfix_operator_matchers, 
    compiler.tokens.CONTINUING_POSTFIX: continuing_postfix_operator_matchers, 
    compiler.tokens.SEPERATORS:         sepperators_matchers, 
    compiler.tokens.GROUP_OPEN:         group_open_matchers, 
    compiler.tokens.GROUP_CLOSE:        group_close_matchers, 
}
