import matplotlib.gridspec
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


def add_line_plot(ax, df, ylim):
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

    # Fix ticks on y-axis
    ax.set_ylim(0.0, ylim)
    ax.tick_params(axis='y', labelsize=11)

    # Fix ticks on x-axis
    ax.set_xlim(xs[0], xs[-1])
    ax.set_xticks([1000, 750, 500, 250, 50])
    ax.set_xticklabels(["0", "25", "50", "75", "95"])
    ax.tick_params(axis='x', labelsize=11)

    # ADDITION: Add dotted lines at y ticks
    xticks =  ax.xaxis.get_majorticklocs()
    yticks =  ax.yaxis.get_majorticklocs()[:-1]
    for y in yticks:
        ax.plot(xticks, [y] * len(xticks), "--", dashes=(2, 2),
                lw=0.5, color="black", alpha=0.3)

    # ADDITION: Remove some of the axes
    ax.get_xaxis().tick_bottom() 
    ax.get_yaxis().tick_left() 
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


if __name__ == "__main__":
    # Read in data file
    df = pandas.read_csv("data_for_figure.csv")

    # Set up figure
    fig = matplotlib.pyplot.figure(figsize=(8, 9))
    gs = matplotlib.gridspec.GridSpec(3, 2)

    # Add each (beautiful) subplot
    gtees = df.GTEE.unique()
    trlns = df.TRLN.unique()
    for i, trln in enumerate(trlns):
        if i == 2:
            ylim = 0.50
        else:
            ylim = 0.20
        for j, gtee in enumerate(gtees):
            ax = matplotlib.pyplot.subplot(gs[i, j])
            
            # Add title
            ax.set_title(trln + " -- " + gtee, fontsize=15)

            # Label axes
            if i == 2:
                ax.set_xlabel("Percent Filtered", fontsize=14)
            if j == 0:
                ax.set_ylabel("Species Tree Error", fontsize=14)

            # Add plot
            xdf = df[(df["GTEE"] == gtee) & (df["TRLN"] == trln)]
            add_line_plot(ax, xdf, ylim)

    # Add legend
    ax = matplotlib.pyplot.subplot(gs[2, 1])
    ax.legend(frameon=False, ncol=5, fontsize=12,
              loc='upper center', bbox_to_anchor=(-0.1, -0.25))

    # Save plot
    gs.tight_layout(fig, rect=[0, 0.05, 1, 1])
    matplotlib.pyplot.savefig("figure_lineplot.png", format="png", dpi=300)
