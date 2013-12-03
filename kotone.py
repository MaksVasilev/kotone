#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import sys
from time import gmtime, strftime
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-m", "--mode", dest="mode", default='apply',
                  help="working mode: apply, extract, append-from-template, append-from-palete, convert", metavar="MODE")
parser.add_option("-t", "--template", dest="template_f",
                  help="template file to generate stylesheet (apply mode)", metavar="TEMPLATE")
parser.add_option("-p", "--palete", dest="palete_f",
                  help="name of palete file to applyed to template", metavar="PALETE")
parser.add_option("-o", "--output", dest="output_f", default='-',
                  help="output file", metavar="OUTPUT")
parser.add_option("-s", "--stylsheet", dest="css_f",
                  help="stylsheet file where from extracted colors (extract mode)", metavar="CSS")

(options, args) = parser.parse_args()

if (options.mode == 'apply'):
    print "\nmode —» apply palete to template\n"

    if (options.template_f is None or options.palete_f is None):
        parser.error("Template and palete filename is required!\nsee -h to usage help")

    if options.output_f == "-":
        n = sys.stdout
    else:
        n = open(options.output_f, "w")

    f = open(options.template_f, 'r')
    t = open(options.palete_f, 'r')

    tone = {}
    out = []

    for line in t:
        ci = re.split('\s+', line)
        tone[ci[0]] = ci[1].upper()
        print ci[0], '—»', tone[ci[0]]

    for line in f:
        k = re.compile('#{([a-z,A-Z,-]+)}').findall(line)
        if k:
            for c in k:
                line = re.sub(('{' + c + '}'), tone[c], line)
        out.append(line)

    for l2 in out:
        n.write(l2)
    n.write('\n/* converted from «' + options.template_f + '» by palete «' + options.palete_f + '» - ' + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' GMT */\n')

    f.close()
    t.close()
    n.close()

if (options.mode == 'extract'):
    print "\nmode —» extract colors from stylesheet to palete\n"

    if (options.css_f is None or options.palete_f is None):
        parser.error("Stylesheet and palete filename is required!\nsee -h to usage help")

    if options.palete_f == "-":
        w = sys.stdout
    else:
        w = open(options.palete_f, "w")

    f = open(options.css_f, 'r')
    n = open(options.css_f + '.normalized-color', 'w')

    tone = []
    out = []

    for line in f:
        k = re.compile('#([A-F,a-f,0-9]+)').findall(line)
        if k:
            for c in k:
                if len(c) == 3:
                    c2 = (c[0] + c[0] + c[1] + c[1] + c[2] + c[2]).upper()
                    tone.append(c2)
                    line = re.sub(c, c2, line)
                elif len(c) == 6:
                    c2 = c.upper()
                    tone.append(c2)
                    line = re.sub(c, c2, line)
        out.append(line)

    tone = list(set(tone))

    for a in tone:
        w.write("color-" + a + "\t" + a + '\n')

    for l2 in out:
        n.write(l2)

    f.close()
    w.close()
    n.close()

if (options.mode == 'append-from-template'):
    print "\nmode —» append new color to palete from template\n"

if (options.mode == 'append-from-palete'):
    print "\nmode —» append new color to palete from other palete\n"
