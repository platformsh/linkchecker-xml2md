#!/usr/bin/env python3
import xml.etree.ElementTree as ET
from tabulate import tabulate
import argparse


def parse_xml_to_markdown(xmlfile):
    """
    Simple xml to markdown parser for converting xml generated by https://pypi.org/project/LinkChecker/ into a markdown
    table suitable for using as a comment in a GitHub issue
    @:parameter xmlfile xml file generated by linkchecker
    @:return string markdown of converted xml
    """
    tree = ET.parse(xmlfile)
    root = tree.getroot()

    tableData = []
    for link in root.findall('urldata'):
        # we need
        # * broken link - realurl
        # * the URL of where the broken link appears - parent
        # * where in the above it appears - parent.attrib.line
        # * the "result" - valid.attrib.result
        fullURL = link.find('realurl').text
        parentLink = link.find("parent")
        parentURL = parentLink.text
        parentLoc = parentLink.attrib.get('line')
        result = link.find('valid').attrib.get('result')

        brokenLinkRow = [fullURL, parentURL, parentLoc, result]
        tableData.append(brokenLinkRow)

    # Generate the table
    table = tabulate(tableData, headers=['Broken Link', 'Parent', 'Line in Parent', 'Reason'], tablefmt="github")
    print(table)
    print("\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Parse Linkchecker XML output to markdown.')
    parser.add_argument('xmlfile', type=str, help='Path to the XML file generated by Linkchecker')
    args = parser.parse_args()

    parse_xml_to_markdown(args.xmlfile)
