import os
import nibabel as nib
import numpy as np
from scipy.ndimage import zoom

def resample_to_1mm(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        
    for patient_folder in os.listdir(input_folder):
        patient_path = os.path.join(input_folder, patient_folder)
        if os.path.isdir(patient_path):
            output_patient_folder = os.path.join(output_folder, patient_folder)
            if not os.path.exists(output_patient_folder):
                os.makedirs(output_patient_folder)
    
            for filename in os.listdir(patient_path):
                if filename.startswith('LT') and filename.endswith('.nii'):
                    input_filepath = os.path.join(patient_path, filename)
                    output_filepath = os.path.join(output_patient_folder, filename)
                    
                    # check if file already exists in output folder
                    if os.path.exists(output_filepath):
                        print(f"Already exists, skipping: {filename}")
                        continue
                    
                    img = nib.load(input_filepath)
                    header = img.header

                    pixel_dims = header.get_zooms()[:3]  # (height, width, slice thickness)
                    print(f"Processing {filename}: pixel dimensions {pixel_dims}")
                    if all(np.isclose(dim, 1.0) for dim in pixel_dims):
                        nib.save(img, output_filepath)
                        print(f"Copied {filename} to {output_filepath} (no resampling needed)")
                    else:
                        zoom_factors = [1.0 / dim for dim in pixel_dims]
                        img_data = img.get_fdata()
                        resampled_data = zoom(img_data, zoom_factors, mode="nearest", order=3)

                        # convert the resampled data to float32 to avoid header issues
                        resampled_data = resampled_data.astype(np.float32)
                        new_affine = img.affine.copy()
                        new_affine[:3, :3] = np.diag([1.0, 1.0, 1.0])
                        new_header = header.copy()
                        new_header.set_data_shape(resampled_data.shape)
                        new_header.set_zooms((1.0, 1.0, 1.0))

                        new_img = nib.Nifti1Image(resampled_data, affine=new_affine, header=new_header)
                        nib.save(new_img, output_filepath)
                        print(f"Resampled {filename} and saved to {output_filepath}")

input_folder = '/projects/b1038/Pulmonary/ksenkow/CLAD_serial_CT/data/2nifti'
output_folder = '/projects/b1038/Pulmonary/ksenkow/CLAD_serial_CT/data/3nifti_standardized'
os.makedirs(output_folder, exist_ok=True)

resample_to_1mm(input_folder, output_folder)