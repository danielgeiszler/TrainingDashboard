import matplotlib.pyplot as plt
import seaborn as sns


def summary_plot(df):
    ax = sns.lineplot(
        data=df,
        x="Cycle",
        y="True_Improvement",
        hue="Exercise",
        marker='o',
        estimator=None,
        errorbar=None
    )
    x_ticks = range(df["Cycle"].min(), df["Cycle"].max() + 1)
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