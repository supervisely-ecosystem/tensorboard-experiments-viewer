import os
from pathlib import Path
from typing import List
from supervisely import Api, logger, Progress
import supervisely.io.fs as sly_fs

example_path = "/experiments/<project_id>_<project_name>/<task_id>_<framework_name>/logs/"


def get_experiment_logs_by_task_ids(api: Api, team_id: int, ids: List[int]):
    all_files = api.file.list(team_id, "/experiments", recursive=True, return_type="fileinfo")
    experiment_paths = []
    train_ids = [f"{str(id)}_" for id in ids]
    for file_info in all_files:
        if any([train_id in file_info.path for train_id in train_ids]):
            if ".tfevents." in file_info.path:
                experiment_paths.append(file_info.path)
    return experiment_paths


def download_tf_log_file(api: Api, team_id: int, metrics_dir: str, remote_file: str):
    parts = list(Path(remote_file).parts)
    if len(parts) != 6:
        raise KeyError(
            "Invalid path structure. Experiment not found. Please provide a valid path to file from Team Files 'experiments' folder. "
            f"Example: '{example_path}events.out.tfevents.xxx'"
        )
    experiment_id = parts[3]
    experiment_path = os.path.join(metrics_dir, experiment_id)
    sly_fs.mkdir(experiment_path, True)
    local_file = os.path.join(experiment_path, sly_fs.get_file_name_with_ext(remote_file))
    api.file.download(team_id, remote_file, local_file)
    logger.info(f"File downloaded to: {local_file}")


def download_tf_log_dir(api: Api, team_id: int, metrics_dir: str, remote_folder: str):
    if remote_folder == "/":
        raise KeyError("Permission denied. It is not safe to run app the root directory")
    logger.info(f"Directory to download: {remote_folder}")
    sizeb = api.file.get_directory_size(team_id, remote_folder)
    progress = Progress(f"Downloading metrics from {remote_folder}", total_cnt=sizeb, is_size=True)
    parts = list(Path(remote_folder).parts)
    if len(parts) != 5:
        raise KeyError(
            "Invalid path structure. Experiment not found. Please provide a valid folder from Team Files 'experiments' folder. "
            f"Example: '{example_path}'"
        )

    experiment_id = parts[3]
    experiment_path = os.path.join(metrics_dir, experiment_id)
    sly_fs.mkdir(experiment_path, True)
    api.file.download_directory(team_id, remote_folder, experiment_path, progress.iters_done_report)
    logger.info(f"Folder downloaded to: {experiment_path}")
