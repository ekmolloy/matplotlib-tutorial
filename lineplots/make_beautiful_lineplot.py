import matplotlib.pyplot
import numpy
import pandas
import sys

# BASED ON:
# http://www.randalolson.com/2014/06/28/how-to-make-beautiful-data-visualizations-in-python-with-matplotlib/

# ADDITION: Change the font to Helvetica
matplotlib.pyplot.rc('text', usetex=True)
matplotlib.pyplot.rcParams['text.latex.preamble'] = [r'\usepackage{helvet} \usepackage{sfmath}']

# ADDITION: Use the TABLEAU 20 colors   
tableau20 = [(31, 119, 180), (174, 199, 232),
             (255, 127, 14), (255, 187, 120),    
             (44, 160, 44), (152, 223, 138),
             (214, 39, 40), (255, 152, 150),    
             (148, 103, 189), (197, 176, 213),
             (140, 86, 75), (196, 156, 148),    
             (227, 119, 194), (247, 182, 210),
             (127, 127, 127), (199, 199, 199),    
             (188, 189, 34), (219, 219, 141),
             (23, 190, 207), (158, 218, 229)]

# and map RGB values to the [0, 1]
for i in range(len(tableau20)):
    r, g, b = tableau20[i]
    tableau20[i] = (r / 255., g / 255., b / 255.)

# Read in data file
df = pandas.read_csv("data_for_lineplot.csv")

# Set up plot
fig = matplotlib.pyplot.figure(figsize=(6, 4))
ax = fig.add_subplot(1, 1, 1)

# For each method draw a line
mthds = df.MTHD.unique()
xs = df.KEEP.unique()
for i, mthd in enumerate(mthds):
    ys = df[df["MTHD"] == mthd].STEE_AV.values
    zs = df[df["MTHD"] == mthd].STEE_SE.values

    # Uncomment if you need to fix the ordering...
    # ys = []
    # for keep in xs:
    #     xdf = df[(df["MTHD"] == mthd) & (df["KEEP"] == keep)]
    #     ys.append(xdf.STEE_AV.values[0])

    # Draw line
    if mthd == "caml" or mthd == "svdquartets":
        ys = numpy.repeat(ys[0], len(ys))
        ax.plot(xs, ys, '--', lw=2.5, color=tableau20[2*i], label=mthd)
    else:
        ax.fill_between(xs, ys - zs, ys + zs, 
                        color=tableau20[2*i+1], alpha=0.5)
        ax.plot(xs, ys, '-', lw=2.5, color=tableau20[2*i], label=mthd)

# Label axes
ax.set_xlabel("Percent Filtered", fontsize=14)
ax.set_ylabel("Species Tree Error", fontsize=14)

# Fix ticks on y-axis
ax.set_ylim(0.0, 0.15)
ax.tick_params(axis='y', labelsize=11)

# Fix ticks on x-axis
ax.set_xlim(xs[0], xs[-1])
ax.set_xticks([1000, 750, 500, 250, 50])
ax.set_xticklabels(["0", "25", "50", "75", "95"])
ax.tick_params(axis='x', labelsize=11)

# Add legend
ax.legend(frameon=False, fontsize=12, loc="upper right")

# ADDITION: Add dotted lines at y ticks
xticks =  ax.xaxis.get_majorticklocs()
yticks =  ax.yaxis.get_majorticklocs()[:-1]
for y in yticks:
    if y > 0.09:
        xs = list(xticks[:-2]) + [400]
        ax.plot(xs, [y] * len(xs), "--", dashes=(2, 2),
                lw=0.5, color="black", alpha=0.3)
    else:
        ax.plot(xticks, [y] * len(xticks), "--", dashes=(2, 2),
                lw=0.5, color="black", alpha=0.3)

# NOTE: You can see the attributes by using dir, e.g.,
# print dir(ax.yaxis)

# ADDITION: Remove some of the axes
ax.get_xaxis().tick_bottom() 
ax.get_yaxis().tick_left() 
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

# Save plot
fig.set_tight_layout(True)
matplotlib.pyplot.savefig("beautiful_lineplot.png", format="png", dpi=300)
