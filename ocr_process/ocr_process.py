import easyocr  
import argparse  
import os  
import json  
from decord import VideoReader, cpu  
from multiprocessing import Pool  


def generate_video_json(video_json_dir):           
    video_dir = video_json_dir if os.path.isdir(video_json_dir) else os.path.dirname(video_json_dir)      
    video_dict = {}      
    for root, dirs, files in os.walk(video_dir):      
        video_files = [f for f in files if f.endswith(('.mp4', '.avi', '.mov'))]      
        video_dict.update({os.path.splitext(f)[0]: os.path.join(root, f) for f in video_files})      
    json_file = os.path.join(video_dir, 'without_text.json') if os.path.isdir(video_json_dir) else video_json_dir      
    with open(json_file, 'w') as f:          
        json.dump(video_dict, f, indent=2)        
    print(f'{json_file} already generated')  
  
def process_video(args):  
    name, path = args  
    reader = easyocr.Reader(['ch_sim','en']) # create a reader object in each child process  
    # reader = easyocr.Reader(['ch_sim','en'], gpu=False) # if you don't want to use GPU
    video = VideoReader(path, ctx=cpu(0))    
    total_frames = len(video)    
    frames_to_extract = [total_frames * i // 6 for i in range(6)]    
  
    for frame_num in frames_to_extract:    
        frame = video[frame_num].asnumpy()    
        result = reader.readtext(frame, detail=0)    
        if result:    
            print(f"Deleting {name} due to detected text.")    
            os.remove(path)    
            return False  
    return True  
  
def main(video_json_file):  
    if os.path.isdir(video_json_file) or not os.path.exists(video_json_file):      
        generate_video_json(video_json_file)  
    json_file = os.path.join(video_json_file, 'without_text.json') if os.path.isdir(video_json_file) else video_json_file      
    with open(json_file, 'r') as f:      
        all_mp4_pre = json.load(f)      
    print(f'origin total number is {len(all_mp4_pre)}')  
  
    with Pool() as p:  
        results = p.map(process_video, [(name, path) for name, path in all_mp4_pre.items()])  
  
    remaining_mp4_pre = {name: path for ((name, path), result) in zip(all_mp4_pre.items(), results) if result}   
    
    # write the remaining videos back to the json file  
    with open(json_file, 'w') as f:      
        json.dump(remaining_mp4_pre, f, indent=2)
    print(f"the number without any text is {len(remaining_mp4_pre)}") 
  
if __name__ == "__main__":  
    parser = argparse.ArgumentParser()      
    parser.add_argument('-i', '--video_json_file', help='Path to the input json file, Content is the path to the split video. If you do not have a json file, just pass the path to the video.')      
    args = parser.parse_args()      
    main(args.video_json_file)  
