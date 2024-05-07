# We use open sourced MaxMind's GeoLite database to obtain geo location information of IPs collected.
import geoip2.database
import json
import csv
from tqdm import tqdm


############ step 1: load database; setup global variables#############

########################################################
# please preprocess to load ips as a list here
ip_list = []
# please write output csv file path here:
output_file = f'output.csv'
#######################################################
cityreader = geoip2.database.Reader('GeoLite2-City.mmdb')
asnreader = geoip2.database.Reader('GeoLite2-ASN.mmdb')

g = open(output_file,'w')
writer = csv.writer(g)

header = True
city_miss = 0
asn_miss = 0
row_count = 0

############## step 2: use two readers to obtain needed info###########
for ip in tqdm(ip_list):
    row_count += 1
    if header:
        writer.writerow(['index','ip', 'MM_City', 'MM_Country', 'MM_Latitude','MM_longitude','MM_ASN', 'MM_ASN_ORG'])
        header = False
        continue

    # Add '.1' for the final octet of every IP address
    ip_addr = '.'.join(ip.split('.')[:-1] + ['1'])
    city = ''
    country = ''
    lat = ''
    lon = ''
    asn = ''
    asn_org = ''
    try:
        city_resp = cityreader.city(ip_addr)
        try:
            city = city_resp.city.names['en']
        except:
            pass
        try:
            country = city_resp.country.names['en']
        except:
            pass
        try:
            lat = city_resp.location.latitude
            lon = city_resp.location.longitude
        except:
            pass
    except:
        city_miss += 1
        
        pass

    try:
        asn_resp = asnreader.asn(ip_addr)
        try:
            asn = asn_resp.autonomous_system_number
        except:
            pass
        try:
            asn_org = asn_resp.autonomous_system_organization
        except:
            pass
    except:
        asn_miss += 1
        pass
    writer.writerow([row_count, ip_addr, city, country, lat, lon, asn, asn_org])
g.close()
print('City miss %d' % city_miss)
print('ASN miss %d' % asn_miss)