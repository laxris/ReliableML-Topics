import os
import dill
import urllib2
from collections import defaultdict
from bs4 import BeautifulSoup

# Maximum 1000 per year is reasonable
QUERY_PATTERN = 'http://ieeexplore.ieee.org/gateway/ipsSearch.jsp?hc=1000&pn='
QUERY_PATTERN_YEAR = '&py='

# Starting 2007
JOURNALS = dict()
"""
JOURNALS['IEEE_TPAMI'] = (34, range(2007, 2017))
JOURNALS['IEEE_NN'] = (72, range(2007, 2012))
JOURNALS['IEEE_NN_LS'] = (5962385, range(2012, 2017))
JOURNALS['IEEE_KDA'] = (69, range(2007, 2017))
JOURNALS['IEEE_MI'] = (42, range(2007, 2017))
JOURNALS['IEEE_EC'] = (4235, range(2007, 2017))
JOURNALS['IEEE_CIM'] = (10207, range(2007, 2017))
JOURNALS['IEEE_ASLP'] = (10376, range(2007, 2017))
JOURNALS['IEEE_IS'] = (9670, range(2007, 2017))
JOURNALS['IEEE_SMCB'] = (3477, range(2007, 2013))
JOURNALS['IEEE_FS'] = (91, range(2007, 2017))

JOURNALS['IEEE_TPAMI'] = (34, range(1979, 2017))
JOURNALS['IEEE_NN'] = (72, range(1990, 2012))
JOURNALS['IEEE_NN_LS'] = (5962385, range(2012, 2017))
JOURNALS['IEEE_KDA'] = (69, range(1989, 2017))
JOURNALS['IEEE_MI'] = (42, range(1982, 2017))
JOURNALS['IEEE_EC'] = (4235, range(1997, 2017))
JOURNALS['IEEE_CIM'] = (10207, range(2006, 2017))
JOURNALS['IEEE_ASLP'] = (10376, range(2006, 2017))
JOURNALS['IEEE_IS'] = (9670, range(2001, 2017))
JOURNALS['IEEE_SMCB'] = (3477, range(1996, 2013))
JOURNALS['IEEE_FS'] = (91, range(1993, 2017))
"""


PROCEEDINGS = defaultdict(lambda: defaultdict(dict))

PROCEEDINGS['IEEE_NETWORKING'] = {
    2015: 7128766,
    2016: 7493812,
}


PROCEEDINGS['IEEE_CNSM'] = {
    2015: 7360263,
    2016: 7803495,
}

PROCEEDINGS['IEEE_LCN'] = {
    2016: 7795840,
    2014: 7360816,
}

PROCEEDINGS['INFO_WORKSHOP'] = {
    2013: 6556114,
    2016: 7556623,
}

PROCEEDINGS['INFOCOM'] = {
    2016: 7515093,
    2015: 7170114,
}

def maybe_pickle_abstracts(name, force=False):
    file_name = '{0}_abstracts'.format(name)

    set_filename = '{0}.dill'.format(file_name)
    if os.path.exists(set_filename) and not force:
        print '{0} already present - Loading dill.'.format(set_filename)
        abstracts = dill.load(open(set_filename, 'rb'))
    else:
        publication_number, years = JOURNALS[name]
        abstracts = get_abstracts(publication_number, years)
        abstracts = [abstracts[v][k] for v in years for k in abstracts[v]]
        try:
            print 'Dilling {0}'.format(set_filename)
            dill.dump(abstracts, open(set_filename, 'wb'))
        except Exception as e:
            print('Unable to save data to', set_filename, ':', e)
    return abstracts


def maybe_pickle_proceeding_abstracts(name, force=False):
    file_name = '{0}_abstracts'.format(name)

    set_filename = '{0}.dill'.format(file_name)
    if os.path.exists(set_filename) and not force:
        print '{0} already present - Loading dill.'.format(set_filename)
        abstracts = dill.load(open(set_filename, 'rb'))
    else:
        abstracts = []
        count = 0
        for year in PROCEEDINGS[name]:
            tmp_abstracts = get_abstracts(PROCEEDINGS[name][year], (year,))
            count += len(tmp_abstracts[year])
            abstracts += [tmp_abstracts[year][k] for k in tmp_abstracts[year]]
        print 'TOTAL={0}'.format(count)
        try:
            print 'Dilling {0}'.format(set_filename)
            dill.dump(abstracts, open(set_filename, 'wb'))
        except Exception as e:
            print('Unable to save data to', set_filename, ':', e)
    return abstracts


def get_abstracts(publication_number, years):
    res = defaultdict(lambda: defaultdict(set))

    total = 0
    total_actual = 0
    for year in years:
        query = '{0}{1}{2}{3}'.format(QUERY_PATTERN, publication_number, QUERY_PATTERN_YEAR, year)
        print 'Starting {0}'.format(query)
        page = urllib2.urlopen(query).read()
        soup = BeautifulSoup(page, 'lxml-xml')
        documents = soup.findAll('document')

        count = len(documents)
        count_actual = 0
        for document in documents:
            doi = document.find('doi').getText()
            abstract = document.findAll('abstract')
            # Some may not have an abstract
            if len(abstract):
                count_actual += 1
                res[year][doi] = abstract[0].getText()

        print 'COUNT={0}/{1}'.format(count_actual, count)
        total += count
        total_actual += count_actual

    print 'TOTAL={0}/{1}'.format(total_actual, total)
    return res
