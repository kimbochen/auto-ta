const { createProxyMiddleware } = require('http-proxy-middleware');

module.exports = function(app) {
  app.use(
    ['/'],
    createProxyMiddleware({
      target: `http://${process.env.SERVER_IP}:${process.env.SERVER_PORT}`,
      changeOrigin: true,
    })
  );
};
