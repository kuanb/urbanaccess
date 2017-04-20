import sys
import urbanaccess

def continue_check(clarify=False):
    print('\n---------------')
    message = '[yN] Continue?'
    if clarify:
        message = 'Not a valid option. Try again.\n' + message
    response = raw_input(message)
    if response in ['yY']:
        pass
    elif response in ['nN']:
        print('Exiting...')
        sys.exit()
    else:
        clarify = True
        continue_check(clarify)


# let's find transit providers in Madison, WI
search_results = urbanaccess.gtfsfeeds.search(search_text='madison')
# 4 results will be returned, you can see them by printing the dataframe below
print('Results from searching for Madison on now-defunct GTFS Data Exchange')
print(search_results.head(5))
continue_check()

# add a feed to the gtfs to include in the analysis
feeds = urbanaccess.gtfsfeeds.feeds
name = 'madison'
# Note: query suggests: http://www.cityofmadison.com/metro/gtfs/mmt_gtfs.zip
#       but this address is currently is 404'ing (04-16-2017)
#       ...as a result, using link below which _does_ work in the meantime
url = 'http://www.gtfs-data-exchange.com/agency/city-of-madison/latest.zip'
new_feed =  {name:url}
feeds.add_feed(new_feed)

# download the feed, will be placed in folders within data/gtfsfeed_text
# according to the dict key name
urbanaccess.gtfsfeeds.download()

# now that we have saved the raw gtfs data, we need to load it in
gtfsfeed_path = None # use default gtfs save location
validation = True
verbose = True
bbox = (-89.566399,42.984056,-89.229584,43.171917)
remove_stops_outsidebbox = True
append_definitions = True
loaded_feeds = urbanaccess.gtfs.load.gtfsfeed_to_df(gtfsfeed_path,
                                                    validation,
                                                    verbose,
                                                    bbox,
                                                    remove_stops_outsidebbox,
                                                    append_definitions)

print('gtfsfeed_to_df returns processed df of corresponding GTFS feed text files')
print('Loaded feeds sample of stops:')
print(loaded_feeds.stops.head())
print('Loaded feeds sample of routes:')
print(loaded_feeds.routes.head())
print('Loaded feeds sample of trips:')
print(loaded_feeds.trips.head())
print('Loaded feeds sample of stop_times:')
print(loaded_feeds.stop_times.head())
print('Loaded feeds sample of calendar:')
print(loaded_feeds.calendar.head())
print('Loaded feeds sample of calendar_dates:')
print(loaded_feeds.calendar_dates.head())
print('Loaded feeds sample of stop_times_int:')
print(loaded_feeds.stop_times_int.head())
print('Loaded feeds sample of headways:')
print(loaded_feeds.headways.head())

# now we need to calculate the headways, given the downloaded gtfs
headway_timerange =  ['07:00:00','10:00:00'] # approx a.m. peak
urbanaccess.gtfs.headways.headways(loaded_feeds, headway_timerange)
