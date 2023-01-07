import re

def replace_ru_to_eng(text):
    """
    This function replaces all Russian letters that look like English letters with English letters.
    :param text: initial text
    :return: result text
    """
    eng = 'ABCEHKMOPTX'
    rus = 'АВСЕНКМОРТХ'
    for letter in text:
        if letter in rus:
            text = text.replace(letter, eng[rus.index(letter)])
    return text


def get_data_with_re(text):
    """
    This function receives text and extracts unit number, spare parts part number and quantity from it.
    :param text: initial text
    :return:  A tuple of unit number, spare parts part number and quantity. (unit_number, part_number, qty)
    """
    qty_re = r'\s\d{1,2}\b'
    unit_number_re = r'[KkCc]-[\w/\\-]+'
    command_re = r'^\/[aA][dD]*'

    qty = int(re.findall(qty_re, text)[0].strip())
    unit_number = re.findall(unit_number_re, text)[0]
    command = re.findall(command_re, text)[0]
    part_number = re.sub(command, '', re.sub(unit_number_re, '', re.sub(qty_re, '', text))).strip()
    if "\\" in unit_number:
        unit_number = unit_number.replace('\\', '/')
    if unit_number.count('-') > 1:
        unit_number = unit_number.replace('-', '/')
        unit_number = unit_number.replace('/', '-', 1)

    return unit_number, part_number, qty


