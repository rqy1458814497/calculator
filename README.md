#A Small Interperter
##Version 2.0
Using a unnaming language(maybe I will name it 'RQY-language', after I finish it).

##Files:
* Constants.py Defines some constants.
* Lexer.py Includes class *Token* and *Lexer*.
* Parser.py Includes class *Parser* and *AST*, *AST_Num*, *AST_ID*, etc.
* ASTVisiter.py Includes class *ASTVisiter*.
* main.py The entry point to the program. Includes **main()**, **runcmd()**
* spi.py Five files in one. Including all content of files above.

##Support syntax:
###Name:
Like other languages, a name (of a variable or a function) begins with letters or '\_', and only includes letters, '\_' and digits.
###Number:
Numbers can be '1', '3', '3e4', '3.3', '.3e5', but not '.e4', '1.'(in other words, there must be sometihing after '.', or between '.' and 'e').
###Expression:
Some number, variable or function call with unary operators('+' or '-') connected with binary operators('+', '-', '\*', '/', '^'(pow), '==', '!=', '>', '<', '>=', '<=', '=') and parentheses, for example,
    1+3
    -a+4
    f(1, a, a+7)
    1------4 *it means 1-(-(-(-(-(-4)))))*
    (s+4 <= 0) == 0
'^' and '=' are right-associative, and others are left-associative.
Priority levels of binary operators(from lowest to highest):
=
== !=
\> \< \>= \<=
\+ \-
\* /
^
###Statement:
Pay attention: No ';' after any statement(at least in v2.0).
1. **expression** It won't do anything without assign. Pay attention: function call also belong to it.
2. **print expression** Output the value of expression.
3. **return expression** Return from a function(so you can't write it ouside any function).
4. **'{'stat stat stat ...'}'** A statement bolck.
5. **'while' '('condition')' stat**  While loop.
6. **'if' '('condition')' stat [else stat]** If statement or if-else statement.
###Function:
Function definitions are begin with reserved word 'func', such as:
    func fac(n) {
      return n
    }
You can't define functions in another function.
Support recurse function.
