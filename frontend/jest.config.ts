import type { Config } from "jest";

const config: Config = {
  preset: "ts-jest",
  testEnvironment: "jsdom",
  setupFilesAfterEnv: ["@testing-library/jest-dom"],
  moduleNameMapper: {
    "\\.(css|less)$": "<rootDir>/__mocks__/fileMock.ts",
    "import.meta.env": "<rootDir>/__mocks__/envMock.ts",
  },
  transform: {
    "^.+\\.tsx?$": [
      "ts-jest",
      {
        tsconfig: {
          verbatimModuleSyntax: false,
          module: "esnext",
          moduleResolution: "bundler",
        },
        diagnostics: false,
      },
    ],
  },
};

export default config;
