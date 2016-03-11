#!/usr/bin/python

import re
import csv
import logging

import requests
from bs4 import BeautifulSoup

BASE_URL = 'http://research.amnh.org/vz/herpetology/amphibia/index.php//Amphibia/%s/%s/%s/%s-%s'

def download_species_page(record):
    order = record['order']
    family = record['family']
    genus = record['genus']
    species = record['species']
    logging.info("Starting species page download: %s %s" % (genus, species))

    sname_str = ''
    auth_str = ''
    fname_str = ''
    tloc_str = ''
    dist_str = ''

    sp_url = BASE_URL % (order, family, genus, genus, species)
    # logging.info('  %s' % sp_url)

    r = requests.get(sp_url)
    soup = BeautifulSoup(r.text)

    title = soup.title.string

    logging.info(title)
    sname_str = '%s %s' % (genus, species)
    fname_str = (title.split('|')[0]).strip()
    auth_str = (fname_str.split(sname_str)[1]).strip()

    # Get the type locality from synonym tag
    syn_tag = soup.select('div.synonymy')
    syn_text = syn_tag[0].get_text()
    p = re.compile('Type locality:')
    m = p.search(syn_text)
    if m:
        tloc_str = syn_text[m.end():]

    # Get the Distribution
    for header in soup.find_all('h3', text=re.compile('Distribution')):
        dist_str = header.findNext('p').string

    logging.info('Full: %s' % fname_str)
    logging.info('sp.name: %s' % sname_str)
    logging.info('author: %s' % auth_str)
    logging.info('Type locality: %s' % tloc_str)
    logging.info('Distribution: %s' % dist_str)
    record.update({
        'scientificname':fname_str.encode('utf8'),
        'binomial': sname_str,
        'author': auth_str.encode('utf8'),
        'locality': tloc_str.encode('utf8'),
        'dist': dist_str.encode('utf8')
    })
    return record


def test_sp_page():

    sname_str = ''
    auth_str = ''
    fname_str = ''
    tloc_str = ''
    dist_str = ''

    soup = BeautifulSoup(open("Allophryne-relicta.html"))
    # logging.info(' >> %s' % soup.title.string)

    title = soup.title.string

    logging.info(title)
    sname_str = 'Allophryne resplendens'
    fname_str = (title.split('|')[0]).strip()
    auth_str = (fname_str.split(sname_str)[1]).strip()

    # Get the type locality from synonym tag
    syn_tag = soup.select('div.synonymy')
    syn_text = syn_tag[0].get_text()
    p = re.compile('Type locality:')
    m = p.search(syn_text)
    if m:
        tloc_str = syn_text[m.end():]

    # Get the Distribution
    for header in soup.find_all('h3', text=re.compile('Distribution')):
        dist_str = header.findNext('p').string

    logging.info('Full: %s' % fname_str)
    logging.info('sp.name: %s' % sname_str)
    logging.info('author: %s' % auth_str)
    logging.info('Type locality: %s' % tloc_str)
    logging.info('Distribution: %s' % dist_str)


def process(reader, writer):
    for record in reader:
        # logging.info(row)
        rec = download_species_page(record)
        writer.writerow(rec)


def setup_logging(level=logging.DEBUG):
    FULL_FORMAT = "%(levelname)s %(asctime)s %(funcName)s %(lineno)d %(message)s"
    FORMAT = " >> %(lineno)d | %(message)s"
    logging.basicConfig(format=FORMAT, level=logging.DEBUG)


def main():
    setup_logging()
    # test_sp_page()
    with open("test2.csv", "r") as fin:
        with open('output.csv','w') as fout:
            reader = csv.DictReader(fin, delimiter='\t')
            fieldnames = reader.fieldnames
            fieldnames.append('scientificname')
            fieldnames.append('binomial')
            fieldnames.append('author')
            fieldnames.append('locality')
            fieldnames.append('dist')
            writer = csv.DictWriter(fout, fieldnames=fieldnames)
            writer.writeheader()
            process(reader, writer)
            # fin.close()


if __name__ == "__main__":
    main()
