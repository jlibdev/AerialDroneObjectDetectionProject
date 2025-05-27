import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useState, type ChangeEvent } from "react";
import { LocalInference } from "../dialogs/InferenceDialogs";

const VideoStreamHandler = () => {
  const [ytURL, setytURL] = useState<string | null>(null);
  const [videoFile, setVideoFile] = useState<File | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);

  const handleFileChange = (e: ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    setVideoFile(file);
  };

  return (
    <div className="flex flex-col w-full h-full justify-center items-center gap-2">
      <h1 className="text-black text-2xl font-extralight">
        Aerial Threat Detection
      </h1>
      <div className="flex flex-col ring-1 rounded-2xl border-2 p-5 gap-5 min-w-[25vw]">
        <section className="flex gap-2 flex-col">
          <Label htmlFor="yturl">Youtube Inference</Label>
          <section className="flex gap-2">
            <Input
              disabled
              type="url"
              placeholder="Enter Youtube URL"
              name="yturl"
            ></Input>
            <Button disabled>Infer Video</Button>
          </section>
        </section>

        <section className="flex flex-col gap-2">
          <Label htmlFor="fileup">Local File</Label>
          <section className="flex gap-2">
            <Input
              type="file"
              name="fileup"
              accept="video/*"
              onChange={handleFileChange}
            ></Input>
            <LocalInference
              isLoading={isLoading}
              setIsLoading={setIsLoading}
              videoFile={videoFile}
            >
              <Button disabled={isLoading || videoFile == null}>
                Infer Video
              </Button>
            </LocalInference>
          </section>
        </section>
        <Button disabled>Switch to Stream</Button>
      </div>
    </div>
  );
};

export default VideoStreamHandler;
