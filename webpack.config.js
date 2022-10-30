const path = require('path');
const webpack = require('webpack');
const BundleTracker = require('webpack-bundle-tracker');

module.exports = {
    context: __dirname,
    entry: './js/index',
    output: {
        path: path.resolve('./dist/'),
        filename: "[name]-[fullhash].js"
    },
    plugins: [
        new BundleTracker({filename: './webpack-stats.json'})
    ],
};