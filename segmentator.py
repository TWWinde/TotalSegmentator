from totalsegmentator.python_api import totalsegmentator
import os
import nibabel as nib
import numpy as np

classes= {
                    # "0": "background",
                    "1": "spleen",
                    "2": "kidney_right",
                    "3": "kidney_left",
                    "4": "gallbladder",
                    "5": "liver",
                    "6": "stomach",
                    "7": "aorta",
                    "8": "inferior_vena_cava",
                    "9": "portal_vein_and_splenic_vein",
                    "10": "pancreas",
                    "11": "adrenal_gland_right",
                    "12": "adrenal_gland_left",
                    "13": "lung_upper_lobe_left",
                    "14": "lung_lower_lobe_left",
                    "15": "lung_upper_lobe_right",
                    "16": "lung_middle_lobe_right",
                    "17": "lung_lower_lobe_right",
                    "18": "vertebrae_L5",
                    "19": "vertebrae_L4",
                    "20": "vertebrae_L3",
                    "21": "vertebrae_L2",
                    "22": "vertebrae_L1",
                    "23": "vertebrae_T12",
                    "24": "vertebrae_T11",
                    "25": "vertebrae_T10",
                    "26": "vertebrae_T9",
                    "27": "vertebrae_T8",
                    "28": "vertebrae_T7",
                    "29": "vertebrae_T6",
                    "30": "vertebrae_T5",
                    "31": "vertebrae_T4",
                    "32": "vertebrae_T3",
                    "33": "vertebrae_T2",
                    "34": "vertebrae_T1",
                    "35": "vertebrae_C7",
                    "36": "vertebrae_C6",
                    "37": "vertebrae_C5",
                    "38": "vertebrae_C4",
                    "39": "vertebrae_C3",
                    "40": "vertebrae_C2",
                    "41": "vertebrae_C1",
                    "42": "esophagus",
                    "43": "trachea",
                    "44": "heart_myocardium",
                    "45": "heart_atrium_left",
                    "46": "heart_ventricle_left",
                    "47": "heart_atrium_right",
                    "48": "heart_ventricle_right",
                    "49": "pulmonary_artery",
                    "50": "brain",
                    "51": "iliac_artery_left",
                    "52": "iliac_artery_right",
                    "53": "iliac_vena_left",
                    "54": "iliac_vena_right",
                    "55": "small_bowel",
                    "56": "duodenum",
                    "57": "colon",
                    "58": "rib_left_1",
                    "59": "rib_left_2",
                    "60": "rib_left_3",
                    "61": "rib_left_4",
                    "62": "rib_left_5",
                    "63": "rib_left_6",
                    "64": "rib_left_7",
                    "65": "rib_left_8",
                    "66": "rib_left_9",
                    "67": "rib_left_10",
                    "68": "rib_left_11",
                    "69": "rib_left_12",
                    "70": "rib_right_1",
                    "71": "rib_right_2",
                    "72": "rib_right_3",
                    "73": "rib_right_4",
                    "74": "rib_right_5",
                    "75": "rib_right_6",
                    "76": "rib_right_7",
                    "77": "rib_right_8",
                    "78": "rib_right_9",
                    "79": "rib_right_10",
                    "80": "rib_right_11",
                    "81": "rib_right_12",
                    "82": "humerus_left",
                    "83": "humerus_right",
                    "84": "scapula_left",
                    "85": "scapula_right",
                    "86": "clavicula_left",
                    "87": "clavicula_right",
                    "88": "femur_left",
                    "89": "femur_right",
                    "90": "hip_left",
                    "91": "hip_right",
                    "92": "sacrum",
                    "93": "face",
                    "94": "gluteus_maximus_left",
                    "95": "gluteus_maximus_right",
                    "96": "gluteus_medius_left",
                    "97": "gluteus_medius_right",
                    "98": "gluteus_minimus_left",
                    "99": "gluteus_minimus_right",
                    "100": "autochthon_left",
                    "101": "autochthon_right",
                    "102": "iliopsoas_left",
                    "103": "iliopsoas_right",
                    "104": "urinary_bladder",
                    "105": "skin"
}


def combine_labels(label_root_path, classes):
    people_name = os.listdir(label_root_path)
    output_path = os.path.join(label_root_path, 'merged_label')
    pelvis_path = '/data/private/autoPET/Task1/pelvis'
    for item in people_name:
        if item != 'merged_label':
            nii_root_path = os.path.join(label_root_path, item)
            ct = nib.load(os.path.join(pelvis_path, item, 'ct.nii.gz'))
            ct_example = ct.get_fdata()
            ct_affine = ct.affine
            merged_data = np.zeros_like(ct_example)
            for key in classes:
                nii_name = classes[f'{key}'] + '.nii.gz'
                nii_path = os.path.join(nii_root_path, nii_name)
                anatomy = nib.load(nii_path)
                data_anatomy = anatomy.get_fdata()
                merged_data[data_anatomy != 0] = key
            merged_label = nib.Nifti1Image(merged_data, affine=ct_affine)
            nib.save(merged_label, os.path.join(output_path, f'{item}_ct_label.nii.gz'))


def total_segmentor(root_path, output_root_path):
    people_name = os.listdir(root_path)
    for item in people_name:
        if item != 'overview':
            input_path = os.path.join(root_path, item, 'ct.nii.gz')
            output_path = os.path.join(output_root_path, item)
            os.makedirs(output_path, exist_ok=True)
            #totalsegmentator(input_path, output_path, task='body')
            totalsegmentator(input_path, output_path, task='tissue_types', license_number='aca_PNH2NRJCT58HD8')


if __name__ == "__main__":
    root_path = '/data/private/autoPET/Task1/pelvis/'
    output_root_path = '/data/private/autoPET/Task1/ct_label'
    label_root_path = '/data/private/autoPET/Task1/ct_label'
    total_segmentor(root_path, output_root_path)
    #combine_labels(label_root_path, classes)

