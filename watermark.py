#!/usr/bin/env python3
# ------This only works if selected folder does not contain any files besides image files------
import os
import tkinter as tk
from tkinter import filedialog as fd
from PIL import Image

#Tkinter initializations
window = tk.Tk()
window.title("Watermark")
window.geometry("500x300")
title_row = 0
folder_row = 1
watermark_row = 2
selection_row = 3
intensity_row = 4
final_row = 5
left = 0
center = 1
SIZE_OPTIONS = ["Small","Medium","Large","Full"]
SIZE_OPTIONS_FACTOR = [5,3,1.33,1]
INTENSITY_OPTIONS = ["Heavy", "Light"]
INTENSITY_OPTIONS_FACTOR = [256,50] #Opacity

#Pillow initializations
folder= ""
watermark_path = ""
watermark_position = (0,0)

# ------Tkinter helper functions------
#Folder path for pictures to be processed
def folder_select():
	global folder
	folder_name = fd.askdirectory()
	phrase_display(folder_name,center,folder_row)
	folder = folder_name
	return

#Set full path of watermark image
def watermark_select():
	global watermark_path
	watermark = fd.askopenfilename()
	phrase_display(watermark,center,watermark_row)
	watermark_path = watermark
	return

#Show full paths in Tkinter
def phrase_display(text,column,row):
	phrase = tk.Text(master=window,height = 1, width = 30)
	phrase.grid(column = column, row = row)
	phrase.insert(tk.END, text[-30:])
	phrase.configure(state='disabled')
	return

# ------Pillow Helper Functions------
#Center watermark image
def center_position(x1,x2,y1,y2):
	x = 0
	y = 0
	x = abs(x1 - x2) // 2
	y = abs(y1 - y2) // 2
	return (x, y)

#Create folder for watermarked images if it doesn't exist
def create_watermarked_folder():
	try:
		os.makedirs(folder + "/Watermarked")
	except:
		pass

#Error handler prior to creating watermark
def create_watermark_wrapper():
	try:
		create_watermark()
	except:
		phrase_display("Select folder and watermark.",center,final_row)

#Main function that brings it all together to create watermarks
def create_watermark():
	create_watermarked_folder()
	watermark_image = Image.open(watermark_path)
	watermark_scaler = watermark_scale.get()
	size_choice = SIZE_OPTIONS_FACTOR[SIZE_OPTIONS.index(watermark_scaler)]
	intensity_chooser = intensity_scale.get()
	intensity_choice = INTENSITY_OPTIONS_FACTOR[INTENSITY_OPTIONS.index(intensity_chooser)]

	for item in os.listdir(folder):
		if not item.startswith('.') and os.path.isfile(folder + "/" + item):
			#Prepare image before watermark
			image = Image.open(folder + "/" + item).copy().convert('RGB')
			im_width, im_height = image.size
			wm_width, wm_height = watermark_image.size
			wm_copy = watermark_image.copy()

			#Scaling calculations for watermark
			width_ratio = im_width / wm_width
			height_ratio = im_height / wm_height
			wm_ratio = wm_height / wm_width
			desired__height = im_height / size_choice
			desired_width = im_width / size_choice

			#Scaled width and height for watermark
			if width_ratio < height_ratio:
				wm_width = int(desired_width)
				wm_height = int(wm_width * wm_ratio)
			else:
				wm_height = int(desired__height)
				wm_width = int(wm_height / wm_ratio)
			
			#Apply watermark to new image
			wm_copy = wm_copy.resize((wm_width, wm_height),Image.ANTIALIAS)
			wm_width, wm_height = wm_copy.size
			wm_copy.putalpha(wm_copy.convert('L').point(lambda p: min(p, intensity_choice)))
			watermark_position = center_position(im_width,wm_width,im_height,wm_height)
			image.paste(wm_copy, watermark_position, wm_copy)
			image.save(folder + "/Watermarked/" + item, quality=100)

	phrase_display("Watermark complete.",center,final_row)

# ------Tkinter Components------
#Title
prompt = tk.Label(text="Select folder with images", font = ("Times New Roman",20))
prompt.grid(column=1,row=title_row)

#Button - Folder
folder_button = tk.Button(text="Select folder", command=folder_select)
folder_button.grid(column=left,row=folder_row)
print(folder)

#Button - Watermark
watermark_path_button = tk.Button(text="Select watermark", command=watermark_select)
watermark_path_button.grid(column=left,row=watermark_row)

#Label - Watermark Size
size_list_label = tk.Label(text="Watermark Size", font = ("Times New Roman",14))
size_list_label.grid(column=left,row=selection_row)

#Dropdown Size List
watermark_scale = tk.StringVar(window)
watermark_scale.set(SIZE_OPTIONS[0]) # default value
size_list = tk.OptionMenu(window, watermark_scale, *SIZE_OPTIONS)
size_list.grid(column=center,row=selection_row)

#Label - Watermark Intensity
intensity_label = tk.Label(text="Intensity", font = ("Times New Roman",14))
intensity_label.grid(column=left,row=intensity_row)

#Dropdown Intensity List
intensity_scale = tk.StringVar(window)
intensity_scale.set(INTENSITY_OPTIONS[0]) # default value
intensity_list = tk.OptionMenu(window, intensity_scale, *INTENSITY_OPTIONS)
intensity_list.grid(column=center,row=intensity_row)
	
#Button - Create Watermarks
button3 = tk.Button(text="Watermark Images", command=create_watermark_wrapper)
button3.grid(column=left,row=final_row)

#Run
window.mainloop()
