import matplotlib.pyplot as plt
import seaborn as sns

from matplotlib.colors import LinearSegmentedColormap

# Define the Yeti theme colors
yeti_colors = {
    "primary": "#008cba",   # Blue
    "secondary": "#e7e7e7", # Light gray
    "success": "#43ac6a",   # Green
    "info": "#5bc0de",      # Light blue
    "warning": "#f0ad4e",   # Orange
    "danger": "#d9534f",    # Red
    "light": "#f8f9fa",     # Very light gray
    "dark": "#343a40"       # Dark gray
}

# Create a colormap for categorical data
categorical_colors = [
    yeti_colors["primary"],
    yeti_colors["secondary"],
    yeti_colors["success"],
    yeti_colors["info"],
    yeti_colors["warning"],
    yeti_colors["danger"],
    yeti_colors["dark"]
]

# Create a colormap for continuous data (blending primary to danger)
continuous_colors = [yeti_colors["primary"], yeti_colors["danger"], yeti_colors["info"], yeti_colors["warning"], yeti_colors["success"]]
yeti_continuous_cmap = LinearSegmentedColormap.from_list("YetiContinuous", continuous_colors)

yeti_binary_colors = ["#008cba", "#d9534f"]  # Primary to danger
yeti_binary_cmap = LinearSegmentedColormap.from_list("YetiBinary", yeti_binary_colors)

# Create a custom Seaborn style
sns.set_style("white")  # Base style
sns.set_context("notebook", font_scale=1.0)  # Adjust font scale for better readability

# Modify the style
yeti_style = {
    "axes.edgecolor": "white",  # No visible axes
    "axes.facecolor": "white",  # White grid background
    "axes.grid": False,         # No gridlines
    "xtick.color": "#343a40",     # Hide x-tick marks
    "ytick.color": "#343a40",     # Hide y-tick marks
    "xtick.bottom": False,      # Remove x-tick line
    "ytick.left": False,        # Remove y-tick line
    "grid.color": "white",      # Ensure gridlines are hidden
    "font.family": ["Open Sans", "sans-serif"],  # Font family as Yeti
}

# Apply the custom style
sns.set_style(yeti_style)

def colormap_to_palette(cmap, n_colors):
    return [cmap(i / (n_colors - 1)) for i in range(n_colors)]

def summary_plot(df):
    sampled_palette = colormap_to_palette(yeti_continuous_cmap, df["Exercise"].nunique())

    ax = sns.lineplot(
        data=df,
        x="Cycle",
        y="True_Improvement",
        hue="Exercise",
        marker='o',
        estimator=None,
        errorbar=None,
        palette=sampled_palette
    )
    x_ticks = range(df["Cycle"].min(), df["Cycle"].max() + 1)
    plt.legend(title="exercise", frameon=False)  # Remove legend frame
    plt.xticks(ticks=x_ticks)
    plt.xlabel('cycle')
    plt.ylabel('improvement (%)')
    plt.title(f'overall improvement')

def progress_plot(df, exercise_name):
    print(df)
    ax = sns.lineplot(
        data=df,
        x="Weight",
        y="Reps",
        #hue="Cycle",
        marker='o',
        sort=False,
        estimator = None,
        errorbar = None
    )
    for i, row in df.iterrows():
        ax.text(
            x=row['Weight'],
            y=row['Reps'],
            s=str(row['Cycle']),  # Use Cycle number as the annotation
            color='black',
            fontsize=9,
            ha='center',
            va='center'
        )

    plt.xlabel('weight')
    plt.ylabel('reps')
    plt.title((f'progress for {exercise_name}').lower())


def weight_plot(df, exercise_name):
    sns.lineplot(
        data=df,
        x="Cycle",
        y="Weight",
        marker='o'
    )
    plt.xlabel('cycle')
    plt.ylabel('weight')
    plt.title(f'average weight by cycle for {exercise_name}')


def reps_plot(df, exercise_name):
    sns.lineplot(
        data=df,
        x="Cycle",
        y="Reps",
        marker='o'

    )
    plt.xlabel('cycle')
    plt.ylabel('weight')
    plt.title(f'average reps by cycle for {exercise_name}')


def total_weight_moved_plot(df, exercise_name):
    sns.lineplot(
        data=df,
        x="Cycle",
        y="TotalWeightMoved",
        marker='o'
    )
    plt.xlabel('cycle')
    plt.ylabel('total weight moved')
    plt.title(f'total weight moved by cycle for {exercise_name}')