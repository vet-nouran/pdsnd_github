import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }


months = ('january', 'february', 'march', 'april', 'may', 'june')

weekdays = ('sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday',
            'saturday')

def choice(prompt, choices=('y', 'n')):
    """Return a valid input from the user given an array of possible answers.
    """

    while True:
        choice = input(prompt).lower().strip()
        # terminate the program if the input is end
        if choice == 'end':
            raise SystemExit
        # triggers if the input has only one name
        elif ',' not in choice:
            if choice in choices:
                break
        # triggers if the input has more than one name
        elif ',' in choice:
            choice = [i.strip().lower() for i in choice.split(',')]
            if list(filter(lambda x: x in choices, choice)) == choice:
                break

        prompt = ("\nSomething is not right. Please mind the formatting and "
                  "be sure to enter a valid option:\n>")

    return choice

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    while True:
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
        city = choice("\nFor what city(ies) do you want do select data, "
                      "New York City, Chicago or Washington? Use commas "
                      "to list the names.\n>", CITY_DATA.keys())


    # TO DO: get user input for month (all, january, february, ... , june)
        month = choice("\nFrom January to June, for what month(s) do you "
                       "want do filter data? Use commas to list the names.\n>",
                       months)


    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
        day = choice("\nFor what weekday(s) do you want do filter bikeshare "
                     "data? Use commas to list the names.\n>", weekdays)
        
        
        confirmation = choice("\nPlease confirm that you would like to apply "
                              "the following filter(s) to the bikeshare data."
                              "\n\n City(ies): {}\n Month(s): {}\n Weekday(s)"
                              ": {}\n\n [y] Yes\n [n] No\n\n>"
                              .format(city, month, day))
        if confirmation == 'y':
            break
        else:
            print("\nLet's try this again!")


    print('-'*40)
    return city, month, day


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
    print("\nThe program is loading the data for the filters of your choice.")
    start_time = time.time()

    # filter the data according to the selected city filters
    if isinstance(city, list):
        df = pd.concat(map(lambda city: pd.read_csv(CITY_DATA[city]), city),
                       sort=True)
        # reorganize DataFrame columns after a city concat
        try:
            df = df.reindex(columns=['Unnamed: 0', 'Start Time', 'End Time',
                                     'Trip Duration', 'Start Station',
                                     'End Station', 'User Type', 'Gender',
                                     'Birth Year'])
        except:
            pass
    else:
        df = pd.read_csv(CITY_DATA[city])

    # create columns to display statistics
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Month'] = df['Start Time'].dt.month
    df['Weekday'] = df['Start Time'].dt.weekday_name
    df['Start Hour'] = df['Start Time'].dt.hour

    # filter the data according to month and weekday into two new DataFrames
    if isinstance(month, list):
        df = pd.concat(map(lambda month: df[df['Month'] ==
                           (months.index(month)+1)], month))
    else:
        df = df[df['Month'] == (months.index(month)+1)]

    if isinstance(day, list):
        df = pd.concat(map(lambda day: df[df['Weekday'] ==
                           (day.title())], day))
    else:
        df = df[df['Weekday'] == day.title()]

    print("\nThis took {} seconds.".format((time.time() - start_time)))
    print('-'*40)
    
    return df


def time_statistics(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    most_common_month = df['Month'].mode()[0]
    print('For the selected filter, the month with the most travels is: ' +
          str(months[most_common_month-1]).title() + '.')

    # display the most common day of week
    most_common_day = df['Weekday'].mode()[0]
    print('For the selected filter, the most common day of the week is: ' +
          str(most_common_day) + '.')

    # display the most common start hour
    most_common_hour = df['Start Hour'].mode()[0]
    print('For the selected filter, the most common start hour is: ' +
          str(most_common_hour) + '.')

    print("\nThis took {} seconds.".format((time.time() - start_time)))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = str(df['Start Station'].mode()[0])
    print("For the selected filters, the most common start station is: " +
          most_common_start_station)

    # display most commonly used end station
    most_common_end_station = str(df['End Station'].mode()[0])
    print("For the selected filters, the most common start end is: " +
          most_common_end_station)

    # display most frequent combination of start station and
    # end station trip
    df['Start-End Combination'] = (df['Start Station'] + ' - ' +
                                   df['End Station'])
    most_common_start_end_combination = str(df['Start-End Combination']
                                            .mode()[0])
    print("For the selected filters, the most common start-end combination "
          "of stations is: " + most_common_start_end_combination)

    print("\nThis took {} seconds.".format((time.time() - start_time)))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    
    
    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    total_travel_time = (str(int(total_travel_time//86400)) +
                         'd ' +
                         str(int((total_travel_time % 86400)//3600)) +
                         'h ' +
                         str(int(((total_travel_time % 86400) % 3600)//60)) +
                         'm ' +
                         str(int(((total_travel_time % 86400) % 3600) % 60)) +
                         's')
    print('For the selected filters, the total travel time is : ' +
          total_travel_time + '.')

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    mean_travel_time = (str(int(mean_travel_time//60)) + 'm ' +
                        str(int(mean_travel_time % 60)) + 's')
    print("For the selected filters, the mean travel time is : " +
          mean_travel_time + ".")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    
     # Display counts of user types
    user_types = df['User Type'].value_counts().to_string()
    print("Distribution for user types:")
    print(user_types)

    # Display counts of gender
    try:
        gender_distribution = df['Gender'].value_counts().to_string()
        print("\nDistribution for each gender:")
        print(gender_distribution)
    except KeyError:
        print("We're sorry! There is no data of user genders for {}."
              .format(city.title()))

    # Display earliest, most recent, and most common year of birth
    try:
        earliest_birth_year = str(int(df['Birth Year'].min()))
        print("\nFor the selected filter, the oldest person to ride one "
              "bike was born in: " + earliest_birth_year)
        most_recent_birth_year = str(int(df['Birth Year'].max()))
        print("For the selected filter, the youngest person to ride one "
              "bike was born in: " + most_recent_birth_year)
        most_common_birth_year = str(int(df['Birth Year'].mode()[0]))
        print("For the selected filter, the most common birth year amongst "
              "riders is: " + most_common_birth_year)
    except:
        print("We're sorry! There is no data of birth year for {}."
              .format(city.title()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_statistics(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()