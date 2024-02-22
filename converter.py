import argparse
import cv2
import imageio
import os

GIF_FPS = 10
RESIZE_SCALE = 0.18

# Converts input video into gif, and saves it to specified output folder.
# Should be able to support following video formats:
# Arguments: input_vid (str), output_file(str)
def video_to_gif(input_vid, output_dir, fps=10):

    # Open input_vid with cv2.
    vid_open = cv2.VideoCapture(input_vid)

    if not vid_open.isOpened():
        print("Error with opening video file.")
        return

    # Retrieve path and extension of file.
    path, ext = os.path.splitext(input_vid)
    vid_name = path[7:]
    out_name = os.path.join(output_dir, vid_name + ".gif")

    frames = []
    num_frames = 0
    while (vid_open.isOpened()):
        retval, frame = vid_open.read()
        if not retval:
            break
        num_frames += 1
        # if I mod by 10, gif doesn't loop continuously on mac finder for some reason
        if num_frames % 7 == 0:
            # Resize frame: want to make image frame smaller for gif.
            frame = cv2.resize(frame, (0,0), fx=RESIZE_SCALE, fy=RESIZE_SCALE)
            # Change color format to RGB.
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frames.append(frame)
    
    imageio.mimsave(out_name, frames, loop=0, fps=GIF_FPS)

    # # Writer object to create video files from a sequence of images.
    # For larger video files, probably better to use get_writer and have stream of frames.
    # writer = imageio.get_writer(out_name, fps=GIF_FPS, mode='I')

    return

if __name__ == "__main__":
    # ArgumentParser Object Creation:
    parser = argparse.ArgumentParser()

    # Arguments: input_video_path, output_gif_folder
    # Add Arguments: "-input" -> having hyphen means optional arg, no hyphen means positional arg.
    parser.add_argument("input", help="Video file path")
    parser.add_argument("output", help="Gif output file path")

    # Parse Arguments:
    args = parser.parse_args()

    # Call converter function with command line arguments:
    video_to_gif(args.input, args.output)
