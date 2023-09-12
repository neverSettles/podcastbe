# sections = ['kukufm/kukufm_hindi_finding_zen/section'+ str(i) + '.mp3' for i in range(53)]

# from pydub import AudioSegment

# def combine_mp3s(file_list, output_file):
#     # Initialize an empty audio segment
#     combined_audio = AudioSegment.empty()

#     # Loop through each file and append to combined_audio
#     for file in file_list:
#         audio = AudioSegment.from_mp3(file)
#         combined_audio += audio

#     # Export the combined audio to an output file
#     combined_audio.export(output_file, format="mp3")

# # Usage:
# # file_list = ["song1.mp3", "song2.mp3", "song3.mp3"]
# output_file = "kukufm/combined.mp3"
# combine_mp3s(sections, output_file)

sections = ['kukufm/kukufm_tamil/section'+ str(i) + '.mp3' for i in range(35)]

from pydub import AudioSegment

def combine_mp3s(file_list, output_file):
    # Initialize an empty audio segment
    combined_audio = AudioSegment.empty()

    # Loop through each file and append to combined_audio
    for file in file_list:
        audio = AudioSegment.from_mp3(file)
        combined_audio += audio

    # Export the combined audio to an output file
    combined_audio.export(output_file, format="mp3")

# Usage:
# file_list = ["song1.mp3", "song2.mp3", "song3.mp3"]
output_file = "kukufm/combined.mp3"
combine_mp3s(sections, output_file)
