import os
import nibabel as nib

folder_path = r'/data/ddg9492/code1/jupyter_notebook/lung_upenn/upenn_data/test_1mm'

for filename in os.listdir(folder_path):
    if filename.endswith('.nii.gz'):
        file_path = os.path.join(folder_path, filename)
        try:
            nii = nib.load(file_path)
            sx, sy, sz = nii.header.get_zooms()
            if abs(sx - 1.0) < 1e-10 and abs(sy - 1.0) < 1e-10 and abs(sz - 1.0) < 1e-10:
                print(f"{filename}: Voxel sizes are approximately 1 mm³.")
            else:
                print(f"{filename}: Voxel sizes are not 1 mm³.")
        except Exception as e:
            print(f"Error loading {filename}: {str(e)}")

