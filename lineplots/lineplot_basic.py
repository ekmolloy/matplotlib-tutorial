import matplotlib.pyplot
import numpy
import pandas
import sys

# Read in data file
df = pandas.read_csv("../data.csv")

# Select a model condition
xdf = df[(df["TRLN"] == "10M") & 
         (df["NBPS"] == 0) &
         (df["GTEE"] == "[20,50)")]

# Set up plot
fig = matplotlib.pyplot.figure(figsize=(6, 4))
ax = fig.add_subplot(1,1,1)

# Now add lines to plot, note that we want to draw 
# one line for each method (MTHD) used to estimate the species tree with the
# with the y-axis as the species tree estimation error (STEE) and
# with the x-axis as the amount of data (KEEP) given to the species tree method

# For each method add a line
mthds = xdf["MTHD"].unique()
colors = ['r', 'g', 'b', 'm', 'k']
for mthd, color in zip(mthds, colors):
    ydf = xdf[(xdf["MTHD"] == mthd)]

    # Compute average and standard error for each amount of data (KEEP)
    av = []  # Average or Mean
    se = []  # Standard Error = Standard Deviation / SQRT(Numer of Samples)
    keeps = xdf["KEEP"].unique()
    for keep in keeps:
        zdf = ydf[ydf["KEEP"] == keep]
        ser = zdf.STEE.values
        av.append(numpy.mean(ser))
        se.append(numpy.std(ser) / numpy.sqrt(ser.size))
    av = numpy.array(av)
    se = numpy.array(se)

    # Draw line for a method
    if mthd == "caml" or mthd == "svdquartets":
        av = numpy.repeat(av[0], len(av))
        ax.plot(keeps, av, '--',
                color=color, label=mthd)
    else:
        ax.fill_between(keeps, av - se, av + se, 
                        color=color, alpha=0.25)
        ax.plot(keeps, av, '-', color=color, label=mthd)

# Label axes
ax.set_xlabel("Percent Filtered", fontsize=14)
ax.set_ylabel("Species Tree Error", fontsize=14)

# Label ticks on y-axis
ax.set_ylim(0.0, 0.20)
ax.tick_params(axis='y', labelsize=11)

# Label ticks on x-axis
ax.set_xlim(keeps[0], keeps[-1])
ax.set_xticks([1000, 750, 500, 250, 50])
ax.set_xticklabels(["0", "25", "50", "75", "95"])
ax.tick_params(axis='x', labelsize=11)

# Add legend
ax.legend(frameon=False, fontsize=12, loc="upper right") 

# Save plot
fig.set_tight_layout(True)
matplotlib.pyplot.savefig("lineplot_basic.pdf", format="pdf", dpi=300)