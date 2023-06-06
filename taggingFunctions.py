import os
import json
from PySide2.QtWidgets import QMessageBox
import tempfile
import shutil
import subprocess
import shlex
import base64
import binascii

##FUNCTIONS BELOW

#Saving tag functions

def collect_tagging_data(video_window_instance):
    # For play_type, we're checking which buttons are checked.
    play_type = {btn: video_window_instance.play_type_selectors[btn].isChecked() for btn in video_window_instance.play_type_selectors}
    
    # For line_rushes, we're getting the current text in each combo box.
    line_rushes = {}
    for rush_type in video_window_instance.line_rush_selectors:
        line_rushes[rush_type] = {rush: video_window_instance.line_rush_selectors[rush_type][rush].currentText() for rush in video_window_instance.line_rush_selectors[rush_type]}
        
    # For strength, we're getting the current text in each combo box and the checked status of each checkbox.
    strength = {}
    for strength_type in video_window_instance.strength_selectors:
        strength[strength_type] = [video_window_instance.strength_selectors[strength_type][0].currentText(), 
                                   video_window_instance.strength_selectors[strength_type][1].isChecked()]
    
    # For scoring chances, we're getting the current text in each combo box.
    scoring_chances = {chance: video_window_instance.scoring_chance_selectors[chance].currentText() for chance in video_window_instance.scoring_chance_selectors}
    
    # For play_attributes, we're checking which checkboxes are checked.
    attributes = {attr: video_window_instance.play_attribute_selectors[attr].isChecked() for attr in video_window_instance.play_attribute_selectors}

    # Combining all data in a single dictionary
    tagging_data = {
        'play_type': play_type,
        'line_rushes': line_rushes,
        'strength': strength,
        'scoring_chances': scoring_chances,
        'attributes': attributes
    }

    return tagging_data

def add_comment_to_video(video_file_path, comment):
    # Create a temporary file in the same directory as the original file
    temp_file = os.path.join(tempfile.gettempdir(), 'temp.mp4')

    # Convert the comment to bytes
    comment_bytes = comment.encode('utf-8')

    # Encode the bytes as a base64 string
    base64_bytes = base64.b64encode(comment_bytes)

    # Convert the base64 bytes back into a string
    base64_comment = base64_bytes.decode('utf-8')

    # Define the command to output a new file
    command = f'ffmpeg -i "{video_file_path}" -metadata comment="{base64_comment}" -c copy "{temp_file}"'

    # Split the command into arguments for subprocess
    args = shlex.split(command)
    
    # Run the command
    subprocess.run(args)

    # Replace the original file with the new file
    shutil.move(temp_file, video_file_path)

def save_tagging_data(video_window_instance, video_file_path):
    # Collect the tagging data
    tagging_data = collect_tagging_data(video_window_instance)

    # If you want to check if a comment exists, add code here
    # Prompt the user for overwrite
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Warning)
    msg.setText("This video file may have tagging data. Do you want to overwrite it?")
    msg.setWindowTitle("Overwrite existing tagging data?")
    msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

    return_value = msg.exec()
    if return_value != QMessageBox.Ok:
        return

    # Save the tagging data to the video
    if save_tagging_data_to_video(video_file_path, tagging_data):
        print("Tagging data saved successfully.")
    else:
        print("Failed to save tagging data.")

def save_tagging_data_to_video(video_file_path, tagging_data):
    # Get the extension of the video file
    file_extension = os.path.splitext(video_file_path)[1].lower()

    # Supported video formats
    supported_formats = ['.mp4', '.mov', '.mkv', '.ts', '.avi']

    if file_extension not in supported_formats:
        raise ValueError(f"Unsupported video format: {file_extension}")

    try:
        # We're going to save the tagging data as a JSON string in the comments field.
        # First, we convert the dictionary to a JSON string.
        json_tagging_data = json.dumps(tagging_data)

        # Then, we add it to the comments field.
        add_comment_to_video(video_file_path, json_tagging_data)

    except Exception as e:
        print(f"An error occurred while trying to save tagging data to the video file: {e}")
        return False

    return True


#Loading tags functions

