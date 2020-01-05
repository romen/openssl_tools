#!/usr/bin/env python3

# Copyright 2019 The OpenSSL Project Authors. All Rights Reserved.
#
# Licensed under the Apache License 2.0 (the "License").  You may not use
# this file except in compliance with the License.  You can obtain a copy
# in the file LICENSE in the source distribution or at
# https://www.openssl.org/source/license.html

# Run this using:
#   bn_rand_range.py > $(OPENSSL)/test/bn_rand_range.h
#
# There is a dependency of scipi, include the package python3-scipy to resolve
# this.

from datetime import datetime
from scipy.stats import chi2, binom

alpha_chi2 = 0.95
alpha_binomial = 0.9999
test_cases = list(range(2, 20)) \
             + [x * 10 + 10 for x in range(1, 10)] \
             + [x * 1000 for x in range(1, 11)]

# The rest of this file produces the C include file

def do_case(n):
    "Output a single formatted row in the table"
    ns = "%d," % n
    iterations = "%d," % (n * (100 if n < 1000 else 10))
    critical = "%f" % (chi2.ppf(alpha_chi2, n - 1))
    print("    { %6s %8s %12s }," % ( ns, iterations, critical ))

# Work out the copyright year range
year = datetime.today().year
if year != 2019:
    year = "2019-%d" % year

print("""/*
 * WARNING: do not edit!
 * Generated by statistics/bn_rand_range.py in the OpenSSL tool repository.
 *
 * Copyright %s The OpenSSL Project Authors. All Rights Reserved.
 *
 * Licensed under the Apache License 2.0 (the "License").  You may not use
 * this file except in compliance with the License.  You can obtain a copy
 * in the file LICENSE in the source distribution or at
 * https://www.openssl.org/source/license.html
 */

static const struct {
    unsigned int range;
    unsigned int iterations;
    double critical;
} rand_range_cases[] = {""" % year)
num_cases = len(list(map(do_case, test_cases)))
print("};\n")

# Finally, calculate and output the lower tail binomial threshold.
b_thresh = binom.isf(alpha_binomial, num_cases, alpha_chi2)
print("static const int binomial_critical = %d;\n" % b_thresh)