/**
 * Instantiate by dependency injection.
 *
 * function (PartyCrasher, $scope) { ... }
 */
angular.module('PartyCrasherApp')
.factory('PartyCrasher', function ($http) {

  class PartyCrasher {

    /**
     * Fetch a bucket by (project, threshold, id) tuple.
     *
     * Returns a Promise of data.
     */
    fetchBucket({project, threshold, id}) {
      if (!(project && threshold && id)) {
        return Promise.reject(`Must provide project, threshold, and id`);
      }

      return $http.get(bucketURL({project, threshold, id}))
        .then(({data}) => data);
    }
    
    /**
     * Fetch a bucket by (project, id) pair.
     *
     * Returns a Promise of the report.
     */
    fetchReport({project, id}) {
      if (!(project && id)) {
        return Promise.reject(`Must provide project and id`);
      }

      return $http.get(reportURL({ project, id }))
        .then(({data}) => data);
    }

    /**
     * Searches for buckets.
     */
    search() {
      /* TODO */
    }
  }

  function bucketURL({ project, threshold, id }) {
    return `/${project}/buckets/${threshold}/${id}`;
  }

  function reportURL({ project, id }) {
    /* Get rid of project prefix. */
    id = id.replace(/^[*\w]+:/, '');
    return `/${project}/reports/${id}`;
  }

  
  return new PartyCrasher();
});
