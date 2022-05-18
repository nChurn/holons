// vue.config.js

// if (process.env.NODE_ENV === 'production') {


const pages = {
    'app': {
        entry: './src/main.js',
        chunks: ['chunk-vendors']
    },
}


  module.exports = {
    pages: pages,
    filenameHashing: false,
    productionSourceMap: false,
    outputDir: '../static/build/app/',
    lintOnSave: true
  }
// }


// const BundleTracker = require("webpack-bundle-tracker");
// 
// module.exports = {
//     publicPath: "http://0.0.0.0:8080/",
//     // outputDir: './dist/',
//     filenameHashing: false,
//     productionSourceMap: false,
//     outputDir: '../static/build/app/',
// 
//     chainWebpack: config => {
// 
//         config.optimization
//             .splitChunks(false)
// 
//         config
//             .plugin('BundleTracker')
//             .use(BundleTracker, [{filename: '../frontend/webpack-stats.json'}])
// 
//         config.resolve.alias
//             .set('__STATIC__', 'static')
// 
//         config.devServer
//             .public('http://0.0.0.0:8080')
//             .host('0.0.0.0')
//             .port(8080)
//             // .hotOnly(true)
//             // .watchOptions({poll: 1000})
//             .https(false)
//             .headers({"Access-Control-Allow-Origin": ["\*"]})
//             }
//         };
