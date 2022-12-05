ascii_uppercase = 'BCDEFGHIJKLMNOPQRSTUVWXYZ'


def group_by(lst, kw):
    '''This is a function creates list of list by keyword.'''
    # using list comprehension + zip() + slicing + enumerate()
    # Split list into lists by particular value
    size = len(lst)
    idx_list = [idx + 1 for idx, val in enumerate(lst) if val == kw]

    res = [lst[i: j] for i, j in
           zip([0] + idx_list, idx_list +
               ([size] if idx_list[-1] != size else []))]
    return res


def flat_tag(tags):
    '''This is a function converts tag obj to a flat list of string.'''
    str_list = []
    for tag in tags:
        string_in_a_box = []
        for string in tag.stripped_strings:
            string_in_a_box.append(string)
        if len(string_in_a_box) > 1:
            string_in_a_box = '\n'.join(string_in_a_box)
        else:
            string_in_a_box = ''.join(string_in_a_box)
        str_list.append(string_in_a_box)
    return str_list


def flat_tag2(tags):
    '''This function flats the string from <td>.'''
    str_list = []
    for tag in tags:
        p_tags = tag.find_all('p')
        for p_tag in p_tags:
            for str_row in p_tag.stripped_strings:
                str_row += f'{str_row}\n'
            str_list.append(str_row)
    return str_list


def newline_alphabet(w):
    '''This function add a newline before the first uppercase except 'A'. '''
    ascii_uppercase = 'BCDEFGHIJKLMNOPQRSTUVWXYZ'
    idx = 0
    for i in w:
        if i in ascii_uppercase:
            idx = w.index(i)
            break
    new = w[:idx] + '\n' + w[idx:]
    return new


def newline_chieng(w):
    '''This function adds a newline between Chinese and English, except 'A'.'''
    try:
        for i in range(len(w)):
            if u'\u4e00' < w[i] < u'\u9fff' and w[i + 1] in ascii_uppercase:
                w = w[:i + 1] + '\n' + w[i + 1:]

            if u'\u4e00' < w[i] < u'\u9fff' and w[i - 1] in ascii_uppercase:
                w = w[:i] + '\n' + w[i:]

            if w[i] == ')':
                w = w[:i + 1] + '\n' + w[i + 1:]
    except IndexError:
        pass

    return w


def tags2strlist(tags):
    str_list = []
    for tag in tags:
        p_tags = tag.find_all('p')
        box = ''
        for p_tag in p_tags:
            row = ''
            for w in p_tag.stripped_strings:
                row += w
            box += row + '\n'
        while len(box) > 0  and box[-1] == '\n':
            box = box[:-1]
        str_list.append(box)

        # str_list.append(newline_alphabet(box))
    # for s in str_list:
    #     if s == '\n':
    #         s.replace('\n', '')
    return str_list
