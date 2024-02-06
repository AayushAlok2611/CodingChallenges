class JsonParsingService:
    """
    This accepst json in the format of string and returns python's dictionary
    """
    OPEN_CURLY_BRACE = '{'
    CLOSE_CURLY_BRACE = '}'
    COMMA = ','
    COLON = ':'
    DECIMAL = '.'
    OPEN_SQAURE_BRACE = '['
    CLOSE_SQUARE_BRACE = ']'
    DOUBLE_QUOTE = '"'

    def __init__(self,json_string) -> None:
        self.json_string = self.get_json_string_after_skipping_unncessary_characters(json_string)
        self.idx = 0
    
    def is_char_needed(self,ch):
        is_significant_character = ch in [
            self.OPEN_CURLY_BRACE,
            self.CLOSE_CURLY_BRACE,
            self.OPEN_SQAURE_BRACE,
            self.CLOSE_SQUARE_BRACE,
            self.COLON,
            self.COMMA,
            self.DOUBLE_QUOTE,
            self.DECIMAL,
        ]
        return ch.isalpha() or ch.isdigit() or is_significant_character
    
    def consume(self,char):
        while self.idx < len(self.json_string) and self.json_string[self.idx]==char:
            self.idx += 1
    
    def get_json_string_after_skipping_unncessary_characters(self, json_string):
        ans = ""
        i = 0
        while i < len(json_string):
            if self.is_char_needed(json_string[i]):
                ans = ans + json_string[i]
            i += 1
        return ans

    
    def parse_value(self):
        currentChar = self.json_string[self.idx]
        
        if currentChar == self.OPEN_CURLY_BRACE:
            return self.parse_object()
        elif currentChar == self.OPEN_SQAURE_BRACE:
            return self.parse_array()
        elif currentChar == self.DOUBLE_QUOTE:
            return self.parse_string()
        elif currentChar.isdigit() or currentChar == '-':
            return self.parse_number()
        elif currentChar == 't' or currentChar == 'f':
            return self.parse_boolean()
        elif currentChar == 'n': 
            return self.parse_null()

        raise Exception("Invalid JSON")
    


    def parse_object(self):
        properties = dict()

        # move idx
        self.consume(self.OPEN_CURLY_BRACE)

        while self.idx< len(self.json_string) and self.json_string[self.idx]!=self.CLOSE_CURLY_BRACE:

            key = self.parse_string()

            self.consume(self.COLON)

            value = self.parse_value()

            properties[key] = value

            # Check for a comma, indicating more properties
            if self.json_string[self.idx] == self.COMMA:
                self.consume(self.COMMA)

        # move idx ahead of closing curly brace
        self.consume(self.CLOSE_CURLY_BRACE)
        return properties

    def parse_array(self):
        # move idx ahead of opening square brace
        self.consume(self.OPEN_SQAURE_BRACE) 

        elements = []
        while self.idx< len(self.json_string) and self.json_string[self.idx]!=self.CLOSE_SQUARE_BRACE:
            # Parse array element
            element = self.parse_value()
            elements.append(element)


            # Check for a comma, indicating more elements
            if self.json_string[self.idx] == self.COMMA:
                self.consume(self.COMMA)
            
        # move idx ahead of closing sqaure brace
        self.consume(self.CLOSE_SQUARE_BRACE)
        return elements

    def parse_number(self):
        startIndex = self.idx

        # Consume digits and optional decimal point
        while self.json_string[self.idx].isdigit() or self.json_string[self.idx]== '.':
            self.idx += 1

        numberStr = self.json_string[startIndex: self.idx]
        return float(numberStr)

    def parse_boolean(self): 
        boolStr = ""

        while self.idx < len(self.json_string) and self.json_string[self.idx].isalpha():
            boolStr = boolStr + self.json_string[self.idx]
            self.idx += 1
        

        if boolStr == "true":
            return True
        elif boolStr == "false":
            return False

        raise Exception("Invalid boolean value")

    def parse_null(self):
        # moving self.idx ahead "null"
        while self.idx < len(self.json_string) and self.json_string[self.idx].isalpha():        
            self.idx += 1
        return None

    def parse_string(self):
        # move idx ahead of starting double quote
        self.consume(self.DOUBLE_QUOTE)

        key = ""
        while self.idx < len(self.json_string) and self.json_string[self.idx]!=self.DOUBLE_QUOTE:
            key = key + self.json_string[self.idx]
            self.idx += 1

        # move idx ahead of ending double quote
        self.consume(self.DOUBLE_QUOTE)
        return key

    def parse(self): 
        # skipping whitespaces between start of jsonString and 1st {
        return self.parse_value()
