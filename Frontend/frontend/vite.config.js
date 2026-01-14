export default {
  server: {
    proxy: {
      "/predict": {
        target: "http://localhost:8000",
        changeOrigin: true,
      },
    },
  },
};

