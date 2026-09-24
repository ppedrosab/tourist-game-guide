// AsyncStorage no existe en jest: se usa el mock oficial en todos los tests.
jest.mock("@react-native-async-storage/async-storage", () =>
  require("@react-native-async-storage/async-storage/jest/async-storage-mock"),
);
