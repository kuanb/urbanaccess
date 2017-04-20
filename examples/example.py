import sys
import urbanaccess

def continue_check(clarify=False):
    message = '[yN] Continue?'
    if clarify:
        message = 'Not a valid option. Try again.\n' + message
    response = raw_input(message)
    if response in ['y', 'Y']:
        pass
    elif response in ['n', 'N']:
        print('Exiting...')
        sys.exit()
    else:
        clarify = True
        continue_check(clarify)


# let's find transit providers in Madison, WI
search_results = urbanaccess.gtfsfeeds.search(search_text='madison')
# 4 results will be returned, you can see them by printing the dataframe below
print('Results from searching for Madison on now-defunct GTFS Data Exchange')
print(search_results)

# add a feed to the gtfs to include in the analysis
feeds = urbanaccess.gtfsfeeds.feeds
name = 'madison'
url = 'http://www.cityofmadison.com/metro/gtfs/mmt_gtfs.zip'
new_feed =  {name:url}
feeds.add_feed(new_feed)

# download the feed, will be placed in folders within data/gtfsfeed_text
# according to the dict key name
urbanaccess.gtfsfeeds.download()

# now that we have saved the raw gtfs data, we need to load it in
gtfsfeed_path = 'data/gtfsfeed_text/'
validation = True
verbose = True
bbox = (-89.566399,42.984056,-89.229584,43.171917)
remove_stops_outsidebbox = True
append_definitions = True
urbanaccess.gtfs.load.gtfsfeed_to_df(gtfsfeed_path,
                                     validation,
                                     verbose,
                                     bbox,
                                     remove_stops_outsidebbox,
                                     append_definitions)
