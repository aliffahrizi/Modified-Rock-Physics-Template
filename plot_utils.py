"""
Shared plotting helpers for the Modified Rock Physics Template workflow.

These wrap the styling pattern used throughout main.ipynb (major/minor grid,
colorbar cross-plots, and depth-track comparisons) so it's defined once
instead of copy-pasted per cell.
"""

import matplotlib.pyplot as plt


def apply_grid_style(ax=None, major_color="green", minor_color="green"):
    """Apply the standard major/minor grid + minor ticks used across the notebook.

    Parameters
    ----------
    ax : matplotlib.axes.Axes, optional
        Axes to style. Defaults to the current axes (plt.gca()).
    """
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
    """Colorbar cross-plot with consistent styling.

    Replaces the repeated pattern:
        plt.scatter(x, y, c=c, cmap="jet", s=10, label="well")
        plt.xlabel(...); plt.ylabel(...); plt.title(...)
        plt.colorbar(label=...)
        plt.minorticks_on(); plt.grid(...)
        plt.show()

    Returns the Axes and the scatter handle (ax, sc) in case further
    customization is needed (e.g. plt.xlim after calling this).
    """
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
    """Multi-curve comparison against depth (e.g. RHO vs RHO_MLR, VP vs VP model).

    Parameters
    ----------
    depth : array-like
        Shared depth axis for all curves.
    series : dict[str, array-like]
        Mapping of legend label -> data to plot against depth.
    linestyles : dict[str, str], optional
        Mapping of legend label -> matplotlib linestyle (e.g. {"Model": "--"}).
        Curves not listed default to a solid line.

    Example
    -------
    depth_comparison_plot(
        well['DEPTH'],
        {"RHO": well['RHO'], "RHO MLR": RHO_MLR_SW1},
        ylabel="RHO (g/cm3)",
        title="RHO vs RHO MLR",
        linestyles={"RHO MLR": "--"},
    )
    """
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
