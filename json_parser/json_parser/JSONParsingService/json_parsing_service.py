
class JsonParsingService:
    OPEN_CURLY_BRACE = '{'
    CLOSE_CURLY_BRACE = '}'
    COMMA = ','
    COLON = ':'
    DECIMAL = '.'
    OPEN_SQAURE_BRACE = '['
    CLOSE_SQUARE_BRACE = ']'
    DOUBLE_QUOTE = '"'

    def __init__(self,json_string) -> None:
        self.json_string = json_string
        self.idx = 0
    

    def skipWhitespaces(self):
        while self.idx < len(self.json_string) and self.json_string[self.idx]==' ':
            self.idx += 1
    
    def consume(self,char):
        while self.idx < len(self.json_string) and self.json_string[self.idx]==char:
            self.idx += 1
    
    
    
    def parseValue(self):
        currentChar = self.json_string[self.idx]

        if currentChar == self.OPEN_CURLY_BRACE:
            return self.parseObject()
        elif currentChar == self.OPEN_SQAURE_BRACE:
            return self.parseArray()
        elif currentChar == self.DOUBLE_QUOTE:
            return self.parseString()
        elif currentChar.isdigit() or currentChar == '-':
            return self.parseNumber()
        elif currentChar == 't' or currentChar == 'f':
            return self.parseBoolean()
        elif currentChar == 'n': 
            return self.parseNull()

        raise Exception("Invalid JSON")
    


    def parseObject(self):
        # skip whit spaces between { and first key's double quote
        self.skipWhitespaces()
        properties = dict()

        # move idx
        self.consume(self.OPEN_CURLY_BRACE)

        while self.idx< len(self.json_string) and self.json_string[self.idx]!=self.CLOSE_CURLY_BRACE:
            key = self.parseString()

            self.skipWhitespaces()
            self.consume(self.COLON)

            value = self.parseValue()
            properties[key] = value

            self.skipWhitespaces()

            # Check for a comma, indicating more properties
            if self.json_string[self.idx] == self.COMMA:
                self.consume(self.COMMA)
                self.skipWhitespaces()
        
        # move idx ahead of closing curly brace
        self.consume(self.CLOSE_CURLY_BRACE)
        return properties

    def parseArray(self):
        # move idx ahead of opening square brace
        self.consume(self.OPEN_SQAURE_BRACE) 
        self.skipWhitespaces()

        elements = []
        while self.idx< len(self.json_string) and self.json_string[self.idx]!=self.CLOSE_SQUARE_BRACE:
            # Parse array element
            element = self.parseValue()
            elements.append(element)

            self.skipWhitespaces()

            # Check for a comma, indicating more elements
            if self.json_string[self.idx] == self.COMMA:
                self.consume(self.COMMA)
                self.skipWhitespaces()
            
        # move idx ahead of closing sqaure brace
        self.consume(self.CLOSE_SQUARE_BRACE)
        return elements

    def parseNumber(self):
        startIndex = self.idx

        # Consume digits and optional decimal point
        while self.json_string[self.idx].isdigit() or self.json_string[self.idx]== '.':
            self.idx += 1

        numberStr = self.json_string[startIndex, self.idx]
        return float(numberStr)

    def parseBoolean(self): 
        boolStr = ""

        while self.idx < len(self.json_string) and self.json_string[self.idx].isalpha():
            boolStr = boolStr + self.json_string[self.idx]
            self.idx += 1
        

        if boolStr == "true":
            return True;
        elif boolStr == "false":
            return False

        raise Exception("Invalid boolean value")

    def parseNull(self):
        # moving self.idx ahead "null"
        while self.idx < len(self.json_string) and self.json_string[self.idx].isalpha():        
            self.idx += 1
        return None

    def parseString(self):
        # move idx ahead of starting double quote
        self.consume(self.DOUBLE_QUOTE)

        self.skipWhitespaces()

        key = ""
        while self.idx < len(self.json_string) and self.json_string[self.idx]!=self.DOUBLE_QUOTE:
            key = key + self.json_string[self.idx]
            self.idx += 1

        # move idx ahead of ending double quote
        self.consume(self.DOUBLE_QUOTE)
        return key

    def parse(self): 
        # skipping whitespaces between start of jsonString and 1st {
        self.skipWhitespaces() 
        return self.parseValue()
