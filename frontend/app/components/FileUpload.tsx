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

const FileUpload: React.FC<FileUploadProps> = ({ onUploadSuccess }) => {
  const [isProcessing, setIsProcessing] = useState(false);
  const [processingFiles, setProcessingFiles] = useState<File[]>([]);
  const [uploadError, setUploadError] = useState<string | null>(null);
  const [completedCount, setCompletedCount] = useState<number | null>(null);

  const processFiles = async (files: File[]) => {
    setIsProcessing(true);
    setProcessingFiles(files);
    setUploadError(null);
    setCompletedCount(null);

    try {
      // Batch upload files to backend
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
      const succeeded = results.filter((r) => r.transcription).length;

      setCompletedCount(succeeded);
      onUploadSuccess();
    } catch (err: any) {
      setUploadError(err.message);
    } finally {
      setIsProcessing(false);
    }
  };

  const onDrop = useCallback(
    (acceptedFiles: File[]) => {
      setCompletedCount(null);
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
            <div className="upload-status">
              <div className="spinner" />
              <p>Transcribing your files… please wait</p>
              <ul className="processing-file-list">
                {processingFiles.map((f, i) => (
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
          ) : (
            <>
              <span className="upload-icon">🎤</span>
              <h3>Drop your audio files here</h3>
              <p>
                or <span className="browse-text">click to browse</span>
              </p>
              <p className="supported-formats">
                MP3, MP4, MPEG, MPGA, M4A, WAV, WEBM <br /> Max {MAX_FILES}{" "}
                files with a max size of {MAX_FILE_SIZE_MB} MB each
              </p>
            </>
          )}
        </div>
      </div>

      {completedCount !== null && !isProcessing && (
        <p className="upload-success">
          ✅ {completedCount} file{completedCount !== 1 ? "s" : ""} transcribed
          successfully
        </p>
      )}

      {uploadError && (
        <div className="upload-error">
          <h5>Upload failed</h5>
          <p>{uploadError}</p>
        </div>
      )}

      {fileRejections.length > 0 && (
        <div className="upload-error">
          <h5>⚠️ Some files were rejected:</h5>
          {fileRejections.map(({ file, errors }) => (
            <div key={file.name}>
              <p>
                <strong>{file.name}</strong>
              </p>
              <ul>
                {errors.map((e) => (
                  <li key={e.code}>{e.message}</li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default FileUpload;
