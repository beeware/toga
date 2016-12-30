var webpack = require('webpack');

module.exports = {
    entry: {
        "toga": "./toga/toga.js",
        "toga.min": "./toga/toga.js"
    },
    devtool: 'source-map',
    output: {
        path: __dirname,
        filename: "[name].js",
        library: 'toga',
        libraryTarget: 'umd'
    },
    target: 'web',
    plugins: [
        new webpack.optimize.UglifyJsPlugin({
            include: /\.min\.js$/,
            minimize: true
        })
    ],
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
                loader: "babel-loader",
                exclude: /node_modules/
            },
            {
                include: /\.json$/,
                loader: "json-loader"
            },
            {
                test: /\.(css|scss)$/,
                loaders: [ 'style', 'css', 'sass' ]
            }
        ]

    },
    // eslint: {
    //     configFile: './.eslintrc',
    //     failOnWarning: false,
    //     failOnError: true
    // }
}
