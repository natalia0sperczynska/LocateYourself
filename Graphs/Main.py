import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from User.User import User

def open_file(file_path: str):
    """
    Open a CSV file and loads it into DataFrame.

    Args:
        file_path (string): Path to the CSV file that is to be opened.

    Returns:
        data(pd.DataFrame):Loaded CSV file.
        None: If no file was found.
    """
    try:
        data = pd.read_csv(file_path)
        return data
    except FileNotFoundError:
        print("File not found")
        return None


def show_table(df: pd.DataFrame):
    if df is not None:
        print(df.describe())
        print(df.head())
    else:
        print("No data to display")

def percentage(df: pd.DataFrame):
    df = df.dropna()
    plt.hist(df['REM sleep percentage'], label='REM (%)', alpha=0.5)
    plt.hist(df['Deep sleep percentage'], label='Deep (%)', alpha=0.5)
    plt.hist(df['Light sleep percentage'], label='Light (%)', alpha=0.5)
    plt.xlabel('percentage')
    plt.ylabel('count')
    plt.legend()


def graph_distribution(df: pd.DataFrame, user:User, ax):
    """
    Plots a distribution graph for 'Sleep efficiency' using the provided DataFrame and user data.
    Uses Seaborn's KDE plot to visualize the distribution of the 'Sleep efficiency' column
    and annotates the plot with the user's specific sleep efficiency value.

    Parameters:
        df : pd.DataFrame
            The DataFrame containing the data. It must have a column named 'Sleep efficiency'.

        user : User
            The User object that contains the attribute `sleep_efficiency`, representing the user's sleep efficiency value.

        ax : matplotlib.axes.Axes
            The matplotlib Axes object where the plot will be drawn.

        Notes:
        The user mark is marked with a "hand-drawn" style using Matplotlib's xkcd mode.
    """
    with plt.xkcd():
        sns.kdeplot(data=df, x='Sleep efficiency',  fill=True,ax=ax)
        plt.xlabel('Sleep Efficiency', fontsize=12)
        plt.ylabel('Density', fontsize=12)
        ax.axvline(x=user.sleep_efficiency, color='r', label='axvline - full height')
        ax.annotate('You', xy=(user.sleep_efficiency, 2), xytext=(user.sleep_efficiency, 2.5), arrowprops=dict(facecolor='black', shrink=0.05))


def graph_smoking_influence_sleep_efficiency(df: pd.DataFrame,user:User,ax):
    """
        Plots the relationship between smoking status and sleep efficiency.
        Generates a bar plot showing the average sleep efficiency for different smoking statuses.
        It also marks the user's data point on the plot, showing where their sleep efficiency lies according to their smoking status.

        Parameters:
        df : pd.DataFrame
            The DataFrame containing the data. It must have columns named 'Smoking status' and 'Sleep efficiency'.
            The 'Smoking status' column should contain values indicating whether the individual is a smoker or non-smoker.

        user : User
            The User object that contains the user's individual data. The `user` should have attributes:
            - `smoking_status`: A boolean representing whether the user smokes (True for smoker, False for non-smoker).
            - `sleep_efficiency`: A float representing the user's sleep efficiency.

        ax : matplotlib.axes.Axes
            The axes to plot the graph on.

        Notes:
            The user mark is marked with a "hand-drawn" style using Matplotlib's xkcd mode.
        """
    df = df.dropna()
    sns.barplot(df, x='Smoking status', y='Sleep efficiency', palette=['#FF4D00', '#A6D609'],ax=ax)
    plt.xlabel('Smoking Status', fontsize=12)
    plt.ylabel('Sleep Efficiency', fontsize=12)
    with plt.xkcd():
        if not user.smoking_status:
            x_pos = 1
            mark='or'
        else:
            x_pos = 0
            mark='ob'
        ax.plot(x_pos, user.sleep_efficiency, mark)
        ax.annotate('You',
                    xy=(x_pos, user.sleep_efficiency),
                    xytext=(x_pos +0.2, user.sleep_efficiency),
                    arrowprops=dict(facecolor='black', shrink=0.05))


def graph_caffeine_influence_awakenings(df: pd.DataFrame,user:User,ax):
    """
       Plots the relationship between caffeine consumption and number of awakenings during the night.
       Creates a count plot for caffeine consumption categories (Low, Medium, High, Very High) against
       categories of the number of awakenings (0-2, 3-5, 6+). It also marks the user's data point on the plot.

       Parameters:
       df : pd.DataFrame
           The DataFrame containing the data. It must have columns named 'Caffeine consumption' and 'Awakenings'.
           The 'Caffeine consumption' column should be numeric and represent the amount of caffeine consumed.
           The 'Awakenings' column should be numeric and represent the number of times a user wakes up during the night.

       user : User
           The User object that contains the user's individual data. The `user` should have attributes:
           - `coffein_consumption`: A numeric value representing the amount of caffeine consumed by the user.
           - `waking_up_during_night`: A numeric value representing the number of awakenings the user experiences at night.

       ax : matplotlib.axes.Axes
           The axes to plot the graph on.

       Notes:
       The user mark is marked with a "hand-drawn" style using Matplotlib's xkcd mode.
       """
    caffeine_bins = [0, 50, 100, 150, 200]
    caffeine_labels = ['Low', 'Medium', 'High', 'Very High']
    awakening_bins = [0, 2, 5, 10]
    awakening_labels = ['0-2', '3-5', '6+']
    df['Caffeine consumption (Category)'] = pd.cut(df['Caffeine consumption'], bins=caffeine_bins,
                                                   labels=caffeine_labels, right=False)
    df['Awakenings (Category)'] = pd.cut(df['Awakenings'], bins=awakening_bins, labels=awakening_labels, right=False)
    sns.countplot(x='Caffeine consumption (Category)', hue='Awakenings (Category)', data=df, palette='viridis', ax=ax)
    plt.xlabel('Caffeine Consumption', fontsize=12)
    plt.ylabel('Number of Awakenings', fontsize=12)
    user_caffeine_category = pd.cut([user.coffein_consumption], bins=caffeine_bins, labels=caffeine_labels, right=False)[0]
    user_awakening_category = pd.cut([user.waking_up_during_night], bins=awakening_bins, labels=awakening_labels, right=False)[0]
    with plt.xkcd():
        ax.plot(user_caffeine_category, user_awakening_category, 'or', markersize=10, label='You', zorder=5)
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles=handles, labels=labels, loc='upper right')
    plt.tight_layout()


