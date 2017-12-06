import numpy
import pandas

# GOAL: Examine impact of gene filtering on method performance

# STEP 0: Read CSV file into data frame
df = pandas.read_csv("../data.csv")

# Data frame contains the following columns:
# TRLN = model condition (species tree height)
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

# STEP 1: Select a model condition
df = df[(df["TRLN"] == "10M") &
        (df["NBPS"] == 0) &
        (df["GTEE"] == "[20,50)")]

# STEP 2: Re-format data for plotting.
mthds = df.MTHD.unique()  # List methods
keeps = df.KEEP.unique()  # List number of genes given to methods

cols = ["MTHD", "KEEP", "STEE_AV", "STEE_SE"]
rows = []

for mthd in mthds:
    for keep in keeps:
        stee = df[(df["MTHD"] == mthd) & (df["KEEP"] == keep)].STEE.values

        row = {}
        row["MTHD"] = mthd
        row["KEEP"] = keep
        row["STEE_AV"] = numpy.mean(stee)
        row["STEE_SE"] = numpy.std(stee) / numpy.sqrt(stee.size)

        rows.append(row)

# STEP 3: Build and save dataframe
df = pandas.DataFrame(rows, columns=cols)
df.to_csv("data_for_lineplot.csv",
          sep=',', na_rep="NA", head=False, index=False)
