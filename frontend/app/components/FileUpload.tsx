import React, { useCallback, useState } from "react";
import { useDropzone } from "react-dropzone";
import { BACKEND_URL, MAX_FILES, MAX_FILE_SIZE_MB } from "../const";
import "./FileUpload.css";

const SUPPORTED_FORMATS = {
  "audio/mpeg": [".mp3", ".mpeg", ".mpga"],
  "audio/mp4": [".mp4", ".m4a"],
  "audio/wav": [".wav"],
  "audio/webm": [".webm"],
};

interface FileUploadProps {
  onUploadSuccess: () => void;
}

interface UploadResult {
  filename: string;
  transcription?: string;
  error?: string;
}

const ProcessingView: React.FC<{ files: File[] }> = ({ files }) => (
  <div className="upload-status">
    <div className="spinner" />
    <p>Transcribing your files… please wait</p>
    <ul className="processing-file-list">
      {files.map((f, i) => (
        <li key={f.name}>
          <span className="file-index">{i + 1}.</span>
          <span className="file-name">{f.name}</span>
          <span className="file-size">
            {(f.size / 1024 / 1024).toFixed(1)} MB
          </span>
        </li>
      ))}
    </ul>
  </div>
);

const IdleView: React.FC = () => (
  <>
    <span className="upload-icon">🎤</span>
    <h3>Drop your audio files here</h3>
    <p>
      or <span className="browse-text">click to browse</span>
    </p>
    <p className="supported-formats">
      MP3, MP4, MPEG, MPGA, M4A, WAV, WEBM <br />
      Max {MAX_FILES} files with a max size of {MAX_FILE_SIZE_MB} MB each
    </p>
  </>
);

interface ErrorBlockProps {
  title: string;
  items: { key: string; label: string; detail?: string }[];
}

const ErrorBlock: React.FC<ErrorBlockProps> = ({ title, items }) => (
  <div className="upload-error">
    <h5>{title}</h5>
    <ul>
      {items.map(({ key, label, detail }) => (
        <li key={key}>
          <strong>{label}</strong>
          {detail && <p>{detail}</p>}
        </li>
      ))}
    </ul>
  </div>
);

const FileUpload: React.FC<FileUploadProps> = ({ onUploadSuccess }) => {
  const [isProcessing, setIsProcessing] = useState(false);
  const [processingFiles, setProcessingFiles] = useState<File[]>([]);
  const [uploadError, setUploadError] = useState<string | null>(null);
  const [completedCount, setCompletedCount] = useState<number>(0);
  const [failedResults, setFailedResults] = useState<UploadResult[]>([]);

  const processFiles = async (files: File[]) => {
    setIsProcessing(true);
    setProcessingFiles(files);
    setUploadError(null);
    setCompletedCount(0);
    setFailedResults([]);

    try {
      const formData = new FormData();
      files.forEach((f) => formData.append("file", f));

      const response = await fetch(`${BACKEND_URL}/transcribe`, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || "Upload failed");
      }

      const results: UploadResult[] = await response.json();
      setCompletedCount(results.filter((r) => r.transcription).length);
      setFailedResults(results.filter((r) => r.error));
      onUploadSuccess();
    } catch (err: any) {
      setUploadError(err.message);
    } finally {
      setIsProcessing(false);
    }
  };

  const onDrop = useCallback(
    (acceptedFiles: File[]) => {
      setCompletedCount(0);
      setFailedResults([]);
      if (acceptedFiles.length) processFiles(acceptedFiles.slice(0, MAX_FILES));
    },
    [onUploadSuccess],
  );

  const { getRootProps, getInputProps, isDragActive, fileRejections } =
    useDropzone({
      onDrop,
      accept: SUPPORTED_FORMATS,
      maxFiles: MAX_FILES,
      maxSize: MAX_FILE_SIZE_MB * 1024 * 1024,
      disabled: isProcessing,
    });

  return (
    <div className="file-upload">
      <div
        {...getRootProps()}
        className={`dropzone ${isDragActive ? "drag-active" : ""} ${isProcessing ? "processing" : ""}`}
      >
        <input {...getInputProps()} />
        <div className="dropzone-content">
          {isProcessing ? (
            <ProcessingView files={processingFiles} />
          ) : (
            <IdleView />
          )}
        </div>
      </div>

      {completedCount > 0 && !isProcessing && (
        <p className="upload-success">
          ✅ {completedCount} file{completedCount !== 1 ? "s" : ""} transcribed
          successfully
        </p>
      )}

      {failedResults.length > 0 && (
        <ErrorBlock
          title={`⚠️ ${failedResults.length} file${failedResults.length !== 1 ? "s" : ""} failed:`}
          items={failedResults.map((r) => ({
            key: r.filename,
            label: r.filename,
            detail: r.error,
          }))}
        />
      )}

      {uploadError && (
        <ErrorBlock
          title="Upload failed"
          items={[{ key: "error", label: uploadError }]}
        />
      )}

      {fileRejections.length > 0 && (
        <ErrorBlock
          title="⚠️ Some files were rejected:"
          items={fileRejections.map(({ file, errors }) => ({
            key: file.name,
            label: file.name,
            detail: errors.map((e) => e.message).join(", "),
          }))}
        />
      )}
    </div>
  );
};

export default FileUpload;
