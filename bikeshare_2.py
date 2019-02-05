import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input('What city data do you want to explore: ')
    while city.lower() not in ('chicago', 'new york city', 'washington'):
        print('Sorry! I didnt catch that, try again!')
        city = input('What city data do you want to explore: ')

    # TO DO: get user input for month (all, january, february, ... , june)
    months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    month = input('What month do you want to explore: ')
    while month.lower() not in months:
        print('Sorry! I didnt catch that, try again!')
        month = input('What month do you want to explore: ')

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    weekdays = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    day = input('What day do you want to explore: ')
    while day.lower() not in weekdays:
        print('Sorry! I didnt catch that, try again!')
        day = input('What day do you want to explore: ')

    print('-'*40)
    return city.lower(), month.lower(), day.lower()


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df= pd.read_csv(CITY_DATA[city])
    
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    df['month'] = df['Start Time'].dt.month
    
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
        month = months.index(month) + 1
        df = df[df['month'] == month]
       
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
        


    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    popular_month = int(df['month'].mode())
    print("Busiest month is: " + str(months[popular_month - 1]))


    # TO DO: display the most common day of week
    popular_day = df['day_of_week'].mode().to_string(index = False)
    print("Busiest day is: " + str(popular_day))
    # TO DO: display the most common start hour
    popular_start_hour = df['Start Time'].dt.hour.mode()[0]
    print("The most common start hour is: " + str(popular_start_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    print("The most commonly used start station is: " + df['Start Station'].mode().to_string(index = False))


    # TO DO: display most commonly used end station
    print("The most commonly used end station is: " + df['End Station'].mode().to_string(index = False))

    # TO DO: display most frequent combination of start station and end station trip
    popular_trips = df.groupby(['Start Station', 'End Station'])['Start Time'].count().sort_values(ascending = False)
    print("Most popular trip: " + str(popular_trips.index[0][0]) + " to " + str(popular_trips.index[0][1]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_trip_duration = df['Trip Duration'].sum()
    m, s = divmod(total_trip_duration, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)
   
    print("Total travel time is: "+ str(d) + " days, " + str(h) + " hours, " + str(m) + " minutes and " + str(s) + " seconds.")


    # TO DO: display mean travel time
    mean_trip_duration = df['Trip Duration'].mean()
    m, s = divmod(mean_trip_duration, 60)
    h, m = divmod(m, 60)   
    print("Average travel time is: " + str(h) + " hours, " + str(m) + " minutes and " + str(s) + " seconds.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types)


    # TO DO: Display counts of gender
    
    if 'Gender' in df:
        gender_counts = df['Gender'].value_counts()
        print(gender_counts)

    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        print("Earliest birth year: " + str(int(df['Birth Year'].min())))
        print("Most recent birth year: " + str(int(df['Birth Year'].max())))
        print("Most common birth year: " + str(int(df['Birth Year'].mode())))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    head = 0
    tail = 5
    while True:
        display_raw_data = input('\nWould you like to see raw data? Enter yes or no.\n')
        if display_raw_data.lower() != 'yes':
            break
        print(df.iloc[head:tail])
        head += 5
        tail += 5

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
