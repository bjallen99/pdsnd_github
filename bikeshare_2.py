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
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    while True:
            try:
                city = str(input("Please enter the city you would like to explore (chicago, new york city, washington): ")).lower()
                contains_city = CITY_DATA[city]
                break # if no exceptions, break from loop
            except:
                print("That is not a valid city entry - please try again") # otherwise, prompt user for another entry and restart loop
                continue
    # get user input for month (all, january, february, ... , june)
    while True:
        month = str(input("Please enter the month you would like to explore (all, january, february... , june): ")).lower()
        if month in ("all", "january", "february", "march", "april", "may", "june"):
            break # if 'month' is in list, break from loop
        else:
            print("That is not a valid month entry - please try again") # otherwise, prompt user for another entry and restart loop
            continue

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = str(input("Please enter the day to explore (all, monday, tuesday... , sunday): ")).lower()
        if day.lower() in ("all", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"):
            break # if 'day' is in list, break from loop
        else:
            print("That is not a valid entry - please try again")  # otherwise, prompt user for another entry and restart loop
            continue

    print('-'*40) # print line under the title to improve readbility
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
    #load the data for user specified city
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column from string to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns -- note same solution as problem 3
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable -- note same solution as problem 3
    if month != 'all':
        #months in array sequentially with index '0', so add one to get a numeric representation of month
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        # filter by month numeric representation of month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable - as above, same solution as problem #3
    if day != 'all':
        # filter by day of week to create the new dataframe - no trans needed - days stored as weekday names
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most popular day and hour of travel.

    Args:
        (df) bikeshare data df with columns: Start Time, End Time, Trip Duration, Start Station, End Station, User           Type, Gender, Birth Year)
     """
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # convert the Start Time column from string to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # display the most common start times
    df['time_only'] = df['Start Time'].dt.time
    popular_time = df.time_only.mode()[0]
    print('The Most Frequent Time of Travel is: ', popular_time)

    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print('The Most Frequent Day of Travel is: ', popular_day)

    # display the most common start hour
    popular_hour = df['day_of_week'].mode()[0]
    # extract hour from the Start Time column to create an hour column

    # find the most common hour (from 0 to 23)
    df['hour'] = df['Start Time'].dt.hour #create an hour column on which we can run mode
    popular_hour = df.hour.mode()[0]
    print('Most Frequent Start Hour: ', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip.

        Args:
        (df) bikeshare data df with columns: Start Time, End Time, Trip Duration, Start Station, End Station, User           Type, Gender, Birth Year)
     """
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_st = df['Start Station'].mode()[0]
    print('The most commonly used start station is: ', popular_start_st)

    # display most commonly used end station
    popular_end_st = df['End Station'].mode()[0]
    print('The most commonly used end station is: ', popular_end_st)

    # display most frequent combination of start station and end station trip
    station_combo = df['Start Station'] + " >>> " + df['End Station'] #combine start and stop for mode
    popular_combo_st = station_combo.mode()[0]
    print('The most common combination of start and stop stations is: \n', popular_combo_st)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration.
        Args:
        (df) bikeshare data df with columns: Start Time, End Time, Trip Duration, Start Station, End Station, User           Type, Gender, Birth Year)
     """
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print ("The total travel time is: ", round(df['Trip Duration'].sum()/86400, 2), "days") #change seconds to days
    # display mean travel time
    print("The average travel time is: ", round(df['Trip Duration'].mean()/60, 2), "mins") # change seconds to mins


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays key statistics on bikeshare users.
        Args:
        (df) bikeshare data df with columns: Start Time, End Time, Trip Duration, Start Station, End Station, User           Type, Gender, Birth Year)
     """
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print("Count of user types:\n")
    print(user_types.to_string(header=False),"\n") #print but remove footer for better readibility

    # Display counts of gender
    try:
        gender_types = df['Gender'].value_counts()
        print("Count of user genders:\n")
        print(gender_types.to_string(header=False), "\n") #print but remove footer for better readibility
    except:
        print("\n No gender data... \n") #For washington with missing columns, return appropriate message

    # Display earliest, most recent, and most common year of birth
    try:
        by_min = str(df['Birth Year'].min())
        by_max = str(df['Birth Year'].max())
        most_common_by = str(df['Birth Year'].mode()[0])
        print("The eldest bikeshare user was born in: ", by_min[:4]) # trim uneccesary characters
        print("The youngest bikeshare user was born in: ", by_max[:4])
        print("The most common birth year of riders is: ", most_common_by[:4])
    except:
        print("\n No birth year data... \n") #For washington with missing columns, return appropriate message

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def print_raw_data(df):
    """Displays raw data on request by the user. Asks for user to indicate if they want to display raw input, tells         the user number of rows and prompts for how many the user would like to display.
        Args:
        (df) bikeshare data df with columns: Start Time, End Time, Trip Duration, Start Station, End Station, User           Type, Gender, Birth Year)
     """
    print('\nDisplaying individual trip data...\n')
    start_time = time.time()

    # seek user input on whether they would like to see individual trip data
    while True:
        user_choice = str(input("Would you like to view individual trip data? (yes, no)): ")).lower()
        if user_choice in ("yes"):
            total_rows=len(df.axes[0]) # get number of rows
            print("There are ", total_rows, " records in your filtered range\n")
            try: #ask the user to specific how many rows they want to display
                raw_rows = int(input("How many raw data records would you like to see (enter as int)?: "))
                i = 0
                while i < raw_rows:
                    print(df.iloc[i], '\n') #print raw data for the filtered content
                    i += 1
                break #break for while loop as we have diplayed
            except:
                print("Not a valid input for records to display - let's try again!")
                continue
        elif user_choice in ("no"):
            break
        else:
            print("That is not a valid entry - please try again")  # otherwise, prompt for another entry
            continue

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        print_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
