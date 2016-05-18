module.exports = {
    "env": {
        "browser": true,
        "es6": true
    },
    "extends": "eslint:recommended",
    "rules": {
        "indent": [
            "error",
            2
        ],
        "linebreak-style": [
            "error",
            "unix"
        ],
        "quotes": [
            "error",
            "single",
             {
                 "avoidEscape": true,
                 "allowTemplateLiterals": true
             }
        ],
        "semi": [
            "error",
            "always"
        ]
    },
    "globals": {
        // Disallow assignment to angular.
        "angular": false,
        "moment": false
    }
};
