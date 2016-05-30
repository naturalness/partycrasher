/**
 * Instantiate by dependency injection.
 *
 * function (PartyCrasher, $scope) { ... }
 */
angular.module('PartyCrasherApp')
.factory('PartyCrasher', function ($http, $httpParamSerializer) {
  class PartyCrasher {

    /**
     * Fetch a bucket by (project, threshold, id) tuple.
     *
     * Returns a Promise of data.
     */
    fetchBucket({project, threshold, id}) {
      if (!(project && threshold && id)) {
        return Promise.reject(new Error('Must provide project, threshold, and id'));
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
        return Promise.reject(new Error('Must provide project and id'));
      }

      return $http.get(reportURL({ project, id }))
        .then(({data}) => data);
    }

    /**
     * Searches for buckets.
     */
    search({ project, threshold, since }) {
      return $http.get(searchUrl({ project, threshold, since }))
        .then(({data}) => data);
    }
  }

  function bucketURL({ project, threshold, id }) {
    return `/${project}/buckets/${threshold}/${id}`;
  }

  function reportURL({ project, id }) {
    /* Get rid of project prefix. */
    return `/${project}/reports/${id}`;
  }

  function searchUrl({project, threshold, since}) {
    var query = $httpParamSerializer({ since: since || '3-days-ago' });

    if (!project || project === '*') {
      /* Search ALL projects. */
      return `/buckets/${threshold}?${query}`;
    } else {
      /* Search just this project. */
      return `/${project}/buckets/${threshold}?${query}`;
    }
  }

  return new PartyCrasher();
});