def graph_sleep_efficiency_age(df: pd.DataFrame,user,ax):
    """
        Plots the average sleep efficiency for age groups in 5-year intervals.
        This function groups the data by age ranges (e.g., 0-4, 5-9, etc.), calculates the average sleep efficiency
        for each group, and displays a horizontal bar plot.

        Parameters:
        df : pd.DataFrame
            The DataFrame containing the data. It must have columns named 'Age' and 'Sleep efficiency'.

            user : User
            The User that contains the attribute `sleep_efficiency`, representing the user's sleep efficiency value and age representing age of the user

         ax : matplotlib.axes.Axes
            The matplotlib Axes object where the plot will be drawn.

        Notes:
            The user mark is marked with a "hand-drawn" style using Matplotlib's xkcd mode.

        """
    bins = range(0, 81, 5)
    labels = [f'{i}-{i + 4}' for i in range(0, 80, 5)]
    df['Age Group'] = pd.cut(df['Age'], bins=bins, right=False, labels=labels)
    avg_sleep_efficiency = df.groupby('Age Group')['Sleep efficiency'].mean().reset_index()
    sns.set_theme(style="whitegrid")
    plt.xlabel('Average Sleep Efficiency', fontsize=12)
    plt.ylabel('Age Group', fontsize=12)
    sns.despine(left=True, bottom=True)
    plt.tight_layout()
    sns.barplot(
        data=avg_sleep_efficiency,
        x='Sleep efficiency',
        y='Age Group',
        orient='h',ax=ax
    )
    user_age_group=pd.cut([user.age],bins=bins, right=False, labels=labels)[0]
    with plt.xkcd():
        ax.plot(user.sleep_efficiency,user_age_group,"or")
        ax.annotate('You',
                    xy=(user.sleep_efficiency, user_age_group),
                    xytext=(user.sleep_efficiency, user_age_group),
                    arrowprops=dict(facecolor='black', shrink=0.05))


def graph_exercise_sleep_efficiency(df: pd.DataFrame, user,ax):
    sns.set_theme(style="white")
    sns.scatterplot(x='Sleep efficiency', y='Exercise frequency', hue='Exercise frequency',s=50,data=df, ax=ax,legend=True)
    plt.xlabel("Sleep Efficiency", fontsize=10)
    plt.ylabel("Exercise Frequency", fontsize=10)
    sns.despine()
    plt.tight_layout(h_pad=2)
    ax.legend(fontsize=8, title="Exercise Frequency", title_fontsize='8')
    with plt.xkcd():
        ax.scatter(x=user.sleep_efficiency,y= user.exercise, color='b', s=100, zorder=5, edgecolor='black', alpha=0.8)
        ax.annotate('You',
                xy=(user.sleep_efficiency, user.exercise),
                xytext=(user.sleep_efficiency, user.exercise))


def graph_male_female(df:pd.DataFrame,user,ax):
    """
    Plots a boxplot for 'Sleep efficiency' by gender and annotates the user's specific value.
    Uses Seaborn's boxplot to visualize the distribution of 'Sleep efficiency' for different genders
    and overlays a horizontal line and annotation for the user's specific sleep efficiency value.

    Parameters:
    df : pd.DataFrame
        The DataFrame containing the data. It must have columns named 'Gender' and 'Sleep efficiency'.

    user : User
        The User that contains the attributes `sex` (indicating the user's gender as 'Male' or 'Female') and
        `sleep_efficiency` (representing the user's sleep efficiency value).

    ax : matplotlib.axes.Axes
        The matplotlib Axes object where the plot will be drawn.

    Notes:
    The plot is created with a fun "hand-drawn" style using Matplotlib's xkcd mode.
    """
    sns.boxplot(data=df, x='Gender', y='Sleep efficiency', hue='Gender', palette={'Female': 'red', 'Male': 'blue'}, legend=False,ax=ax)
    plt.xlabel('Gender',fontsize=12)
    plt.ylabel('Sleep Efficiency',fontsize=12)
    with plt.xkcd():
        if user.sex== 'Male':
            x_pos=1
            line_color = 'r'
        else:
            x_pos=0
            line_color = 'b'
        ax.hlines(y=user.sleep_efficiency, xmin=x_pos - 0.4, xmax=x_pos + 0.4, color=line_color, linewidth=2)
        ax.annotate(
            'You',
            xy=(x_pos, user.sleep_efficiency),
            xytext=(x_pos + 0.1, user.sleep_efficiency + 0.1),
            arrowprops=dict(
                facecolor='k',
                shrink=0.1,width=0.5, headwidth=8
            )
        )

if __name__ == '__main__':
    pass
    #grpahs daataset
    data_sleep_efficiency = "../Data/Sleep_Efficiency.csv"
    data=open_file(data_sleep_efficiency)




