from codegen.batch import Batch

from lexing.lexer  import Lexer
from lexing.source import StringSource
from lexing.token  import Token

from parsing.parser import Parser

from parsing.draw_ast import draw_ast_tree

if __name__ == '__main__':
    source = StringSource(
"""
a=[]
a.q = 'ass'
a.lol = function () { console.log('ass', this.q) }
a.lol()
""")
    lexer  = Lexer(source)
    parser = Parser(lexer)

    ast = parser.generate_abstract_syntax_tree()
    draw_ast_tree(ast)

    batch = Batch(ast)
    code = batch.generate_code()

    f = open('test.bat', 'w')
    f.write(code)
    f.close()
    print
    print
    print code
