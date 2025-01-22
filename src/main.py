import os
import threading
import subprocess
import supervisely as sly
from dotenv import load_dotenv
from pathlib import Path
import supervisely.io.fs as sly_fs
import supervisely.io.json as sly_json
from utils import get_experiment_logs_by_task_ids, download_tf_log_file, download_tf_log_dir

metrics_dir = "/tmp"
if sly.is_development():
    load_dotenv("local.env")
    load_dotenv(os.path.expanduser("~/supervisely.env"))
    # load_dotenv(os.path.expanduser("~/supervisely_demo.env"))
    # load_dotenv(os.path.expanduser("~/supervisely_umar.env"))
    metrics_dir = sly.app.get_data_dir()

team_id = sly.env.team_id()
remote_folder = sly.env.folder(raise_not_found=False)
remote_file = sly.env.file(raise_not_found=False)


api = sly.Api.from_env()

if sly.is_production():
    task_id = sly.env.task_id()
    task_info = api.task.get_info_by_id(task_id)
    session_token = task_info["meta"]["sessionToken"]


if remote_file is not None:
    sly.logger.info(f"File to download: {remote_file}")
    name = sly.fs.get_file_name_with_ext(remote_file)

    # Tensorboard event file
    if ".tfevents." in name:
        download_tf_log_file(api, team_id, metrics_dir, remote_file)

    elif sly_fs.get_file_ext(name) == ".json":
        local_file = os.path.join(metrics_dir, name)
        api.file.download(team_id, remote_file, local_file)
        sly.logger.info(f"File downloaded to: {local_file}")

        file = sly_json.load_json_file(local_file)

        train_task_ids = None
        possible_keys = [
            "taskIds",
            "train_task_ids",
            "training_task_ids",
            "trainTaskIds",
            "trainingTaskIds",
        ]
        for key in possible_keys:
            train_task_ids = file.get(key, None)
            if train_task_ids is not None:
                break
        if train_task_ids is None:
            raise KeyError(
                f"Invalid JSON file. Field with training task ids not found. One of the following keys is expected: {', '.join(possible_keys)}"
            )

        experiment_log_paths = get_experiment_logs_by_task_ids(api, team_id, train_task_ids)
        for remote_log_path in experiment_log_paths:
            try:
                download_tf_log_file(api, team_id, metrics_dir, remote_log_path)
            except Exception as e:
                sly.logger.warning(
                    f"Failed to download file: '{remote_log_path}'. Error: '{repr(e)}'"
                )
    else:
        raise KeyError("Invalid file extension. Only .json and .tfevents files are supported.")

elif remote_folder is not None:
    download_tf_log_dir(api, team_id, metrics_dir, remote_folder)

sly.logger.debug(f"Metrics directory: {metrics_dir}")

args = [
    "tensorboard",
    "--logdir",
    metrics_dir,
    "--host=0.0.0.0",
    "--port=8000",
    "--load_fast=true",
    "--reload_multifile=true",
]
if sly.is_production():
    args.extend(["--path_prefix", f"/net/{session_token}"])

tensorboard_process = subprocess.Popen(args)
sly.logger.info("TensorBoard started. It will auto-terminate after 5 hours.")

# Set task progress
progress = sly.Progress(f"Tensorboard server is ready", total_cnt=1, is_size=False)
progress.iter_done_report()


def kill_tensorboard():
    sly.logger.info("Terminating TensorBoard process after 5 hours...")
    tensorboard_process.terminate()


# Schedule process termination
time_to_terminate = 5 * 60 * 60
auto_kill_timer = threading.Timer(time_to_terminate, kill_tensorboard)
auto_kill_timer.start()

try:
    tensorboard_process.wait()
except KeyboardInterrupt:
    sly.logger.info("Shutting down TensorBoard manually...")
    tensorboard_process.terminate()
    auto_kill_timer.cancel()
