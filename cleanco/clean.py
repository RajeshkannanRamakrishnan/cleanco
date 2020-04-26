"""Functions to help clean & normalize business names.

See http://www.unicode.org/reports/tr15/#Normalization_Forms_Table for details
on Unicode normalization and the NFKD normalization used here.

Basic usage:

>> terms = get_terms()
>> clean_name("Daddy & Sons, Ltd.", terms)
Daddy & Sons

"""

import functools
import operator
from collections import OrderedDict
import re
import unicodedata
from iso20275 import ElfEntry


tail_removal_rexp = re.compile(r"[^\.\w]+$", flags=re.UNICODE)


def get_terms():
    terms = []

    for elf_code, values in Elf.items():
        entity_codes = Elf[elf_code][0].local_abbreviations
        if ";" in entity_codes:
            split = entity_codes.split(';')
            for split_item in split:
                terms.append(split_item)
        else:
            terms.append(entity_codes)
    
    terms = filter(None, terms)
    terms = list(filter(None, terms))
    return (terms)

def strip_tail(name):
    "Get rid of all trailing non-letter symbols except the dot"
    match = re.search(tail_removal_rexp, name)
    if match is not None:
        name = name[: match.span()[0]]
    return name


def normalized(text):
    "caseless Unicode normalization"
    return unicodedata.normalize("NFKD", text.casefold())


def basename(name, terms, suffix=True, prefix=False, middle=False, multi=False):
    "return cleaned base version of the business name"

    name = strip_tail(name)
    parts = name.split()
    nparts = [normalized(p) for p in parts]

    # return name without suffixed/prefixed/middle type term(s)
    for term in (normalized(t) for t in terms):
        if suffix and nparts[-1] == term:
            del nparts[-1]
            del parts[-1]
            if multi == False:
                break
        if prefix and nparts[0] == term:
            del nparts[0]
            del parts[0]
            if multi == False:
                break
        if middle:
            try:
                idx = nparts.index(term)
            except ValueError:
                pass
            else:
                del nparts[idx]
                del parts[idx]
            if multi == False:
                break

    return strip_tail(" ".join(parts))


