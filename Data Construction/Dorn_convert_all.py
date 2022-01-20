import subprocess
from lxml import etree
import pandas as pd
import regex as re

path_Dorn = "../Dataset/Dorn"
data = pd.read_csv("../Dataset/Dorn.csv")
# some keywords to identify a Python or Cuda code snippet
judge_set_notJava = set(('def','using','include','const','->','define','struct','sizeof','typedef','namespace','cudafloat', 'float3', 'int2',
                         '__syncthreads', 'fprintf', 'OutputArray32', 'SHA_TRANSFORM'))
# some keywords to identify a Java code snippet
judge_set_java = set(('public','static','protected','private','extends','final','@Override'))
data_index = set()
# primitive data types and method return types in java
judge_list = ['byte', 'short', 'int', 'long', 'float', 'double', 'boolean', 'char', 'String', 'void', 'Object']
# all keywords in Java
keywords = ["abstract", "assert", "boolean", "break", "byte",
            "case", "catch", "char", "class", "const",
            "continue", "default", "do", "double", "else",
            "enum", "extends", "final", "finally", "float",
            "for", "goto", "if", "implements", "import",
            "instanceof", "int", "interface", "long", "native",
            "new", "package", "private", " protected", "public",
            "return", "strictfp", "short", "static", "super",
            "switch", "synchronized", "this", "throw", "throws",
            "transient", "try", "void", "volatile", "while"]

# record some names that are not identifiers
not_identifier = ['true', 'false', 'null',
            "abstract", "assert", "break",
            "case", "catch", "class", "const",
            "continue", "default", "do", "double", "else",
            "enum", "extends", "final", "finally",
            "for", "goto", "if", "implements", "import",
            "instanceof", "interface", "native",
            "new", "package", "private", " protected", "public",
            "return", "strictfp", "static", "super",
            "switch", "synchronized", "this", "throw", "throws",
            "transient", "try", "void", "volatile", "while"
            ]

# traverse 360 code snippets in Dorn
# this is used to identify whether the type a code snippet is Java or not
for i in range(0,360):
    index = "Dorn" + str(i)
    output = subprocess.run(['srcml.exe', path_Dorn + "\Dorn" + str(i) + ".java"], capture_output=True, check=False)
    root = etree.fromstring(output.stdout)
    # prevent comments and some expression from interfering with judgment
    comment_list = root.xpath('//*[local-name() = "comment"]')
    expr_list = root.xpath('./*[local-name() = "expr"]')
    for comment in comment_list:
        comment.getparent().remove(comment)
    for expr in expr_list:
        expr.getparent().remove(expr)

    # use XPath to read all content
    list = root.xpath("//text()")
    # use 'flag' to judge whether a code snippet is Java snippet
    # flag = 0  -->  the type of the code snippet is Java
    flag = 1
    # 'enter_loop' is used to record whether there is a pointer or '&'
    enter_loop = 1
    # Roughly judge whether there is a pointer in the function
    pointer_list = root.xpath('//*[local-name() = "argument"]/*[local-name() = "expr"]/*[local-name() = "operator"]')
    for element in pointer_list:
        if element.text == '*':
            enter_loop = 0

    # judge whether there is a pointer variable
    pointer_list = root.xpath('//*[local-name() = "expr"]/*[local-name() = "operator"]')
    for element in pointer_list:
        if element.text == '*':
            parent = element.getparent()
            new_list = parent.xpath('./*[local-name() = "operator"]')
            if len(new_list) == 1:
                enter_loop = 0
            elif len(new_list) == 2 and new_list[1].text == '=':
                enter_loop = 0

    # '&'
    address_list = root.xpath('//*[local-name() = "expr"]/*[local-name() = "operator"]')
    for element in address_list:
        if element.text == '&':
            enter_loop = 0

    # further judgment
    if enter_loop == 1:
        loop_continue = 0
        for content in list:
            # the content of the variable 'content' may contain many characters  (Dorn213)
            # we first split the variable 'content' with space
            content = str(content)
            for element in content.split():
                if element in judge_set_notJava:
                    flag = 1
                    loop_continue = 1
                    break
                elif element in judge_set_java:
                    flag = 0
                    # there may be a phenomenon that there is 'public' in the expression
                    # loop_continue = 1
                    break
                elif 'CUDA' in element.upper():
                    flag = 1
                    loop_continue = 1
                    break
                # if it is a java fragment, there must be ';'
                # prevent comment-only fragments from being judged as Java code fragments
                elif element == ';':
                    flag = 0
            if(loop_continue == 1):
                break

    if(flag == 0):
        data_index.add(i)

# remove some code snippets that cannot be detected as not Java
extra_list = [10, 32, 35, 60, 98, 140,
              145, 148, 162, 165, 203,
              210, 216, 239, 249, 253, 309]

