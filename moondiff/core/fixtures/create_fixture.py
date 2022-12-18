"""
Quick and dirty script to make fixtures for the db, first for the Apollo 12 site. I should really do this using the django models, but I'm in a hurry. Probably upgrade it later.
"""

import yaml

pairs = {
    'LO_3153_HIGH_RES_1_COSMETIC_cog_c1.tif': 'M1108432631RE_3154_1_cog_crop.tif',
    'LO_3153_HIGH_RES_2_COSMETIC_cog_c1.tif': 'M1142596053RE_3153_3_cog_crop.tif',
    'LO_3153_HIGH_RES_3_COSMETIC_cog_c1.tif': 'M1154371500LE_3154_3_cog_crop.tif',
    'LO_3154_HIGH_RES_1_COSMETIC_cog_c1.tif': 'M1154371500RE_3153_2_cog_crop.tif',
    'LO_3154_HIGH_RES_2_COSMETIC_cog_c1.tif': 'M1184980308LE_3154_2_cog_crop.tif',
    'LO_3154_HIGH_RES_3_COSMETIC_cog_c1.tif': 'M1184980308RE_3153_1_cog_crop.tif'
}


def moondiff_fixture_from_dict(img_dict=pairs, img_first_pid=23, pair_first_pid=13, pairset_pk=2):
    imgpk = img_first_pid
    pairpk = pair_first_pid

    fixtures = []

    fixtures.append(
        {
            'model': 'core.pairset',
            'pk': pairset_pk,
            'fields': {
                'name': 'Apollo 12 landing site area',
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
                'product_id': oldimg.replace('_cog','').replace('.tif','').replace('LO_',''),
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
                'product_id': newimg.replace('_cog.tif',''),
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
                'coreg_notes': 'Initial tiepoints: Heather Lethcoe, Tobey Miner. Coregistration: Tom Logan 2022-12-12.'
            }
        })
        pairpk = pairpk + 1
    return fixtures


with open('apollo12.yaml', 'w') as fixtures_file:
    yaml.dump(moondiff_fixture_from_dict(), fixtures_file)