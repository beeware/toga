var path = require('path');
var webpack = require('webpack');
// var ExtractTextPlugin = require("extract-text-webpack-plugin");

module.exports = {
    entry: {
        "toga": "./toga/toga.js",
        "toga.min": "./toga/toga.js"
    },
    output: {
        path: path.join(__dirname, './dist'),
        filename: "[name].js",
        library: 'toga',
        libraryTarget: 'umd'
    },
    target: 'web',
    plugins: [
        new webpack.optimize.UglifyJsPlugin({
            include: /\.min\.js$/,
            minimize: true
        }),
        // new ExtractTextPlugin("[name].css"),
        new webpack.HotModuleReplacementPlugin(),
        new webpack.NoErrorsPlugin()
    ],
    devtool: 'source-map',
    module: {
        // preLoaders: [
        //     {
        //         test: /\.js$/,
        //         loader: 'eslint',
        //         exclude: /node_modules/,
        //     }
        // ],
        loaders: [
            {
                test: /\.js$/,
                loader: "babel",
                exclude: /node_modules/
            },
            {
                include: /\.json$/,
                loader: "json"
            },
            {
                test: /\.css$/,
                // loader: ExtractTextPlugin.extract('style', 'css', 'resolve-url')
                loaders: ['style', 'css']
            },
            {
                test: /\.s?css$/,
                // loader: ExtractTextPlugin.extract('style', 'css', 'sass', 'resolve-url')
                loaders: ['style', 'css', 'sass']
            },
            {
                test: /\.woff(2)?(\?v=[0-9]\.[0-9]\.[0-9])?$/,
                loader: 'url?limit=10000&mimetype=application/font-woff'
            },
            {
                test: /\.(ttf|eot|svg)(\?v=[0-9]\.[0-9]\.[0-9])?$/,
                loader: 'file'
            }
        ]

    }
    // eslint: {
    //     configFile: './.eslintrc',
    //     failOnWarning: false,
    //     failOnError: true
    // }
}
