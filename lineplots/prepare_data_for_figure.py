import numpy
import pandas
import sys

# GOAL: Examine impact of gene filtering on method performance

# STEP 0: Read CSV file into data frame
df = pandas.read_csv("../data.csv")

# Data frame contains the following columns:
# TRLN = model condition (species tree height, related to ILS)
# RATE = model condition (speciation rate)
# NBPS = model condition (number of base pairs or sequence length)
# GTEE = model condition (gene tree estimation error)
# KEEP = number of genes given to the species tree estimation method
#        during gene filtering experiments
# MTHD = species tree estimation METHOD
# STEE = species tree estimation ERROR

# NOTE: We want to plot the
# *average* species tree estimation error (STEE) on the y-axis versus the
# number of genes (KEEP) used in species tree estimation on the x-axis,
# drawing one line for each species tree estimation method (MTHD).

# STEP 1: Select models condition for figure
xdf = df[(df["NBPS"] == 0) & (df["GTEE"] == "[20,50)")]
ydf = df[(df["NBPS"] == 100) & (df["GTEE"] == "[50,80)")]
df = pandas.concat([xdf, ydf])

# STEP 2: Re-format data for plotting.
trlns = df.TRLN.unique()  # List model condition (species tree height, related to ILS)
gtees = df.GTEE.unique()  # List model condition (gene tree estimation error or GTEE) 
mthds = df.MTHD.unique()  # List methods
keeps = df.KEEP.unique()  # List number of genes given to methods

cols = ["TRLN", "GTEE", "MTHD", "KEEP", "STEE_AV", "STEE_SE"]
rows = []

for trln in trlns:
    for gtee in gtees:
        for mthd in mthds:
            for keep in keeps:
                stee = df[(df["TRLN"] == trln) &
                          (df["GTEE"] == gtee) &
                          (df["MTHD"] == mthd) & 
                          (df["KEEP"] == keep)].STEE.values

                row = {}
                row["TRLN"] = trln
                row["GTEE"] = gtee
                row["MTHD"] = mthd
                row["KEEP"] = keep
                row["STEE_AV"] = numpy.mean(stee)
                row["STEE_SE"] = numpy.std(stee) / numpy.sqrt(stee.size)

                rows.append(row)

# STEP 3: Build and save dataframe
df = pandas.DataFrame(rows, columns=cols)
df.to_csv("data_for_figure.csv",
          sep=',', na_rep="NA", head=False, index=False)
