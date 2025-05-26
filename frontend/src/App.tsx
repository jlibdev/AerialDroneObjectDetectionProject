import React, { useState } from "react";

const App = () => {
  const [videoUrl, setVideoUrl] = useState<string | null>(null);
  const [uploading, setUploading] = useState(false);

  const handleUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    const formData = new FormData();
    formData.append("video", file);

    setUploading(true);

    try {
      const response = await fetch("http://localhost:8000/upload", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("Upload failed");
      }

      const data = await response.json();
      setVideoUrl("http://localhost:8000" + data.videoUrl);
    } catch (err) {
      alert("Error uploading video");
      console.error(err);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 p-8 flex flex-col items-center">
      <h1 className="text-3xl font-bold mb-6">Upload & Play Video</h1>

      <input
        type="file"
        accept="video/*"
        onChange={handleUpload}
        className="mb-4"
      />

      {uploading && <p className="text-blue-500">Uploading...</p>}

      {videoUrl && (
        <div className="mt-6">
          <video
            src={videoUrl}
            controls
            width="640"
            className="rounded-xl shadow-lg"
          />
          <div className="mt-4">
            <a
              href={videoUrl}
              download
              className="text-white bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded-lg"
            >
              Download Video
            </a>
          </div>
        </div>
      )}
    </div>
  );
};

export default App;
