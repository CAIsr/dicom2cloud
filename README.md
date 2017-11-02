# Clinic2Cloud - A platform independent graphical user interface for anonymizing and uploading clinical brain scans to an image processing cloud instance

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

## Example pipeline
