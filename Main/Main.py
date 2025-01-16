import pandas
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
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

def show_table(df:pd.DataFrame):
    if df is not None:
        print(df.describe())
        print(df.head())
    else:
        print("No data to display")


def distribution(df:pd.DataFrame):
    df = df.dropna()
    sns.kdeplot(data=df,x='Sleep efficiency',fill=True).set_title('Sleep efficiency', fontsize=20)
    plt.xlabel('Sleep Efficiency', fontsize=12)
    plt.ylabel('Density', fontsize=12)
    plt.show()

def percentage(df:pd.DataFrame):
    df = df.dropna()
    plt.hist(df['REM sleep percentage'], label='REM (%)', alpha=0.5)
    plt.hist(df['Deep sleep percentage'], label='Deep (%)', alpha=0.5)
    plt.hist(df['Light sleep percentage'], label='Light (%)', alpha=0.5)
    plt.xlabel('percentage')
    plt.ylabel('count')
    plt.legend()
    plt.show()

def age_distribution_sleep_efficiency(df:pd.DataFrame):
    df = df.dropna()
    sns.set_theme(style="whitegrid")
    sns.barplot(df, x=df['Age'].head(20), y=df['Sleep efficiency'],hue='Exercise frequency',orient='h')
    plt.xlabel('Sleep Efficiency', fontsize=12)
    plt.ylabel('Age', fontsize=12)
    plt.xticks([x for x in range(1,71, 5)],  rotation=45)
    plt.title('Age vs Sleep Efficiency and Exercise frequency',fontsize=16)
    plt.grid(axis='both', alpha=0.7)
    sns.despine(left=True, bottom=True)
    plt.show()

def age_distribution_sleep_efficiency_scatter(df: pd.DataFrame):
    sns.scatterplot(data=df, x='Age', y='Sleep efficiency')
    plt.title('Age vs Sleep Efficiency')
    plt.xlabel('Age')
    plt.ylabel('Sleep Efficiency')
    plt.show()

def graph_smoking_influence_sleep_efficiency(df:pd.DataFrame):
    df = df.dropna()
    sns.barplot(df,x='Smoking status', y='Sleep efficiency',palette=['#FF4D00', '#A6D609'])
    plt.title('Smoking Status vs Sleep Efficiency', fontsize=16)
    plt.xlabel('Smoking Status', fontsize=12)
    plt.ylabel('Sleep Efficiency', fontsize=12)
    plt.tight_layout()
    plt.show()

def graph_caffeine_influence_awakenings(df:pd.DataFrame):
    df = df.dropna()
    sns.countplot(x=df['Caffeine consumption'],hue=df['Awakenings'], palette='viridis')
    plt.title('Coffeine consumption vs Awakenings during night', fontsize=16)
    plt.xlabel('Coffeine consumption', fontsize=12)
    plt.ylabel('Awakenings(number)', fontsize=12)
    plt.show()

def age_distribution_sleep_efficiency1(df: pd.DataFrame):
    df = df.dropna().copy()
    df['Age groups'] = pd.cut(df['Age'], bins=range(0, int(df['Age'].max()) + 8, 8), right=False)
    sns.set_theme(style="whitegrid")
    plt.figure(figsize=(12, 8))
    sns.barplot(
        data=df,
        x='Sleep efficiency',
        y='Age groups',
        hue='Exercise frequency',
        orient='h'
    )
    plt.xlabel('Sleep Efficiency', fontsize=12)
    plt.ylabel('Age', fontsize=12)
    plt.title('Age vs Sleep Efficiency and Exercise Frequency', fontsize=16)
    plt.grid(axis='both', alpha=0.7)
    sns.despine(left=True, bottom=True)
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    file_path = "../Data/Sleep_Efficiency.csv"
    data = open_file(file_path)
    # print(data)
    # show_table(data)
    #distribution(data)
    # percentage(data)
    # graph_caffeine_influence_awakenings(data)
    age_distribution_sleep_efficiency1(data)
   # age_distribution_sleep_efficiency_scatter(data)
   #  graph_smoking_influence_sleep_efficiency(data)