def load_tags_from_video(video_file_path):
    """
    get a JSON from the comments section of a video file (.mp4)
    """
    # Define the command to read the comment from the video file
    command = f'ffprobe -loglevel error -show_entries format_tags=comment -of default=noprint_wrappers=1:nokey=1 "{video_file_path}"'

    # Split the command into arguments for subprocess
    args = shlex.split(command)

    # Run the command and capture the output
    process = subprocess.run(args, capture_output=True, text=True)

    # Get the output as a string
    base64_comment = process.stdout.strip()

    # If the base64_comment is empty, return None. This way we can set the defaults when there is no tagging meta data present.
    if not base64_comment:
        return None

    try:
        # Convert the base64 string into bytes. If it's not a valid base64 string, this will raise a binascii.Error.
        base64_bytes = base64_comment.encode('utf-8')
        comment_bytes = base64.b64decode(base64_bytes)

        # Convert the bytes back into a string
        comment = comment_bytes.decode('utf-8')

    except binascii.Error:  # This error is raised when the input string cannot be decoded as base64
        # If the comment is not a valid base64 string, we return None,
        # treating this case as if the comments section was empty.
        return None

    try:
        # Try to parse the JSON string into a Python dictionary
        tag_states_json = json.loads(comment)
        return tag_states_json
    except json.JSONDecodeError:
        # If the comment isn't valid JSON, return None
        return None

def set_from_comments(video_window_instance, tag_states_json):
    """
    Update the user interface elements based on the data in the video file's comments.
    
    The argument `tag_states_json` should be a dictionary that maps the user interface elements 
    to the corresponding data in the video file's comments.
    """
    
    # Iterate over the play type buttons and set their state according to the comment data
    for play_type, button in video_window_instance.play_type_selectors.items():
        if play_type in tag_states_json['play_type']:
            button.setChecked(tag_states_json['play_type'][play_type])
            print(f'{play_type} has been set to tag saved state value')
        else:
            button.setChecked(False)

    # Iterate over the line rush selectors and set their state according to the comment data
    for rush_type, rush_dict in video_window_instance.line_rush_selectors.items():
        for rush_is_for, combo in rush_dict.items():
            if rush_type in tag_states_json['line_rushes'] and rush_is_for in tag_states_json['line_rushes'][rush_type]:
                combo.setCurrentText(str(tag_states_json['line_rushes'][rush_type][rush_is_for]))
            else:
                combo.setCurrentText('N/A')

    # Iterate over the strength selectors and set their state according to the comment data
    for strength_of, strength_list in video_window_instance.strength_selectors.items():
        if strength_of in tag_states_json['strength']:
            strength_list[0].setCurrentText(str(tag_states_json['strength'][strength_of][0])) # set the combo box
            strength_list[1].setChecked(tag_states_json['strength'][strength_of][1]) # set the NE checkbox
        else:
            strength_list[0].setCurrentText('N/A') # set default value for the combo box
            strength_list[1].setChecked(False) # set default value for the NE checkbox

    # Iterate over the scoring chance selectors and set their state according to the comment data
    for chance_is, combo in video_window_instance.scoring_chance_selectors.items():
        if chance_is in tag_states_json['scoring_chances']:
            combo.setCurrentText(tag_states_json['scoring_chances'][chance_is])
        else:
            combo.setCurrentText('N/A')

    # Iterate over the play attribute selectors and set their state according to the comment data
    for play_attribute, checkbox in video_window_instance.play_attribute_selectors.items():
        if play_attribute in tag_states_json['attributes']:
            checkbox.setChecked(tag_states_json['attributes'][play_attribute])
        else:
            checkbox.setChecked(False)

    #redraw the window
    video_window_instance.update()





def set_default_tagging_data(video_window_instance):
    """
    Update the user interface elements based on the default data.
    """
    # Iterate over the play type buttons and set their state according to the comment data
    for play_type, button in video_window_instance.play_type_selectors.items():
        button.setChecked(False)
        print(f'play type {play_type} reset ')
       
    # Iterate over the line rush selectors and set their state according to the comment data
    for rush_type, rush_dict in video_window_instance.line_rush_selectors.items():
        for rush_is_for, combo in rush_dict.items():
            combo.setCurrentIndex(0)
            print(f'{rush_type}: {rush_is_for} reset')
            
     # Iterate over the strength selectors and set their state according to the comment data
    for strength_of, strength_list in video_window_instance.strength_selectors.items():
        strength_list[0].setCurrentText('5')
        strength_list[1].setChecked(False)
        print(f'strength - {strength_of}: reset values to {strength_list}')

    # Iterate over the scoring chance selectors and set their state according to the comment data
    for chance_is, combo in video_window_instance.scoring_chance_selectors.items():
        combo.setCurrentText('N/A')
        print(f'{chance_is}: reset')

    # Iterate over the play attribute selectors and set their state according to the comment data
    for play_attribute, checkbox in video_window_instance.play_attribute_selectors.items():
        checkbox.setChecked(False)
        print(f'{play_attribute}: reset')
        
    #redraw the window on change
    video_window_instance.update()
