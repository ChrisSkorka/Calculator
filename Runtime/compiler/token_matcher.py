import re
import compiler.tokens_definition as tokens_definition



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

# select regex or keyword on a token by tokenbasis

value_matchers =                        FirstMatcher(  [RegexMatcher(t) if 'regex' in t else KeywordMatcher(t) for t in tokens_definition.values])
infix_operator_matchers =               LongestMatcher([RegexMatcher(t) if 'regex' in t else KeywordMatcher(t) for t in tokens_definition.infix_operators])
prefix_operator_matchers =              LongestMatcher([RegexMatcher(t) if 'regex' in t else KeywordMatcher(t) for t in tokens_definition.prefix_operators])
postfix_operator_matchers =             LongestMatcher([RegexMatcher(t) if 'regex' in t else KeywordMatcher(t) for t in tokens_definition.postfix_operators])
seperator_signals_matchers =            LongestMatcher([RegexMatcher(t) if 'regex' in t else KeywordMatcher(t) for t in tokens_definition.seperator_signals])
close_signals_matchers =                LongestMatcher([RegexMatcher(t) if 'regex' in t else KeywordMatcher(t) for t in tokens_definition.close_signals])

called_value_matchers =                 FirstMatcher(  [RegexMatcher(t) if 'regex' in t else KeywordMatcher(t) for t in tokens_definition.called_values])
called_prefix_operator_matchers =       LongestMatcher([RegexMatcher(t) if 'regex' in t else KeywordMatcher(t) for t in tokens_definition.called_prefix_operators])
continuing_infix_operator_matchers =    LongestMatcher([RegexMatcher(t) if 'regex' in t else KeywordMatcher(t) for t in tokens_definition.continuing_infix_operators])
continuing_postfix_operator_matchers =  LongestMatcher([RegexMatcher(t) if 'regex' in t else KeywordMatcher(t) for t in tokens_definition.continuing_postfix_operators])

token_matchers = {
    tokens_definition.VALUE:              value_matchers, 
    tokens_definition.INFIX:              infix_operator_matchers, 
    tokens_definition.PREFIX:             prefix_operator_matchers, 
    tokens_definition.POSTFIX:            postfix_operator_matchers, 
    tokens_definition.SEPERATOR:          seperator_signals_matchers, 
    tokens_definition.END_GROUP:          close_signals_matchers, 

    tokens_definition.CALLED_VALUE:       called_value_matchers, 
    tokens_definition.CALLED_PREFIX:      called_prefix_operator_matchers, 
    tokens_definition.CONTINUING_INFIX:   continuing_infix_operator_matchers, 
    tokens_definition.CONTINUING_POSTFIX: continuing_postfix_operator_matchers, 
}
