"""
Quick and dirty script to make fixtures for the db, first for the Apollo 12 
site. I should really do this using the django models, but I'm in a hurry. 
Probably upgrade it later.
"""

import yaml

lo_imgs = [
'LO_5116_high_res_1_774RE_v1.tif',
'LO_5116_high_res_2_400LE_v1.tif',
'LO_5116_high_res_2_400RE_v1.tif',
'LO_5116_high_res_2_407LE_v1.tif',
'LO_5116_high_res_2_407RE_v1.tif',
'LO_5116_high_res_3_069LE_v1.tif',
'LO_5117_high_res_1_202LE_v1.tif',
'LO_5117_high_res_2_668LE_v1.tif',
'LO_5117_high_res_3_200LE_v1.tif',
'LO_5117_high_res_3_200RE_v1.tif',
'LO_5118_high_res_1_202LE_v1.tif',
'LO_5118_high_res_2_653LE_v1.tif',
'LO_5118_high_res_3_200LE_v1.tif',
'LO_5118_high_res_3_200RE_v1.tif',
'LO_5119_high_res_1_202LE_v1.tif',
'LO_5119_high_res_2_668LE_v1.tif',
'LO_5119_high_res_3_200LE_v1.tif'
]

nac_imgs = [
'NAC_M1114191668LE_5117_2_v1.tif',
'NAC_M1114191668LE_5119_2_v1.tif',
'NAC_M1149530653LE_5118_2_v1.tif',
'NAC_M1238975774RE_5116_1_v1.tif',
'NAC_M1287200400LE_5116_2_v1.tif',
'NAC_M1287200400RE_5116_2_v1.tif',
'NAC_M1293058202LE_5117_1_v1.tif',
'NAC_M1293058202LE_5118_1_v1.tif',
'NAC_M1293058202LE_5119_1_v1.tif',
'NAC_M1300119200LE_5117_3_v1.tif',
'NAC_M1300119200LE_5118_3_v1.tif',
'NAC_M1300119200RE_5117_3_v1.tif',
'NAC_M1300119200RE_5118_3_v1.tif',
'NAC_M181194407LE_5116_2_v1.tif',
'NAC_M181194407RE_5116_2_v1.tif',
'NAC_M188271069LE_5116_3_v1.tif',
'NAC_M1300119200LE_5119_3_v1.tif'
]

def dict_from_loganstyle_lists():
    outdict = {}
    for lo_img in lo_imgs:
        lo_fname_split = lo_img.split('_')
        nac_suffix = lo_fname_split[5]
        lo_setnum = lo_fname_split[1]
        lo_imgnum = lo_fname_split[4]
        for nac_img in nac_imgs:
            nac_fname_split = nac_img.split('_')
            if nac_suffix in nac_img and nac_fname_split[2] == lo_setnum and nac_fname_split[3] == lo_imgnum:
                outdict[lo_img] = nac_img
    return outdict

def moondiff_fixture_from_dict(img_dict, img_first_pid=35,
                               pair_first_pid=19, pairset_pk=3):
    imgpk = img_first_pid
    pairpk = pair_first_pid

    fixtures = []

    fixtures.append(
        {
            'model': 'core.pairset',
            'pk': pairset_pk,
            'fields': {
                'name': 'Alphonsus area',
                'notes': '',
            }
        }
    )

    for oldimg, newimg in img_dict.items():

        oldimg_pk = imgpk
        fixtures.append({
            'model': 'core.image',
            'pk': imgpk,
            'fields': {
                'spacecraft_camera': 1,
                'product_id': oldimg.replace('_cog', '').replace('.tif',
                                                                 '').replace(
                    'LO_', ''),
                'file_data': f'images/{oldimg}'
            }
        })
        imgpk = imgpk + 1

        newimg_pk = imgpk
        if 'RE' in newimg:
            camera_pk = 2
        else:
            camera_pk = 3
        fixtures.append({
            'model': 'core.image',
            'pk': imgpk,
            'fields': {
                'spacecraft_camera': camera_pk,
                'product_id': newimg.replace('.tif', ''),
                'file_data': f'images/{newimg}'
            }
        })
        imgpk = imgpk + 1

        fixtures.append({
            'model': 'core.pair',
            'pk': pairpk,
            'fields': {
                'old_image': oldimg_pk,
                'new_image': newimg_pk,
                'pairset': pairset_pk,
                'coreg_notes': 'Initial tiepoints: Heather Lethcoe, '
                               'Tobey Miner. Coregistration: Tom Logan '
                               '2023.'
            }
        })
        pairpk = pairpk + 1
    return fixtures


with open('alphonsus.yaml', 'w') as fixtures_file:
    img_dict = dict_from_loganstyle_lists()
    yaml.dump(moondiff_fixture_from_dict(img_dict=img_dict), fixtures_file)
