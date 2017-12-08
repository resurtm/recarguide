const path = require('path');
const webpack = require('webpack');
const ExtractTextPlugin = require('extract-text-webpack-plugin');

const config = {
  entry: path.join(__dirname, 'js', 'index.js'),
  output: {
    path: path.join(__dirname, 'dist'),
    filename: 'index.js'
  },
  devtool: 'eval-source-map',
  module: {
    rules: [
      {
        test: /\.(png|svg|gif|jpg|jpeg|woff|woff2|eot|ttf)$/,
        use: {loader: 'url-loader?limit=4000'}
      },
      {
        test: /\.(scss|css)$/,
        use: ExtractTextPlugin.extract({
          use: [
            /*{loader: 'style-loader'},*/
            {loader: 'css-loader'},
            {
              loader: 'postcss-loader',
              options: {
                plugins: function () {
                  return [require('precss'), require('autoprefixer')];
                }
              }
            },
            {loader: 'sass-loader'}
          ]
        })
      }
    ]
  },
  plugins: [
    new ExtractTextPlugin('index.css'),
    new webpack.ProvidePlugin({
      $: 'jquery',
      jQuery: 'jquery',
      'window.jQuery': 'jquery',
      Popper: ['popper.js', 'default'],
      Alert: 'exports-loader?Alert!bootstrap/js/dist/alert',
      Button: 'exports-loader?Button!bootstrap/js/dist/button',
      Carousel: 'exports-loader?Carousel!bootstrap/js/dist/carousel',
      Collapse: 'exports-loader?Collapse!bootstrap/js/dist/collapse',
      Dropdown: 'exports-loader?Dropdown!bootstrap/js/dist/dropdown',
      Modal: 'exports-loader?Modal!bootstrap/js/dist/modal',
      Popover: 'exports-loader?Popover!bootstrap/js/dist/popover',
      Scrollspy: 'exports-loader?Scrollspy!bootstrap/js/dist/scrollspy',
      Tab: 'exports-loader?Tab!bootstrap/js/dist/tab',
      Tooltip: "exports-loader?Tooltip!bootstrap/js/dist/tooltip",
      Util: 'exports-loader?Util!bootstrap/js/dist/util'
    })
  ]
};

module.exports = config;
