import React from "react";
import { render, screen, waitFor } from "@testing-library/react";
import "@testing-library/jest-dom";
import FileUpload from "./FileUpload";

const mockOnDrop = jest.fn();
jest.mock("react-dropzone", () => ({
  useDropzone: ({ onDrop }: { onDrop: (files: File[]) => void }) => {
    mockOnDrop.mockImplementation(onDrop);
    return {
      getRootProps: () => ({}),
      getInputProps: () => ({}),
      isDragActive: false,
      fileRejections: [],
    };
  },
}));

jest.mock("../const", () => ({
  BACKEND_URL: "http://localhost:8000",
}));

beforeEach(() => {
  global.fetch = jest.fn().mockResolvedValue({
    ok: true,
    json: async () => [{ filename: "audio.mp3", transcription: "Hello world" }],
  });
});

afterEach(() => jest.clearAllMocks());

describe("FileUpload", () => {
  test("shows success message after files are transcribed successfully", async () => {
    const onUploadSuccess = jest.fn();
    render(<FileUpload onUploadSuccess={onUploadSuccess} />);

    const file = new File(["audio content"], "audio.mp3", {
      type: "audio/mpeg",
    });
    await mockOnDrop([file]);

    await waitFor(() => {
      expect(
        screen.getByText(/1 file transcribed successfully/i),
      ).toBeInTheDocument();
    });

    expect(onUploadSuccess).toHaveBeenCalledTimes(1);
  });
});
