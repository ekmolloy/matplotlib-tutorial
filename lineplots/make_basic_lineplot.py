import matplotlib.pyplot
import numpy
import pandas
import sys

# Read in data file
df = pandas.read_csv("data_for_lineplot.csv")

# Set up plot
fig = matplotlib.pyplot.figure(figsize=(6, 4))
ax = fig.add_subplot(1, 1, 1)

# For each method add a line
mthds = df.MTHD.unique()
colors = ['r', 'g', 'b', 'm', 'k']
xs = df.KEEP.unique()
for mthd, color in zip(mthds, colors):
    ys = df[df["MTHD"] == mthd].STEE_AV.values

    # Uncomment if you need to fix the ordering...
    # ys = []
    # for keep in xs:
    #     xdf = df[(df["MTHD"] == mthd) & (df["KEEP"] == keep)]
    #     ys.append(xdf.STEE_AV.values[0])

    # Draw line for a method
    if mthd == "caml" or mthd == "svdquartets":
        ys = numpy.repeat(ys[0], len(ys))
        ax.plot(xs, ys, '--', color=color, label=mthd)
    else:
        ax.plot(xs, ys, '-', color=color, label=mthd)

# Label axes
ax.set_xlabel("Percent Filtered", fontsize=14)
ax.set_ylabel("Species Tree Error", fontsize=14)

# Label ticks on y-axis
ax.set_ylim(0.0, 0.15)
ax.tick_params(axis='y', labelsize=11)

# Label ticks on x-axis
ax.set_xlim(xs[0], xs[-1])
ax.set_xticks([1000, 750, 500, 250, 50])
ax.set_xticklabels(["0", "25", "50", "75", "95"])
ax.tick_params(axis='x', labelsize=11)

# Add legend
ax.legend(frameon=False, fontsize=12, loc="upper right")

# Save plot
fig.set_tight_layout(True)
matplotlib.pyplot.savefig("lineplot_basic.png", format="png", dpi=300)
