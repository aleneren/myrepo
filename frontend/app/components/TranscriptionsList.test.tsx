import { render, screen } from "@testing-library/react";
import "@testing-library/jest-dom";
import TranscriptionsList from "./TranscriptionsList";

const mockTranscriptions = [
  {
    id: 1,
    filename: "interview.mp3",
    transcription: "Hello world this is a test",
    created_at: new Date().toISOString(),
  },
  {
    id: 2,
    filename: "meeting.wav",
    transcription: "This is the second transcription",
    created_at: new Date().toISOString(),
  },
];

describe("TranscriptionsList", () => {
  test("renders transcription cards when transcriptions are passed", () => {
    render(<TranscriptionsList transcriptions={mockTranscriptions} />);

    // count label
    expect(screen.getByText("2 transcriptions")).toBeInTheDocument();

    // filenames
    expect(screen.getByText(/interview.mp3/i)).toBeInTheDocument();
    expect(screen.getByText(/meeting.wav/i)).toBeInTheDocument();

    // transcription text
    expect(screen.getByText("Hello world this is a test")).toBeInTheDocument();
    expect(
      screen.getByText("This is the second transcription"),
    ).toBeInTheDocument();

    // empty state should NOT appear
    expect(screen.queryByText("No transcriptions yet")).not.toBeInTheDocument();
  });
});
