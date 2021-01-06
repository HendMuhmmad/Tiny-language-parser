#EBNF

"""
program→ stmt-sequence
stmt-sequence → statement {; statement}
statement→ if-stmt | repeat-stmt | assign-stmt | read-stmt | write-stmt
if-stmt → if exp then stmt-sequence [else stmt-sequence] end
repeat-stmt → repeat stmt-sequence until exp
assign-stmt → identifier := exp
read-stmt → read identifier
write-stmt → write exp
exp → simple-exp [comparison-op simple-exp]
comparison-op → < | =
simple-exp → term {addop term}
addop → + | -
term → factor {mulop factor}
mulop → * | /
factor → (exp) | number | identifier

"""
import pydot
import random

class Parser:
    
    def __init__(self,tokens_table):
        self.tokens_table = tokens_table
        self.counter = 0
        self.max_counter = len(tokens_table)
        self.syntax_tree = pydot.Dot(graph_type='graph',rankdir = "TB")
        self.id_counter = 0
    
    
    def match(self,expected_token):
        if self.counter == self.max_counter:
            return 0 # error-end-of-tokens

        if self.tokens_table[self.counter]["token_type"] == expected_token:
            token_val = self.tokens_table[self.counter]["token_value"]
            self.counter = self.counter + 1
            return token_val # match-found
        else:
            return  0 # error-no-match

    def stmt_sequence(self):
        # stmt-sequence → statement {; statement}
        r = lambda: random.randint(0,255)
        rand_color = ('#%02X%02X%02X' % (r(),r(),r()))
        stmt_node = self.statement()
        temp_node = stmt_node
        # if (self.counter < self.max_counter) and (self.tokens_table[self.counter]["token_type"] != 'SEMICOLON'):
        #     raise Exception("No semi-colon found")
        while self.match("SEMICOLON"):
            stmt_node_n = self.statement()
            #to be connected horizontally
            self.syntax_tree.add_edge(pydot.Edge(temp_node,stmt_node_n,constraint=False,color = rand_color))
            temp_node = stmt_node_n

        self.syntax_tree.write_png("syntax_tree.png")
        return stmt_node

        
    def statement(self):
        # statement→ if-stmt | repeat-stmt | assign-stmt | read-stmt | write-stmt
        if self.match("IF"):
            return self.if_stmt()      

        elif self.match("REPEAT"):
            return self.repeat_stmt()

        elif self.match("READ"):

            id = self.read_stmt()
            read_node = pydot.Node(str(self.id_counter), label=f"read\n({id})", shape="rect",rank="same")
            self.syntax_tree.add_node(read_node)
            self.id_counter = self.id_counter + 1
            return read_node

        elif self.match("WRITE"):

            write_node = pydot.Node(str(self.id_counter), label=f"write", shape="rect",rank="same")
            self.syntax_tree.add_node(write_node)
            self.id_counter = self.id_counter + 1
            stmt_node = self.write_stmt()
            self.syntax_tree.add_edge(pydot.Edge(write_node,stmt_node))
            return write_node

            
        elif self.match("IDENTIFIER"):

            id = self.tokens_table[self.counter-1]["token_value"]
            assign_node = pydot.Node(str(self.id_counter), label=f"assign\n({id})", shape="rect",rank="same")
            self.syntax_tree.add_node(assign_node)
            self.id_counter = self.id_counter + 1
            node = self.assign_stmt()
            self.syntax_tree.add_edge(pydot.Edge(assign_node,node))
            return assign_node

        else:
            raise Exception("No match found")
            
    
    def if_stmt(self):
        # if-stmt → if exp then stmt-sequence [else stmt-sequence] end
        if_node = pydot.Node(str(self.id_counter), label=f"if", shape="rect",rank="same")
        self.syntax_tree.add_node(if_node)
        self.id_counter = self.id_counter + 1
        exp_node = self.exp()
        if self.match("THEN"):
            then_node = self.stmt_sequence()
            self.syntax_tree.add_edge(pydot.Edge(if_node,exp_node))
            self.syntax_tree.add_edge(pydot.Edge(if_node,then_node))

        else:
            raise Exception("No match found")

        if self.match("ELSE"):
            else_node = self.stmt_sequence()
            self.syntax_tree.add_edge(pydot.Edge(if_node,else_node,style="dotted"))
        
        if not self.match("END"):
            raise Exception("No match found")

        return if_node

    def repeat_stmt(self):
        # repeat-stmt → repeat stmt-sequence until exp
        repeat_node = pydot.Node(str(self.id_counter), label=f"repeat", shape="rect",rank="same")
        self.syntax_tree.add_node(repeat_node)
        self.id_counter = self.id_counter + 1
        stmt_node = self.stmt_sequence()
        if self.match("UNTIL"):
            exp_node = self.exp()
            self.syntax_tree.add_edge(pydot.Edge(repeat_node,stmt_node))
            self.syntax_tree.add_edge(pydot.Edge(repeat_node,exp_node))
        else:
            raise Exception("No match found")

        return repeat_node

    def read_stmt(self):
        # read-stmt → read identifier
        id = self.match("IDENTIFIER")
        if id:
            return id
        else:
            raise Exception("No match found")


    def write_stmt(self):
        # write-stmt → write exp
        return self.exp()

    def assign_stmt(self):
        # assign-stmt → identifier := exp
        if self.match("ASSIGN"):
            assign_node = self.exp()
            return assign_node
        else:
            raise Exception("No match found")

    def exp(self):
        # exp → simple-exp [comparison-op simple-exp]
        # comparison-op → < | =
        simple_exp_node = self.simple_exp()
        if self.match("LESS THAN") or self.match("EQUAL"):
            op = self.tokens_table[self.counter-1]["token_value"]
            op_node = pydot.Node(str(self.id_counter), label=f"op\n({op})")
            self.syntax_tree.add_node(op_node)
            self.id_counter = self.id_counter + 1
            simple_exp_node2 = self.simple_exp()
            self.syntax_tree.add_edge(pydot.Edge(op_node,simple_exp_node))
            self.syntax_tree.add_edge(pydot.Edge(op_node,simple_exp_node2))
            simple_exp_node = op_node

        return simple_exp_node 

    def simple_exp(self):
        # simple-exp → term {addop term}
        # addop → + | -
        term_node = self.term()
        while self.match("PLUS") or self.match("MINUS"):
            op = self.tokens_table[self.counter-1]["token_value"]
            op_node = pydot.Node(str(self.id_counter), label=f"op\n({op})")
            self.syntax_tree.add_node(op_node)
            self.id_counter = self.id_counter + 1
            term_node2 = self.term()
            self.syntax_tree.add_edge(pydot.Edge(op_node,term_node))
            self.syntax_tree.add_edge(pydot.Edge(op_node,term_node2))
            term_node = op_node
        return term_node

    def term(self):
        # term → factor {mulop factor}
        # mulop → * | /
        factor_node = self.factor()
        while self.match("MULTIPLY") or self.match("DIVIDE"):
            op = self.tokens_table[self.counter-1]["token_value"]
            op_node = pydot.Node(str(self.id_counter), label=f"op\n({op})")
            self.syntax_tree.add_node(op_node)
            self.id_counter = self.id_counter + 1
            factor_node2 = self.factor()
            self.syntax_tree.add_edge(pydot.Edge(op_node,factor_node))
            self.syntax_tree.add_edge(pydot.Edge(op_node,factor_node2))
            factor_node = op_node

        return factor_node

    def factor(self):
        # factor → (exp) | number | identifier
        if self.match("LEFT BRACKET"):
            exp_node = self.exp()
            if not self.match("RIGHT BRACKET"):
                raise Exception("No match found")
            return exp_node
        elif self.match("NUMBER"):
            const  = self.tokens_table[self.counter-1]["token_value"]
            const_node = pydot.Node(str(self.id_counter), label=f"const\n({const})")
            self.id_counter = self.id_counter + 1
            self.syntax_tree.add_node(const_node)
            return const_node
        
        elif self.match("IDENTIFIER"):
            id  = self.tokens_table[self.counter-1]["token_value"]
            id_node = pydot.Node(str(self.id_counter), label=f"id\n({id})")
            self.syntax_tree.add_node(id_node)
            self.id_counter = self.id_counter + 1
            return id_node

        else:
            raise Exception("No match found")