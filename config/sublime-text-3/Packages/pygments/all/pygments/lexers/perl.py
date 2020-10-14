# -*- coding: utf-8 -*-
"""
    pygments.lexers.perl
    ~~~~~~~~~~~~~~~~~~~~

    Lexers for Perl and related languages.

    :copyright: Copyright 2006-2015 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

import re

from pygments.lexer import RegexLexer, ExtendedRegexLexer, include, bygroups, \
    using, this, default, words
from pygments.token import Text, Comment, Operator, Keyword, Name, String, \
    Number, Punctuation
from pygments.util import shebang_matches

__all__ = ['PerlLexer', 'Perl6Lexer']


class PerlLexer(RegexLexer):
    """
    For `Perl <http://www.perl.org>`_ source code.
    """

    name = 'Perl'
    aliases = ['perl', 'pl']
    filenames = ['*.pl', '*.pm', '*.t']
    mimetypes = ['text/x-perl', 'application/x-perl']

    flags = re.DOTALL | re.MULTILINE
    # TODO: give this to a perl guy who knows how to parse perl...
    tokens = {
        'balanced-regex': [
            (r'/(\\\\|\\[^\\]|[^\\/])*/[egimosx]*', String.Regex, '#pop'),
            (r'!(\\\\|\\[^\\]|[^\\!])*![egimosx]*', String.Regex, '#pop'),
            (r'\\(\\\\|[^\\])*\\[egimosx]*', String.Regex, '#pop'),
            (r'\{(\\\\|\\[^\\]|[^\\}])*\}[egimosx]*', String.Regex, '#pop'),
            (r'<(\\\\|\\[^\\]|[^\\>])*>[egimosx]*', String.Regex, '#pop'),
            (r'\[(\\\\|\\[^\\]|[^\\\]])*\][egimosx]*', String.Regex, '#pop'),
            (r'\((\\\\|\\[^\\]|[^\\)])*\)[egimosx]*', String.Regex, '#pop'),
            (r'@(\\\\|\\[^\\]|[^\\@])*@[egimosx]*', String.Regex, '#pop'),
            (r'%(\\\\|\\[^\\]|[^\\%])*%[egimosx]*', String.Regex, '#pop'),
            (r'\$(\\\\|\\[^\\]|[^\\$])*\$[egimosx]*', String.Regex, '#pop'),
        ],
        'root': [
            (r'\A\#!.+?$', Comment.Hashbang),
            (r'\#.*?$', Comment.Single),
            (r'^=[a-zA-Z0-9]+\s+.*?\n=cut', Comment.Multiline),
            (words((
                'case', 'continue', 'do', 'else', 'elsif', 'for', 'foreach',
                'if', 'last', 'my', 'next', 'our', 'redo', 'reset', 'then',
                'unless', 'until', 'while', 'use', 'print', 'new', 'BEGIN',
                'CHECK', 'INIT', 'END', 'return'), suffix=r'\b'),
             Keyword),
            (r'(format)(\s+)(\w+)(\s*)(=)(\s*\n)',
             bygroups(Keyword, Text, Name, Text, Punctuation, Text), 'format'),
            (r'(eq|lt|gt|le|ge|ne|not|and|or|cmp)\b', Operator.Word),
            # common delimiters
            (r's/(\\\\|\\[^\\]|[^\\/])*/(\\\\|\\[^\\]|[^\\/])*/[egimosx]*',
                String.Regex),
            (r's!(\\\\|\\!|[^!])*!(\\\\|\\!|[^!])*![egimosx]*', String.Regex),
            (r's\\(\\\\|[^\\])*\\(\\\\|[^\\])*\\[egimosx]*', String.Regex),
            (r's@(\\\\|\\[^\\]|[^\\@])*@(\\\\|\\[^\\]|[^\\@])*@[egimosx]*',
                String.Regex),
            (r's%(\\\\|\\[^\\]|[^\\%])*%(\\\\|\\[^\\]|[^\\%])*%[egimosx]*',
                String.Regex),
            # balanced delimiters
            (r's\{(\\\\|\\[^\\]|[^\\}])*\}\s*', String.Regex, 'balanced-regex'),
            (r's<(\\\\|\\[^\\]|[^\\>])*>\s*', String.Regex, 'balanced-regex'),
            (r's\[(\\\\|\\[^\\]|[^\\\]])*\]\s*', String.Regex,
                'balanced-regex'),
            (r's\((\\\\|\\[^\\]|[^\\)])*\)\s*', String.Regex,
                'balanced-regex'),

            (r'm?/(\\\\|\\[^\\]|[^\\/\n])*/[gcimosx]*', String.Regex),
            (r'm(?=[/!\\{<\[(@%$])', String.Regex, 'balanced-regex'),
            (r'((?<==~)|(?<=\())\s*/(\\\\|\\[^\\]|[^\\/])*/[gcimosx]*',
                String.Regex),
            (r'\s+', Text),
            (words((
                'abs', 'accept', 'alarm', 'atan2', 'bind', 'binmode', 'bless', 'caller', 'chdir',
                'chmod', 'chomp', 'chop', 'chown', 'chr', 'chroot', 'close', 'closedir', 'connect',
                'continue', 'cos', 'crypt', 'dbmclose', 'dbmopen', 'defined', 'delete', 'die',
                'dump', 'each', 'endgrent', 'endhostent', 'endnetent', 'endprotoent',
                'endpwent', 'endservent', 'eof', 'eval', 'exec', 'exists', 'exit', 'exp', 'fcntl',
                'fileno', 'flock', 'fork', 'format', 'formline', 'getc', 'getgrent', 'getgrgid',
                'getgrnam', 'gethostbyaddr', 'gethostbyname', 'gethostent', 'getlogin',
                'getnetbyaddr', 'getnetbyname', 'getnetent', 'getpeername', 'getpgrp',
                'getppid', 'getpriority', 'getprotobyname', 'getprotobynumber',
                'getprotoent', 'getpwent', 'getpwnam', 'getpwuid', 'getservbyname',
                'getservbyport', 'getservent', 'getsockname', 'getsockopt', 'glob', 'gmtime',
                'goto', 'grep', 'hex', 'import', 'index', 'int', 'ioctl', 'join', 'keys', 'kill', 'last',
                'lc', 'lcfirst', 'length', 'link', 'listen', 'local', 'localtime', 'log', 'lstat',
                'map', 'mkdir', 'msgctl', 'msgget', 'msgrcv', 'msgsnd', 'my', 'next', 'no', 'oct', 'open',
                'opendir', 'ord', 'our', 'pack', 'package', 'pipe', 'pop', 'pos', 'printf',
                'prototype', 'push', 'quotemeta', 'rand', 'read', 'readdir',
                'readline', 'readlink', 'readpipe', 'recv', 'redo', 'ref', 'rename', 'require',
                'reverse', 'rewinddir', 'rindex', 'rmdir', 'scalar', 'seek', 'seekdir',
                'select', 'semctl', 'semget', 'semop', 'send', 'setgrent', 'sethostent', 'setnetent',
                'setpgrp', 'setpriority', 'setprotoent', 'setpwent', 'setservent',
                'setsockopt', 'shift', 'shmctl', 'shmget', 'shmread', 'shmwrite', 'shutdown',
                'sin', 'sleep', 'socket', 'socketpair', 'sort', 'splice', 'split', 'sprintf', 'sqrt',
                'srand', 'stat', 'study', 'substr', 'symlink', 'syscall', 'sysopen', 'sysread',
                'sysseek', 'system', 'syswrite', 'tell', 'telldir', 'tie', 'tied', 'time', 'times', 'tr',
                'truncate', 'uc', 'ucfirst', 'umask', 'undef', 'unlink', 'unpack', 'unshift', 'untie',
                'utime', 'values', 'vec', 'wait', 'waitpid', 'wantarray', 'warn', 'write'), suffix=r'\b'),
             Name.Builtin),
            (r'((__(DATA|DIE|WARN)__)|(STD(IN|OUT|ERR)))\b', Name.Builtin.Pseudo),
            (r'<<([\'"]?)([a-zA-Z_]\w*)\1;?\n.*?\n\2\n', String),
            (r'__END__', Comment.Preproc, 'end-part'),
            (r'\$\^[ADEFHILMOPSTWX]', Name.Variable.Global),
            (r"\$[\\\"\[\]'&`+*.,;=%~?@$!<>(^|/-](?!\w)", Name.Variable.Global),
            (r'[$@%#]+', Name.Variable, 'varname'),
            (r'0_?[0-7]+(_[0-7]+)*', Number.Oct),
            (r'0x[0-9A-Fa-f]+(_[0-9A-Fa-f]+)*', Number.Hex),
            (r'0b[01]+(_[01]+)*', Number.Bin),
            (r'(?i)(\d*(_\d*)*\.\d+(_\d*)*|\d+(_\d*)*\.\d+(_\d*)*)(e[+-]?\d+)?',
             Number.Float),
            (r'(?i)\d+(_\d*)*e[+-]?\d+(_\d*)*', Number.Float),
            (r'\d+(_\d+)*', Number.Integer),
            (r"'(\\\\|\\[^\\]|[^'\\])*'", String),
            (r'"(\\\\|\\[^\\]|[^"\\])*"', String),
            (r'`(\\\\|\\[^\\]|[^`\\])*`', String.Backtick),
            (r'<([^\s>]+)>', String.Regex),
            (r'(q|qq|qw|qr|qx)\{', String.Other, 'cb-string'),
            (r'(q|qq|qw|qr|qx)\(', String.Other, 'rb-string'),
            (r'(q|qq|qw|qr|qx)\[', String.Other, 'sb-string'),
            (r'(q|qq|qw|qr|qx)\<', String.Other, 'lt-string'),
            (r'(q|qq|qw|qr|qx)([\W_])(.|\n)*?\2', String.Other),
            (r'package\s+', Keyword, 'modulename'),
            (r'sub\s+', Keyword, 'funcname'),
            (r'(\[\]|\*\*|::|<<|>>|>=|<=>|<=|={3}|!=|=~|'
             r'!~|&&?|\|\||\.{1,3})', Operator),
            (r'[-+/*%=<>&^|!\\~]=?', Operator),
            (r'[()\[\]:;,<>/?{}]', Punctuation),  # yes, there's no shortage
                                                  # of punctuation in Perl!
            (r'(?=\w)', Name, 'name'),
        ],
        'format': [
            (r'\.\n', String.Interpol, '#pop'),
            (r'[^\n]*\n', String.Interpol),
        ],
        'varname': [
            (r'\s+', Text),
            (r'\{', Punctuation, '#pop'),    # hash syntax?
            (r'\)|,', Punctuation, '#pop'),  # argument specifier
            (r'\w+::', Name.Namespace),
            (r'[\w:]+', Name.Variable, '#pop'),
        ],
        'name': [
            (r'\w+::', Name.Namespace),
            (r'[\w:]+', Name, '#pop'),
            (r'[A-Z_]+(?=\W)', Name.Constant, '#pop'),
            (r'(?=\W)', Text, '#pop'),
        ],
        'modulename': [
            (r'[a-zA-Z_]\w*', Name.Namespace, '#pop')
        ],
        'funcname': [
            (r'[a-zA-Z_]\w*[!?]?', Name.Function),
            (r'\s+', Text),
            # argument declaration
            (r'(\([$@%]*\))(\s*)', bygroups(Punctuation, Text)),
            (r';', Punctuation, '#pop'),
            (r'.*?\{', Punctuation, '#pop'),
        ],
        'cb-string': [
            (r'\\[{}\\]', String.Other),
            (r'\\', String.Other),
            (r'\{', String.Other, 'cb-string'),
            (r'\}', String.Other, '#pop'),
            (r'[^{}\\]+', String.Other)
        ],
        'rb-string': [
            (r'\\[()\\]', String.Other),
            (r'\\', String.Other),
            (r'\(', String.Other, 'rb-string'),
            (r'\)', String.Other, '#pop'),
            (r'[^()]+', String.Other)
        ],
        'sb-string': [
            (r'\\[\[\]\\]', String.Other),
            (r'\\', String.Other),
            (r'\[', String.Other, 'sb-string'),
            (r'\]', String.Other, '#pop'),
            (r'[^\[\]]+', String.Other)
        ],
        'lt-string': [
            (r'\\[<>\\]', String.Other),
            (r'\\', String.Other),
            (r'\<', String.Other, 'lt-string'),
            (r'\>', String.Other, '#pop'),
            (r'[^<>]+', String.Other)
        ],
        'end-part': [
            (r'.+', Comment.Preproc, '#pop')
        ]
    }

    def analyse_text(text):
        if shebang_matches(text, r'perl'):
            return True
        if re.search('(?:my|our)\s+[$@%(]', text):
            return 0.9


class Perl6Lexer(ExtendedRegexLexer):
    """
    For `Perl 6 <http://www.perl6.org>`_ source code.

    .. versionadded:: 2.0
    """

    name = 'Perl6'
    aliases = ['perl6', 'pl6']
    filenames = ['*.pl', '*.pm', '*.nqp', '*.p6', '*.6pl', '*.p6l', '*.pl6',
                 '*.6pm', '*.p6m', '*.pm6', '*.t']
    mimetypes = ['text/x-perl6', 'application/x-perl6']
    flags = re.MULTILINE | re.DOTALL | re.UNICODE

    PERL6_IDENTIFIER_RANGE = "['\w:-]"

    PERL6_KEYWORDS = (
        'BEGIN', 'CATCH', 'CHECK', 'CONTROL', 'END', 'ENTER', 'FIRST', 'INIT',
        'KEEP', 'LAST', 'LEAVE', 'NEXT', 'POST', 'PRE', 'START', 'TEMP',
        'UNDO', 'as', 'assoc', 'async', 'augment', 'binary', 'break', 'but',
        'cached', 'category', 'class', 'constant', 'contend', 'continue',
        'copy', 'deep', 'default', 'defequiv', 'defer', 'die', 'do', 'else',
        'elsif', 'enum', 'equiv', 'exit', 'export', 'fail', 'fatal', 'for',
        'gather', 'given', 'goto', 'grammar', 'handles', 'has', 'if', 'inline',
        'irs', 'is', 'last', 'leave', 'let', 'lift', 'loop', 'looser', 'macro',
        'make', 'maybe', 'method', 'module', 'multi', 'my', 'next', 'of',
        'ofs', 'only', 'oo', 'ors', 'our', 'package', 'parsed', 'prec',
        'proto', 'readonly', 'redo', 'ref', 'regex', 'reparsed', 'repeat',
        'require', 'required', 'return', 'returns', 'role', 'rule', 'rw',
        'self', 'slang', 'state', 'sub', 'submethod', 'subset', 'supersede',
        'take', 'temp', 'tighter', 'token', 'trusts', 'try', 'unary',
        'unless', 'until', 'use', 'warn', 'when', 'where', 'while', 'will',
    )

    PERL6_BUILTINS = (
        'ACCEPTS', 'HOW', 'REJECTS', 'VAR', 'WHAT', 'WHENCE', 'WHERE', 'WHICH',
        'WHO', 'abs', 'acos', 'acosec', 'acosech', 'acosh', 'acotan', 'acotanh',
        'all', 'any', 'approx', 'arity', 'asec', 'asech', 'asin', 'asinh',
        'assuming', 'atan', 'atan2', 'atanh', 'attr', 'bless', 'body', 'by',
        'bytes', 'caller', 'callsame', 'callwith', 'can', 'capitalize', 'cat',
        'ceiling', 'chars', 'chmod', 'chomp', 'chop', 'chr', 'chroot',
        'circumfix', 'cis', 'classify', 'clone', 'close', 'cmp_ok', 'codes',
        'comb', 'connect', 'contains', 'context', 'cos', 'cosec', 'cosech',
        'cosh', 'cotan', 'cotanh', 'count', 'defined', 'delete', 'diag',
        'dies_ok', 'does', 'e', 'each', 'eager', 'elems', 'end', 'eof', 'eval',
        'eval_dies_ok', 'eval_elsewhere', 'eval_lives_ok', 'evalfile', 'exists',
        'exp', 'first', 'flip', 'floor', 'flunk', 'flush', 'fmt', 'force_todo',
        'fork', 'from', 'getc', 'gethost', 'getlogin', 'getpeername', 'getpw',
        'gmtime', 'graphs', 'grep', 'hints', 'hyper', 'im', 'index', 'infix',
        'invert', 'is_approx', 'is_deeply', 'isa', 'isa_ok', 'isnt', 'iterator',
        'join', 'key', 'keys', 'kill', 'kv', 'lastcall', 'lazy', 'lc', 'lcfirst',
        'like', 'lines', 'link', 'lives_ok', 'localtime', 'log', 'log10', 'map',
        'max', 'min', 'minmax', 'name', 'new', 'nextsame', 'nextwith', 'nfc',
        'nfd', 'nfkc', 'nfkd', 'nok_error', 'nonce', 'none', 'normalize', 'not',
        'nothing', 'ok', 'once', 'one', 'open', 'opendir', 'operator', 'ord',
        'p5chomp', 'p5chop', 'pack', 'pair', 'pairs', 'pass', 'perl', 'pi',
        'pick', 'plan', 'plan_ok', 'polar', 'pop', 'pos', 'postcircumfix',
        'postfix', 'pred', 'prefix', 'print', 'printf', 'push', 'quasi',
        'quotemeta', 'rand', 're', 'read', 'readdir', 'readline', 'reduce',
        'reverse', 'rewind', 'rewinddir', 'rindex', 'roots', 'round',
        'roundrobin', 'run', 'runinstead', 'sameaccent', 'samecase', 'say',
        'sec', 'sech', 'sech', 'seek', 'shape', 'shift', 'sign', 'signature',
        'sin', 'sinh', 'skip', 'skip_rest', 'sleep', 'slurp', 'sort', 'splice',
        'split', 'sprintf', 'sqrt', 'srand', 'strand', 'subst', 'substr', 'succ',
        'sum', 'symlink', 'tan', 'tanh', 'throws_ok', 'time', 'times', 'to',
        'todo', 'trim', 'trim_end', 'trim_start', 'true', 'truncate', 'uc',
        'ucfirst', 'undef', 'undefine', 'uniq', 'unlike', 'unlink', 'unpack',
        'unpolar', 'unshift', 'unwrap', 'use_ok', 'value', 'values', 'vec',
        'version_lt', 'void', 'wait', 'want', 'wrap', 'write', 'zip',
    )

    PERL6_BUILTIN_CLASSES = (
        'Abstraction', 'Any', 'AnyChar', 'Array', 'Associative', 'Bag', 'Bit',
        'Blob', 'Block', 'Bool', 'Buf', 'Byte', 'Callable', 'Capture', 'Char', 'Class',
        'Code', 'Codepoint', 'Comparator', 'Complex', 'Decreasing', 'Exception',
        'Failure', 'False', 'Grammar', 'Grapheme', 'Hash', 'IO', 'Increasing',
        'Int', 'Junction', 'KeyBag', 'KeyExtractor', 'KeyHash', 'KeySet',
        'KitchenSink', 'List', 'Macro', 'Mapping', 'Match', 'Matcher', 'Method',
        'Module', 'Num', 'Object', 'Ordered', 'Ordering', 'OrderingPair',
        'Package', 'Pair', 'Positional', 'Proxy', 'Range', 'Rat', 'Regex',
        'Role', 'Routine', 'Scalar', 'Seq', 'Set', 'Signature', 'Str', 'StrLen',
        'StrPos', 'Sub', 'Submethod', 'True', 'UInt', 'Undef', 'Version', 'Void',
        'Whatever', 'bit', 'bool', 'buf', 'buf1', 'buf16', 'buf2', 'buf32',
        'buf4', 'buf64', 'buf8', 'complex', 'int', 'int1', 'int16', 'int2',
        'int32', 'int4', 'int64', 'int8', 'num', 'rat', 'rat1', 'rat16', 'rat2',
        'rat32', 'rat4', 'rat64', 'rat8', 'uint', 'uint1', 'uint16', 'uint2',
        'uint32', 'uint4', 'uint64', 'uint8', 'utf16', 'utf32', 'utf8',
    )

    PERL6_OPERATORS = (
        'X', 'Z', 'after', 'also', 'and', 'andthen', 'before', 'cmp', 'div',
        'eq', 'eqv', 'extra', 'ff', 'fff', 'ge', 'gt', 'le', 'leg', 'lt', 'm',
        'mm', 'mod', 'ne', 'or', 'orelse', 'rx', 's', 'tr', 'x', 'xor', 'xx',
        '++', '--', '**', '!', '+', '-', '~', '?', '|', '||', '+^', '~^', '?^',
        '^', '*', '/', '%', '%%', '+&', '+<', '+>', '~&', '~<', '~>', '?&',
        'gcd', 'lcm', '+', '-', '+|', '+^', '~|', '~^', '?|', '?^',
        '~', '&', '^', 'but', 'does', '<=>', '..', '..^', '^..', '^..^',
        '!=', '==', '<', '<=', '>', '>=', '~~', '===', '!eqv',
        '&&', '||', '^^', '//', 'min', 'max', '??', '!!', 'ff', 'fff', 'so',
        'not', '<==', '==>', '<<==', '==>>',
    )

    # Perl 6 has a *lot* of possible bracketing characters
    # this list was lifted fro ¹ß5cT@Êüëû?¶Ë%İuÂ[ñÜoÈ†zÔû·©‡Lnîà˜HÁÅ•Œ9¿îzÕÌîóÇÃGÂã—å~¶û‘Şòî§êÀ˜™î'­«É‡ûYî§î«ë.CÉıùùµ?Ş ÛxPà§¦IŞg¯Ó{§*¥ÿóù80o‚÷ü“ˆI!´uŠC¬ySG _åLáúóiO›ºîŒ\OtıHC¼`æpx…ë$7ÂõCC®®é†r9¦±gŸö]U×A`´Ó÷;¿8 ôÚƒ¤-¹ıUsxÜU®Wíß3(÷¢‹vî©k’qM3*ÚÒœ‡ó#®;)j[,B,}SM<_€«šp¡‚ÏXû:@“Åhó#q˜¿šƒ€¤ù«Ç°“#ıS/.}SËDv~ş:?Ãù	'Å¦œŸv>Ò{­Éß–˜x
Uàúşp~ÊùUruM7ÔWaGX?àæÓÄ¼îŒÌ6~ŞïüŒ9hä\1HÊ˜CîÏÃã.omÇomGtÃ@7<¿t_;î³‘•ÄJ°`VAÌŠîòk N ‹W*×½©eœ¯ªö0¿Ã|lUtyßí}¤·xïœ®Ï&ì´~úÚğŸh >ŸIXrå={|.¹¢ı·¢-Ú ÁÖlZÓÔÍmé½X[š¯ÀÈşƒ¤İÔc9äêšn¨¯º¶0¾ÁxÚ?Ğèª«Ëê$´aü(‚‘ÆËÌÁÆ8(=OC*×½©eœ/ÀÆWT°³š{r­¬Õ„Š¶v…ï}90a¥ñıƒ”ŒXeıˆkß”3’­o¿Ö—°¾ –ÛAWd}±õ‘Ş‹Xß»CZ¯¦í´¾ÖYß§C®®»õUÙRnv_wF”†Tò~'gÁHëû;P'EX·äë•bUëoUs4BF=ù˜4<ŒYİ	‘Şke´‚®ü¶Bf9õ\5¶J>Z!«º#.~SÍL_EMá=piƒI;iòVé-Ÿø{ªS&áµ$eÊ¤İ´‡\ı¦œ¡¾1Ã{å¾xmd4 På80›†ıu€‰
pq%Nòú6»üiöséäÃ§ç¦:um8¡%¤¬KáıÎHŠ7%<HŠ´’£šÂã®q½jÿ¾˜ëcLÜ*vÏı/"ÎLI£0Şòn×âÀ˜‹n×ƒ¤Œ¹T×½1lq0|äåÚæßÚ®Ğğ›~.şá(fEX*k¶‚@¦ùÚmôıV22Ô¶X„-]e]FúªìŒàá­]ÎI#)#y<q¥;0¦#…Ï¯¿?`ªÊtÈÕ5İP_˜csÀPn·5ÀpDú~çgÆl m…2j€RwåëUcüú?Âß2H2\éj€îˆ4ÖBäé ˜ÙyÅ )3wu@qÄÅoª™é«²=€'¸[3|èE”~?EòMó˜²³ò;H*(õŠÊÃa‹wnn—¡¾0[4 ßG9ëÚ°!'ÂtzË7liÙŸMÙ¸Aåƒ”Lé5‡-Şaù2’ìÇ¹ÿÿ[dÀ&€$<ˆUşWûéû?3aÓŒARf®ò?}wëU;*[£x”KØ[|¨j€êˆ4äÑ )cV:Ÿj’
L5@ê¹úM9C¹¶ë·¶%ÚG¹‹ûFéÄ}Fàêó^ãy@Kûçóq`Ö‚Z>ï—ı…Ğ†Š+jºA¾êYÂöçÓ7tmxÊ“Æø¤§BÈc¢x_B®6b¡ E)…\ú¦˜‰¾s3ã~ÜŸy\ûf–ç¹˜ÑéûŸ˜O;„<H*0‹0›Ãã®|½jôü/ûiš†N0s¿ÚÛ~7tRÒHèHßçüÛ2„ÆƒÄ/ïÿ!·7Íë;J›ÂşûW×µ=2»Y8ŠÒéGÓPó]šrû*N*û«á‹jºY\ÑñgEáXñißEâ¨"V·A¤±XÅL&0>ŞÔñ ¥`V¬â‹cúe¤£ (´ lœ¼böê„\¶=Ò÷;80å¢ƒó$eÊ%Ûq ³K¾k\¯+Û+»‚¨Ös0j L…ìô}L¿¥!`®\cy§:av‡çM!uu†óÎ³R ‘ïÓ¾;eüñq`@£ùºSùàËâ‹ß3ÏáÛà¶ÑšÑÈøŒdŒô–×ÌîÀƒ[è1HÊ˜Û_-‡\ı¦œ¡l{ûµ}ä€Æ£4°¯xĞe|·ñ‘Æb˜(™k—¤câ.ãõË;Œ|úF¾LôUØ^ÍØáæsJäug²³#}¿ó—Svº¿¯$˜ò8:nZ×+ÆºÖßº¶h††fè]×ÑĞ¼ô¡p/ÖPØŞ˜¹±´½Ç°“G345C¹úM9C}•6*<S-Ğ±ÅU™_m~¤·x¥şlÆª‚ævr¾ŒÏg2V‡X³/ñ|Öğ¾ÂKV³Áƒ*ï«½4´‹æ+Fö¦
ãïï«¼o‡\ÓÇe(›_~Í/a>q­éº3Ú	Šw‚HïÅ
ÌoÕ¡Ío,•¿?Ì/2_MT(:=İP_µ-A‰EqÁÍò>ÛûHoíïëÇ3Ío¾JÈ„YO~‹+ßÔ‹š‹š£2:¡¢Tì ¬NÈî„Hßïüî €éi1H*Õ	júÌ*è®~½jGQÓ0f" Š[aA’÷ÉŞGú>çß–!f_‰ARÆLò¾6‡_w½j/¦÷‚å£k«ûD40Ò÷8s9  >j®IPrÆ‘ú¸ì8\ÿÓôÊ“Úú´ïÀ6úÌÜ™,X›i¬‚ºã±ª<
–eÔPø_‹R+ÓËtÈÕoÊê¨fİZa.˜Èÿ£JÙ³W#æ²é‘¾ßùşlÊE÷ôOQÑ÷í¥\ò¼T‡Ç]×+v@Î!'ŒÌK×‘ñÓÆGú~çG`ÊIÇóŠAR¦œ2>w9ÿûç·f4 Orüo.ãçšÙÈJb%¸Ÿ«ƒ ¦ûú/.ÓƒX¼]×½©eœ¯ª°§88ŸÑ4CÎÇ¡/Ò[| •ÓÇ;3û*!úÈ—‹C.}SÌD.éú-i>àAŠûNÂíªiwQ#½ëKó¹³´åøû£¬]uMË!WÇô~ê«°½&ÌLU×¥!£û\#O5ê¢›¢ã–r½R`ç÷‘MÛãÚ*ñ|ú¼uŸ×ó¹˜n¿¶‹vRÒ1´´›5Ô çAh™ÅÏ_Ïkx¾OnÏ]äÀ†YqŸqãé½ØóîÛ©æÀÄûH!’21äJ¼<*EõÛe¨¯’Öğ|¿6±ùlÙ;#JC*	í¬É
‚1sµw N ŠP*×Õ\ã¸ªy;•nÜ‚z®¥ëÎˆ·8Ò÷;:0qa9×ŠARF.b^‡Ç]ózÕªæ0?Ãüçe±¯èñ,ó³Íô–ÏüAÕ1³øZ’2f–ùk8äê7ååÚößÚæh…ŒV 	lI2?£˜ÆZh†A0³DNÌ­dd¨í¯ŠC®}SÍH_•MÑ 	†>/¸â×\R$7@¤!æp`ÊÄ’îo‰÷o: ıOv™]¹Ã@4'À9ÜIçôòÿ±HjÿˆLn£`™­XÛ!«'ÊêYÏ;˜¸«ü)Åõd0 X…étº÷WÄÄ­öz‘1%w>êOÕÏ­Æè òÌöOw×S³»Î£ûKæíp¥àÿÜ™şÏo,R2òÖ ¬Y;QÎH¯ÎîaÈ˜¼â¯İU”U”‘†<`vÆÔwjX$˜•˜s9dõD9C¹³í·³+ÆaÁŞYu=Ãò8Ì¦ğã|ÏâÀĞ×Yc‘”¡—Æa6‡¬(g¨WoW	LX: ;`ËÔLO@¤Ó½9LÀØ±HÊ˜S#0¾O­Ï­öÀœ14ÀØë•v2M˜~Dò]ûsrÆ½œäc¦F`L‡¬ííc(@ı# ®â#†&`x"}jÅíº7òà _OjÜÀc¸:deî6Ï«­#Üp³/]¯L—ûİîGêØ(Ü›ğ£^¤cÄ.ëûvÈÒ‰b&rOËoOñ¯ì?İUÓÎ_É®wA÷» ÒéŞ™;' ·X$Ğ„Ş>rğ§±-¬çÑBà´AÊ6L©èˆ7Ğ¶C6¶T'»FÚÃü&ó{„¬(g¤7d¸Ï³]›º^™*÷«İ4ä±QÈ7äG½œöÍxİƒ±-‡,(f"»ÿk~ó+ÌäùµÁƒ*ó«Í4j‘¸80rsERÁ,ó[sÈê‰r†zõµ„ù<ÚU^1ìEî»é#_`]ŒYhİ±HÊ˜Eö7G,¨f¦7e¸ÏÃ[ZñhŞ¤ÌÛ”NCUêfdµ‹tŒ˜å~Y:QÌDroŸ?öç°Ÿ»Zt=ÙŸm?Êt4Ãş¸7r¦ûµÄ"¥`–ûš¢LMı‰#=ÚZÎb€Äİµ–^í?˜•‘N÷şé€”¸Mò")RJj
OÍÏ­ÆÎî¿-<ÁıÓİy
ı*ı<»7¡·g!Ò(¦í¼dÖn±HÇÄ[³P†C–Æöú1Ñ«±»›‘§ºÌÒ`)B,FTñ¦İ
Ì¸I—¿±H) ‹ #dmm7Òr…û<Åe¼Ró:»—Ü_v?ÒG~qgÆ\|æ{‘”1—ÜÏË!«'ÊÊî¯_÷of à¥zşå)çDµ
ÙéÛEq³rE:Ş9å}nï‡Ê'¤Máü9Ìñÿ¥ë
¦¬Ÿ´ş‘†xÓ~f<gC}ğøüáı¤÷¾gií5‘;:;:¢¥ç(WÏW’×“é$¾V;}Š]'À“ŠÀÄçd¨øH’”‰!Wõ?%BV×S†z5v%Š]¯D—ñ}Òé#~½œOÊ÷f<GÃªÿ¹HÉŒP«ü!jc÷G<îêÏÏ9g3ñvøºÑ[¾<ºæ {"îıÓAsöŠERA\H¼¿OÍÏ­öèj›Æl0s³8<h2¿ÙüH§{u`ÌFów‹ERÆl2‡§êçV{b%Šòr…uñZ…Xé
ë××+½ß¾JÈ€£–BNÔ­ï¿Ö× ­À]èÔ‚L•õÕÖG¥*v\Y}Æ"©@–õk9dõD9C½zZÂúB@ÇK³Èúbë#û“eˆYÄWc‘”1‹¬_İáã©ò¹ÕØÛöÛÛü5t†¹³0aKÖ0dC¤Ós²¡3‡aîX$eè¬qX^İbÖæ˜€Œ	˜xgÍó¢ù€*z?»ƒ€c+çˆåñ…'ÖÄ4|X+QÅ¨|^¶€ÂİÙ‡Wè¼¾qù¼t³V¡9ÎB|ß·‰:^¤D>©QL!‹cûÇHv»şu;Ÿ7™7ÜãÔØçÙ½ˆ¼ív¤Ós²™7Óo?_7ó–ÛãëğõÔ­öèì®	G×õdDiH%Ó½¹9Fš>hç û(Â¡èõÈ-Å®–ß®®¾™/'n¤½Vá*:…öõ¯ã.A\¥cZhO"dáD1ó¼:Ã÷	;8;Ú?åû´ï‘>ò|ôáÀúz÷‹¤Œ9å{ßY=QÎPoÌğ}ÂJşrwü…S”†TÚøâõê ùEÒ/¶? Š°+b]í5}ÿµ}Ó8Ù¾ºŒŒ6>ÒéŞ¿xĞóöER&ò¾;z<´?·Ø£§=¬çÁ­±6şÚ.ë»­ô‘ï°¾u¦ì´¾XNòÑ×®Æ¶éÕåõÆë;¬oğ´Á½Kı*uÚE›#­o÷B@aSÄºØû1œoß_ë[XÏvÖ­ëÉÈúfë#}J5¼Êêr`àÆ³}eoıùÃú&ëë×!«k»¡^M­Û˜dq|ûª¾PÕß¨H§{s`LóõX$eÌ*ïëpøxª}n5övÿö¶Æ$ğôÆKÁ£B6±’(T¸W÷ÁË¨¾^©ò½i¯{ÒFÈ²gwšZÂûïyx+° Èûbï#ù®ı
YØMÛüùÃû"ïËvÈêÚn¨fï3¼,M×“‘÷ÙŞGúÈg
Ju`ÌÌßø¢öğoÊï³¼/İ!«ë)CÙûõë}ïy€ã³|Ú÷¿ïùr³"”‚ûy;dÚ¯ÓåY¤„O¬vÄ"díD9#İ=›8 ¼;ûxài¢ô Dò€Ü “·‰B^$˜€cCVO”3”;;ÿtöú|oCoŒƒú[Ï³{z{"}ŠmŒƒ@ö
èÍqp³ôù¼¡·Æ!7‡¬®í†zõv—À¼,-ÿ}·®Wfi'à‘N÷şå 0Ï`¯Irç£¯ÃÇSës«±·ã··+âé
lÆõdª «¡‡BãÎæÀĞçÿ9Jx‘T@WA‡¬(g¨WogŒÀdWqS0§)>ê×ÙíJí¯S#"tt•!v>©Y:QÌDoÆğÂÏ½t½2CşûiÈc£€oÄ6¦ûÓñ0Èü½²´¶›Èæÿ=Gº‰ÌÜW˜?dş°ù‘N÷şÌ<èún±H* eşîO9øÓØæw˜¿à>¾@}òZE©èˆ÷¥İ
ÙÙÒõEJ†„Ä±4vï‰ÜØöÛØ£Ğ1
ün-˜Ò4
Í£iÓvŞ1kX¤cà¦QXË!Kk»‰^]ma~cÑªëÉÈüfó#yŒÉ*LÙèúy?h‘T`ÊüÕ²z¢œ¡^˜u³ÂN~ÿ'şÂ*÷«İtº÷/Æ¬´_ßæI“ëÃş*ûç×áã©õ¹Õèıõ¿†ÿşOtxB¨lB_« F1llºdÖî±HÇÄĞ:M‡,(f¢WcKø_HWt=ù_ì¤!ÿ§ïYh¿Ş@úøá~‘û³:dmî6‘»Z~»šc2¬¾ŒF!{"}je¼aÇt`äÌwìX±HÊÌY£0¶CVO”3Ô³±bDA4êz¡µ}~½³V:´m1+´X¤@.©œ†C?rºú&Ú<®ıÓİµ©³ êac)‚,øÏ›Ùp›(ãEJW„!k'ÊÉ^ÿµzó¬öOwç¡©ëÉ"o[éSksgfŞ´ú²Ë%Kv¢[Éğùãõ(÷?nK!på À²tSmªqâzßÌ‹RÛ×&ª3\P¯Æ® ô¢şğ¶j±“rOÉnK/XË2ÉOR+11• 'uoU¦OÈF"¶µÜ¿}UÄÓµ­nß‹eoà‹3ÃÎø¤4DÆ^¨+&¦
dî…zË<îšŸíè«Ÿé¾¼²8ß¶ÕU˜ÏLL¹ÓŸ”˜ºóc£õ¶1=-™¯»v¶3(½hæø8:åï’?Ü–¼»üU×bìP¿æ˜˜IŒê×"Ók{ô‡<ıŠßC|¼˜ğ,¥Sü.ñÃí•|g—!#ˆ±Qùm,xrú!~§øeÉDõ„t‚zuµE[ñÔÀºâ7‰îtÆ'¥&úRcb*a6Š_ºÌ×];Û©7½_Y³)~•øò¦Î·1òı÷dÎ¹Ÿk0†ùºkgƒşóWÿúã—GóPÿ*ıÃíÅüÇå.# ¡11U@Sÿ<e¢zB:A½[Bÿ@w
õ/Ò?Ü–¾ø1;gÂ,88çS	³PÿÜd¢zB:A©·ã··9vCv/±^®K€Î“ĞáN;>As'\+&¦tæ†ë¸IÆŸÖú¹îË+‹ëÍÃµÂv|“”èé…kıØ™;à2»ÚggCkûok¯Ø8Æ]ş½ü¡º¸.í‡p[1ÿyº±PsLæ¬›ø¹q‘‰ÒOøG8GWç¿›ÚûU¹şİÓÇç:íúâl€‡;Ù´OŒ~™¸p¬‡öL‡l4QİÃÇGPoÌ˜ÅËV›G“RtzîÌ`Á˜Q­Æ„<HÂNu+ÉŞşÊ>qvûòÊîÂ`víjÂ¥e…sÛãY·áÚñĞCÓ±Ü6®'³€0Q™ázut†ğÓé º\ŒIá§„·¥Ÿ.üê2D9!¼ê¬ÂO
¿¦LTOH'(õõçhı¬Ç6˜¾F×DÌB¦3ÁI9HM×'€ÉÛh½nÙ©®.ÀáZ¢·Ó5„£1Ü–ı9´™kÉ£¹p¬×ééIŠ3ZL/ÊÚwğuæa»nKß]ûÙdˆ²¯ÇÄT¢ììå2Q=! ¤}ùÕ¾‡öİåœşlO¢“YÈtz%„é:€ñ˜{Bšà%n¥…²ûÌ«§-”oŞÍá/Òá
4*ß¤|¸Ó2„ØĞÌ1cb*16*?n™Ç]ã³³¡§ù·§u	ºº°Ø„Ãõ¨ĞÏLh¹Ó¯2]±¸kµ>6´§³¥.ó¸«~v¶£·5¤¯.½¿ªFö`BŠ‘NOíÊ÷[F Bó¡Y‚x²P4!“X^t%”/®dw<ìğB¾"Àp[öÒOC„İë#&¦d!e_2QİÃûGPRşWøÂgT÷<™Âg	n«•'ãiˆ9c›ò!Ñú!|¦ğ½ÉDu†êÕZ?×}yõÄµ›ãã¹øİ¿ôáwÚñKF`Bü†7×¯ãÓñÛße7­ÏNæõSêŸÖ^±.ßx¼›ÿÜ‹ÛáÒv·kŒ§!æÛO¶Öípq;´!Õ=¼}u´vàÄöå•Å¡aÃNagbÊlšŒ§Ì¡_Ë110™Î–ªLTg¸ Ş˜90ïg|<ëæÒ·§÷ÀÉë€ôjuÆÄ<b\”¿Ş2Qšá"’şë¯ş'¼/¯ì.æ)$."–;íø*CÌú×=1U@Bw™Ç]õ³³¡?Îs~ ®®Âì œú†Û²O—¿Ü2D9ÙSL$ÆÉ/j-2Q:!™ˆŞŒ!>>öer|<ƒâ‰nOïƒ×øa`Ú«ãPü²d¢4ÃE$ñç¯ø#ÄÇ§´Tæ¡øCâ‡Û‹!214´pâú!ş ø¥ÉDu†êÕX?ä}yõÄå›£yøğw=ü…VÚáK†(;zšï˜ÌyÈß)‘uÜ´>;:;~;Ûc/àD—ıµš]•¶€üÌ@·óÀÆë Fí=1€=—-M™(LD¯¶¶P¿¹úøeo`£úMê‡ÛÓWÆÓeƒìü iıP¿Qı\e¢:Ã¥ÆößÆÖØÕÅ½GóğMPõ&·«~Ğ¹¦AWœ[.<ÜZ?6Cåf¸n™¨ÎpA½z[ƒÒ‹z/¿±ğMPô&w:ÂsµZLvÃ¡~¡úW—¹oªŸHuğ•ĞŞOu^Õû_(|‘ğáöÌÆ§+ÑáaÇŸ™ù Ë+2QÑbE!±Û¯Ø9Ä~®òmßlŒæ¡ØÙÅ>İVéy¤Ì5dˆÕ…\À-‰©DìéliÉDuŞ%¨W3ãYÏ^´r|õk	RnKşl(s‚´†XML%HOgKM¦OÈF"õµşöõŠíy9ìˆ£Qÿ«ˆ˜V:£“’¤ë‰™¸8Ì×];[tµã¬öå•Åæqñ}e¸“Mˆ˜]ª/N\oÂôkÇ\S&ª3\PoÌ ô¢…ããXKâ‡Û’£ç+Ë¤šX0q}mÈEñW•éÅM"‰ÿóÏT·ûH¼\Îç ƒÑ<™È™Èó¦é¥üÇÍ)#ÁjÇ#NLÈÈó–‰ê	éõêëù§Ë?›®ÂlÀœM˜r[úéòÏ*C˜º['¦æ¤üÕÒ	J½Í¿½±†Ë;3Góp;m‡p§¯k1;ñpsùØƒ›a™ÇMŸëhìı‡ë?&GóPÿ!ıÃíÙ]ÿ1d$ôè”Öıõ×oÅ¯
ÔÓv_^Y`]“Nı»ôw:ã“Ò ³CÕåú¡§ş£É<î*ŸúÿÊßÙºKê?¯M ?3iYv3š†xdì{b&ñz6K¦—f4y^Mm¡}óv¢U4Ô¾Iûp{r×¾w	í;ËBûvhß¨}Ÿ2Qw	ŠMõ¯àŸ®ÖØ	¸…£y¸ªvB¸­X…Y† +iKLL%èÊĞ«LTOH'¨WoK<ûÅmş^m.D¡şEú‡;ñIi€Y |[11•07@—õºi'Ck×okKì‡âû¡uæ!²ˆéôJ®@k2m-&ä	^à¶Au+œWSsh]ËÍCí³´·eÏø)ºb†ô-ÇÄLbÌ”¾™(îá!½ ¯P'º:9š‡Ê_R¾.š–ıò=R‡Q^¼Î˜˜J”•¯K&ª'¤Ô³¦ëWGüß¤£i‡UA™+dÆz ‘Ë3|àúÙI°çßıØp®ûòÊîÂ`¶mÌÄ¤•"Øÿ…bõK„¦c¹
•É, Ì}Ó¾“ı·×-DœàÊàh	È%±Ãmé—‹]ºQ.ˆ]°Ç´>7æ¢ØeÊDu†J}¿}]% ]S<ÀÅï"³éôJ™Á4‚Ow­Àä­´P×cóG8¯®Î~º–Ù{•]ƒIé§¤w:ã“Ò€qBÆ¼bb*ANŠ_d½nÚÉĞÔşÛT?Ğ}yewùó”]1ÀüÌd–;ñIiÀ<Ûbb*1{:[2ÿ'»\²$Wa º•Ü uøƒ7ôF¹ÿñ³2î4 !K·ØE¾z²­¡=îo¥p4)I§çF˜ÖéË3!M°ÒBYıæ…7BùáJfÿxfW`Pù!åÃmÉGg<!´/¯˜˜JŒƒÊçK&ª3\P’¾ÿJßCzü•Ï£yØÔ®®†;=ñM† ùG>ã[•!}?ÛÙÙ<d¾z²½õ+İ—«bŸ+‹k ïÙ¹NÛWAçrã3ˆË³C˜Š÷DO4³ı6³Å	°ûÚıÔäh€†p»M/Ö=rÈ®ÿeòš˜*(ıx6š¨NP¯fÖĞü^Y\ãhj^§0å¶ô÷wÛ\U†0í{Øtìš{:Ûê2Qá‚zc†æÕÅ´¿R>ŞBåËEÌp{zÜ\ä‡éÙ-‡şËxd¡2£$ùë¯ü~ûreOæ¡üEò‡;=ñ]†äßĞSûõ`®`ŞSæñTÿ<Ù¾æ?»üİõG3åÏ’?Ü–>/ÆÓf†ü»ÄÄTÂÌ”W™¨îá1©µ?¿Gû_³v9ÉºŸmönfÎ`wÂkµüİ­]+&f *³ØÖ%E.–££ÍNµÓùÊâ4š§’®ŠNnOï¯_ n†ÆØô&-Òr¿˜ŞşÎÃDu†ê…é—º/W‡Áì	È-ÙåM</bÜì¡Fæá¦æ+Ìç™;Ù“ËEÿWò†[Ú—+{Æ?¦ÓÉ%_’<Ü^ŠáX.*Ï˜˜G¼‹ÂÛ%&J3\D¯®’ÏÆÑ<~Iøp{zD†!Êá'>VÂ¯CøEág—‰ê|JPhkñwãŸÆÎ8Ó•Gó@ÏAèp[1H0¶A³©ãŠ‰©íéPŠ'dÓ«µ3äŸ.ÿoÏ üCòIÓÓ{`ç:QmÄÄ<B”L™(LDêëşíëˆÃ0ü0ŒÊÑ<<C‡!Ü^ÌÃ(2Ä<pƒöÃ0xF“‰êÔ«±=äï.ßÍCù»ä·¥ïŞÙ¾d³£·o˜öù;åï—LTg¸ Ş˜AéE5Ş¶Ù¶ MKŞü4÷&C‡³÷˜˜JÙhzñ„l$z!¶`ÄßŞöF½›ô·çv½Û%#¡w×ÈDAHµ{˜(LD:¢ë÷ˆÖĞ7¹¦Ñ<Ô¾Jûp[±êÚ·)CÈÚ7ˆ©ıCûJí)Ou­j„êÕØ”^´q¼…ÚinK^\{6¹<ÚhÏöjÿĞ¾PûÖezqF“H}¿}õÛİ—«û¡zq4O!r!r¸Ó¿e2XëSr!²¬ã¡ıy’mÍ¡>.rÕ?©ÕEÈT?Kıp[ú<OC”ê×S‰2Sıºd¢:Ã¥ÖŸÖ’ØËW­şù÷3qåN6¡ıEp}™¸GS—él«Éä™©Ößw?+îk_®î ²9š§Pª‡Ûû¥,ˆ3WvLL€Tİè¸‰ê	éõÂôËİ—+‹ëÍÓyÏÄ”;=ñM†07dçïŒÂàş`z:Û2§ÚçÉÙû¿²×¿ÌP8ŞEé—¤·•Z.}ÑZÄÊ(ÏíCøEáK•é¥LœWSWh›Ş¨ì,j¿¤}¸=·kï¿¨*.‰D„ö|9´h¿¨}Ş2Qá‚RSÛoSgœÜärãh„©“;M+6ıS‘«AO¼ù¹ÅÄT‚<	¹ËDõ„t‚zõÖ¯w_®ÊÂël¡cñ‘ëôDnô;éÂ›‰yè¹ø¦×IìÏ“ê¤åíÚvÇMæ¡òÊnO_=rÈÆúal:öå=m-™¨ÎpAIùŸS·µ/WöTåh*ß» å¶b÷uÈ\E† íš„ØtìÊ{:Ûj2Qá‚zõ¶…òÍõÜ›£y(~[Ä·¥oˆC˜ví@¬&¦¦§³­K&ª'¤”z[~{Ûj@{Wï¯®Kãh:áNg|RB£©¶qìÌD´^<©ÆÖĞ¿ºş÷OYŒæ¡şUú‡Û²W×k-Ä
ùw‰‰™ÄX)ÿ®2QÜÃ?BzA–P¿¸úkq4Õ/R?Ü–½¸úkÊeìkÅÄT¢,TŸ=ğ'´@ı5?‚’ú¿â—¿¸˜«q4‘EL§òş¯*#€ÑÏÕbBà%n§…º	¹„ójª_ì¾\Y³©{–îò¦—fè>¯˜ÌyœÍÌÃ¹Â|=õdóîŸ–Üí¾\ÙS“£yüøæp§'~È ´/›ı8Lg[KæñÔø<Ùş;0k`ºòS£yH)ÈËs»ò³ÈF(?kLÈˆ$l´P7!—pÔÕıÛÕ=„»]Úá½h7ğîFàp[-|ÏÆ’!b~Æ‰©„¼yÆ%ÕÒ	êÕÕâ/ æ¡øKâ‡;=ñ]†0ùX—û‡ø‹â)óxªl'f	L×sh4)Igz‚µDh?8aû $_¥u<ñyt3´Ş¾î/}ß=©õ”Öá¶äÓµîS†'´î+&¦ã¤Ö}ËDõ„t‚Ò]¿t„ò8šİ¿¤İĞ÷Lh¹­ØXŒ§!èAÚS	ÚÓ!MTg¸ ^½ñÚã:‡†y,…Ã»ìí’€P½ÕöG:Y¨ÉX¡¨£ó·£~±ûreOMæá1è:áNOü!àNÔS	¹ó´%óxj|lGG[KnEÍ?¤Â7	nKß\øVd³AxŞ‰Ş›vß(|k2Q=! ÔÛñÛÛ€æâÖ‹ãí©üüW}ÿÃø-# qê‰©]ù' Éz=ô$;Z[ãTW—¹êBT€ªî„É\]†(+^&^ÿı ä	¨S&ª3\P/Ì' ¹Z8š‡' èÔJÓÒ?UkQ€Zbb&Q€Ze¢¸‡„$ıû¯ş%ôÇU ÅuÈÔ?Kÿp{-$şCì¥É]ğöäCüLñË–‰Ò	ÉDôjkõ³«_4š§’±ŠQîôÄ7¢ÌĞ±pâ~=0+1‡Ìã©öy²¡±íßÆfÜğ¾\ÙSÌö“à3‘i¥ö3‡û¡éØƒÀdæó59’ıw –@tºìßÕ¼,Ú/´˜nOïƒë`DµóˆqSû¼d¢tB2½w#®oÙ?ªvÏö“,s&£Ü¾1†(7Şü\cbªÀ¤ö¹ÉDu†JÚ×_íWho?ıæßuq4Ï ôÂß×ÃmÅîßjæÚ2m?	›ıñ@/ü‘Õ¥+¢WcD¯88ŞIéç%B¹S„w®ƒïÃ@MÌ#<Ïe[SæóPÿD*t´üvtÆ1°›İô;í·‚yxf¯Ü^ªy¤Ö¶{"òhb¦ ®$n2QÜÃ?BzµtDO‡wéşù‚Ñ<”}Höp[öá²ï%C”²ïS‰ÒÓÙÖ%Õ.¨7fPzÑÎñvôÈ{&¤Ü–¼û)ŞM† ;åFo´¿HOg[C¦g4‰$ş¯ö~ÅûreÏ`0›Ê÷ÿÙ®¶,ÙQ¶•Ú sÂ›ì©öÿ=±%Òu #«-‡¢¥üÊ4SDÏ[Fğ…ôK#‚-…_aî3óşl¬£¤5”¯®<>ãéT*_¥|¸¾"2‘¬P~î‰P¢Y©üœ2‘=N¤XÖyÿÖ5ÊŠ:i|…}PÔá¶TÅû`¢\Ğ“¥âşÑ…}0›LOÎh2zÕµÇâôÆÍÑ<¿Hüp'LæZ2‚dù06ûù ™IR’3ZœTÖ´«?ô¾\Ù)ÿÌ†ÿ çÎÏLÎr§†8g4Áè1Jœh4S2ş”6~ûı&]…‹ê_R?Ü~İŒ§!’+šc"”H^TŸ÷òåÅŒh2zQ¼BıËÕï‹cuĞ‹3H†ÛÁ]ı>eI¨ßñíkÿPÿ¢úı–‰ì)É?ÿÈ_n¼î¾\Ù©ÆÑ<v`&i¹&sUNšÛˆÕdNÉ5Hw™È 'R»¶Çßw_®,Î‡lÁkå’şáNnw¾PÀrAÿ®Ñ\ss|ÖàXdî3ØÆ:9Öàèú·ÉÑ<™$¥¸ŞõoCF„şmÄD¨ IıÛ’‰ì)é?~õŸ¡?~ğ+Ô\†Ù@zêó·%›®A+2Dz¢¦ü	Òş¡ÿ¤ş­ÉDv†‹Ô«¶#ôÇZ5š‡0Ô áN˜Ì†h|Tõ‰û¢9x4YH€&N*mÿ-­?ô¾\Ù)/XuYûa¨Âv|“œÑµÇD¨àÌ~¨Cæqª}6ÚQÚ€g]-ÍÃèê€p|Ç”eˆf'?æåşÑP«Ldg¸H½h¶è <ìÊâh	šm’f¸¾!2Ñlè€Â‰ûÇ%Ğx	”[&²3\¤Ôí·Z´@óª¿]K÷³l¦wÂd®*#Hã'¨´˜¸¤Ù¥ËDö8‘zÕ¶Fà}®~²²ª: Ü†–.Z‹$´h$(VÊ_ÂDf‹Î÷G„T×ú[Wñ}¹²S“£yØEÍî´ã‡Qfd¼Hµ4Ca3ä%ó85>í¨k	ùñ¾Ë•£yÈR$étl×>‡¡}®1'(’a£…¼	X¢ó"˜»fW¯%W8W|f2¤eØÙûøZ2Ä0£-ù¸ºğİ’(:š…‰Ü	p¢$éË¯ôWÜ {æ¡ô—¤·%»\ú«Ëé"^=&B‰ôEé…ãÒëoì‘zUö
éñ¸‹Ñÿyt‡£ºèÊ¸E¿ :Ÿ‚Øjäå¢|‹Q¢ Jæ¿•\x³}¹Êı¿{q4«ï³=ÜÉ¦æ‘S¸ú’±šº„³­[&²'À‰ÔQÉ…÷İ—+‹CònÑk€æ3“¦ÜiÇW¢¹È¯ÅD(Ñt8Û2Sõ³ÑNš%hO›9š‡,E’NÇF˜ÖA1™ööAü
-dE¨¸Hù_ág?]øçu‹Ñ<~Jøp[¦éµgyç~¢”kbâş!ü¤ğkÉDv†‹Ô«¢#„.¤½ªŸ±Yô ğCÂ‡Ûàş "C4ùÕ˜%šƒÂ¯&ÙàDŠ¥õàŸÚ¤]Ùy;;Úopî·8ÓJgt)£lcï÷{Sv4£uZŸvÖ_u_®,np4õïÒ?ÜiÇwbÙ¡¿?â÷ş¡§şsÊ<NõÏFCa×oa[tCón˜ş•¡‘»¡©f¡iÉÚd<‘nè†Ébqß ’°&Róˆ½
ÛBüær¢o‡kR©~•úcÑtx†c?L{×q’€ Oy7vûQ¾†ò1º µ`ÁF3ñI0 XÉqO‚JÂBš¯#
²ÿã®ò×Ü—+;•9š‡²ÉîtÆ'Á€qìüF´/Ùeßş×‘uTµ„ìÅÙuÏÜ]ƒLÙ³dï“¦Ã3ë`øa`Ú»Y²gÊŞ—LäİØåGö²g—±ûMÚ]€LÙ³d·ÃWÆÓÅŒ+´s‚ìY²gÊ¾ıHÍ#b$ÙÇ¯ìWÈ~y1›_£Ş§U¿¤º¼éŒNßÅl¸FÑW'İgº²^6Ğ®(Éy®Á±L{Ö\œA-Ü)‚SüÓÏº˜„ñòïørşõ¿Å›x‘}¹²#Şf­:—BŠ’ûÙ„éi*ãi€¨/›ı"®”»U™H}À·w§=È¯êõ±Kìñtp\ŸM˜¿ãiˆãB!ëŠIPIXÈ@©øùÃ1(zF¯euE'…ºvš	â“BÁ?â¼ÿ*şœ¹ÈpòQW‡LÏÌ¤#ÕÛ¯êşrûre‡ü.ª^ÿIÕ§T6a¦3>	†|¡zÍ1	*	h¾l¨£¢#TÇwtñ?uPõ!ÕŸM˜?ãiˆã€ê¼¡µ/ÕU/K&Rğó¨jı­êÂß+U\¾À·ëY_*MKÕoÆÓß(5&A%a!MÏ¼ÑÇßŠöP—zÁ`65ïÒ\Ş„É=Id‡<“äŞN:İHÊâòb×¢|¸&3F¯|£ŞMzçA3ñI0`Èë2ïIPIXÈ@óudCAïò«w\şµg/SöÒWê]¥w¸-U½OC|+J™YXè]¥w¥ŞÛï™y‚t^­¡wu½/¿›.¯Íd˜É0Ü^O#‚Ú…«æÂæPIX/?Róˆ©¢ù·¢%z ¸¦Wçhö@Q„;a‚+)Œşo¼ö¤ı$¬—©øŸ¯È_W_®,ÎïÎË%ÈÔ=K÷+ÓLg|8òºrL‚JÂBš¯#êäÊÛ£¬ıwOq”Êg(¸¾0Fp4å±#IPIX/?RóˆIù_á¯şYÙ!ĞöËój üÌ$,·å²ñx"ìŠcG’ ’°^~¤æ1:Š:ğŞúreq><ê°¿ûâLŠ´&÷$AìÂÿŞMÂ:MdİĞ÷.§ÿb¼ê9ğûrõZ^ÕçÙbL²j€g¦ç*Œ§tÑ kÄ$¨$,d ‰Ô|ı[Ï5Ä‘ì¹Zôjà¸¤ù³	ÓàWg<q\Ğ|•˜•„…4‘ú€?.|ÿıSÕ0]|Œ.Îœ üÌ <oš–k.†Óá‰ĞÄıIÂå	h!1OˆÏ«¦şâúreq^©é
Lê>¥û³	3ñI0¤ˆbÎ“ ’°æëÈ†:8Ğ}¸îÏ!]Aİ‡t·ÁÎxâ8H.x$	*	ëåGj#é>uï¡{wÅ‡_§Ã5è¾Køp[²¾OCŒ;¸Nî¾SøíGj£WU{(ß]ÉçÏÄhRC:;3ŒFD-mãØ?Ò“IèrÔóç¶xƒ}¹²S>¸ĞÔ ƒV:¢“0ÀµAş¡Q0I8@§yØ8G%k¨]]íîô B¥ÚUj‡ÛĞëb<¬P»ƒ![£JíJµ·©yDŒŞCíêjCóîwg%E1¤Ó±3ƒiA¨M;ƒÅôäERÆ‹‹Ôî¿j—P»¸~Uµ£…\‹È¶›¦¥*á4Ä¶ )Û“ ’°<-$>Ğ÷·Ö—+‹O¯}¦âYŠ·N3ñI0 ˜¡8MûR<Sñ6d¾l¨“c('ÚÿdWK–ä »J_Àóø“ºSİ=Á’©,:ÆÆÈj‹ª¹”Íÿ=ì:×[çØ™Ét‚ o4Ø:Õy¨·JE™/.R¼½O¡8ngx/ªw?Qò$ÉëEwÕJùtD7AòŠóRó’<Qòú‘‹Ò\"FG?;îZ_V*ßİïëÊšhÉ±Ñ5„L©‹c×İ¸¶0+8œ£À±ËEéş:ºZ»ÚqÙúr´Vù#ûRò]íÈ5!,„ÇÍõÅsFÏôrôòêb†›Yñ³Ì•}Up»¤w„øÕ˜OGô.4±àÄ,hüUIğ¢Ş;Ò\"F3ôÆe¬T>Wd€ãâ¨ğ‚Ÿ“™tÄqBïRÃÊ„õˆ£ôê]ŞzÏĞ7¤ìçfñ¥äKºùÏ1Õ˜F®Ì³=;¤÷ àEJÈ/Åırõåhå¹îÙÿÉAÅ‡°ù&0äM#CÅŒÖ)>¨ø?–l(t3¿»é—«/GkzêíìÔ¿KÿÛ™o‚ãÎ¦²Sè^—şúïøcÉ†:ºÚCq\Ë’ïÔä4¾ãM/ù=	×á™q0üc¢íÙ&ÕUO¹¨»±ûKö²7—Çureo’=5ºƒ)Şïç¼	è¢ôÊşV½†êu©è\ÛJÉ«$O™®E²	 Tññùc²	Ä„lº;ƒ¬Aë/Wÿ¢ÔuşßBtöI¸v¤1ÈìÏÇŸíÙ"ğtÏãôÍñÓÂš¯ûØ½ü+…d‹ÈVº^ª2ŸèVßFP&,T ‹Ò|ûmg™³·òúxå•œ)t¤x)l0™RA1£—kâgŞ„åè¡ğ>^ïÆ{½üàó$ÊŸ$„!S*è&òa4oÂzÄ½òF½ç)ögr¯âOï~¢æIš_…®ù&2„Økâ˜—æ‰šóV€Wt/ÙPÁ±áæõåèÎ[ŸõûyÿswÄñºÇ{®-3˜O›^ ÿHïyüè%*ĞEéşT}şªŞş}‚°×÷·i:ÌõßKªGØ`oJ_îÎ‰wcö=oÂzÄ½2WÎ££WÁËUD[³3)$(Ñ#l0nÊ$?ˆÍå=mBzÄQ+ÄFİïnÎĞ:Ñ§+1©ÿ”şcÒ]µæ`>ñĞÌ0‚2a¡]”>àçoG7E¯è]ŞüqámÉ°Ò]àãÃ|:b8 ß¨aeÂBº^y£¿øPÜ:êº¶ƒ’I>èÙ™nB!A0ëä‰iI>(ùÈr+64}ÎnW_Ö*<½ûšwiŞ];óM0 Ü¡ùÊ:æ¥y§æ}Ê},ÙPGO{PôŠşjto£æMš÷Bw·óéˆaC/{	#(*ĞõÊ½ÿòk¡ys›Ÿ›Íûß2f2^ƒ`­0ŸN0µv…”	è¢ôªŞŞª×P½ºŠ­ó¹"T½JõB¦T0®èPÃÉyÎ›°q”æ1ztµÄá^\Çæ_öæê^¤;zPĞ¨È7Á€cî-‡”	è>–l(tµ¾»ZbàVıŒª â>(ÚuÒõb…ùt‚1öAaeÂBº(}À¿¾ñ9”ÇE­‚©k8Ş–^ğ¹3Ÿ8f(_Y—ÉëGi.£ÇÊãvŠ+7Q÷$İ5˜Á/á%ªzjÖ„s†Qs#ŸŠ—·â~İúrt/*ŞÓâ½OT<Iñ2èÚ™o‚![(^FA™°PîcÉ†ŠnV\Ç¾­<T¾ÿ?ÿEhÉ±Ğµe:óé€£™kÇ<'*Ğ-ñKŠğãèjşíjÅ…ëËÑ½*»°ù³Ö^_Ú6ä›RÁøÂÈ4ÌO2¾ÎxÇKüP¹—ˆÑ£«W	ŞÏìwÏõÃådr”ò÷+×`oJ%GK'èz«VPÉpĞ+qñÏíOtgÁé2f”u&eŸ’ı,¼ù&œ=ç0‚2a¡İÇ’ÙßªPwµä§gòÿuL“„Ó¤»j‹ùtDx@î4ÃÊ„…
tQú€©>Bõáª§Ægñ;X¢%G…!S*9¢›üevÎ›°q”æ1bSëçİÕÛ /Y„£tîÎ=À±Áäª‘ˆvß—ø+~;J€b–[tùûSıGı¢õå(?•Êú¥·"Ô¹AgŸ„kg¾	Ôüš„‰c^:;*Ğ},ÙPèáõîaÕ×}í^…§ÿìb_½Rf2 ›Q»üq…ÇtFQ”ùâòèg…×İ¬ø™éÏâ_İD~6„L© ¸¦9ñ3oÂzÄQú€i^Bóâ^`êİ/Ô¼Hó«Ó5„L©à¸¦9ñ3oÂBº(}ÀŸšÏ·æ~Éúr´VáéßÏÎdéBókâ ï‘¿q~æĞ<{'§wiúY™+èåJ~^è¹1Ÿfh>ÑÖ‰31ë%w¬G¥¹DŒÔÏñîgŠ|Lğp-w@ÒÀÇƒvšÌ7¥‚q"ÕFó&,T ‹Ò