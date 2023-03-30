from ply.lex import lex

states = (('comment', 'exclusive'),)

tokens = (
    'NUMBER', 'INT', 'IDENTIFIER', 'LPAR',
    'RPAR', 'OBRAC', 'CBRAC', 'LINETERMINATOR',
    'COMMA', 'WHILE', 'EQUAL', 'LESS',
    'GREATER', 'MULT', 'MINUS',
    'PLUS', 'FUNCTION', 'PROGRAM', 'FOR',
    'IN', 'OSQBRAC', 'CSQBRAC', 'DOTDOT',
    'NEWLINE'
)

t_INT = r'int'
t_FOR = r'for'
t_IDENTIFIER = r'\w+'
t_LINETERMINATOR = r';'
t_EQUAL = r'='
t_GREATER = r'>'
t_MULT = r'\*'
t_MINUS = r'-'
t_PLUS = r'\+'
t_DOTDOT = r'\.\.'
t_LESS = r'<'
t_LPAR = r'\('
t_RPAR = r'\)'
t_OBRAC = r'{'
t_CBRAC = r'}'
t_OSQBRAC = r'\['
t_CSQBRAC = r'\]'
t_COMMA = r','
t_FUNCTION = r'function'
t_PROGRAM = r'program'
t_WHILE = r'while'
t_IN = r'\bin\b'


def t_comment_endmultiline(t):
    r'\*/'
    lexer.begin("INITIAL")


def t_startmultiline(t):
    r'/\*'
    lexer.begin("comment")


def t_comment_multiline(t):
    r'(/\*(.|\n)*?\*/)|(//.*)'


def t_NUMBER(t):
    r'[0-9]+'
    t.value = int(t.value)
    return t


def t_comment(t):
    r'//.*'


def t_ANY_newline(t):
    r'\n'
    t.lexer.lineno += 1


def t_ANY_space(t):
    r'\s'


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


def t_comment_anychar(t):
    r'.+'


def t_comment_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


lexer = lex()


def main():

    lexer.indice = ""

    test = """
    int i = 10, a[10] = {1,2,3,4,5,6,7,8,9,10};
    
    /*
    asdf
    */
    
    // Programa principal
    program myMax{
      int max = a[0];
      for i in [1..9]{
        if max < a[i] {
          max = a[i];
        }
      }
      print(max);
    }
    """

    lexer.input(test)
    while True:

        tok = lexer.token()

        if not tok:
            break

        print(tok)


if __name__ == '__main__':
    SystemExit(main())
