import subprocess
import json
import streamlit as st
import tempfile
import os

# Predefined options for bitrate, pixel formats, framerates and scales
bitrate_options = (
    '36M', '42M', '45M', '60M', '63M', '75M', '80M', '84M', '90M', '100M', '110M', '115M', '120M', '145M', '175M', '180M', '185M', '220M', '240M', '290M', '350M', '365M', '390M', '440M', '730M', '880M'
)

pixel_formats = (
    'gbrp10', 'yuv422p', 'yuv422p10', 'yuv444p10'
)

# Predefined combinations of frame size, bitrate, and pixel format
ffmpeg_combinations = [
    {"Frame size": "1920x1080p", "Bitrate": "880Mbps", "Pixel format": "yuv444p10, gbrp10"},
    {"Frame size": "1920x1080p", "Bitrate": "730Mbps", "Pixel format": "yuv444p10, gbrp10"},
    {"Frame size": "1920x1080p", "Bitrate": "440Mbps", "Pixel format": "yuv444p10, gbrp10"},
    {"Frame size": "1920x1080p", "Bitrate": "390Mbps", "Pixel format": "yuv444p10, gbrp10"},
    {"Frame size": "1920x1080p", "Bitrate": "350Mbps", "Pixel format": "yuv444p10, gbrp10"},
    {"Frame size": "1920x1080p", "Bitrate": "440Mbps", "Pixel format": "yuv422p10"},
    {"Frame size": "1920x1080p", "Bitrate": "365Mbps", "Pixel format": "yuv422p10"},
    {"Frame size": "1920x1080p", "Bitrate": "185Mbps", "Pixel format": "yuv422p10"},
    {"Frame size": "1920x1080p", "Bitrate": "175Mbps", "Pixel format": "yuv422p10"},
    {"Frame size": "1920x1080p", "Bitrate": "440Mbps", "Pixel format": "yuv422p"},
    {"Frame size": "1920x1080p", "Bitrate": "365Mbps", "Pixel format": "yuv422p"},
    {"Frame size": "1920x1080p", "Bitrate": "290Mbps", "Pixel format": "yuv422p"},
    {"Frame size": "1920x1080p", "Bitrate": "240Mbps", "Pixel format": "yuv422p"},
    {"Frame size": "1920x1080p", "Bitrate": "220Mbps", "Pixel format": "yuv422p"},
    {"Frame size": "1920x1080p", "Bitrate": "185Mbps", "Pixel format": "yuv422p"},
    {"Frame size": "1920x1080p", "Bitrate": "175Mbps", "Pixel format": "yuv422p"},
    {"Frame size": "1920x1080p", "Bitrate": "145Mbps", "Pixel format": "yuv422p"},
    {"Frame size": "1920x1080p", "Bitrate": "120Mbps", "Pixel format": "yuv422p"},
    {"Frame size": "1920x1080p", "Bitrate": "115Mbps", "Pixel format": "yuv422p"},
    {"Frame size": "1920x1080p", "Bitrate": "90Mbps", "Pixel format": "yuv422p"},
    {"Frame size": "1920x1080p", "Bitrate": "75Mbps", "Pixel format": "yuv422p"},
    {"Frame size": "1920x1080p", "Bitrate": "45Mbps", "Pixel format": "yuv422p"},
    {"Frame size": "1920x1080p", "Bitrate": "36Mbps", "Pixel format": "yuv422p"},
    {"Frame size": "1920x1080i", "Bitrate": "220Mbps", "Pixel format": "yuv422p10"},
    {"Frame size": "1920x1080i", "Bitrate": "185Mbps", "Pixel format": "yuv422p10"},
    {"Frame size": "1920x1080i", "Bitrate": "220Mbps", "Pixel format": "yuv422p"},
    {"Frame size": "1920x1080i", "Bitrate": "185Mbps", "Pixel format": "yuv422p"},
    {"Frame size": "1920x1080i", "Bitrate": "145Mbps", "Pixel format": "yuv422p"},
    {"Frame size": "1920x1080i", "Bitrate": "120Mbps", "Pixel format": "yuv422p"},
    {"Frame size": "1440x1080p", "Bitrate": "110Mbps", "Pixel format": "yuv422p"},
    {"Frame size": "1440x1080p", "Bitrate": "100Mbps", "Pixel format": "yuv422p"},
    {"Frame size": "1440x1080p", "Bitrate": "84Mbps", "Pixel format": "yuv422p"},
    {"Frame size": "1440x1080p", "Bitrate": "63Mbps", "Pixel format": "yuv422p"},
    {"Frame size": "1440x1080i", "Bitrate": "145Mbps", "Pixel format": "yuv422p"},
    {"Frame size": "1440x1080i", "Bitrate": "120Mbps", "Pixel format": "yuv422p"},
    {"Frame size": "1440x1080i", "Bitrate": "110Mbps", "Pixel format": "yuv422p"},
    {"Frame size": "1440x1080i", "Bitrate": "100Mbps", "Pixel format": "yuv422p"},
    {"Frame size": "1440x1080i", "Bitrate": "90Mbps", "Pixel format": "yuv422p"},
    {"Frame size": "1440x1080i", "Bitrate": "80Mbps", "Pixel format": "yuv422p"},
    {"Frame size": "1280x720p", "Bitrate": "220Mbps", "Pixel format": "yuv422p10"},
    {"Frame size": "1280x720p", "Bitrate": "180Mbps", "Pixel format": "yuv422p10"},
    {"Frame size": "1280x720p", "Bitrate": "90Mbps", "Pixel format": "yuv422p10"},
    {"Frame size": "1280x720p", "Bitrate": "220Mbps", "Pixel format": "yuv422p"},
    {"Frame size": "1280x720p", "Bitrate": "180Mbps", "Pixel format": "yuv422p"},
    {"Frame size": "1280x720p", "Bitrate": "145Mbps", "Pixel format": "yuv422p"},
    {"Frame size": "1280x720p", "Bitrate": "120Mbps", "Pixel format": "yuv422p"},
    {"Frame size": "1280x720p", "Bitrate": "110Mbps", "Pixel format": "yuv422p"},
    {"Frame size": "1280x720p", "Bitrate": "90Mbps", "Pixel format": "yuv422p"},
    {"Frame size": "1280x720p", "Bitrate": "75Mbps", "Pixel format": "yuv422p"},
    {"Frame size": "1280x720p", "Bitrate": "60Mbps", "Pixel format": "yuv422p"},
    {"Frame size": "960x720p", "Bitrate": "115Mbps", "Pixel format": "yuv422p"},
    {"Frame size": "960x720p", "Bitrate": "75Mbps", "Pixel format": "yuv422p"},
    {"Frame size": "960x720p", "Bitrate": "60Mbps", "Pixel format": "yuv422p"},
    {"Frame size": "960x720p", "Bitrate": "42Mbps", "Pixel format": "yuv422p"},
]

