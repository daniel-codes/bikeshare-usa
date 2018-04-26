# Author: Daniel Cummings
# Project: Explore US Bikeshare Data
# Date: 4/23/2018
# Email: daniel.j.cummings@me.com

import time
import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt

# Bikeshare ride data source(s)
CITY_DATA = { 'Chicago': 'chicago.csv',
              'New York City': 'new_york_city.csv',
              'Washington': 'washington.csv' }

# Lists for lookup and index reference
month_list = ['All', 'January', 'February', 'March',\
              'April', 'May', 'June']
day_list = ['All', 'Sunday', 'Monday', 'Tuesday',\
            'Wednesday', 'Thursday', 'Friday', 'Saturday']

# Matplotlib axis and title font size
axis_font = 14

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
        # Get user input for city (Chicago, New York City, Washington).
        print('City data is available for Chicago, New York City, and Washington.')
        city = input('Enter City: ').title()
        while city not in CITY_DATA:
            city = input('Invalid entry.\nPlease enter Chicago, New York City, or\
            Washington: ').title()
        
        # Get user input for month (all, january, february, ... , june)
        print('\nMonth data is available for all, January, February, ... , June.')
        month = input('Enter Month (full name) or All: ').title()
        while month not in month_list:
            month = input('Invalid entry, options are: \
                        \n - All \n - January \n - February \n - March \
                        \n - April \n - May \n - June \
                        \nPlease enter a valid month: ').title()
        
        # Get user input for day of week (all, monday, tuesday, ... sunday)
        print('\nDay of the week data is available for all, Monday, Tuesday, ... , Sunday.')
        day = input('Enter Day of the Week (full name) or All: ').title()
        while day not in day_list:
            day = input('Invalid entry, options are: \
                        \n - All \n - Sunday \n - Monday \n - Tuesday \
                        \n - Wednesday \n - Thursday \n - Friday \n - Saturday \
                        \nPlease enter a valid day of the week: ').title()
        
        # Verify selection with user
        answer = input('You selected the following:\n  City: {}\n  Month(s): {}\n  Day(s): {}\
                        \nIs this correct? (Y or N):'.format(city.title(), month, day)).lower()
        while answer not in ['y','n']:
            answer = input('Incorrect input. Enter Y or N:').lower()
                            
        if answer == 'y':
            break
        else:
            continue
        
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df_all - Pandas DataFrame containing city data with no filters
        df - Pandas DataFrame containing city data filtered by month and day
    """
    print('Loading city data...')
 
    # Load DataFrame for city
    df = pd.read_csv(CITY_DATA[city]) 
    
    # Convert start and end times to datetime type
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    
    # Create multiple new DataFrame Time Series
    df['month'] = df['Start Time'].dt.month
    df['day_str'] = df['Start Time'].dt.weekday_name
    df['day_int'] = df['Start Time'].dt.weekday
    df['hour'] = df['Start Time'].dt.hour  
    
    # Create side copy of df without filters
    df_all = df.copy()
    
    # Filter DataFrame by month
    month_idx = month_list.index(month)
    if month != 'All':
        df = df[df['month'] == month_idx]

    # Filter DataFrame by day of week
    if day != 'All':
        df = df[df['day_str'] == day]

    print('-'*40)
    return df_all, df

def time_stats(df, city, month, day):
    """
    Displays statistics on the most frequent times of travel.
    
    Input:
    df - expects unfiltered df to generate month and day plots
    """

    print('\nCalculating The Most Frequent Times of Travel...\
          \n\nCity: {}, Month: {}, Day: {}.\n'.format(city, month, day))
    
    # Display the most/least common month
    month_max = df['month'].value_counts().idxmax()
    print('Most common month for travel (Jan-Jun): {}'.format(month_list[month_max]))
    month_min = df['month'].value_counts().idxmin()
    print('Least common month for travel (Jan-Jun): {}'.format(month_list[month_min]))
    
    # Plot a histogram of the ridership per month for specified city
    plt.hist(df['month'].values, bins=6, range=(0.5,6.5), align='mid',\
        edgecolor='gray', alpha=0.5)
    plt.xlabel('Month', fontsize=axis_font)
    plt.ylabel('Ride Frequency', fontsize=axis_font)
    plt.title('{} Ridership per Month'.format(city), fontsize=axis_font)
    month_plt_idx = [1, 2, 3, 4, 5, 6]
    month_plt_list = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
    plt.xticks(month_plt_idx, month_plt_list)
    plt.show()
    
    # Filter DataFrame by month
    month_idx = month_list.index(month)
    if month != 'All':
        df = df[df['month'] == month_idx]

    # Display the most/least common day of week
    day_max = df['day_str'].value_counts().idxmax()
    print('Most common day for travel (Month: {}): {}'.format(month, day_max))
    day_min = df['day_str'].value_counts().idxmin()
    print('Least common day for travel (Month: {}): {}'.format(month, day_min))
    
    # Plot a histogram of the ridership per day for specified city          
    plt.hist(df['day_int'].values, bins=7, range=(-0.5,6.5), align='mid',\
             edgecolor='gray', alpha=0.5, color='g')
    plt.xlabel('Day', fontsize=axis_font)
    plt.ylabel('Ride Frequency', fontsize=axis_font)
    plt.title('{} Ridership per Day of the Week \n(Month: {})'\
              .format(city, month), fontsize=axis_font)
    day_plt_idx = [0, 1, 2, 3, 4, 5, 6]
    day_plt_list = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    plt.xticks(day_plt_idx, day_plt_list)
    plt.show()
    
    # Filter DataFrame by day of week
    if day != 'All':
        df = df[df['day_str'] == day]
        
    # Display the most common start hour
    hr_max = df['hour'].value_counts().idxmax()
    hr_maxt = datetime.datetime.strptime(str(hr_max), "%H")
    print('Most common hour for travel (Month: {}, Day: {}): {}'\
          .format(month, day, hr_maxt.strftime("%I %p")))
    hr_min = df['hour'].value_counts().idxmin()
    hr_mint = datetime.datetime.strptime(str(hr_min), "%H")
    print('Least common hour for travel (Month: {}, Day: {}): {}'\
          .format(month, day, hr_mint.strftime("%I %p")))
    
    # Plot a histogram of the ridership per hour for specified city          
    plt.hist(df['hour'].values, bins=24, align='mid',\
    edgecolor='gray', alpha=0.8, color='r')
    plt.xlabel('Hour (24 hour)', fontsize=axis_font)
    plt.ylabel('Ride Frequency', fontsize=axis_font)
    plt.title('{} Ridership per Hour \n(Month: {}, Day: {})'\
              .format(city, month, day), fontsize=axis_font)
    plt.show()
    
    print('-'*40)

    
def station_stats(df, city, month, day):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\
           \n\nCity: {}, Month: {}, Day: {}.\n'.format(city, month, day))
    start_time = time.time()
    
    # Display most/least commonly used start stations
    start_stn = df['Start Station'].value_counts()
    print('Most common start stations:\
            \n  1. {}\
            \n  2. {}\
            \n  3. {}'
          .format(start_stn.index[0], start_stn.index[1], start_stn.index[2]))
    print('Least common start stations:\
            \n  1. {}\
            \n  2. {}\
            \n  3. {}\n'
          .format(start_stn.index[-1], start_stn.index[-2], start_stn.index[-3]))
    
    # Display most/least commonly used end stations
    end_stn = df['End Station'].value_counts()
    print('Most common end stations:\
            \n  1. {}\
            \n  2. {}\
            \n  3. {}'
          .format(end_stn.index[0], end_stn.index[1], end_stn.index[2]))
    print('Least common end stations:\
            \n  1. {}\
            \n  2. {}\
            \n  3. {}\n'
          .format(end_stn.index[-1], end_stn.index[-2], end_stn.index[-3]))
    
    # display most/least frequent combination of start station and end station trip
    df['Full path'] = df['Start Station'] + ' --> ' + df['End Station']
    full_path = df['Full path'].value_counts()
    print('Most popular routes:\
            \n  1. {}\
            \n  2. {}\
            \n  3. {}'
          .format(full_path.index[0], full_path.index[1], full_path.index[2]))
    print('Least popular routes:\
            \n  1. {}\
            \n  2. {}\
            \n  3. {}'
          .format(full_path.index[-1], full_path.index[-2], full_path.index[-3]))
    
    print("\nCalculation took {:.3f} seconds.".format(time.time() - start_time))
    print('-'*40)
    
    
def trip_duration_stats(df, city, month, day):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\
           \n\nCity: {}, Month: {}, Day: {}.\n'.format(city, month, day))
    
    # display total travel time
    travel_time = df['Trip Duration'].sum()
    print("Total travel time (hrs:min:sec): {}"\
          .format(datetime.timedelta(seconds=travel_time)))
    
    # display mean travel time
    mean_time = df['Trip Duration'].mean()
    print("Mean travel time (hrs:min:sec): {}"\
          .format(datetime.timedelta(seconds=mean_time)))

    df['Trip Minutes'] = df['Trip Duration'] / 60
    females = df[df['Gender']=='Female']
    males = df[df['Gender']=='Male']
    
    # Plot a histogram of trip duration by gender   
    plt.hist([males['Trip Minutes'],females['Trip Minutes']], bins=16,\
             align='mid', stacked=True, range=(0,40),\
             edgecolor='gray', alpha=0.5, label=('males','females'))
    plt.xlabel('Trip Duration (Minutes)', fontsize=axis_font)
    plt.ylabel('Frequency', fontsize=axis_font)
    plt.title('{} Trip Duration Histogram\n by gender (Month: {}, Day: {})'\
              .format(city, month, day), fontsize=axis_font)
    plt.legend()
    plt.show()
    
    year = datetime.date.today().year
    df['age'] = df['Birth Year'].apply(lambda x: year - x)
    age_20s = df[df['age'] < 30]
    age_30s = df[(df['age'] >= 30) & (df['age'] < 40)]
    age_40s = df[(df['age'] >= 40) & (df['age'] < 50)]
    age_50s = df[df['age'] >= 50]
    
    # Plot a histogram of trip duration by gender   
    plt.hist([age_20s['Trip Minutes'], age_30s['Trip Minutes'], age_40s['Trip Minutes'],\
             age_40s['Trip Minutes']], bins=16, align='mid', stacked=True, range=(0,40),\
             edgecolor='gray', alpha=0.5, label=('20\'s','30\'s','40\'s','> 50'))
    plt.xlabel('Trip Duration (Minutes)', fontsize=axis_font)
    plt.ylabel('Frequency', fontsize=axis_font)
    plt.title('{} Trip Duration by Age Group \n(Month: {}, Day: {})'\
              .format(city, month, day), fontsize=axis_font)
    plt.legend()
    plt.show()
    
    print('-'*40)   
    
    
def user_stats(df, city, month, day):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\
           \n\nCity: {}, Month: {}, Day: {}.\n'.format(city, month, day))

    # Display counts of user types
    user_type = df['User Type'].value_counts()
    print('User type stats: \n{}\n'.format(user_type))
    
    # Display counts of gender
    gender = df['Gender'].value_counts()
    print('Gender type stats: \n{}\n'.format(gender))

    # Display earliest, most recent, and most common year of birth
    by_min = df['Birth Year'].min()
    by_max = df['Birth Year'].max()
    by_common = df['Birth Year'].value_counts().idxmax()
    print('Year of birth stats: \nMin: {} \nMax: {} \nMost Common: {}\n'\
          .format(by_min, by_max, by_common))
    
    # Create Series by age and gender for histogram       
    year = datetime.date.today().year
    df['age'] = df['Birth Year'].apply(lambda x: year - x)
    females = df[df['Gender'] == 'Female']
    males = df[df['Gender'] == 'Male']
    
    # Plot a histogram of the ridership by age and gender   
    plt.hist([males['age'], females['age']], bins=35, align='mid', stacked=True,\
             range=(0,80), edgecolor='gray', alpha=0.5, label=('male','female'))
    plt.xlabel('Age (Years)', fontsize=axis_font)
    plt.ylabel('Ride Frequency', fontsize=axis_font)
    plt.title('{} Ridership\n by Age & Gender (Month: {}, Day: {})'\
              .format(city, month, day), fontsize=axis_font)
    plt.legend()
    plt.show()
    
    print('-'*40)

def df_data(df, city, month, day):
    ''' Print filtered DataFrame data for user '''
    print('\nDataFrame data available for...\
           \n\nCity: {}, Month: {}, Day: {}.\n'.format(city, month, day))
    start_time = time.time()
    
    print('\nDataFrame contains {} rows of data.'.format(len(df)))
    
    while True:
        lines = int(input('\nHow many lines of the data would you like to see? (enter number): '))
    
        if lines >= 0 and lines <= len(df):
            break
        else:
            print('Invalide entry. Outside of range 0-{}.'.format(len(df)))
            continue
    
    print(df.head(lines))
    
    print("\nCalculation took {:.3f} seconds.".format(time.time() - start_time))
    print('-'*40)

def main():
    while True:
        city, month, day = get_filters()
        #df_full is returned for time_stats function month/day summaries
        df_full, df = load_data(city, month, day)
        
        while True:
            print('\nEnter number from below options:\
                    \n1 - Time Stats\
                    \n2 - Station Stats\
                    \n3 - Trip Duration Stats\
                    \n4 - User Stats\
                    \n5 - DataFrame Data\
                    \n6 - Exit (or restart)')
            menu_choice = input('Enter number: ')
            
            if menu_choice == '1':
                time_stats(df_full, city, month, day)
            elif menu_choice == '2':
                station_stats(df, city, month, day)
            elif menu_choice == '3':
                trip_duration_stats(df, city, month, day)
            elif menu_choice == '4':
                user_stats(df, city, month, day)
            elif menu_choice == '5':
                df_data(df, city, month, day)
            elif menu_choice == '6':
                break
            else:
                print('Invalid entry.\n')
                continue
        
        restart = input('\nWould you like to restart? Enter Y or N: ')
        if restart.lower() != 'y':
            break
    print('Exiting Program.\n')


if __name__ == "__main__":
	main()