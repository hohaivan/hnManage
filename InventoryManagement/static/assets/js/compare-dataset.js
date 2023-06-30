// Helper function to compare two datasets
    function isDatasetsEqual(datasets1, datasets2) {
        if (datasets1 === null || datasets2 === null) {
            return false;
        }
        if (datasets1.length !== datasets2.length) {
            return false;
        }
        for (var i = 0; i < datasets1.length; i++) {
            if (!isDatasetEqual(datasets1[i], datasets2[i])) {
                return false;
            }
        }
        return true;
    }
     // Helper function to compare two individual datasets
    function isDatasetEqual(dataset1, dataset2) {
        if (dataset1.label !== dataset2.label) {
            return false;
        }
        if (dataset1.data.length !== dataset2.data.length) {
            return false;
        }
        for (var i = 0; i < dataset1.data.length; i++) {
            if (dataset1.data[i] !== dataset2.data[i]) {
                return false;
            }
        }
        return true;
    }