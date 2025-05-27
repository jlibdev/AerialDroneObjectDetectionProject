import {
  Dialog,
  DialogClose,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { useState, type Dispatch, type SetStateAction } from "react";
import { cn } from "../../lib/utils";
import { Button } from "@/components/ui/button";
import axios from "axios";
import { Label } from "@/components/ui/label";

export const LocalInference = ({
  isLoading,
  setIsLoading,
  children,
  videoFile,
}: {
  isLoading: boolean;
  setIsLoading: Dispatch<SetStateAction<boolean>>;
  children: React.ReactNode;
  videoFile: File | null;
}) => {
  const [videoUrl, setVideoUrl] = useState<string | null>(null);
  const apiBaseUrl = import.meta.env.VITE_API_BASE_URL;
  const handleInfer = async () => {
    if (!videoFile) return;

    const formData = new FormData();
    formData.append("video", videoFile);

    try {
      setIsLoading(true);
      const response = await axios.post(`${apiBaseUrl}/upload`, formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      setVideoUrl(response.data.videoUrl);
    } catch (err) {
      alert("Error uploading video");
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Dialog>
      <DialogTrigger asChild onClick={handleInfer}>
        {children}
      </DialogTrigger>
      <DialogContent
        className={cn(
          "min-w-[50vw] min-h-[75vh] flex flex-col flex-wrap",
          isLoading && "bg-accent"
        )}
      >
        <DialogHeader>
          <DialogTitle>Local Video Inference</DialogTitle>
          <DialogDescription>
            Inferencing on video using YOLOv8 Medium Model Trained On Militray
            Dataset....
            <Label className="flex items-center">
              <span className="font-bold">Desclaimer:</span>
              This project is conceptual and strictly educational. It is not
              intended for real-life military application without proper ethical
              evaluation and government oversight.
            </Label>
          </DialogDescription>
        </DialogHeader>
        {isLoading ? (
          <div className="flex items-center justify-center h-full w-full flex-grow">
            <div className="w-12 h-12 border-4 border-black border-t-transparent rounded-full animate-spin"></div>
          </div>
        ) : (
          <video
            className="h-full w-full flex-grow"
            src={`${apiBaseUrl}/video/` + videoUrl}
            controls
          ></video>
        )}
        <DialogFooter>
          <DialogClose>
            <Button
              type="button"
              className="p-5"
              onClick={() => setIsLoading(false)}
            >
              Done
            </Button>
          </DialogClose>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
};
