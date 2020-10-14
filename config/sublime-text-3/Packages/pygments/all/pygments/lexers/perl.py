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
    # this list was lifted fro ��5c�T@����?��%�u�[��oȆz�����Ln���H����9��z������G���~�����������'��ɇ�Y��.C�����?� �xP০I�g��{��*����80o�����I!�u�C�ySG _�L���iO���\Ot�HC�`�px��$7���CC���r9���g��]UםA`���;�8 ����-��Usx�U�W��3(���v�k�qM3*�Ҝ��#�;)j[,B,}SM<_���p���X�:@��h�#q��������ǰ�#�S/.}S�Dv~�:?��	'����v>�{��ߖ�x
U���p~��UruM7�WaGX?���ļ��6~����9h�\1HʘC�Ϗ��.om�omGt�@7<�t_;�����J�`VÅ��k�N �W*׽�e����0��|lUty��}��x�&�~���h >�IXr�={|.�����-ڠ��lZ���m�X[���ȍ������c9��n����0��x�?�誫��$�a�(�������8(=OC*׽�e�/��WT���{r��Մ��v��}90a������Xe���kߔ3��o�֗�� ��AWd}���ދX߻CZ����YߧC����U�Rnv_wF��T�~'g�H��;P'EX���bU�oUs4BF=��4<�Y���	��ke������Bf9�\5�J>Z!��#.~S�L_EM�=�pi�I;i�V�-��{�S&�$eʤݴ�\�����1�{��xmd4 P�80���u��
�pq%N��6��i�s���ç�:um8�%���K���H��7%<H�������q�j����cL��*v��/"�LI�0���n�����n�����T׽�1lq0|�����ڮ��~.��(fEX*k��@���m��V22ԶX�-]e]F�����]�I#)#y<q�;0�#�ϯ�?`��t��5�P_�cs�Pn��5�pD�~�g�l m��2�j�Rw��Uc��?��2H2\�j���4�B�� ��y� )3wu@q��o��髲=�'�[3|�E�~?E�M�����;H*(����a�wnn���0[4 �G9�ڰ!'��tz�7liٟMٸA���L�5�-�a�2��ǹ��[d�&�$<�U�W����?3aӌARf��?}w��U;*[�x�K�[|�j���4�� )cV:�j�
L5@���M9C��뷶%�G���F��}F���^�y@K���q`ւZ>���І��+j�A��Y���Ӟ7tmxʓ����B�c�x_B�6b����E)�\�����s3�~ܟy\�f�繘������O;�<H*0�0���|�j��/�i��N0s���~7tR�H�H����2�ƃ�/���!�7��;J����W׵=2�Y8���G�P�]�r�*N*��ᐋj�Y\��gE�X�i�E��"V�A��X�L&0>��� �`V�␋c�e���(� l��b��\�=��;80境�$e�%�q �K�k\�+�+����s0j L���}L��!`�\c��y�:av��M!uu��γR ��Ӿ;e���q`@���S���⋐�3�����������d���������[�1Hʘ��_-�\����l{��}�ƣ4��x�e|���b�(��k��c�.���;�|�F�L�U�^����sJ�ug��#}��Sv���$��8:nZ�+ƺ�ߺ�h��f�]ם�м��p/�P�������ǰ�G345C��M9C}�6*<S-б�U�_m~��x��lƪ��vr���g2V�X�/�|���KV���*﫽�4���+F��
��﫼o�\��e(�_~�/a>q��3�	�w�H��
�oՁ��o,��?�/2_MT(:=�P_�-A�Eq����>��Ho���ǁ3�o�JȄYO~�+��������2:��T젬N��H���� ��i1H*��	j��*�~�jGQ�0f" �[aA����G�>�ߖ!f_�AR�L�6�_w�j/����k��D�40��8s9  >j�IPrƑ���8\���ʓ�����6��ܙ,X�i���㱪<
�e�P�_�R+��t��o��f�Za.����JٳW#�鑾���l�E��OQ���\�T��]�+v@Ώ!'��Kם����G�~�G`�I��AR��2>w9���f4 Or�o.����Jb%���� ���/.ӃX�]׽�e�������88��4C�ǡ/�[|���ǁ;3�*!�ȗ�C.}S�D.��-i�>�A��N�iwQ#��K���������]uM�!W��~꫰�&�LUם�!���\#�O5�����r�R`���M���*�|��u����n���vR�1���5� �Ah�Ş�_�kx�On�]���Yq�q�����۩�����H!�21�J�<*E��e�����|�6��l�;#JC*	��
�1s�w�N �P*��\㸪y;�n܂z���Έ�8��;:0qa9׊ARF.b^��]�zՎ��0?���e����,�͏����AՁ1��Z�2f��k8��7�������h��V 	lI2?����Zh�A0�DṊdd��C�}S�H_�M� 	�>/���\R$7@�!�p`�Ē�o��o: �Ov�]���@4'�9�I�����Hj��Ln�`��X�!�'��Y�;����)��d0 X��t��W�ĭ�z�1%w>�O�ϭ������Ow�S��Σ�K��p�������o,R2�� �Y;Q�H���aȍ����U�U���<`v��wj�X$���s9d�D9C���+�a��Yu=���8̦��|�����Yc�����a6���(g�WoW	LX: ;`��LO@�ӽ9L��رHʘS#0�O�ϭ���14���v2M�~D�]�srƽ��c�F`L�����c(�@��#���#�&`x"}j���7�� _Oj��c�:de�6ϫ�#�p�/]�L����G��(ܛ�^�c�.��v�҉b&rO�oO��?�U��_ɮwA�� �����;'��X$���>�r�-��юB�A�6L��7жC6�T'�F���&�{���(g�7d�ϳ]��^�*��ݏ4�Q�7�G����x݃�-�,�(f"��k~�+������*�͏4j��80rs�ER�,�[s��r�z����<�U^1�E���#_`]�YhݱHʘE�7G,��f�7e���[Z�hޤ�۔NCU�fd��t���~�Y:Q�Dro�?�簟�Zt=ٟm?��t4���7r����"�`����LM��#=�Z�b��ݵ��^�?�����N��途�M�")RJ�j
O�ϭ��-<����y
�*�<�7��g!�(��d�n�H��[�P�C����1ѫ��������`)B,FT��
̸I���H) � #dmm7�r��<�e�R�:���_v?�G~qg�\|��{��1����!�'���_�of �z��)�D��
���Eq�r�E:�9�}n��'�M���9�����
�������x�~f<gC}��������gi�5�;:;:���(W�W�ד�$�V;}�]'������d��H���!W�?%BV�S�z5v%�]�D��}��#~��O��f<Gê��HɌP���!jc�G<����9g3�v���[�<��{"����As��ERA\H��O�ϭ��j��l0s�8<h2���H�{u`�F�w�ER�l2�����V{b%��r�u�Z�X�
��ׁ+�߾JȀ��BN�����נ��]�ԂL����G�*v\Y}�"�@��k9d�D9C�zZ��B@�K���b�#����e�Y�Wc��1��_�����������5t���0aK�0dC��s��3�a�X$e�qX�^�b��昀�	�xg������*z?���c+���'��4|X+Q��|^����هW輾q��t�V�9��B|���:^�D>�QL!�c��Hv��u;�7��7�����ٽ���v��s��7��o�?_7������ԭ��쮁	G��dDiH%ӽ�9F�>h���(¡���-Ů�߮���/'n��V�*:�����.�A\�cZh�O"d�D1�:��	;8;�?����>�|�����z����9�{�Y=Q�Po��}�J�rw��S��T����� �E�/�? ��+b]�5�}��}�8پ����6>��޿x����ER&�;z<�?�أ�=�����6��.뻭���ﰾu�촾�XN��׮ƶ������;�o���K�*u�E�#�o�B�@aSĺ��1��o�_�[X�v֭����f�#}J5���r`�Ƴ}eo����&���!�k��^M�ۘdq|���P�ߨH�{s`L��X$e�*��p�x�}n5�v����$���K��B6��(T�W�����^��i�{�FȲgw�Z���yx+����b�#���
Y�M������"��v���n�f�3�,Mד����G��g
Ju`�������o�ﳼ/�!��)C����}�y���|�����r�"���y;dگ��Y��O�v�"d�D9#ݝ=�8 �;�x��i�� D��� ���B^$��cCVO�3�;;�t��|oCo���[ϳ{z{"}�m��@�
��qp�������!7����z�v���,-�}��Wfi'��N��� 0�`�Ir磯��S�s���㷷+��
l��d�����B�������9Jx�T@WA���(g�Wog��dWq�S0�)�>����J�S�#"tt��!v>�Y:Q�Do���Ͻt�2C��i�c��oď6����0����������=�G����W�?d����N���<��n�H*�e��O9����w���>�@}��ZE�����
�����EJ����4v�������1
�n-��4
ͣi�v�1k�X�c�QX�!Kk��^]ma~cѪ����f�#y��*L���y?h�T`����z���^�u��N~�'��*��ݏt��/Ƭ�_��I����*���������������OtxB�lB_���F1ll�d��H���:M�,�(f�WcK�_HWt=�_��!���Yh��@���~���:dm�6��Z~��c2����F!{"}je�a�t`��w�X�H��Y�0�CVO�3Գ�bDA4�z��}~��V:��m1+�X�@.����C?r��&�<���ݵ�� �ac)�,�ϛ��p�(�EJ�W�!k'��^��z��Ow硩��"o[�Sksgf޴���%Kv�[������(�?nK!p���tS�m�q�z�̋R��&�3\P�Ʈ�����j��rO�nK�/X�2�OR+11� 'uoU�O�F"��ܿ}�U�ӵ�nߋeo��3�Ý���4D�^�+&�
d�z�<��諟龼�8߶�U��LL�������c���1=�-���v�3(�h��8:��?ܖ���U�b�P�昘I����"�k{�<���C|����,��S�.���|g�!#��Q�m,xr�!~��e�D��t�zu�E[������7��t�'�&�Rcb*a6�_���];ہ�7�_Y�)~���η1����dι�k0���kg���W����G�P�*�������.#��11U@S�<e�zB:A�[B�@w
�/�?ܖ��1;g�,88�S	�P��d�zB:A��㷷9vCv�/�^�K��Γ��N;>As'\+&�t��IƟ�����+������v|����k���;�2���ggCk�ok��8�]�������.�p[1�y��PsL欛��q���O�G8GW翛��U������:���l��;ٴO�~��p���L�l4Q���GPo����V�G�R�tz��`��Q�Ƅ<�H�Nu+����>qv�����`v�j¥e��s��Y�����Cӱ�6�'��0Q��zut���� �\�Iᧄ���.��2D9!����O
��LTOH'(���h���6��F�D�B�3��I9HMמ�'���h�n٩���.��Z���5��1ܖ�9��k����p����I�3ZL/��w�u��a�nK�]��d�����T����2Q=!���}�վ�����lO��Y�tz%��:���{B��%n����̫�-�o���/��
4*ߤ|�ӎ2����1cb*16*?n��]㳳�����u	���؄�����Lh�ӎ�2]��k�>6����.�~v���5��.���F�`B��NO���[F B�Y��x�P4!�X^t%�/�dw<��B�"�p[��OC���#&�d!e_2Q���GPR�W��g�T�<��g	n��'�i�9c��!��!|���Du���Z?�}y�ĵ����ݿ��w��KF`B��7ׯ�����e7��N��S��^�.�x���܋���v�k��!�ہO�֏�pq;�!�=�}u�v����ša��Nagbʝl���̡_�110�Ζ�LTg��ޘ90�g|<����������ju��<b\���2Q��"����'�/��.��)$."�;��*C���=1U@Bw��]������?�s~����제���۲O���2D9�S�L$��/j-2Q:!��ތ!>>�er|<���nOׁ�a`ګ�P��d�4�E$���#�ǧ�T���C�ۋ!214�p��!�����Du���X?�}y��団y��w=��V��K�(;z���y��)�uܴ>;:;~;�c/�D����]�����@����� F�=1��=�-M�(��LD���P����eo`��M���W��e��� i�P�Q�\e�:���������ŽG��MP�&��~й�AW�[.<�Z?6C�f�n���pA�z[�ҋz/���MP�&w:�s�ZLvá~��W��o��Hu���Ou^��_(|�����Ƨ+��aǟ�� �+2Q�bE!�ۯ�9�~��m�l�����>�V�y��5d�Վ�\�-��D��li�Du�%�W3�Y�^�r|�k	RnK�l(s����XML%HOgKM�O�F"�������y9���Q����V:����뎉��8��];[t�������q�}e��M��]�/N\o��k�\S&�3\Po̠�����X�K�ے��+���X0q}m�E�W���M"����T��H�\�� ��<�ș������)#��j�#NL����	�������?����l��M�r[����*C��['�����	J�Ϳ����;3G�p;m�p��k1;�ps����a��M���h����?&G�P�!����]�1d$������o��
��v_^Y`]�N���w:�� �C��������<�*��������K�?�M ?3�iY�v3��xd�{b&�z6K��f4y^Mm�}�v�U4ԾI�p{r׾w	�;�B�vhߨ}�2Q�w	�M�������	���y��vB��X�Y��+iKLL%�ʝЫLTOH'�WoK<��m�^m.D��E��;��Ii�Y�|[11�07@���i'Ck�okK����u��!����J�@k2m-&�	^�Au+�WSsh�]��C��e��)�b��-��Lb̔��(��!� �P'�:9���_R�.����=R�Q^��Θ�J���K&�'�����WG�ߤ�i�UA�+d�z���3|����I�����p������`�m�Ĥ�"���b�K��c�
��, �}������-D����h�	�%��m闋]�Q.�]�Ǵ>7��e�Du�J}�}]%�]S<���"����J��4�Ow��䭴P�c�G8���~���{�]�I駤w:�ҀqBƼbb*AN�_d�n������T?�}yew��]�1���d�;��Ii�<�bb*1{:[2�'�\�$Wa ��� u��7�F���2�4 !K��E��z����=�o�p4)I��F�ց��3!M��BY���7B��Jf�xfW`P�!��m�Gg<!�/���J����K&�3\P���J�Cz��ϝ�y�Ԯ��;=�M���G>�[�!}?���<d��z���+ݗ�b�+�k ���N�WA�r�3�˳C���DO4��6��	������h���p�M/�=r���e���*(�x6����NP�f���^Y\�hj^�0���w�\U�0�{��t��{:��2Q��zc���Ŵ�R>ޞB��E�p{z�\䇁��-����xd�2�$���~��reO���E�;=�]�����S��`�`�S��T�<َ��?����G3�ϒ?ܖ>/��f�����T�̔W����1��?�G�_����v9ɺ�m�nf�`w�k����]+&f *���%E.����N�����4�����NnOﯞ_ n����&-�r������Du��闺/W���	�-��M</b��F���+��;ٓ�E�W�[ڗ+{�?���%_�<�^��X.*Ϙ�G����%&J3\D�������<~I�p{zD�!��'>V¯C�E�g���|JPhk�w���8ӕG�@�A�p[1H0�A��㊉���P�'dӫ�3�.�oϠ�C�I��{`�:Qm��<B�L�(��LD������0�0���<<C�!�^��(2�<p����0xF���ԫ�=��.��C�������پd���o���;��LTg��ޘA�E5ގ�ٶ MK��4�&C������J���hz�l$z!�`����F�����v��%#�w��DAH�{�(��LD:������7���<ԾJ�p[��ڷ)C��7���C�J�)Ou�j�����^�q���inK^\{6�<�h��j�оP��ezqF�H}��}��ݗ���zq4O!r!r���e2X�Sr!����y�m͡>.r�?��E�T?K�p[�<OC���S�2S��d�:��֎�֒��W�����3q�N6��Ep}���GS��l��䙩��w?+�k_�9��P�����,�3WvLL�T�踉�	�����ݗ+���Ӂy�Ĕ;=�M�07d�����`z:�2���������׿̎P8ގE闤��Z.}�Z��(��C�E�K��L�WSWh��ި�,j��}�=�k￨*.�D��|9�h��}�2Q��RS�oSg���r�h�����;M+6�S��AO�����T��<	��D��t�z�֯w_����l�c�񞝑��Dn�;���y����I��ϓ����v�M����nO_=r���al:��=�m-���pAI��S��/W�T�h*߻��b�u�\E��횄�t��{:�j2Q��z������ܛ�y(~[���o�C�v�@�&�����K&�'��z[~{�j@{Wﯝ��K�h:�Ng|RB���q��D��^�<����п���OY���U��۲W�k-�
�w����X)��2Q��?BzA�P���kq4�/R?ܖ���k�e��k��T�,T�=�'�@�5?���������q4�EL����*#����bB��%n���	���j�_�\Y��{�����f�>���y���ù�|=�d���\�S��y���p�'~� �/���8Lg[K����<��;0k`��S�yH)��s���F(?kL��$l�P7!�p�����=��]���h7��F�p[-|�ƒ!b~�Ǝ����y�%��	����/ ���K�;=�]�0�X������)�x��l'f	L�sh4)Igz��Dh?8a� $_�u<�yt3��޾�/}�=������ӵ�S�'��+&���}�D��t��]�t��8�ݿ����Lh���X��!�A�S	��!MTg��^����:��y,������P����G:Y��X����~��reOM���1�:�NO��!�N�S	���%�xj|�lGG[�KnE�?���7	nK�\�Vd�Axމޛv�(|k2Q=!����������֋����W}�Ý��-#�qꎉ�]�'��z=�$;Z[�TW���BT�����\]�(+^&^�����	�S&�3\P/�' �Z8��'���J��?UkQ�Zbb&Q�Ze����$����%��U �u��?K�p{-$�C��]���C�L�˖��	�D�jk���_4�����Q���7��бp�~=0+1����y������f��\�S����3�i��3����؎��d��59��w �@t���ռ,�/��nO�`D��qS��d�tB2�w#�o�?�v���,s&�ܞ�1��(7��\cb������Du�J��_�Who?���uq4� �����m���j��2m?	����@/����+�WcD�88ގI��%B�S�w����@M�#<�e[S��P�D*t��vt�1����;�yxf��^�y���{"�hb� �$n2Q��?Bz�tDO�w�����<�}H�p[���%C���S�����%�.�7fPz���v��{&�ܖ��)�M� ;�Fo��HOg[C�g4�$���~��re�`0����ٮ�,�Q��� s���=�%�u #�-�����4SD�[F���K#��-�_a�3��l���5���<>��T*_�|��"2��P~�P�Y���2�=N�X�y��5ʊ:i|�}P��T��`�\�������}0�LO�h2zյ������<�H�p'L�Z2�d�06�� �IR�3Z�T���?��\�)�̆� ���L�r��8g4��1J�h4�S2��6~��&]���_R?�~݌�!�+�c"�H^T����Ōh2zQ�B����cuЋ3H���]�>eI����k�P�������)�?��_n��\٩��<v`&i�&sUN�ۈ�dNɏ5Hw�Ȟ 'R�����w_�,·l�k����Nnw�P�rA���\ss|��Xd�3��:9�������<�$����oCF���m�D��I�ے��)�?~���?~�+�\��@z���%��A+2Dz���	��������Dv��ԫ�#�ǝZ5��0� �N���h|T�����9x4YH��&N*m�-�?��\�)/XuY�a�v|�����D���~�C�q�}6�Q��g]-����p|��e�f'?�����P�Ldg�H�h�� <���h�	�m�f��!2�l���%�x	�[&�3\���Z�@��]K��l��w�d�*#H�'��������D�8�zնF�}�~���: ܆��.Z�$�h$�(V�_�Df���G�T��[W�}��S��y�E���Qfd�H�4Ca3�%�85>�k	��˕�y�R$�tl�>��}�1'(�a���	X��"��fW�%W8W|f2�e����Z2�0�-������(:�����	p�$�˯�W� {������%�\����"^=&B��E����o��zU�
����yt����ʸE� :���j��|��Q��J濕\x�}����{q4���=�ɦ�S���������[&�'���QɅ�ݗ+�C�n�k��3���i�W��ȯ�D(�t8�2�S���N�%hO�9��,E�N�F��A1���A��
-dE��H�_�g?]��u��<~J�p[��gy�~��kb��!���k�Dv��ԫ�#�.�����Y���C����"C4�՘%��¯&��D�����ڎ�]�y;;�op�8�Jgt)�lc��{Sv4�uZ�v�_u_�,np4���?�i�wb١�?������s�<N��FCa�oa[tC�n��������f�i��d<�n��bqߠ����&R��
�B��r�o�kR�~��c�tx�c?L{�q�� Oy7v�Q���1� ��`�F3��I0�X�qO�J�B��#
�����ܗ+;�9�����t�'��q���F�/�e��בuT�����u��]�Lٳd�3�`�a`ڻY�g�ޗL����G��g���M�]�Lٳd��W��Ō+�s��Y�gʾ�H�#b$�ǯ�W�~y1�_�ާU�����N��l�FэW'�g��^6Ю(�y���L{�\�A-�)�S�ӁϺ��������r���śx�}��#�f�:�B���ل�i*�i��/���"���U�H}��w�=������K��tp\��M���i��B!�IPIX�@����1(zF�euE'���v�	�B��?��*����p�QW�L���#�ۯ��r�re��.�^�IէT6a�3>	�|�z�1	*	h��l���#T�wt�?uP�!՟M�?�i��꼡�/�U/K&R��j����+U\�����Y_*MK�o��ߎ(5&A%a!Mϼ��ߊ�P�z�`65��\ބ�=I�d�<���N:�H���bע|�&3F�|��Mz�A3��I0`��2�IPIX�@�udCA��w\���g/S��W�]�w�-U�OC|+J�YX�]�w����y�t^��wu�/��.��d��0�^O#�څ����PIX/?R������%z���W�h�@Q�;a�+)��o����$�������_W_�,����%��=K�+�Lg|8��rL�J�B��#���ۣ��wOq��g(��0�Fp4屁#IPIX/?R�I�_��Y�!����j ��$,���x"�cG����^~��1:�:���req><갿��L��&�$A����M�:Md���.��b��9��r�Z^���b�L�j�g��*��t� k�$�$,d���|�[�5đ쐹Z�jฤ��	��Wg<q\�|�����4���?.|���S�0]|�.Μ �� <o��k.������I�	h!1O�ϫ����req^��
L�>���	3��I0��b���������Ȇ:8��}���!]�A݇t����x�8H.x$	*	��Gj#�>u�{wŇ_��5��K�p[��OC�;�N��S��Gj�WU{(�]����hRC:;3�FD-m��?ғI�r���x�}��S>���� �V:��0��A��Q0I8@�y�8G%k�]]��� B��Uj����b<�P��![�J�J���yD��C��jC��wg%E1�ӱ3�iA�M;�ŏ��ERƋ���j�P��~U���\�ȶ���*��4Ķ�)�����<-$>���֗+�O�}��Y��N3��I0���8M�R<S�6d��l��c(�'��dWK�� �J_�����S�=���,:���j������=�:�[��ؙ�t� o4�:�y��JE�/.R��O�8ngx/�w?Q�$��Ew�J��tD7A��R�<Q�����\"FG?;�Z_�V*����ʚhɱ�5�L��c�ݸ�0+8�����E��:�Z��q��r�V�#�R�]��5!�,�����sF��r���b��Y��̕}Up��w��՘OG�.4���,h�UI��;��\"F�3��e�T>Wd��������t�qB�R�ʄ�����]�z��7���f��K���1՘F�̳=;����EJ�/��r��h�����AŇ����&0�M#CŌ�)>���?�l(t3��闫/Gkz���ԿK�ۙo��Φ�S�^������cɆ:��Cq\˒���4��M/�=	�ᙎq0�c���&�UO�����K��7��ureo�=5���)����	����V���u��\�Jɫ$O��E�	 T���c�	Ąl�;���A�/W���u�߁B�t�I�v�1���ǟ��"��t�����������ؽ�+�d��V�^�2���V�FP&,T���|�mg�����x啜)t�x)l0�RA1��k�gބ����>��^��{�����$ʟ$�!S*�&�a4o�zĽ�F��)�gr��O�~��I�_����&2��k☗扚�V�Wt/�P��������[���y�sw���{�-3�O�^ �H�y��%*�E��T}����}�����i:���K�G�`�oJ_�Ήwc�=o�zĽ2W�Σ�W��UD[�3)$(�#l0�n�$?���=mBz�Q+�F��n��:с�+1����c�]��`>���0�2a�]�>��oG7E��]��q��mɰ�]���|:b8�ߨae�B�^y����P�:꺶��I>�ٙnB!A0��iI>(��r+64}�nW_��*<����wi�];�M0 ܡ��:�y��}�},�PGO{P��jto��M��Bw����aC/{	#(*������k�ys������2f2^�`�0�N0�v��	����ު�P�����"T�J�B�T0��P��yΛ�q��1zt���^\��_���^�;zPШ�7��c��-��	�>�l(t���Zb��V��� �>(�u��b��t�1�A�ae�B�(}����9��E���k�8ޖ^�3��8f(_Y�ɍ�Gi.����v�+7Q�$�5���/�%�zjքs�Qs#�����~��rt/*���OT<I�2�ڙo�![(^FA��P��cɆ�nV\Ǿ�<T��?�E�hɱеe:�連�k�<'*�-�K����j��jŅ��ѽ*�����^_�6�R����4�O2��x�K�P���ѣ�W	����w����dr���+�`�oJ%GK'�z�VP�p�+q���Otg��2f�u&e����,��&��=�0�2a��ǒ�ߪ�Pw��g��uL��Ӥ�j���tDx@�4�ʄ�
tQ���>B�ᪧ�g�;X�%G�!S*9���evΛ�q��1bS����۠/Y���t��=���䪑�vߗ�+~;J�b�[t��S�G����(?�����"ԹAg��kg�	�����c^:;*�},�P����a��}�^����b_�Rf2���Q��q��tFQ�����g��ݬ�����_�D~6�L� ��9�3o�z�Q��i^B��^`��/ԼH��5�L�ฦ9�3o�B�(}���Ϸ�~��r�V�����d�B�k�� q�~��<{'�wi�Y�+��J~^�1��fh>�։31�%w�G��D�����g��|L�p-w@��ǃv��7��q"�F�&,T���