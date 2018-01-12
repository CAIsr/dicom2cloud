[![Codacy Badge](https://api.codacy.com/project/badge/Grade/f26b00376cb2407bb1dbd107d8b1c53b)](https://www.codacy.com/app/stebo85/dicom2cloud?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=CAIsr/dicom2cloud&amp;utm_campaign=Badge_Grade)

# Dicom2Cloud - A platform independent graphical user interface for anonymizing and uploading clinical brain scans to an image processing cloud instance

## What is the problem you want to solve?
Current image processing techniques have reached a high level of sophistication and allow the extraction of extensive information from medical imaging data. The problem is that most of these modern post processing techniques are not applied in a clinical setting, because the software developed by scientists is difficult to use, often does not run on operating systems used by clinicians, and requires extensive hardware resources. The integration of new post processing techniques by vendors often takes many years, if the vendors take the risk at all to implement a new technique. One solution to bring modern image processing into the clinic would be to take the medical data outside of the clinic and utilize a powerful cloud instance where all tools are installed and the clinician can upload the data. The problem however is, that medical data contains sensitive information that cannot be easily removed, such as facial features in magnetic resonance imaging data of the brain.

## Why do you want to solve this problem?
Modern image processing algorithms could potentially have a high clinical impact and could help diagnose a variety of diseases, like Multiple sclerosis, Parkinson, and other neurodegenerative diseases. Unfortunately the use of new exciting techniques is currently limited to a few specialized centers where expertise exists to run these algorithms. This severely limits the translation of research into clinics and it often takes years until vendors implement new processing techniques into their clinical platforms.

## What do you envision as the ideal solution for this problem?
The ideal solution would be a platform-independent (win, mac, linux) software/browser plugin that is easy to use, reads standard DICOM data, anonymizes the data and uploads it to a cloud instance and starts the processing. Anonymization of brain scans needs to remove facial features so that patients cannot be re-identified in a 3D rendering of their head. However, it is not possible to simply cut off the area where the face is, as this would affect registration tools by creating artificial edges.

## What sort of Open Source solution do you think can be created in 48 hours, by a small team of developers, designers and data analysts?
A GUI data ingests DICOM data, anonymizes the data and uploads it to a cloud instance.

## What are the current solutions for handling this problem?
Currently no software exists that combines these tasks. Companies provide DICOM uploaders to their clouds (https://www.dicomlibrary.com/, https://boxdicom.com/, https://orca.de.com/orca/) but the security model does not involve proper anonymization. There are open-source projects that upload DICOM images (https://github.com/conorbranagan/dicom-uploader, https://github.com/inodb/dicom-flask-uploader), but de-facing anonymiztion has not been implemented yet. There is a project that provides a de-facing algorithm without cutting off the face (https://github.com/BIC-MNI/EZminc/blob/ITK4/scripts/deface_minipipe.pl) that would work for this kind of data. This tool replaces the patient face with an average face, but has a large amount of software dependencies, which could make an integration challenging.

## Example datasets
https://cloudstor.aarnet.edu.au/plus/index.php/s/d82ybF0SugqBsJp

```bash
  curl -u "d82ybF0SugqBsJp:<password>" "https://cloudstor.aarnet.edu.au/plus/public.php/webdav" -o example.zip

  unzip example.zip
```

interface files for cloud:
https://nextcloud.qriscloud.org.au/index.php/s/AJo9U3Tlf4pLyGl

## Steps that needed to performed on the client side for "Atlas" pipeline
```bash
cd exampleData/7T_mp2rage_Atlasing_sorted/

dcm2mnc GR_IR_M_10_mp2rage-wip900_0.75iso_7T_UNI-DEN/* .


cd test_sb_20150915_105259/
deface_minipipe.pl test_sb_20150915_105259_10_mri.mnc --beastlib /opt/minc/share/beast-library-1.1/ --model-dir /opt/minc/share/icbm152_model_09c/ --model mni_icbm152_t1_tal_nlin_sym_09c defaced.mnc



mincanon brain_defaced.mnc

```
## Steps that needed to performed on the cloud side for "Atlas" pipeline
```bash
mnc2nii brain_defaced.mnc brain_defaced.nii
recon-all -i brain_defaced.nii -subjid your_subject_name
recon-all  -all -subjid your_subject_name
```

## Steps that needed to performed on the client side for "QSM" pipeline one echo
```bash
cd exampleData/3T_multi-echo_QSM_sorted/

dcm2mnc GR_M_12_QSM_p2_1mmIso_TE20/* .
dcm2mnc GR_P_13_QSM_p2_1mmIso_TE20/* .

cd dev_siemens_sb_20170705_134507/
deface_minipipe.pl dev_siemens_sb_20170705_134507_12d1_mri.mnc mag_defaced.mnc

deface_minipipe.pl dev_siemens_sb_20170705_134507_13d1_mri.mnc phs_defaced.mnc

mincanon mag_defaced.mnc
mincanon phs_defaced.mnc
```

## Steps for "QSM" pipeline on the cloud instance
```bash
mnc2nii mag_defaced.mnc mag_defaced.nii
mnc2nii phs_defaced.mnc phs_defaced.nii

bet2 mag_defaced.nii magnitude_bet2

tgv_qsm -p phs_defaced.nii -m magnitude_bet2_mask.nii.gz -f 2.89 -t 0.02 -s -o qsm
```
