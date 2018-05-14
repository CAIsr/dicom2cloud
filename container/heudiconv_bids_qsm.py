#
import os
def create_key(template, outtype=('nii.gz',), annotation_classes=None):
        if template is None or not template:
                raise ValueError('Template must be a valid format string')
        return template, outtype, annotation_classes
def infotodict(seqinfo):
        outdicom = ('dicom', 'nii.gz')
        mag = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_T1w', outtype=outdicom)
        phs = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_T1map', outtype=outdicom)
        info = {mag: [], phs: [],}
        last_run = len(seqinfo)
        for s in seqinfo:
                if ('mp2rage_highRes_0p5iso_slab_UNI-DEN' in s.series_description):
                        info[t1w] = [s.series_id] # assign if a single series meets criteria
                if ('mp2rage_highRes_0p5iso_slab_UNI_Images' in s.series_description):
                        info[uni] = [s.series_id]
                if ('mp2rage_highRes_0p5iso_slab_INV1' in s.series_description):
                        info[iv1] = [s.series_id]
                if ('mp2rage_highRes_0p5iso_slab_INV2' in s.series_description):
                        info[iv2] = [s.series_id]
                if ('mp2rage_highRes_0p5iso_slab_T1_Images' in s.series_description):
                        info[t1map] = [s.series_id]
                if ('tse_hippo_TraToLongaxis_rep' in s.series_description):
                        info[t2w].append([s.series_id])
                if ('MEAN_Various' in s.series_description):
                        info[t2m] = [s.series_id]
        return info


#commandline: heudiconv -d /data/dumu/barth/7TShare/Data/3_studies/Hippocampus/{subject}/*/*IMA -s {subject} -f /data/dumu/barth/Data/3_studies/Hippocampus/convert_bids_script/heudiconv_file_bids.py -c dcm2niix -b --minmeta -o /winmounts/uqtshaw/uq-research/QSM28SUBJ-Q0530/qsm28subj/data/

