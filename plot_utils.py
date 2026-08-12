


import matplotlib.pyplot as plt


def apply_grid_style(ax=None, major_color="green", minor_color="green"):
    ax = ax or plt.gca()
    ax.minorticks_on()
    ax.grid(which="major", linestyle="-", linewidth=0.5, color=major_color)
    ax.grid(which="minor", linestyle=":", linewidth=0.5, color=minor_color)
    return ax


def styled_scatter(
    x, y, c,
    ax=None,
    cmap="jet",
    s=10,
    xlabel="",
    ylabel="",
    title="",
    cbar_label="",
    vmin=None,
    vmax=None,
    invert_yaxis=False,
):
    
    if ax is None:
        fig, ax = plt.subplots()

    sc = ax.scatter(x, y, c=c, cmap=cmap, s=s, vmin=vmin, vmax=vmax)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    apply_grid_style(ax)
    plt.colorbar(sc, ax=ax, label=cbar_label)

    if invert_yaxis:
        ax.invert_yaxis()

    return ax, sc


def depth_comparison_plot(
    depth,
    series,
    xlabel="Depth",
    ylabel="",
    title="",
    figsize=(15, 4),
    linestyles=None,
):
   
    linestyles = linestyles or {}
    fig, ax = plt.subplots(figsize=figsize)

    for label, values in series.items():
        ax.plot(depth, values, linestyles.get(label, "-"), label=label)

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.legend()
    apply_grid_style(ax)
    plt.show()
    return ax