framerates = (
    "24","25","30","50","60"
)

scales = ("1920x1080","1280x720")

def get_codecs(ffprobe_path, path):
    """
    Retrieves the video and audio codecs of a file using ffprobe.
    
    Args:
        ffprobe_path (str): Path to the ffprobe executable.
        path (str): Path to the input file.
    
    Returns:
        tuple: A tuple containing the video codec and audio codec.

    May throw error depending on the OS used and the shell=true argument in subprocess.run

    
    """
    command = [ffprobe_path, '-v', 'error', '-show_entries', 'stream=codec_name', '-of', 'json', path]
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    if result.returncode != 0:
        st.error(f"ffprobe failed with error: {result.stderr.decode('utf-8')}")
        return None, None
    
    probe_output = json.loads(result.stdout)
    streams = probe_output.get("streams", [])
    
    video_codec = streams[0].get('codec_name') if len(streams) > 0 else None
    audio_codec = streams[1].get('codec_name') if len(streams) > 1 else None
    
    return video_codec, audio_codec

def run_ffmpeg_command(ffmpeg_path, args):
    """
    Executes an ffmpeg command with the provided arguments.
    
    Args:
        ffmpeg_path (str): Path to the ffmpeg executable.
        args (list): List of arguments to pass to ffmpeg.
    
    Returns:
        tuple: A tuple containing the stdout and stderr from the ffmpeg process.
    """
    try:
        command = [ffmpeg_path] + args
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.stdout, result.stderr
    except Exception as e:
        return None, str(e)

def get_ffmpeg_path():
    """
    Prompts the user to input the path to the ffmpeg executable.
    
    Returns:
        str: The path to the ffmpeg executable.
    """
    return st.text_input("Enter the absolute ffmpeg path:", placeholder=r"C:\ffmpeg\bin\ffmpeg.exe")