for index in extra_list:
    if index in data_index:
        data_index.remove(index)

for index in data_index:
    print(index)
print(len(data_index))

for i in range(0,360):
    # index = "Dorn" + str(i)
    name_ID = data.iat[i,0]
    index = str(name_ID).replace('Dorn','')
    index = int(index)
    # judge whether the variable 'i' is in the 'data_index'
    if index not in data_index:
        data_fill = [name_ID, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                     0, 0, 0, 0, 0, 0, 0, 0, 0,
                     0, 0, 0, 0, 0, 0, 0, 0]
        data[i:i + 1] = data_fill
        continue

    output = subprocess.run(['srcml.exe', path_Dorn + "\Dorn" + str(index) + ".java"], capture_output=True, check=False)
    root = etree.fromstring(output.stdout)

    # ***********************************************************************************************************
    # count the number of lines in which the comment appears
    comment_list = root.xpath('//*[local-name() = "comment"]')
    comment_count = 0
    for comment in comment_list:
        text = comment.xpath('./text()')
        for element in text:
            if '\n' in element:
                comment_count += element.count('\n')
        comment_count += 1

    # calculate the number of total indentation, lines, and characters (including comments)
    list = root.xpath("//text()")
    total_content = root.xpath("//text()")
    line_count = 0
    line_char_sum = 0
    indentation_count = 0
    for element in list:
        if '\n' in element:
            line_count += element.count('\n')
            indentation_count += element.count('    ')
            indentation_count += element.count('\t')
            element = element.replace('\n', '')
            element = element.replace('\t', '    ')
        line_char_sum += len(element)
    # +1 manually because there is no '\n' on the last line
    line_count += 1

    # prevent row count from being 0
    if(line_count == 0):
        data_fill = [name_ID, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                      0, 0, 0, 0, 0, 0, 0, 0, 0,
                      0, 0, 0, 0, 0, 0, 0, 0]
        data[i - 1:i] = data_fill
        continue

    # ***********************************************************************************************************
    # first count the average line length and the maximum line length
    # maximum line length
    line_char_max = 0
    # record the current line character count
    line_char_count = 0
    # considering that some indentations are implemented with spaces, we consider indentation when counting char
    # Sc9, Buse1
    for element in list:
        if '\n' in element:
            # There is a special case here where the last newline character in a comment will appear alone
            if element == '\n':
                line_char_max = line_char_count if line_char_count >= line_char_max else line_char_max
                line_char_count = 0
                continue
            line_list = element.split('\n')
            length = len(line_list)
            # '\n' always appears with the indentation on the next line
            for index in range(length - 1):
                line = line_list[index]
                line = line.replace('\t', '    ')
                line_char_count += len(line)
                line_char_max = line_char_count if line_char_count >= line_char_max else line_char_max
                line_char_count = 0
            line = line_list[length - 1]
            line = line.replace('\t', '    ')
            line_char_count += len(line)
            continue
        line_char_count += len(element)

    max_line_length = line_char_max
    avg_line_length = line_char_sum / line_count
    # calculate the proportion of comments
    comment_percent = comment_count / line_count

    # remove all comments
    for comment in comment_list:
        comment.getparent().remove(comment)

    # remove the expression fragment at the beginning of the code
    expr_list = root.xpath('./*[local-name() = "expr"]')
    for expr in expr_list:
        expr.getparent().remove(expr)

    # XPath to read all content
    list = root.xpath("//text()")
    # reads all strings
    string_list = root.xpath('//*[local-name() = "literal"]')

    # ***********************************************************************************************************
    # calculate metrics related to identifiers
    # average identifier length
    avg_identifier_length = 0
    # maximum identifier length
    max_identifier_length = 0
    # average number of identifiers
    avg_identifier = 0
    # row maximum identifiers
    max_identifier = 0
    # maximum number of occurrences of an identifier
    max_single_identifier = 0
    # record all occurrences of identifiers
    identifier_set = set()
    # total number of identifiers
    identifier_count = 0
    # record the frequency of occurrence of each identifier
    identifier_freq = {}
    # get all that named by 'name' in the xml
    name_list = root.xpath('//*[local-name() = "name"]')
    # get all that named by 'type/name' in the xml
    type_list = root.xpath('//*[local-name() = "type"]/*[local-name() = "name"]')

    for element in name_list:
        if element.text is not None and element.text not in not_identifier:
            identifier_set.add(element.text)
            identifier_count += 1
            # record the frequency of occurrence of different identifiers
            if element.text in identifier_freq:
                identifier_freq[element.text] += 1
            else:
                identifier_freq[element.text] = 1
    for element in type_list:
        if element.text is not None and element.text in judge_list:
            identifier_count -= 1
            if element.text in identifier_set:
                identifier_set.remove(element.text)
            # if this identifier is misidentified, change the frequency of this identifier to 0
            identifier_freq[element.text] = 0

    # find the maximum number of occurrences of the identifier
    freq_max = 0
    for element in identifier_freq:
        freq_max = identifier_freq[element] if identifier_freq[element] >= freq_max else freq_max
    max_single_identifier = freq_max

    # row average identifiers
    avg_identifier = identifier_count / line_count
    count = 0
    # calculate the maximum number of identifiers in a row
    for element in list:
        # prevent the space at the end of the string from affecting the judgment
        element = element.replace(' ', '')
        if element in identifier_set:
            count += 1
        if '\n' in element:
            max_identifier = count if count >= max_identifier else max_identifier
            count = 0
    # avoid the case of only one line i.e. without '\n'
    if max_identifier == 0:
        max_identifier = count

    # record the length of identifiers
    total_length = 0
    max_length = 0

    # average and maximum length of identifiers
    for element in identifier_set:
        total_length += len(element)
        max_length = len(element) if len(element) >= max_length else max_length
    max_identifier_length = max_length
    avg_identifier_length = total_length / len(identifier_set)

    # ***********************************************************************************************************
    # count the number of symbols
    # '+'  '*'  '%'  '/' '-'
    arithmetic_count = 0
    arithmetic_list = ['+', '*', '%', '/', '-', '-=', '+=', '*=', '/=', '%=', '++', '--']
    # '=='  '<'  '>'  '>='  '<='  '!='
    comparison_count = 0
    comparison_list = ['==', '<', '>', '>=', '<=', '!=']
    # '='
    assignment_count = 0
    # some special cases of assignment symbols
    special_assignment = ['+=', '-=', '++', '--', '*=', '/=', '%=']
    # ','
    comma_count = 0
    # '.'
    dot_count = 0
    # ')' '}'
    bracket_count = 0
    # get all elements named by 'operator' in the xml
    operations = root.xpath('//*[local-name() = "operator"]')
    for operator in operations:
        element = operator.text
        element = element.strip()
        if element in arithmetic_list:
            arithmetic_count += 1
            if element in special_assignment:
                assignment_count += 1
        elif element in comparison_list:
            comparison_count += 1
        elif element == '.':
            dot_count += 1

    # ***********************************************************
    # here we need to judge whether '+' appears as a connection symbol of string
    # extra_count = 0
    # strings = root.xpath('//*[local-name() = "literal"]')
    # for s in strings:
    #     follow_operator = s.xpath('./following-sibling::*[local-name() = "operator"]')
    #     if len(follow_operator) != 0:
    #         x = follow_operator[0].text
    #         if x == "+":
    #             extra_count += 1
    #     above_operator = s.xpath('./preceding-sibling::*[local-name() = "operator"]')
    #     if len(above_operator) != 0:
    #         x = above_operator[0].text
    #         if x == "+":
    #             extra_count += 1

    # the arithmetic number calculated here is subtracted from the extra "+" number above
    # arithmetic_count -= extra_count
    # ***********************************************************

    avg_arithmetic = arithmetic_count / line_count
    avg_comparison = comparison_count / line_count
    avg_dot = dot_count / line_count
    # since '=' will be used in the initial assignment statement, it is not calculated in the above loop
    # ',' and '(' will appear in the function parameters in the same way, so they are also calculated separately
    for element in list:
        element = element.strip()
        if ',' in element:
            comma_count += element.count(',')
        if '(' in element or '{' in element:
            bracket_count += element.count('(') + element.count('{')
        # assignment symbols are divided separately in the xml
        if element == '=':
            assignment_count += 1

    # subtract the ',' and '(, {' that appear in the string
    for element in string_list:
        if element.text is not None:
            element = element.text
            if "," in element:
                comma_count -= element.count(",")
            if "(" in element or "{" in element:
                bracket_count -= element.count("(")
                bracket_count -= element.count("{")

    avg_comma = comma_count / line_count
    avg_bracket = bracket_count / line_count
    avg_assignment = assignment_count / line_count

    # ***********************************************************************************************************
    # count blank lines
    blank_line_count = 0
    for element in list:
        if '\n\n' in element:
            # prevent multiple blank lines from appearing in a row
            blank_line_count += element.count('\n') - 1
    avg_blank = blank_line_count / line_count

    # ***********************************************************************************************************
    # count keywords
    keyword_count = 0
    max_keyword = 0
    count = 0
    for element in list:
        # prevent the ';' behind keywords interfere with judgment
        # i.e.   return a;
        element = element.replace(';', ' ')
        # the keywords such as else and if will appear together
        # i.e.   'else if'
        element_list = element.split(' ')
        for text in element_list:
            if text in keywords:
                keyword_count += 1
                count += 1
            if '\n' in element:
                max_keyword = count if count >= max_keyword else max_keyword
                count = 0
    avg_keyword = keyword_count / line_count

    # ***********************************************************************************************************
    # calculate loop and if statement
    avg_loop = 0
    avg_if = 0
    for_list = root.xpath('//*[local-name() = "for"]')
    # Sc87
    while_list = root.xpath('//*[local-name() = "while"]')
    avg_loop = (len(for_list) + len(while_list)) / line_count
    # Sc197
    if_list = root.xpath('//*[local-name() = "if"]')
    # Sc15 Buse14
    # The choice here is the 'else' in if_stmt to prevent the ternary operator '?' interference
    else_list = root.xpath('//*[local-name() = "if_stmt"]/*[local-name() = "else"]')
    avg_if = (len(if_list) + len(else_list)) / line_count

    # ***********************************************************************************************************
    # calculate indentation and spaces
    # average number of spaces in a line
    avg_space = 0
    # total number of spaces
    space_count = 0
    # maximum line indentation
    max_indentation = 0
    # average line indentation
    # blank lines are not included here
    avg_indentation = indentation_count / (line_count - blank_line_count)
    for element in list:
        # indentation usually occurs with the newline character \n (only \n and \t occur)
        # Buse12
        temp = element.count('\n')
        if temp == 1:
            # some indentations appear in the form of spaces
            element = element.replace('\t', '    ')
            element = element.replace('\n', '')
            length = element.count(' ')
            # count spaces
            space_count += length % 4
            length = length - length % 4
            indent = length / 4
            max_indentation = indent if indent >= max_indentation else max_indentation
        elif temp > 1:
            temp_list = element.split('\n')
            for index in range(temp):
                temp_element = temp_list[index]
                if temp_element == '':
                    continue
                temp_element = temp_element.replace('\t', '    ')
                length = temp_element.count(" ")
                # count spaces
                space_count += length % 4
                length = length - length % 4
                indent = length / 4
                max_indentation = indent if indent >= max_indentation else max_indentation
        elif ' ' in element:
            space_count += element.count(' ')
    # subtract the number of spaces that appear in the string
    string_list = root.xpath('//*[local-name() = "literal" and @type = "string"]')
    for element in string_list:
        element = element.text
        space_count -= element.count(' ')
    avg_space = space_count / line_count

    # ***********************************************************************************************************
    # calculate the average number of numbers and the max number of numbers 
    avg_number = 0
    max_number = 0
    count = 0
    number_list = root.xpath('//*[local-name() = "literal" and @type = "number"]')
    avg_number = len(number_list) / line_count
    pattern = re.compile('[0-9]+')
    for element in list:
        match = pattern.findall(element)
        if match:
            count += 1
        if '\n' in element:
            max_number = count if count >= max_number else max_number
            count = 0

    # ***********************************************************************************************************
    # count the maximum number of occurrences of a character
    char_freq = {}
    max_single_char = 0
    for element in list:
        element = element.replace(' ', '')
        if '\n' in element:
            element = element.replace('\n', '')
            element = element.replace('\t', '')
        for c in element:
            if c in char_freq:
                char_freq[c] += 1
            else:
                char_freq[c] = 1
    for c in char_freq:
        max_single_char = char_freq[c] if char_freq[c] >= max_single_char else max_single_char
    # ***********************************************************************************************************

    score = data.iat[i, 26]
    # limit the number of decimal places
    avg_identifier_length = round(avg_identifier_length, 4)
    avg_identifier = round(avg_identifier, 4)
    avg_arithmetic = round(avg_arithmetic, 4)
    avg_comparison = round(avg_comparison, 4)
    avg_assignment = round(avg_assignment, 4)
    avg_comma = round(avg_comma, 4)
    avg_dot = round(avg_dot, 4)
    avg_bracket = round(avg_bracket, 4)
    avg_keyword = round(avg_keyword, 4)
    avg_number = round(avg_number, 4)
    avg_loop = round(avg_loop, 4)
    avg_if = round(avg_if, 4)
    avg_space = round(avg_space, 4)
    avg_indentation = round(avg_indentation, 4)
    avg_blank = round(avg_blank, 4)
    avg_line_length = round(avg_line_length, 4)
    comment_percent = round(comment_percent, 4)
    data_fill = [name_ID, avg_identifier_length, max_identifier_length, avg_identifier, max_identifier,
                 max_single_identifier, avg_arithmetic, avg_comparison, avg_assignment, avg_comma, avg_dot,
                 avg_bracket, max_keyword, avg_keyword, max_number, avg_number, avg_loop, avg_if,
                 avg_space, max_indentation, avg_indentation, comment_percent, max_single_char, avg_blank,
                 max_line_length, avg_line_length, score
                 ]
    data[i:i + 1] = data_fill

# save
data.to_csv("../Result/data_Dorn_all.csv", index=False)