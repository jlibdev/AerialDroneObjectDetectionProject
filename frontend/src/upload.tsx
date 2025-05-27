import React, { useState } from "react";

interface UploadResponse {
  filename: string;
  url: string;
}

export const UploadForm: React.FC<{ onUpload: (url: string) => void }> = ({
  onUpload,
}) => {
  const [uploading, setUploading] = useState(false);

  const handleUpload = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const form = e.currentTarget;
    const fileInput = form.file as HTMLInputElement;
    if (!fileInput.files || fileInput.files.length === 0) return;

    const formData = new FormData();
    formData.append("file", fileInput.files[0]);

    setUploading(true);
    try {
      const response = await fetch("http://localhost:8000/upload", {
        method: "POST",
        body: formData,
      });
      const data: UploadResponse = await response.json();
      onUpload(data.url);
    } catch (err) {
      alert("Upload failed");
      console.error(err);
    } finally {
      setUploading(false);
    }
  };

  return (
    <form onSubmit={handleUpload}>
      <input type="file" name="file" accept="video/*" required />
      <button type="submit" disabled={uploading}>
        {uploading ? "Uploading..." : "Upload Video"}
      </button>
    </form>
  );
};

export const VideoPlayer: React.FC<{ videoUrl: string }> = ({ videoUrl }) => {
  if (!videoUrl) return null;

  return (
    <div>
      <h3>Processed Video</h3>
      <video controls width="720" src={`http://localhost:8000${videoUrl}`} />
    </div>
  );
};
