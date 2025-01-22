<div align="center" markdown>
<img src="https://github.com/user-attachments/assets/71d57891-8299-42ae-b007-3bd798624a52">

# View experiment metrics in Tensorboard

<p align="center">
  <a href="#Overview">Overview</a> •
  <a href="#How-To-Use">How To Use</a> •
  <a href="#Acknowledgment">Acknowledgment</a>
</p>

[![](https://img.shields.io/badge/supervisely-ecosystem-brightgreen)](https://ecosystem.supervisely.com)
[![](https://img.shields.io/badge/slack-chat-green.svg?logo=slack)](https://supervisely.com/slack)
![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/supervisely-ecosystem/tensorboard-experiments-viewer)
[![views](https://app.supervisely.com/img/badges/views/supervisely-ecosystem/tensorboard-experiments-viewer.png)](https://supervisely.com)
[![runs](https://app.supervisely.com/img/badges/runs/supervisely-ecosystem/tensorboard-experiments-viewer.png)](https://supervisely.com)

</div>

## Overview

Run Tensorboard from the context menu of `.tfevents.` file, directory or `.json` file in Team Files.

When running app from the context menu of `.json` file, it should include one of the following keys:

- `taskIds`
- `train_task_ids`
- `training_task_ids`
- `trainTaskIds`
- `trainingTaskIds`

The value should be a list of task ids of training sessions that you want to view and compare in Tensorboard.

Example of `.json` file:

```json
{
  "trainingTaskIds": [2315, 2316, 2317]
}
```

# How To Use

1. Run app from the context menu of directory or file in **Team Files** -> `Run app` -> `Tensorboard Experiments Viewer`

2. Wait for the tensorboard server to start. You will see a notification when the server is ready.

3. Stop app manually once you finish with it or it will be stopped automatically after 5 hours.

# Acknowledgment

This app is based on the [Tensorboard](https://github.com/tensorflow/tensorboard) ![GitHub Org's stars](https://img.shields.io/github/stars/tensorflow/tensorboard?style=social) by tensorflow team .
