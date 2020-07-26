import click
import numpy as np

import core
import cntk
from pathlib import Path

# Uncomment if you want to use CPU forcely
# cntk.try_set_default_device(cntk.device.cpu())


@click.version_option(prog_name='DeepDanbooru-EvalOnly', version='1.0.0')
@click.group()
def main():
    pass


# @main.command('evaluate')
# @click.argument('project_path', type=click.Path(exists=True, resolve_path=True, file_okay=False, dir_okay=True))
# @click.argument('image_path', type=click.Path(exists=True, resolve_path=True, file_okay=True, dir_okay=False))
# @click.option('--threshold', default=0.5, help='Score threshold for result.')



def evaluate_project(project_path, image_path, threshold=0.5): #project_path,
    # project_path='D:\Projects\GitHub\Tens2\danbooru-resnet_custom_v1-p3'
    # print(image_path)
    temp=[None]
    model, tags = core.load_model_and_tags(project_path)

    image = core.load_image_as_hwc(
        image_path, (299, 299))  # resize to 299x299x3
    image = np.ascontiguousarray(np.transpose(
        image, (2, 0, 1)), dtype=np.float32)  # transpose HWC to CHW (3x299x299)

    results = model.eval(image).reshape(tags.shape[0])  # array of tag score

    # for i in range(len(tags)):
    #     if results[i] > threshold:
    #         print(f'{tags[i]},{results[i]}')

    return tags,results


@main.command('evaluate-batch')
@click.argument('project_path', type=click.Path(exists=True, resolve_path=True, file_okay=False, dir_okay=True))
@click.argument('folder_path', type=click.Path(exists=True, resolve_path=True, file_okay=False, dir_okay=True))
@click.option('--threshold', default=0.5, help='Score threshold for result.')
def evaluate_project_batch(project_path, folder_path, threshold):
    model, tags = core.load_model_and_tags(project_path)
    image_path_list = core.get_files_recursively(folder_path)
    
    for image_path in image_path_list:
        print(f'File={image_path}')

        image = core.load_image_as_hwc(
            image_path, (299, 299))  # resize to 299x299x3
        image = np.ascontiguousarray(np.transpose(
            image, (2, 0, 1)), dtype=np.float32)  # transpose HWC to CHW (3x299x299)

        results = model.eval(image).reshape(
            tags.shape[0])  # array of tag score

        # for i in range(len(tags)):
        #     if results[i] > threshold:
        #         print(f'{tags[i]},{results[i]}')


if __name__ == '__main__':
    main()
