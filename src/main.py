import os
import threading
import subprocess
import supervisely as sly
from dotenv import load_dotenv
from pathlib import Path
import supervisely.io.fs as sly_fs

metrics_dir = "/tmp"
if sly.is_development():
    load_dotenv("local.env")
    load_dotenv(os.path.expanduser("~/supervisely.env"))
    metrics_dir = sly.app.get_data_dir()

team_id = sly.env.team_id()
remote_folder = sly.env.folder(raise_not_found=False)
remote_file = sly.env.file(raise_not_found=False)

api = sly.Api.from_env()

example_path = "/experiments/<project_id>_<project_name>/<task_id>_<framework_name>/logs/"

if remote_file is not None:
    sly.logger.info(f"File to download: {remote_file}")
    name = sly.fs.get_file_name_with_ext(remote_file)
    if ".tfevents." not in name:
        raise KeyError(
            f'Extension ".tfevents." not found. File {remote_file} is not metrics for Tensorboard.'
        )

    parts = list(Path(remote_file).parts)
    sly.logger.debug(f"Path parts: {parts}")
    sly.logger.debug(len(parts))
    if len(parts) != 6:
        raise KeyError(
            "Invalid path structure. Experiment not found. Please provide a valid path to file from Team Files 'experiments' folder. "
            f"Example: '{example_path}events.out.tfevents.xxx'"
        )
    experiment_id = parts[3]
    experiment_path = os.path.join(metrics_dir, experiment_id)
    sly_fs.mkdir(experiment_path, True)
    local_file = os.path.join(experiment_path, name)
    api.file.download(team_id, remote_file, local_file)
    sly.logger.info(f"File downloaded to: {local_file}")

elif remote_folder is not None:
    if remote_folder == "/":
        raise KeyError("Permission denied. It is not safe to run app the root directory")
    sly.logger.info(f"Directory to download: {remote_folder}")
    sizeb = api.file.get_directory_size(team_id, remote_folder)
    progress = sly.Progress(
        f"Downloading metrics from {remote_folder}", total_cnt=sizeb, is_size=True
    )
    parts = list(Path(remote_folder).parts)
    sly.logger.debug(f"Path parts: {parts}")
    sly.logger.debug(len(parts))
    if len(parts) != 5:
        raise KeyError(
            "Invalid path structure. Experiment not found. Please provide a valid folder from Team Files 'experiments' folder. "
            f"Example: '{example_path}'"
        )

    experiment_id = parts[3]
    experiment_path = os.path.join(metrics_dir, experiment_id)
    sly_fs.mkdir(experiment_path, True)
    api.file.download_directory(team_id, remote_folder, experiment_path, progress.iters_done_report)
    sly.logger.info(f"Folder downloaded to: {experiment_path}")

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
tensorboard_process = subprocess.Popen(args)
sly.logger.info("TensorBoard started. It will auto-terminate after 5 hours.")

# Set task progress
progress = sly.Progress(f"Tensorboard server is ready.", total_cnt=1, is_size=False)
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
