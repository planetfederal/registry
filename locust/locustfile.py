from locust import HttpLocust, TaskSet, task
import random, json

def query_facets(l):
    contents = open('queries/query-facets.json', 'rb').read()
    l.client.post("/perftest2/_search", data=contents, name="query-facets")

def query_geo_big(l):
    contents = open('queries/query-geo-big.json', 'rb').read()
    l.client.post("/perftest2/_search", data=contents, name="query-geo-big")

def query_geo_bottom_left(l):
    contents = open('queries/query-geo-bottom-left.json', 'rb').read()
    l.client.post("/perftest2/_search", data=contents, name="query-geo-bottom-left")

def query_geo_center(l):
    contents = open('queries/query-geo-center.json', 'rb').read()
    l.client.post("/perftest2/_search", data=contents, name="query-geo-center")

def query_geo_top_right(l):
    contents = open('queries/query-geo-top-right.json', 'rb').read()
    l.client.post("/perftest2/_search", data=contents, name="query-geo-top-right")

def query_originator_boost(l):
    contents = open('queries/query-originator-boost.json', 'rb').read()
    l.client.post("/perftest2/_search", data=contents, name="query-originator-boost")

def query_qtext(l):
    contents = open('queries/query-qtext.json', 'rb').read()
    l.client.post("/perftest2/_search", data=contents, name="query-qtext")

def query_qtext_fields1(l):
    contents = open('queries/query-qtext-fields1.json', 'rb').read()
    l.client.post("/perftest2/_search", data=contents, name="query-qtext-fields1")

def query_qtext_fields2(l):
    contents = open('queries/query-qtext-fields2.json', 'rb').read()
    l.client.post("/perftest2/_search", data=contents, name="query-qtext-fields2")

def query_qtext_fields3(l):
    contents = open('queries/query-qtext-fields3.json', 'rb').read()
    l.client.post("/perftest2/_search", data=contents, name="query-qtext-fields3")

def query_time_gap_24(l):
    contents = open('queries/query-time-gap-24.json', 'rb').read()
    l.client.post("/perftest2/_search", data=contents, name="query-time-gap-24")

def query_time_gap1y(l):
    contents = open('queries/query-time-gap1y.json', 'rb').read()
    l.client.post("/perftest2/_search", data=contents, name="query-time-gap1y")

def query_time_range_2000(l):
    contents = open('queries/query-time-range-2000.json', 'rb').read()
    l.client.post("/perftest2/_search", data=contents, name="query-time-range-2000")

def query_time_range_from(l):
    contents = open('queries/query-time-range-from.json', 'rb').read()
    l.client.post("/perftest2/_search", data=contents, name="query-time-range-from")

def query_time_range_stars(l):
    contents = open('queries/query-time-range-stars.json', 'rb').read()
    l.client.post("/perftest2/_search", data=contents, name="query-time-range-stars")

def query_time_range_up_to(l):
    contents = open('queries/query-time-range-up-to.json', 'rb').read()
    l.client.post("/perftest2/_search", data=contents, name="query-time-range-up-to")

def query_title_boost(l):
    contents = open('queries/query-title-boost.json', 'rb').read()
    l.client.post("/perftest2/_search", data=contents, name="query-title-boost")

def query_user_filter(l):
    contents = open('queries/query-user-filter.json', 'rb').read()
    l.client.post("/perftest2/_search", data=contents, name="query-user-filter")

def query_uuid(l):
    contents = open('queries/query-uuid.json', 'rb').read()
    l.client.post("/perftest2/_search", data=contents, name="query-uuid")

def random_heatmap(l):
    minx = random.uniform(-180.0, 179.0)
    miny = random.uniform(-90.0, 89.0)
    maxx = random.uniform(minx, 180.0)
    maxy = random.uniform(miny, 90.0)
    max_cells = random.uniform(900, 1000)
    grid_level = random.uniform(2, 12)
    dist_err = random.uniform(0, 0.5)
    dist_err_pct = random.uniform(0, 0.5)

    query = {
        "query": {
            "match_all": {}
        },
        "aggs" : {
            "viewport" : {
                "heatmap" : {
                    "field" : "layer_geoshape",
                    "dist_err_pct" : dist_err_pct,
                    "max_cells" : max_cells,
                    "geom" : {
                        "geo_shape": {
                            "location": {
                                "shape": {
                                    "type": "envelope",
                                    "coordinates" : [[minx, miny], [maxx, maxy]]
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    #print(json.dumps(query))
    l.client.post("/perftest2/_search", data=json.dumps(query), name="query-random-heatmap")


class MyTaskSet(TaskSet):
    tasks = [
        query_facets,
        query_geo_big,
        query_geo_bottom_left,
        query_geo_center,
        query_geo_top_right,
        query_originator_boost,
        query_qtext_fields1,
        query_qtext_fields2,
        query_qtext_fields3,
        query_qtext,
        query_time_gap_24,
        query_time_gap1y,
        query_time_range_2000,
        query_time_range_from,
        query_time_range_stars,
        query_time_range_up_to,
        query_title_boost,
        query_user_filter,
        query_uuid,
        random_heatmap
    ]

class MyLocust(HttpLocust):
    task_set = MyTaskSet
    min_wait = 5000
    max_wait = 15000

