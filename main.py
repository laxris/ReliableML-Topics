#!/usr/bin/python3

import sys
from collections import Counter
import itertools
from operator import add
import IEEE_general
from general import get_keywords_of_single_abstract_RAKE, get_keywords_of_single_abstract_grams


METHOD = get_keywords_of_single_abstract_grams


# Avoids some strange unicode error...
# <http://stackoverflow.com/questions/21129020/how-to-fix-unicodedecodeerror-ascii-codec-cant-decode-byte>
reload(sys)
sys.setdefaultencoding('utf8')


DETAILS = dict()
# Journals
"""
DETAILS['IEEE_FS'] = ('IEEE Transactions on Fuzzy Systems', 8.746)
DETAILS['IEEE_SMCB'] = ('IEEE Transactions on Systems, Man, and Cybernetics, Part B (Cybernetics)', 6.220)
DETAILS['IEEE_TPAMI'] = ('IEEE Transactions on Pattern Analysis and Machine Intelligence', 5.781)
DETAILS['IEEE_NN_LS'] = ('IEEE Transactions on Neural Networks and Learning Systems', 4.291)
DETAILS['IEEE_EC'] = ('IEEE Transactions on Evolutionary Computation', 3.654)
DETAILS['IEEE_NN'] = ('IEEE Transactions on Neural Networks', 2.633)
DETAILS['IEEE_CIM'] = ('IEEE Computational Intelligence Magazine', 2.571)
DETAILS['IEEE_ASLP'] = ('IEEE Transactions on Audio, Speech and Language Processing', 2.475)
DETAILS['IEEE_MI'] = ('IEEE Transactions on Medical Imaging', 3.390)
DETAILS['IEEE_IS'] = ('IEEE Intelligent Systems', 2.340)
DETAILS['IEEE_KDA'] = ('IEEE Transactions on Knowledge and Data Engineering', 2.067)
"""

# Conferences
DETAILS['IEEE_NETWORKING'] = ('IFIP Networking', 1)
DETAILS['IEEE_CNSM'] = ('CNSM', 1)
DETAILS['IEEE_LCN'] = ('IEEE Local Computer Networks', 1)
DETAILS['INFOCOM'] = ('IEEE INFOCOM', 1)
DETAILS['INFO_WORKSHOP'] = ('IEEE INFOCOM Workshops', 1)


def get_content(func, argument=None):
    if argument:
        return [METHOD(abs) for abs in func(argument)]
    else:
        return [METHOD(abs) for abs in func()]


def main():
    # TODO: better cleaning: get rid of \n, math, non-ASCII, some HTML, etc.
    source = dict()
    # Journals
    """
    source['IEEE_SMCB'] = get_content(IEEE_general.maybe_pickle_abstracts, 'IEEE_SMCB')
    source['IEEE_TPAMI'] = get_content(IEEE_general.maybe_pickle_abstracts, 'IEEE_TPAMI')
    source['IEEE_NN_LS'] = get_content(IEEE_general.maybe_pickle_abstracts, 'IEEE_NN_LS')
    source['IEEE_EC'] = get_content(IEEE_general.maybe_pickle_abstracts, 'IEEE_EC')
    source['IEEE_NN'] = get_content(IEEE_general.maybe_pickle_abstracts, 'IEEE_NN')
    source['IEEE_CIM'] = get_content(IEEE_general.maybe_pickle_abstracts, 'IEEE_CIM')
    source['IEEE_ASLP'] = get_content(IEEE_general.maybe_pickle_abstracts, 'IEEE_ASLP')
    source['IEEE_MI'] = get_content(IEEE_general.maybe_pickle_abstracts, 'IEEE_MI')
    source['IEEE_IS'] = get_content(IEEE_general.maybe_pickle_abstracts, 'IEEE_IS')
    source['IEEE_KDA'] = get_content(IEEE_general.maybe_pickle_abstracts, 'IEEE_KDA')
    """

    # Conferences
    source['IEEE_NETWORKING'] = get_content(IEEE_general.maybe_pickle_proceeding_abstracts, 'IEEE_NETWORKING')
    source['IEEE_CNSM'] = get_content(IEEE_general.maybe_pickle_proceeding_abstracts, 'IEEE_CNSM')
    source['IEEE_LCN'] = get_content(IEEE_general.maybe_pickle_proceeding_abstracts, 'IEEE_LCN')
    source['INFOCOM'] = get_content(IEEE_general.maybe_pickle_proceeding_abstracts, 'INFOCOM')
    source['INFO_WORKSHOP'] = get_content(IEEE_general.maybe_pickle_proceeding_abstracts, 'INFO_WORKSHOP')

    total = 0
    for s in source.keys():
        count = len(source[s])
        total += count
        print 'Number of {0} abstracts: {1}'.format(DETAILS[s][0], count)

    print 'Total = {0}'.format(total)

    # Weight sources by impact factor
    all_impacts = [d[1] for d in DETAILS.values() if d[1] != None]
    mean_impact = 1. * sum(all_impacts) / len(all_impacts)
    counters = dict()
    for s in source.keys():
        counters[s] = Counter(list(itertools.chain(*source[s])))
        impact = DETAILS[s][1]
        if not impact:
            impact = mean_impact
        for w in counters[s]:
            counters[s][w] *= impact

    for k in reduce(add, counters.values(), Counter()).most_common(500):
        print k

if __name__ == '__main__':
    main()
