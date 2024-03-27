import json
import os
import argparse
from glob import glob
from os.path import join as osj
from multiprocessing import Pool

import imageio
import torch
from decord import VideoReader, cpu
from tqdm import tqdm

from opensora.dataset import CenterCropResizeVideo

save_frames = 64 # the number of frames for each splited video 
size = 512
transform = CenterCropResizeVideo(size=size) # crop and resize the video to size*size

def process_video(video_path, save_path):  
    try:  
        decord_vr = VideoReader(video_path, ctx=cpu(0), num_threads=1)  
        total_frames = len(decord_vr)  
  
        video_save_path, filename = os.path.split(video_path)  
        filename = filename[:-4]  
        video_save_path = save_path  
        os.makedirs(video_save_path, exist_ok=True)  
        cnt = 0  
        for i in range(0, total_frames, save_frames):  
            frame_indice = list(range(i, i+save_frames))  
            if frame_indice[-1] >= total_frames:  
                break  
            if os.path.exists(osj(video_save_path, f"{filename}_{cnt:03d}.mp4")):  
                cnt += 1  
                continue  
            video_data = decord_vr.get_batch(frame_indice).asnumpy()  
            video_data = torch.from_numpy(video_data)  
            video_data = video_data.permute(0, 3, 1, 2)  
            video_data = transform(video_data)  
            video = video_data.to(torch.uint8)  
            video = video.permute(0, 2, 3, 1)  
            imageio.mimwrite(osj(video_save_path, f"{filename}_{cnt:03d}.mp4"), video, fps=24, quality=9)  
            cnt += 1  
    except:  
        pass  
  
def generate_video_json(video_json_dir):         
    video_dir = video_json_dir if os.path.isdir(video_json_dir) else os.path.dirname(video_json_dir)    
    video_dict = {}    
    for root, dirs, files in os.walk(video_dir):    
        video_files = [f for f in files if f.endswith(('.mp4', '.avi', '.mov'))]    
        video_dict.update({os.path.splitext(f)[0]: os.path.join(root, f) for f in video_files})    
    json_file = os.path.join(video_dir, 'split.json') if os.path.isdir(video_json_dir) else video_json_dir    
    with open(json_file, 'w') as f:        
        json.dump(video_dict, f, indent=2)      
    print(f'{json_file} already generated')    
  
def main(video_json_file, save_path):    
    if os.path.isdir(video_json_file) or not os.path.exists(video_json_file):    
        generate_video_json(video_json_file)    
    json_file = os.path.join(video_json_file, 'split.json') if os.path.isdir(video_json_file) else video_json_file    
    with open(json_file, 'r') as f:    
        all_mp4_pre = json.load(f)    
    print(f'origin {len(all_mp4_pre)}')    
    for name, path in all_mp4_pre.items():  
        process_video(path, save_path)  
    print('split Done!')    
  
if __name__ == '__main__':    
    parser = argparse.ArgumentParser()    
    parser.add_argument('--video_json_file', help='Path to the input json file, Content is the path to the split video. If you do not have a json file, just pass the path to the video.')    
    parser.add_argument('--save_path', help='Path to save splited files')    
    args = parser.parse_args()    
    main(args.video_json_file, args.save_path)
