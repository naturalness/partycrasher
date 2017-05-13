################################################################################
# REST API endpoints                                                           #
################################################################################
class HTTP:
    path = '/'

################################################################################
# Bucketing                                                                    #
################################################################################
#thresholds = [int(10**(t/24.0)*10)/10.0 for t in range(0, 24*2+1)]
thresholds = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0]
class Bucketing:
    # A list of selectable buckets thresholds. For every report uploaded,
    # PartyCrasher will provide bucket assignments for each threshold provided
    # in this list. The range is between 1.0 and 10.0:
    #
    #  - 1.0 means that all reports should be placed in one bucket;
    #  - 10.0 means that all reports should be in a bucket of their own.
    #
    # Empirically, values between 3.5 and 4.5 seem to be the most useful.
    # <https://peerj.com/preprints/1705/>
    thresholds = thresholds
    # The default threshold when simply querying for a report's bucket assignment.
    # Using [index_method=CamelCase], [index_stackframe=true], and
    # [index_context=true], 4.0 was empirically determined to be the most
    # reasonable default.
    # <https://peerj.com/preprints/1705/>
    default_threshold = 3.8


    # The only option available is MLTCamelCase.
    tokenization = "partycrasher.bucketer.MLTCamelCase"

    # Configuration options for MLTCamelCase
    class MLT:
        max_query_terms = 20
        terminate_after = None
        min_score = min(thresholds)
        remove_fields = []
        keep_fields = [r'stacktrace.function']
        rescore_remove_fields = []
        rescore_keep_fields = None
        rescore_window_size = 500
        rescore_weight = 1.0
        search_weight = 1.0

################################################################################
# ElasticSearch                                                                #
################################################################################
class ElasticSearch:
    hosts = "localhost:9200"
    allow_delete_all = False
    indexbase = "crashes"
    # This is passed directly to ElasticSearch on index creation,
    # see https://www.elastic.co/guide/en/elasticsearch/reference/5.1/indices-create-index.html
    number_of_shards = 1 
    number_of_replicas = 0

    # This is passed directly to ElasticSearch on index creation
    # https://www.elastic.co/guide/en/elasticsearch/reference/current/index-modules-translog.html
    translog_durability = "async"
    throttle_type = "none"

    # Sets the similarity type for ElasticSeach, will affect bucket performance
    # Should be set to classic by default
    similarity = "classic"
    # Options for BM25 similarity, ignored if similarity is not 'BM25'
    # https://www.elastic.co/guide/en/elasticsearch/reference/5.x/index-modules-similarity.html#index-modules-similarity
    similarity_k1 = 1.2 
    similarity_b = 0.75
    