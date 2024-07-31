import os
import nibabel as nib
import numpy as np
from scipy.ndimage import zoom

def resample_to_1mm(input_folder, output_folder):
    for root, dirs, files in os.walk(input_folder):
        for file in files:
            if file.startswith('LT') and file.endswith('.nii'):
                input_path = os.path.join(root, file)
                relative_path = os.path.relpath(root, input_folder)
                output_dir = os.path.join(output_folder, relative_path)
                os.makedirs(output_dir, exist_ok=True)
                output_path = os.path.join(output_dir, file)
                
                img = nib.load(input_path)
                header = img.header
                
                pixel_dims = header.get_zooms()[:3]  # (height, width, slice thickness)
                print(f"Processing {file}: pixel dimensions {pixel_dims}")
                
                if all(np.isclose(dim, 1.0) for dim in pixel_dims):
                    nib.save(img, output_path)
                    print(f"Copied {file} to {output_path} (no resampling needed)")
                else:
                    # calculate zoom factors for resampling
                    zoom_factors = [original / target for original, target in zip(pixel_dims, (1.0, 1.0, 1.0))]
                    img_data = img.get_fdata()
                    resampled_data = zoom(img_data, zoom_factors, mode="nearest", order=3)

                    # adjust affine matrix for new voxel sizes
                    new_affine = np.copy(img.affine)
                    new_affine[:3, :3] *= np.diag([1/factor for factor in zoom_factors])

                    new_img = nib.Nifti1Image(resampled_data, affine=new_affine)
                    new_img.header.set_zooms((1.0, 1.0, 1.0))
                    nib.save(new_img, output_path)
                    print(f"Resampled {file} and saved to {output_path}")

input_folder = '/projects/b1038/Pulmonary/ksenkow/CLAD_serial_CT/data/2nifti'
output_folder = '/projects/b1038/Pulmonary/ksenkow/CLAD_serial_CT/data/3nifti_standardized'

resample_to_1mm(input_folder, output_folder)