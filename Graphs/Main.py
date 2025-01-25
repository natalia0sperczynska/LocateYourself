import matplotlib
import pandas
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.pyplot import subplot, xlabel, ylabel, tight_layout

file_path1 = "/Data/Sleep_Efficiency.csv"


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


def distribution(df: pd.DataFrame,user,ax):
    #df = df.dropna()
    sns.kdeplot(data=df, x='Sleep efficiency',  fill=True,ax=ax).set_title('Sleep efficiency', fontsize=20)
    plt.xlabel('Sleep Efficiency', fontsize=12)
    plt.ylabel('Density', fontsize=12)
    ax.axvline(x=user.sleep_efficeincy, color='r', label='axvline - full height')
    #plt.show()


def age_distribution_sleep_efficiency(df: pd.DataFrame):
    df = df.dropna()
    sns.set_theme(style="whitegrid")
    sns.barplot(df, x=df['Age'].head(20), y=df['Sleep efficiency'], hue='Exercise frequency', orient='h')
    plt.xlabel('Sleep Efficiency', fontsize=12)
    plt.ylabel('Age', fontsize=12)
    plt.xticks([x for x in range(1, 71, 5)], rotation=45)
    plt.title('Age vs Sleep Efficiency and Exercise frequency', fontsize=16)
    plt.grid(axis='both', alpha=0.7)
    sns.despine(left=True, bottom=True)

def graph_smoking_influence_sleep_efficiency(df: pd.DataFrame,ax):
    df = df.dropna()
    sns.barplot(df, x='Smoking status', y='Sleep efficiency', palette=['#FF4D00', '#A6D609'],ax=ax)
    plt.title('Smoking Status vs Sleep Efficiency', fontsize=10)
    plt.xlabel('Smoking Status', fontsize=12)
    plt.ylabel('Sleep Efficiency', fontsize=12)


def graph_caffeine_influence_awakenings(df: pd.DataFrame,ax):
    df = df.dropna()
    sns.countplot(x=df['Caffeine consumption'], hue=df['Awakenings'], palette='viridis',ax=ax)
    plt.title('Coffeine consumption vs Awakenings during night', fontsize=16)
    plt.xlabel('Coffeine consumption', fontsize=12)
    plt.ylabel('Awakenings(number)', fontsize=12)


def age_distribution_sleep_efficiency1(df: pd.DataFrame,ax):
    df = df.dropna().copy()
    df['Age groups'] = pd.cut(df['Age'], bins=range(0, int(df['Age'].max()) + 8, 8), right=False)
    sns.set_theme(style="whitegrid")
    plt.figure(figsize=(12, 8))
    sns.barplot(
        data=df,
        x='Sleep efficiency',
        y='Age groups',
        hue='Exercise frequency',
        orient='h',ax=ax
    )
    plt.xlabel('Sleep Efficiency', fontsize=12)
    plt.ylabel('Age', fontsize=12)
    plt.title('Age vs Sleep Efficiency and Exercise Frequency', fontsize=16)
    plt.grid(axis='both', alpha=0.7)
    sns.despine(left=True, bottom=True)
    plt.tight_layout()


def graph_male_female(df:pd.DataFrame,user,ax):
    sns.boxplot(data=df, x='Gender', y='Sleep efficiency', hue='Gender', palette={'Female': 'red', 'Male': 'blue'}, legend=False,ax=ax)
    plt.title('Distribution of Sleep Efficiency by Gender',fontsize=10)
    plt.xlabel('Gender')
    plt.ylabel('Sleep Efficiency')
    if(user.sex=='Male'):
        ax.hlines(y=user.sleep_efficeincy, xmin=0.6, xmax=1.4, color='r', label='axvline - full height')
    else:
        ax.hlines(y=user.sleep_efficeincy, xmin=-0.4, xmax=0.4, color='b', label='axvline - full height')

if __name__ == '__main__':
    pass
    #grpahs first daataset
    data_sleep_efficiency = "../Data/Sleep_Efficiency.csv"
    data=open_file(data_sleep_efficiency)
    # data_sleep_efficiency = open_file(data_sleep_efficiency)
    # plots(data_sleep_efficiency)
    # #print(data)
    # # show_table(data)
    #distribution(data)
    # #percentage(data)
    # graph_caffeine_influence_awakenings(data_sleep_efficiency)
    # age_distribution_sleep_efficiency1(data_sleep_efficiency)




