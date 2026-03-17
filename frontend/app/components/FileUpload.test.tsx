import { act } from "react";
import { render, screen } from "@testing-library/react";
import "@testing-library/jest-dom";
import FileUpload from "./FileUpload";

// This will store the onDrop callback internally
let mockOnDrop: (files: File[]) => void;

jest.mock("react-dropzone", () => ({
  useDropzone: (props: { onDrop: (files: File[]) => void }) => {
    // Capture the onDrop callback
    mockOnDrop = props.onDrop;
    return {
      getRootProps: () => ({ "data-testid": "dropzone" }),
      getInputProps: () => ({ "data-testid": "input" }),
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

    // Create a fake file
    const file = new File(["audio content"], "audio.mp3", {
      type: "audio/mpeg",
    });

    await act(async () => {
      await mockOnDrop([file]);
    });

    // Wait for the success message (React async state updates)
    expect(
      await screen.findByText(/1 file transcribed successfully/i),
    ).toBeInTheDocument();

    // Ensure the callback was called
    expect(onUploadSuccess).toHaveBeenCalledTimes(1);
  });
});