def get_ffprobe_path():
    """
    Prompts the user to input the path to the ffprobe executable.
    
    Returns:
        str: The path to the ffprobe executable.
    """
    return st.text_input("Enter the absolute ffprobe path:", placeholder=r"C:\ffmpeg\bin\ffprobe.exe")

def get_file_path():
    """
    Allows the user to upload files and returns their paths and names.
    
    Returns:
        tuple: A tuple containing a list of file paths and a list of file names.
    """
    uploaded_files = st.file_uploader("File selection", accept_multiple_files=True, type=["flv", "mkv", "mp4", "avi", "mov", "mxf"])
    paths = []
    names = []
    
    if uploaded_files:
        for file in uploaded_files:
            temp_dir = tempfile.mkdtemp()
            path = os.path.join(temp_dir, file.name)
            paths.append(path)
            fixed_name = file.name.split(".")[0]
            names.append(fixed_name)
            with open(path, "wb") as f:
                f.write(file.getvalue())
        return paths, names
    else:
        return None, None

def get_options():
    """
    Retrieves user-selected options for bitrate, pixel format, framerate, scale and path output.
    
    Returns:
        tuple: A tuple containing the selected options
    """
    bitrate = st.selectbox("Select the bitrate:", bitrate_options)
    pixel_format = st.selectbox("Select the pixel format:", pixel_formats)
    framerate = st.selectbox("Select the output framerate:", framerates)
    scale = st.selectbox("Select the output scale:",scales)
    output_path = st.text_input("Type the absolute path to the output folder",placeholder=r"C:\Users\User\Videos")
    return bitrate, pixel_format, framerate, scale, output_path

def frontend():
    """
    Displays the frontend interface using Streamlit.
    """
    st.image("https://img.pikbest.com/element_our/20230301/bg/86e09351bab02.png!sw800",width=150)
    st.title("DNxHD Video Converter")
    st.divider()
    st.markdown("- Check the possible combinations for bitrate and pixel format based on your input video resolution.")
    st.markdown("- All input videos will be processed with the selected specifications.")
    st.markdown("- Ensure the output folder / files do not already exist to avoid conflicts.")
    st.markdown("- Ensure ffmpeg and ffprobe are installed and added to the path.")
    st.markdown("- Ensure you have at least 3 times the size of the files as free storage.")
    st.dataframe(ffmpeg_combinations, hide_index=True, width=750)
    st.divider()
    st.text("Enter the desired values:")

if __name__ == "__main__":
    # Display the frontend interface
    frontend()
    
    # Retrieve user inputs
    bitrate, pixel_format, framerate, scale, output_path = get_options()

    # By default, we assume the user has added ffmpeg and ffprobe to the OS path so the executable path shouldnt be retrieved

    # ffmpeg_path = get_ffmpeg_path()
    # ffprobe_path = get_ffprobe_path()

    ffmpeg_path = "ffmpeg"
    ffprobe_path = "ffprobe"

    paths, names = get_file_path()
    
    if ffmpeg_path and output_path and paths and names and ffprobe_path and st.button("Start"):

        # Create a directory for converted files if it doesn't exist
        converted_folder = os.path.join(output_path, "converted")
        if not os.path.exists(converted_folder):
            os.makedirs(converted_folder)
       
        # Generate lists for ffmpeg arguments and codecs
        list_args = []
        list_codecs = []
        
        for path, name in zip(paths, names):
            list_args.append(['-i', str(path), '-c:v', 'dnxhd', '-vf', f"fps={framerate},scale={scale},format={pixel_format}", "-b:v", bitrate, '-c:a', 'pcm_s16be', f"{converted_folder}/{name}.mov"])
            list_codecs.append(get_codecs(ffprobe_path, path))
        
        # Execute ffmpeg commands and display results
        for arg, codec in zip(list_args, list_codecs):
            if codec[1] == "pcm_s16be":
                arg[9] = "copy"
            stdout, stderr = run_ffmpeg_command(ffmpeg_path, arg)
            st.text("Input file codecs:")
            st.code(codec, language=None)
            st.text("Running ffmpeg with arguments:")
            st.code(arg, language=None)
            st.text("Terminal output:")
            st.code(stderr, language=None)