/**
 * Instantiate by dependency injection.
 *
 * function (PartyCrasher, $scope) { ... }
 */
angular.module('PartyCrasherApp')
.factory('PartyCrasher', function ($http) {

  class PartyCrasher {

    /**
     * Fetch a bucket by (project, threshold, id) pair.
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
     * Searches for buckets.
     */
    search() {
      /* TODO */
    }
  }

  function bucketURL({ project, threshold, id }) {
    return `/${project}/buckets/${threshold}/${id}`;
  }

  
  return new PartyCrasher();
});
