module.exports = {
    "env": {
        "browser": true,
        "es6": true
    },
    "extends": "eslint:recommended",
    "rules": {
        "indent": [
            "error",
            2,
            {
                "SwitchCase": 1
            }
        ],
        "linebreak-style": [
            "error",
            "unix"
        ],
        "quotes": [
            "off"
        ],
        "no-unused-vars": [
            "error",
            {
                "argsIgnorePattern": '^_'
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
        "moment": false,
        "_": false
    }
};
