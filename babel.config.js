module.exports = function (api) {
  api.cache(true);
  return {
    // zustand/middleware (ESM) usa import.meta, que el bundle de Metro no admite sin transformar.
    presets: [["babel-preset-expo", { unstable_transformImportMeta: true }]],
  };
};
