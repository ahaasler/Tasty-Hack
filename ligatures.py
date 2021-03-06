from functools import reduce
from glob import glob
from char_mapping import char_name_dict, char_dict


def create_fira_ligatures_def(pattern):
    """ Create ligatures definition by reading a text file contains full list of ligatures
    :param pattern: glob pattern
    :return:
    """
    def get_ligatures_from_files(files):
        lines = []
        for file in files:
            with open(file, 'r') as f:
                for line in f:
                    lines.append(line.strip().split(' '))
        return reduce(list.__add__, lines)

    def is_valid_ligature(ligature):
        # not empty and all chars exist in the dictionary
        return ligature != '' and reduce(lambda acc, c: acc and c in char_name_dict, list(ligature), True)

    def ligature_to_def(ligature):
        chars = list(map(lambda c: char_name_dict[c], list(ligature)))
        firacode_ligature_name = reduce(lambda acc, e: '{}_{}'.format(acc, e), chars) + '.liga'
        return {
            'chars': chars,
            'firacode_ligature_name': firacode_ligature_name
        }

    xs = list(filter(is_valid_ligature, get_ligatures_from_files(files = glob(pattern))))
    defs = list(map(ligature_to_def, xs))

    print("Prepared to add these ligatures:", xs)
    return defs


# 'COPY_CHARACTER_GLYPHS' feature required to prepend the punctuations characters
ligatures = [{'chars': list(char_dict.keys()), 'firacode_ligature_name': None}] \
            + create_fira_ligatures_def(pattern = 'fonts/fira/showcases/showcases.txt')

print("Definitions:", ligatures)
