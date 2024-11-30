import matplotlib.pyplot as plt
import seaborn as sns

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