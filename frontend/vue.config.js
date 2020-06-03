const path = require('path');

module.exports = {
    outputDir: path.resolve(__dirname, '../backend/dist'),
    assetsDir: './static',
    devServer: {
        proxy: {
            '/analyse_word': {
                target: 'http://localhost:5000',
                ws: false,
                changeOrigin: true
            }
        }
    }
};
