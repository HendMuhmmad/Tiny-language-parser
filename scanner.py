from re import sub
import csv

class Scanner:
    def __init__(self,code):
        self.code = code
        self.scanner_table = []
        self.reseverd_words = {
                        "if":"IF",
                        "then":"THEN",
                        "else":"ELSE",
                        "end":"END",
                        "repeat":"REPEAT",
                        "until":"UNTIL",
                        "read":"READ",
                        "write":"WRITE"}
        self.special_sympols = {
                        "+":"PLUS",
                        "-":"MINUS",
                        "*":"MULTIPLY",
                        "/":"DIVIDE",
                        "=":"EQUAL",
                        ":=":"ASSIGN",
                        "<":"LESS THAN",
                        "(":"LEFT BRACKET",
                        ")":"RIGHT BRACKET",
                        ";":"SEMICOLON",  
                    }

    def get_tokens(self):
        semi_colon = 0
        no_tabs = self.code.replace('\t', ' ')
        no_comments = sub('{[^}]+}', '', no_tabs)
        statments = no_comments.split('\n')
        statments = list(filter(None,statments))
        for statment in statments:
            tokens = statment.split(' ')
            tokens = list(filter(None,tokens))
            for token in tokens:
                if token[-1] == ";":
                    semi_colon = 1
                    token = token[0:-1]
                if token in self.reseverd_words:
                    self.scanner_table.append({"token_type":self.reseverd_words[token],"token_value":token})
                elif token in self.special_sympols:
                    self.scanner_table.append({"token_type":self.special_sympols[token],"token_value":token})
                elif token.isalpha():
                    self.scanner_table.append({"token_type":"IDENTIFIER","token_value":token})
                elif token.isnumeric():
                    self.scanner_table.append({"token_type":"NUMBER","token_value":token})  
            if semi_colon == 1:
                semi_colon = 0    
                self.scanner_table.append({"token_type":"SEMICOLON","token_value":";"})
        with open("tokens_table.csv", "w") as f:
            writer = csv.DictWriter(f, fieldnames=self.scanner_table[0].keys())
            writer.writeheader()
            for data in self.scanner_table:
                writer.writerow(data)
        return self.scanner_table



    



                
                
                   



            






