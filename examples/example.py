import sys
import urbanaccess

def continue_check(clarify=False):
    print('\n---------------')
    message = '[yN] Continue?'
    if clarify:
        message = 'Not a valid option. Try again.\n' + message
    response = raw_input(message)
    if response in ['y',
                                        'Y']:
        pass
    elif response in ['n',
                                        'N']:
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
bbox = (-89.566399, 42.984056, -89.229584, 43.171917)
remove_stops_outsidebbox = True
append_definitions = True
# updates these attributes: stops, routes, trips, stop_times, calendar,
#                           calendar_dates, stop_times_int, headways
loaded_feeds = urbanaccess.gtfs.load.gtfsfeed_to_df(gtfsfeed_path,
                                                    validation,
                                                    verbose,
                                                    bbox,
                                                    remove_stops_outsidebbox,
                                                    append_definitions)

# what remains an empty dataframe is stop_times_int, which we still
# need to generate before we can get to calculating headways
columns = ['route_id', 'direction_id', 'trip_id', 'service_id', 
           'unique_agency_id']
day = 'wednesday' # pick an arbitrary day of week
tripschedualselector = urbanaccess.gtfs.network.tripschedualselector
cal_selected_trips = tripschedualselector(
                                input_trips_df = loaded_feeds.trips[columns],
                                input_calendar_df = loaded_feeds.calendar,
                                day = day)

# approximate missing stop times via linear interpolation
interpolatestoptimes = urbanaccess.gtfs.network.interpolatestoptimes
intermediate_interpolation = interpolatestoptimes(
                                stop_times_df = loaded_feeds.stop_times,
                                calendar_selected_trips_df = cal_selected_trips,
                                day = day)

# now calculate the difference in top times in new column
timedifference = urbanaccess.gtfs.network.timedifference
stop_times_int = timedifference(stop_times_df = intermediate_interpolation)

# now we can update loaded_feeds with this new dataframe
loaded_feeds.stop_times_int = stop_times_int

# now we need to calculate the headways, given the downloaded gtfs
headway_timerange = ['07:00:00','10:00:00'] # approx a.m. peak
# the below function updates loaded_feeds, so that headways is populated
loaded_feeds = urbanaccess.gtfs.headways.headways(
                    loaded_feeds, headway_timerange)

# save the results from these initial processing steps locally
filename = 'temp_network_analyzed.h5'
urbanaccess.gtfs.network.save_processed_gtfs_data(loaded_feeds, 'data', filename)
# we can now reload from that save location if we want
loaded_feeds = urbanaccess.gtfs.network.load_processed_gtfs_data('data', filename)

# now we're ready to download OSM data, let's use same bbox from gtfs search
osm_nodes, osm_edges = urbanaccess.osm.load.ua_network_from_bbox(bbox = bbox)
