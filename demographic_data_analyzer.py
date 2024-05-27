import pandas as pd

def calculate_demographic_data(print_data=True):
    # Read data from file
    column_names = [
        'age', 'workclass', 'fnlwgt', 'education', 'education-num', 'marital-status',
        'occupation', 'relationship', 'race', 'sex', 'capital-gain', 'capital-loss',
        'hours-per-week', 'native-country', 'salary'
    ]
    
    # Read the data, explicitly skip header row
    df = pd.read_csv('adult.data.csv', header=None, names=column_names, na_values=' ?', skipinitialspace=True)
    
    # Drop rows with missing values
    df.dropna(inplace=True)
    
    # Strip whitespace from all string columns
    str_cols = df.select_dtypes(['object']).columns
    df[str_cols] = df[str_cols].apply(lambda x: x.str.strip())

    # Ensure correct data types
    # Convert all relevant columns to numeric, if conversion fails, invalid parsing will set as NaN
    numeric_columns = ['age', 'fnlwgt', 'education-num', 'capital-gain', 'capital-loss', 'hours-per-week']
    df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric, errors='coerce')
    
    # Drop rows with NaN values resulting from failed conversions
    df.dropna(inplace=True)

    # How many of each race are represented in this dataset? This should be a Pandas series with race names as the index labels.
    race_count = df['race'].value_counts()

    # What is the average age of men?
    average_age_men = df[df['sex'] == 'Male']['age'].mean().round(1)

    # What is the percentage of people who have a Bachelor's degree?
    percentage_bachelors = ((df['education'] == 'Bachelors').mean() * 100).round(1)

    # What percentage of people with advanced education (`Bachelors`, `Masters`, or `Doctorate`) make more than 50K?
    # What percentage of people without advanced education make more than 50K?

    # with and without `Bachelors`, `Masters`, or `Doctorate`
    higher_education = df['education'].isin(['Bachelors', 'Masters', 'Doctorate'])
    lower_education = ~higher_education

    # percentage with salary >50K
    higher_education_rich = ((df[higher_education]['salary'] == '>50K').mean() * 100).round(1)
    lower_education_rich =  ((df[lower_education]['salary'] == '>50K').mean() * 100).round(1)

    # What is the minimum number of hours a person works per week (hours-per-week feature)?
    min_work_hours = df['hours-per-week'].min()

    # What percentage of the people who work the minimum number of hours per week have a salary of >50K?
    num_min_workers = df[df['hours-per-week'] == min_work_hours]
    rich_percentage = ((num_min_workers['salary'] == '>50K').mean() * 100).round(1)

    # What country has the highest percentage of people that earn >50K?
    country_salary = df[df['salary'] == '>50K']['native-country'].value_counts()
    country_count = df['native-country'].value_counts()
    highest_earning_country = (country_salary / country_count * 100).idxmax()
    highest_earning_country_percentage = (country_salary / country_count * 100).max().round(1)

    # Identify the most popular occupation for those who earn >50K in India.
    top_IN_occupation = df[(df['native-country'] == 'India') & (df['salary'] == '>50K')]['occupation'].mode()[0]

    # DO NOT MODIFY BELOW THIS LINE

    if print_data:
        print("Number of each race:\n", race_count) 
        print("Average age of men:", average_age_men)
        print(f"Percentage with Bachelors degrees: {percentage_bachelors}%")
        print(f"Percentage with higher education that earn >50K: {higher_education_rich}%")
        print(f"Percentage without higher education that earn >50K: {lower_education_rich}%")
        print(f"Min work time: {min_work_hours} hours/week")
        print(f"Percentage of rich among those who work fewest hours: {rich_percentage}%")
        print("Country with highest percentage of rich:", highest_earning_country)
        print(f"Highest percentage of rich people in country: {highest_earning_country_percentage}%")
        print("Top occupations in India:", top_IN_occupation)

    return {
        'race_count': race_count,
        'average_age_men': average_age_men,
        'percentage_bachelors': percentage_bachelors,
        'higher_education_rich': higher_education_rich,
        'lower_education_rich': lower_education_rich,
        'min_work_hours': min_work_hours,
        'rich_percentage': rich_percentage,
        'highest_earning_country': highest_earning_country,
        'highest_earning_country_percentage': highest_earning_country_percentage,
        'top_IN_occupation': top_IN_occupation
    }
